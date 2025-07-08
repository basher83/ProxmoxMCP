"""
Module for managing VM console operations.

This module provides functionality for interacting with VM consoles:
- Executing commands within VMs via QEMU guest agent
- Handling command execution lifecycle
- Managing command output and status
- Error handling and logging

The module implements a robust command execution system with:
- VM state verification
- Asynchronous command execution
- Detailed status tracking
- Comprehensive error handling
"""

import logging
from typing import Any


class VMConsoleManager:
    """Manager class for VM console operations.

    Provides functionality for:
    - Executing commands in VM consoles
    - Managing command execution lifecycle
    - Handling command output and errors
    - Monitoring execution status

    Uses QEMU guest agent for reliable command execution with:
    - VM state verification before execution
    - Asynchronous command processing
    - Detailed output capture
    - Comprehensive error handling
    """

    def __init__(self, proxmox_api: Any) -> None:
        """Initialize the VM console manager.

        Args:
            proxmox_api: Initialized ProxmoxAPI instance
        """
        self.proxmox = proxmox_api
        self.logger = logging.getLogger("proxmox-mcp.vm-console")

    def _validate_vm_for_execution(self, node: str, vmid: str) -> None:
        """Validate that VM exists and is running for command execution."""
        vm_status = self.proxmox.nodes(node).qemu(vmid).status.current.get()
        if vm_status["status"] != "running":
            self.logger.error(f"Failed to execute command on VM {vmid}: VM is not running")
            raise ValueError(f"VM {vmid} on node {node} is not running")

    async def _execute_command_via_agent(self, node: str, vmid: str, command: str) -> int:
        """Start command execution via QEMU guest agent and return PID."""
        endpoint = self.proxmox.nodes(node).qemu(vmid).agent
        self.logger.debug(f"Using API endpoint: {endpoint}")

        try:
            self.logger.debug(f"Executing command via agent: {command}")
            exec_result = endpoint("exec").post(command=command)
            self.logger.debug(f"Raw exec response: {exec_result}")
            self.logger.info(f"Command started with result: {exec_result}")
        except Exception as e:
            self.logger.error(f"Failed to start command: {str(e)}")
            raise RuntimeError(f"Failed to start command: {str(e)}") from e

        if "pid" not in exec_result:
            raise RuntimeError("No PID returned from command execution")

        try:
            return int(exec_result["pid"])
        except (TypeError, ValueError) as err:
            raise RuntimeError(f"Unexpected PID value: {exec_result!r}") from err

    async def _get_command_results(self, node: str, vmid: str, pid: int) -> dict[str, Any]:
        """Wait for command completion and get results."""
        import asyncio

        self.logger.info(f"Waiting for command completion (PID: {pid})...")
        await asyncio.sleep(1)  # Allow command to complete

        endpoint = self.proxmox.nodes(node).qemu(vmid).agent
        try:
            self.logger.debug(f"Getting status for PID {pid}...")
            console = endpoint("exec-status").get(pid=pid)
            self.logger.debug(f"Raw exec-status response: {console}")
            if not console:
                raise RuntimeError("No response from exec-status")
        except Exception as e:
            self.logger.error(f"Failed to get command status: {str(e)}")
            raise RuntimeError(f"Failed to get command status: {str(e)}") from e

        self.logger.info(f"Command completed with status: {console}")
        if not isinstance(console, dict):
            raise RuntimeError(f"Expected dict response, got {type(console).__name__}: {console!r}")
        return console

    def _process_command_response(self, console: Any) -> dict[str, Any]:
        """Process and format command execution response."""
        self.logger.debug(f"Raw API response type: {type(console)}")
        self.logger.debug(f"Raw API response: {console}")

        if isinstance(console, dict):
            # Handle exec-status response format
            output = console.get("out-data", "")
            error = console.get("err-data", "")
            exit_code = console.get("exitcode", 0)
            exited = console.get("exited", 0)

            if not exited:
                self.logger.warning("Command may not have completed")
        else:
            # Some versions might return data differently
            self.logger.debug(f"Unexpected response type: {type(console)}")
            output = str(console)
            error = ""
            exit_code = 0

        self.logger.debug(f"Processed output: {output}")
        self.logger.debug(f"Processed error: {error}")
        self.logger.debug(f"Processed exit code: {exit_code}")

        return {
            "success": True,
            "output": output,
            "error": error,
            "exit_code": exit_code,
        }

    async def execute_command(self, node: str, vmid: str, command: str) -> dict[str, Any]:
        """
        Execute a shell command in a VM via the QEMU guest agent.

        This method performs two main phases:
        1. **Initiation**:
           - Validates that the VM exists and is running.
           - Uses the guest agent to start the command.
           - Captures the command's PID for tracking.

        2. **Result Collection**:
           - Polls the guest agent for command status and output.
           - Collects stdout, stderr, and exit code.

        **Requirements**:
        - VM must be powered on.
        - QEMU guest agent must be installed and running.
        - Sufficient permissions for command execution.

        Args:
            node (str): Name of the Proxmox node (e.g., "pve1").
            vmid (str): ID of the target VM (e.g., "100").
            command (str): Shell command to run inside the VM.

        Returns:
            dict[str, Any]: Result of the command execution:
                {
                    "success": bool,
                    "output": str,
                    "error": str,
                    "exit_code": int
                }

        Raises:
            ValueError: If VM is not found, not running, or agent is unavailable.
            RuntimeError: If command execution or status retrieval fails.
        """
        try:
            self._log_command_start(node, vmid, command)

            self._validate_vm_for_execution(node, vmid)

            pid = await self._execute_command_via_agent(node, vmid, command)

            console_output = await self._get_command_results(node, vmid, pid)

            result = self._process_command_response(console_output)

            self._log_command_success(node, vmid, command)

            return result

        except ValueError:
            raise
        except Exception as e:
            self._handle_command_exception(e, node, vmid)

    def _log_command_start(self, node: str, vmid: str, command: str) -> None:
        self.logger.info(f"Executing command on VM {vmid} (node: {node}): {command}")

    def _log_command_success(self, node: str, vmid: str, command: str) -> None:
        self.logger.debug(f"Executed command '{command}' on VM {vmid} (node: {node})")

    def _handle_command_exception(self, e: Exception, node: str, vmid: str) -> None:
        self.logger.error(f"Failed to execute command on VM {vmid}: {str(e)}")
        if "not found" in str(e).lower():
            raise ValueError(f"VM {vmid} not found on node {node}") from e
        raise RuntimeError(f"Failed to execute command: {str(e)}") from e
