# Issue Instructions

This document provides comprehensive guidelines for Claude Code when working on GitHub
issues in the ProxmoxMCP repository. Follow these instructions to ensure consistent,
high-quality issue resolution that aligns with project standards.

## Pre-Work Phase

### 1. Issue Analysis

- **Read the complete issue description** carefully, including all comments and updates
- Identify the **issue type** from labels (bug, enhancement, security, etc.)
- Determine **affected components** (server, config, tools, formatting, docker, etc.)
- Check for **linked issues** or dependencies
- Review any **acceptance criteria** provided
- Assess the **effort level** and complexity

### 2. Codebase Exploration

- Use `Glob` and `Grep` tools to understand relevant code structure
- Read existing implementations of similar functionality
- Identify integration points and dependencies
- Review test patterns for the affected components
- Check for existing error handling and logging patterns

## Implementation Phase

### 3. Planning and Architecture

- Create a **TodoWrite** task list breaking down the implementation
- Follow **existing architectural patterns** from the codebase
- Ensure **consistency** with ProxmoxMCP design principles:
  - MCP protocol compliance
  - Proxmox API integration patterns
  - Pydantic validation models
  - Rich formatting with themes
  - Comprehensive error handling

### 4. Code Implementation Guidelines

#### Security Considerations

- **Never expose secrets** in code, logs, or outputs
- Use **environment variables** for sensitive configuration
- Implement **input validation** for all user inputs
- Follow **principle of least privilege**
- Add **audit logging** for sensitive operations

#### ProxmoxMCP-Specific Patterns

- **Inherit from ProxmoxTool** for new tool implementations
- Use **Pydantic models** for all configuration and validation
- Implement **rich formatting** using ProxmoxTheme and ProxmoxFormatters
- Add **comprehensive error handling** with specific exception types
- Follow **async patterns** for VM operations when applicable

#### Code Quality Standards

- **Type hints required** for all functions and methods
- **Docstrings required** for all public functions and classes
- **Follow existing import organization** (will be enforced by autofix.ci)
- **Consistent naming conventions** with the codebase
- **No hardcoded values** - use configuration or constants

### 5. Testing Requirements

- **Add comprehensive tests** for new functionality
- **Use existing test patterns** from the test suite
- **Mock Proxmox API calls** in tests
- **Test error conditions** and edge cases
- **Ensure backward compatibility** when modifying existing code

### 6. Documentation Updates

- **Update relevant documentation** in `docs/` directory
- **Add tool descriptions** to `tools/definitions.py` for new MCP tools
- **Update README.md** if adding new features or changing installation
- **Add examples** to demonstrate new functionality

## Quality Assurance Phase

### 7. Pre-Commit Validation

Run all quality checks before committing:

```bash
# Required quality checks
pytest && black . && mypy .

# Additional validation for ProxmoxMCP
export PROXMOX_MCP_CONFIG="proxmox-config/config.json"
python -m proxmox_mcp.server  # Test server startup

# Docker validation (if applicable)
docker compose build
```

### 8. Security Validation

- **Review for secret exposure** in code and logs
- **Test authentication flows** if authentication is involved
- **Validate input sanitization** for command execution
- **Check SSL/TLS configurations** if network communication is involved
- **Review file permissions** for any created files

### 9. Integration Testing

- **Test MCP tool functionality** individually
- **Verify Proxmox API integration** if applicable
- **Test error handling paths** and fallback mechanisms
- **Validate output formatting** consistency
- **Check configuration loading** if config changes are made

## Commit and Documentation Phase

### 10. Commit Guidelines

- **Follow commit message template** from `.gitmessage`
- **Use appropriate commit type**: feat, fix, security, config, docker, refactor, test, docs, ci, perf
- **Include detailed commit body** explaining what and why (not how)
- **Reference the issue number** with "Fixes #issue-number"
- **Mention affected components** and breaking changes

## Component-Specific Guidelines

### Server Component (`src/proxmox_mcp/server.py`)

- Follow FastMCP patterns for tool registration
- Maintain clean dependency injection
- Add proper signal handling for new services
- Update tool descriptions in imports

### Tools Component (`src/proxmox_mcp/tools/`)

- Inherit from `ProxmoxTool` base class
- Use consistent error handling patterns
- Implement rich formatting via templates
- Add tool descriptions to `definitions.py`

### Configuration (`src/proxmox_mcp/config/`)

- Use Pydantic models for validation
- Support environment variable fallbacks
- Maintain backward compatibility
- Add field documentation

### Formatting (`src/proxmox_mcp/formatting/`)

- Use ProxmoxTheme for consistent styling
- Add reusable formatting functions
- Support emoji and color toggles
- Follow existing template patterns

### Docker (`Dockerfile`, `compose.yaml`)

- Follow security best practices (non-root user)
- Use specific version tags
- Add proper health checks
- Document environment variables

## Issue Type-Specific Guidelines

### Bug Fixes

- **Reproduce the issue** first to understand the problem
- **Identify root cause** rather than treating symptoms
- **Add regression tests** to prevent future occurrences
- **Consider backward compatibility** impacts

### Enhancement/Features

- **Design for extensibility** and future enhancement
- **Follow existing patterns** and architectural principles
- **Add comprehensive documentation** and examples
- **Consider performance implications**

### Security Issues

- **Treat with highest priority** and urgency
- **Avoid exposing sensitive information** in commits or logs
- **Add security tests** and validation
- **Document security considerations**

### Documentation Issues

- **Ensure accuracy** and completeness
- **Add practical examples** and use cases
- **Maintain consistency** with existing documentation style
- **Cross-reference related documentation**

## Common Pitfalls to Avoid

### Technical Pitfalls

- **Don't hardcode configuration values** - use config system
- **Don't break existing API compatibility** without proper versioning
- **Don't skip error handling** - follow comprehensive error patterns
- **Don't ignore type checking** - resolve all mypy issues

### Process Pitfalls

- **Don't skip testing** - all changes need test coverage
- **Don't commit secrets** - use environment variables
- **Don't ignore security implications** - consider attack vectors
- **Don't skip documentation** - undocumented features are unusable

### ProxmoxMCP-Specific Pitfalls

- **Don't bypass MCP protocol patterns** - maintain compatibility
- **Don't ignore Proxmox API error handling** - network issues are common
- **Don't skip rich formatting** - maintain consistent output style
- **Don't hardcode Proxmox-specific values** - use configuration

## Success Criteria

An issue is successfully resolved when:

1. **Functionality works** as described in the issue
2. **All tests pass** including new tests for the functionality
3. **Code quality checks pass** (pytest, black, mypy)
4. **Documentation is updated** appropriately
5. **Security considerations** are addressed
6. **Backward compatibility** is maintained (unless breaking change is intended)
7. **Integration tests pass** with Proxmox API (when applicable)
8. **Commit follows standards** with proper message and references

## Post-Implementation

### 11. Knowledge Capture

- **Document lessons learned** for future similar issues
- **Update architectural patterns** if new patterns emerge
- **Consider roadmap implications** for future development

### 12. Monitoring and Validation

- **Monitor for related issues** after implementation
- **Validate real-world usage** when possible
- **Be available for follow-up questions** and clarifications
- **Consider performance implications** in production environments

---

## Quick Reference Checklist

Before marking an issue as complete, verify:

- [ ] Issue requirements fully understood and addressed
- [ ] Implementation follows ProxmoxMCP architectural patterns
- [ ] Comprehensive tests added and passing
- [ ] Security considerations addressed
- [ ] Documentation updated appropriately
- [ ] Code quality checks passing (pytest, black, mypy)
- [ ] Integration testing completed
- [ ] Commit message follows template and references issue
- [ ] Backward compatibility maintained
- [ ] Performance implications considered

This systematic approach ensures consistent, high-quality issue resolution that
maintains ProxmoxMCP's standards and architectural integrity.
