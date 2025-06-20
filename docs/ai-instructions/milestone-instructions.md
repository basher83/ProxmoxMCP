# Milestone Management Instructions

This document provides comprehensive guidelines for Claude Code when working with GitHub
milestones in the ProxmoxMCP repository. Follow these instructions to ensure consistent
milestone management that aligns with project development phases and roadmap objectives.

## Overview and Purpose

### What are Milestones in ProxmoxMCP?

Milestones represent significant development phases in the ProxmoxMCP project lifecycle,
each with specific goals, features, and release targets. They help organize issues and
pull requests by version, track progress toward release objectives, and maintain
development focus on key deliverables.

### ProxmoxMCP Milestone Strategy

The project follows a structured release strategy:

- **v0.9.0**: Pre-Release Stabilization - Security, testing, documentation
- **v1.0.0**: First Stable Release - Production-ready core functionality  
- **v1.1.0**: Enhanced Features - Extended tool coverage and optimizations
- **v1.2.0**: Production Hardening - Enterprise features and scalability

## Milestone Management Workflow

### 1. Research and Context Analysis

Before creating or modifying milestones:

- Review existing milestones: `gh milestone list`
- Check current roadmap alignment in `docs/ROADMAP.md`
- Analyze issue distribution across milestones
- Consider ProxmoxMCP development priorities and dependencies

### 2. Milestone Creation

#### Creating New Milestones

Use the GitHub CLI to create milestones with comprehensive descriptions:

```bash
# Create milestone with all required fields
gh milestone create "v0.9.0" \
  --description "Security improvements, core functionality testing, documentation completion, Docker optimization" \
  --due-date "2025-08-15"
```

#### ProxmoxMCP-Specific Milestone Descriptions

Each milestone should include:

- **Security implications** and requirements
- **Core functionality** changes and stability targets
- **Documentation** requirements and updates
- **Testing** and quality assurance goals
- **Docker and deployment** considerations

### 3. Issue Assignment to Milestones

#### Assigning Issues During Creation

```bash
gh issue create \
  --title "[ENHANCEMENT] Add LXC container management support" \
  --milestone "v1.1.0" \
  --label "enhancement,component:tools,priority:medium" \
  --body "Detailed issue description..."
```

#### Assigning Existing Issues

```bash
# Assign by issue number
gh issue edit 42 --milestone "v1.0.0"

# Assign with additional modifications
gh issue edit 42 --milestone "v1.0.0" --add-label "priority:high"
```

#### Batch Assignment for Related Issues

```bash
# Find related issues and assign to milestone
gh issue list --label "component:security" --json number | \
  jq -r '.[].number' | \
  xargs -I {} gh issue edit {} --milestone "v0.9.0"
```

### 4. Milestone Monitoring and Management

#### Viewing Milestone Progress

```bash
# List all milestones with progress
gh milestone list

# View specific milestone details
gh milestone view "v1.0.0"

# Check milestone completion status
gh api repos/basher83/ProxmoxMCP/milestones --jq '.[] | select(.title=="v1.0.0") | {title, open_issues, closed_issues}'
```

#### Updating Milestone Information

```bash
# Update description or due date
gh milestone edit "v0.9.0" \
  --description "Updated: Security improvements, core functionality testing, documentation completion" \
  --due-date "2025-09-15"
```

## ProxmoxMCP Integration Guidelines

### 5. Component-Based Milestone Planning

#### Server Component Milestones

- Focus on MCP protocol compliance and FastMCP integration
- Include authentication and security improvements
- Plan for configuration management enhancements

#### Tools Component Milestones

- Organize by Proxmox functionality (VM, storage, cluster, node operations)
- Consider tool dependency relationships
- Plan for error handling and rich formatting consistency

#### Security Milestones

- Prioritize authentication and encryption features
- Include input validation and secure configuration
- Plan for security testing and vulnerability assessments

#### Documentation Milestones

- Align with feature releases and API changes
- Include installation guides and deployment documentation
- Plan for user guides and troubleshooting resources

### 6. Milestone Validation and Quality Assurance

#### Pre-Release Milestone Validation

Before closing a milestone, ensure:

- All critical issues are resolved
- Security requirements are met
- Documentation is updated
- Testing requirements are fulfilled
- Docker and deployment functionality is verified

#### Post-Release Milestone Review

After milestone completion:

- Analyze completion metrics and timeline accuracy
- Document lessons learned for future planning
- Update roadmap based on actual progress
- Plan follow-up milestones based on feedback

## Advanced Milestone Operations

### 7. Milestone Analytics and Reporting

#### Progress Tracking

```bash
# Generate milestone progress report
gh api repos/basher83/ProxmoxMCP/milestones | \
  jq '.[] | {title, state, open_issues, closed_issues, due_on}' > milestone_progress.json
```

#### Issue Distribution Analysis

```bash
# Analyze issues by component and milestone
gh issue list --milestone "v1.0.0" --json labels,title,number | \
  jq '.[] | select(.labels[] | .name | startswith("component:")) | 
    {number, title, component: [.labels[] | select(.name | startswith("component:")) | .name]}'
```

### 8. Milestone Cleanup and Maintenance

#### Removing Milestone Assignments

```bash
# Remove milestone from issue
gh issue edit 42 --milestone ""

# Bulk remove milestone from all issues
gh issue list --milestone "old-milestone" --json number | \
  jq -r '.[].number' | \
  xargs -I {} gh issue edit {} --milestone ""
```

#### Deleting Obsolete Milestones

```bash
# Delete milestone (only after removing all assignments)
gh milestone delete "obsolete-milestone"
```

## Integration with Development Workflow

### 9. Continuous Integration with Milestones

#### Pre-commit Milestone Validation

- Verify issue assignments align with current development focus
- Check milestone progress before major commits
- Ensure new features align with milestone objectives

#### Release Planning Integration

- Use milestone completion as release readiness indicator
- Plan testing phases around milestone deliverables
- Coordinate documentation updates with milestone closures

### 10. Roadmap Synchronization

#### Milestone-Roadmap Alignment

- Ensure milestones reflect roadmap phase objectives
- Update roadmap based on milestone progress and challenges
- Maintain consistency between milestone descriptions and roadmap goals

#### Timeline Management

- Regularly review milestone due dates against actual progress
- Adjust timelines based on complexity and dependencies
- Communicate timeline changes through milestone updates

## Best Practices and Anti-Patterns

### Best Practices

- **Clear milestone descriptions** with specific, measurable goals
- **Regular milestone review** and progress assessment
- **Component-based issue organization** within milestones
- **Security-first milestone planning** for ProxmoxMCP requirements
- **Documentation synchronization** with milestone releases

### Anti-Patterns to Avoid

- **Overly broad milestones** without specific deliverables
- **Ignoring component dependencies** when planning milestones
- **Milestone scope creep** without proper evaluation
- **Missing security considerations** in milestone planning
- **Disconnected milestone and roadmap objectives**

## Quick Reference Commands

### Essential Milestone Commands

```bash
# List all milestones
gh milestone list

# Create new milestone
gh milestone create "TITLE" --description "DESC" --due-date "YYYY-MM-DD"

# View milestone details
gh milestone view "MILESTONE_NAME"

# Edit milestone
gh milestone edit "MILESTONE_NAME" --description "NEW_DESC" --due-date "YYYY-MM-DD"

# Assign issue to milestone
gh issue edit ISSUE_NUMBER --milestone "MILESTONE_NAME"

# Remove milestone assignment
gh issue edit ISSUE_NUMBER --milestone ""

# Delete milestone
gh milestone delete "MILESTONE_NAME"
```

### ProxmoxMCP-Specific Examples

```bash
# Create v0.9.0 milestone
gh milestone create "v0.9.0" \
  --description "Security improvements, core functionality testing, documentation completion, Docker optimization" \
  --due-date "2025-08-15"

# Assign security issue to v0.9.0
gh issue edit 45 --milestone "v0.9.0" --add-label "component:authentication,priority:high"

# View v1.0.0 progress
gh milestone view "v1.0.0"
```

This structured approach ensures consistent milestone management that supports
ProxmoxMCP's development workflow, maintains project organization, and facilitates
efficient progress tracking toward release objectives.
