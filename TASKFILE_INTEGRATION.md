# Taskfile Integration Guide for ProxmoxMCP Branch Management

## 🚀 Quick Integration

To integrate branch management tasks into your existing Taskfile.yml:

```bash
# Run the integration script
./scripts/branch-templates/integrate-taskfile.sh

# Or manually copy from the integrated version
cp Taskfile-integrated.yml Taskfile.yml
```

## 📋 New Tasks Overview

### Branch Creation Tasks

| Task | Description | Usage |
|------|-------------|-------|
| `task branch` | Interactive branch creation | `task branch` |
| `task branch:feature` | Create feature branch | `task branch:feature -- "desc" [issue]` |
| `task branch:fix` | Create fix branch | `task branch:fix -- "description" [issue]` |
| `task branch:security` | Create security branch | `task branch:security -- "description"` |
| `task branch:chore` | Create chore branch | `task branch:chore -- "description"` |
| `task branch:hotfix` | Create hotfix branch | `task branch:hotfix -- "description"` |
| `task branch:release` | Create release branch | `task branch:release -- "v1.0.0"` |

### Branch Management Tasks

| Task | Description | Usage |
|------|-------------|-------|
| `task branch:validate` | Validate current branch | `task branch:validate` |
| `task branch:validate:all` | Validate all branches | `task branch:validate:all` |
| `task branch:check` | Check specific branch | `task branch:check -- "branch-name"` |
| `task branch:status` | Show branch status | `task branch:status` |
| `task branch:sync` | Sync with main | `task branch:sync` |
| `task branch:clean` | Show cleanup commands | `task branch:clean` |
| `task branch:list` | List all branches | `task branch:list` |

### Workflow Tasks

| Task | Description | Usage |
|------|-------------|-------|
| `task work:start` | Start new work | `task work:start` |
| `task work:save` | Save current work | `task work:save` |
| `task work:finish` | Finish and prepare PR | `task work:finish` |
| `task branch:ready` | Check PR readiness | `task branch:ready` |
| `task branch:workflow` | Complete workflow | `task branch:workflow` |

## 🎯 Usage Examples

### Starting New Work

```bash
# Start working on a new feature
task work:start
# This will:
# 1. Guide you through branch creation
# 2. Set up development environment
# 3. Show next steps

# Or create specific branch types directly
task branch:feature -- "add-vm-monitoring-tools" 123
task branch:fix -- "memory-leak-connection-pool" 58
task branch:security -- "fix-shell-injection"
```

### During Development

```bash
# Save your work (quality checks + commit guidance)
task work:save

# Check if your branch is ready for PR
task branch:ready

# Validate your branch name
task branch:validate

# See all your branches
task branch:list
```

### Finishing Work

```bash
# Complete your work and get PR guidance
task work:finish

# Check branch status
task branch:status

# Sync with main if needed
task branch:sync
```

### Quality Assurance Integration

```bash
# The branch:ready task combines:
task branch:ready
# - Branch name validation
# - All code quality checks (format, lint, type)
# - Test execution
# - YAML validation
```

## 🔄 Integration with Existing Tasks

The new branch tasks work seamlessly with your existing workflow:

```bash
# Combined workflow example
task work:start                    # Create branch + setup
# ... make your changes ...
task quick                         # Format + lint + test (existing task)
task work:save                     # Quality check + commit helper
task work:finish                   # Final checks + PR guidance

# Or step by step
task branch:feature -- "new-api" 123
task setup                         # Existing setup task
# ... development work ...
task check                         # Existing quality checks
task branch:ready                  # New: combines validation + checks
```

## 🎨 Task Features

### Command Line Arguments

```bash
# Feature branches with issue numbers
task branch:feature -- "add-monitoring" 123
task branch:feature -- "improve-performance"

# Fix branches
task branch:fix -- "connection-timeout" 58
task branch:fix -- "null-pointer-exception"

# Security branches
task branch:security -- "cve-2025-47273-fix"
task branch:security -- "input-validation"

# Release branches
task branch:release -- "v1.0.0"
task branch:release -- "v1.1.0-beta"

# Branch validation
task branch:check -- "feature/123-my-branch"
task branch:check -- "invalid-branch-name"
```

### Interactive Mode

```bash
# Guided experience for beginners
task branch
# This opens the interactive branch creator with:
# - Branch type selection
# - Description input
# - Issue number linking
# - Confirmation and guidance
```

### Status and Information

```bash
# Show current branch and git status
task branch:status

# List all branches with commit info
task branch:list

# Show project information including branch
task info
```

## 🔧 Advanced Usage

### Custom Workflows

```bash
# Create your own workflow combinations
task branch:feature -- "new-tool" 123 && task setup && task dev

# Check everything before creating PR
task branch:ready && echo "Ready for PR!"

# Quick branch creation and immediate development
task work:start && code .
```

### Git Integration

```bash
# The tasks handle git operations automatically:
# - Update main branch before creating new branches
# - Push branches with upstream tracking
# - Provide git commands for manual operations

# Branch cleanup (shows commands to run)
task branch:clean
# Output: Commands to delete merged branches
```

### CI/CD Integration

```bash
# Local CI simulation with branch validation
task ci && task branch:validate

# Pre-commit workflow
task pre-commit && task branch:ready
```

## 🛠️ Customization

### Modifying Tasks

You can customize the branch tasks by editing the Taskfile.yml:

```yaml
# Example: Add your own branch workflow
custom:workflow:
  desc: My custom workflow
  cmds:
    - task: branch:feature
    - task: setup
    - task: test
    - echo "Custom workflow complete!"
```

### Environment Variables

The tasks respect your existing environment:

```yaml
env:
  PYTHONPATH: "src:{{.PYTHONPATH}}"  # Existing
  # Branch scripts use git configuration automatically
```

## 📊 Task List Integration

The new tasks are organized in the task list:

```bash
task --list
```

Shows organized sections:

- **Branch Management**: All branch-related tasks
- **Development Setup**: Existing setup tasks
- **Code Quality**: Existing quality tasks
- **Testing**: Existing test tasks
- etc.

## 🔄 Migration and Compatibility

### Backward Compatibility

All your existing tasks remain unchanged:

- ✅ `task setup` - Still works exactly the same
- ✅ `task quick` - No changes to existing workflow
- ✅ `task check` - All quality checks unchanged
- ✅ `task ci` - CI simulation unchanged

### New Dependencies

The branch tasks only require:

- Git (already required for your project)
- Bash (standard on macOS/Linux)
- The branch template scripts (included)

No additional dependencies needed!

## 🚨 Troubleshooting

### Common Issues

**Task not found:**

```bash
# Make sure integration completed
task --list | grep branch

# If not found, re-run integration
./scripts/branch-templates/integrate-taskfile.sh
```

**Branch script not executable:**

```bash
chmod +x scripts/branch-templates/*.sh
```

**Git errors:**

```bash
# Make sure you're in the git repository
git status

# Check if main branch exists
git branch -a
```

### Getting Help

```bash
# Show all available tasks
task --list

# Show task description
task --summary branch:feature

# Show project info including current branch
task info

# Validate current setup
task branch:validate
```

## 🎉 Quick Start Cheat Sheet

```bash
# Essential commands for daily use
task branch                        # Create new branch (interactive)
task work:start                    # Start new work (create + setup)
task work:save                     # Save work (check + commit help)
task work:finish                   # Finish work (ready + PR guide)

# Quick branch creation
task branch:feature -- "desc" 123  # Feature with issue
task branch:fix -- "desc" 58      # Fix with issue
task branch:hotfix -- "desc"      # Emergency fix

# Quality and validation
task branch:ready                  # Check if ready for PR
task quick                         # Fast quality check (existing)
task check                         # Full quality check (existing)

# Status and management
task branch:status                 # Current branch info
task branch:list                   # All branches overview
task info                          # Project + branch info
```

This integration makes branch management a natural part of your existing Task workflow while
maintaining all the power and flexibility of your current setup!
