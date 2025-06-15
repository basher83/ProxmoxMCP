#!/bin/bash
# Quick hotfix branch creation (for critical production issues)
# Usage: ./hotfix.sh <description>

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/create-branch.sh"

echo -e "\033[0;31m⚠️  HOTFIX BRANCH CREATION ⚠️\033[0m"
echo "This creates a hotfix branch for critical production issues."
echo "Hotfix branches get expedited review and should contain minimal changes."
echo

if [ $# -eq 1 ]; then
    main "hotfix" "$1"
else
    echo "Usage: $0 <description>"
    echo "Example: $0 'critical-security-patch'"
    echo "Example: $0 'production-down-fix'"
    exit 1
fi
