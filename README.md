# 📖 README

## 🚀 Proxmox Manager - Proxmox MCP Server

[![autofix enabled](https://shields.io/badge/autofix.ci-yes-success?logo=data:image/svg+xml;base64,PHN2ZyBmaWxsPSIjZmZmIiB2aWV3Qm94PSIwIDAgMTI4IDEyOCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCB0cmFuc2Zvcm09InNjYWxlKDAuMDYxLC0wLjA2MSkgdHJhbnNsYXRlKC0yNTAsLTE3NTApIiBkPSJNMTMyNSAtMzQwcS0xMTUgMCAtMTY0LjUgMzIuNXQtNDkuNSAxMTQuNXEwIDMyIDUgNzAuNXQxMC41IDcyLjV0NS41IDU0djIyMHEtMzQgLTkgLTY5LjUgLTE0dC03MS41IC01cS0xMzYgMCAtMjUxLjUgNjJ0LTE5MSAxNjl0LTkyLjUgMjQxcS05MCAxMjAgLTkwIDI2NnEwIDEwOCA0OC41IDIwMC41dDEzMiAxNTUuNXQxODguNSA4MXExNSA5OSAxMDAuNSAxODAuNXQyMTcgMTMwLjV0MjgyLjUgNDlxMTM2IDAgMjU2LjUgLTQ2IHQyMDkgLTEyNy41dDEyOC41IC0xODkuNXExNDkgLTgyIDIyNyAtMjEzLjV0NzggLTI5OS41cTAgLTEzNiAtNTggLTI0NnQtMTY1LjUgLTE4NC41dC0yNTYuNSAtMTAzLjVsLTI0MyAtMzAwdi01MnEwIC0yNyAzLjUgLTU2LjV0Ni41IC01Ny41dDMgLTUycTAgLTg1IC00MS41IC0xMTguNXQtMTU3LjUgLTMzLjV6TTEzMjUgLTI2MHE3NyAwIDk4IDE0LjV0MjEgNTcuNXEwIDI5IC0zIDY4dC02LjUgNzN0LTMuNSA0OHY2NGwyMDcgMjQ5IHEtMzEgMCAtNjAgNS41dC01NCAxMi41bC0xMDQgLTEyM3EtMSAzNCAtMiA2My41dC0xIDU0LjVxMCA2OSA5IDEyM2wzMSAyMDBsLTExNSAtMjhsLTQ2IC0yNzFsLTIwNSAyMjZxLTE5IC0xNSAtNDMgLTI4LjV0LTU1IC0yNi41bDIxOSAtMjQydi0yNzZxMCAtMjAgLTUuNSAtNjB0LTEwLjUgLTc5dC01IC01OHEwIC00MCAzMCAtNTMuNXQxMDQgLTEzLjV6TTEyNjIgNjE2cS0xMTkgMCAtMjI5LjUgMzQuNXQtMTkzLjUgOTYuNWw0OCA2NCBxNzMgLTU1IDE3MC41IC04NXQyMDQuNSAtMzBxMTM3IDAgMjQ5IDQ1LjV0MTc5IDEyMXQ2NyAxNjUuNWg4MHEwIC0xMTQgLTc3LjUgLTIwNy41dC0yMDggLTE0OXQtMjg5LjUgLTU1LjV6TTgwMyA1OTVxODAgMCAxNDkgMjkuNXQxMDggNzIuNWwyMjEgLTY3bDMwOSA4NnE0NyAtMzIgMTA0LjUgLTUwdDExNy41IC0xOHE5MSAwIDE2NSAzOHQxMTguNSAxMDMuNXQ0NC41IDE0Ni41cTAgNzYgLTM0LjUgMTQ5dC05NS41IDEzNHQtMTQzIDk5IHEtMzcgMTA3IC0xMTUuNSAxODMuNXQtMTg2IDExNy41dC0yMzAuNSA0MXEtMTAzIDAgLTE5Ny41IC0yNnQtMTY5IC03Mi41dC0xMTcuNSAtMTA4dC00MyAtMTMxLjVxMCAtMzQgMTQuNSAtNjIuNXQ0MC41IC01MC41bC01NSAtNTlxLTM0IDI5IC01NCA2NS41dC0yNSA4MS41cS04MSAtMTggLTE0NSAtNzB0LTEwMSAtMTI1LjV0LTM3IC0xNTguNXEwIC0xMDIgNDguNSAtMTgwLjV0MTI5LjUgLTEyM3QxNzkgLTQ0LjV6Ii8+PC9zdmc+)](https://autofix.ci)
<img alt="GitHub commit activity" src="https://img.shields.io/github/commit-activity/w/basher83/ProxmoxMCP">

![ProxmoxMCP](https://github.com/user-attachments/assets/e32ab79f-be8a-420c-ab2d-475612150534)

> **Note**: This is a maintained fork of the original [canvrno/ProxmoxMCP](https://github.com/canvrno/ProxmoxMCP) repository, adding Docker support and ongoing maintenance. The original repository appears to be inactive since February 2025.

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

### 🏗️ Built With

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

1.  Clone and set up environment:

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

2.  Install dependencies:

    ```bash
    # Install with development dependencies
    uv pip install -e ".[dev]"
    ```

3.  Create configuration:

    ```bash
    # Create config directory and copy template
    mkdir -p proxmox-config
    cp config/config.example.json proxmox-config/config.json
    ```

4.  Edit `proxmox-config/config.json`:

    ```json
    {
        "proxmox": {
            "host": "PROXMOX_HOST",        # Required: Your Proxmox server address
            "port": 8006,                  # Optional: Default is 8006
            "verify_ssl": true,            # Optional: Set false only for self-signed certs
            "service": "PVE"               # Optional: Default is PVE
        },
        "auth": {
            "user": "USER@pve",            # Required: Your Proxmox username
            "token_name": "TOKEN_NAME",    # Required: API token ID
            "token_value": "TOKEN_VALUE"   # Required: API token value
        },
        "logging": {
            "level": "INFO",               # Optional: DEBUG for more detail
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "file": "proxmox_mcp.log"      # Optional: Log to file
        }
    }
    ```

#### Verifying Installation

1.  Check Python environment:

    ```bash
    python -c "import proxmox_mcp; print('Installation OK')"
    ```

2.  Run the tests:

    ```bash
    pytest
    ```

3.  Verify configuration:

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

```json
{
  "mcpServers": {
    "github.com/basher83/ProxmoxMCP": {
      "command": "/absolute/path/to/ProxmoxMCP/.venv/bin/python",
      "args": ["-m", "proxmox_mcp.server"],
      "cwd": "/absolute/path/to/ProxmoxMCP",
      "env": {
        "PYTHONPATH": "/absolute/path/to/ProxmoxMCP/src",
        "PROXMOX_MCP_CONFIG": "/absolute/path/to/ProxmoxMCP/proxmox-config/config.json",
        "PROXMOX_HOST": "your-proxmox-host",
        "PROXMOX_USER": "username@pve",
        "PROXMOX_TOKEN_NAME": "token-name",
        "PROXMOX_TOKEN_VALUE": "token-value",
        "PROXMOX_PORT": "8006",
        "PROXMOX_VERIFY_SSL": "false",
        "PROXMOX_SERVICE": "PVE",
        "LOG_LEVEL": "DEBUG"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

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

  ```
  🖥️ Proxmox Nodes

  🖥️ pve-compute-01
    • Status: ONLINE
    • Uptime: ⏳ 156d 12h
    • CPU Cores: 64
    • Memory: 186.5 GB / 512.0 GB (36.4%)

  🖥️ pve-compute-02
    • Status: ONLINE
    • Uptime: ⏳ 156d 11h
    • CPU Cores: 64
    • Memory: 201.3 GB / 512.0 GB (39.3%)
  ```

### get_node_status

Get detailed status of a specific node.

- Parameters:
  - `node` (string, required): Name of the node
- Example Response:

  ```
  🖥️ Node: pve-compute-01
    • Status: ONLINE
    • Uptime: ⏳ 156d 12h
    • CPU Usage: 42.3%
    • CPU Cores: 64 (AMD EPYC 7763)
    • Memory: 186.5 GB / 512.0 GB (36.4%)
    • Network: ⬆️ 12.8 GB/s ⬇️ 9.2 GB/s
    • Temperature: 38°C
  ```

### get_vms

List all VMs across the cluster.

- Parameters: None
- Example Response:

  ```
  🗃️ Virtual Machines

  🗃️ prod-db-master (ID: 100)
    • Status: RUNNING
    • Node: pve-compute-01
    • CPU Cores: 16
    • Memory: 92.3 GB / 128.0 GB (72.1%)

  🗃️ prod-web-01 (ID: 102)
    • Status: RUNNING
    • Node: pve-compute-01
    • CPU Cores: 8
    • Memory: 12.8 GB / 32.0 GB (40.0%)
  ```

### get_storage

List available storage.

- Parameters: None
- Example Response:

  ```
  💾 Storage Pools

  💾 ceph-prod
    • Status: ONLINE
    • Type: rbd
    • Usage: 12.8 TB / 20.0 TB (64.0%)
    • IOPS: ⬆️ 15.2k ⬇️ 12.8k

  💾 local-zfs
    • Status: ONLINE
    • Type: zfspool
    • Usage: 3.2 TB / 8.0 TB (40.0%)
    • IOPS: ⬆️ 42.8k ⬇️ 35.6k
  ```

### get_cluster_status

Get overall cluster status.

- Parameters: None
- Example Response:

  ```
  ⚙️ Proxmox Cluster

    • Name: enterprise-cloud
    • Status: HEALTHY
    • Quorum: OK
    • Nodes: 4 ONLINE
    • Version: 8.1.3
    • HA Status: ACTIVE
    • Resources:
      - Total CPU Cores: 192
      - Total Memory: 1536 GB
      - Total Storage: 70 TB
    • Workload:
      - Running VMs: 7
      - Total VMs: 8
      - Average CPU Usage: 38.6%
      - Average Memory Usage: 42.8%
  ```

### execute_vm_command

Execute a command in a VM's console using QEMU Guest Agent.

- Parameters:
  - `node` (string, required): Name of the node where VM is running
  - `vmid` (string, required): ID of the VM
  - `command` (string, required): Command to execute
- Example Response:

  ```
  🔧 Console Command Result
    • Status: SUCCESS
    • Command: systemctl status nginx
    • Node: pve-compute-01
    • VM: prod-web-01 (ID: 102)

  Output:
  ● nginx.service - A high performance web server and a reverse proxy server
     Loaded: loaded (/lib/systemd/system/nginx.service; enabled; vendor preset: enabled)
     Active: active (running) since Tue 2025-02-18 15:23:45 UTC; 2 months 3 days ago
  ```

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

   ```yaml
   environment:
     PROXMOX_MCP_CONFIG: /app/proxmox-config/config.json
   ```

   Or by using an `.env` file and uncommenting the `env_file` line in the compose file.

4. **(Optional) Mount volumes** if you want to persist configuration or logs:

   ```yaml
   volumes:
     - ./proxmox-config:/app/proxmox-config
     - ./logs:/app/logs
   ```

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

### 📁 Project Structure

```
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
