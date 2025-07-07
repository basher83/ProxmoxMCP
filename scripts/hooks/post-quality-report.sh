#!/bin/bash
# Post-quality report hook for ProxmoxMCP
# Generates summary after quality checks

# Get repository root dynamically
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

# Ensure logs directory exists
mkdir -p ${REPO_ROOT}/.claude/logs

# Create report file
REPORT_FILE="${REPO_ROOT}/.claude/logs/quality-report-$(date +%Y%m%d-%H%M%S).txt"

echo "Quality Check Report - $(date)" > "$REPORT_FILE"
echo "================================" >> "$REPORT_FILE"

# Check recent test results
if [ -f ".coverage" ]; then
    COVERAGE=$(coverage report --format=total 2>/dev/null || echo "N/A")
    echo "Test Coverage: $COVERAGE%" >> "$REPORT_FILE"
fi

# Count issues using exit codes and actual output
# Run mypy and capture both output and exit code
MYPY_OUTPUT=$(mypy . 2>&1)
MYPY_EXIT=$?
if [ "$MYPY_EXIT" -eq 0 ]; then
    MYPY_ERRORS=0
else
    # Count actual error lines (excluding summary lines)
    MYPY_ERRORS=$(echo "$MYPY_OUTPUT" | grep -E "\.py:[0-9]+:" | grep -c "error:" || echo "0")
fi

# Run ruff and capture both output and exit code
RUFF_OUTPUT=$(ruff check . 2>&1)
RUFF_EXIT=$?
if [ "$RUFF_EXIT" -eq 0 ]; then
    RUFF_ERRORS=0
else
    # Count actual diagnostic lines (format: path/file.py:line:col: CODE message)
    # Ruff codes are always one letter + 3 digits (e.g., F401, E501, W292)
    RUFF_ERRORS=$(echo "$RUFF_OUTPUT" | grep -E "\.py:[0-9]+:[0-9]+: [A-Z][0-9]{3}" | wc -l)
fi

echo "MyPy Errors: $MYPY_ERRORS" >> "$REPORT_FILE"
echo "Ruff Issues: $RUFF_ERRORS" >> "$REPORT_FILE"

# ProxmoxMCP specific checks
echo "" >> "$REPORT_FILE"
echo "ProxmoxMCP Checks:" >> "$REPORT_FILE"
echo "-----------------" >> "$REPORT_FILE"

# Check for TODO/FIXME items
TODO_COUNT=$(grep -r "TODO\|FIXME" src/ --include="*.py" 2>/dev/null | wc -l)
echo "TODO/FIXME items: $TODO_COUNT" >> "$REPORT_FILE"

# Check for security patterns
SECURITY_ISSUES=$(grep -r "password\|token" src/ --include="*.py" 2>/dev/null | grep -v "Field\|BaseModel" | wc -l)
echo "Potential security patterns: $SECURITY_ISSUES" >> "$REPORT_FILE"

# Exit code summary
echo "" >> "$REPORT_FILE"
echo "Exit Codes:" >> "$REPORT_FILE"
echo "-----------" >> "$REPORT_FILE"
echo "MyPy: $MYPY_EXIT (0=pass, non-zero=fail)" >> "$REPORT_FILE"
echo "Ruff: $RUFF_EXIT (0=pass, non-zero=fail)" >> "$REPORT_FILE"

# Summary
echo "" >> "$REPORT_FILE"
if [ "$MYPY_EXIT" -eq 0 ] && [ "$RUFF_EXIT" -eq 0 ]; then
    echo "✅ All quality checks passed!" | tee -a "$REPORT_FILE"
else
    echo "❌ Quality issues detected - review report" | tee -a "$REPORT_FILE"
    if [ "$MYPY_ERRORS" -gt 0 ]; then
        echo "   - MyPy found $MYPY_ERRORS error(s)" | tee -a "$REPORT_FILE"
    fi
    if [ "$RUFF_ERRORS" -gt 0 ]; then
        echo "   - Ruff found $RUFF_ERRORS issue(s)" | tee -a "$REPORT_FILE"
    fi
fi

echo "📊 Report saved to: $REPORT_FILE"
exit 0