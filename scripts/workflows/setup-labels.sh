#!/bin/bash
# GitHub Labels Setup Script for ProxmoxMCP
# This script applies the standardized labels defined in labels.yml

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo -e "${RED}Error: GitHub CLI (gh) is not installed.${NC}"
    echo "Please install it from: https://cli.github.com/"
    exit 1
fi

# Check if user is authenticated
if ! gh auth status &> /dev/null; then
    echo -e "${RED}Error: Not authenticated with GitHub CLI.${NC}"
    echo "Please run: gh auth login"
    exit 1
fi

echo -e "${BLUE}Setting up ProxmoxMCP GitHub labels...${NC}"

# Function to create or update a label
create_or_update_label() {
    local name="$1"
    local color="$2"
    local description="$3"

    # Try to create the label, if it exists, update it
    if gh label create "$name" --color "$color" --description "$description" 2>/dev/null; then
        echo -e "${GREEN}✓ Created label: $name${NC}"
    else
        # Label exists, update it
        if gh label edit "$name" --color "$color" --description "$description" 2>/dev/null; then
            echo -e "${YELLOW}✓ Updated label: $name${NC}"
        else
            echo -e "${RED}✗ Failed to create/update label: $name${NC}"
        fi
    fi
}

echo -e "${BLUE}Creating Issue Type Labels...${NC}"
create_or_update_label "bug" "d73a4a" "Something isn't working correctly"
create_or_update_label "enhancement" "a2eeef" "New feature or request"
create_or_update_label "documentation" "0075ca" "Improvements or additions to documentation"
create_or_update_label "security" "b60205" "Security-related issues or improvements"
create_or_update_label "performance" "fbca04" "Performance-related issues or improvements"
create_or_update_label "question" "d876e3" "Further information is requested"

echo -e "${BLUE}Creating Priority Labels...${NC}"
create_or_update_label "priority:critical" "b60205" "Critical priority - immediate attention required"
create_or_update_label "priority:high" "d93f0b" "High priority - should be addressed soon"
create_or_update_label "priority:medium" "fbca04" "Medium priority - normal timeline"
create_or_update_label "priority:low" "0e8a16" "Low priority - can be addressed later"

echo -e "${BLUE}Creating Status Labels...${NC}"
create_or_update_label "status:needs-investigation" "f9d0c4" "Requires investigation to understand the issue"
create_or_update_label "status:confirmed" "0e8a16" "Issue has been confirmed and reproduced"
create_or_update_label "status:in-progress" "fbca04" "Work is currently in progress"
create_or_update_label "status:blocked" "d73a4a" "Cannot proceed due to external dependencies"
create_or_update_label "status:ready-for-review" "0075ca" "Ready for code review"
create_or_update_label "status:waiting-for-feedback" "f9d0c4" "Waiting for feedback from reporter or community"

echo -e "${BLUE}Creating Component Labels...${NC}"
create_or_update_label "component:server" "1d76db" "Core MCP server implementation"
create_or_update_label "component:config" "1d76db" "Configuration system and loading"
create_or_update_label "component:tools" "1d76db" "MCP tool implementations"
create_or_update_label "component:formatting" "1d76db" "Output formatting and theming"
create_or_update_label "component:docker" "0052cc" "Docker and containerization"
create_or_update_label "component:authentication" "b60205" "Authentication and security"
create_or_update_label "component:api" "1d76db" "Proxmox API integration"
create_or_update_label "component:testing" "0e8a16" "Test suite and testing infrastructure"

echo -e "${BLUE}Creating Platform Labels...${NC}"
create_or_update_label "platform:linux" "5319e7" "Linux-specific issues"
create_or_update_label "platform:windows" "5319e7" "Windows-specific issues"
create_or_update_label "platform:macos" "5319e7" "macOS-specific issues"
create_or_update_label "platform:docker" "0052cc" "Docker-specific issues"

echo -e "${BLUE}Creating Proxmox Version Labels...${NC}"
create_or_update_label "proxmox:7.x" "ff6b35" "Proxmox VE 7.x versions"
create_or_update_label "proxmox:8.x" "ff6b35" "Proxmox VE 8.x versions"

echo -e "${BLUE}Creating Effort Labels...${NC}"
create_or_update_label "effort:small" "c2e0c6" "Small effort - hours to days"
create_or_update_label "effort:medium" "ffeaa7" "Medium effort - days to weeks"
create_or_update_label "effort:large" "fdcb6e" "Large effort - weeks to months"

echo -e "${BLUE}Creating Community Labels...${NC}"
create_or_update_label "help-wanted" "008672" "Extra attention is needed - community help welcome"
create_or_update_label "good-first-issue" "7057ff" "Good for newcomers"
create_or_update_label "hacktoberfest" "ff6b35" "Suitable for Hacktoberfest contributions"

echo -e "${BLUE}Creating Special Labels...${NC}"
create_or_update_label "duplicate" "cfd3d7" "This issue or pull request already exists"
create_or_update_label "invalid" "e4e669" "This doesn't seem right"
create_or_update_label "wontfix" "ffffff" "This will not be worked on"
create_or_update_label "dependencies" "0366d6" "Pull requests that update a dependency file"
create_or_update_label "python" "306998" "Python-related changes"
create_or_update_label "github-actions" "000000" "GitHub Actions and CI/CD related"

echo -e "${BLUE}Creating Discussion Labels...${NC}"
create_or_update_label "discussion" "d876e3" "Discussion topic"
create_or_update_label "show-and-tell" "0e8a16" "Community showcase"
create_or_update_label "ideas" "a2eeef" "Ideas and brainstorming"
create_or_update_label "community-support" "008672" "Community help and support"

echo -e "${BLUE}Creating Installation Labels...${NC}"
create_or_update_label "installation" "f9d0c4" "Installation and setup related"
create_or_update_label "configuration" "f9d0c4" "Configuration-related issues"

echo -e "${BLUE}Creating Integration Labels...${NC}"
create_or_update_label "integration:cline" "bfd4f2" "Cline integration specific"
create_or_update_label "integration:mcp" "bfd4f2" "MCP protocol specific"
create_or_update_label "integration:proxmox" "ff6b35" "Proxmox integration specific"

echo -e "${GREEN}✅ Label setup complete!${NC}"
echo -e "${BLUE}You can now use these labels in issues and pull requests.${NC}"
