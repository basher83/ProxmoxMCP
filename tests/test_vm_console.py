"""
Tests for VM console operations.
"""

from unittest.mock import Mock

import pytest

from proxmox_mcp.tools.console import VMConsoleManager


@pytest.fixture
def mock_proxmox():
    """Fixture to create a mock ProxmoxAPI instance."""
    mock = Mock()
    # Setup chained mock calls for VM status check
    mock.nodes.return_value.qemu.return_value.status.current.get.return_value = {
        "status": "running"
    }

    # Setup agent endpoint
    agent_mock = mock.nodes.return_value.qemu.return_value.agent

    # Mock exec endpoint - returns PID
    exec_mock = Mock()
    exec_mock.post.return_value = {"pid": 12345}
    agent_mock.return_value = exec_mock

    # Mock exec-status endpoint - returns command result
    exec_status_mock = Mock()
    exec_status_mock.get.return_value = {
        "out-data": "command output",
        "err-data": "",
        "exitcode": 0,
        "exited": 1,
    }

    # Set up the agent call chain
    def agent_endpoint(endpoint_name):
        if endpoint_name == "exec":
            return exec_mock
        elif endpoint_name == "exec-status":
            return exec_status_mock
        return Mock()

    agent_mock.side_effect = agent_endpoint

    return mock


@pytest.fixture
def vm_console(mock_proxmox):
    """Fixture to create a VMConsoleManager instance."""
    return VMConsoleManager(mock_proxmox)


@pytest.mark.asyncio
async def test_execute_command_success(vm_console, mock_proxmox):
    """Test successful command execution."""
    result = await vm_console.execute_command("node1", "100", "ls -l")

    assert result["success"] is True
    assert result["output"] == "command output"
    assert result["error"] == ""
    assert result["exit_code"] == 0

    # Verify correct API calls
    mock_proxmox.nodes.assert_called_with("node1")
    mock_proxmox.nodes.return_value.qemu.assert_called_with("100")


@pytest.mark.asyncio
async def test_execute_command_vm_not_running(vm_console, mock_proxmox):
    """Test command execution on stopped VM."""
    mock_proxmox.nodes.return_value.qemu.return_value.status.current.get.return_value = {
        "status": "stopped"
    }

    with pytest.raises(ValueError, match="not running"):
        await vm_console.execute_command("node1", "100", "ls -l")


@pytest.mark.asyncio
async def test_execute_command_vm_not_found(vm_console, mock_proxmox):
    """Test command execution on non-existent VM."""
    mock_proxmox.nodes.return_value.qemu.return_value.status.current.get.side_effect = (
        Exception("VM not found")
    )

    with pytest.raises(ValueError, match="not found"):
        await vm_console.execute_command("node1", "100", "ls -l")


@pytest.mark.asyncio
async def test_execute_command_failure(vm_console, mock_proxmox):
    """Test command execution failure."""
    # Override the agent mock to raise an exception on exec
    agent_mock = mock_proxmox.nodes.return_value.qemu.return_value.agent

    def agent_endpoint_failure(endpoint_name):
        if endpoint_name == "exec":
            exec_mock = Mock()
            exec_mock.post.side_effect = Exception("Command failed")
            return exec_mock
        return Mock()

    agent_mock.side_effect = agent_endpoint_failure

    with pytest.raises(RuntimeError, match="Failed to execute command"):
        await vm_console.execute_command("node1", "100", "ls -l")


@pytest.mark.asyncio
async def test_execute_command_with_error_output(vm_console, mock_proxmox):
    """Test command execution with error output."""
    # Override the default exec-status mock for this test
    agent_mock = mock_proxmox.nodes.return_value.qemu.return_value.agent
    exec_status_mock = Mock()
    exec_status_mock.get.return_value = {
        "out-data": "",
        "err-data": "command error",
        "exitcode": 1,
        "exited": 1,
    }

    def agent_endpoint(endpoint_name):
        if endpoint_name == "exec":
            exec_mock = Mock()
            exec_mock.post.return_value = {"pid": 12345}
            return exec_mock
        elif endpoint_name == "exec-status":
            return exec_status_mock
        return Mock()

    agent_mock.side_effect = agent_endpoint

    result = await vm_console.execute_command("node1", "100", "invalid-command")

    assert result["success"] is True  # Success refers to API call, not command
    assert result["output"] == ""
    assert result["error"] == "command error"
    assert result["exit_code"] == 1
