# Issue Creation Instructions

This document provides comprehensive guidelines for Claude Code when creating GitHub issues in the ProxmoxMCP repository. Follow these instructions to ensure consistent, well-structured issues that align with project standards and facilitate efficient resolution.

## Pre-Creation Analysis

### 1. Memory and Context Research

- **ALWAYS start** by using `get_all_coding_preferences` to understand existing patterns
- Use `search_coding_preferences` to find related implementations or similar issues
- Review existing open issues to avoid duplicates: `gh issue list`
- Check the roadmap (`docs/ROADMAP.md`) to understand project priorities

### 2. Issue Classification

Determine the appropriate issue type based on the problem or request:

- **bug**: Something isn't working correctly
- **enhancement**: New feature or request  
- **security**: Security-related issues or improvements
- **documentation**: Improvements or additions to documentation
- **performance**: Performance-related issues or improvements
- **question**: Further information is requested

### 3. Scope and Impact Assessment

Identify which ProxmoxMCP components are affected:

- **component:server** - Core MCP server implementation
- **component:config** - Configuration system and loading
- **component:tools** - MCP tool implementations  
- **component:formatting** - Output formatting and theming
- **component:docker** - Docker and containerization
- **component:authentication** - Authentication and security
- **component:api** - Proxmox API integration
- **component:testing** - Test suite and testing infrastructure

## Issue Structure and Content

### 4. Title Format
Use clear, descriptive titles following these patterns:

```
[TYPE] Brief description of the issue or feature
```

**Examples:**
- `[BUG] VM command execution fails with timeout errors`
- `[ENHANCEMENT] Add LXC container management support`
- `[SECURITY] Implement rate limiting for API calls`
- `[DOCUMENTATION] Update installation guide for Docker deployment`

### 5. Issue Body Template

#### For Bug Reports:
```markdown
## Summary
Brief description of the bug and its impact.

## Environment
- **ProxmoxMCP Version**: [version]
- **Proxmox VE Version**: [version] 
- **Platform**: [Linux/Windows/macOS/Docker]
- **Python Version**: [version]

## Steps to Reproduce
1. Step one
2. Step two  
3. Step three

## Expected Behavior
What should happen.

## Actual Behavior
What actually happens.

## Error Output
```
[Paste error messages, logs, or stack traces here]
```

## ProxmoxMCP Impact
- **Affected Components**: [List of components]
- **MCP Protocol Impact**: [Any MCP-specific issues]
- **Proxmox API Impact**: [API-related problems]
- **Security Implications**: [If applicable]

## Additional Context
- Configuration details (redacted of sensitive info)
- Related issues or pull requests
- Workarounds attempted

## Proposed Solution
[If you have ideas for fixing the issue]
```

#### For Enhancement Requests:
```markdown
## Summary
Brief description of the proposed feature and its value.

## Use Case
Describe the problem this enhancement solves and who benefits.

## Proposed Implementation
Detailed description of how this could be implemented.

### Technical Details
- **Affected Components**: [List of components that would be modified]
- **MCP Protocol Changes**: [Any MCP protocol modifications needed]
- **Proxmox API Integration**: [New API endpoints or usage]
- **Configuration Changes**: [New config options needed]

### Code Examples
```python
# Example of proposed API or usage
def new_feature():
    pass
```

## ProxmoxMCP Integration
- **Architectural Considerations**: [How this fits with existing design]
- **Security Implications**: [Security considerations]
- **Performance Impact**: [Expected performance implications]
- **Breaking Changes**: [Any breaking changes required]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Implementation Notes
- **Dependencies**: [Required libraries or external dependencies]
- **Testing Requirements**: [What tests need to be added]
- **Documentation Updates**: [What docs need updating]

## Timeline
[Estimated timeline or priority level]
```

#### For Security Issues:
```markdown
## Security Issue Summary
Brief description of the security concern (avoid detailed exploit info in public issues).

## Severity Assessment
- **Impact**: [High/Medium/Low]
- **Likelihood**: [High/Medium/Low]
- **CVSS Score**: [If applicable]

## Affected Components
- **Components**: [List of affected ProxmoxMCP components]
- **Attack Vectors**: [How the vulnerability could be exploited]
- **Data at Risk**: [What sensitive data could be compromised]

## Current Behavior
Description of the current insecure behavior.

## Proposed Security Enhancement
How to address the security concern.

## Implementation Requirements
- **Authentication Changes**: [If auth is involved]
- **Encryption Requirements**: [If encryption is needed]
- **Input Validation**: [If input validation is required]
- **Access Controls**: [If permissions need updating]

## Testing Requirements
- [ ] Security test cases
- [ ] Penetration testing
- [ ] Code review requirements

## Timeline
[Urgency level - critical security issues should be marked priority:critical]
```

### 6. Label Assignment Guidelines

#### Required Labels (Choose One Primary Type):
- `bug` - For defects and issues
- `enhancement` - For new features and improvements
- `security` - For security-related issues
- `documentation` - For documentation improvements
- `performance` - For performance issues

#### Priority Labels (Choose One):
- `priority:critical`