# GitHub Instructions

This document provides guidelines for Claude Code when working with Git operations and
GitHub integration for the ProxmoxMCP repository.

**CRITICAL**: Always treat GitHub API as the authoritative source for repository state.
Local git state may be stale and lead to incorrect analysis or decisions.

## Repository State Management

### GitHub API as Authoritative Source

Before performing any branch analysis, repository assessment, or development planning:

```bash
# REQUIRED: Fetch latest remote state
git fetch origin

# Verify current branch state against remote
gh repo view --json defaultBranch,pushedAt
gh branch --list --all --verbose

# Cross-reference local vs remote branch state
git status
git branch -vv  # Show tracking branch relationship
gh api repos/basher83/ProxmoxMCP/branches --jq \
  '.[] | {name, commit: .commit.sha[0:7], protected}'
```

### Stale Branch Cleanup (Prerequisite for Analysis)

**ALWAYS perform stale branch cleanup** before branch analysis or strategic planning:

```bash
# 1. Identify stale local branches
git branch --merged main | grep -v main

# 2. Identify remote-tracking branches for deleted remotes
git remote prune origin --dry-run

# 3. List branches with no remote tracking
git for-each-ref --format='%(refname:short) %(upstream:track)' refs/heads | \
  grep '\[gone\]'

# 4. Clean up stale branches (after verification)
git branch --merged main | grep -v main | xargs -r git branch -d
git remote prune origin
git for-each-ref --format='%(refname:short) %(upstream:track)' refs/heads | \
  grep '\[gone\]' | awk '{print $1}' | xargs -r git branch -D
```

### State Cross-Reference Validation

When analyzing repository state, **ALWAYS cross-reference**:

```bash
# Local git state
git log --oneline -10
git status --porcelain

# GitHub API state (authoritative)
gh api repos/basher83/ProxmoxMCP/commits/main --jq \
  '.sha[0:7] + " " + .commit.message'
gh api repos/basher83/ProxmoxMCP/contents --jq \
  '.[] | select(.type=="file") | .name'

# Branch comparison
git log --oneline main..origin/main  # Commits behind
git log --oneline origin/main..main  # Commits ahead
gh api repos/basher83/ProxmoxMCP/compare/main...HEAD --jq \
  '{ahead_by, behind_by, status}'
```

## Git Configuration

The repository uses the following Git configuration from `/workspaces/ProxmoxMCP/example.gitconfig`:

### User Information

- **Name**: basher83
- **Email**: <crashoverride6545@gmail.com>

### Repository Settings

- **Default Branch**: `main`
- **Pull Strategy**: `rebase` (maintains linear history)
- **Push Strategy**: `current` with auto-setup of remote tracking
- **Merge Conflicts**: `diff3` style for better conflict resolution
- **Commit Template**: `.gitmessage` (enforces consistent commit formatting)

### Useful Git Aliases

```bash
git st          # status
git co          # checkout
git br          # branch
git cm          # commit
git lg          # enhanced log with graph
git sync        # fetch and show status
git ahead       # commits ahead of origin/main
git behind      # commits behind origin/main
git staged      # show staged changes
git files       # show changed file names only
git cleanup     # remove merged branches
git amend       # amend commit without editing
git tree        # graphical tree log
```

## Commit Message Guidelines

The repository uses a commit template at `/workspaces/ProxmoxMCP/.gitmessage`. All
commits must follow these conventions:

### Structure

```
type: brief description (max 50 chars)

Detailed explanation of what and why (not how).
Include impact on ProxmoxMCP components.
Wrap at 72 characters.

Fixes #issue-number
Co-authored-by: Name <email@example.com>
```

### Commit Types for ProxmoxMCP

- **feat**: New feature or tool implementation
- **fix**: Bug fix or issue resolution
- **security**: Security-related changes (encryption, validation, etc.)
- **config**: Configuration or setup changes
- **docker**: Docker/containerization changes
- **refactor**: Code refactoring without functional changes
- **test**: Adding or updating tests
- **docs**: Documentation updates
- **ci**: CI/CD pipeline changes
- **perf**: Performance improvements

### Required Information in Commit Body

- **Affected Components**: Mention specific ProxmoxMCP components (tools, formatting, config, core)
- **MCP Protocol Impact**: Include MCP protocol or Proxmox API impact if applicable
- **Breaking Changes**: Note configuration updates or breaking changes required
- **Security Implications**: Reference security implications for encryption/auth changes
- **Docker Impact**: Mention Docker/container impact if applicable
- **File References**: Include specific file paths when relevant (e.g., core/proxmox.py)

### Example Commits

```
security: implement token encryption at rest

Add Fernet-based encryption for Proxmox API tokens in
config files. Updates config/loader.py with automatic
decryption and maintains backward compatibility with
plain-text tokens. Requires PROXMOX_MCP_MASTER_KEY env var.

docker: enhance container security with non-root user

Update Dockerfile to run as dedicated mcp user instead
of root. Implements security best practices with proper
file permissions and resource limits in compose.yaml.

feat: add VM console management functionality

Implement interactive console access for VMs through QEMU
guest agent integration. Adds new MCP tools for command
execution and console interaction. Updates server.py tool
registration and extends VM tool capabilities.
```

## Branch Management

### Main Branch Protection

- **Branch**: `main` (default)
- **Protection**: Direct pushes discouraged; use pull requests
- **History**: Linear history maintained via rebase strategy

### Feature Branch Naming

Use descriptive branch names following the pattern:

- `feature/component-functionality-description`
- `fix/component-issue-description`
- `security/component-security-improvement`
- `docker/container-enhancement-description`
- `config/configuration-update-description`

Examples:

```bash
feature/vm-console-management
fix/proxmox-api-timeout-handling
security/token-encryption-implementation
docker/non-root-user-setup
config/ssl-verification-default
test/vm-command-execution-coverage
docs/installation-guide-update
```

## Pull Request Guidelines

### PR Title Format

Follow the same conventions as commit messages:

```
type: brief description of the change
```

### PR Description Template

```markdown
## Summary

Brief overview of the change and its purpose.

## ProxmoxMCP Impact

- **Affected Components**: List of impacted ProxmoxMCP components (tools, config, core, formatting)
- **MCP Protocol Changes**: Any MCP protocol or tool registration modifications
- **Proxmox API Impact**: Changes to Proxmox API usage or authentication
- **Breaking Changes**: Required configuration updates or manual steps
- **Security Implications**: Security-related considerations

## Testing

- [ ] Unit tests pass (`pytest`)
- [ ] Type checking passes (`mypy .`)
- [ ] Code formatting applied (`black .`)
- [ ] Proxmox connection tested
- [ ] Docker build successful (if applicable)
- [ ] MCP tools function correctly

## Deployment Notes

- Configuration file updates required
- Environment variable changes needed
- Docker image rebuild necessary
- Any special considerations for deployment or rollback
```

## GitHub Integration Best Practices

### Issue Linking

- Always link commits to GitHub issues when applicable
- Use `Fixes #123` or `Closes #123` in commit messages
- Reference issues in PR descriptions for tracking
- Link to roadmap phases when implementing planned features

### Development Validation Commands

Before committing ProxmoxMCP changes, verify with:

```bash
# Run all quality checks
pytest && black . && mypy .

# Test MCP server startup
export PROXMOX_MCP_CONFIG="proxmox-config/config.json"
python -m proxmox_mcp.server

# Docker build test (if Docker changes made)
docker compose build

# Configuration validation
python -c "from proxmox_mcp.config.loader import load_config; load_config()"
```

### Security Considerations

- **Never commit secrets**: Use environment variables or external config files
- **Validate token encryption**: Test encryption/decryption functionality
- **Verify SSL settings**: Ensure proper SSL configuration
- **Test authentication**: Verify Proxmox API token functionality
- **Review permissions**: Check MCP tool permissions and access controls

## Workflow Integration

### Pre-commit Checklist

1. Run development validation commands
2. Check commit message follows `.gitmessage` template
3. Verify no secrets in tracked files
4. Test affected MCP tools individually
5. Ensure documentation is updated
6. Verify Docker compatibility (if applicable)
7. Check roadmap alignment for new features

### Post-commit Actions

1. Monitor MCP server health after deployment
2. Verify Proxmox API connectivity
3. Test MCP tool functionality
4. Review server logs for issues
5. Update any related documentation
6. Update roadmap progress if milestone reached

## Repository Structure Considerations

When making changes, consider the ProxmoxMCP architecture:

- **Core Components**: Server implementation in `src/proxmox_mcp/server.py`
- **Configuration**: Config handling in `src/proxmox_mcp/config/`
- **Tools**: MCP tool implementations in `src/proxmox_mcp/tools/`
- **Formatting**: Output formatting in `src/proxmox_mcp/formatting/`
- **Docker**: Container configuration in `Dockerfile` and `compose.yaml`
- **Tests**: Test suite in `tests/`
- **Documentation**: Project docs in `docs/` and `README.md`

All changes should maintain the MCP protocol compliance and Proxmox API integration patterns.
