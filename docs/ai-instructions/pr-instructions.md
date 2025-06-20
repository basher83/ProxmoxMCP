# Pull Request Instructions

This document provides comprehensive guidelines for Claude Code when working with pull
requests in the ProxmoxMCP repository. Follow these instructions to ensure consistent,
high-quality PR review, testing, and merging that aligns with project standards.

## Pre-PR Analysis Phase

### 1. Pull Request Assessment

- **Read the complete PR description** carefully, including all comments and updates
- Identify the **PR type** from labels (bug fix, enhancement, feature, security, etc.)
- Determine **affected components** (server, config, tools, formatting, docker, etc.)
- Check for **linked issues** and dependencies
- Review **acceptance criteria** and implementation scope
- Assess **breaking changes** and backward compatibility impact

### 2. Codebase Integration Analysis

- Use `Glob` and `Grep` tools to understand how changes fit into existing code structure
- Review related implementations and architectural patterns
- Identify integration points and potential conflicts
- Check for consistency with ProxmoxMCP design principles
- Assess impact on MCP protocol compliance and Proxmox API integration

## PR Review Phase

### 3. Code Quality Assessment

#### Code Implementation Review

- **Follow existing architectural patterns** from the codebase
- Ensure **consistency** with ProxmoxMCP design principles:
  - MCP protocol compliance and tool registration patterns
  - Proxmox API integration and error handling
  - Pydantic validation models for all inputs
  - Rich formatting with ProxmoxTheme consistency
  - Comprehensive error handling with specific exceptions

#### Security Review

- **Verify no secrets exposure** in code, logs, or outputs
- Check **input validation** for all user inputs and API parameters
- Review **authentication flows** and token handling
- Assess **command execution security** for VM operations
- Verify **configuration encryption** handling if applicable
- Check **SSL/TLS configurations** for network communications

#### ProxmoxMCP-Specific Pattern Compliance

- **Tool inheritance**: New tools inherit from ProxmoxTool base class
- **Pydantic validation**: All configuration and API parameters use Pydantic models
- **Rich formatting**: Consistent use of ProxmoxTheme and ProxmoxFormatters
- **Error handling**: Comprehensive error handling with specific exception types
- **Async patterns**: Proper async implementation for VM operations
- **Type safety**: Type hints for all functions and methods

### 4. Testing and Validation Requirements

#### Automated Testing Review

- **Verify comprehensive test coverage** for new functionality
- **Check existing test patterns** are followed from the test suite
- **Ensure mocked Proxmox API calls** in tests to avoid live server dependencies
- **Validate error condition testing** and edge case coverage
- **Confirm backward compatibility** testing when modifying existing code

#### Manual Testing Requirements

- **Test MCP tool functionality** individually with realistic scenarios
- **Verify Proxmox API integration** if applicable (connection, authentication, operations)
- **Test error handling paths** and fallback mechanisms
- **Validate output formatting** consistency across different scenarios
- **Check configuration loading** if config changes are involved

### 5. Documentation and Communication Review

#### Documentation Updates

- **Verify relevant documentation** updates in `docs/` directory
- **Check tool descriptions** in `tools/definitions.py` for new MCP tools
- **Validate README.md updates** if adding user-facing features
- **Ensure examples demonstrate** new functionality appropriately

#### Commit Message Quality

- **Follow commit message template** from `.gitmessage`
- **Use appropriate commit type**: feat, fix, security, config, docker, refactor, test, docs, ci, perf
- **Include detailed commit body** explaining what and why (not how)
- **Reference linked issues** with "Fixes #issue-number" or "Closes #issue-number"
- **Mention affected components** and any breaking changes

## Testing and Validation Phase

### 6. Pre-Merge Quality Assurance

#### Comprehensive Testing Execution

Run all required quality checks in the PR environment:

```bash
# Core quality checks (required for all PRs)
pytest && black . && mypy .

# ProxmoxMCP-specific validation
export PROXMOX_MCP_CONFIG="proxmox-config/config.json"
python -m proxmox_mcp.server  # Test server startup

# Docker validation (if Docker changes involved)
docker compose build && docker compose up --build -d
```

#### Integration Testing

- **Test MCP tool integration** with realistic Proxmox environments
- **Verify tool registration** and discovery in MCP server
- **Test configuration loading** and environment variable handling
- **Validate API authentication** and connection management
- **Check formatting output** in various scenarios and themes

#### Security Testing

- **Review for secret exposure** in code changes and test outputs
- **Test authentication mechanisms** if authentication is modified
- **Validate input sanitization** for command execution features
- **Check encryption/decryption** functionality if security features are involved
- **Verify file permissions** for any created or modified files

### 7. Performance and Compatibility Assessment

#### Performance Impact Analysis

- **Assess performance implications** of code changes
- **Check for potential memory leaks** or resource consumption issues
- **Evaluate API call efficiency** and rate limiting considerations
- **Test with realistic data volumes** (multiple VMs, large configurations)

#### Compatibility Verification

- **Test backward compatibility** with existing configurations
- **Verify Python version compatibility** (3.10+)
- **Check dependency compatibility** and version constraints
- **Test across deployment methods** (pip install, Docker, development)

## Approval and Merge Phase

### 8. Final Validation and Approval

#### Component-Specific Validation

**Server Component** (`src/proxmox_mcp/server.py`):

- Verify FastMCP patterns and tool registration
- Check dependency injection and service management
- Validate signal handling for new services

**Tools Component** (`src/proxmox_mcp/tools/`):

- Confirm ProxmoxTool inheritance and consistent error handling
- Validate rich formatting implementation via templates
- Check tool descriptions in `definitions.py`

**Configuration** (`src/proxmox_mcp/config/`):

- Verify Pydantic model validation and backward compatibility
- Test environment variable fallbacks and field documentation

**Formatting** (`src/proxmox_mcp/formatting/`):

- Check ProxmoxTheme consistency and reusable formatting functions
- Validate emoji and color toggle support

**Docker** (`Dockerfile`, `compose.yaml`):

- Verify security best practices and health checks
- Test environment variable configuration and volume mounts

#### Breaking Changes Assessment

- **Document all breaking changes** clearly in PR description
- **Provide migration guidance** for configuration or API changes
- **Ensure proper versioning** if breaking changes are introduced
- **Test upgrade scenarios** from previous versions

### 9. Merge Execution and Validation

#### Pre-Merge Checklist

- [ ] All automated tests pass consistently
- [ ] Manual testing completed successfully
- [ ] Documentation is updated appropriately
- [ ] Security review completed without issues
- [ ] Performance impact assessed and acceptable
- [ ] Backward compatibility maintained or breaking changes documented
- [ ] Code quality checks pass (pytest, black, mypy)
- [ ] Integration tests with Proxmox API successful
- [ ] Commit messages follow project standards

#### Merge Strategy

- **Use squash and merge** for feature branches to maintain clean history
- **Preserve individual commits** for complex changes that benefit from detailed history
- **Follow linear history preference** from git configuration
- **Update branch protection rules** if merging requires special permissions

## Post-Merge Phase

### 10. Post-Merge Validation and Monitoring

#### Immediate Validation

- **Monitor MCP server health** after deployment changes
- **Verify Proxmox API connectivity** and authentication
- **Test affected MCP tools** in production-like environment
- **Review server logs** for any new errors or warnings
- **Validate configuration loading** in deployed environment

#### Knowledge Capture and Documentation

- **Document new architectural decisions** and implementation patterns
- **Store security best practices** and configuration approaches
- **Update development workflow** documentation if processes changed

### 11. Continuous Improvement

#### Feedback Integration

- **Monitor for related issues** or bug reports after merge
- **Collect performance metrics** if performance-related changes were made
- **Document lessons learned** for future similar PRs
- **Update PR template** if review process reveals gaps

#### Roadmap Alignment

- **Update roadmap progress** if milestones were achieved
- **Identify follow-up tasks** or technical debt created
- **Plan future improvements** based on implementation experience

## Component-Specific PR Guidelines

### Server Component PRs

- Focus on FastMCP compliance and tool registration patterns
- Verify proper dependency injection and configuration management
- Test server startup, shutdown, and signal handling
- Validate MCP protocol message handling and routing

### Tools Component PRs

- Ensure all new tools inherit from ProxmoxTool base class
- Implement comprehensive error handling and logging
- Use rich formatting templates for consistent output
- Add tool descriptions to `definitions.py` registry

### Configuration PRs

- Use Pydantic models for all new configuration options
- Maintain backward compatibility with existing config files
- Support environment variable fallbacks
- Document all new configuration fields

### Security-Related PRs

- Follow responsible disclosure practices for vulnerability fixes
- Implement defense-in-depth security measures
- Add comprehensive security testing and validation
- Document security implications and best practices

### Performance PRs

- Include benchmarking data and performance analysis
- Test with realistic workloads and data volumes
- Consider memory usage and resource consumption
- Validate performance improvements meet expectations

## Anti-Patterns to Avoid

### Code Quality Pitfalls

- **Don't approve PRs** that bypass type checking or code formatting
- **Don't merge PRs** without comprehensive test coverage
- **Don't ignore security implications** of code changes
- **Don't skip integration testing** for ProxmoxMCP-specific functionality

### Process Pitfalls

- **Don't merge without thorough review** of all changed files
- **Don't ignore CI/CD failures** or quality check issues
- **Don't skip documentation updates** for user-facing changes
- **Don't merge breaking changes** without proper versioning and migration guides

### ProxmoxMCP-Specific Pitfalls

- **Don't bypass MCP protocol patterns** or tool registration requirements
- **Don't ignore Proxmox API error handling** for network and authentication failures
- **Don't skip rich formatting implementation** for output consistency
- **Don't hardcode Proxmox-specific values** that should be configurable

## Success Criteria

A pull request is successfully reviewed and ready for merge when:

1. **Code quality standards met** with passing tests and quality checks
2. **Security review completed** with no identified vulnerabilities
3. **Integration testing successful** with MCP and Proxmox API
4. **Documentation updated** appropriately for changes
5. **Backward compatibility maintained** or breaking changes properly documented
6. **Performance impact assessed** and acceptable
7. **Architectural consistency** with ProxmoxMCP design principles
8. **Commit history clean** with proper message formatting
9. **All required approvals** obtained from maintainers
10. **CI/CD pipeline passing** consistently

## Quick Reference Checklist

Before approving any PR, verify:

- [ ] Memory and context research completed for changes
- [ ] Code follows ProxmoxMCP architectural patterns
- [ ] Comprehensive testing added and passing
- [ ] Security considerations addressed
- [ ] Documentation updated appropriately
- [ ] Integration testing with Proxmox API completed
- [ ] Performance impact assessed
- [ ] Backward compatibility maintained
- [ ] Commit messages follow project standards
- [ ] All quality checks passing (pytest, black, mypy)
- [ ] Breaking changes documented with migration guidance
- [ ] Component-specific validation completed

This systematic approach ensures consistent, high-quality pull request review and
merging that maintains ProxmoxMCP's standards, security, and architectural integrity
while facilitating efficient development workflows.
