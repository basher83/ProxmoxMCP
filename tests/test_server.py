"""
Tests for the Proxmox MCP server.
"""

import json
import os
import tempfile
from unittest.mock import patch

from mcp.server.fastmcp.exceptions import ToolError
import pytest

from proxmox_mcp.server import ProxmoxMCPServer


@pytest.fixture
def mock_env_vars():
    """Fixture to set up test environment variables."""
    env_vars = {
        "PROXMOX_HOST": "test.proxmox.com",
        "PROXMOX_USER": "test@pve",
        "PROXMOX_TOKEN_NAME": "test_token",
        "PROXMOX_TOKEN_VALUE": "test_value",
        "LOG_LEVEL": "DEBUG",
    }
    with patch.dict(os.environ, env_vars):
        yield env_vars


@pytest.fixture
def temp_config_file(mock_env_vars):
    """Create a temporary config file for testing."""
    config_data = {
        "proxmox": {"host": "test.proxmox.com", "port": 8006, "verify_ssl": False},
        "auth": {
            "user": "test@pve",
            "token_name": "test_token",
            "token_value": "test_value",
        },
        "logging": {"level": "DEBUG"},
    }

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(config_data, f)
        config_path = f.name

    # Set the config path environment variable
    with patch.dict(os.environ, {"PROXMOX_MCP_CONFIG": config_path}):
        yield config_path

    # Clean up
    os.unlink(config_path)


@pytest.fixture
def mock_proxmox():
    """Fixture to mock ProxmoxAPI."""
    with patch("proxmox_mcp.core.proxmox.ProxmoxAPI") as mock:
        mock.return_value.nodes.get.return_value = [
            {"node": "node1", "status": "online"},
            {"node": "node2", "status": "online"},
        ]
        yield mock


@pytest.fixture
def server(temp_config_file, mock_proxmox):
    """Fixture to create a ProxmoxMCPServer instance."""
    return ProxmoxMCPServer(config_path=temp_config_file)


def test_server_initialization(server, mock_proxmox):
    """Test server initialization with environment variables."""
    assert server.config.proxmox.host == "test.proxmox.com"
    assert server.config.auth.user == "test@pve"
    assert server.config.auth.token_name == "test_token"
    assert server.config.auth.token_value == "test_value"
    assert server.config.logging.level == "DEBUG"

    mock_proxmox.assert_called_once()


@pytest.mark.asyncio
async def test_list_tools(server):
    """Test listing available tools."""
    tools = await server.mcp.list_tools()

    assert len(tools) > 0
    tool_names = [tool.name for tool in tools]
    assert "get_nodes" in tool_names
    assert "get_vms" in tool_names
    assert "get_containers" in tool_names
    assert "execute_vm_command" in tool_names


@pytest.mark.asyncio
async def test_get_nodes(server, mock_proxmox):
    """Test get_nodes tool."""
    # Mock the API chain properly
    mock_proxmox.return_value.nodes.get.return_value = [
        {"node": "node1", "status": "online"},
        {"node": "node2", "status": "online"},
    ]

    # Mock detailed node status calls with proper data types
    mock_status_1 = {
        "uptime": 123456,
        "cpuinfo": {"cpus": 8},
        "memory": {"used": 8000000000, "total": 16000000000},
    }
    mock_status_2 = {
        "uptime": 654321,
        "cpuinfo": {"cpus": 16},
        "memory": {"used": 12000000000, "total": 32000000000},
    }

    # Set up the mocking chain for node status calls
    mock_proxmox.return_value.nodes.return_value.status.get.side_effect = [
        mock_status_1,
        mock_status_2,
    ]

    response = await server.mcp.call_tool("get_nodes", {})

    # The response should be formatted text, not JSON
    assert len(response) == 1
    assert "Proxmox Nodes" in response[0].text
    assert "node1" in response[0].text
    assert "node2" in response[0].text


@pytest.mark.asyncio
async def test_get_node_status_missing_parameter(server):
    """Test get_node_status tool with missing parameter."""
    with pytest.raises(ToolError, match="Field required"):
        await server.mcp.call_tool("get_node_status", {})


@pytest.mark.asyncio
async def test_get_node_status(server, mock_proxmox):
    """Test get_node_status tool with valid parameter."""
    mock_proxmox.return_value.nodes.return_value.status.get.return_value = {
        "status": "running",
        "uptime": 123456,
        "cpuinfo": {"cpus": 4},
        "memory": {"used": 4000000000, "total": 8000000000},
    }

    response = await server.mcp.call_tool("get_node_status", {"node": "node1"})

    # The response should be formatted text, not JSON
    assert len(response) == 1
    assert "node1" in response[0].text
    assert "RUNNING" in response[0].text


@pytest.mark.asyncio
async def test_get_vms(server, mock_proxmox):
    """Test get_vms tool."""
    mock_proxmox.return_value.nodes.get.return_value = [{"node": "node1", "status": "online"}]
    mock_proxmox.return_value.nodes.return_value.qemu.get.return_value = [
        {
            "vmid": "100",
            "name": "vm1",
            "status": "running",
            "mem": 2000000000,
            "maxmem": 4000000000,
        },
        {
            "vmid": "101",
            "name": "vm2",
            "status": "stopped",
            "mem": 0,
            "maxmem": 2000000000,
        },
    ]

    # Mock VM config calls for CPU cores
    mock_config_1 = {"cores": 2}
    mock_config_2 = {"cores": 4}
    mock_proxmox.return_value.nodes.return_value.qemu.return_value.config.get.side_effect = [
        mock_config_1,
        mock_config_2,
    ]

    response = await server.mcp.call_tool("get_vms", {})

    # The response should be formatted text, not JSON
    assert len(response) == 1
    assert "Virtual Machines" in response[0].text
    assert "vm1" in response[0].text
    assert "vm2" in response[0].text


@pytest.mark.asyncio
async def test_get_containers(server, mock_proxmox):
    """Test get_containers tool."""
    mock_proxmox.return_value.nodes.get.return_value = [{"node": "node1", "status": "online"}]
    mock_proxmox.return_value.nodes.return_value.lxc.get.return_value = [
        {
            "vmid": "200",
            "name": "container1",
            "status": "running",
            "mem": 1000000000,
            "maxmem": 2000000000,
        },
        {
            "vmid": "201",
            "name": "container2",
            "status": "stopped",
            "mem": 0,
            "maxmem": 1000000000,
        },
    ]

    # Mock container config calls for CPU cores and template
    mock_config_1 = {"cores": 2, "ostemplate": "ubuntu-20.04"}
    mock_config_2 = {"cores": 1, "ostemplate": "debian-11"}
    mock_proxmox.return_value.nodes.return_value.lxc.return_value.config.get.side_effect = [
        mock_config_1,
        mock_config_2,
    ]

    response = await server.mcp.call_tool("get_containers", {})

    # The response should be formatted text, not JSON
    assert len(response) == 1
    assert "Containers" in response[0].text
    assert "container1" in response[0].text
    assert "container2" in response[0].text


@pytest.mark.asyncio
async def test_get_storage(server, mock_proxmox):
    """Test get_storage tool."""
    mock_proxmox.return_value.storage.get.return_value = [
        {"storage": "local", "type": "dir", "enabled": True},
        {"storage": "ceph", "type": "rbd", "enabled": True},
    ]

    # Mock storage status calls with proper numeric types
    mock_status_1 = {
        "used": 500000000000,
        "total": 1000000000000,
        "avail": 500000000000,
    }
    mock_status_2 = {
        "used": 2000000000000,
        "total": 5000000000000,
        "avail": 3000000000000,
    }
    mock_proxmox.return_value.nodes.return_value.storage.return_value.status.get.side_effect = [
        mock_status_1,
        mock_status_2,
    ]

    response = await server.mcp.call_tool("get_storage", {})

    # The response should be formatted text, not JSON
    assert len(response) == 1
    assert "Storage Pools" in response[0].text
    assert "local" in response[0].text
    assert "ceph" in response[0].text


@pytest.mark.asyncio
async def test_get_cluster_status(server, mock_proxmox):
    """Test get_cluster_status tool."""
    mock_proxmox.return_value.cluster.status.get.return_value = [
        {"name": "test-cluster", "type": "cluster", "quorate": 1},
        {"name": "node1", "type": "node", "online": 1},
        {"name": "node2", "type": "node", "online": 1},
    ]

    response = await server.mcp.call_tool("get_cluster_status", {})

    # The response should be formatted text, not JSON
    assert len(response) == 1
    assert "Cluster" in response[0].text
    assert "test-cluster" in response[0].text


@pytest.mark.asyncio
async def test_execute_vm_command_success(server, mock_proxmox):
    """Test successful VM command execution."""
    # Mock VM status check
    mock_status = mock_proxmox.return_value.nodes.return_value.qemu.return_value.status
    mock_status.current.get.return_value = {"status": "running"}

    # Mock the two-phase command execution
    # Phase 1: exec returns PID
    mock_agent = mock_proxmox.return_value.nodes.return_value.qemu.return_value.agent
    mock_agent.return_value.post.return_value = {"pid": 12345}

    # Phase 2: exec-status returns results
    mock_agent.return_value.get.return_value = {
        "out-data": "command output",
        "err-data": "",
        "exitcode": 0,
        "exited": 1,
    }

    response = await server.mcp.call_tool(
        "execute_vm_command", {"node": "node1", "vmid": "100", "command": "ls -l"}
    )

    # The response should be formatted text, not JSON
    assert len(response) == 1
    assert "Command Output" in response[0].text or "command output" in response[0].text


@pytest.mark.asyncio
async def test_execute_vm_command_missing_parameters(server):
    """Test VM command execution with missing parameters."""
    with pytest.raises(ToolError):
        await server.mcp.call_tool("execute_vm_command", {})


@pytest.mark.asyncio
async def test_execute_vm_command_vm_not_running(server, mock_proxmox):
    """Test VM command execution when VM is not running."""
    mock_status = mock_proxmox.return_value.nodes.return_value.qemu.return_value.status
    mock_status.current.get.return_value = {"status": "stopped"}

    with pytest.raises(ToolError, match="not running"):
        await server.mcp.call_tool(
            "execute_vm_command", {"node": "node1", "vmid": "100", "command": "ls -l"}
        )


@pytest.mark.asyncio
async def test_execute_vm_command_with_error(server, mock_proxmox):
    """Test VM command execution with command error."""
    # Mock VM status check
    mock_status = mock_proxmox.return_value.nodes.return_value.qemu.return_value.status
    mock_status.current.get.return_value = {"status": "running"}

    # Mock the two-phase command execution
    # Phase 1: exec returns PID
    mock_agent = mock_proxmox.return_value.nodes.return_value.qemu.return_value.agent
    mock_agent.return_value.post.return_value = {"pid": 12346}

    # Phase 2: exec-status returns error results
    mock_agent.return_value.get.return_value = {
        "out-data": "",
        "err-data": "command not found",
        "exitcode": 1,
        "exited": 1,
    }

    response = await server.mcp.call_tool(
        "execute_vm_command",
        {"node": "node1", "vmid": "100", "command": "invalid-command"},
    )

    # The response should be formatted text, not JSON
    assert len(response) == 1
    assert "Command Output" in response[0].text or "command not found" in response[0].text
