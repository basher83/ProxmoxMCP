#!/bin/bash
# Setup script for enhanced pre-commit hooks
# This script addresses all Codacy issues identified

set -e

echo "🚀 Setting up enhanced pre-commit hooks for ProxmoxMCP..."
echo

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: This script must be run from the project root directory"
    exit 1
fi

# Install dependencies
echo "📦 Installing development dependencies..."
uv sync --extra dev

# Install pre-commit hooks
echo "🪝 Installing pre-commit hooks..."
uv run pre-commit install
uv run pre-commit install --hook-type commit-msg

# Run initial checks to catch existing issues
echo "🔍 Running initial security scan..."
echo "   (This will identify current issues to fix)"

# Run bandit security check (allow failures for initial run)
echo "🔒 Running Bandit security analysis..."
if uv run bandit -r src/ --format custom --skip B101,B601 --exclude tests/; then
    echo "✅ No security issues found!"
else
    echo "⚠️  Security issues found. These will be addressed in the GitHub issues created."
fi

echo
echo "🧹 Running code style fixes..."
# Fix trailing whitespace and other style issues
uv run pre-commit run trailing-whitespace --all-files || true
uv run pre-commit run end-of-file-fixer --all-files || true
uv run pre-commit run mixed-line-ending --all-files || true

# Format code
echo "🎨 Formatting code..."
uv run black .
uv run ruff format .

# Check complexity (informational)
echo "📊 Checking code complexity..."
if command -v radon >/dev/null 2>&1; then
    echo "Current complexity report:"
    uv run radon cc src/ --min B --show-complexity || true
else
    echo "ℹ️  Install radon for complexity analysis: uv add radon"
fi

echo
echo "🎯 Pre-commit setup complete!"
echo
echo "📋 Next steps:"
echo "   1. Run 'task hooks:run' to test all hooks"
echo "   2. Address security issues in GitHub issues #61 and #65"
echo "   3. Refactor complex methods (issue #62)"
echo "   4. Fix remaining style issues (issue #63)"
echo
echo "💡 Available commands:"
echo "   • task pre-commit    - Run all checks"
echo "   • task security      - Run security analysis"
echo "   • task complexity    - Check code complexity"
echo "   • task hooks:run     - Run all pre-commit hooks"
echo
echo "✅ Enhanced pre-commit hooks are now active!"
echo "   Your next commit will automatically run these checks."
