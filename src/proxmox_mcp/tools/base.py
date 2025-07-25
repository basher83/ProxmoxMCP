"""
Base classes and utilities for Proxmox MCP tools.

This module provides the foundation for all Proxmox MCP tools, including:
- Base tool class with common functionality
- Response formatting utilities
- Structured error handling with ProxmoxMCP exceptions
- Logging setup

All tool implementations inherit from the ProxmoxTool base class to ensure
consistent behavior and error handling across the MCP server.
"""

import logging
from typing import Any, Callable, Dict, List, Optional

from mcp.types import TextContent as Content
from proxmoxer import ProxmoxAPI

from ..exceptions import ProxmoxMCPError, map_proxmox_error
from ..formatting import ProxmoxTemplates


class ProxmoxTool:
    """Base class for Proxmox MCP tools with structured exception handling.

    This class provides common functionality used by all Proxmox tool implementations:
    - Proxmox API access
    - Standardized logging
    - Response formatting
    - Structured error handling with ProxmoxMCP exceptions

    All tool classes should inherit from this base class to ensure consistent
    behavior and error handling across the MCP server.
    """

    def __init__(self, proxmox_api: ProxmoxAPI):
        """Initialize the tool.

        Args:
            proxmox_api: Initialized ProxmoxAPI instance
        """
        self.proxmox = proxmox_api
        self.logger = logging.getLogger(f"proxmox-mcp.{self.__class__.__name__.lower()}")

    def _format_response(self, data: Any, resource_type: Optional[str] = None) -> List[Content]:
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
        return ProxmoxTemplates.node_status("unknown", data if isinstance(data, dict) else {})

    def _handle_error(self, operation: str, error: Exception, 
                     resource_type: str = "", resource_id: str = "") -> None:
        """Handle and log errors from Proxmox operations with structured exceptions.

        Provides standardized error handling across all tools by:
        - Logging errors with appropriate context
        - Mapping generic exceptions to structured ProxmoxMCP exceptions
        - Preserving error context for debugging and monitoring
        - Ensuring consistent error reporting across all tools

        Args:
            operation: Description of the operation that failed (e.g., "get node status")
            error: The exception that occurred during the operation
            resource_type: Type of resource involved (e.g., "vm", "node", "storage")
            resource_id: ID of the resource involved (e.g., VM ID, node name)

        Raises:
            ProxmoxMCPError: Appropriate structured exception based on error analysis
        """
        # Don't re-wrap ProxmoxMCP exceptions
        if isinstance(error, ProxmoxMCPError):
            self.logger.error(f"Operation '{operation}' failed: {error}")
            raise error
        
        # Map generic exceptions to structured ProxmoxMCP exceptions
        mapped_exception = map_proxmox_error(
            error=error,
            operation=operation,
            resource_type=resource_type,
            resource_id=resource_id
        )
        
        # Add tool-specific context
        mapped_exception.context.update({
            "tool_class": self.__class__.__name__,
            "proxmox_api_available": self.proxmox is not None
        })
        
        # Log with structured context
        self.logger.error(
            f"Tool operation failed: {operation}. "
            f"Error: {mapped_exception.error_code} - {mapped_exception.message}",
            extra={"error_context": mapped_exception.context}
        )
        
        raise mapped_exception from error
