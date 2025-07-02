#!/bin/bash
# Post-markdown lint hook for ProxmoxMCP
# Validates markdown files after edits

# Get file path from arguments
FILE_PATH=$(echo "$CLAUDE_TOOL_ARGUMENTS" | jq -r '.file_path // empty')

if [ -z "$FILE_PATH" ] || [ ! -f "$FILE_PATH" ]; then
    exit 0
fi

# Check if it's a markdown file
if [[ "$FILE_PATH" == *.md ]]; then
    echo "📝 Checking Markdown formatting..."
    
    # Check if markdownlint is installed
    if command -v markdownlint &> /dev/null; then
        # Run markdownlint with project config
        markdownlint -c /workspaces/ProxmoxMCP/.markdownlint.jsonc "$FILE_PATH" 2>&1 || {
            echo "⚠️  Markdown linting issues found in $FILE_PATH"
            echo "💡 Run 'markdownlint -c /workspaces/ProxmoxMCP/.markdownlint.jsonc --fix \"$FILE_PATH\"' to auto-fix issues"
            # Don't exit with error - just warn
        }
    else
        # Check for markdownlint-cli2
        if command -v markdownlint-cli2 &> /dev/null; then
            markdownlint-cli2 "$FILE_PATH" 2>&1 || {
                echo "⚠️  Markdown linting issues found"
                echo "💡 Run 'markdownlint-cli2-fix \"$FILE_PATH\"' to auto-fix"
            }
        else
            echo "💡 Consider installing markdownlint for markdown validation:"
            echo "   npm install -g markdownlint-cli"
            echo "   or: npm install -g markdownlint-cli2"
        fi
    fi
    
    # Check for common markdown issues
    if grep -q "```$" "$FILE_PATH"; then
        echo "⚠️  Found code blocks without language specifiers"
    fi
    
    if grep -E "^#{1,6}[^ ]" "$FILE_PATH"; then
        echo "⚠️  Found headers without space after #"
    fi
    
    # ProxmoxMCP specific checks
    if [[ "$FILE_PATH" == *"docs/"* ]]; then
        echo "📚 Documentation file updated - ensure links are valid"
    fi
fi

exit 0