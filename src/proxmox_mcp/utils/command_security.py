"""
Command security utilities for VM command execution.
Provides validation, sanitization, and security controls for VM commands.
"""

import logging
import re
import shlex
from typing import List, Optional, Set

from pydantic import BaseModel


class CommandSecurityConfig(BaseModel):
    """Configuration for command security settings."""

    max_command_length: int = 1000
    timeout_seconds: int = 300
    allow_shell_operators: bool = False
    allowed_commands: Optional[Set[str]] = None
    blocked_patterns: List[str] = [
        r"rm\s+-rf\s+/",  # Dangerous rm commands
        r"dd\s+if=.*of=",  # Disk operations
        r"mkfs\.",  # Filesystem operations
        r"fdisk",  # Disk partitioning
        r"passwd",  # Password changes
        r"su\s+",  # User switching
        r"sudo\s+",  # Privilege escalation
        r"chmod\s+777",  # Dangerous permissions
    ]


class CommandValidator:
    """Validates and sanitizes VM commands for security."""

    def __init__(self, config: Optional[CommandSecurityConfig] = None):
        self.config = config or CommandSecurityConfig()
        self.logger = logging.getLogger("proxmox-mcp.command-security")

    def validate_command(self, command: str) -> str:
        """
        Validate and sanitize a command for safe execution.

        Args:
            command: Raw command string to validate

        Returns:
            str: Sanitized command safe for execution

        Raises:
            ValueError: If command fails security validation
        """
        if len(command) > self.config.max_command_length:
            raise ValueError(f"Command exceeds maximum length of {self.config.max_command_length}")

        for pattern in self.config.blocked_patterns:
            if re.search(pattern, command, re.IGNORECASE):
                self.logger.warning(f"Blocked dangerous command pattern: {pattern}")
                raise ValueError(f"Command contains blocked pattern: {pattern}")

        if not self.config.allow_shell_operators:
            dangerous_operators = ["|", "&", ";", "$(", "`", ">", "<", "||", "&&"]
            for op in dangerous_operators:
                if op in command:
                    raise ValueError(f"Shell operator '{op}' not allowed")

        if self.config.allowed_commands:
            command_parts = shlex.split(command)
            if command_parts and command_parts[0] not in self.config.allowed_commands:
                raise ValueError(f"Command '{command_parts[0]}' not in allowed list")

        try:
            parsed_command = shlex.split(command)
            sanitized = shlex.join(parsed_command)

            self.logger.info(f"Command validated successfully: {sanitized}")
            return sanitized

        except ValueError as e:
            raise ValueError(f"Invalid command syntax: {e}") from e


def create_secure_command_validator() -> CommandValidator:
    """Create a command validator with secure default settings."""
    config = CommandSecurityConfig(
        max_command_length=500,
        timeout_seconds=60,
        allow_shell_operators=False,
        allowed_commands=None,
    )
    return CommandValidator(config)
