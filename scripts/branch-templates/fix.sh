#!/bin/bash
# Quick fix branch creation
# Usage: ./fix.sh <description> [issue-number]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/create-branch.sh"

if [ $# -eq 1 ]; then
    main "fix" "$1"
elif [ $# -eq 2 ]; then
    main "fix" "$1" "$2"
else
    echo "Usage: $0 <description> [issue-number]"
    echo "Example: $0 'memory-leak-fix' 58"
    exit 1
fi
