#!/usr/bin/env bash
# Branch Management System - Main Interface
# Comprehensive branch management for ProxmoxMCP project

set -euo pipefail

# Source configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/branch-templates/config.sh
source "${SCRIPT_DIR}/config.sh"

# Source the is_protected_branch function from validate.sh
is_protected_branch() {
    local branch_name="$1"

    for protected in "${PROTECTED_BRANCHES[@]}"; do
        if [[ "$branch_name" == "$protected" ]]; then
            return 0
        fi
    done
    return 1
}

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

# Function to check if we're in a git repository
check_git_repo() {
    if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
        print_error "Not in a git repository"
        exit 1
    fi
}

# Function to get current branch
get_current_branch() {
    git rev-parse --abbrev-ref HEAD 2>/dev/null || echo ""
}

# Function to create a new branch with validation
create_branch() {
    local branch_type="$1"
    local component="$2"
    local description="$3"

    # Generate branch name
    local branch_name
    branch_name=$(suggest_branch_name "$branch_type" "$component" "$description")

    print_status "Creating branch: $branch_name"

    # Validate the generated name
    if ! "${SCRIPT_DIR}/validate.sh" --name "$branch_name" >/dev/null 2>&1; then
        print_error "Generated branch name is invalid"
        "${SCRIPT_DIR}/validate.sh" --name "$branch_name"
        return 1
    fi

    # Check if branch already exists
    if git show-ref --verify --quiet "refs/heads/$branch_name"; then
        print_error "Branch $branch_name already exists"
        return 1
    fi

    # Create the branch
    if git checkout -b "$branch_name" 2>/dev/null; then
        print_success "Created and switched to branch: $branch_name"

        # Show next steps
        echo ""
        print_status "Next steps:"
        echo "  1. Make your changes"
        echo "  2. Commit with descriptive messages"
        echo "  3. Push branch: git push -u origin $branch_name"
        echo "  4. Create pull request"

        return 0
    else
        print_error "Failed to create branch"
        return 1
    fi
}

# Function to interactively create a branch
interactive_create() {
    echo ""
    print_status "Interactive Branch Creation"
    echo ""

    # Select branch type
    echo "Select branch type:"
    local types=("$BRANCH_PREFIX_FEATURE" "$BRANCH_PREFIX_FIX" "$BRANCH_PREFIX_SECURITY" \
        "$BRANCH_PREFIX_DOCKER" "$BRANCH_PREFIX_CONFIG" "$BRANCH_PREFIX_DOCS" \
        "$BRANCH_PREFIX_CI" "$BRANCH_PREFIX_PERF")

    for i in "${!types[@]}"; do
        echo "  $((i + 1)). ${types[i]}"
    done
    echo ""

    local type_choice
    read -rp "Enter choice (1-${#types[@]}): " type_choice

    if [[ ! "$type_choice" =~ ^[1-8]$ ]]; then
        print_error "Invalid choice"
        return 1
    fi

    local selected_type="${types[$((type_choice - 1))]}"

    # Select component
    echo ""
    echo "Select component:"
    for i in "${!VALID_COMPONENTS[@]}"; do
        if ((i % 4 == 0)); then
            echo ""
        fi
        printf "  %2d. %-12s" "$((i + 1))" "${VALID_COMPONENTS[i]}"
    done
    echo ""
    echo ""

    local component_choice
    read -rp "Enter choice (1-${#VALID_COMPONENTS[@]}): " component_choice

    if [[ ! "$component_choice" =~ ^[0-9]+$ ]] || \
        ((component_choice < 1 || component_choice > ${#VALID_COMPONENTS[@]})); then
        print_error "Invalid choice"
        return 1
    fi

    local selected_component="${VALID_COMPONENTS[$((component_choice - 1))]}"

    # Get description
    echo ""
    local description
    read -rp "Enter description (e.g., 'timeout-handling', 'new-feature'): " description

    if [[ -z "$description" ]]; then
        print_error "Description is required"
        return 1
    fi

    # Create the branch
    create_branch "$selected_type" "$selected_component" "$description"
}

# Function to list branches with validation status
list_branches() {
    local show_all="${1:-false}"
    local current_branch
    current_branch=$(get_current_branch)

    print_status "Branch Status Report"
    echo ""

    # Get list of branches and remove prefixes in a single `sed` call
    local branches
    if [[ "$show_all" == "true" ]]; then
        branches=$(git branch -a | sed -E 's/^[* ] |remotes\/origin\///g' | sort -u)
    else
        branches=$(git branch | sed 's/^[* ] //' | sort)
    fi

    local valid_count=0
    local invalid_count=0
    local protected_count=0

    while IFS= read -r branch; do
        if [[ -z "$branch" ]] || [[ "$branch" == "HEAD" ]]; then
            continue
        fi

        local status_icon="?"
        local status_color="$COLOR_NC"

        # Check if current branch
        local current_marker=""
        if [[ "$branch" == "$current_branch" ]]; then
            current_marker=" ${COLOR_GREEN}*${COLOR_NC}"
        fi

        # Check if protected
        if is_protected_branch "$branch"; then
            status_icon="🛡️"
            status_color="$COLOR_BLUE"
            ((protected_count++))
        elif "${SCRIPT_DIR}/validate.sh" --name "$branch" >/dev/null 2>&1; then
            status_icon="✅"
            status_color="$COLOR_GREEN"
            ((valid_count++))
        else
            status_icon="❌"
            status_color="$COLOR_RED"
            ((invalid_count++))
        fi

        printf "  %s %s%-50s%s%s\n" "$status_icon" "$status_color" "$branch" "$COLOR_NC" "$current_marker"

    done <<<"$branches"

    # Summary
    echo ""
    print_status "Summary:"
    echo "  ✅ Valid branches: $valid_count"
    echo "  ❌ Invalid branches: $invalid_count"
    echo "  🛡️ Protected branches: $protected_count"

    if ((invalid_count > 0)); then
        echo ""
        print_warning "Some branches don't follow naming conventions"
        print_status "Run 'validate' command to see details"
    fi
}

# Function to cleanup merged branches
cleanup_merged() {
    local dry_run="${1:-false}"
    local default_branch="${DEFAULT_BRANCH}"
    local current_branch
    current_branch=$(get_current_branch)

    print_status "Cleaning up merged branches..."

    # Switch to default branch if not already there
    if [[ "$current_branch" != "$default_branch" ]]; then
        print_status "Switching to $default_branch branch"
        git checkout "$default_branch"
    fi

    # Update default branch
    print_status "Updating $default_branch branch"
    git pull origin "$default_branch"

    # Find merged branches
    local merged_branches
    merged_branches=$(git branch --merged "$default_branch" | grep -v "^\*" | \
        grep -v "^[[:space:]]*$default_branch$" | xargs)

    if [[ -z "$merged_branches" ]]; then
        print_success "No merged branches to clean up"
        return 0
    fi

    echo ""
    print_status "Merged branches found:"
    for branch in $merged_branches; do
        # Skip protected branches
        if is_protected_branch "$branch"; then
            continue
        fi
        echo "  - $branch"
    done

    if [[ "$dry_run" == "true" ]]; then
        print_status "Dry run mode - no branches deleted"
        return 0
    fi

    echo ""
    read -rp "Delete these merged branches? (y/N): " confirm

    if [[ "$confirm" =~ ^[Yy]$ ]]; then
        for branch in $merged_branches; do
            if ! is_protected_branch "$branch"; then
                if git branch -d "$branch" 2>/dev/null; then
                    print_success "Deleted branch: $branch"
                else
                    print_warning "Could not delete branch: $branch"
                fi
            fi
        done
    else
        print_status "Branch cleanup cancelled"
    fi
}

# Function to show help
show_help() {
    cat <<EOF
Branch Management System for ProxmoxMCP

Usage: $0 <command> [options]

COMMANDS:
    create          Create a new branch interactively
    validate        Validate current branch or all branches
    list            List all branches with validation status
    cleanup         Clean up merged branches
    help            Show this help message

OPTIONS:
    --all           Include remote branches (for list command)
    --dry-run       Show what would be deleted (for cleanup command)

EXAMPLES:
    $0 create                      # Interactive branch creation
    $0 validate                    # Validate current branch
    $0 list                        # List local branches
    $0 list --all                  # List all branches
    $0 cleanup                     # Clean up merged branches
    $0 cleanup --dry-run           # Show what would be cleaned up

BRANCH NAMING CONVENTIONS:
    Format: <type>/<component>-<description>
    
    Types:
      - feature   : New features
      - fix       : Bug fixes
      - security  : Security improvements
      - docker    : Container updates
      - config    : Configuration changes
      - docs      : Documentation
      - ci        : CI/CD changes
      - perf      : Performance improvements
    
    Components:
      vm, container, storage, network, backup, auth, encryption,
      config, api, mcp, core, tools, formatting, docker, proxmox,
      console, management

EOF
}

# Main function
main() {
    check_git_repo

    local command="${1:-help}"
    shift || true

    case "$command" in
    create | c)
        interactive_create
        ;;
    validate | v)
        "${SCRIPT_DIR}/validate.sh" --current
        ;;
    list | l)
        local show_all=false
        if [[ "${1:-}" == "--all" ]]; then
            show_all=true
        fi
        list_branches "$show_all"
        ;;
    cleanup | clean)
        local dry_run=false
        if [[ "${1:-}" == "--dry-run" ]]; then
            dry_run=true
        fi
        cleanup_merged "$dry_run"
        ;;
    help | h | --help | -h)
        show_help
        ;;
    *)
        print_error "Unknown command: $command"
        echo ""
        show_help
        exit 1
        ;;
    esac
}

# Run main function
main "$@"
