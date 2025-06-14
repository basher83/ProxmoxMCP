---
name: Installation Help
about: Get help with ProxmoxMCP installation and setup
title: "[INSTALL] "
labels: help-wanted, installation
assignees: ""
---

## Installation Issue

<!-- Describe what's going wrong with your installation -->

## Installation Method

- [ ] Docker/Docker Compose
- [ ] Manual pip installation
- [ ] Development setup

## Where are you stuck?

- [ ] Environment setup (Python, UV)
- [ ] Dependency installation
- [ ] Configuration file setup
- [ ] Proxmox connection testing
- [ ] MCP server startup
- [ ] Other:

## Environment

- **Operating System**: <!-- e.g., Ubuntu 22.04, Windows 11 -->
- **Python Version**: <!-- e.g., 3.10.4 (run: python --version) -->

## Error Message

```
Paste the error message here
```

## Commands You Ran

```bash
# Show the exact commands you ran
git clone https://github.com/basher83/ProxmoxMCP.git
cd ProxmoxMCP
# ... continue with your commands
```

## Configuration (if applicable)

<!-- Share your config file content (remove sensitive tokens!) -->

```json
{
  "proxmox": {
    "host": "REDACTED",
    "port": 8006,
    "verify_ssl": false
  },
  "auth": {
    "user": "REDACTED",
    "token_name": "REDACTED",
    "token_value": "REDACTED"
  }
}
```

## What you've already tried

- [ ] Followed the README installation guide
- [ ] Checked Python version compatibility (3.10+)
- [ ] Verified virtual environment activation
- [ ] Tested Proxmox connection manually
- [ ] Searched existing issues

## Additional Context

<!-- Any other details that might help -->
