#!/bin/bash
# Pre-code quality check hook for ProxmoxMCP
# Validates file edits match project standards

# Get repository root dynamically
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

# Get file path from arguments
FILE_PATH=$(echo "$CLAUDE_TOOL_ARGUMENTS" | jq -r '.file_path // empty')

if [ -z "$FILE_PATH" ]; then
    exit 0
fi

# Check if it's a Python file
if [[ "$FILE_PATH" == *.py ]]; then
    echo "📋 Pre-edit validation for Python file: $FILE_PATH"
    
    # Check if file exists (for edits)
    if [ -f "$FILE_PATH" ]; then
        # Validate current file syntax
        python -m py_compile "$FILE_PATH" 2>/dev/null || {
            echo "⚠️  WARNING: File has existing syntax errors"
        }
    fi
    
    # Check for ProxmoxMCP specific patterns
    if [[ "$FILE_PATH" == *"tools/"* ]]; then
        echo "🔧 Tool file detected - ensure ProxmoxTool inheritance"
    fi
    
    if [[ "$FILE_PATH" == *"config/"* ]]; then
        echo "⚙️  Config file detected - ensure Pydantic validation"
    fi
fi

# Check for test files
if [[ "$FILE_PATH" == *"test_"* ]] || [[ "$FILE_PATH" == *"_test.py" ]]; then
    echo "🧪 Test file detected - ensure pytest compatibility"
fi

exit 0