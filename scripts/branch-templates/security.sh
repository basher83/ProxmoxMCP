#!/bin/bash
# Quick security branch creation
# Usage: ./security.sh <description>

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/create-branch.sh"

if [ $# -eq 1 ]; then
    main "security" "$1"
else
    echo "Usage: $0 <description>"
    echo "Example: $0 'fix-shell-injection'"
    echo "Example: $0 'cve-2025-47273-setuptools'"
    exit 1
fi
