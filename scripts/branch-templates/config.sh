#!/usr/bin/env bash
# Branch Management System Configuration
# Configuration file for ProxmoxMCP branch management templates and validation

set -euo pipefail

# Core Configuration - Export variables that may be used by external scripts
export BRANCH_PREFIX_FEATURE="feature"
export BRANCH_PREFIX_FIX="fix"
export BRANCH_PREFIX_SECURITY="security"
export BRANCH_PREFIX_DOCKER="docker"
export BRANCH_PREFIX_CONFIG="config"
export BRANCH_PREFIX_DOCS="docs"
export BRANCH_PREFIX_CI="ci"
export BRANCH_PREFIX_PERF="perf"

# Main branch settings
export DEFAULT_BRANCH="main"
export PROTECTED_BRANCHES=("main" "develop" "staging")

# Branch naming patterns
export MAX_BRANCH_NAME_LENGTH=80
export MIN_BRANCH_NAME_LENGTH=10

# Component identifiers that can be used in branch names
export VALID_COMPONENTS=(
    "vm"
    "container"
    "storage"
    "network"
    "backup"
    "auth"
    "encryption"
    "config"
    "api"
    "mcp"
    "core"
    "tools"
    "formatting"
    "docker"
    "proxmox"
    "console"
    "management"
)

# Validation settings
export REQUIRE_COMPONENT_IN_NAME=true
export ALLOW_ISSUE_NUMBERS=true
export REQUIRE_DESCRIPTIVE_SUFFIX=true

# Git settings
export REQUIRE_LINEAR_HISTORY=true
export REQUIRE_SIGN_OFF=false
export AUTO_DELETE_MERGED_BRANCHES=true

# Colors for output (used by validation script)
export COLOR_RED='\033[0;31m'
export COLOR_GREEN='\033[0;32m'
export COLOR_YELLOW='\033[1;33m'
export COLOR_BLUE='\033[0;34m'
export COLOR_NC='\033[0m'

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
export TEMPLATES_DIR="${SCRIPT_DIR}"

# Function to check if a branch name matches valid patterns
is_valid_branch_prefix() {
    local branch_name="$1"
    local valid_prefixes=(
        "$BRANCH_PREFIX_FEATURE"
        "$BRANCH_PREFIX_FIX" 
        "$BRANCH_PREFIX_SECURITY"
        "$BRANCH_PREFIX_DOCKER"
        "$BRANCH_PREFIX_CONFIG"
        "$BRANCH_PREFIX_DOCS"
        "$BRANCH_PREFIX_CI"
        "$BRANCH_PREFIX_PERF"
    )
    
    for prefix in "${valid_prefixes[@]}"; do
        if [[ "$branch_name" == "$prefix/"* ]]; then
            return 0
        fi
    done
    return 1
}

# Function to check if a component is valid
is_valid_component() {
    local component="$1"
    for valid in "${VALID_COMPONENTS[@]}"; do
        if [[ "$component" == "$valid" ]]; then
            return 0
        fi
    done
    return 1
}

# Function to generate branch name suggestions
suggest_branch_name() {
    local type="$1"
    local component="$2"
    local description="$3"
    
    # Sanitize description - replace spaces and special chars with hyphens
    local clean_description="${description,,}"  # lowercase
    clean_description="${clean_description//[^a-z0-9]/-}"  # replace non-alphanumeric with hyphens
    clean_description="${clean_description//--/-}"  # replace double hyphens
    clean_description="${clean_description#-}"  # remove leading hyphen
    clean_description="${clean_description%-}"  # remove trailing hyphen
    
    echo "${type}/${component}-${clean_description}"
}

# Function to load configuration from file if it exists
load_user_config() {
    local config_file="${REPO_ROOT}/.branch-config"
    if [[ -f "$config_file" ]]; then
        # shellcheck source=/dev/null
        source "$config_file"
    fi
}

# Load user configuration if available
load_user_config