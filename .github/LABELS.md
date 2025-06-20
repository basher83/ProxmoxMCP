# GitHub Labels Guide

This document explains the standardized label system used in the ProxmoxMCP repository to help
organize and categorize issues, pull requests, and discussions.

## Label Categories

### 🏷️ Issue Type Labels

| Label | Description | When to Use |
|-------|-------------|-------------|
| `bug` | Something isn't working correctly | When reporting broken functionality |
| `enhancement` | New feature or request | For new features or improvements |
| `documentation` | Improvements or additions to documentation | Documentation issues or improvements |
| `security` | Security-related issues or improvements | Security vulnerabilities or enhancements |
| `performance` | Performance-related issues or improvements | Performance problems or optimizations |
| `question` | Further information is requested | General questions about usage |

### 🎯 Priority Labels

| Label | Description | Response Time |
|-------|-------------|---------------|
| `priority:critical` | Critical priority - immediate attention required | < 24 hours |
| `priority:high` | High priority - should be addressed soon | < 1 week |
| `priority:medium` | Medium priority - normal timeline | < 1 month |
| `priority:low` | Low priority - can be addressed later | No specific timeline |

### 📊 Status Labels

| Label | Description | Usage |
|-------|-------------|--------|
| `status:needs-investigation` | Requires investigation to understand the issue | Initial triage |
| `status:confirmed` | Issue has been confirmed and reproduced | After verification |
| `status:in-progress` | Work is currently in progress | During development |
| `status:blocked` | Cannot proceed due to external dependencies | When blocked |
| `status:ready-for-review` | Ready for code review | Before merge |
| `status:waiting-for-feedback` | Waiting for feedback from reporter or community | Pending response |

### 🔧 Component Labels

| Label | Description | Files/Areas |
|-------|-------------|-------------|
| `component:server` | Core MCP server implementation | `src/proxmox_mcp/server.py` |
| `component:config` | Configuration system and loading | `src/proxmox_mcp/config/` |
| `component:tools` | MCP tool implementations | `src/proxmox_mcp/tools/` |
| `component:formatting` | Output formatting and theming | `src/proxmox_mcp/formatting/` |
| `component:docker` | Docker and containerization | `Dockerfile`, `compose.yaml` |
| `component:authentication` | Authentication and security | `src/proxmox_mcp/utils/auth.py` |
| `component:api` | Proxmox API integration | `src/proxmox_mcp/core/proxmox.py` |
| `component:testing` | Test suite and testing infrastructure | `tests/` |

### 💻 Platform Labels

| Label | Description | Usage |
|-------|-------------|--------|
| `platform:linux` | Linux-specific issues | Linux deployment issues |
| `platform:windows` | Windows-specific issues | Windows deployment issues |
| `platform:macos` | macOS-specific issues | macOS deployment issues |
| `platform:docker` | Docker-specific issues | Container-related problems |

### 🖥️ Proxmox Version Labels

| Label | Description | Usage |
|-------|-------------|--------|
| `proxmox:7.x` | Proxmox VE 7.x versions | Issues specific to PVE 7.x |
| `proxmox:8.x` | Proxmox VE 8.x versions | Issues specific to PVE 8.x |

### ⏱️ Effort Labels

| Label | Description | Time Estimate |
|-------|-------------|---------------|
| `effort:small` | Small effort - hours to days | < 1 week |
| `effort:medium` | Medium effort - days to weeks | 1-4 weeks |
| `effort:large` | Large effort - weeks to months | > 1 month |

### 🤝 Community Labels

| Label | Description | Usage |
|-------|-------------|--------|
| `help-wanted` | Extra attention is needed - community help welcome | Community contributions welcome |
| `good-first-issue` | Good for newcomers | Beginner-friendly issues |
| `hacktoberfest` | Suitable for Hacktoberfest contributions | October contributions |

### 🔗 Integration Labels

| Label | Description | Usage |
|-------|-------------|--------|
| `integration:cline` | Cline integration specific | Cline IDE issues |
| `integration:mcp` | MCP protocol specific | MCP protocol issues |
| `integration:proxmox` | Proxmox integration specific | Proxmox API issues |

### 💬 Discussion Labels

| Label | Description | Usage |
|-------|-------------|--------|
| `discussion` | Discussion topic | General discussions |
| `show-and-tell` | Community showcase | Project showcases |
| `ideas` | Ideas and brainstorming | Feature brainstorming |
| `community-support` | Community help and support | Community help |

### 🛠️ Installation Labels

| Label | Description | Usage |
|-------|-------------|--------|
| `installation` | Installation and setup related | Setup problems |
| `configuration` | Configuration-related issues | Config issues |

## Label Usage Guidelines

### For Issue Reporters

1. **Always use at least one Issue Type label** (`bug`, `enhancement`, etc.)
2. **Add Priority label if urgent** (`priority:critical`, `priority:high`)
3. **Include Component labels** when you know the affected area
4. **Add Platform labels** for platform-specific issues
5. **Use Integration labels** for integration-related issues

### For Maintainers

1. **Triage new issues** by adding appropriate labels within 24-48 hours
2. **Update Status labels** as work progresses
3. **Add Effort labels** during sprint planning
4. **Use Component labels** for better organization
5. **Apply Community labels** for issues suitable for contributors

### Label Combinations

**Bug Reports:**

```
bug + priority:high + component:server + platform:linux
```

**Feature Requests:**

```
enhancement + effort:medium + component:tools + help-wanted
```

**Documentation:**

```
documentation + good-first-issue + effort:small
```

**Security Issues:**

```
security + priority:critical + component:authentication
```

## Setting Up Labels

### Automatic Setup

Run the provided script to set up all labels:

```bash
cd .github
./setup-labels.sh
```

### Manual Setup

Use GitHub CLI to create individual labels:

```bash
gh label create "priority:high" --color "d93f0b" --description "High priority - should be addressed soon"
```

### Bulk Import

Import all labels from the YAML file:

```bash
# Using a YAML processing tool
cat labels.yml | yq -r '.[] | "gh label create \"" + .name + "\" --color \"" + .color + 
  "\" --description \"" + .description + "\""' | bash
```

## Label Management

### Regular Maintenance

- **Weekly**: Review and update status labels
- **Monthly**: Analyze label usage and adjust as needed
- **Quarterly**: Review label effectiveness and update this documentation

### Adding New Labels

1. Update `labels.yml` with the new label definition
2. Run `./setup-labels.sh` to apply changes
3. Update this documentation
4. Announce changes in discussions

### Removing Labels

1. Ensure no active issues use the label
2. Remove from `labels.yml`
3. Delete from GitHub repository
4. Update documentation

## Label Analytics

Use labels for project insights:

- **Bug Rate**: Issues with `bug` label vs total issues
- **Priority Distribution**: Breakdown by priority labels
- **Component Health**: Issues by component labels
- **Community Engagement**: Usage of `help-wanted` and `good-first-issue`

---

**Last Updated**: January 30, 2025
**Next Review**: April 30, 2025
