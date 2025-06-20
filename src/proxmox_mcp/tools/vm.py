"""
VM-related tools for Proxmox MCP.

This module provides tools for managing and interacting with Proxmox VMs:
- Listing all VMs across the cluster with their status
- Retrieving detailed VM information including:
  * Resource allocation (CPU, memory)
  * Runtime status
  * Node placement
- Executing commands within VMs via QEMU guest agent
- Handling VM console operations

The tools implement fallback mechanisms for scenarios where
detailed VM information might be temporarily unavailable.
"""

from typing import Any, List

from mcp.types import TextContent as Content

from .base import ProxmoxTool
from .console.manager import VMConsoleManager


class VMTools(ProxmoxTool):
    """Tools for managing Proxmox VMs.

    Provides functionality for:
    - Retrieving cluster-wide VM information
    - Getting detailed VM status and configuration
    - Executing commands within VMs
    - Managing VM console operations

    Implements fallback mechanisms for scenarios where detailed
    VM information might be temporarily unavailable. Integrates
    with QEMU guest agent for VM command execution.
    """

    def __init__(self, proxmox_api: Any) -> None:
        """Initialize VM tools.

        Args:
            proxmox_api: Initialized ProxmoxAPI instance
        """
        super().__init__(proxmox_api)
        self.console_manager = VMConsoleManager(proxmox_api)

    def get_vms(self) -> List[Content]:
        """List all virtual machines across the cluster with detailed status.

        Retrieves comprehensive information for each VM including:
        - Basic identification (ID, name)
        - Runtime status (running, stopped)
        - Resource allocation and usage:
          * CPU cores
          * Memory allocation and usage
        - Node placement

        Implements an optimized approach that minimizes API calls by:
        - Batching VM queries per node
        - Using fallback data when detailed config is unavailable
        - Reducing redundant API round trips
        - Isolating node-level failures to prevent total operation failure

        Returns:
            List of Content objects containing formatted VM information:
            {
                "vmid": "100",
                "name": "vm-name",
                "status": "running/stopped",
                "node": "node-name",
                "cpus": core_count,
                "memory": {
                    "used": bytes,
                    "total": bytes
                }
            }

        Raises:
            RuntimeError: If the cluster-wide VM query fails
        """
        try:
            result = []
            nodes = self.proxmox.nodes.get()

            for node in nodes:
                node_name = node["node"]
                try:
                    vms = self.proxmox.nodes(node_name).qemu.get()

                    vm_configs = {}
                    for vm in vms:
                        vmid = vm["vmid"]
                        try:
                            config = (
                                self.proxmox.nodes(node_name).qemu(vmid).config.get()
                            )
                            vm_configs[vmid] = config
                        except Exception:
                            vm_configs[vmid] = None

                    for vm in vms:
                        vmid = vm["vmid"]
                        config = vm_configs.get(vmid)

                        vm_data = {
                            "vmid": vmid,
                            "name": vm["name"],
                            "status": vm["status"],
                            "node": node_name,
                            "cpus": config.get("cores", "N/A") if config else "N/A",
                            "memory": {
                                "used": vm.get("mem", 0),
                                "total": vm.get("maxmem", 0),
                            },
                        }
                        result.append(vm_data)

                except Exception as e:
                    self.logger.warning(f"Failed to get VMs for node {node_name}: {e}")
                    continue

            return self._format_response(result, "vms")
        except Exception as e:
            self._handle_error("get VMs", e)
            return []

    async def execute_command(
        self, node: str, vmid: str, command: str
    ) -> List[Content]:
        """Execute a command in a VM via QEMU guest agent.

        Uses the QEMU guest agent to execute commands within a running VM.
        Requires:
        - VM must be running
        - QEMU guest agent must be installed and running in the VM
        - Command execution permissions must be enabled

        Args:
            node: Host node name (e.g., 'pve1', 'proxmox-node2')
            vmid: VM ID number (e.g., '100', '101')
            command: Shell command to run (e.g., 'uname -a', 'systemctl status nginx')

        Returns:
            List of Content objects containing formatted command output:
            {
                "success": true/false,
                "output": "command output",
                "error": "error message if any"
            }

        Raises:
            ValueError: If VM is not found, not running, or guest agent is not available
            RuntimeError: If command execution fails due to permissions or other issues
        """
        try:
            result = await self.console_manager.execute_command(node, vmid, command)
            # Use the command output formatter from ProxmoxFormatters
            from ..formatting import ProxmoxFormatters

            formatted = ProxmoxFormatters.format_command_output(
                success=result["success"],
                command=command,
                output=result["output"],
                error=result.get("error"),
            )
            return [Content(type="text", text=formatted)]
        except Exception as e:
            self._handle_error(f"execute command on VM {vmid}", e)
            return []
