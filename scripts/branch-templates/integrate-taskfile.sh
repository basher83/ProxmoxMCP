#!/bin/bash

# ProxmoxMCP Taskfile Integration Script
# Safely integrates branch management tasks into existing Taskfile.yml

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

TASKFILE="Taskfile.yml"
BACKUP_FILE="Taskfile.yml.backup.$(date +%Y%m%d_%H%M%S)"
INTEGRATED_FILE="Taskfile-integrated.yml"

echo -e "${BLUE}ProxmoxMCP Taskfile Integration${NC}"
echo "================================="
echo

# Check if files exist
if [ ! -f "$TASKFILE" ]; then
    echo -e "${RED}Error: Taskfile.yml not found${NC}"
    exit 1
fi

if [ ! -f "$INTEGRATED_FILE" ]; then
    echo -e "${RED}Error: Taskfile-integrated.yml not found${NC}"
    echo "Make sure you're running this from the project root"
    exit 1
fi

# Create backup
echo -e "${YELLOW}Creating backup of current Taskfile.yml...${NC}"
cp "$TASKFILE" "$BACKUP_FILE"
echo -e "${GREEN}✅ Backup created: $BACKUP_FILE${NC}"
echo

# Show what will be added
echo -e "${BLUE}New branch management tasks that will be added:${NC}"
echo "• branch: - Interactive branch creation"
echo "• branch:feature: - Create feature branches"
echo "• branch:fix: - Create fix branches"
echo "• branch:security: - Create security branches"
echo "• branch:chore: - Create chore branches"
echo "• branch:hotfix: - Create hotfix branches"
echo "• branch:release: - Create release branches"
echo "• branch:validate: - Validate branch names"
echo "• branch:status: - Show branch status"
echo "• branch:sync: - Sync with main branch"
echo "• branch:ready: - Check if ready for PR"
echo "• work:start: - Start new work workflow"
echo "• work:save: - Save current work"
echo "• work:finish: - Finish work and prepare PR"
echo

# Confirm
read -p "Replace current Taskfile.yml with integrated version? (y/N): " -n 1 -r
echo

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Integration cancelled${NC}"
    echo -e "${BLUE}To manually integrate, you can:${NC}"
    echo "1. Review the changes in Taskfile-integrated.yml"
    echo "2. Copy the branch management sections to your Taskfile.yml"
    echo "3. Or replace your Taskfile.yml with the integrated version"
    exit 0
fi

# Replace file
echo -e "${BLUE}Integrating branch management tasks...${NC}"
cp "$INTEGRATED_FILE" "$TASKFILE"

echo -e "${GREEN}✅ Integration completed successfully!${NC}"
echo
echo -e "${BLUE}Quick test:${NC}"
task --list | grep -E "(branch|work):" || echo "No branch tasks found in list"

echo
echo -e "${GREEN}🎉 Ready to use! Try these commands:${NC}"
echo "  task branch                    # Interactive branch creation"
echo "  task branch:feature -- \"description\" 123"
echo "  task branch:validate           # Check current branch name"
echo "  task work:start               # Start new work workflow"
echo "  task --list                   # See all available tasks"
echo
echo -e "${YELLOW}📁 Files:${NC}"
echo "  • Original: $BACKUP_FILE (backup)"
echo "  • Current: $TASKFILE (integrated version)"
echo "  • Reference: $INTEGRATED_FILE (keep for reference)"
