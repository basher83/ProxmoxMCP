"""
ProxmoxMCP exception hierarchy for standardized error handling.

This module defines a comprehensive exception hierarchy for the ProxmoxMCP
project, providing structured error handling and consistent error reporting
across all components. The hierarchy is designed to map common Proxmox API
errors to specific exception types while maintaining compatibility with
existing error handling patterns.

Exception Categories:
- Base ProxmoxMCP exceptions
- Authentication and authorization errors
- Resource and connectivity errors
- Configuration and validation errors
- Security-related errors
- Tool-specific operational errors

Each exception includes contextual information to aid in debugging and
provides structured error reporting for both logging and user feedback.
"""

from typing import Any, Dict, Optional


class ProxmoxMCPError(Exception):
    """Base exception for all ProxmoxMCP-related errors.

    Provides common functionality for all ProxmoxMCP exceptions including:
    - Structured error context
    - Error categorization
    - Enhanced logging support
    - Standardized error reporting

    All ProxmoxMCP exceptions should inherit from this base class to ensure
    consistent error handling and reporting across the application.
    """

    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        cause: Optional[Exception] = None,
    ):
        """Initialize ProxmoxMCP base exception.

        Args:
            message: Human-readable error message
            error_code: Optional error code for programmatic handling
            context: Optional dictionary with error context information
            cause: Optional underlying exception that caused this error
        """
        super().__init__(message)
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        self.context = context or {}
        self.cause = cause

    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for structured logging.

        Returns:
            Dictionary representation of the exception
        """
        return {
            "error_type": self.__class__.__name__,
            "error_code": self.error_code,
            "message": self.message,
            "context": self.context,
            "cause": str(self.cause) if self.cause else None,
        }

    def __str__(self) -> str:
        """String representation of the exception."""
        parts = [self.message]

        if self.error_code and self.error_code != self.__class__.__name__:
            parts.append(f"(Code: {self.error_code})")

        if self.context:
            context_str = ", ".join(f"{k}={v}" for k, v in self.context.items())
            parts.append(f"[{context_str}]")

        return " ".join(parts)


# Authentication and Authorization Errors


class ProxmoxAuthError(ProxmoxMCPError):
    """Authentication-related errors.

    Raised when authentication with the Proxmox API fails due to:
    - Invalid credentials (username, token)
    - Expired or revoked tokens
    - Authentication service unavailability
    - Token encryption/decryption failures
    """

    def __init__(self, message: str, auth_method: Optional[str] = None, **kwargs):
        """Initialize authentication error.

        Args:
            message: Error description
            auth_method: Authentication method that failed (e.g., "token", "password")
            **kwargs: Additional arguments passed to base class
        """
        context = kwargs.get("context", {})
        if auth_method:
            context["auth_method"] = auth_method
        kwargs["context"] = context

        super().__init__(message, **kwargs)


class ProxmoxPermissionError(ProxmoxMCPError):
    """Permission and authorization errors.

    Raised when the authenticated user lacks sufficient permissions for:
    - Accessing specific Proxmox resources
    - Performing requested operations
    - Reading sensitive configuration data
    - Executing commands in VMs
    """

    def __init__(
        self,
        message: str,
        resource: Optional[str] = None,
        operation: Optional[str] = None,
        **kwargs,
    ):
        """Initialize permission error.

        Args:
            message: Error description
            resource: Resource that was accessed (e.g., "vm", "node", "storage")
            operation: Operation that was attempted (e.g., "read", "write", "execute")
            **kwargs: Additional arguments passed to base class
        """
        context = kwargs.get("context", {})
        if resource:
            context["resource"] = resource
        if operation:
            context["operation"] = operation
        kwargs["context"] = context

        super().__init__(message, **kwargs)


# Resource and Connectivity Errors


class ProxmoxConnectionError(ProxmoxMCPError):
    """Network connectivity and API communication errors.

    Raised when communication with the Proxmox API fails due to:
    - Network connectivity issues
    - SSL/TLS certificate problems
    - API service unavailability
    - Timeout errors
    - DNS resolution failures
    """

    def __init__(
        self, message: str, host: Optional[str] = None, port: Optional[int] = None, **kwargs
    ):
        """Initialize connection error.

        Args:
            message: Error description
            host: Proxmox host that was being contacted
            port: Port number that was being used
            **kwargs: Additional arguments passed to base class
        """
        context = kwargs.get("context", {})
        if host:
            context["host"] = host
        if port:
            context["port"] = port
        kwargs["context"] = context

        super().__init__(message, **kwargs)


class ProxmoxResourceNotFoundError(ProxmoxMCPError):
    """Resource not found errors.

    Raised when requested Proxmox resources cannot be found:
    - VMs that don't exist or are not accessible
    - Nodes that are offline or not part of the cluster
    - Storage pools that are not configured
    - Containers that have been removed
    """

    def __init__(
        self,
        message: str,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        **kwargs,
    ):
        """Initialize resource not found error.

        Args:
            message: Error description
            resource_type: Type of resource (e.g., "vm", "node", "storage")
            resource_id: ID of the resource that wasn't found
            **kwargs: Additional arguments passed to base class
        """
        context = kwargs.get("context", {})
        if resource_type:
            context["resource_type"] = resource_type
        if resource_id:
            context["resource_id"] = resource_id
        kwargs["context"] = context

        super().__init__(message, **kwargs)


class ProxmoxResourceUnavailableError(ProxmoxMCPError):
    """Resource temporarily unavailable errors.

    Raised when resources exist but are not currently accessible:
    - VMs that are powered off or in maintenance mode
    - Nodes that are temporarily offline
    - Services that are restarting or under heavy load
    - QEMU guest agents that are not running
    """

    def __init__(
        self,
        message: str,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        reason: Optional[str] = None,
        **kwargs,
    ):
        """Initialize resource unavailable error.

        Args:
            message: Error description
            resource_type: Type of resource (e.g., "vm", "node", "storage")
            resource_id: ID of the unavailable resource
            reason: Reason for unavailability (e.g., "powered_off", "agent_not_running")
            **kwargs: Additional arguments passed to base class
        """
        context = kwargs.get("context", {})
        if resource_type:
            context["resource_type"] = resource_type
        if resource_id:
            context["resource_id"] = resource_id
        if reason:
            context["reason"] = reason
        kwargs["context"] = context

        super().__init__(message, **kwargs)


# Configuration and Validation Errors


class ProxmoxConfigError(ProxmoxMCPError):
    """Configuration-related errors.

    Raised when configuration issues prevent proper operation:
    - Invalid configuration file format
    - Missing required configuration parameters
    - Configuration validation failures
    - Environment variable resolution errors
    """

    def __init__(
        self,
        message: str,
        config_file: Optional[str] = None,
        config_field: Optional[str] = None,
        **kwargs,
    ):
        """Initialize configuration error.

        Args:
            message: Error description
            config_file: Configuration file that caused the error
            config_field: Specific configuration field that is invalid
            **kwargs: Additional arguments passed to base class
        """
        context = kwargs.get("context", {})
        if config_file:
            context["config_file"] = config_file
        if config_field:
            context["config_field"] = config_field
        kwargs["context"] = context

        super().__init__(message, **kwargs)


class ProxmoxValidationError(ProxmoxMCPError):
    """Input validation and data format errors.

    Raised when input data fails validation:
    - Invalid VM IDs or node names
    - Malformed command parameters
    - Data type validation failures
    - Parameter range or format errors
    """

    def __init__(
        self,
        message: str,
        field: Optional[str] = None,
        value: Optional[Any] = None,
        expected_type: Optional[str] = None,
        **kwargs,
    ):
        """Initialize validation error.

        Args:
            message: Error description
            field: Field name that failed validation
            value: Value that failed validation (be careful with sensitive data)
            expected_type: Expected data type or format
            **kwargs: Additional arguments passed to base class
        """
        context = kwargs.get("context", {})
        if field:
            context["field"] = field
        if value is not None and not _is_sensitive_field(field):
            context["value"] = str(value)[:100]  # Truncate long values
        if expected_type:
            context["expected_type"] = expected_type
        kwargs["context"] = context

        super().__init__(message, **kwargs)


# Security-Related Errors


class ProxmoxSecurityError(ProxmoxMCPError):
    """Security-related errors and violations.

    Raised when security policies are violated or security threats are detected:
    - Command injection attempts
    - Unauthorized operation attempts
    - Security policy violations
    - Suspicious activity detection
    """

    def __init__(
        self,
        message: str,
        violation_type: Optional[str] = None,
        severity: Optional[str] = None,
        **kwargs,
    ):
        """Initialize security error.

        Args:
            message: Error description
            violation_type: Type of security violation (e.g., "injection", "unauthorized")
            severity: Severity level (e.g., "low", "medium", "high", "critical")
            **kwargs: Additional arguments passed to base class
        """
        context = kwargs.get("context", {})
        if violation_type:
            context["violation_type"] = violation_type
        if severity:
            context["severity"] = severity
        kwargs["context"] = context

        super().__init__(message, **kwargs)


# Tool-Specific Operational Errors


class ProxmoxToolError(ProxmoxMCPError):
    """Tool-specific operational errors.

    Raised when MCP tool operations fail due to:
    - Tool-specific logic errors
    - Unexpected API response formats
    - Data processing failures
    - Tool configuration issues
    """

    def __init__(
        self,
        message: str,
        tool_name: Optional[str] = None,
        operation: Optional[str] = None,
        **kwargs,
    ):
        """Initialize tool error.

        Args:
            message: Error description
            tool_name: Name of the tool that encountered the error
            operation: Operation that failed (e.g., "get_vms", "execute_command")
            **kwargs: Additional arguments passed to base class
        """
        context = kwargs.get("context", {})
        if tool_name:
            context["tool_name"] = tool_name
        if operation:
            context["operation"] = operation
        kwargs["context"] = context

        super().__init__(message, **kwargs)


class ProxmoxAPIError(ProxmoxMCPError):
    """Proxmox API-specific errors.

    Raised when the Proxmox API returns unexpected responses:
    - API version compatibility issues
    - Malformed API responses
    - API rate limiting
    - API maintenance mode
    """

    def __init__(
        self,
        message: str,
        api_endpoint: Optional[str] = None,
        status_code: Optional[int] = None,
        response_data: Optional[str] = None,
        **kwargs,
    ):
        """Initialize API error.

        Args:
            message: Error description
            api_endpoint: API endpoint that caused the error
            status_code: HTTP status code returned by the API
            response_data: Response data from the API (truncated for logging)
            **kwargs: Additional arguments passed to base class
        """
        context = kwargs.get("context", {})
        if api_endpoint:
            context["api_endpoint"] = api_endpoint
        if status_code:
            context["status_code"] = status_code
        if response_data:
            context["response_data"] = str(response_data)[:200]  # Truncate long responses
        kwargs["context"] = context

        super().__init__(message, **kwargs)


# Utility Functions


def _is_sensitive_field(field_name: Optional[str]) -> bool:
    """Check if a field name indicates sensitive data that shouldn't be logged.

    Args:
        field_name: Name of the field to check

    Returns:
        True if the field is considered sensitive
    """
    if not field_name:
        return False

    sensitive_keywords = ["password", "token", "secret", "key", "credential", "auth"]
    field_lower = field_name.lower()

    return any(keyword in field_lower for keyword in sensitive_keywords)


def map_proxmox_error(
    error: Exception, operation: str = "", resource_type: str = "", resource_id: str = ""
) -> ProxmoxMCPError:
    """Map a generic exception to an appropriate ProxmoxMCP exception.

    This function analyzes generic exceptions (often from the proxmoxer library)
    and maps them to specific ProxmoxMCP exception types based on error patterns
    and context information.

    Args:
        error: The original exception to map
        operation: Operation that was being performed when the error occurred
        resource_type: Type of resource involved (e.g., "vm", "node")
        resource_id: ID of the resource involved

    Returns:
        Appropriate ProxmoxMCP exception with enhanced context
    """
    error_str = str(error).lower()
    context = {
        "original_error": str(error),
        "operation": operation,
        "resource_type": resource_type,
        "resource_id": resource_id,
    }

    # Authentication errors
    if any(keyword in error_str for keyword in ["auth", "login", "credential", "token"]):
        return ProxmoxAuthError(
            f"Authentication failed during {operation}", context=context, cause=error
        )

    # Permission errors
    if any(keyword in error_str for keyword in ["permission", "access denied", "forbidden", "403"]):
        return ProxmoxPermissionError(
            f"Permission denied for {operation}",
            resource=resource_type,
            operation=operation,
            context=context,
            cause=error,
        )

    # Connection errors
    if any(keyword in error_str for keyword in ["connection", "network", "timeout", "unreachable"]):
        return ProxmoxConnectionError(
            f"Connection failed during {operation}", context=context, cause=error
        )

    # Resource not found errors
    if any(keyword in error_str for keyword in ["not found", "404", "does not exist"]):
        return ProxmoxResourceNotFoundError(
            f"Resource not found during {operation}",
            resource_type=resource_type,
            resource_id=resource_id,
            context=context,
            cause=error,
        )

    # Resource unavailable errors
    if any(
        keyword in error_str for keyword in ["offline", "stopped", "unavailable", "not running"]
    ):
        return ProxmoxResourceUnavailableError(
            f"Resource unavailable during {operation}",
            resource_type=resource_type,
            resource_id=resource_id,
            context=context,
            cause=error,
        )

    # Default to generic tool error
    return ProxmoxToolError(
        f"Operation failed: {operation}", operation=operation, context=context, cause=error
    )
