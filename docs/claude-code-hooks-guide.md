# Claude Code Hooks Guide for ProxmoxMCP

## Overview

This guide explains how to use Claude Code hooks to enhance your development workflow in the ProxmoxMCP
project. Hooks provide automated quality checks, security validation, and helpful notifications during
your Claude Code sessions.

## Quick Start

To enable hooks for your ProxmoxMCP development, you have three options:

### Option 1: Project-Level Settings (Recommended)

```bash
# Copy hooks to project-level settings (committed to repo)
cp claude-code-hooks.json .claude/settings.json

# This allows all team members to use the same hooks
```

### Option 2: Local Project Settings (Not Committed)

```bash
# Copy hooks to local project settings (gitignored)
cp claude-code-hooks.json .claude/settings.local.json

# This is for personal customizations
```

### Option 3: User-Level Settings (All Projects)

```bash
# Copy hooks to user-level settings
cp claude-code-hooks.json ~/.claude/settings.json

# Or merge with existing settings
jq -s '.[0] * .[1]' ~/.claude/settings.json claude-code-hooks.json > ~/.claude/settings.new.json
mv ~/.claude/settings.new.json ~/.claude/settings.json
```

**Note**: Settings file locations:

- User-level: `~/.claude/settings.json`
- Project-level: `.claude/settings.json`
- Local project: `.claude/settings.local.json`

## Implemented Hooks

### 1. Security Validation Hooks

**Pre-Bash Security Check** (`pre-bash-security-check.sh`)

- Validates commands before execution
- Blocks potentially dangerous operations
- Warns about credential exposure
- Monitors access to sensitive configuration files

Example blocked patterns:

- `rm -rf /`
- Direct disk operations (`dd`, `mkfs`)
- Overly permissive chmod operations
- Credential exposure in command lines

### 2. Code Quality Hooks

**Pre-Code Quality Check** (`pre-code-quality-check.sh`)

- Validates Python syntax before edits
- Provides context-aware warnings for different file types
- Reminds about ProxmoxMCP-specific patterns

**Post-Edit Format** (`post-edit-format.sh`)

- Automatically formats Python files with Black
- Runs Ruff auto-fixes
- Validates JSON syntax
- Provides file-specific reminders

**Post-Markdown Lint** (`post-markdown-lint.sh`)

- Validates markdown files against project rules
- Uses `.markdownlint.jsonc` configuration
- Suggests auto-fix commands for issues
- Checks for common markdown problems

### 3. Quality Assurance Hooks

**Post-Bash Validation** (`post-bash-validation.sh`)

- Analyzes command results
- Provides helpful tips for failed tests
- Tracks command history
- Gives context-specific feedback

**Post-Quality Report** (`post-quality-report.sh`)

- Generates comprehensive quality reports
- Tracks test coverage
- Counts type errors and linting issues
- Monitors TODO/FIXME items
- Checks for security patterns

### 4. Notification and Logging

**Notification Handler** (`notification-handler.sh`)

- Sends desktop notifications (if available)
- Color-coded terminal output
- Logs all notifications with timestamps

**Session Summary** (`session-summary.sh`)

- Generates end-of-session reports
- Lists modified files
- Provides recommendations
- Tracks ProxmoxMCP-specific changes

## Usage Examples

### Example 1: Running Tests with Feedback

When you run:

```bash
pytest
```

The hooks will:

1. Log the command execution
2. Analyze the results
3. Provide success/failure feedback
4. Suggest next steps if tests fail

### Example 2: Editing Python Files

When editing a Python file:

```python
# Edit src/proxmox_mcp/tools/new_tool.py
```

The hooks will:

1. Check current file syntax
2. Remind about ProxmoxTool inheritance
3. Auto-format with Black after edit
4. Run Ruff fixes
5. Remind to register the tool

### Example 3: Security Protection

If you accidentally try:

```bash
echo $PROXMOX_API_TOKEN > config.txt
```

The hook will:

1. Warn about credential exposure
2. Log the security concern
3. Suggest using environment variables

## Customization

### Adding New Hooks

1. Create a new script in `/scripts/hooks/`
2. Add the hook configuration to `claude-code-hooks.json`
3. Make the script executable

Example custom hook:

```bash
#!/bin/bash
# Custom ProxmoxMCP-specific validation
# Add your custom logic here
```

### Modifying Existing Hooks

All hooks are in `/scripts/hooks/` and can be customized:

- Adjust security patterns in `pre-bash-security-check.sh`
- Add new quality checks in `post-quality-report.sh`
- Customize notifications in `notification-handler.sh`

## Best Practices

1. **Review Hook Output**: Pay attention to warnings and suggestions
2. **Keep Hooks Fast**: Hooks should complete quickly to avoid blocking
3. **Test Hooks**: Run hooks manually to verify behavior
4. **Log Review**: Periodically check `.claude/logs/` for patterns
5. **Update Patterns**: Adjust security patterns based on your needs

## Troubleshooting

### Hooks Not Running

1. Verify settings file location:

   ```bash
   # Check user-level settings
   cat ~/.claude/settings.json | jq '.hooks'
   
   # Check project-level settings
   cat .claude/settings.json | jq '.hooks'
   
   # Check local project settings
   cat .claude/settings.local.json | jq '.hooks'
   ```

2. Check script permissions:

   ```bash
   ls -la /workspaces/ProxmoxMCP/scripts/hooks/
   ```

3. Test hooks manually:

   ```bash
   CLAUDE_TOOL_ARGUMENTS='{"command":"pytest"}' bash scripts/hooks/pre-bash-security-check.sh
   ```

### Hook Blocking Valid Operations

If a hook incorrectly blocks an operation:

1. Review the hook script
2. Adjust patterns as needed
3. Use exit code 0 to allow, 1 to block

### Performance Issues

If hooks slow down operations:

1. Add timeouts to long-running checks
2. Run expensive checks asynchronously
3. Cache results where appropriate

## Integration with ProxmoxMCP Workflow

The hooks are designed to support the ProxmoxMCP quality assurance workflow:

1. **Pre-commit checks** run automatically
2. **Security validation** prevents credential leaks
3. **Quality reports** track code health
4. **Session summaries** help with task tracking

## Advanced Features

### JSON Output for Tool Control

Hooks can return JSON to control tool behavior:

```bash
#!/bin/bash
# Return JSON to provide additional context
cat <<EOF
{
  "message": "Custom validation passed",
  "data": {
    "coverage": "95%",
    "issues": 0
  }
}
EOF
```

### Conditional Hook Execution

Use matchers for fine-grained control:

```json
{
  "matcher": "pytest.*--cov",
  "hooks": [{
    "type": "command",
    "command": "scripts/hooks/coverage-report.sh"
  }]
}
```

## Security Considerations

- Hooks run with your user permissions
- Never store credentials in hook scripts
- Validate all inputs in hook scripts
- Use read-only operations where possible
- Log security events for audit trails

## Future Enhancements

Potential improvements for ProxmoxMCP hooks:

1. **Proxmox API validation** - Verify API calls before execution
2. **Automated documentation updates** - Update docs on code changes
3. **Performance monitoring** - Track operation durations
4. **Integration testing hooks** - Run integration tests automatically
5. **Deployment readiness checks** - Validate before deployments
