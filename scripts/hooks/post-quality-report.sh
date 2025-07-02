#!/bin/bash
# Post-quality report hook for ProxmoxMCP
# Generates summary after quality checks

# Create report file
REPORT_FILE="/workspaces/ProxmoxMCP/.claude/logs/quality-report-$(date +%Y%m%d-%H%M%S).txt"

echo "Quality Check Report - $(date)" > "$REPORT_FILE"
echo "================================" >> "$REPORT_FILE"

# Check recent test results
if [ -f ".coverage" ]; then
    COVERAGE=$(coverage report --format=total 2>/dev/null || echo "N/A")
    echo "Test Coverage: $COVERAGE%" >> "$REPORT_FILE"
fi

# Count issues
MYPY_ERRORS=$(mypy . 2>&1 | grep -c "error:" || echo "0")
RUFF_ERRORS=$(ruff check . 2>&1 | grep -c "error:" || echo "0")

echo "MyPy Errors: $MYPY_ERRORS" >> "$REPORT_FILE"
echo "Ruff Errors: $RUFF_ERRORS" >> "$REPORT_FILE"

# ProxmoxMCP specific checks
echo "" >> "$REPORT_FILE"
echo "ProxmoxMCP Checks:" >> "$REPORT_FILE"
echo "-----------------" >> "$REPORT_FILE"

# Check for TODO/FIXME items
TODO_COUNT=$(grep -r "TODO\|FIXME" src/ --include="*.py" | wc -l || echo "0")
echo "TODO/FIXME items: $TODO_COUNT" >> "$REPORT_FILE"

# Check for security patterns
SECURITY_ISSUES=$(grep -r "password\|token" src/ --include="*.py" | grep -v "Field\|BaseModel" | wc -l || echo "0")
echo "Potential security patterns: $SECURITY_ISSUES" >> "$REPORT_FILE"

# Summary
echo "" >> "$REPORT_FILE"
if [ "$MYPY_ERRORS" -eq 0 ] && [ "$RUFF_ERRORS" -eq 0 ]; then
    echo "✅ All quality checks passed!" | tee -a "$REPORT_FILE"
else
    echo "❌ Quality issues detected - review report" | tee -a "$REPORT_FILE"
fi

echo "📊 Report saved to: $REPORT_FILE"
exit 0