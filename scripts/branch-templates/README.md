# Branch Management System

A comprehensive branch management system for the ProxmoxMCP project that enforces consistent branch naming conventions and provides tools for branch validation and management.

## Files

- **`config.sh`** - Configuration and shared functions for the branch management system
- **`validate.sh`** - Branch name validation tool
- **`branch-manager.sh`** - Main interface for branch management operations

## Quick Start

### Validate Current Branch
```bash
./scripts/branch-templates/validate.sh --current
```

### Create a New Branch Interactively
```bash
./scripts/branch-templates/branch-manager.sh create
```

### List All Branches with Validation Status
```bash
./scripts/branch-templates/branch-manager.sh list
```

## Branch Naming Convention

All branches must follow the format: `<type>/<component>-<description>`

### Valid Types

- `feature` - New features and enhancements
- `fix` - Bug fixes and patches  
- `security` - Security improvements
- `docker` - Container and deployment updates
- `config` - Configuration changes
- `docs` - Documentation updates
- `ci` - CI/CD pipeline changes
- `perf` - Performance improvements

### Valid Components
- `vm` - Virtual machine management
- `container` - Container operations
- `storage` - Storage management
- `network` - Network configuration
- `backup` - Backup operations
- `auth` - Authentication/authorization
- `encryption` - Security and encryption
- `config` - Configuration management
- `api` - API development
- `mcp` - MCP protocol implementation
- `core` - Core functionality
- `tools` - Development tools
- `formatting` - Code formatting
- `docker` - Docker-specific changes
- `proxmox` - Proxmox API integration
- `console` - Console management
- `management` - General management features

### Examples of Valid Branch Names
- `feature/vm-console-management`
- `fix/api-timeout-handling`
- `security/encryption-key-rotation`
- `docker/container-security-hardening`
- `config/proxmox-connection-settings`

## Usage Guide

### Validation Tool (`validate.sh`)

```bash
# Validate current branch
./scripts/branch-templates/validate.sh --current

# Validate a specific branch name
./scripts/branch-templates/validate.sh --name "feature/vm-console"

# Validate branch name (positional argument)
./scripts/branch-templates/validate.sh "fix/api-timeout-handling"
```

### Branch Manager (`branch-manager.sh`)

```bash
# Interactive branch creation
./scripts/branch-templates/branch-manager.sh create

# Validate current branch
./scripts/branch-templates/branch-manager.sh validate

# List local branches with status
./scripts/branch-templates/branch-manager.sh list

# List all branches (including remote)
./scripts/branch-templates/branch-manager.sh list --all

# Clean up merged branches
./scripts/branch-templates/branch-manager.sh cleanup

# Dry run cleanup (show what would be deleted)
./scripts/branch-templates/branch-manager.sh cleanup --dry-run

# Show help
./scripts/branch-templates/branch-manager.sh help
```

## Configuration

The system can be customized by creating a `.branch-config` file in the repository root:

```bash
# Override default settings
export MAX_BRANCH_NAME_LENGTH=100
export REQUIRE_COMPONENT_IN_NAME=false
export AUTO_DELETE_MERGED_BRANCHES=false

# Add custom components
VALID_COMPONENTS+=("custom-component")
```

## Integration with Git Hooks

You can integrate the validation into Git hooks for automatic enforcement:

### Pre-push Hook
```bash
#!/bin/bash
# .git/hooks/pre-push
./scripts/branch-templates/validate.sh --current
```

### Pre-commit Hook (for branch validation)
```bash
#!/bin/bash
# .git/hooks/pre-commit
./scripts/branch-templates/validate.sh --current >/dev/null 2>&1 || {
    echo "Branch name validation failed. Run validation for details:"
    echo "./scripts/branch-templates/validate.sh --current"
    exit 1
}
```

## Shell Script Quality

All scripts follow best practices:
- ✅ Proper shebang (`#!/usr/bin/env bash`)
- ✅ Error handling with `set -euo pipefail`
- ✅ All variables properly used or exported
- ✅ Parameter expansion used instead of `sed` where appropriate
- ✅ No unused variables (all variables are exported for external use)
- ✅ Proper shellcheck compliance

## Troubleshooting

### Common Issues

1. **Permission denied**: Ensure scripts are executable
   ```bash
   chmod +x scripts/branch-templates/*.sh
   ```

2. **Branch validation fails**: Check that your branch name follows the convention
   ```bash
   ./scripts/branch-templates/validate.sh --name "your-branch-name"
   ```

3. **Not in git repository**: Run commands from within the repository root

### Getting Help

All scripts include built-in help:
```bash
./scripts/branch-templates/validate.sh --help
./scripts/branch-templates/branch-manager.sh help
```