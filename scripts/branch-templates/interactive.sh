#!/bin/bash

# Interactive Branch Creator for ProxmoxMCP
# Provides a guided experience for creating branches

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

show_header() {
    clear
    echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║                    ProxmoxMCP Branch Creator                 ║${NC}"
    echo -e "${BLUE}║                     Interactive Mode                        ║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo
}

get_branch_type() {
    echo -e "${CYAN}Select branch type:${NC}"
    echo "1) 🚀 Feature - New functionality"
    echo "2) 🐛 Fix - Bug fixes"
    echo "3) 🔒 Security - Security improvements"
    echo "4) 🧹 Chore - Maintenance tasks"
    echo "5) 📦 Release - Version releases"
    echo "6) 🚨 Hotfix - Critical production fixes"
    echo

    while true; do
        read -p "Enter choice (1-6): " choice
        case $choice in
            1) BRANCH_TYPE="feature"; break ;;
            2) BRANCH_TYPE="fix"; break ;;
            3) BRANCH_TYPE="security"; break ;;
            4) BRANCH_TYPE="chore"; break ;;
            5) BRANCH_TYPE="release"; break ;;
            6) BRANCH_TYPE="hotfix"; break ;;
            *) echo -e "${RED}Invalid choice. Please enter 1-6.${NC}" ;;
        esac
    done

    echo -e "${GREEN}Selected: ${BRANCH_TYPE}${NC}"
    echo
}

get_description() {
    echo -e "${CYAN}Enter branch description:${NC}"

    # Provide examples based on branch type
    case $BRANCH_TYPE in
        feature)
            echo -e "${YELLOW}Examples: 'add-vm-monitoring-tools', 'implement-new-api-endpoint'${NC}"
            ;;
        fix)
            echo -e "${YELLOW}Examples: 'memory-leak-connection-pool', 'authentication-timeout'${NC}"
            ;;
        security)
            echo -e "${YELLOW}Examples: 'fix-shell-injection', 'cve-2025-47273-setuptools'${NC}"
            ;;
        chore)
            echo -e "${YELLOW}Examples: 'update-documentation', 'dependency-updates'${NC}"
            ;;
        release)
            echo -e "${YELLOW}Examples: 'v1.0.0', 'v1.1.0-beta'${NC}"
            ;;
        hotfix)
            echo -e "${YELLOW}Examples: 'critical-security-patch', 'production-down-fix'${NC}"
            ;;
    esac

    while true; do
        read -p "Description: " DESCRIPTION
        if [[ -n "$DESCRIPTION" ]]; then
            break
        else
            echo -e "${RED}Description cannot be empty.${NC}"
        fi
    done

    echo -e "${GREEN}Description: ${DESCRIPTION}${NC}"
    echo
}

get_issue_number() {
    if [[ "$BRANCH_TYPE" == "feature" || "$BRANCH_TYPE" == "fix" ]]; then
        echo -e "${CYAN}GitHub Issue Number (optional):${NC}"
        echo -e "${YELLOW}Link this branch to a GitHub issue for better tracking${NC}"
        read -p "Issue number (press Enter to skip): " ISSUE_NUMBER

        if [[ -n "$ISSUE_NUMBER" ]]; then
            # Validate it's a number
            if [[ "$ISSUE_NUMBER" =~ ^[0-9]+$ ]]; then
                echo -e "${GREEN}Issue: #${ISSUE_NUMBER}${NC}"
            else
                echo -e "${RED}Invalid issue number. Continuing without issue link.${NC}"
                ISSUE_NUMBER=""
            fi
        else
            echo -e "${YELLOW}No issue number specified${NC}"
        fi
        echo
    fi
}

show_summary() {
    echo -e "${CYAN}Branch Creation Summary:${NC}"
    echo -e "  Type: ${GREEN}${BRANCH_TYPE}${NC}"
    echo -e "  Description: ${GREEN}${DESCRIPTION}${NC}"
    if [[ -n "$ISSUE_NUMBER" ]]; then
        echo -e "  Issue: ${GREEN}#${ISSUE_NUMBER}${NC}"
    fi

    # Show what the branch name will be
    case $BRANCH_TYPE in
        feature|fix)
            if [[ -n "$ISSUE_NUMBER" ]]; then
                CLEAN_DESC=$(echo "$DESCRIPTION" | tr '[:upper:]' '[:lower:]' | \
                sed 's/[^a-z0-9-]/-/g' | sed 's/--*/-/g' | sed 's/^-\|-$//g')
                BRANCH_NAME="${BRANCH_TYPE}/${ISSUE_NUMBER}-${CLEAN_DESC}"
            else
                CLEAN_DESC=$(echo "$DESCRIPTION" | tr '[:upper:]' '[:lower:]' | \
                sed 's/[^a-z0-9-]/-/g' | sed 's/--*/-/g' | sed 's/^-\|-$//g')
                BRANCH_NAME="${BRANCH_TYPE}/${CLEAN_DESC}"
            fi
            ;;
        *)
            CLEAN_DESC=$(echo "$DESCRIPTION" | tr '[:upper:]' '[:lower:]' | \
                sed 's/[^a-z0-9-]/-/g' | sed 's/--*/-/g' | sed 's/^-\|-$//g')
            BRANCH_NAME="${BRANCH_TYPE}/${CLEAN_DESC}"
            ;;
    esac

    echo -e "  Branch Name: ${BLUE}${BRANCH_NAME}${NC}"
    echo
}

confirm_creation() {
    echo -e "${YELLOW}Create this branch? (y/N):${NC}"
    read -p "> " -n 1 -r
    echo

    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${RED}Branch creation cancelled.${NC}"
        exit 0
    fi
}

create_branch() {
    echo -e "${BLUE}Creating branch...${NC}"
    echo

    # Call the main creation script
    if [[ -n "$ISSUE_NUMBER" ]]; then
        "$SCRIPT_DIR/create-branch.sh" "$BRANCH_TYPE" "$DESCRIPTION" "$ISSUE_NUMBER"
    else
        "$SCRIPT_DIR/create-branch.sh" "$BRANCH_TYPE" "$DESCRIPTION"
    fi
}

show_completion() {
    echo
    echo -e "${GREEN}✅ Branch creation completed successfully!${NC}"
    echo
    echo -e "${CYAN}What's next?${NC}"
    echo "1. Start working on your changes"
    echo "2. Commit your work with proper commit messages"
    echo "3. Push commits: git push"
    echo "4. Create a Pull Request when ready"
    echo
    echo -e "${YELLOW}Press any key to exit...${NC}"
    read -n 1 -s
}

# Main execution
main() {
    show_header
    get_branch_type
    get_description
    get_issue_number
    show_summary
    confirm_creation
    create_branch
    show_completion
}

# Run if executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
