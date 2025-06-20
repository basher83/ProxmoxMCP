# YAML Linting Setup for ProxmoxMCP

This repository includes comprehensive YAML linting and auto-fixing capabilities using `yamllint` and task automation.

## Quick Start

### Install Task (if not already installed)

```bash
# On macOS
brew install go-task/tap/go-task

# On Linux
sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b ~/.local/bin

# Or download from https://github.com/go-task/task/releases
```

### Setup Development Environment

```bash
# Install dependencies (including yamllint)
task setup
```

## YAML Linting Commands

### Using Task (Recommended)

```bash
# Lint all YAML files
task yaml:lint

# Show detailed issues
task yaml:fix

# Strict check (exits with error if issues found)
task yaml:check

# Auto-fix all code issues (Python + YAML)
task fix

# Run all quality checks
task check

# Pre-commit style workflow
task pre-commit
```

### Using the Scripts Directly

```bash
# Lint all YAML files
./scripts/yaml-lint.sh

# Show detailed issues
./scripts/yaml-lint.sh --fix

# Strict check
./scripts/yaml-lint.sh --check

# Auto-fix spacing issues
./scripts/yaml-autofix.sh
```

### Using VS Code Tasks

- Open Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`)
- Type "Tasks: Run Task"
- Choose from:
  - `Lint YAML Files`
  - `Fix YAML Issues`
  - `Check YAML (Strict)`

## Configuration

### yamllint Configuration (`.yamllint.yml`)

The repository includes a customized yamllint configuration that:

- Sets line length to 120 characters (flexible for GitHub Actions)
- Uses 2-space indentation
- Allows common GitHub Actions truthy values (`yes`, `no`, `on`, `off`)
- Ignores lock files and template directories
- Provides warnings instead of errors for line length

### Supported Files

The linting automatically finds and checks:

- `*.yml` files
- `*.yaml` files
- Excludes: `pnpm-lock.yaml`, `yarn.lock`, `package-lock.json`
- Ignores: `node_modules`, `.git`, `venv`, `__pycache__`

## Integration

### GitHub Actions

YAML linting is integrated into:

1. **Autofix Workflow** (`.github/workflows/autofix.yml`) - Runs on every PR/push
2. **Dedicated YAML Lint Workflow** (`.github/workflows/yaml-lint.yml`) - Triggered by YAML changes

### Pre-commit Integration

Add to your development workflow:

```bash
# Run before committing
task pre-commit

# Or run full CI simulation
task ci
```

## Common YAML Issues and Fixes

### 1. Line Length

```yaml
# ❌ Too long
- name: This is a very long line that exceeds the maximum line length limit and should be broken down

# ✅ Fixed
- name: >
    This is a very long line that exceeds the maximum line length limit
    and should be broken down
```

### 2. Indentation

```yaml
# ❌ Wrong indentation
steps:
- name: Step 1
  run: echo "hello"

# ✅ Correct indentation
steps:
  - name: Step 1
    run: echo "hello"
```

### 3. Truthy Values

```yaml
# ❌ Inconsistent
enabled: True
debug: false
cache: yes

# ✅ Consistent
enabled: true
debug: false
cache: true
```

## Troubleshooting

### yamllint Not Found

```bash
# Reinstall dependencies
task setup
# or
uv sync --extra dev
```

### Permission Denied

```bash
# Make script executable
chmod +x scripts/yaml-lint.sh
chmod +x scripts/yaml-autofix.sh
```

### Custom Rules

Edit `.yamllint.yml` to customize rules for your needs. See [yamllint
documentation](https://yamllint.readthedocs.io/en/stable/configuration.html) for
all available options.

## Available Task Commands

Run `task --list` to see all available commands:

```text
task: Available tasks for this project:
* default:              Show available tasks
* check:                Run all code quality checks
* ci:                   Run CI checks locally
* fix:                  Auto-fix all fixable issues
* pre-commit:           Run pre-commit checks
* quick:                Quick development check
* setup:                Set up development environment
* yaml:autofix:         Auto-fix YAML spacing issues
* yaml:check:           Check YAML files (strict mode)
* yaml:fix:             Show detailed YAML linting issues
* yaml:lint:            Lint all YAML files
```
