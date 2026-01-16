# ProxmoxMCP

[![autofix enabled](https://shields.io/badge/autofix.ci-yes-success)](https://autofix.ci)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/fcb0843f9b1a45a586b0a5426d0a09c0)](https://app.codacy.com/gh/basher83/ProxmoxMCP/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
![CodeRabbit Pull Request Reviews](https://img.shields.io/coderabbit/prs/github/basher83/ProxmoxMCP?utm_source=oss&utm_medium=github&utm_campaign=basher83%2FProxmoxMCP&labelColor=171717&color=FF570A&link=https%3A%2F%2Fcoderabbit.ai&label=CodeRabbit+Reviews)
<img alt="GitHub commit activity" src="https://img.shields.io/github/commit-activity/w/basher83/ProxmoxMCP">

> [!WARNING]
> **⚠️ ARCHIVED - NO LONGER MAINTAINED ⚠️**
>
> This repository is deprecated and no longer supported. No further updates, bug fixes, or security patches will be provided.
> Please consider using alternative solutions for Proxmox MCP integration.

![ProxmoxMCP](https://github.com/user-attachments/assets/e32ab79f-be8a-420c-ab2d-475612150534)

A Model Context Protocol (MCP) server that enables AI assistants like Claude to manage
Proxmox virtual infrastructure through simple, secure commands.

> **Note**: This is a maintained fork of [canvrno/ProxmoxMCP](https://github.com/canvrno/ProxmoxMCP)
> with Docker support and active maintenance.

## ✨ Features

- 🖥️ **Node Management** - List nodes, check status, monitor resources
- 🚀 **VM Control** - List VMs, execute commands via QEMU Guest Agent
- 💾 **Storage Monitoring** - View storage pools and usage
- 🏢 **Cluster Overview** - Monitor overall cluster health
- 🔒 **Secure by Default** - Token-based authentication, SSL verification
- 🤖 **AI-Powered Diagnostics** - Get intelligent insights about your infrastructure

## 🚀 Quick Start

### Prerequisites

- Python 3.10+ or Docker
- Access to a Proxmox server
- Proxmox API token ([setup guide](#️-proxmox-api-token-setup))

### Installation Options

#### Option 1: UV with MCP Client (Recommended)

1. **Install UV**:

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Create your Proxmox config** (e.g., `~/proxmox-config.json`):

   ```json
   {
     "host": "your-proxmox-host.com",
     "user": "root@pam",
     "token_name": "mcp-token",
     "token_value": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
     "verify_ssl": true
   }
   ```

3. **Add to your MCP client settings**:

   ```json
   {
     "mcpServers": {
       "proxmox": {
         "command": "uvx",
         "args": [
           "--from",
           "git+https://github.com/basher83/ProxmoxMCP.git",
           "proxmox-mcp"
         ],
         "env": {
           "PROXMOX_MCP_CONFIG": "/Users/yourname/proxmox-config.json"
         }
       }
     }
   }
   ```

#### Option 2: Docker with MCP Client

> **Note**: Environment variable configuration is planned for a future release.
> Currently, you'll need to use a custom Docker image with your config file.

```json
{
  "mcpServers": {
    "proxmox": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e",
        "PROXMOX_HOST=your-proxmox-host.com",
        "-e",
        "PROXMOX_USER=root@pam",
        "-e",
        "PROXMOX_TOKEN_NAME=mcp-token",
        "-e",
        "PROXMOX_TOKEN_VALUE=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        "-e",
        "PROXMOX_VERIFY_SSL=true",
        "ghcr.io/basher83/proxmoxmcp:latest"
      ]
    }
  }
}
```

## ⚙️ Proxmox API Token Setup

1. Log into your Proxmox web interface
2. Navigate to **Datacenter → Permissions → API Tokens**
3. Click **Add** and create a new token:
   - **User**: Select user (e.g., `root@pam`)
   - **Token ID**: Enter a name (e.g., `mcp-token`)
   - **Privilege Separation**: Uncheck for full access
4. Copy the displayed token value - you won't see it again!

> **Note**: Set `"verify_ssl": false` in your config if using self-signed certificates.

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

## 📖 Documentation

- **[Complete Documentation](https://the-mothership.gitbook.io/proxmox-mcp/)** - Full guides and tutorials
- **[Developer Guide](docs/DEVELOPER.md)** - Development setup and workflow
- **[Contributing Guidelines](CONTRIBUTING.md)** - How to contribute

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## 🙏 Acknowledgments

- Original project by [canvrno](https://github.com/canvrno/ProxmoxMCP)
- Built with [Model Context Protocol](https://github.com/modelcontextprotocol/sdk)
- Powered by [Proxmoxer](https://github.com/proxmoxer/proxmoxer)
