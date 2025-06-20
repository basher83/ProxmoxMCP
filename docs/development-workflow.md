# Development Workflow

This document provides comprehensive documentation for all automated workflows,
CI/CD processes, and development practices in the ProxmoxMCP project.

## Table of Contents

- [Overview](#overview)
- [CI/CD Workflows](#cicd-workflows)
- [Dependency Management](#dependency-management)
- [Development Tools](#development-tools)
- [Quality Assurance](#quality-assurance)
- [Contributing Guidelines](#contributing-guidelines)

## Overview

The ProxmoxMCP project uses a modern development workflow with automated code
quality, dependency management, and AI-assisted development. All workflows are
designed to maintain high code quality while reducing manual overhead for
contributors.

### Key Principles

- **Automated Quality**: Code formatting and linting happen automatically
- **AI-Assisted Development**: Claude Code helps with issue resolution and code reviews
- **Security First**: All dependencies and code changes are automatically reviewed
- **Consistent Standards**: Enforced through automated tooling and workflows

## CI/CD Workflows

### 1. autofix.ci Workflow (`.github/workflows/autofix.yml`)

**Purpose**: Automatically fixes code formatting and quality issues in pull requests.

**Triggers**:

- Pull request creation and updates
- Pushes to the `main` branch

**Tools Used**:

- **black**: Python code formatting
- **ruff**: Linting and import sorting with auto-fix
- **mypy**: Type checking (informational)

**Process**:

1. Sets up Python 3.10 environment
2. Installs UV package manager with caching
3. Creates virtual environment and installs dev dependencies
4. Runs black formatter with fallback to auto-fix mode
5. Runs ruff with `--fix` flag for linting and import organization
6. Runs mypy for type checking validation
7. Commits any fixes directly to the PR branch via autofix.ci

**Key Features**:

- Uses `--exit-zero` flags to prevent workflow failures
- Caches dependencies for faster execution
- Follows project's established tooling standards
- Automatically handles import organization (complements manual configuration)

**Badge Status**: [![autofix enabled](https://shields.io/badge/autofix.ci-yes-success)](https://autofix.ci)

### 2. Claude Auto Review (`.github/workflows/claude-auto-review.yml`)

**Purpose**: Provides AI-powered code review and quality checks for pull requests.

**Triggers**:

- Pull request opened
- Pull request synchronized (new commits)

**Components**:

#### Auto Review Job

- **Runtime**: ubuntu-latest
- **Permissions**: contents:read, pull-requests:write, id-token:write
- **AI Model**: Uses Claude via Anthropic API
- **Focus Areas**:
  - Code quality and best practices
  - Potential bugs or security issues
  - Performance considerations
  - Test coverage analysis
  - Documentation completeness

#### Quality Checks Job

- **Runtime**: ubuntu-latest  
- **Python Version**: 3.9 (note: should be updated to 3.10 for consistency)
- **Tools**: pytest, black, mypy
- **Process**: Runs full quality check suite

**Integration**: Uses `mcp__github__add_pull_request_review_comment` for inline feedback.

### 3. Claude Issue Assignment (`.github/workflows/claude-issue-assignment.yml`)

**Purpose**: Automatically implements solutions when Claude Code bot is assigned to GitHub issues.

**Triggers**:

- Issue assignment to `claude-code-bot` or issues labeled with `claude-code`

**Process**:

1. **Notification**: Adds comment explaining that Claude Code will work on the issue
2. **Environment Setup**: Python 3.10, UV package manager, project dependencies
3. **Implementation**: Claude Code analyzes requirements and implements solution
4. **Quality Assurance**: Runs pytest, black, mypy to ensure code quality
5. **Branch Management**: Creates new branch for the work
6. **Pull Request**: Automatically creates PR when implementation is complete

**Key Features**:

- 120-minute timeout for complex issues
- Follows project guidelines from CLAUDE.md
- Automatic PR creation with issue linking
- Progress tracking through GitHub comments

**Branch Naming**: `claude/issue-{number}-{description}`

## Dependency Management

### Dependabot Configuration (`.github/dependabot.yml`)

**Purpose**: Automated dependency updates across multiple ecosystems.

**Schedule**: Weekly updates on different days to distribute load:

- **Monday 09:00 UTC**: Python dependencies
- **Tuesday 09:00 UTC**: Docker dependencies  
- **Wednesday 09:00 UTC**: GitHub Actions

#### Python Dependencies

- **Ecosystem**: pip
- **Grouping Strategy**:
  - **Production**: proxmoxer, pydantic, fastmcp (minor/patch only)
  - **Development**: pytest*, black, mypy, ruff (minor/patch only)
- **Major Version Protection**: Critical dependencies are protected from major updates
- **Labels**: `dependencies`, `python`
- **Assignee**: @basher83

#### Docker Dependencies

- **Ecosystem**: docker
- **Target**: Root directory Dockerfile
- **Labels**: `dependencies`, `docker`
- **Commit Prefix**: `docker:`

#### GitHub Actions

- **Ecosystem**: github-actions
- **Target**: `.github/workflows/` directory
- **Labels**: `dependencies`, `github-actions`
- **Commit Prefix**: `ci:`

**Security Features**:

- Major version updates require manual review
- Automatic assignment to maintainers
- Consistent labeling for easy filtering

## Development Tools

### Code Quality Stack

#### Black (Code Formatting)

- **Version**: 23.x
- **Configuration**: Inherits line length from ruff (100 characters)
- **Usage**: `black .`
- **Integration**: Automatic via autofix.ci workflow

#### Ruff (Linting & Import Sorting)

- **Version**: 0.1.x
- **Rules**: E (errors), F (pyflakes), B (bugbear), I (import sorting)
- **Target**: Python 3.10+
- **Usage**: `ruff check . --fix`
- **Import Sorting**: Configured for ProxmoxMCP with first-party package recognition

#### MyPy (Type Checking)

- **Version**: 1.x
- **Configuration**: Strict type checking enabled
- **Features**:
  - Disallows untyped definitions
  - Warns on unused ignores and redundant casts
  - Checks untyped definitions
- **Usage**: `mypy .`

#### Pytest (Testing)

- **Version**: 7.x
- **Mode**: Strict asyncio mode
- **Extensions**: pytest-asyncio for async test support
- **Usage**: `pytest`

### Package Management

#### UV Package Manager

- **Purpose**: Fast Python package installation and environment management
- **Features**: Caching, lock files, virtual environment management
- **Integration**: Used in all CI workflows for consistent dependency management

### Environment Setup

```bash
# Create and activate virtual environment
uv venv
source .venv/bin/activate  # Linux/macOS
.\.venv\Scripts\Activate.ps1  # Windows

# Install with development dependencies
uv pip install -e ".[dev]"
```

## Quality Assurance

### Local Development Commands

```bash
# Run individual tools
pytest          # Run tests
black .         # Format code
mypy .          # Type checking
ruff check .    # Linting
ruff check . --fix  # Fix linting issues

# Combined quality check (recommended)
pytest && black . && mypy . && ruff check .
```

### CI Quality Gates

All pull requests must pass:

1. **autofix.ci**: Automatic code formatting and linting
2. **Claude Auto Review**: AI-powered code review
3. **Quality Checks**: Full test suite and type checking

### Pre-commit Recommendations

While not enforced, developers can optionally use:

```bash
# Install pre-commit hooks (optional)
pip install pre-commit
pre-commit install
```

## Contributing Guidelines

### Pull Request Workflow

1. **Create Feature Branch**: `git checkout -b feature/description`
2. **Make Changes**: Implement your feature or fix
3. **Local Testing**: Run quality checks locally
4. **Push Changes**: `git push origin feature/description`
5. **Create PR**: GitHub will trigger autofix.ci and Claude review
6. **Address Feedback**: Respond to AI and human reviewer comments
7. **Merge**: Once approved and checks pass

### Issue Assignment Workflow

1. **Create Issue**: Use GitHub issue templates
2. **Label for Claude**: Add `claude-code` label or assign to `claude-code-bot`
3. **Automatic Implementation**: Claude Code will work on the issue
4. **Review PR**: Review the automatically created pull request
5. **Merge**: Approve and merge when satisfied

### Code Standards

- **Python Version**: 3.10+
- **Code Style**: Black formatting (100 character line length)
- **Import Organization**: Automated via ruff isort
- **Type Hints**: Required for all functions and methods
- **Testing**: Pytest with async support
- **Documentation**: Docstrings for all public functions

### Commit Message Guidelines

Follow the established commit template (`.gitmessage`):

```
type: brief description (max 50 chars)

Detailed explanation of what and why (not how).
Include impact on ProxmoxMCP components.
Wrap at 72 characters.

Fixes #issue-number
Co-authored-by: Name <email@example.com>
```

**Commit Types**:

- `feat`: New features
- `fix`: Bug fixes
- `security`: Security improvements
- `config`: Configuration changes
- `docker`: Container/deployment changes
- `refactor`: Code refactoring
- `test`: Test additions/updates
- `docs`: Documentation updates
- `ci`: CI/CD changes
- `deps`: Dependency updates

## Troubleshooting

### Common Issues

#### autofix.ci Not Running

- Check that the workflow file is named exactly `autofix.yml`
- Verify the autofix.ci app is installed on the repository
- Ensure branch protection rules allow autofix commits

#### Claude Code Assignment Not Working

- Verify the `claude-code` label exists in the repository
- Check that `ANTHROPIC_API_KEY` secret is configured
- Ensure issue templates are being used correctly

#### Quality Checks Failing

- Run checks locally first: `pytest && black . && mypy .`
- Check for Python version mismatch (should be 3.10+)
- Verify all dev dependencies are installed

#### Dependency Update Issues

- Check Dependabot configuration syntax
- Verify repository permissions for Dependabot
- Review ignored dependencies list

### Getting Help

- **Documentation**: Check this file and `CLAUDE.md`
- **Issues**: Create GitHub issue with `question` label
- **Discussions**: Use GitHub Discussions for broader topics
- **Security**: Use GitHub Security tab for security-related issues

## Future Enhancements

### Planned Additions

- **Release Automation**: Automated semantic versioning and releases
- **Security Scanning**: CodeQL and dependency vulnerability scanning  
- **Performance Testing**: Automated performance regression testing
- **Documentation**: Automated API documentation generation
- **Integration Testing**: End-to-end testing with mock Proxmox environments

### Configuration Files Reference

- **`.github/workflows/autofix.yml`**: autofix.ci configuration
- **`.github/workflows/claude-auto-review.yml`**: AI code review
- **`.github/workflows/claude-issue-assignment.yml`**: Automated issue resolution
- **`.github/dependabot.yml`**: Dependency update configuration
- **`pyproject.toml`**: Python project configuration and tool settings
- **`CLAUDE.md`**: Development commands and project guidelines
- **`.gitmessage`**: Commit message template

---

This workflow documentation is maintained alongside the codebase. When adding new
workflows or modifying existing ones, please update this document accordingly.
