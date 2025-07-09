"""
Storage-related tools for Proxmox MCP.

This module provides tools for managing and monitoring Proxmox storage:
- Listing all storage pools across the cluster
- Retrieving detailed storage information including:
  * Storage type and content types
  * Usage statistics and capacity
  * Availability status
  * Node assignments

The tools implement fallback mechanisms for scenarios where
detailed storage information might be temporarily unavailable.
"""

from typing import Any, Dict, List

from mcp.types import TextContent as Content

from .base import ProxmoxTool


class StorageTools(ProxmoxTool):
    """Tools for managing Proxmox storage.

    Provides functionality for:
    - Retrieving cluster-wide storage information
    - Monitoring storage pool status and health
    - Tracking storage utilization and capacity
    - Managing storage content types

    Implements fallback mechanisms for scenarios where detailed
    storage information might be temporarily unavailable.
    """

    def get_storage(self) -> List[Content]:
        """List storage pools across the cluster with detailed status.

        Retrieves comprehensive information for each storage pool including:
        - Basic identification (name, type)
        - Content types supported (VM disks, backups, ISO images, etc.)
        - Availability status (online/offline)
        - Usage statistics:
          * Used space
          * Total capacity
          * Available space

        Implements a fallback mechanism that returns basic information
        if detailed status retrieval fails for any storage pool.

        Returns:
            List of Content objects containing formatted storage information:
            {
                "storage": "storage-name",
                "type": "storage-type",
                "content": ["content-types"],
                "status": "online/offline",
                "used": bytes,
                "total": bytes,
                "available": bytes
            }

        Raises:
            RuntimeError: If the cluster-wide storage query fails
        """
        try:
            all_storage = self.proxmox.storage.get()
            detailed_storage = [
                self._get_storage_details(store) for store in all_storage
            ]
            return self._format_response(detailed_storage, "storage")
        except Exception as e:
            self._handle_error("get storage", e)
            return []

    def _get_storage_details(self, store: Dict[str, Any]) -> Dict[str, Any]:
        """Fetch detailed storage usage or fallback to basic info."""
        storage_name = store["storage"]
        storage_type = store["type"]
        storage_node = store.get("node", "localhost")

        try:
            status = self.proxmox.nodes(storage_node).storage(storage_name).status.get()
            return self._format_storage(store, status)
        except Exception:
            return self._format_storage(store, None)

    def _format_storage(
        self, store: Dict[str, Any], status: Dict[str, Any] | None
    ) -> Dict[str, Any]:
        """Format storage data for response output."""
        return {
            "storage": store["storage"],
            "type": store["type"],
            "content": store.get("content", []),
            "status": "online" if store.get("enabled", True) else "offline",
            "used": status.get("used", 0) if status else 0,
            "total": status.get("total", 0) if status else 0,
            "available": status.get("avail", 0) if status else 0,
        }
