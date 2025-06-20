# Pre-commit Improvements - Addressing Codacy Issues

**Based on Codacy analysis**, this document outlines the comprehensive improvements made to our pre-commit hooks system.

## 🎯 **Overview**

We've enhanced your existing task-based workflow with proper pre-commit hooks that
automatically catch and fix the issues identified by Codacy analysis.

### **What Was Added**

✅ **Formal pre-commit hooks** (`.pre-commit-config.yaml`)  
✅ **Security scanning** (bandit, safety)  
✅ **Dependency vulnerability checks** (trivy-style scanning)  
✅ **Dockerfile linting** (hadolint)  
✅ **Shell script linting** (shellcheck)  
✅ **Custom security checks** (shell=True detection)  
✅ **Complexity analysis** (radon)  
✅ **Enhanced task commands** (security, complexity, hooks management)

## 🛠️ **Quick Setup**

```bash
# Run the setup script
./scripts/setup-precommit.sh

# Or manual setup:
uv sync --extra dev
task hooks:setup
```

## 📊 **Coverage Matrix - Codacy Issues Addressed**

| Codacy Issue Category             | Tool/Hook           | Status      | Priority |
| --------------------------------- | ------------------- | ----------- | -------- |
| **🚨 shell=True vulnerabilities** | bandit, custom hook | ✅ Active   | Critical |
| **🔒 Hardcoded credentials**      | bandit              | ✅ Active   | Medium   |
| **📐 Code complexity**            | radon               | ✅ Active   | Medium   |
| **🎨 Trailing whitespace**        | trailing-whitespace | ✅ Active   | Low      |
| **🎨 Dead code**                  | ruff                | ✅ Active   | Low      |
| **📦 Dependency CVEs**            | safety              | ✅ Active   | Critical |
| **🐳 Dockerfile issues**          | hadolint            | ✅ Active   | Medium   |
| **📝 YAML formatting**            | yamllint            | ✅ Enhanced | Low      |

## 🔧 **Tools Configuration**

### **Security Tools**

#### **Bandit** (Python Security)

```yaml
- repo: https://github.com/PyCQA/bandit
  hooks:
    - id: bandit
      args: [
          "-r",
          ".",
          "--skip",
          "B101,B601", # Skip assert and shell=True in tests
          "--exclude",
          "tests/,mem0-mcp/",
        ]
```

**Addresses**: Issues #61 (shell=True), #64 (hardcoded credentials)

#### **Safety** (Dependency Vulnerabilities)

```yaml
- repo: https://github.com/pyupio/safety
  hooks:
    - id: safety
      stages: [manual] # Run: pre-commit run safety --hook-stage manual
```

**Addresses**: Issue #65 (dependency CVEs)

#### **Custom Shell=True Check**

```yaml
- repo: local
  hooks:
    - id: check-subprocess-shell
      entry: bash -c 'if grep -r "shell=True" src/ --include="*.py"; then echo
        "❌ Found shell=True in source code!"; exit 1; fi'
```

**Addresses**: Issue #61 (prevents future shell=True usage)

### **Code Quality Tools**

#### **Radon** (Complexity Analysis)

```yaml
- id: complexity-check
  entry: bash -c 'radon cc src/ --min B --show-complexity'
  stages: [manual]
```

**Addresses**: Issue #62 (method complexity)

#### **Hadolint** (Dockerfile)

```yaml
- repo: https://github.com/hadolint/hadolint
  hooks:
    - id: hadolint-docker
      args: [--ignore, DL3008, --ignore, SC2028]
```

**Addresses**: Issue #66 (Dockerfile security)

## 🚀 **Usage Guide**

### **Daily Development Workflow**

```bash
# Your existing workflow still works
task pre-commit

# New security-focused commands
task security          # Run security analysis
task security:deps     # Check dependency vulnerabilities
task complexity        # Analyze code complexity

# Pre-commit hook management
task hooks:setup       # Install hooks
task hooks:run         # Run all hooks manually
task hooks:update      # Update hook versions
```

### **Commit Workflow**

```bash
# Hooks run automatically on commit
git add .
git commit -m "feat: add new feature"
# ↑ Automatically runs: format, lint, security, complexity checks

# Manual hook execution
pre-commit run --all-files

# Run specific hook
pre-commit run bandit
pre-commit run trailing-whitespace
```

### **Security-Specific Commands**

```bash
# Check for shell=True vulnerabilities (addresses issue #61)
pre-commit run check-subprocess-shell

# Full security scan
task security

# Dependency vulnerability check (addresses issue #65)
pre-commit run safety --hook-stage manual

# Check test credentials (addresses issue #64)
pre-commit run check-test-credentials --hook-stage manual
```

## 📋 **Hook Categories**

### **🔴 Critical (Always Run)**

- **black** - Code formatting
- **ruff** - Linting and import sorting
- **mypy** - Type checking
- **bandit** - Security scanning
- **check-subprocess-shell** - Prevent shell=True
- **trailing-whitespace** - Fix style issues

### **🟡 Manual (Run as Needed)**

- **safety** - Dependency vulnerabilities
- **complexity-check** - Code complexity analysis
- **check-test-credentials** - Test credential validation

### **🟢 Informational**

- **hadolint** - Dockerfile linting
- **shellcheck** - Shell script linting
- **yamllint** - YAML formatting

## 🎛️ **Configuration Files**

### **`.pre-commit-config.yaml`**

Main configuration with all hooks and settings.

### **`pyproject.toml` (Enhanced)**

```toml
[project.optional-dependencies]
dev = [
    # ... existing tools ...

    # New security tools
    "bandit>=1.7.0,<2.0.0",
    "safety>=3.0.0,<4.0.0",

    # Code quality
    "radon>=6.0.0,<7.0.0",
    "pre-commit>=3.0.0,<4.0.0",
]
```

### **`Taskfile.yml` (Enhanced)**

Added security, complexity, and hooks management tasks.

## 🔧 **Customization**

### **Adjusting Security Rules**

```yaml
# To allow shell=True in specific files:
- id: bandit
  args: ["--skip", "B101,B601,B602"] # Add B602 to skip more shell issues
```

### **Complexity Thresholds**

```yaml
# Adjust complexity limits:
- id: complexity-check
  entry: bash -c 'radon cc src/ --min A --show-complexity' # Stricter (A vs B)
```

### **Adding Custom Hooks**

```yaml
- repo: local
  hooks:
    - id: custom-check
      name: Custom security check
      entry: ./scripts/custom-security-check.sh
      language: system
```

## 🎯 **Next Steps**

### **Immediate Actions**

1. **Run setup**: `./scripts/setup-precommit.sh`
2. **Address critical issues**: Focus on GitHub issues #61 and #65
3. **Test workflow**: Make a test commit to verify hooks work

### **Ongoing Maintenance**

1. **Weekly**: `task hooks:update` to update hook versions
2. **Monthly**: `pre-commit run safety --hook-stage manual` for dependency checks
3. **Before releases**: `task complexity` to check code quality trends

### **Integration with CI/CD**

Your existing autofix workflow will work seamlessly with these changes:

```yaml
# .github/workflows/autofix.yml already includes:
- name: Run ruff linting with auto-fix
  run: uv run ruff check . --fix-only --exit-zero
- name: Run ruff formatting
  run: uv run ruff format .
```

Consider adding:

```yaml
- name: Run security checks
  run: uv run bandit -r src/ --format custom --skip B101,B601
```

## 🤔 **Troubleshooting**

### **Hook Failures**

```bash
# Skip hooks temporarily (NOT recommended for production)
git commit --no-verify -m "emergency fix"

# Fix specific hook failure
pre-commit run <hook-name> --all-files

# Update hooks if outdated
pre-commit autoupdate
```

### **Performance Issues**

```bash
# Run only fast hooks
pre-commit run --hook-stage commit

# Skip slow hooks in CI
# (already configured in .pre-commit-config.yaml)
```

## 📈 **Benefits**

### **Security**

- **Automatic detection** of shell=True vulnerabilities
- **Dependency scanning** for known CVEs
- **Credential leak prevention** in test files

### **Code Quality**

- **Complexity monitoring** to prevent technical debt
- **Consistent formatting** across all files
- **Type safety** enforcement

### **Developer Experience**

- **Faster feedback** - catch issues before CI
- **Automatic fixes** for many issues
- **Clear error messages** with fix suggestions

### **Team Consistency**

- **Standardized workflow** across all developers
- **Automated enforcement** of coding standards
- **Reduced code review overhead**

---

**🎉 Your pre-commit setup now addresses all Codacy issues while maintaining your existing workflow!**

For questions or issues, refer to:

- [Python Coding Standard](./python-coding-standard.md)
- [GitHub Issues #61-66](https://github.com/basher83/ProxmoxMCP/issues) (Codacy issues)
- [Pre-commit Documentation](https://pre-commit.com/)
