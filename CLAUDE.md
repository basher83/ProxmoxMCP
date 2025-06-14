# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Additional Instructions

- memory workflow @/workspaces/ProxmoxMCP/docs/ai-instructions/memory-instructions.md (not supported in Codex)
- context workflow @/workspaces/ProxmoxMCP/docs/ai-instructions/context-instructions.md
- github workflow @/workspaces/ProxmoxMCP/docs/ai-instructions/github-instructions.md
- issue creation workflow @/workspaces/ProxmoxMCP/docs/ai-instructions/issue-creation-instructions.md
- issue resolution workflow @/workspaces/ProxmoxMCP/docs/ai-instructions/issue-resolution-instructions.md
- pr workflow @/workspaces/ProxmoxMCP/docs/ai-instructions/pr-instructions.md
- milestone workflow @/workspaces/ProxmoxMCP/docs/ai-instructions/milestone-instructions.md

## Development Commands

### Environment Setup

```bash
# Set up git configuration (recommended for development)
cp example.gitconfig .git/config
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Create and activate virtual environment
uv venv
source .venv/bin/activate  # Linux/macOS
.\.venv\Scripts\Activate.ps1  # Windows

# Install dependencies with development tools
uv pip install -e ".[dev]"
```

### Testing and Quality Assurance

```bash
# Run tests
pytest

# Format code
black .

# Type checking
mypy .

# Lint code
ruff .

# Run all quality checks sequentially
pytest && black . && mypy . && ruff .
```

### Running the Server

```bash
# Set config path and run server
export PROXMOX_MCP_CONFIG="proxmox-config/config.json"
python -m proxmox_mcp.server

# Or with Docker
docker compose up --build
```

### Configuration Setup

```bash
# Create config directory and copy template
mkdir -p proxmox-config
cp proxmox-config/config.example.json proxmox-config/config.json
# Edit config.json with your Proxmox credentials
```

## Architecture Overview

### Core Components

- **server.py**: Main MCP server implementation using FastMCP, handles tool registration and request routing
- **core/proxmox.py**: ProxmoxManager class that manages API connections and authentication
- **config/**: Configuration loading and validation using Pydantic models
- **tools/**: Individual tool implementations (node, VM, storage, cluster operations)
- **formatting/**: Rich output formatting with themes, colors, and structured display

### Key Design Patterns

- **Tool-based Architecture**: Each Proxmox operation is implemented as a separate MCP tool
- **Pydantic Validation**: All configuration and API parameters use Pydantic models for type safety
- **Centralized Formatting**: All output uses consistent formatting through the formatting module
- **Async Support**: VM command execution supports async operations via QEMU guest agent

### Tool Categories

1. **Node Tools**: `get_nodes`, `get_node_status` - Cluster node management
2. **VM Tools**: `get_vms`, `execute_vm_command` - Virtual machine operations
3. **Storage Tools**: `get_storage` - Storage pool information
4. **Cluster Tools**: `get_cluster_status` - Overall cluster health

### Configuration Requirements

- Requires `PROXMOX_MCP_CONFIG` environment variable pointing to config JSON file
- Config must include Proxmox connection details (host, port, SSL settings) and authentication (user, token_name, token_value)
- Supports both file-based and environment variable configuration

### Authentication

- Uses Proxmox API tokens (not passwords) for secure authentication
- Tokens must have appropriate permissions for the operations being performed
- Connection is tested during server startup

### Output Formatting

- Rich formatted output with emojis, colors, and structured layout
- Consistent formatting across all tools using theme system
- Human-readable resource usage (bytes, percentages, uptime)

## Important Implementation Notes

### VM Command Execution

- Requires QEMU Guest Agent to be installed and running in target VMs
- Commands execute asynchronously and return both stdout and stderr
- Returns proper exit codes and handles command failures gracefully

### Error Handling

- Connection failures during startup cause server to exit with detailed error messages
- API operation failures are caught and returned as formatted error responses
- SSL verification can be disabled for self-signed certificates via config

### Testing

- Uses pytest with async support for testing MCP operations
- Test configuration should use mock Proxmox API to avoid requiring live server
- Tests are located in `tests/` directory

### Dependencies

- Built on Model Context Protocol (MCP) SDK for tool interface
- Uses `proxmoxer` library for Proxmox API communication
- Requires Python 3.10+ with modern async/await support

## Memories

- "When tasked are completed you must commit changes to github"
- When submitting PR reviews with complex text containing special shell characters, it's better to:
  1. Use simpler review text, or
  2. Escape special characters properly, or
  3. Submit reviews through the GitHub web interface for complex formatting
