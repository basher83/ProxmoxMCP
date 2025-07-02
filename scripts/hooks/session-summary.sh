#!/bin/bash
# Session summary hook for ProxmoxMCP
# Generates summary when Claude Code session ends

# Get repository root dynamically
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

# Ensure logs directory exists
mkdir -p ${REPO_ROOT}/.claude/logs

SUMMARY_FILE="${REPO_ROOT}/.claude/logs/session-$(date +%Y%m%d-%H%M%S).summary"

echo "Claude Code Session Summary" > "$SUMMARY_FILE"
echo "==========================" >> "$SUMMARY_FILE"
echo "Date: $(date)" >> "$SUMMARY_FILE"
echo "" >> "$SUMMARY_FILE"

# Count operations
if [ -f "${REPO_ROOT}/.claude/logs/command-history.log" ]; then
    COMMAND_COUNT=$(wc -l < ${REPO_ROOT}/.claude/logs/command-history.log)
    echo "Commands executed: $COMMAND_COUNT" >> "$SUMMARY_FILE"
fi

# List modified files
echo "" >> "$SUMMARY_FILE"
echo "Modified Files:" >> "$SUMMARY_FILE"
git status --porcelain 2>/dev/null | while read -r line; do
    echo "  $line" >> "$SUMMARY_FILE"
done

# Check for uncommitted changes
UNCOMMITTED=$(git status --porcelain 2>/dev/null | wc -l)
if [ "$UNCOMMITTED" -gt 0 ]; then
    echo "" >> "$SUMMARY_FILE"
    echo "⚠️  Uncommitted changes: $UNCOMMITTED files" >> "$SUMMARY_FILE"
fi

# ProxmoxMCP specific summary
echo "" >> "$SUMMARY_FILE"
echo "ProxmoxMCP Activity:" >> "$SUMMARY_FILE"

# Check if any tools were modified
TOOLS_MODIFIED=$(git status --porcelain 2>/dev/null | grep "src/proxmox_mcp/tools/" | wc -l)
if [ "$TOOLS_MODIFIED" -gt 0 ]; then
    echo "  - Modified $TOOLS_MODIFIED tool files" >> "$SUMMARY_FILE"
fi

# Check if config was modified
CONFIG_MODIFIED=$(git status --porcelain 2>/dev/null | grep "config/" | wc -l)
if [ "$CONFIG_MODIFIED" -gt 0 ]; then
    echo "  - Modified configuration files" >> "$SUMMARY_FILE"
fi

# Final recommendations
echo "" >> "$SUMMARY_FILE"
echo "Recommendations:" >> "$SUMMARY_FILE"
if [ "$UNCOMMITTED" -gt 0 ]; then
    echo "  1. Run quality checks: pytest && black . && mypy . && ruff ." >> "$SUMMARY_FILE"
    echo "  2. Commit your changes with descriptive message" >> "$SUMMARY_FILE"
fi

# Display summary
cat "$SUMMARY_FILE"
echo ""
echo "📄 Full summary saved to: $SUMMARY_FILE"

exit 0