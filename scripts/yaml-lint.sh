#!/usr/bin/env bash
# YAML Linting and Auto-fix Script for ProxmoxMCP
# This script provides consistent YAML linting and auto-fixing across the repository

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
YAMLLINT_CONFIG="${REPO_ROOT}/.yamllint.yml"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if yamllint is available
check_yamllint() {
    if ! command -v uv &> /dev/null; then
        print_error "UV is not installed. Please install UV first."
        exit 1
    fi

    print_status "Checking yamllint availability..."
    if ! uv run yamllint --version &> /dev/null; then
        print_error "yamllint is not available. Installing dependencies..."
        uv sync --extra dev
    fi
}

# Function to find all YAML files
find_yaml_files() {
    find "${REPO_ROOT}" -type f \( -name "*.yml" -o -name "*.yaml" \) \
        -not -path "*/node_modules/*" \
        -not -path "*/.git/*" \
        -not -path "*/venv/*" \
        -not -path "*/.venv/*" \
        -not -path "*/__pycache__/*" \
        -not -name "pnpm-lock.yaml" \
        -not -name "yarn.lock" \
        -not -name "package-lock.json"
}

# Function to lint YAML files
lint_yaml() {
    local fix_mode="${1:-false}"
    local exit_code=0

    print_status "Running yamllint on YAML files..."

    if [ "$fix_mode" = "true" ]; then
        print_status "Auto-fix mode enabled"
    fi

    print_status "Finding YAML files..."
    local yaml_files
    yaml_files=$(find_yaml_files)

    if [ -z "$yaml_files" ]; then
        print_warning "No YAML files found to lint"
        return 0
    fi

    local file_count
    file_count=$(echo "$yaml_files" | wc -l)
    print_status "Found $file_count YAML files to check"

    local failed_files=()

    while IFS= read -r file; do
        printf "Checking %-60s " "$(basename "$file")..."

        if uv run yamllint -c "$YAMLLINT_CONFIG" "$file" 2>/dev/null; then
            echo -e "${GREEN}✓${NC}"
        else
            echo -e "${RED}✗${NC}"
            failed_files+=("$file")

            if [ "$fix_mode" = "true" ]; then
                # For now, yamllint doesn't have auto-fix, so we'll show the errors
                print_warning "Showing issues for $file:"
                uv run yamllint -c "$YAMLLINT_CONFIG" "$file" 2>&1 || true
                echo ""
            fi
        fi
    done <<< "$yaml_files"

    # Summary
    echo ""
    if [ ${#failed_files[@]} -eq 0 ]; then
        print_success "All YAML files passed linting! ✨"
    else
        print_error "Found issues in ${#failed_files[@]} YAML files:"
        for file in "${failed_files[@]}"; do
            echo "  - $(basename "$file")"
        done

        if [ "$fix_mode" != "true" ]; then
            echo ""
            print_status "Run with --fix to see detailed issues"
        fi

        exit_code=1
    fi

    return $exit_code
}

# Function to show help
show_help() {
    cat << EOF
YAML Linting and Auto-fix Script for ProxmoxMCP

Usage: $0 [OPTIONS]

OPTIONS:
    --lint, -l          Lint all YAML files (default)
    --fix, -f           Show detailed linting issues
    --check, -c         Check only (exit with error if issues found)
    --help, -h          Show this help message

EXAMPLES:
    $0                  # Lint all YAML files
    $0 --fix            # Show detailed issues
    $0 --check          # Check and exit with error code if issues found

CONFIGURATION:
    YAML linting rules are configured in .yamllint.yml

EOF
}

# Main function
main() {
    local action="lint"
    local fix_mode="false"

    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --lint|-l)
                action="lint"
                shift
                ;;
            --fix|-f)
                action="lint"
                fix_mode="true"
                shift
                ;;
            --check|-c)
                action="check"
                shift
                ;;
            --help|-h)
                show_help
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done

    # Change to repo root
    cd "$REPO_ROOT"

    # Check dependencies
    check_yamllint

    # Run the requested action
    case $action in
        lint)
            lint_yaml "$fix_mode"
            ;;
        check)
            lint_yaml "false"
            ;;
        *)
            print_error "Unknown action: $action"
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
