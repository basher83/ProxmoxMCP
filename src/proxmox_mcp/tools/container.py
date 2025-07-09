"""
Container-related tools for Proxmox MCP.

This module provides tools for managing and monitoring Proxmox LXC containers:
- Listing all containers across the cluster with their status
- Retrieving detailed container information including:
  * Resource allocation (CPU, memory)
  * Runtime status
  * Node placement
  * Container template information

The tools implement fallback mechanisms for scenarios where
detailed container information might be temporarily unavailable.
"""

from typing import List, Dict, Any

from mcp.types import TextContent as Content

from .base import ProxmoxTool


class ContainerTools(ProxmoxTool):
    """Tools for managing Proxmox LXC containers.

    Provides functionality for:
    - Retrieving cluster-wide container information
    - Getting detailed container status and configuration
    - Monitoring container health and resources
    - Handling container-specific API operations

    Implements fallback mechanisms for scenarios where detailed
    container information might be temporarily unavailable.
    """


    def get_containers(self) -> List[Content]:
        """List all LXC containers across the cluster with detailed status.

        Retrieves comprehensive information for each container including:
        - Basic identification (ID, name)
        - Runtime status (running, stopped)
        - Resource allocation and usage:
          * CPU cores
          * Memory allocation and usage
        - Node placement
        - Template information

        Implements a fallback mechanism that returns basic information
        if detailed configuration retrieval fails for any container.

        Returns:
            List of Content objects containing formatted container information:
            {
                "vmid": "200",
                "name": "container-name",
                "status": "running/stopped",
                "node": "node-name",
                "cpus": core_count,
                "memory": {
                    "used": bytes,
                    "total": bytes
                },
                "template": "template-name"
            }

        Raises:
            RuntimeError: If the cluster-wide container query fails
        """
        try:
            all_containers = []
            for node_name in self._get_all_nodes():
                containers = self._get_containers_for_node(node_name)
                all_containers.extend(containers)
            return self._format_response(all_containers, "containers")
        except Exception as e:
            self._handle_error("get containers", e)
            return []

    def _get_all_nodes(self) -> List[str]:
        """Fetch all node names in the Proxmox cluster."""
        return [node["node"] for node in self.proxmox.nodes.get()]

    def _get_containers_for_node(self, node_name: str) -> List[Dict[str, Any]]:
        """Retrieve and format all containers on a given node."""
        containers = self._get_node_containers(node_name)
        return [self._get_container_details(node_name, container) for container in containers]

    def _get_node_containers(self, node_name: str) -> Any:
        """Fetch list of LXC containers from a specific node."""
        return self.proxmox.nodes(node_name).lxc.get()

    def _get_container_details(self, node_name: str, container: Dict[str, Any]) -> Dict[str, Any]:
        """Retrieve detailed info about a container or fallback to minimal info.

        Tries to fetch config info for CPU and template; falls back if failed.
        """
        vmid = container["vmid"]
        try:
            config = self.proxmox.nodes(node_name).lxc(vmid).config.get()
            cpus = config.get("cores", "N/A")
            template = config.get("ostemplate", "N/A")
        except Exception:
            cpus = "N/A"
            template = "N/A"

        return {
            "vmid": vmid,
            "name": container["name"],
            "status": container["status"],
            "node": node_name,
            "cpus": cpus,
            "memory": {
                "used": container.get("mem", 0),
                "total": container.get("maxmem", 0),
            },
            "template": template,
        }
