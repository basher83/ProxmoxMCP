# ProxmoxMCP Task Completion Workflow

## Required Quality Checks
When completing any coding task, always run these commands in order:

### 1. Code Quality Pipeline
```bash
# Format code (required - fixes formatting issues)
black .

# Type checking (required - must pass without errors)
mypy .

# Lint and auto-fix (required - addresses code quality issues)
ruff .
```

### 2. Testing Pipeline
```bash
# Run comprehensive test suite (required - all tests must pass)
pytest

# Optional: Run category-specific tests if working on specific components
task test:security    # For authentication/encryption changes
task test:tools       # For MCP tool implementations
task test:config      # For configuration management changes
```

### 3. Configuration Validation
```bash
# Test server startup with configuration (required if config changes made)
export PROXMOX_MCP_CONFIG="proxmox-config/config.json"
python -m proxmox_mcp.server
```

### 4. Docker Validation (if applicable)
```bash
# Test Docker build if Dockerfile or compose changes made
docker compose build
```

## Automated Task Commands
For efficiency, use these combined task commands:

### Complete Pre-commit Workflow
```bash
task pre-commit
# Runs: format, lint:fix, type:check, yaml:lint:dev
```

### Full CI Simulation
```bash
task ci
# Runs: all quality checks + comprehensive test suite
```

### Quick Development Check
```bash
task quick
# Runs: format, lint:fix, test
```

## Quality Standards
All tasks must meet these criteria before completion:

1. **Zero Type Errors**: `mypy .` must pass without errors
2. **Code Formatting**: All code must be formatted with `black`
3. **Linting Clean**: `ruff` should report no issues
4. **Test Coverage**: All tests must pass, new features need tests
5. **Configuration Valid**: Server must start successfully if config touched
6. **Docker Compatible**: If Docker files changed, build must succeed

## Special Considerations

### ProxmoxMCP-Specific Validations
- **MCP Protocol Compliance**: Ensure new tools follow MCP patterns
- **Proxmox API Integration**: Test API connectivity if Proxmox code changed
- **Rich Formatting**: Verify output formatting consistency
- **Security**: No secrets in code, proper input validation

### Documentation Requirements
- Update relevant documentation in `docs/` if user-facing changes
- Add tool descriptions to `tools/definitions.py` for new MCP tools
- Update README.md if adding new features or changing installation

### Breaking Changes
- Test backward compatibility with existing configurations
- Document any breaking changes in commit messages
- Update migration guidance if configuration format changes

## Failure Handling
If any quality check fails:

1. **Fix the specific issue** reported by the tool
2. **Re-run the full pipeline** to ensure no regressions
3. **Test edge cases** related to the fix
4. **Update tests** if behavior intentionally changed

## Memory Updates
After completing significant tasks:
- Use coding preferences memory to capture new patterns
- Document architectural decisions for future reference
- Store security best practices and configuration patterns