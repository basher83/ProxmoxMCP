"""
Base classes and utilities for Proxmox MCP tools.

This module provides the foundation for all Proxmox MCP tools, including:
- Base tool class with common functionality
- Response formatting utilities
- Error handling mechanisms
- Logging setup

All tool implementations inherit from the ProxmoxTool base class to ensure
consistent behavior and error handling across the MCP server.
"""

import logging
from typing import Any, Callable, Dict, List, Optional

from mcp.types import TextContent as Content
from proxmoxer import ProxmoxAPI

from ..formatting import ProxmoxTemplates


class ProxmoxTool:
    """Base class for Proxmox MCP tools.

    This class provides common functionality used by all Proxmox tool implementations:
    - Proxmox API access
    - Standardized logging
    - Response formatting
    - Error handling

    All tool classes should inherit from this base class to ensure consistent
    behavior and error handling across the MCP server.
    """

    def __init__(self, proxmox_api: ProxmoxAPI):
        """Initialize the tool.

        Args:
            proxmox_api: Initialized ProxmoxAPI instance
        """
        self.proxmox = proxmox_api
        self.logger = logging.getLogger(
            f"proxmox-mcp.{self.__class__.__name__.lower()}"
        )

    def _format_response(
        self, data: Any, resource_type: Optional[str] = None
    ) -> List[Content]:
        """Format response data into MCP content using templates.

        This method handles formatting of various Proxmox resource types into
        consistent MCP content responses. It uses specialized templates for
        different resource types (nodes, VMs, storage, etc.) and falls back
        to JSON formatting for unknown types.

        Args:
            data: Raw data from Proxmox API to format
            resource_type: Type of resource for template selection. Valid types:
                         'nodes', 'node_status', 'vms', 'storage', 'containers', 'cluster'

        Returns:
            List of Content objects formatted according to resource type
        """
        formatted = self._get_formatted_content(data, resource_type)
        return [Content(type="text", text=formatted)]

    def _get_formatted_content(self, data: Any, resource_type: Optional[str]) -> str:
        """Get formatted content for the specified resource type.

        Args:
            data: Raw data from Proxmox API to format
            resource_type: Type of resource for template selection

        Returns:
            Formatted string content
        """
        if resource_type == "node_status":
            return self._format_node_status(data)

        # Use dictionary lookup for simple template mappings
        template_mapping: Dict[str, Callable[[Any], str]] = {
            "nodes": ProxmoxTemplates.node_list,
            "vms": ProxmoxTemplates.vm_list,
            "storage": ProxmoxTemplates.storage_list,
            "containers": ProxmoxTemplates.container_list,
            "cluster": ProxmoxTemplates.cluster_status,
        }

        if resource_type in template_mapping:
            return template_mapping[resource_type](data)

        # Fallback to JSON formatting for unknown types
        import json

        return json.dumps(data, indent=2)

    def _format_node_status(self, data: Any) -> str:
        """Format node status data with special handling for tuple format.

        Args:
            data: Node status data (either tuple or dict)

        Returns:
            Formatted node status string
        """
        if isinstance(data, tuple) and len(data) == 2:
            return ProxmoxTemplates.node_status(data[0], data[1])
        return ProxmoxTemplates.node_status(
            "unknown", data if isinstance(data, dict) else {}
        )

    def _handle_error(self, operation: str, error: Exception) -> None:
        """Handle and log errors from Proxmox operations.

        Provides standardized error handling across all tools by:
        - Logging errors with appropriate context
        - Categorizing errors into specific exception types
        - Converting Proxmox-specific errors into standard Python exceptions

        Args:
            operation: Description of the operation that failed (e.g., "get node status")
            error: The exception that occurred during the operation

        Raises:
            ValueError: For invalid input, missing resources, or permission issues
            RuntimeError: For unexpected errors or API failures
        """
        error_msg = str(error)
        self.logger.error(f"Failed to {operation}: {error_msg}")

        if "not found" in error_msg.lower():
            raise ValueError(f"Resource not found: {error_msg}")
        if "permission denied" in error_msg.lower():
            raise ValueError(f"Permission denied: {error_msg}")
        if "invalid" in error_msg.lower():
            raise ValueError(f"Invalid input: {error_msg}")

        raise RuntimeError(f"Failed to {operation}: {error_msg}")
