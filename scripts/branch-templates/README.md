# Branch Management System

A comprehensive branch management system for the ProxmoxMCP project that provides
both automated branch templates and validation tools to enforce consistent branch
naming conventions.

## 🚀 Quick Start

### Using Branch Templates (Recommended)

```bash
# Navigate to the scripts directory
cd scripts/branch-templates

# Create a feature branch
./feature.sh "add-vm-monitoring-tools" 123

# Create a fix branch
./fix.sh "memory-leak-connection-pool" 58

# Create a security branch
./security.sh "fix-shell-injection"

# Create a hotfix branch
./hotfix.sh "critical-security-patch"
```

### Using Branch Manager (Interactive)

```bash
# Interactive branch creation
./scripts/branch-templates/branch-manager.sh create

# Validate current branch
./scripts/branch-templates/validate.sh --current

# List all branches with validation status
./scripts/branch-templates/branch-manager.sh list
```

## 📁 Files Overview

| File                | Purpose                                             |
| ------------------- | --------------------------------------------------- |
| `create-branch.sh`  | Main branch creation script with full functionality |
| `branch-manager.sh` | Interactive branch management interface             |
| `validate.sh`       | Branch name validation tool                         |
| `feature.sh`        | Quick feature branch creation                       |
| `fix.sh`            | Quick fix branch creation                           |
| `security.sh`       | Quick security branch creation                      |
| `hotfix.sh`         | Quick hotfix branch creation                        |
| `config.sh`         | Configuration settings and shared functions         |
| `README.md`         | This documentation                                  |

## 🎯 Branch Naming Conventions

All branches must follow the format: `<type>/<component>-<description>` or legacy format: `<type>/[issue-]<description>`

### Valid Types

| Type       | Purpose                          | Legacy Support   |
| ---------- | -------------------------------- | ---------------- |
| `feature`  | New features and enhancements    | ✅               |
| `fix`      | Bug fixes and patches            | ✅               |
| `security` | Security improvements            | ✅               |
| `docker`   | Container and deployment updates | ✅               |
| `config`   | Configuration changes            | ✅               |
| `docs`     | Documentation updates            | ✅               |
| `ci`       | CI/CD pipeline changes           | ✅               |
| `perf`     | Performance improvements         | ✅               |
| `chore`    | Maintenance tasks                | ✅ (legacy only) |
| `release`  | Release preparation              | ✅ (legacy only) |
| `hotfix`   | Critical production fixes        | ✅               |

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

### Branch Name Examples

| Branch Type | Modern Format                         | Legacy Format                   |
| ----------- | ------------------------------------- | ------------------------------- |
| Feature     | `feature/vm-console-management`       | `feature/123-add-vm-monitoring` |
| Fix         | `fix/api-timeout-handling`            | `fix/58-memory-leak-fix`        |
| Security    | `security/encryption-key-rotation`    | `security/fix-shell-injection`  |
| Docker      | `docker/container-security-hardening` | N/A                             |
| Config      | `config/proxmox-connection-settings`  | N/A                             |

## 🔧 Usage

### Branch Templates (Quick Creation)

```bash
./create-branch.sh <type> <description> [issue-number]
```

**Examples:**

```bash
./create-branch.sh feature "add-vm-monitoring-tools" 123
./create-branch.sh fix "memory-leak-connection-pool" 58
./create-branch.sh security "fix-shell-injection"
./create-branch.sh chore "update-documentation"
./create-branch.sh release "v1.0.0"
./create-branch.sh hotfix "critical-security-patch"
```

### Quick Helper Scripts

For faster workflows, use the helper scripts:

```bash
# Feature branches
./feature.sh "add-new-tool" 123
./feature.sh "improve-error-handling"

# Fix branches
./fix.sh "connection-timeout" 58
./fix.sh "null-pointer-exception"

# Security branches
./security.sh "cve-2025-47273-setuptools"
./security.sh "input-validation-fix"

# Hotfix branches (critical issues only)
./hotfix.sh "production-down-fix"
./hotfix.sh "security-patch-immediate"
```

### Validation Tool (`validate.sh`)

```bash
# Validate current branch
./scripts/branch-templates/validate.sh --current

# Validate a specific branch name
./scripts/branch-templates/validate.sh --name "feature/vm-console"

# Validate branch name (positional argument)
./scripts/branch-templates/validate.sh "fix/api-timeout-handling"

# Validate all local branches
./scripts/branch-templates/validate.sh --check-all
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

## ✨ Script Features

### Automatic Validation

- ✅ Validates branch type and description
- ✅ Checks git repository status
- ✅ Warns about uncommitted changes
- ✅ Ensures main branch exists and is current
- ✅ Validates component naming (modern format)
- ✅ Backward compatibility with legacy patterns

### Smart Branch Management

- 🔄 Automatically updates main branch before creating new branch
- 📤 Pushes branch to remote with upstream tracking
- 🏷️ Generates clean, consistent branch names
- 📋 Provides branch-specific guidance and next steps
- 🧹 Automated cleanup of merged branches

### User Experience

- 🎨 Colored output for better readability
- 📖 Comprehensive help and usage information
- ⚡ Quick helper scripts for common operations
- 🛡️ Safety checks and confirmations
- 💬 Interactive mode for guided branch creation

## 🔄 Workflow Integration

### With GitHub Issues

```bash
# Create feature branch for issue #123
./feature.sh "implement-new-api-endpoint" 123

# Create fix branch for issue #58
./fix.sh "resolve-authentication-bug" 58
```

### With Claude Code

When Claude Code is assigned to an issue, it will automatically:

1. Create a branch using pattern: `claude/issue-{number}-{description}`
2. Implement the solution
3. Create a pull request

For manual work on Claude-identified issues:

```bash
./feature.sh "claude-suggested-improvement" 123
```

### Emergency Hotfixes

```bash
# For critical production issues
./hotfix.sh "critical-security-vulnerability"
```

This will:

- Create the hotfix branch immediately
- Show warning about expedited review process
- Provide guidance for minimal, focused changes

## 📋 Commit Message Templates

The scripts provide guidance for commit messages following conventional commit format:

### Feature Commits

```
feat: implement new VM monitoring tools

- Add VM metrics collection
- Implement memory usage tracking
- Add CPU utilization monitoring

Closes #123
```

### Fix Commits

```
fix: resolve memory leak in connection pool

- Fix connection cleanup in error scenarios
- Add proper resource disposal
- Update connection timeout handling

Fixes #58
```

### Security Commits

```
security: fix shell injection vulnerability

- Replace subprocess calls with shell=False
- Add input validation for command parameters
- Update security documentation

Addresses CVE-2025-XXXX
```

### Hotfix Commits

```
hotfix: patch critical authentication bypass

- Fix JWT token validation logic
- Add additional security checks
- Requires immediate deployment

Critical security fix
```

## 🔧 Configuration

### System Configuration

Edit `config.sh` to customize:

- **Branch prefixes**: Modify naming conventions
- **Commit templates**: Customize commit message formats
- **Review requirements**: Set reviewer counts by branch type
- **Git settings**: Change main branch name or remote
- **Validation rules**: Component requirements, naming patterns

### User Configuration

Create a `.branch-config` file in the repository root for personal overrides:

```bash
# Override default settings
export MAX_BRANCH_NAME_LENGTH=100
export REQUIRE_COMPONENT_IN_NAME=false
export AUTO_DELETE_MERGED_BRANCHES=false

# Add custom components
VALID_COMPONENTS+=("custom-component")
```

## 🔗 Integration with Development Tools

### Pre-commit Hooks

Add branch validation to your pre-commit configuration:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: branch-validation
        name: Branch name validation
        entry: ./scripts/branch-templates/validate.sh --current
        language: script
        pass_filenames: false
        always_run: true
```

### Git Hooks

#### Pre-push Hook

```bash
#!/bin/bash
# .git/hooks/pre-push
./scripts/branch-templates/validate.sh --current
```

### VS Code Integration

Add to your VS Code settings for quick access:

```json
{
  "terminal.integrated.profiles.osx": {
    "Branch Creator": {
      "path": "/Users/basher8383/dev/personal/ProxmoxMCP/scripts/branch-templates",
      "args": ["./create-branch.sh"]
    }
  }
}
```

### Git Aliases

Add to your `.gitconfig`:

```ini
[alias]
  new-feature = "!f() { ./scripts/branch-templates/feature.sh \"$1\" \"$2\"; }; f"
  new-fix = "!f() { ./scripts/branch-templates/fix.sh \"$1\" \"$2\"; }; f"
  new-security = "!f() { ./scripts/branch-templates/security.sh \"$1\"; }; f"
  validate-branch = "!./scripts/branch-templates/validate.sh --current"
```

Usage:

```bash
git new-feature "add-monitoring" 123
git new-fix "connection-issue" 58
git validate-branch
```

### Task Integration

Add to your `Taskfile.yml`:

```yaml
tasks:
  branch:feature:
    desc: Create a new feature branch
    cmds:
      - ./scripts/branch-templates/feature.sh "{{.CLI_ARGS}}"

  branch:fix:
    desc: Create a new fix branch
    cmds:
      - ./scripts/branch-templates/fix.sh "{{.CLI_ARGS}}"

  branch:validate:
    desc: Validate current branch name
    cmds:
      - ./scripts/branch-templates/validate.sh --current
```

Usage:

```bash
task branch:feature -- "add-monitoring" 123
task branch:fix -- "connection-issue" 58
task branch:validate
```

## 🚨 Troubleshooting

### Common Issues

**Script not executable:**

```bash
chmod +x scripts/branch-templates/*.sh
```

**Not in git repository:**

```bash
cd /path/to/ProxmoxMCP
./scripts/branch-templates/feature.sh "my-feature"
```

**Main branch not found:**

```bash
# Ensure you're on the correct repository
git branch -a
```

**Uncommitted changes warning:**

```bash
# Commit or stash changes first
git add .
git commit -m "WIP: save current work"
# or
git stash
```

**Branch name validation errors:**

```bash
# Use the validation tool to check your branch name
./scripts/branch-templates/validate.sh "my-branch-name"

# Get suggestions for valid names
./scripts/branch-templates/validate.sh "invalid-branch-name"
```

### Manual Branch Creation

If scripts fail, you can still create branches manually following the conventions:

```bash
# Update main
git checkout main
git pull origin main

# Create and push branch
git checkout -b feature/vm-console-management
git push -u origin feature/vm-console-management
```

## 📚 Related Documentation

- [Branching Strategy Guide](../../docs/branching-strategy-guide.md)
- [Development Workflow](../../docs/development-workflow.md)
- [Contributing Guidelines](../../CONTRIBUTING.md)
- [Claude Code Automation](../../docs/claude-code-automation.md)

## 🔄 Updates and Maintenance

To update the branch management system:

1. Modify the scripts or configuration
2. Test with a sample branch creation
3. Update this README if needed
4. Run validation tests:

   ```bash
   ./scripts/branch-templates/validate.sh --check-all
   ```

5. Commit changes with:

   ```bash
   git add scripts/branch-templates/
   git commit -m "chore: update branch management system"
   ```

## 💡 Tips and Best Practices

1. **Use issue numbers**: Always include issue numbers for features and fixes when available
2. **Choose appropriate components**: Select the most relevant component for your branch
3. **Keep descriptions short**: Use clear, hyphenated descriptions
4. **Test locally**: Run quality checks before pushing
5. **Follow conventions**: Use the provided commit message templates
6. **Update documentation**: Keep docs in sync with code changes
7. **Validate early**: Use the validation tools before creating branches
8. **Clean up regularly**: Use the branch manager to clean up merged branches

## 🎯 Migration Guide

### From Legacy to Modern Format

If you have existing branches using the legacy format, they will continue to work. For new
branches, consider using the modern component-based format:

**Legacy:** `feature/123-add-monitoring`  
**Modern:** `feature/vm-monitoring-dashboard`

The validation system supports both formats for backward compatibility.

---

This branch management system is designed to work seamlessly with the ProxmoxMCP development
workflow and existing automation. For questions or improvements, please create an issue or
discussion in the repository.
