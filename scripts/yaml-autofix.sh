#!/usr/bin/env bash
# Working YAML Auto-fix Script for ProxmoxMCP
# Fixes trailing spaces, missing newlines in YAML files

set -euo pipefail

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}[INFO]${NC} Auto-fixing YAML files..."

# Fix trailing spaces and missing newlines
find . -name "*.yml" -o -name "*.yaml" | \
  grep -v node_modules | \
  grep -v .git | \
  grep -v venv | \
  grep -v pnmp-lock | \
  xargs -I{} sh -c 'echo "Fixing {}" && sed -i "s/[[:space:]]*$//" "{}" && \
    if [ -n "$(tail -c1 "{}" 2>/dev/null)" ]; then echo >> "{}"; fi'

echo ""
echo -e "${GREEN}[SUCCESS]${NC} YAML auto-fix completed!"

# Run yamllint verification if available
if command -v uv >/dev/null 2>&1 && uv run yamllint --version >/dev/null 2>&1; then
    echo -e "${BLUE}[INFO]${NC} Running yamllint verification..."
    ./scripts/yaml-lint.sh --check || {
        echo ""
        echo "Some issues remain (mostly line length warnings)."
        exit 1
    }
fi
