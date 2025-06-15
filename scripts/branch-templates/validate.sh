#!/bin/bash

# Branch Validation Script for ProxmoxMCP
# Validates branch names against established conventions

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Branch name patterns
FEATURE_PATTERN="^feature/([0-9]+-)?[a-z0-9-]+$"
FIX_PATTERN="^fix/([0-9]+-)?[a-z0-9-]+$"
SECURITY_PATTERN="^security/[a-z0-9-]+$"
CHORE_PATTERN="^chore/[a-z0-9-]+$"
RELEASE_PATTERN="^release/v?[0-9]+\.[0-9]+\.[0-9]+(-.*)?$"
HOTFIX_PATTERN="^hotfix/[a-z0-9-]+$"
CLAUDE_PATTERN="^claude/issue-[0-9]+-[a-z0-9-]+$"

print_usage() {
    echo -e "${BLUE}ProxmoxMCP Branch Validation Tool${NC}"
    echo
    echo "Usage: $0 [branch-name]"
    echo
    echo "If no branch name is provided, validates the current branch."
    echo
    echo "Examples:"
    echo "  $0                                    # Validate current branch"
    echo "  $0 feature/123-add-monitoring        # Validate specific branch"
    echo "  $0 --check-all                       # Validate all local branches"
    echo
}

validate_branch_name() {
    local branch_name="$1"
    local is_valid=false
    local branch_type=""
    local suggestions=""

    # Remove origin/ prefix if present
    branch_name=$(echo "$branch_name" | sed 's|^origin/||')

    # Skip main and development branches
    if [[ "$branch_name" == "main" || "$branch_name" == "master" || "$branch_name" == "develop" ]]; then
        echo -e "${GREEN}✅ ${branch_name} - Main/development branch${NC}"
        return 0
    fi

    # Check against patterns
    if [[ $branch_name =~ $FEATURE_PATTERN ]]; then
        is_valid=true
        branch_type="feature"
    elif [[ $branch_name =~ $FIX_PATTERN ]]; then
        is_valid=true
        branch_type="fix"
    elif [[ $branch_name =~ $SECURITY_PATTERN ]]; then
        is_valid=true
        branch_type="security"
    elif [[ $branch_name =~ $CHORE_PATTERN ]]; then
        is_valid=true
        branch_type="chore"
    elif [[ $branch_name =~ $RELEASE_PATTERN ]]; then
        is_valid=true
        branch_type="release"
    elif [[ $branch_name =~ $HOTFIX_PATTERN ]]; then
        is_valid=true
        branch_type="hotfix"
    elif [[ $branch_name =~ $CLAUDE_PATTERN ]]; then
        is_valid=true
        branch_type="claude-code"
    fi

    if $is_valid; then
        echo -e "${GREEN}✅ ${branch_name} - Valid ${branch_type} branch${NC}"
        return 0
    else
        echo -e "${RED}❌ ${branch_name} - Invalid branch name${NC}"

        # Provide suggestions
        echo -e "${YELLOW}Expected formats:${NC}"
        echo "  feature/[issue-]description  (e.g., feature/123-add-monitoring)"
        echo "  fix/[issue-]description      (e.g., fix/58-memory-leak)"
        echo "  security/description         (e.g., security/fix-injection)"
        echo "  chore/description           (e.g., chore/update-docs)"
        echo "  release/version             (e.g., release/v1.0.0)"
        echo "  hotfix/description          (e.g., hotfix/critical-patch)"
        echo

        # Try to suggest corrections
        suggest_corrections "$branch_name"
        return 1
    fi
}

suggest_corrections() {
    local branch_name="$1"
    local suggestions=""

    # Extract potential type and description
    if [[ $branch_name =~ ^([^/]+)/(.+)$ ]]; then
        local type="${BASH_REMATCH[1]}"
        local desc="${BASH_REMATCH[2]}"

        # Clean up description
        local clean_desc=$(echo "$desc" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]/-/g' | sed 's/--*/-/g' | sed 's/^-\|-$//g')

        echo -e "${YELLOW}Suggestions:${NC}"

        # Check if type is valid
        case $type in
            feature|fix|security|chore|release|hotfix)
                if [[ "$clean_desc" != "$desc" ]]; then
                    echo "  ${type}/${clean_desc}"
                fi
                ;;
            feat)
                echo "  feature/${clean_desc}"
                ;;
            bugfix|bug)
                echo "  fix/${clean_desc}"
                ;;
            sec)
                echo "  security/${clean_desc}"
                ;;
            maintenance|maint)
                echo "  chore/${clean_desc}"
                ;;
            rel)
                echo "  release/${clean_desc}"
                ;;
            *)
                echo "  feature/${clean_desc}  (if this is a new feature)"
                echo "  fix/${clean_desc}      (if this is a bug fix)"
                echo "  chore/${clean_desc}    (if this is maintenance)"
                ;;
        esac
    else
        # No slash found, suggest adding type
        local clean_name=$(echo "$branch_name" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]/-/g' | sed 's/--*/-/g' | sed 's/^-\|-$//g')
        echo -e "${YELLOW}Suggestions:${NC}"
        echo "  feature/${clean_name}  (if this is a new feature)"
        echo "  fix/${clean_name}      (if this is a bug fix)"
        echo "  chore/${clean_name}    (if this is maintenance)"
    fi
    echo
}

get_current_branch() {
    git rev-parse --abbrev-ref HEAD 2>/dev/null || {
        echo -e "${RED}Error: Not in a git repository${NC}"
        exit 1
    }
}

check_all_branches() {
    echo -e "${BLUE}Validating all local branches...${NC}"
    echo

    local all_valid=true
    local branches=$(git branch --format='%(refname:short)' | grep -v '^remotes/')

    while IFS= read -r branch; do
        if ! validate_branch_name "$branch"; then
            all_valid=false
        fi
    done <<< "$branches"

    echo
    if $all_valid; then
        echo -e "${GREEN}🎉 All branches follow naming conventions!${NC}"
        return 0
    else
        echo -e "${RED}⚠️  Some branches don't follow naming conventions${NC}"
        echo -e "${YELLOW}Use the branch creation scripts to ensure proper naming${NC}"
        return 1
    fi
}

main() {
    if [[ $# -eq 0 ]]; then
        # Validate current branch
        local current_branch=$(get_current_branch)
        echo -e "${BLUE}Validating current branch: ${current_branch}${NC}"
        echo
        validate_branch_name "$current_branch"
    elif [[ "$1" == "--check-all" ]]; then
        check_all_branches
    elif [[ "$1" == "-h" || "$1" == "--help" ]]; then
        print_usage
    else
        # Validate specific branch
        echo -e "${BLUE}Validating branch: $1${NC}"
        echo
        validate_branch_name "$1"
    fi
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
