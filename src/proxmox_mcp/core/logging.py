"""
Logging configuration for the Proxmox MCP server.

This module handles logging setup and configuration:
- File and console logging handlers
- Log level management
- Format customization
- Handler lifecycle management

The logging system supports:
- Configurable log levels
- File-based logging with path resolution
- Console logging for errors
- Custom format strings
- Multiple handler management
"""

import logging
import os
from typing import List, Optional

from ..config.models import LoggingConfig


def setup_logging(config: LoggingConfig) -> logging.Logger:
    """Configure and initialize logging system.

    Sets up a comprehensive logging system with:
    - File logging (if configured)
    - Console logging for errors
    - Removes existing handlers and installs new ones

    Args:
        config: Logging configuration containing:
            - level: Log level (e.g., "INFO")
            - format: Log format string
            - file: Optional log file path

    Returns:
        Logger instance for "proxmox-mcp"
    """
    log_file = _resolve_log_path(config.file)
    handlers = _create_logging_handlers(config, log_file)
    _configure_logger(handlers, config.level, config.format)

    return logging.getLogger("proxmox-mcp")


def _resolve_log_path(path: Optional[str]) -> Optional[str]:
    """Resolve relative log file path to absolute."""
    if path and not os.path.isabs(path):
        return os.path.join(os.getcwd(), path)
    return path


def _create_logging_handlers(
    config: LoggingConfig, log_file: Optional[str]
) -> List[logging.Handler]:
    """Create file and console handlers with appropriate log levels."""
    handlers: List[logging.Handler] = []

    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(getattr(logging, config.level.upper()))
        handlers.append(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)
    handlers.append(console_handler)

    return handlers


def _configure_logger(handlers: List[logging.Handler], level: str, fmt: str) -> None:
    """Apply formatters, clear existing handlers, and set up new ones."""
    formatter = logging.Formatter(fmt)
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))

    # Remove old handlers
    for h in list(root_logger.handlers):  # type: ignore[assignment]
        root_logger.removeHandler(h)

    # Add new handlers
    for h in handlers:
        h.setFormatter(formatter)
        root_logger.addHandler(h)
