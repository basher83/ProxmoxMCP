#!/bin/bash

# ProxmoxMCP Branch Creation Script
# Creates branches following the established branching strategy
# Usage: ./create-branch.sh <type> <description> [issue-number]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
MAIN_BRANCH="main"
REMOTE="origin"

# Functions
print_usage() {
    echo -e "${BLUE}ProxmoxMCP Branch Creation Tool${NC}"
    echo
    echo "Usage: $0 <type> <description> [issue-number]"
    echo
    echo "Branch Types:"
    echo "  feature    - New feature development (feature/123-description)"
    echo "  fix        - Bug fixes (fix/123-description)"
    echo "  security   - Security-related changes (security/description)"
    echo "  chore      - Maintenance tasks (chore/description)"
    echo "  release    - Release preparation (release/v1.0.0)"
    echo "  hotfix     - Critical production fixes (hotfix/description)"
    echo
    echo "Examples:"
    echo "  $0 feature 'add-vm-monitoring-tools' 123"
    echo "  $0 fix 'memory-leak-connection-pool' 58"
    echo "  $0 security 'fix-shell-injection'"
    echo "  $0 chore 'update-documentation'"
    echo "  $0 release 'v1.0.0'"
    echo "  $0 hotfix 'critical-security-patch'"
    echo
}

validate_inputs() {
    if [ $# -lt 2 ]; then
        echo -e "${RED}Error: Missing required arguments${NC}"
        print_usage
        exit 1
    fi

    TYPE=$1
    DESCRIPTION=$2
    ISSUE_NUMBER=$3

    # Validate branch type
    case $TYPE in
        feature|fix|security|chore|release|hotfix)
            ;;
        *)
            echo -e "${RED}Error: Invalid branch type '$TYPE'${NC}"
            print_usage
            exit 1
            ;;
    esac

    # Validate description
    if [[ -z "$DESCRIPTION" ]]; then
        echo -e "${RED}Error: Description cannot be empty${NC}"
        exit 1
    fi

    # Clean description (replace spaces with hyphens, lowercase, remove special chars)
    CLEAN_DESCRIPTION=$(echo "$DESCRIPTION" | tr '[:upper:]' '[:lower:]' | \
        sed 's/[^a-z0-9-]/-/g' | sed 's/--*/-/g' | sed 's/^-\|-$//g')
}

check_git_status() {
    # Check if we're in a git repository
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        echo -e "${RED}Error: Not in a git repository${NC}"
        exit 1
    fi

    # Check if main branch exists
    if ! git show-ref --verify --quiet refs/heads/$MAIN_BRANCH; then
        echo -e "${RED}Error: Main branch '$MAIN_BRANCH' not found${NC}"
        exit 1
    fi

    # Check for uncommitted changes
    if ! git diff-index --quiet HEAD --; then
        echo -e "${YELLOW}Warning: You have uncommitted changes${NC}"
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

update_main_branch() {
    echo -e "${BLUE}Updating main branch...${NC}"

    # Switch to main and pull latest
    git checkout $MAIN_BRANCH
    git pull $REMOTE $MAIN_BRANCH

    echo -e "${GREEN}Main branch updated${NC}"
}

create_branch_name() {
    case $TYPE in
        feature|fix)
            if [[ -n "$ISSUE_NUMBER" ]]; then
                BRANCH_NAME="${TYPE}/${ISSUE_NUMBER}-${CLEAN_DESCRIPTION}"
            else
                BRANCH_NAME="${TYPE}/${CLEAN_DESCRIPTION}"
            fi
            ;;
        security|chore|hotfix)
            BRANCH_NAME="${TYPE}/${CLEAN_DESCRIPTION}"
            ;;
        release)
            # For releases, description should be version number
            if [[ ! "$CLEAN_DESCRIPTION" =~ ^v?[0-9]+\.[0-9]+\.[0-9]+(-.*)?$ ]]; then
                echo -e "${YELLOW}Warning: Release description should be a version number (e.g., v1.0.0)${NC}"
            fi
            BRANCH_NAME="${TYPE}/${CLEAN_DESCRIPTION}"
            ;;
    esac
}

create_and_setup_branch() {
    echo -e "${BLUE}Creating branch: ${BRANCH_NAME}${NC}"

    # Create and checkout new branch
    git checkout -b "$BRANCH_NAME"

    # Push branch to remote
    git push -u $REMOTE "$BRANCH_NAME"

    echo -e "${GREEN}Branch created and pushed successfully!${NC}"
}

show_next_steps() {
    echo
    echo -e "${BLUE}Next Steps:${NC}"
    echo "1. Make your changes and commit them"
    echo "2. Push commits to the branch"
    echo "3. Create a Pull Request when ready"
    echo

    # Branch-specific guidance
    case $TYPE in
        feature)
            echo -e "${BLUE}Feature Branch Guidelines:${NC}"
            echo "• Link to issue #$ISSUE_NUMBER in commits and PR"
            echo "• Ensure adequate test coverage"
            echo "• Update documentation if needed"
            echo "• Use commit format: 'feat: description'"
            ;;
        fix)
            echo -e "${BLUE}Fix Branch Guidelines:${NC}"
            echo "• Reference issue #$ISSUE_NUMBER if applicable"
            echo "• Include test to prevent regression"
            echo "• Use commit format: 'fix: description'"
            ;;
        security)
            echo -e "${BLUE}Security Branch Guidelines:${NC}"
            echo "• Follow security review process"
            echo "• Update SECURITY.md if needed"
            echo "• Use commit format: 'security: description'"
            ;;
        hotfix)
            echo -e "${BLUE}Hotfix Branch Guidelines:${NC}"
            echo "• Make minimal, focused changes"
            echo "• Request expedited review"
            echo "• Use commit format: 'hotfix: description'"
            ;;
        release)
            echo -e "${BLUE}Release Branch Guidelines:${NC}"
            echo "• Update version numbers"
            echo "• Finalize release notes"
            echo "• Update documentation"
            echo "• Tag release after merge"
            ;;
        chore)
            echo -e "${BLUE}Chore Branch Guidelines:${NC}"
            echo "• Focus on maintenance tasks"
            echo "• Update dependencies if applicable"
            echo "• Use commit format: 'chore: description'"
            ;;
    esac

    echo
    echo -e "${YELLOW}Useful Commands:${NC}"
    echo "  git commit -m 'type: description'   # Commit changes"
    echo "  git push                            # Push commits"
    echo "  gh pr create                        # Create PR (if GitHub CLI installed)"
    echo
}

# Main execution
main() {
    validate_inputs "$@"
    check_git_status
    update_main_branch
    create_branch_name
    create_and_setup_branch
    show_next_steps
}

# Check if script is being sourced or executed
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
