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

#### For Bug Reports

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

#### For Enhancement Requests

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

#### Required Labels (Choose One Primary Type)

- `bug` - For defects and issues
- `enhancement` - For new features and improvements
- `security` - For security-related issues
- `documentation` - For documentation improvements
- `performance` - For performance issues

#### Priority Labels (Choose One)

- `priority:critical` - Security vulnerabilities, system-breaking bugs
- `priority:high` - Important features, significant bugs
- `priority:medium` - Normal features and improvements
- `priority:low` - Nice-to-have features, minor issues

#### Component Labels (Choose Relevant Ones)

- `component:server` - MCP server core
- `component:config` - Configuration system
- `component:tools` - Tool implementations
- `component:formatting` - Output formatting
- `component:docker` - Docker/containerization
- `component:authentication` - Auth and security
- `component:api` - Proxmox API integration
- `component:testing` - Test infrastructure

#### Effort Labels (Choose One)

- `effort:small` - Hours to days of work
- `effort:medium` - Days to weeks of work
- `effort:large` - Weeks to months of work

#### Status Labels (Optional)

- `status:needs-investigation` - Requires research
- `status:confirmed` - Issue reproduced and verified
- `status:blocked` - Cannot proceed due to dependencies

#### Community Labels (Optional)

- `good-first-issue` - Suitable for newcomers
- `help-wanted` - Community assistance welcome

## ProxmoxMCP-Specific Considerations

### 7. Architectural Alignment

Ensure the issue aligns with ProxmoxMCP architecture:

- **MCP Protocol Compliance**: How does this integrate with MCP standards?
- **Proxmox API Integration**: What Proxmox APIs are involved?
- **Tool Organization**: Which tools or tool categories are affected?
- **Configuration Management**: Are config changes needed?
- **Rich Formatting**: How should output be formatted?

### 8. Security and Privacy

- **Never include sensitive information** (tokens, passwords, IPs)
- **Redact configuration files** before pasting
- **Consider security implications** of all requests
- **Mark security issues appropriately** with security labels

### 9. Integration Points

Consider how the issue relates to:

- **Existing MCP tools** and their functionality
- **Proxmox VE versions** and compatibility
- **Docker deployment** scenarios
- **Authentication mechanisms** and token management
- **Configuration encryption** and security

## Issue Lifecycle Management

### 10. Initial Creation

- **Use templates** when available
- **Assign appropriate labels** from the start
- **Link to related issues** if applicable
- **Add to project boards** if part of planned work

### 11. Follow-up Actions

After creating an issue:

- **Monitor for questions** and provide clarifications
- **Update labels** as understanding evolves
- **Link to implementation PRs** when work begins
- **Close with summary** when resolved

## Quality Checklist

Before creating an issue, verify:

- [ ] **Title is clear and descriptive**
- [ ] **Issue type is correctly identified**
- [ ] **All required sections are filled out**
- [ ] **Appropriate labels are assigned**
- [ ] **No sensitive information is included**
- [ ] **Related issues are linked**
- [ ] **ProxmoxMCP-specific considerations are addressed**
- [ ] **Acceptance criteria are clear** (for enhancements)
- [ ] **Steps to reproduce are detailed** (for bugs)
- [ ] **Security implications are considered**

## Examples of Well-Formed Issues

### Bug Report Example

```
Title: [BUG] VM command execution timeout with QEMU guest agent

Labels: bug, priority:high, component:tools, effort:medium

Body includes:
- Clear environment details
- Step-by-step reproduction
- Expected vs actual behavior
- Error logs and stack traces
- ProxmoxMCP component impact analysis
```

### Enhancement Example

```
Title: [ENHANCEMENT] Add batch command execution for multiple VMs

Labels: enhancement, priority:medium, component:tools, effort:large

Body includes:
- Clear use case and value proposition
- Detailed implementation proposal
- Architectural considerations
- Security and performance implications
- Comprehensive acceptance criteria
```

### Security Issue Example

```
Title: [SECURITY] Implement input sanitization for VM commands

Labels: security, priority:critical, component:tools, effort:medium

Body includes:
- Security impact assessment
- Current vulnerable behavior
- Proposed security controls
- Implementation requirements
- Testing strategy
```

## Anti-Patterns to Avoid

### Common Mistakes

- **Vague titles** like "Fix the bug" or "Add feature"
- **Missing component identification**
- **No acceptance criteria** for enhancements
- **Including sensitive information** in public issues
- **Duplicate issues** without checking existing ones
- **Wrong priority assignment** (everything isn't critical)
- **Missing reproduction steps** for bugs
- **No consideration of ProxmoxMCP architecture**

### Quality Issues

- **One-line descriptions** without detail
- **No labels or incorrect labels**
- **Missing security considerations**
- **No testing requirements**
- **Ignoring existing patterns and conventions**

---

## Integration with Development Workflow

### 12. Roadmap Alignment

- **Check roadmap phases** for priority alignment
- **Consider implementation timeline** relative to project goals
- **Identify dependencies** on other roadmap items

### 13. Automation Integration

- **Label for Claude Code** if suitable for automation
- **Consider autofix.ci** implications for code quality
- **Plan for automated testing** and validation

### 14. Documentation Impact

- **Identify documentation updates** needed
- **Plan for README changes** if user-facing
- **Consider workflow documentation** updates

This systematic approach to issue creation ensures that all GitHub issues are well-structured, properly categorized, and contain the information needed for efficient resolution while maintaining ProxmoxMCP's quality standards and architectural integrity.
