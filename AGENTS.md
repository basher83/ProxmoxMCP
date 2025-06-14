# Contributor Guide

## Essential Actions

### Quality Checks (Required Before Committing)

```bash
# Run all quality checks sequentially
pytest && black . && mypy . && ruff .

# Or individually
pytest          # Run test suite
black .         # Code formatting
mypy .          # Type checking
ruff .          # Linting and import sorting
```

### Development Environment

```bash
# Set up virtual environment
uv venv
source .venv/bin/activate  # Linux/macOS
.\.venv\Scripts\Activate.ps1  # Windows

# Install dependencies
uv pip install -e ".[dev]"

# Configure environment
export PROXMOX_MCP_CONFIG="proxmox-config/config.json"
```

### Commit Guidelines

- **Follow commit message template** from `.gitmessage`
- **Use semantic commit types**: feat, fix, security, config, docker, refactor, test, docs, ci, perf
- **Include ProxmoxMCP impact** in commit body
- **Reference issue numbers** with "Fixes #123"
- **Never commit secrets** - use environment variables

### Security Requirements

- ⚠️ **No secrets in code** - use `PROXMOX_MCP_CONFIG` and environment variables
- ⚠️ **Validate input sanitization** for VM command execution
- ⚠️ **Test authentication flows** if auth is involved
- ⚠️ **Review encryption patterns** for sensitive data

### ProxmoxMCP Architecture Patterns

- **Inherit from ProxmoxTool** for new tool implementations
- **Use Pydantic models** for all configuration and validation
- **Implement rich formatting** using ProxmoxTheme and ProxmoxFormatters
- **Follow async patterns** for VM operations when applicable
- **Add comprehensive error handling** with specific exception types

## Documentation References

### Core Documentation

- **@CLAUDE.md** - Primary development instructions and commands
- **@CONTRIBUTING.md** - Pull request workflow and code standards
- **@docs/development-workflow.md** - CI/CD and automation details

### AI Workflow Instructions

- **@docs/ai-instructions/memory-instructions.md** - Memory management workflow _(mem0 server unavailable in Codex; ignore this workflow)_
- **@docs/ai-instructions/context-instructions.md** - Context research workflow
- **@docs/ai-instructions/github-instructions.md** - Git and GitHub best practices
- **@docs/ai-instructions/issue-creation-instructions.md** - Creating well-structured issues
- **@docs/ai-instructions/issue-resolution-instructions.md** - Resolving issues systematically

### Quick References

- **Git Config**: `cp example.gitconfig .git/config`
- **MCP Settings**: `example.mcp_settings.json`
- **Config Template**: `proxmox-config/config.example.json`
- **Roadmap**: `docs/ROADMAP.md`

## Testing Requirements

- **All 71+ tests must pass**
- **Add tests for new functionality**
- **Mock Proxmox API calls in tests**
- **Test error conditions and edge cases**
- **Ensure backward compatibility**

## Common Pitfalls to Avoid

- Don't hardcode configuration values - use config system
- Don't break existing API compatibility without proper versioning
- Don't skip error handling - follow comprehensive error patterns
- Don't ignore type checking - resolve all mypy issues
- Don't commit without running quality checks
- Don't bypass MCP protocol patterns - maintain compatibility
