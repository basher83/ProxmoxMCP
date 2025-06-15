#!/bin/bash
# GitHub Issues Creation Script for ProxmoxMCP Roadmap
# This script creates issues based on the ROADMAP.md phases

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo -e "${RED}Error: GitHub CLI (gh) is not installed.${NC}"
    echo "Please install it from: https://cli.github.com/"
    exit 1
fi

# Check if user is authenticated
if ! gh auth status &> /dev/null; then
    echo -e "${RED}Error: Not authenticated with GitHub CLI.${NC}"
    echo "Please run: gh auth login"
    exit 1
fi

echo -e "${BLUE}Creating ProxmoxMCP Roadmap Issues...${NC}"

# Function to create issue
create_issue() {
    local title="$1"
    local labels="$2"
    local body="$3"

    if gh issue create --title "$title" --label "$labels" --body "$body"; then
        echo -e "${GREEN}✓ Created issue: $title${NC}"
    else
        echo -e "${RED}✗ Failed to create issue: $title${NC}"
    fi
}

# Phase 1: Critical Security Fixes
echo -e "${BLUE}Creating Phase 1: Critical Security Fixes...${NC}"

create_issue \
    "[SECURITY] Implement token encryption at rest" \
    "security,priority:critical,component:config,effort:medium" \
    "## Overview
Implement token encryption for sensitive data in configuration files to enhance security.

## Implementation Tasks
- [ ] Add cryptography.fernet dependency to requirements
- [ ] Update src/proxmox_mcp/config/loader.py with encryption functions
- [ ] Implement key management system
- [ ] Add token encryption/decryption methods
- [ ] Update configuration loading to handle encrypted tokens

## Code Implementation
Add to src/proxmox_mcp/config/loader.py:
```python
import os
from cryptography.fernet import Fernet

def encrypt_token(token: str, key: bytes) -> str:
    \"\"\"Encrypt sensitive tokens\"\"\"
    f = Fernet(key)
    return f.encrypt(token.encode()).decode()

def decrypt_token(encrypted_token: str, key: bytes) -> str:
    \"\"\"Decrypt sensitive tokens\"\"\"
    f = Fernet(key)
    return f.decrypt(encrypted_token.encode()).decode()
```

## Acceptance Criteria
- [ ] Tokens are encrypted at rest
- [ ] Key rotation mechanism implemented
- [ ] Backward compatibility maintained
- [ ] Documentation updated
- [ ] Security tests added

## Timeline
1-2 days

## Related Files
- src/proxmox_mcp/config/loader.py
- src/proxmox_mcp/config/models.py
- requirements.in"

create_issue \
    "[SECURITY] Change default SSL verification to true" \
    "security,priority:high,component:config,effort:small" \
    "## Overview
Change default SSL verification from false to true for enhanced security by default.

## Implementation Tasks
- [ ] Update proxmox-config/config.example.json default value
- [ ] Update documentation to reflect secure defaults
- [ ] Add migration guide for existing users
- [ ] Update README installation instructions

## Changes Required
Update proxmox-config/config.example.json:
```json
{
    \"proxmox\": {
        \"host\": \"your-proxmox-host\",
        \"port\": 8006,
        \"verify_ssl\": true,
        \"service\": \"PVE\"
    }
}
```

## Acceptance Criteria
- [ ] Default verify_ssl changed to true
- [ ] Documentation updated with secure defaults
- [ ] Migration guide created for existing users
- [ ] Breaking change properly documented

## Timeline
Few hours

## Files to Update
- proxmox-config/config.example.json
- README.md
- docs/ (migration guide)"

create_issue \
    "[SECURITY] Implement VM command validation and sanitization" \
    "security,priority:critical,component:tools,effort:medium" \
    "## Overview
Add input validation and sanitization for VM commands to prevent injection attacks and enhance security.

## Implementation Tasks
- [ ] Add command validation in src/proxmox_mcp/tools/vm.py
- [ ] Implement command sanitization with shlex
- [ ] Create command whitelist/allowlist system
- [ ] Add command execution limits and timeouts
- [ ] Add audit logging for executed commands
- [ ] Add security tests for edge cases

## Code Implementation
```python
import shlex
import re
from typing import List, Set

class CommandValidator:
    ALLOWED_COMMANDS: Set[str] = {
        'systemctl', 'ls', 'ps', 'df', 'free', 'uname', 'cat', 'grep'
    }

    def validate_command(self, command: str) -> str:
        # Validate and sanitize shell commands
        if not command or len(command) > 1000:
            raise ValueError(\"Invalid command length\")

        # Check for dangerous patterns
        if re.search(r'[;&|`$()]', command):
            raise ValueError(\"Command contains dangerous characters\")

        # Sanitize command
        return shlex.quote(command)
```

## Security Considerations
- Prevent command injection attacks
- Limit command execution scope
- Add comprehensive logging
- Implement timeout protection

## Acceptance Criteria
- [ ] Command validation prevents injection
- [ ] Sanitization properly escapes dangerous characters
- [ ] Audit logging tracks all executed commands
- [ ] Security tests cover edge cases and attack vectors
- [ ] Documentation updated with security guidelines

## Timeline
1-2 days

## Related Files
- src/proxmox_mcp/tools/vm.py
- tests/test_vm_security.py (new)
- Security documentation"

# Phase 2: Docker Improvements
echo -e "${BLUE}Creating Phase 2: Docker Improvements...${NC}"

create_issue \
    "[DOCKER] Implement Docker security best practices" \
    "security,priority:high,component:docker,effort:medium" \
    "## Overview
Enhance Docker container security with non-root user execution, secrets management, and resource limits.

## Implementation Tasks
- [ ] Run container as non-root user from start
- [ ] Implement Docker secrets for sensitive credentials
- [ ] Add resource limits and health checks
- [ ] Update Dockerfile with security best practices
- [ ] Update docker-compose.yml with security enhancements
- [ ] Add container security documentation

## Dockerfile Improvements
```dockerfile
# Security: Run as non-root from the start
RUN groupadd -r mcp && useradd -r -g mcp mcp
USER mcp

# Add health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \\
  CMD python -m proxmox_mcp.health || exit 1
```

## Docker Compose Enhancements
```yaml
services:
  proxmox-mcp:
    secrets:
      - proxmox_token
    environment:
      PROXMOX_TOKEN_FILE: /run/secrets/proxmox_token
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
    restart: unless-stopped

secrets:
  proxmox_token:
    external: true
```

## Acceptance Criteria
- [ ] Container runs as non-root user
- [ ] Docker secrets implemented for credentials
- [ ] Resource limits configured
- [ ] Health checks functional
- [ ] Security documentation updated

## Timeline
1 day

## Files to Update
- Dockerfile
- compose.yaml
- README.md (Docker section)
- Security documentation"

# Phase 3: Error Handling
echo -e "${BLUE}Creating Phase 3: Error Handling...${NC}"

create_issue \
    "[ENHANCEMENT] Implement ProxmoxMCP-specific exception classes" \
    "enhancement,priority:medium,component:tools,effort:small" \
    "## Overview
Create specific exception classes for better error handling, debugging, and user experience.

## Implementation Tasks
- [ ] Create exception hierarchy in src/proxmox_mcp/tools/base.py
- [ ] Implement specific exception classes for different error types
- [ ] Update existing code to use new exceptions
- [ ] Add error handling documentation
- [ ] Add tests for exception handling

## Exception Classes to Implement
```python
class ProxmoxError(Exception):
    \"\"\"Base exception for Proxmox operations\"\"\"
    pass

class ProxmoxAuthError(ProxmoxError):
    \"\"\"Authentication-related errors\"\"\"
    pass

class ProxmoxResourceNotFoundError(ProxmoxError):
    \"\"\"Resource not found errors\"\"\"
    pass

class ProxmoxConnectionError(ProxmoxError):
    \"\"\"Connection-related errors\"\"\"
    pass

class ProxmoxConfigError(ProxmoxError):
    \"\"\"Configuration-related errors\"\"\"
    pass
```

## Acceptance Criteria
- [ ] Exception hierarchy created
- [ ] Specific exceptions for different error types
- [ ] Existing code updated to use new exceptions
- [ ] Error messages are user-friendly
- [ ] Tests cover exception scenarios

## Timeline
1 day

## Files to Update
- src/proxmox_mcp/tools/base.py
- All tool files to use new exceptions
- Test files for exception coverage"

create_issue \
    "[ENHANCEMENT] Add health check endpoint for monitoring" \
    "enhancement,priority:medium,component:server,effort:small" \
    "## Overview
Add health check tool for monitoring server and Proxmox connection status.

## Implementation Tasks
- [ ] Create health check tool in server
- [ ] Test Proxmox connection health
- [ ] Return structured health status
- [ ] Add health check documentation
- [ ] Integrate with Docker health checks

## Health Check Implementation
```python
@self.mcp.tool(description=\"Check MCP server and Proxmox connection health\")
def health_check():
    try:
        version = self.proxmox.version.get()
        return {
            \"status\": \"healthy\",
            \"proxmox_version\": version,
            \"timestamp\": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            \"status\": \"unhealthy\",
            \"error\": str(e),
            \"timestamp\": datetime.utcnow().isoformat()
        }
```

## Acceptance Criteria
- [ ] Health check tool implemented
- [ ] Returns structured status information
- [ ] Tests Proxmox connectivity
- [ ] Integrates with monitoring systems
- [ ] Documentation updated

## Timeline
1 day

## Files to Update
- src/proxmox_mcp/server.py
- Health check documentation
- Docker health check integration"

echo -e "${GREEN}✅ All roadmap issues created successfully!${NC}"
echo -e "${BLUE}Next steps:${NC}"
echo "1. Create the GitHub Project board manually using the web interface"
echo "2. Follow the instructions in .github/PROJECT_SETUP.md"
echo "3. Add the created issues to the project board"
echo "4. Begin implementing Phase 1 security fixes"
