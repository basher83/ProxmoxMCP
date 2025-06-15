#!/bin/bash
# Quick feature branch creation
# Usage: ./feature.sh <description> [issue-number]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/create-branch.sh"

if [ $# -eq 1 ]; then
    main "feature" "$1"
elif [ $# -eq 2 ]; then
    main "feature" "$1" "$2"
else
    echo "Usage: $0 <description> [issue-number]"
    echo "Example: $0 'add-vm-monitoring' 123"
    exit 1
fi
