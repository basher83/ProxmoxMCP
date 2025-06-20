# Mem0-MCP Setup Guide

> [Mem0-MCP](https://github.com/mem0ai/mem0-mcp) - Memory Optimization for Machine Learning Models

## Overview

This guide walks you through setting up Mem0-MCP in your development environment.
Mem0-MCP provides intelligent memory management capabilities for machine learning
workflows through the Model Context Protocol (MCP).

## Deployment Options

### Cloud-Hosted (Current Setup)

This workspace uses the cloud-hosted version of Mem0, available at [mem0.ai](https://mem0.ai/). This option provides:

- Easy setup and maintenance
- Automatic scaling and updates
- No local resource requirements

### Self-Hosted Alternative

A self-hosted Docker version is available but requires additional configuration
for persistent memory across container restarts. This option may be considered for
future deployments that require:

- Full data control
- Custom configurations
- Offline operation

## Prerequisites

Before setting up Mem0-MCP, ensure you have the following installed:

### UV (Universal Virtual Environment)

UV is required for Python package management and virtual environment creation.

```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add UV to your PATH
source $HOME/.local/share/../bin/env
```

## Installation

### Step 1: Clone the Repository

```bash
cd /workspace
git clone https://github.com/mem0ai/mem0-mcp.git
cd mem0-mcp
```

### Step 2: Configure Environment Variables

Create and configure the `.env` file with your API credentials:

```bash
nano .env
```

Add the following environment variables:

```bash
# Example .env configuration
export MEM0_MCP_API_KEY=your_api_key_here
# Add other required environment variables as needed
```

> **Note:** Replace `your_api_key_here` with your actual Mem0 API key from [mem0.ai](https://mem0.ai/).
>
## Running Mem0-MCP

### Method 1: Manual Activation

For direct control and debugging, you can manually set up and run Mem0-MCP:

```bash
# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate

# Install package in development mode
uv pip install -e .

# Start the server
uv run main.py --host <your_host> --port <your_port>
```

**Default values:**

- Host: `0.0.0.0`
- Port: `8080`

### Method 2: Automated Launch with Shell Alias

For convenience, you can create a shell alias that automates the entire setup and launch process.

#### Setup the Alias

Add the following function to your `.zshrc` file:

```bash
run_mem0() {
    local project_dir="/workspaces/ProxmoxMCP/mem0-mcp"  # Update this path as needed
    local port="${1:-8080}"
    local host="${2:-0.0.0.0}"

    echo "🚀 Starting Mem0-MCP..."
    echo "📁 Project directory: $project_dir"
    echo "🌐 Host: $host"
    echo "🔌 Port: $port"

    # Navigate to project directory
    cd "$project_dir" || { echo "❌ Cannot access $project_dir"; return 1; }

    # Create virtual environment if it doesn't exist
    [[ ! -d .venv ]] && {
        echo "🔨 Creating virtual environment..."
        uv venv || return 1
    }

    # Activate virtual environment
    source .venv/bin/activate || { echo "❌ Failed to activate virtual environment"; return 1; }

    # Install package dependencies  
    echo "📦 Installing package..."
    uv pip install -e . || { echo "❌ Failed to install package"; return 1; }

    # Start the application
    echo "🚀 Starting Mem0-MCP server..."
    uv run main.py --host "$host" --port "$port"
}
```

#### Activate the Alias

Make the alias available in your current session:

```bash
source ~/.zshrc
```

#### Usage

```bash
# Use default settings (host: 0.0.0.0, port: 8080)
run_mem0

# Specify custom port
run_mem0 8081

# Specify custom port and host
run_mem0 8081 127.0.0.1
```

## MCP Client Configuration

Once Mem0-MCP is running, configure your MCP client to connect to the Server-Sent Events (SSE) endpoint.

### Connection Details

- **Endpoint URL:** `http://0.0.0.0:8080/sse`
- **Connection Type:** SSE (Server-Sent Events)

### Claude Desktop Configuration

Add the following configuration to your Claude Desktop MCP settings:

```json
{
  "mcpServers": {
    "mem0": {
      "type": "sse",
      "url": "http://0.0.0.0:8080/sse"
    }
  }
}
```

### Configuration File Location

The MCP configuration file is typically located at:

- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux:** `~/.config/Claude/claude_desktop_config.json`

## Verification

To verify that Mem0-MCP is running correctly:

1. **Check the server status:**

   ```bash
   curl http://0.0.0.0:8080/health
   ```

2. **Test the SSE endpoint:**

   ```bash
   curl -H "Accept: text/event-stream" http://0.0.0.0:8080/sse
   ```

3. **View server logs** for any error messages or connection confirmations.

## Troubleshooting

### Common Issues

- **Port already in use:** Change the port number using the `--port` parameter
- **Virtual environment issues:** Delete `.venv` folder and recreate it
- **API key errors:** Verify your `.env` file configuration
- **Connection refused:** Ensure the server is running and accessible on the specified host/port

### Getting Help

For additional support:

- Check the [Mem0-MCP GitHub repository](https://github.com/mem0ai/mem0-mcp) for issues and documentation
- Review the [Mem0.ai documentation](https://mem0.ai/) for API-related questions
