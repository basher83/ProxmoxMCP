# Claude Code Automation

This repository is configured to work with Claude Code automation for issue
resolution. When you assign an issue to Claude Code, it will automatically create
a branch, implement the solution, and create a pull request.

## How It Works

### 1. Creating an Issue for Claude Code

Use the "Claude Code Task" issue template or manually:

1. Create a new issue
2. Add the `claude-code` label
3. Assign to `claude-code-bot` (or ensure the label is present)
4. Provide clear requirements and acceptance criteria

### 2. Automatic Process

When an issue is assigned to Claude Code, the automation will:

1. **Create Branch**: Generate a new branch named `claude/issue-{number}-{title}`
2. **Comment**: Add a comment to the issue indicating work has started
3. **Implement**: Analyze requirements and implement the solution
4. **Quality Checks**: Run tests, formatting, and type checking
5. **Commit**: Create meaningful commits with the changes
6. **Pull Request**: Create a PR linking back to the issue

### 3. Review Process

After Claude Code completes the work:

1. Review the generated pull request
2. Check that all requirements are met
3. Run additional tests if needed
4. Merge when satisfied or request changes

## Configuration Requirements

### Repository Secrets

The following secrets must be configured in your repository:

- `ANTHROPIC_API_KEY`: Your Anthropic API key for Claude Code
- `GITHUB_TOKEN`: Automatically provided by GitHub Actions

### Permissions

The workflow requires the following permissions:

- `contents: write` - To create branches and commits
- `issues: write` - To comment on issues
- `pull-requests: write` - To create pull requests
- `id-token: write` - For authentication

### Environment Requirements

- **Python Version**: The workflow uses Python 3.10+ (required for MCP SDK compatibility)
- **Package Manager**: Uses `uv` for fast dependency installation
- **Development Tools**: Includes pytest, black, mypy, and ruff for quality checks

### Workflow Configuration

The automation is configured in `.github/workflows/claude-issue-assignment.yml` with:

```yaml
assignee_trigger: "basher83,claude-code-bot"  # Users who can trigger automation
allowed_tools: "bash,read,write,edit,glob,grep"  # Tools Claude Code can use
timeout_minutes: "120"  # Maximum execution time
```

## Issue Template Guidelines

When creating issues for Claude Code, include:

### Clear Task Description

```markdown
## Task Description
Add support for VM snapshot management in the Proxmox MCP server.
```

### Specific Requirements

```markdown
## Requirements
- [ ] Add `create_vm_snapshot` tool
- [ ] Add `delete_vm_snapshot` tool
- [ ] Add `restore_vm_snapshot` tool
- [ ] Include proper error handling
```

### Acceptance Criteria

```markdown
## Acceptance Criteria
- [ ] All tools follow existing patterns in tools/ directory
- [ ] Proper Pydantic models for validation
- [ ] Rich formatted output
- [ ] Tests included
```

### Technical Details

```markdown
## Technical Details
- Use the existing ProxmoxManager pattern
- Follow the formatting standards in formatting/ module
- Add to tools/vm.py or create tools/snapshot.py
```

## Best Practices

### For Issue Creation

- Be specific about requirements
- Provide examples of expected behavior
- Include error cases to handle
- Reference existing code patterns when applicable

### For Review

- Check that the solution follows project conventions
- Verify tests are comprehensive
- Ensure documentation is updated if needed
- Test the implementation manually if possible

## Troubleshooting

### Common Issues

**Workflow doesn't trigger:**

- Ensure the issue has the `claude-code` label
- Check that the assignee is in the `assignee_trigger` list (`basher83` or `claude-code-bot`)
- Verify repository secrets are configured
- Confirm the workflow file is on the main branch

**Python dependency errors:**

- The workflow requires Python 3.10+ for MCP SDK compatibility
- Check that `pyproject.toml` specifies `requires-python = ">=3.10"`
- Verify MCP dependencies are compatible with the Python version

**Implementation fails:**

- Check the workflow logs for detailed error messages
- Ensure the task description is clear and actionable
- Verify the requirements don't conflict with existing code
- Check that the `ANTHROPIC_API_KEY` secret is properly configured

**Quality checks fail:**

- The workflow runs: `pytest && black . && mypy .`
- Claude Code will attempt to fix issues automatically
- Manual intervention may be needed for complex conflicts
- Check individual tool logs for specific failures

**Missing ASSIGNEE_TRIGGER error:**

- Ensure `assignee_trigger` parameter is set in the workflow
- Add your GitHub username to the trigger list
- Verify the workflow configuration matches the action requirements

### Debugging Steps

1. **Check workflow run logs**: Go to Actions tab → failed run → view logs
2. **Verify issue setup**: Confirm labels, assignee, and issue description
3. **Test locally**: Run `uv pip install -e ".[dev]"` to check dependencies
4. **Check secrets**: Ensure `ANTHROPIC_API_KEY` is configured in repository settings

### Getting Help

If you encounter issues with the automation:

1. Check the GitHub Actions logs for detailed error information
2. Review the issue description for clarity and completeness
3. Ensure all required repository secrets are configured
4. Verify Python and dependency compatibility
5. Create a support issue if problems persist

## Workflow Execution Details

### Step-by-Step Process

When an issue is assigned to trigger the automation, the following steps occur:

1. **Branch Creation**

   ```bash
   # Creates branch name from issue number and title
   BRANCH_NAME="claude/issue-${ISSUE_NUMBER}-${CLEAN_TITLE}"
   git checkout -b "$BRANCH_NAME"
   git push origin "$BRANCH_NAME"
   ```

2. **Environment Setup**

   ```bash
   # Set up Python 3.10 environment
   uv venv
   source .venv/bin/activate
   uv pip install -e ".[dev]"
   ```

3. **Claude Code Implementation**
   - Analyzes issue requirements and codebase
   - Implements solution following project patterns
   - Runs quality checks: `pytest && black . && mypy .`
   - Creates meaningful commits with proper messages

4. **Pull Request Creation**
   - Automatic PR with descriptive title
   - Links back to the original issue
   - Includes summary of changes made
   - Ready for review and testing

### Quality Assurance

The workflow automatically runs these checks:

- **pytest**: All test suites must pass
- **black**: Code formatting compliance
- **mypy**: Type checking validation
- **Project patterns**: Follows existing code conventions

## Example Workflow

1. **Create Issue**: Use the Claude Code Task template

   ```
   Title: [CLAUDE] Add VM backup scheduling feature
   Description: Clear requirements and acceptance criteria
   Labels: claude-code, automation
   Assignee: basher83
   ```

2. **Automatic Processing**:
   - Workflow triggers on assignment
   - Creates branch `claude/issue-123-add-vm-backup-scheduling-feature`
   - Adds comment to issue with progress updates

3. **Implementation**:
   - Code is analyzed, written, and tested
   - All quality checks must pass
   - Multiple commits with descriptive messages

4. **Pull Request**:
   - PR #124 created automatically
   - Links to issue #123 with "Closes #123"
   - Includes implementation summary

5. **Review**: You review and merge the PR

6. **Completion**: Issue #123 is automatically closed

This automation streamlines the development process while maintaining code quality and project standards.
