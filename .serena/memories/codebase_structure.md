# ProxmoxMCP Codebase Structure

## Root Directory Layout
```
ProxmoxMCP/
├── src/proxmox_mcp/        # Main source code
├── tests/                  # Test suite
├── proxmox-config/         # Configuration templates and files
├── docs/                   # Documentation
├── scripts/                # Utility scripts
├── .github/               # GitHub workflows and templates
├── pyproject.toml         # Project configuration and dependencies
├── Dockerfile             # Docker container definition
├── compose.yaml           # Docker Compose configuration
├── Taskfile.yml           # Task automation
└── CLAUDE.md              # Claude Code instructions
```

## Source Code Organization (`src/proxmox_mcp/`)

### Core Modules
- **`server.py`**: Main MCP server implementation using FastMCP
- **`__init__.py`**: Package initialization

### Core Components (`core/`)
- **`proxmox.py`**: ProxmoxManager class for API connections and authentication
- **`logging.py`**: Logging configuration and setup

### Configuration Management (`config/`)
- **`models.py`**: Pydantic models for configuration validation
- **`loader.py`**: Configuration loading and processing logic

### MCP Tools (`tools/`)
- **`base.py`**: Base classes for tool implementations
- **`definitions.py`**: Tool registration and descriptions for MCP
- **`node.py`**: Node management tools (`get_nodes`, `get_node_status`)
- **`vm.py`**: VM management tools (`get_vms`, VM operations)
- **`container.py`**: LXC container management
- **`storage.py`**: Storage pool management (`get_storage`)
- **`cluster.py`**: Cluster status and management (`get_cluster_status`)
- **`ai_diagnostics.py`**: AI-powered diagnostic tools
- **`console/`**: VM console command execution
  - **`manager.py`**: Console command execution logic

### Output Formatting (`formatting/`)
- **`theme.py`**: ProxmoxTheme configuration and color schemes
- **`colors.py`**: Color definitions and terminal color support
- **`components.py`**: Reusable formatting components
- **`formatters.py`**: ProxmoxFormatters for consistent output styling
- **`templates.py`**: Output templates for different resource types

### Utilities (`utils/`)
- **`auth.py`**: Authentication helpers
- **`logging.py`**: Logging utilities
- **`encryption.py`**: Encryption/decryption functionality
- **`encrypt_config.py`**: Configuration encryption tools

## Test Organization (`tests/`)
- **`test_server.py`**: MCP server functionality tests
- **`test_config_loader.py`**: Configuration loading tests
- **`test_vm_console.py`**: VM console operations tests
- **`test_encrypt_config.py`**: Configuration encryption tests
- **`test_encryption.py`**: Encryption utility tests

## Configuration (`proxmox-config/`)
- **`config.example.json`**: Template configuration file
- **`config.json`**: Actual configuration (gitignored)

## Key Design Patterns

### MCP Tool Architecture
- All tools inherit from base classes in `tools/base.py`
- Tool registration happens in `tools/definitions.py`
- Rich formatting applied via `formatting/` module
- Comprehensive error handling with specific exception types

### Configuration Management
- Pydantic models for all configuration validation
- Support for environment variable fallbacks
- Encryption support for sensitive configuration
- Backward compatibility maintenance

### API Integration
- Centralized Proxmox API management via `ProxmoxManager`
- Token-based authentication
- Connection testing and validation
- Async support for VM operations

### Output Formatting
- Consistent theme-based formatting across all tools
- Emoji and color support with toggle options
- Structured templates for different resource types
- Human-readable format for metrics (bytes, percentages, uptime)

## External Dependencies Integration
- **MCP SDK**: Tool interface and server implementation
- **Proxmoxer**: Proxmox VE API communication
- **Pydantic**: Data validation and configuration models
- **Cryptography**: Secure configuration encryption
- **Docker**: Containerized deployment with security best practices