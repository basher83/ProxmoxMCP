# Issue Creation Instructions

This document provides comprehensive guidelines for Claude Code when creating GitHub
issues in the ProxmoxMCP repository. Follow these instructions to ensure consistent,
well-structured issues that align with project standards and facilitate efficient
resolution.

## Pre-Creation Analysis

### 1. Issue Classification

Determine the appropriate issue type based on the problem or request:

- **bug**: Something isn't working correctly
- **enhancement**: New feature or request
- **security**: Security-related issues or improvements
- **documentation**: Improvements or additions to documentation
- **performance**: Performance-related issues or improvements
- **question**: Further information is requested

### 2. Scope and Impact Assessment

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

### 3. Title Format

Use clear, descriptive titles following these patterns:

```
[TYPE] Brief description of the issue or feature
```

**Examples:**

- `[BUG] VM command execution fails with timeout errors`
- `[ENHANCEMENT] Add LXC container management support`
- `[SECURITY] Implement rate limiting for API calls`
- `[DOCUMENTATION] Update installation guide for Docker deployment`

### 4. Issue Body Template

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

````markdown
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
````

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

#### For Security Issues

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

### 5. Label Assignment Guidelines

#### Required Labels (Choose One Primary Type)

- `bug` - For defects and issues
- `enhancement` - For new features and improvements
- `security` - For security-related issues
- `documentation` - For documentation improvements
- `performance` - For performance issues

#### Priority Labels (Choose One)

- `priority:critical` - Immediate attention required, blocks critical functionality
- `priority:high` - Important issue, should be addressed in current iteration
- `priority:medium` - Standard priority, address in upcoming iterations
- `priority:low` - Nice to have, address when time permits

#### Component Labels (Choose All That Apply)

- `component:server` - Core MCP server implementation
- `component:config` - Configuration system and loading
- `component:tools` - MCP tool implementations
- `component:formatting` - Output formatting and theming
- `component:docker` - Docker and containerization
- `component:authentication` - Authentication and security
- `component:api` - Proxmox API integration
- `component:testing` - Test suite and testing infrastructure

#### Effort Estimation Labels (Choose One)

- `effort:small` - 1-2 hours of work
- `effort:medium` - Half day to 1 day of work
- `effort:large` - 2-3 days of work
- `effort:xl` - More than 3 days of work

#### Status Labels (Applied Automatically)

- `status:triage` - Needs initial review and classification
- `status:blocked` - Cannot proceed due to dependencies
- `status:in-progress` - Currently being worked on
- `status:review` - Ready for code review
- `status:testing` - In testing phase

#### Community Labels

- `good first issue` - Suitable for new contributors
- `help wanted` - Community assistance appreciated
- `question` - Seeking clarification or information

## ProxmoxMCP-Specific Considerations

### 6. MCP Protocol Compliance

When creating issues related to MCP functionality:

- **Protocol Version**: Specify which MCP protocol version is affected
- **Tool Categories**: Identify which MCP tool categories are involved
- **Resource Management**: Consider impact on MCP resource handling
- **Client Compatibility**: Assess effects on MCP client interactions

### 7. Proxmox Integration Specifics

For Proxmox VE related issues:

- **API Version Compatibility**: Specify Proxmox VE API version requirements
- **Authentication Methods**: Consider PAM, PVE, or API token impacts
- **Node vs Cluster**: Specify if issue affects single node or cluster operations
- **Resource Types**: Identify affected Proxmox resources (VMs, LXC, storage, network)

### 8. Security and Privacy

Always consider security implications:

- **Credential Handling**: How does the issue affect credential management?
- **Data Exposure**: What sensitive data might be exposed?
- **Network Security**: Are there network-level security concerns?
- **Access Control**: How does this affect user permissions and access?

## Issue Lifecycle Management

### 9. Initial Triage Process

After creating an issue:

1. **Automatic Labels**: `status:triage` is automatically applied
2. **Community Review**: Issues are reviewed within 48 hours
3. **Priority Assignment**: Critical issues get immediate attention
4. **Component Assignment**: Relevant maintainers are notified

### 10. Issue Updates and Communication

#### Progress Updates

- Provide regular updates for long-running issues
- Tag relevant maintainers when additional input is needed
- Update labels as status changes (in-progress, blocked, etc.)

#### Community Engagement

- Be responsive to questions and clarification requests
- Provide additional context when requested
- Test proposed solutions and provide feedback

## Quality Checklist

### 11. Before Submitting

- [ ] **Title is clear and descriptive**
- [ ] **Appropriate issue type is selected**
- [ ] **All relevant labels are applied**
- [ ] **Template is fully completed**
- [ ] **Examples or reproduction steps are provided**
- [ ] **Security implications are considered**
- [ ] **Related issues are referenced**
- [ ] **Configuration details are included (sanitized)**

### 12. Content Quality Standards

- **Be Specific**: Avoid vague descriptions like "it doesn't work"
- **Include Context**: Provide environment and configuration details
- **Show Examples**: Include code snippets, commands, or screenshots
- **Consider Impact**: Explain how this affects users or the project
- **Suggest Solutions**: Propose potential fixes or workarounds when possible

## Examples and Best Practices

### 13. Good Issue Examples

#### Example 1: Clear Bug Report

```
[BUG] VM startup command fails with authentication timeout

## Summary
When executing VM startup commands through ProxmoxMCP, operations timeout after 30
seconds with authentication errors, even with valid credentials.

## Environment
- ProxmoxMCP Version: 0.3.0
- Proxmox VE Version: 8.1.4
- Platform: Docker (Alpine Linux)
- Python Version: 3.11.6

## Steps to Reproduce
1. Configure ProxmoxMCP with API token authentication
2. Execute: `tools/vm_start.py --vm-id 100`
3. Wait for timeout error

## Expected Behavior
VM should start successfully within configured timeout period.

## Actual Behavior
Operation fails with: "Authentication timeout after 30 seconds"
```

#### Example 2: Well-Structured Enhancement

```
[ENHANCEMENT] Add batch operations for VM management

## Summary
Enable batch operations for common VM tasks (start, stop, reboot) to improve efficiency when managing multiple VMs.

## Use Case
System administrators managing large VM deployments need to perform operations on
multiple VMs simultaneously rather than executing commands individually.

## Proposed Implementation
Add batch operation support to existing VM management tools with proper error
handling and progress reporting.
```

### 14. Anti-Patterns to Avoid

#### Poor Examples

❌ **Vague Title**: "VM stuff broken"
❌ **Missing Context**: "It doesn't work on my system"
❌ **No Reproduction Steps**: "Random errors sometimes"
❌ **Multiple Issues**: Combining unrelated problems in one issue
❌ **Missing Labels**: Not categorizing or prioritizing the issue

## Integration with Development Workflow

### 15. Issue-to-PR Workflow

1. **Issue Creation**: Follow guidelines in this document
2. **Discussion**: Engage with maintainers for clarification
3. **Assignment**: Issue is assigned to developer or taken by community
4. **Development**: Work begins with reference to issue number
5. **Pull Request**: PR links back to issue for tracking
6. **Review**: Code review process includes issue validation
7. **Closure**: Issue is closed when PR is merged

### 16. Branch Naming Convention

When working on issues, use branch names that reference the issue:

- `fix/issue-123-vm-timeout-errors`
- `feature/issue-456-batch-operations`
- `security/issue-789-auth-improvements`

### 17. Commit Message Format

Reference issues in commit messages:

```
fix: resolve VM startup timeout issues

- Increase default timeout from 30s to 60s
- Add retry logic for authentication failures
- Improve error messaging for timeout scenarios

Fixes #123
```

## Conclusion

Following these comprehensive guidelines ensures that issues created in the ProxmoxMCP repository are:

- **Well-structured** and easy to understand
- **Properly categorized** with appropriate labels
- **Actionable** with clear reproduction steps or requirements
- **Aligned** with project goals and architecture
- **Helpful** for both maintainers and community contributors

Remember: A well-written issue is the foundation of effective problem-solving and
feature development. Take time to provide complete information upfront to facilitate
faster resolution and better collaboration.

For questions about these guidelines or help with issue creation, reach out to the
maintainers or community through the project's communication channels.
