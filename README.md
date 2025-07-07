# 📖 README

## 🚀 Proxmox Manager - Proxmox MCP Server

[![autofix enabled](https://shields.io/badge/autofix.ci-yes-success)](https://autofix.ci)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/fcb0843f9b1a45a586b0a5426d0a09c0)](https://app.codacy.com/gh/basher83/ProxmoxMCP/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
![CodeRabbit Pull Request Reviews](https://img.shields.io/coderabbit/prs/github/basher83/ProxmoxMCP?utm_source=oss&utm_medium=github&utm_campaign=basher83%2FProxmoxMCP&labelColor=171717&color=FF570A&link=https%3A%2F%2Fcoderabbit.ai&label=CodeRabbit+Reviews)
<img alt="GitHub commit activity" src="https://img.shields.io/github/commit-activity/w/basher83/ProxmoxMCP">

![ProxmoxMCP](https://github.com/user-attachments/assets/e32ab79f-be8a-420c-ab2d-475612150534)

> **Note**: This is a maintained fork of the original
> [canvrno/ProxmoxMCP](https://github.com/canvrno/ProxmoxMCP) repository, adding Docker
> support and ongoing maintenance. The original repository appears to be inactive since
> February 2025.

#### What's Different in this Fork?

- ✨ **Full Docker Support**: Added complete Docker and Docker Compose configurations
- 🔒 **Security Focused**: Containerized with security best practices
- 📦 **Easy Deployment**: Simple `docker compose up` deployment
- 🛠️ **Maintained**: Active maintenance and updates
- 💡 **Community Driven**: Open to contributions and improvements

The main addition is comprehensive Docker support, making it easy to deploy and run the Proxmox MCP server in a containerized environment. See the [Docker section](./#🐳-running-with-docker) for details.

A Python-based Model Context Protocol (MCP) server for interacting with Proxmox hypervisors, providing a clean interface for managing nodes, VMs, and containers.

## 📚 Documentation

📖 **[Complete Documentation](https://the-mothership.gitbook.io/proxmox-mcp/)** - Comprehensive guides, API reference, and tutorials on GitBook

## 🏗️ Built With

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview) - An agentic coding tool made by Anthropic
- [Proxmoxer](https://github.com/proxmoxer/proxmoxer) - Python wrapper for Proxmox API
- [MCP SDK](https://github.com/modelcontextprotocol/sdk) - Model Context Protocol SDK
- [Pydantic](https://docs.pydantic.dev/) - Data validation using Python type annotations

### ✨ Features

- 🛠️ Built with the official MCP SDK
- 🔒 Secure token-based authentication with Proxmox
- 🖥️ Tools for managing nodes and VMs
- 💻 VM console command execution
- 📝 Configurable logging system
- ✅ Type-safe implementation with Pydantic
- 🎨 Rich output formatting with customizable themes
- 🪝 Claude Code Hooks integration for automated quality checks and security validation

<https://github.com/user-attachments/assets/1b5f42f7-85d5-4918-aca4-d38413b0e82b>

### 📦 Installation

#### Prerequisites

- UV package manager (recommended)
- Python 3.10 or higher
- Git
- Access to a Proxmox server with API token credentials

Before starting, ensure you have:

- [ ] Proxmox server hostname or IP
- [ ] Proxmox API token (see [API Token Setup](./#proxmox-api-token-setup))
- [ ] UV installed (`pip install uv`)

#### Git Configuration Setup

For development work, it's recommended to configure git with the project-specific settings:

```bash
# Copy the example gitconfig to your local git configuration
cp example.gitconfig .git/config

# Or manually configure git settings (recommended for contributors)
git config user.name "Your Name"
git config user.email "your.email@example.com"
git config core.editor "vscode"
git config init.defaultBranch "main"
git config pull.rebase true
git config push.autoSetupRemote true
```

The `example.gitconfig` file contains optimized settings for this project including:

- Python-specific diff patterns
- JSON and Dockerfile diff improvements
- Useful git aliases (`lg`, `st`, `co`, etc.)
- Security and performance optimizations

**Note**: Review the example file before copying, as it contains sample user credentials that should be replaced with your own.

#### Option 1: Quick Install (Recommended)

1. Clone and set up environment:

    ```bash
    # Clone repository
    cd ~/Documents/Cline/MCP  # For Cline users
    # OR
    cd your/preferred/directory  # For manual installation

    git clone https://github.com/basher83/ProxmoxMCP.git
    cd ProxmoxMCP

    # Create and activate virtual environment
    uv venv
    source .venv/bin/activate  # Linux/macOS
    # OR
    .\.venv\Scripts\Activate.ps1  # Windows
    ```

2. Install dependencies:

    ```bash
    # Install with development dependencies
    uv pip install -e ".[dev]"
    ```

3. Create configuration:

    ```bash
    # Create config directory and copy template
    mkdir -p proxmox-config
    cp config/config.example.json proxmox-config/config.json
    ```

4. Edit `proxmox-config/config.json`:

  ![config.json](graphics/config.json.png)

#### Verifying Installation

1. Check Python environment:

    ```bash
    python -c "import proxmox_mcp; print('Installation OK')"
    ```

2. Run the tests:

    ```bash
    pytest
    ```

3. Verify configuration:

    ```bash
    # Linux/macOS
    PROXMOX_MCP_CONFIG="proxmox-config/config.json" python -m proxmox_mcp.server

    # Windows (PowerShell)
    $env:PROXMOX_MCP_CONFIG="proxmox-config\config.json"; python -m proxmox_mcp.server
    ```

    You should see either:

    - A successful connection to your Proxmox server
    - Or a connection error (if Proxmox details are incorrect)

### ⚙️ Configuration

#### Proxmox API Token Setup

1. Log into your Proxmox web interface
2. Navigate to Datacenter -> Permissions -> API Tokens
3. Create a new API token:
   - Select a user (e.g., root@pam)
   - Enter a token ID (e.g., "mcp-token")
   - Uncheck "Privilege Separation" if you want full access
   - Save and copy both the token ID and secret

#### Migration Notice for Existing Users

**Breaking Change**: Starting with this version, SSL verification is enabled by default (`"verify_ssl": true`).

If you're using self-signed certificates and encounter SSL errors:

1. Update your existing `config.json` to explicitly set `"verify_ssl": false`
2. Or preferably, set up proper SSL certificates for your Proxmox server

This change improves security by default while maintaining flexibility for self-signed certificate environments.

### 🚀 Running the Server

#### Development Mode

For testing and development:

```bash
# Activate virtual environment first
source .venv/bin/activate  # Linux/macOS
# OR
.\.venv\Scripts\Activate.ps1  # Windows

# Run the server
python -m proxmox_mcp.server
```

#### Cline Desktop Integration

For Cline users, add this configuration to your MCP settings file (typically at `~/.config/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`):

 ![cline_mcp_settings.json](graphics/cline_mcp_settings.json.png)

To help generate the correct paths, you can use this command:

```bash
# This will print the MCP settings with your absolute paths filled in
python -c "import os; print(f'''{{
    \"mcpServers\": {{
        \"github.com/basher83/ProxmoxMCP\": {{
            \"command\": \"{os.path.abspath('.venv/bin/python')}\",
            \"args\": [\"-m\", \"proxmox_mcp.server\"],
            \"cwd\": \"{os.getcwd()}\",
            \"env\": {{
                \"PYTHONPATH\": \"{os.path.abspath('src')}\",
                \"PROXMOX_MCP_CONFIG\": \"{os.path.abspath('proxmox-config/config.json')}\",
                ...
            }}
        }}
    }}
}}''')"
```

Important:

- All paths must be absolute
- The Python interpreter must be from your virtual environment
- The PYTHONPATH must point to the src directory
- Restart VSCode after updating MCP settings

## 🔧 Available Tools

The server provides the following MCP tools for interacting with Proxmox:

### get_nodes

Lists all nodes in the Proxmox cluster.

- Parameters: None
- Example Response:

  ![get_nodes command output](graphics/get_nodes.png)

### get_node_status

Get detailed status of a specific node.

- Parameters:
  - `node` (string, required): Name of the node
- Example Response:

  ![get_node_status command output](graphics/get_node_status.png)

### get_vms

List all VMs across the cluster.

- Parameters: None
- Example Response:

  ![get_vms command output](graphics/get_vms.png)

### get_storage

List available storage.

- Parameters: None
- Example Response:

  ![get_storage command output](graphics/get_storage.png)

### get_cluster_status

Get overall cluster status.

- Parameters: None
- Example Response:

  ![get_cluster_status command output](graphics/get_cluster_status.png)

### execute_vm_command

Execute a command in a VM's console using QEMU Guest Agent.

- Parameters:
  - `node` (string, required): Name of the node where VM is running
  - `vmid` (string, required): ID of the VM
  - `command` (string, required): Command to execute
- Example Response:

  ![execute_vm_command output](graphics/execute_vm_command.png)

- Requirements:
  - VM must be running
  - QEMU Guest Agent must be installed and running in the VM
  - Command execution permissions must be enabled in the Guest Agent
- Error Handling:
  - Returns error if VM is not running
  - Returns error if VM is not found
  - Returns error if command execution fails
  - Includes command output even if command returns non-zero exit code

### 🐳 Running with Docker

You can run the Proxmox MCP Server in a containerized environment using Docker and Docker Compose. This is useful for consistent deployments and isolating dependencies.

#### Requirements

- **Docker** and **Docker Compose** installed
- **Python 3.10** (as specified in the Dockerfile base image)
- Access to your Proxmox server and API token credentials
- A valid configuration file (see [Configuration](./#⚙️-configuration))

#### Environment Variables

The following environment variable **must** be set for the server to start:

- `PROXMOX_MCP_CONFIG`: Path to your configuration file inside the container (e.g., `/app/proxmox-config/config.json`)

You may also set other environment variables as needed (see the [Cline Desktop Integration](./#cline-desktop-integration) section for examples):

- `PYTHONPATH`: Should be set to `/app/src` (already set in the compose file)
- Additional Proxmox or logging variables as required by your setup

#### Build and Run

1. **Copy your configuration file** into the `proxmox-config` directory, or mount it as a volume.
2. **Build and start the service:**

   ```bash
   docker compose up --build
   ```

   Or, if using legacy Compose:

   ```bash
   docker-compose up --build
   ```

3. **Set the required environment variable** at runtime. You can do this by editing the `docker-compose.yml` file:

 ![volumes](graphics/environment.png)

   Or by using an `.env` file and uncommenting the `env_file` line in the compose file.

4. **(Optional) Mount volumes** if you want to persist configuration or logs:

 ![volumes](graphics/volumes.png)

#### Ports

- **No ports are exposed by default.**
  - The server runs as a stdio service. If you need to expose a port, add a `ports` section to the `docker-compose.yml` file.

#### Notes

- The container runs as a non-root user for security.
- All dependencies are installed in a virtual environment inside the container.
- If you need to develop locally, you can mount the `src` directory as a volume for live code updates.

For more advanced configuration, see the comments in the provided `docker-compose.yml` and [Configuration](./#⚙️-configuration) section above.

### 👨‍💻 Development

After activating your virtual environment:

- Run tests: `pytest`
- Format code: `black .`
- Type checking: `mypy .`
- Lint: `ruff .`

For enhanced development workflow with Taskfile (recommended):

- Run all tests: `task test`
- Run pre-commit checks: `task pre-commit`
- Run security tests: `task test:security`
- Run with coverage: `task test:coverage`
- Watch mode testing: `task test:watch`

See [Testing Workflow Documentation](docs/testing-workflow.md) for comprehensive testing guide.

#### 🪝 Claude Code Hooks

This project includes Claude Code hooks for automated quality checks and security validation. The hooks are automatically enabled through the project-level settings in `.claude/settings.json`.

**Features:**

- **Security validation**: Blocks dangerous commands and warns about credential exposure
- **Auto-formatting**: Automatically runs Black and Ruff fixes after code edits
- **Markdown linting**: Validates markdown files using `.markdownlint.jsonc` configuration
- **Quality reports**: Generates comprehensive reports after running tests
- **Command logging**: Tracks all executed commands for debugging
- **Session summaries**: Provides end-of-session reports with recommendations

**Hook Types:**

- `PreToolUse`: Security checks before running commands
- `PostToolUse`: Auto-formatting and validation after edits
- `Notification`: Desktop and terminal notifications
- `Stop`: Session summary generation

For detailed information about hooks configuration and customization, see the [Claude Code Hooks Guide](docs/claude-code-hooks-guide.md).

### 🧪 Testing

ProxmoxMCP provides a comprehensive testing workflow with specialized test tasks:

- **`task test`** - Run all tests with enhanced validation (71 tests)
- **`task test:security`** - Security-focused tests (encryption, auth)
- **`task test:tools`** - MCP tools and server functionality
- **`task test:config`** - Configuration and encryption tests
- **`task test:coverage`** - Coverage analysis with intelligent fallback
- **`task test:watch`** - Continuous testing during development

**Current Coverage**: Core functionality, configuration management, encryption, MCP server implementation, and VM console operations.

**Future Improvements**: See [GitHub Issue #75](https://github.com/basher83/ProxmoxMCP/issues/75) for planned testing enhancements including AI diagnostics coverage, formatting module tests, and integration testing.

For detailed testing workflows and best practices, see the [Testing Workflow Documentation](docs/testing-workflow.md).

### 📁 Project Structure

```text
proxmox-mcp/
├── src/
│   └── proxmox_mcp/
│       ├── server.py          # Main MCP server implementation
│       ├── config/            # Configuration handling
│       ├── core/              # Core functionality
│       ├── formatting/        # Output formatting and themes
│       ├── tools/             # Tool implementations
│       │   └── console/       # VM console operations
│       └── utils/             # Utilities (auth, logging)
├── tests/                     # Test suite
├── proxmox-config/
│   └── config.example.json    # Configuration template
├── pyproject.toml            # Project metadata and dependencies
└── LICENSE                   # MIT License
```

### 📄 License

MIT License
