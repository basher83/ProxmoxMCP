#!/bin/bash
# Pre-bash security check hook for ProxmoxMCP
# Validates commands before execution to prevent security issues

# Get the command from environment
COMMAND=$(echo "$CLAUDE_TOOL_ARGUMENTS" | jq -r '.command // empty')

# Security patterns to check
DANGEROUS_PATTERNS=(
    "rm -rf /"
    "dd if=/dev/zero"
    "mkfs"
    "> /dev/sda"
    "chmod 777"
    "curl.*\|.*sh"
    "wget.*\|.*sh"
)

# Credential exposure patterns
CREDENTIAL_PATTERNS=(
    "PROXMOX_API_TOKEN"
    "password="
    "token="
    "secret="
)

# Check for dangerous commands
for pattern in "${DANGEROUS_PATTERNS[@]}"; do
    if echo "$COMMAND" | grep -qE "$pattern"; then
        echo "❌ BLOCKED: Potentially dangerous command detected: $pattern"
        echo "Command: $COMMAND"
        exit 1
    fi
done

# Check for credential exposure
for pattern in "${CREDENTIAL_PATTERNS[@]}"; do
    if echo "$COMMAND" | grep -qE "$pattern.*=.*['\"]"; then
        echo "⚠️  WARNING: Command may expose credentials"
        echo "Consider using environment variables instead"
        # Log but don't block
    fi
done

# Check for ProxmoxMCP specific paths
if echo "$COMMAND" | grep -q "proxmox-config"; then
    echo "🔒 Security Notice: Accessing Proxmox configuration"
fi

echo "✅ Security check passed"
exit 0