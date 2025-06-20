#!/bin/bash
# Branch Management System Validator
# Validates branch names according to ProxmoxMCP conventions

set -euo pipefail

# Source configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/branch-templates/config.sh
source "${SCRIPT_DIR}/config.sh"

# Legacy branch name patterns for backward compatibility
FEATURE_PATTERN="^feature/([0-9]+-)?[a-z0-9-]+$"
FIX_PATTERN="^fix/([0-9]+-)?[a-z0-9-]+$"
SECURITY_PATTERN="^security/[a-z0-9-]+$"
CHORE_PATTERN="^chore/[a-z0-9-]+$"
RELEASE_PATTERN="^release/v?[0-9]+\.[0-9]+\.[0-9]+(-.*)?$"
HOTFIX_PATTERN="^hotfix/[a-z0-9-]+$"
CLAUDE_PATTERN="^claude/issue-[0-9]+-[a-z0-9-]+$"

# Function to print colored output
print_status() {
    echo -e "${COLOR_BLUE}[INFO]${COLOR_NC} $1"
}

print_success() {
    echo -e "${COLOR_GREEN}[SUCCESS]${COLOR_NC} $1"
}

print_warning() {
    echo -e "${COLOR_YELLOW}[WARNING]${COLOR_NC} $1"
}

print_error() {
    echo -e "${COLOR_RED}[ERROR]${COLOR_NC} $1"
}

# Legacy pattern-based validation (for backward compatibility)
validate_legacy_patterns() {
    local branch_name="$1"

    # Check against legacy patterns
    if [[ $branch_name =~ $FEATURE_PATTERN ]] ||
        [[ $branch_name =~ $FIX_PATTERN ]] ||
        [[ $branch_name =~ $SECURITY_PATTERN ]] ||
        [[ $branch_name =~ $CHORE_PATTERN ]] ||
        [[ $branch_name =~ $RELEASE_PATTERN ]] ||
        [[ $branch_name =~ $HOTFIX_PATTERN ]] ||
        [[ $branch_name =~ $CLAUDE_PATTERN ]]; then
        return 0
    fi
    return 1
}

# Function to validate branch name length
validate_length() {
    local branch_name="$1"
    local length=${#branch_name}

    if [[ $length -lt $MIN_BRANCH_NAME_LENGTH ]]; then
        print_error "Branch name too short (${length} chars). Minimum: ${MIN_BRANCH_NAME_LENGTH}"
        return 1
    fi

    if [[ $length -gt $MAX_BRANCH_NAME_LENGTH ]]; then
        print_error "Branch name too long (${length} chars). Maximum: ${MAX_BRANCH_NAME_LENGTH}"
        return 1
    fi

    return 0
}

# Function to validate branch prefix
validate_prefix() {
    local branch_name="$1"

    if ! is_valid_branch_prefix "$branch_name"; then
        print_error "Invalid branch prefix. Valid prefixes are:"
        local valid_prefixes=("$BRANCH_PREFIX_FEATURE" "$BRANCH_PREFIX_FIX" \
            "$BRANCH_PREFIX_SECURITY" "$BRANCH_PREFIX_DOCKER" \
            "$BRANCH_PREFIX_CONFIG" "$BRANCH_PREFIX_DOCS" \
            "$BRANCH_PREFIX_CI" "$BRANCH_PREFIX_PERF")
        for prefix in "${valid_prefixes[@]}"; do
            echo "  - ${prefix}/"
        done
        return 1
    fi

    return 0
}

# Function to validate component in branch name
validate_component() {
    local branch_name="$1"

    if [[ "$REQUIRE_COMPONENT_IN_NAME" != "true" ]]; then
        return 0
    fi

    # Extract the part after the prefix
    local prefix_pattern=""
    local valid_prefixes=("$BRANCH_PREFIX_FEATURE" "$BRANCH_PREFIX_FIX" \
        "$BRANCH_PREFIX_SECURITY" "$BRANCH_PREFIX_DOCKER" \
        "$BRANCH_PREFIX_CONFIG" "$BRANCH_PREFIX_DOCS" \
        "$BRANCH_PREFIX_CI" "$BRANCH_PREFIX_PERF")

    for prefix in "${valid_prefixes[@]}"; do
        if [[ "$branch_name" == "${prefix}/"* ]]; then
            prefix_pattern="${prefix}/"
            break
        fi
    done

    # Remove prefix to get the component part
    local component_part="${branch_name#$prefix_pattern}"

    # Extract first component (everything before first hyphen)
    local first_component="${component_part%%-*}"

    # Check if the first component is valid
    local found_valid_component=false
    for component in "${VALID_COMPONENTS[@]}"; do
        if [[ "$first_component" == "$component" ]]; then
            found_valid_component=true
            break
        fi
    done

    if [[ "$found_valid_component" != "true" ]]; then
        print_error "Branch name should include a valid component. Valid components:"
        printf "  - %s\n" "${VALID_COMPONENTS[@]}"
        return 1
    fi

    return 0
}

# Function to validate descriptive suffix
validate_description() {
    local branch_name="$1"

    if [[ "$REQUIRE_DESCRIPTIVE_SUFFIX" != "true" ]]; then
        return 0
    fi

    # Check if branch name has meaningful description after component
    local name_without_prefix="${branch_name#*/}"            # Remove type prefix
    local name_without_component="${name_without_prefix#*-}" # Remove first component

    # Check if there's a descriptive part after the component
    if [[ -z "$name_without_component" ]] || [[ "$name_without_component" == "$name_without_prefix" ]]; then
        print_error "Branch name should include a descriptive suffix after the component"
        print_status "Example: ${BRANCH_PREFIX_FEATURE}/vm-console-management"
        return 1
    fi

    # Check for minimal description length (at least 3 characters)
    if [[ ${#name_without_component} -lt 3 ]]; then
        print_error "Descriptive suffix too short. Should be at least 3 characters."
        return 1
    fi

    return 0
}

# Function to validate special characters
validate_characters() {
    local branch_name="$1"

    # Check for invalid characters - anything not alphanumeric, hyphen, or slash
    local cleaned_name="${branch_name//[a-zA-Z0-9\/-]/}"

    if [[ -n "$cleaned_name" ]]; then
        print_error "Branch name contains invalid characters: '$cleaned_name'"
        print_status "Only letters, numbers, hyphens, and forward slashes are allowed"
        return 1
    fi

    # Check for consecutive hyphens or hyphens at start/end of segments
    if [[ "$branch_name" =~ --+ ]] || [[ "$branch_name" =~ /-/ ]] || [[ "$branch_name" =~ -$ ]]; then
        print_error "Branch name has invalid hyphen usage (consecutive, leading, or trailing hyphens)"
        return 1
    fi

    return 0
}

# Function to check if branch is protected
is_protected_branch() {
    local branch_name="$1"

    # Remove origin/ prefix if present
    branch_name=${branch_name#origin/}

    # Check main/development branches
    if [[ "$branch_name" == "main" || "$branch_name" == "master" || "$branch_name" == "develop" ]]; then
        return 0
    fi

    for protected in "${PROTECTED_BRANCHES[@]}"; do
        if [[ "$branch_name" == "$protected" ]]; then
            return 0
        fi
    done
    return 1
}

# Function to validate current branch
validate_current_branch() {
    local current_branch
    current_branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "")

    if [[ -z "$current_branch" ]]; then
        print_error "Not in a git repository or unable to determine current branch"
        return 1
    fi

    if is_protected_branch "$current_branch"; then
        print_success "✅ ${current_branch} - Main/development branch"
        return 0
    fi

    print_status "Validating current branch: $current_branch"
    validate_branch_name "$current_branch"
}

# Function to validate a specific branch name
validate_branch_name() {
    local branch_name="$1"
    local validation_passed=true

    # Remove origin/ prefix if present
    branch_name=${branch_name#origin/}

    # Skip protected branches
    if is_protected_branch "$branch_name"; then
        print_success "✅ ${branch_name} - Protected branch"
        return 0
    fi

    print_status "Validating branch name: $branch_name"
    echo ""

    # First try legacy pattern validation for backward compatibility
    if validate_legacy_patterns "$branch_name"; then
        print_success "✅ ${branch_name} - Valid (legacy pattern)"
        return 0
    fi

    # Run comprehensive validations
    if ! validate_length "$branch_name"; then
        validation_passed=false
    fi

    if ! validate_prefix "$branch_name"; then
        validation_passed=false
    fi

    if ! validate_component "$branch_name"; then
        validation_passed=false
    fi

    if ! validate_description "$branch_name"; then
        validation_passed=false
    fi

    if ! validate_characters "$branch_name"; then
        validation_passed=false
    fi

    echo ""
    if [[ "$validation_passed" == "true" ]]; then
        print_success "✅ ${branch_name} - Valid branch name ✨"
        return 0
    else
        print_error "❌ ${branch_name} - Branch name validation failed"
        suggest_corrections "$branch_name"
        return 1
    fi
}

# Function to suggest corrections for invalid branch names
suggest_corrections() {
    local branch_name="$1"

    print_status "Suggestions for improvement:"

    # Try to extract meaningful parts and suggest a better name
    local suggested_type="${BRANCH_PREFIX_FEATURE}"
    local suggested_component="core"
    local suggested_description="update"

    # Clean the name
    local clean_name="${branch_name,,}"     # lowercase
    clean_name="${clean_name//[^a-z0-9]/-}" # replace non-alphanumeric with hyphens
    clean_name="${clean_name//--/-}"        # replace double hyphens
    clean_name="${clean_name#-}"            # remove leading hyphen
    clean_name="${clean_name%-}"            # remove trailing hyphen

    # Check if any valid components are mentioned in the name
    for component in "${VALID_COMPONENTS[@]}"; do
        if [[ "$clean_name" == *"$component"* ]]; then
            suggested_component="$component"
            break
        fi
    done

    local suggestion
    suggestion=$(suggest_branch_name "$suggested_type" "$suggested_component" "$suggested_description")

    echo "  Example: $suggestion"
    echo "  Format: <type>/<component>-<description>"
    echo ""
    echo "  Legacy patterns also supported:"
    echo "    feature/[issue-]description  (e.g., feature/123-add-monitoring)"
    echo "    fix/[issue-]description      (e.g., fix/58-memory-leak)"
    echo "    security/description         (e.g., security/fix-injection)"
    echo ""
}

get_current_branch() {
    git rev-parse --abbrev-ref HEAD 2>/dev/null || {
        print_error "Not in a git repository"
        exit 1
    }
}

check_all_branches() {
    print_status "Validating all local branches..."
    echo

    local all_valid=true
    local branches
    branches=$(git branch --format='%(refname:short)' | grep -v '^remotes/')

    while IFS= read -r branch; do
        if ! validate_branch_name "$branch"; then
            all_valid=false
        fi
    done <<<"$branches"

    echo
    if $all_valid; then
        print_success "🎉 All branches follow naming conventions!"
        return 0
    else
        print_error "⚠️  Some branches don't follow naming conventions"
        print_warning "Use the branch creation scripts to ensure proper naming"
        return 1
    fi
}

# Function to show help
show_help() {
    cat <<EOF
Branch Management System Validator

Usage: $0 [OPTIONS] [BRANCH_NAME]

OPTIONS:
    --current, -c       Validate current branch
    --name, -n NAME     Validate specific branch name
    --check-all         Validate all local branches
    --help, -h          Show this help message

EXAMPLES:
    $0                              # Validate current branch
    $0 --current                    # Validate current branch
    $0 --name feature/vm-console    # Validate specific branch name
    $0 feature/api-enhancement      # Validate branch name (positional)
    $0 --check-all                  # Validate all local branches

BRANCH NAMING CONVENTIONS:
    Modern format: <type>/<component>-<description>
    Legacy format: <type>/[issue-]<description>

    Types: ${BRANCH_PREFIX_FEATURE}, ${BRANCH_PREFIX_FIX}, ${BRANCH_PREFIX_SECURITY}, ${BRANCH_PREFIX_DOCKER}, etc.
    Components: vm, api, config, docker, proxmox, etc.

    Examples:
    - ${BRANCH_PREFIX_FEATURE}/vm-console-management
    - ${BRANCH_PREFIX_FIX}/api-timeout-handling
    - ${BRANCH_PREFIX_SECURITY}/encryption-key-rotation
    - feature/123-add-monitoring (legacy)
EOF
}

main() {
    if [[ $# -eq 0 ]]; then
        validate_current_branch
    elif [[ "$1" == "--check-all" ]]; then
        check_all_branches
    elif [[ "$1" == "--current" || "$1" == "-c" ]]; then
        validate_current_branch
    elif [[ "$1" == "--name" || "$1" == "-n" ]]; then
        if [[ $# -lt 2 ]]; then
            print_error "Branch name required with --name option"
            exit 1
        fi
        validate_branch_name "$2"
    elif [[ "$1" == "-h" || "$1" == "--help" ]]; then
        show_help
    else
        # Validate specific branch (positional argument)
        validate_branch_name "$1"
    fi
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
