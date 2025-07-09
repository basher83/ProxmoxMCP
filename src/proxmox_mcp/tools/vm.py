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

from typing import Any, Dict, List

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
            for node_name in self._get_all_nodes():
                vms = self._get_vms_for_node(node_name)
                result.extend(vms)
            return self._format_response(result, "vms")
        except Exception as e:
            self._handle_error("get VMs", e)
            return []

    def _get_all_nodes(self) -> List[str]:
        """Retrieve a list of all node names in the cluster."""
        return [node["node"] for node in self.proxmox.nodes.get()]

    def _get_vms_for_node(self, node_name: str) -> List[Dict[str, Any]]:
        """Fetch VM details for a specific node, with config fallback and error isolation."""
        try:
            vms = self.proxmox.nodes(node_name).qemu.get()
            configs = self._get_vm_configs(node_name, [vm["vmid"] for vm in vms])
            return [
                self._format_vm(vm, configs.get(vm["vmid"]), node_name) for vm in vms
            ]
        except Exception as e:
            self.logger.warning(f"Failed to get VMs for node {node_name}: {e}")
            return []

    def _get_vm_configs(self, node_name: str, vmids: List[int]) -> Dict[int, Any]:
        """Batch fetch VM config data with fallback."""
        configs = {}
        for vmid in vmids:
            try:
                config = self.proxmox.nodes(node_name).qemu(vmid).config.get()
                configs[vmid] = config
            except Exception:
                configs[vmid] = None
        return configs

    def _format_vm(
        self, vm: Dict[str, Any], config: Dict[str, Any] | None, node_name: str
    ) -> Dict[str, Any]:
        """Format VM data, using fallback values when config is unavailable."""
        return {
            "vmid": vm["vmid"],
            "name": vm["name"],
            "status": vm["status"],
            "node": node_name,
            "cpus": config.get("cores", "N/A") if config else "N/A",
            "memory": {
                "used": vm.get("mem", 0),
                "total": vm.get("maxmem", 0),
            },
        }

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
