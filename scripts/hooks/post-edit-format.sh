#!/bin/bash
# Post-edit formatting hook for ProxmoxMCP
# Automatically formats code after edits

# Get repository root dynamically
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

# Get file path from arguments
FILE_PATH=$(echo "$CLAUDE_TOOL_ARGUMENTS" | jq -r '.file_path // empty')

if [ -z "$FILE_PATH" ] || [ ! -f "$FILE_PATH" ]; then
    exit 0
fi

# Format Python files with ruff
if [[ "$FILE_PATH" == *.py ]]; then
    echo "🎨 Auto-formatting Python file with Ruff..."
    ruff format "$FILE_PATH" 2>/dev/null || {
        echo "⚠️  Ruff formatting failed - file may have syntax errors"
    }
    
    # Run ruff fixes
    echo "🔧 Running Ruff auto-fixes..."
    ruff check "$FILE_PATH" --fix --quiet 2>/dev/null || true
fi

# Validate JSON files
if [[ "$FILE_PATH" == *.json ]]; then
    echo "📋 Validating JSON syntax..."
    python -m json.tool "$FILE_PATH" > /dev/null 2>&1 || {
        echo "❌ Invalid JSON syntax in $FILE_PATH"
        exit 1
    }
fi

# Check for ProxmoxMCP specific files
if [[ "$FILE_PATH" == *"proxmox-config/"* ]]; then
    echo "⚠️  Configuration file modified - remember to update example files"
fi

if [[ "$FILE_PATH" == *"tools/"* ]]; then
    echo "🔧 Tool file modified - ensure tool is registered in definitions.py"
fi

exit 0