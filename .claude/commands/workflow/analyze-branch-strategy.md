# Branch analysis

Comprehensive branch analysis and merge strategy workflow: $ARGUMENTS

This workflow systematically analyzes all branches to optimize merge strategy and maintain
branch purpose alignment. Execute each phase methodically and maintain detailed analysis
throughout.

**IMPORTANT**: Always verify branch analysis against current GitHub state to ensure accuracy.

## Phase 1: Branch Discovery and Initial Assessment

Step 1.1: **Enumerate All Branches (Local and Remote)**

```bash
# Get all local branches with last commit info
git for-each-ref --format='%(refname:short) %(committerdate) %(authorname) %(subject)' refs/heads/ --sort=-committerdate

# Get all remote branches
git branch -r

# Verify against GitHub API for authoritative branch list
gh api repos/OWNER/REPO/branches | jq '.[].name'
```

Step 1.2: **Cross-Reference Local vs Remote State**

- Compare local branch list with GitHub remote branches
- Identify any stale local branches that no longer exist on GitHub
- Note discrepancies that may indicate outdated local state
- Focus on branches that exist on GitHub (authoritative source)

Step 1.3: **Identify Active Development Branches**

- Focus on branches modified within the last 30 days
- Exclude main/master and any deployment branches
- Note branch naming patterns (feature/, bugfix/, chore/, etc.)
- Verify branch existence on GitHub before detailed analysis

Step 1.4: **Create Branch Analysis Matrix**
For each GitHub-verified branch, create an initial assessment:

- Branch name and inferred purpose
- Last activity date and author
- Commit count vs main
- Estimated complexity (file count in diff)
- GitHub branch status confirmation

## Phase 2: Detailed Diff Analysis Per Branch

For each GitHub-verified branch identified in Phase 1, perform comprehensive analysis:

Step 2.1: **Verify Branch Exists and Get Complete Diff Against Main**

```bash
# First verify branch exists on GitHub
gh api repos/OWNER/REPO/branches/BRANCH_NAME || echo "Branch not found on GitHub"

# For each verified branch, get detailed diff
git diff main..BRANCH_NAME --name-status
git diff main..BRANCH_NAME --stat
git log main..BRANCH_NAME --oneline

# Check if branch has associated PRs
gh pr list --head BRANCH_NAME
```

Step 2.2: **Categorize Changes by Type**
Analyze each changed file and categorize:

A. **Infrastructure/Tooling Changes**

- Build configuration (package.json, Dockerfile, CI/CD)
- Linting rules, formatters, type definitions
- Development tooling and scripts
- Documentation updates (README, CONTRIBUTING)

B. **Code Quality Improvements**

- Refactoring without functional changes
- Performance optimizations
- Error handling improvements
- Code style consistency fixes
- Security enhancements

C. **Feature-Specific Implementation**

- New functionality directly related to branch purpose
- Feature-specific tests and documentation
- API changes specific to the feature
- Feature-specific configuration

D. **Bug Fixes**

- General bug fixes unrelated to feature
- Feature-specific bug fixes

Step 2.3: **Cross-Reference with Branch Purpose**
For each branch, extract the intended purpose from:

- Branch name (feature/mcp-claude-sdk-integration)
- Initial commit messages
- Any associated issues or PRs
- Code changes that clearly indicate intent

## Phase 3: Merge Strategy Analysis

Step 3.1: **Immediate Merge Candidates**
Identify changes that should be merged to main immediately:

**High-Priority Immediate Merge:**

- Critical bug fixes affecting main branch
- Security improvements
- CI/CD fixes that benefit all development
- Linting/formatting rule updates
- Documentation improvements
- Development tooling enhancements

**Medium-Priority Immediate Merge:**

- Code quality refactoring with no functional impact
- Performance optimizations in shared code
- Test infrastructure improvements
- Configuration management improvements

Step 3.2: **Branch-Specific Retention**
Changes that should remain in feature branch:

- Incomplete feature implementations
- Feature-specific tests for unreleased functionality
- Experimental code or work-in-progress
- Breaking changes that require coordination
- Feature-specific documentation for unreleased features

Step 3.3: **Anomaly Detection and Stale Branch Identification**
Flag branches with concerning patterns:

- Feature branches with extensive unrelated changes
- Old branches with changes that should have been merged
- Branches with conflicting approaches to same problem
- Branches that might have merge conflicts
- **Stale local branches**: Local branches that no longer exist on GitHub
- **Analysis report inconsistencies**: Branches mentioned in previous reports but missing from GitHub

## Phase 4: Strategic Recommendations

Step 4.1: **Generate Merge Recommendations**
For each branch, create specific recommendations:

1. **Immediate Action Items:**
   - List specific files/changes for immediate cherry-pick to main
   - Estimated effort and risk assessment
   - Suggested PR title and description

2. **Branch Continuation Strategy:**
   - What should remain in the branch
   - Estimated completion timeline
   - Dependencies and blockers

3. **Branch Hygiene Improvements:**
   - Suggestions for better branch management
   - Recommended rebasing or cleanup actions

Step 4.2: **Create Implementation Plan**
Generate a prioritized action plan:

```markdown
## Branch Analysis Summary

### Immediate Merge Queue (Priority Order)
1. [Branch Name] - [Specific Changes] - [Estimated Effort]
2. [Branch Name] - [Specific Changes] - [Estimated Effort]

### Cherry-Pick Candidates
- Branch: feature/mcp-claude-sdk-integration
  - Files for immediate merge: eslint.config.js, .github/workflows/quality.yml
  - Reason: Linting improvements benefit all development
  - Action: Create PR "Improve linting configuration from feature branch"

### Branch Continuation Recommendations
- Branch: feature/mcp-claude-sdk-integration
  - Keep: src/mcp-integration/, tests/mcp/, docs/mcp-integration.md
  - Estimated completion: 2-3 weeks
  - Blockers: API design finalization

### Branch Hygiene Actions
- [Branch Name]: Rebase against current main, resolve conflicts
- [Branch Name]: Consider splitting into smaller focused branches
```

## Phase 5: Execution and Automation

Step 5.1: **Create Automated Actions**
Generate specific git commands for immediate execution:

```bash
# Example cherry-pick operations
git checkout main
git pull origin main
git checkout -b chore/quality-improvements-from-feature-branches

# Cherry-pick specific commits
git cherry-pick -x [commit-hash] # Quality improvements from feature/branch-a
git cherry-pick -x [commit-hash] # Documentation from feature/branch-b
```

Step 5.2: **Integration with Project Automation**
Create follow-up actions that integrate with your existing CI/CD:

- Generate GitHub issues for immediate merge PRs
- Create tracking issues for branch completion
- Update project documentation with branch status
- Schedule follow-up branch analysis

## Phase 6: Reporting and Documentation

Step 6.1: **Create Comprehensive Report**
Generate detailed report including:

- Executive summary of findings
- **GitHub branch verification status**
- Branch-by-branch analysis (GitHub-verified only)
- **Stale branch cleanup recommendations**
- Immediate action items with timelines
- Long-term branch strategy recommendations
- Metrics: lines of code, file changes, estimated merge complexity
- **Discrepancy analysis**: Previous reports vs current GitHub state

Step 6.2: **Update Project Documentation**

- Update @CONTRIBUTING.md with branch management insights
- Create or update branch strategy documentation
- Document any new processes discovered during analysis

## Special Considerations for ProxmoxMCP Project

**Domain-Specific Analysis:**

- Ensure MCP server changes stay in appropriate branches
- Verify Proxmox API integration changes align with feature goals
- Check that configuration examples match their intended branches
- Validate that documentation updates correspond to feature completeness

**Quality Automation Integration:**

- Leverage your existing pytest && black . && mypy . && ruff check . pipeline
- Consider how immediate merges affect your GitHub automation workflows
- Ensure changes don't break your claude-issue-assignment automation

**Security and Configuration Review:**

- Pay special attention to authentication and API key handling changes
- Review any Proxmox configuration changes for security implications
- Ensure MCP server configurations are properly scoped

## Report Generation and Storage

Step 6.1: **Create Report Directory Structure**

```bash
# Create reports directory if it doesn't exist
mkdir -p .claude/reports/branch-analysis
```

Step 6.2: **Generate Timestamped Report**
Save the complete analysis to a timestamped file:

**Report Location:** @.claude/reports/branch-analysis/

Example: `.claude/reports/branch-analysis/branch-analysis-20241217-143022.md`

Step 6.3: **Create Current Analysis Symlink**

```bash
# Create symlink to latest report for easy access
ln -sf branch-analysis-$(date +%Y%m%d-%H%M%S).md .claude/reports/branch-analysis/latest.md
```

## Output Format

Save the analysis in this structured format to the report file:

```markdown
# Branch Analysis Report - [Date]
**Report Location:** .claude/reports/branch-analysis/branch-analysis-YYYYMMDD-HHMMSS.md
**Analysis Scope:** $ARGUMENTS
**Git Commit:** $(git rev-parse HEAD)
**GitHub Verification:** $(date) - Authoritative source check completed

## Executive Summary
- Total GitHub branches: X
- Total local branches: X
- Stale local branches detected: X
- Immediate merge candidates: X files across Y branches
- Estimated effort for immediate merges: X hours
- Branches requiring attention: X

## GitHub Branch Verification
- ✅ Verified GitHub branches: [list]
- ❌ Stale local branches: [list]
- 🔄 Analysis report discrepancies: [previous vs current]

## Detailed Findings
[For each GitHub-verified branch...]

## Stale Branch Cleanup
- Local branches to delete: [list with cleanup commands]
- Previous analysis inconsistencies: [explanation]

## Immediate Action Plan
[Prioritized list with commands...]

## Follow-up Recommendations
[Strategic improvements...]

## Report Metadata
- Analysis Duration: X minutes
- GitHub Branches Examined: [list]
- Local Branches Examined: [list]
- Git Status at Analysis: [clean/dirty]
- GitHub API Status: [success/failure]
- Next Recommended Analysis: [date]
```

Step 6.4: **Update Analysis Index**
Maintain an index of all branch analyses:

**Index Location:** @.claude/reports/branch-analysis/INDEX.md

```markdown
# Branch Analysis History

## Recent Analyses
- [2024-12-17 14:30] Latest comprehensive analysis - 15 branches, 8 immediate actions
- [2024-12-10 09:15] Weekly review - 12 branches, 3 quality improvements
- [2024-12-03 16:45] Post-release cleanup - 18 branches, 12 merges completed

## Analysis Trends
- Average branches per analysis: X
- Most common immediate merge types: [quality, docs, tooling]
- Branch completion velocity: X days average
```

**Important:**

1. **Always verify against GitHub API** before analyzing any branch
2. **Cross-reference with previous reports** to identify cleanup opportunities
3. Always save the complete report to the timestamped file before executing any git operations
4. Present the saved report location for easy reference
5. This analysis is meant to inform decisions, not automatically execute changes
6. The report serves as documentation for future development planning
7. **Include stale branch cleanup** as part of repository hygiene
8. **Note any discrepancies** between local state and GitHub authoritative source
