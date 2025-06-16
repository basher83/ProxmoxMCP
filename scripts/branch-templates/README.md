# Branch Templates

This directory contains scripts and templates to help create branches following the ProxmoxMCP branching strategy.

## 🚀 Quick Start

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

## 📁 Files Overview

| File | Purpose |
|------|---------|
| `create-branch.sh` | Main branch creation script with full functionality |
| `feature.sh` | Quick feature branch creation |
| `fix.sh` | Quick fix branch creation |
| `security.sh` | Quick security branch creation |
| `hotfix.sh` | Quick hotfix branch creation |
| `config.sh` | Configuration settings and templates |
| `README.md` | This documentation |

## 🔧 Usage

### Main Script

```bash
./create-branch.sh <type> <description> [issue-number]
```

**Branch Types:**

- `feature` - New feature development
- `fix` - Bug fixes
- `security` - Security-related changes
- `chore` - Maintenance tasks
- `release` - Release preparation
- `hotfix` - Critical production fixes

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

## 🎯 Branch Naming Conventions

The scripts automatically generate branch names following the established conventions:

| Branch Type | Format | Example |
|-------------|--------|---------|
| Feature | `feature/[issue-]description` | `feature/123-add-vm-monitoring` |
| Fix | `fix/[issue-]description` | `fix/58-memory-leak-fix` |
| Security | `security/description` | `security/fix-shell-injection` |
| Chore | `chore/description` | `chore/update-documentation` |
| Release | `release/version` | `release/v1.0.0` |
| Hotfix | `hotfix/description` | `hotfix/critical-patch` |

## ✨ Script Features

### Automatic Validation

- ✅ Validates branch type and description
- ✅ Checks git repository status
- ✅ Warns about uncommitted changes
- ✅ Ensures main branch exists and is current

### Smart Branch Management

- 🔄 Automatically updates main branch before creating new branch
- 📤 Pushes branch to remote with upstream tracking
- 🏷️ Generates clean, consistent branch names
- 📋 Provides branch-specific guidance and next steps

### User Experience

- 🎨 Colored output for better readability
- 📖 Comprehensive help and usage information
- ⚡ Quick helper scripts for common operations
- 🛡️ Safety checks and confirmations

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

Edit `config.sh` to customize:

- **Branch prefixes**: Modify naming conventions
- **Commit templates**: Customize commit message formats
- **Review requirements**: Set reviewer counts by branch type
- **Git settings**: Change main branch name or remote

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

### Manual Branch Creation

If scripts fail, you can still create branches manually following the conventions:

```bash
# Update main
git checkout main
git pull origin main

# Create and push branch
git checkout -b feature/123-description
git push -u origin feature/123-description
```

## 🔗 Integration with Existing Tools

### VS Code

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
```

Usage:

```bash
git new-feature "add-monitoring" 123
git new-fix "connection-issue" 58
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
```

Usage:

```bash
task branch:feature -- "add-monitoring" 123
task branch:fix -- "connection-issue" 58
```

## 📚 Related Documentation

- [Branching Strategy Guide](../../docs/branching-strategy-guide.md)
- [Development Workflow](../../docs/development-workflow.md)
- [Contributing Guidelines](../../CONTRIBUTING.md)
- [Claude Code Automation](../../docs/claude-code-automation.md)

## 🔄 Updates and Maintenance

To update the branch templates:

1. Modify the scripts or configuration
2. Test with a sample branch creation
3. Update this README if needed
4. Commit changes with:

   ```bash
   git add scripts/branch-templates/
   git commit -m "chore: update branch templates"
   ```

## 💡 Tips and Best Practices

1. **Use issue numbers**: Always include issue numbers for features and fixes
2. **Keep descriptions short**: Use clear, hyphenated descriptions
3. **Test locally**: Run quality checks before pushing
4. **Follow conventions**: Use the provided commit message templates
5. **Update documentation**: Keep docs in sync with code changes

---

These templates are designed to work seamlessly with the ProxmoxMCP development workflow and existing automation. For questions or improvements, please create an issue or discussion in the repository.
