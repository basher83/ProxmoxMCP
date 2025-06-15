#!/usr/bin/env bash
# Branch Management System Validator
# Validates branch names according to ProxmoxMCP conventions

set -euo pipefail

# Source configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/branch-templates/config.sh
source "${SCRIPT_DIR}/config.sh"

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
        echo "  - ${BRANCH_PREFIX_FEATURE}/"
        echo "  - ${BRANCH_PREFIX_FIX}/"
        echo "  - ${BRANCH_PREFIX_SECURITY}/"
        echo "  - ${BRANCH_PREFIX_DOCKER}/"
        echo "  - ${BRANCH_PREFIX_CONFIG}/"
        echo "  - ${BRANCH_PREFIX_DOCS}/"
        echo "  - ${BRANCH_PREFIX_CI}/"
        echo "  - ${BRANCH_PREFIX_PERF}/"
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
    if [[ "$branch_name" == "${BRANCH_PREFIX_FEATURE}/"* ]]; then
        prefix_pattern="${BRANCH_PREFIX_FEATURE}/"
    elif [[ "$branch_name" == "${BRANCH_PREFIX_FIX}/"* ]]; then
        prefix_pattern="${BRANCH_PREFIX_FIX}/"
    elif [[ "$branch_name" == "${BRANCH_PREFIX_SECURITY}/"* ]]; then
        prefix_pattern="${BRANCH_PREFIX_SECURITY}/"
    elif [[ "$branch_name" == "${BRANCH_PREFIX_DOCKER}/"* ]]; then
        prefix_pattern="${BRANCH_PREFIX_DOCKER}/"
    elif [[ "$branch_name" == "${BRANCH_PREFIX_CONFIG}/"* ]]; then
        prefix_pattern="${BRANCH_PREFIX_CONFIG}/"
    elif [[ "$branch_name" == "${BRANCH_PREFIX_DOCS}/"* ]]; then
        prefix_pattern="${BRANCH_PREFIX_DOCS}/"
    elif [[ "$branch_name" == "${BRANCH_PREFIX_CI}/"* ]]; then
        prefix_pattern="${BRANCH_PREFIX_CI}/"
    elif [[ "$branch_name" == "${BRANCH_PREFIX_PERF}/"* ]]; then
        prefix_pattern="${BRANCH_PREFIX_PERF}/"
    fi
    
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
    # Use parameter expansion instead of sed (addresses SC2001)
    local name_without_prefix="${branch_name#*/}"  # Remove type prefix
    local name_without_component="${name_without_prefix#*-}"  # Remove first component
    
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
    
    # Use parameter expansion for character validation (addresses SC2001)
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
        print_warning "You are on protected branch: $current_branch"
        return 0
    fi
    
    print_status "Validating current branch: $current_branch"
    validate_branch_name "$current_branch"
}

# Function to validate a specific branch name
validate_branch_name() {
    local branch_name="$1"
    local validation_passed=true
    
    print_status "Validating branch name: $branch_name"
    echo ""
    
    # Run all validations
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
        print_success "Branch name is valid! ✨"
        return 0
    else
        print_error "Branch name validation failed"
        
        # Suggest a corrected name
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
    
    # Use parameter expansion to clean the name (addresses SC2001)
    local clean_name="${branch_name,,}"  # lowercase
    clean_name="${clean_name//[^a-z0-9]/-}"  # replace non-alphanumeric with hyphens
    clean_name="${clean_name//--/-}"  # replace double hyphens
    clean_name="${clean_name#-}"  # remove leading hyphen
    clean_name="${clean_name%-}"  # remove trailing hyphen
    
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
}

# Function to show help
show_help() {
    cat << EOF
Branch Management System Validator

Usage: $0 [OPTIONS] [BRANCH_NAME]

OPTIONS:
    --current, -c       Validate current branch
    --name, -n NAME     Validate specific branch name
    --help, -h          Show this help message

EXAMPLES:
    $0 --current                    # Validate current branch
    $0 --name feature/vm-console    # Validate specific branch name
    $0 feature/api-enhancement      # Validate branch name (positional)

BRANCH NAMING CONVENTIONS:
    Format: <type>/<component>-<description>
    
    Types: ${BRANCH_PREFIX_FEATURE}, ${BRANCH_PREFIX_FIX}, ${BRANCH_PREFIX_SECURITY}, ${BRANCH_PREFIX_DOCKER}, etc.
    Components: vm, api, config, docker, proxmox, etc.
    
    Examples:
    - ${BRANCH_PREFIX_FEATURE}/vm-console-management
    - ${BRANCH_PREFIX_FIX}/api-timeout-handling
    - ${BRANCH_PREFIX_SECURITY}/encryption-key-rotation

EOF
}

# Main function
main() {
    local action="help"
    local branch_name=""
    
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --current|-c)
                action="current"
                shift
                ;;
            --name|-n)
                action="validate"
                branch_name="$2"
                shift 2
                ;;
            --help|-h)
                show_help
                exit 0
                ;;
            -*)
                print_error "Unknown option: $1"
                show_help
                exit 1
                ;;
            *)
                # Positional argument - treat as branch name
                action="validate"
                branch_name="$1"
                shift
                ;;
        esac
    done
    
    # Execute the requested action
    case $action in
        current)
            validate_current_branch
            ;;
        validate)
            if [[ -z "$branch_name" ]]; then
                print_error "Branch name is required"
                show_help
                exit 1
            fi
            validate_branch_name "$branch_name"
            ;;
        *)
            show_help
            exit 0
            ;;
    esac
}

# Run main function
main "$@"