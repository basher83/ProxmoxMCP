#!/bin/bash
# Post-bash validation hook for ProxmoxMCP
# Analyzes command results and provides feedback

# Get repository root dynamically
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

# Get command and exit code from environment
COMMAND=$(echo "$CLAUDE_TOOL_ARGUMENTS" | jq -r '.command // empty')
EXIT_CODE=$(echo "$CLAUDE_TOOL_RESULT" | jq -r '.exit_code // 0')

# Ensure logs directory exists
mkdir -p ${REPO_ROOT}/.claude/logs

# Log command execution
echo "[$(date +"%Y-%m-%d %H:%M:%S")] Command: $COMMAND (exit: $EXIT_CODE)" >> ${REPO_ROOT}/.claude/logs/command-history.log

# Check for specific ProxmoxMCP commands
if echo "$COMMAND" | grep -q "pytest"; then
    if [ "$EXIT_CODE" -ne 0 ]; then
        echo "❌ Tests failed! Review the output and fix issues before proceeding."
        echo "💡 Tip: Run 'pytest -v' for detailed output"
    else
        echo "✅ All tests passed!"
    fi
fi

if echo "$COMMAND" | grep -q "mypy"; then
    if [ "$EXIT_CODE" -ne 0 ]; then
        echo "❌ Type checking failed! Fix type errors before committing."
        echo "💡 Tip: Use 'mypy . --show-error-codes' for detailed errors"
    fi
fi

if echo "$COMMAND" | grep -q "black"; then
    echo "🎨 Code formatted with Black"
fi

if echo "$COMMAND" | grep -q "ruff"; then
    if [ "$EXIT_CODE" -ne 0 ]; then
        echo "❌ Linting failed! Fix issues or use 'ruff check . --fix'"
    fi
fi

# Check for git operations
if echo "$COMMAND" | grep -qE "git (add|commit|push)"; then
    echo "📝 Git operation completed. Remember to run quality checks before committing!"
fi

exit 0