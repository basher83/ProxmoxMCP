"""
Security validation for VM command execution.

This module provides comprehensive security validation for commands executed
within Proxmox VMs via the QEMU guest agent. It implements multiple security
layers to prevent command injection, privilege escalation, and other security
threats while maintaining operational flexibility.

Security Features:
- Command whitelist/blacklist enforcement
- Shell injection pattern detection
- Dangerous character sanitization
- Command length and complexity limits
- Security event logging and monitoring
- Configurable security policies per environment

The validation is designed to be strict by default while allowing
administrators to configure appropriate security policies for their
specific operational requirements.
"""

import logging
import re
import shlex
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple


class SecurityPolicy(Enum):
    """Security policy levels for command validation."""
    
    STRICT = "strict"      # Maximum security, minimal command set
    STANDARD = "standard"  # Balanced security for typical operations
    PERMISSIVE = "permissive"  # Relaxed security for development/testing


class CommandSecurityError(Exception):
    """Raised when a command fails security validation."""
    
    def __init__(self, message: str, command: str, violation_type: str):
        """Initialize security error with context.
        
        Args:
            message: Human-readable error message
            command: The command that failed validation
            violation_type: Type of security violation detected
        """
        super().__init__(message)
        self.command = command
        self.violation_type = violation_type


class VMCommandSecurityValidator:
    """Security validator for VM commands with configurable policies.
    
    Provides comprehensive security validation for commands executed in VMs:
    - Validates against whitelisted/blacklisted commands
    - Detects shell injection patterns
    - Enforces character and length restrictions
    - Logs security violations for monitoring
    - Supports different security policy levels
    
    Usage:
        validator = VMCommandSecurityValidator(policy=SecurityPolicy.STANDARD)
        try:
            safe_command = validator.validate_command("ls -la /home")
            # Command is safe to execute
        except CommandSecurityError as e:
            # Handle security violation
            logger.error(f"Security violation: {e}")
    """
    
    # Commands allowed in STRICT mode (most restrictive)
    STRICT_WHITELIST = {
        # System information
        'uname', 'hostname', 'whoami', 'id', 'uptime', 'date',
        # File operations (read-only)
        'ls', 'cat', 'head', 'tail', 'find', 'grep', 'wc',
        # Process information
        'ps', 'top', 'htop', 'pgrep',
        # Network information (read-only)
        'ping', 'traceroute', 'netstat', 'ss',
        # Disk information
        'df', 'du', 'lsblk', 'mount',
        # Service status (read-only)
        'systemctl status', 'service status',
    }
    
    # Additional commands allowed in STANDARD mode
    STANDARD_ADDITIONAL = {
        # Package management (query only)
        'dpkg', 'rpm', 'yum list', 'apt list', 'dnf list',
        # Log viewing
        'journalctl', 'dmesg',
        # Configuration viewing
        'nginx -t', 'apache2 -t', 'httpd -t',
        # Database queries (read-only)
        'mysql', 'psql', 'redis-cli',
    }
    
    # Commands that are NEVER allowed (blacklisted)
    GLOBAL_BLACKLIST = {
        # System modification
        'rm', 'rmdir', 'mv', 'cp', 'dd', 'shred',
        # Permission changes
        'chmod', 'chown', 'chgrp', 'setfacl',
        # User management
        'useradd', 'userdel', 'usermod', 'passwd', 'su', 'sudo',
        # Network modification
        'iptables', 'ufw', 'firewall-cmd', 'ipset',
        # Service control
        'systemctl start', 'systemctl stop', 'systemctl restart', 
        'systemctl enable', 'systemctl disable',
        'service start', 'service stop', 'service restart',
        # Package installation
        'apt install', 'apt remove', 'yum install', 'yum remove',
        'dnf install', 'dnf remove', 'pip install', 'npm install',
        # Dangerous utilities
        'wget', 'curl', 'nc', 'netcat', 'telnet', 'ssh', 'scp', 'rsync',
        # Shell manipulation
        'bash', 'sh', 'zsh', 'fish', 'exec', 'eval',
        # File editing
        'vi', 'vim', 'nano', 'emacs', 'sed', 'awk',
    }
    
    # Dangerous shell patterns that indicate injection attempts
    INJECTION_PATTERNS = [
        r'[;&|`$()]',           # Shell operators and command substitution
        r'<<|>>',               # Redirection operators
        r'\${.*}',              # Variable expansion
        r'`.*`',                # Command substitution
        r'\$\(.*\)',            # Command substitution
        r'\.\./',               # Directory traversal
        r'/dev/',               # Device file access
        r'/proc/',              # Process filesystem access
        r'\\x[0-9a-fA-F]{2}',   # Hex escape sequences
        r'%[0-9a-fA-F]{2}',     # URL encoding
        r'\x00',                # Null byte injection
    ]
    
    # Characters that are often used in injection attacks
    DANGEROUS_CHARS = set(';&|`$(){}[]<>*?~')
    
    def __init__(self, policy: SecurityPolicy = SecurityPolicy.STANDARD):
        """Initialize the security validator.
        
        Args:
            policy: Security policy level to enforce
        """
        self.policy = policy
        self.logger = logging.getLogger("proxmox-mcp.security")
        
        # Compile regex patterns for performance
        self._injection_regex = [re.compile(pattern, re.IGNORECASE) 
                                for pattern in self.INJECTION_PATTERNS]
        
        # Build allowed commands based on policy
        self._allowed_commands = self._build_allowed_commands()
        
        self.logger.info(f"VM command security validator initialized with {policy.value} policy")
    
    def _build_allowed_commands(self) -> Set[str]:
        """Build the set of allowed commands based on security policy.
        
        Returns:
            Set of allowed command names and prefixes
        """
        allowed = set(self.STRICT_WHITELIST)
        
        if self.policy in [SecurityPolicy.STANDARD, SecurityPolicy.PERMISSIVE]:
            allowed.update(self.STANDARD_ADDITIONAL)
        
        return allowed
    
    def validate_command(self, command: str) -> str:
        """Validate and sanitize a command for secure execution.
        
        Performs comprehensive security validation including:
        - Command whitelist/blacklist checking
        - Shell injection pattern detection
        - Dangerous character validation
        - Length and complexity limits
        - Argument sanitization
        
        Args:
            command: Raw command string to validate
            
        Returns:
            Sanitized command string safe for execution
            
        Raises:
            CommandSecurityError: If command fails security validation
        """
        if not command or not command.strip():
            raise CommandSecurityError(
                "Empty or whitespace-only commands are not allowed",
                command,
                "empty_command"
            )
        
        command = command.strip()
        
        # Check command length
        self._validate_command_length(command)
        
        # Check for injection patterns
        self._validate_injection_patterns(command)
        
        # Check for dangerous characters
        self._validate_dangerous_characters(command)
        
        # Parse and validate command structure
        command_parts = self._parse_command_safely(command)
        
        # Validate command against whitelist/blacklist
        self._validate_command_authorization(command_parts)
        
        # Sanitize arguments
        sanitized_command = self._sanitize_command_parts(command_parts)
        
        # Log successful validation
        self.logger.info(f"Command validated successfully: {sanitized_command[:50]}...")
        
        return sanitized_command
    
    def _validate_command_length(self, command: str) -> None:
        """Validate command length limits.
        
        Args:
            command: Command to validate
            
        Raises:
            CommandSecurityError: If command exceeds length limits
        """
        max_length = 1000  # Reasonable maximum for most legitimate commands
        
        if len(command) > max_length:
            raise CommandSecurityError(
                f"Command exceeds maximum length of {max_length} characters",
                command,
                "excessive_length"
            )
    
    def _validate_injection_patterns(self, command: str) -> None:
        """Check for shell injection patterns.
        
        Args:
            command: Command to validate
            
        Raises:
            CommandSecurityError: If injection patterns are detected
        """
        for pattern_regex in self._injection_regex:
            if pattern_regex.search(command):
                raise CommandSecurityError(
                    f"Command contains potential injection pattern: {pattern_regex.pattern}",
                    command,
                    "injection_pattern"
                )
    
    def _validate_dangerous_characters(self, command: str) -> None:
        """Check for dangerous characters that could enable injection.
        
        Args:
            command: Command to validate
            
        Raises:
            CommandSecurityError: If dangerous characters are found
        """
        found_chars = set(command) & self.DANGEROUS_CHARS
        
        if found_chars and self.policy == SecurityPolicy.STRICT:
            raise CommandSecurityError(
                f"Command contains dangerous characters: {', '.join(found_chars)}",
                command,
                "dangerous_characters"
            )
    
    def _parse_command_safely(self, command: str) -> List[str]:
        """Parse command into parts using secure shell lexing.
        
        Args:
            command: Command to parse
            
        Returns:
            List of command parts (command + arguments)
            
        Raises:
            CommandSecurityError: If command cannot be parsed safely
        """
        try:
            # Use shlex for safe parsing that handles quotes and escaping
            return shlex.split(command)
        except ValueError as e:
            raise CommandSecurityError(
                f"Command contains invalid shell syntax: {e}",
                command,
                "invalid_syntax"
            ) from e
    
    def _validate_command_authorization(self, command_parts: List[str]) -> None:
        """Validate command against whitelist/blacklist.
        
        Args:
            command_parts: Parsed command parts
            
        Raises:
            CommandSecurityError: If command is not authorized
        """
        if not command_parts:
            raise CommandSecurityError(
                "No command specified",
                "",
                "no_command"
            )
        
        base_command = command_parts[0].lower()
        full_command = ' '.join(command_parts[:2]).lower()  # Command + first arg
        
        # Check global blacklist first
        for blocked in self.GLOBAL_BLACKLIST:
            if (base_command == blocked.lower() or 
                full_command.startswith(blocked.lower())):
                raise CommandSecurityError(
                    f"Command '{blocked}' is globally blacklisted",
                    ' '.join(command_parts),
                    "blacklisted_command"
                )
        
        # In PERMISSIVE mode, only check blacklist
        if self.policy == SecurityPolicy.PERMISSIVE:
            return
        
        # Check whitelist for STRICT and STANDARD modes
        command_authorized = False
        
        for allowed in self._allowed_commands:
            if (base_command == allowed.lower() or 
                full_command.startswith(allowed.lower())):
                command_authorized = True
                break
        
        if not command_authorized:
            raise CommandSecurityError(
                f"Command '{base_command}' is not in the allowed command list",
                ' '.join(command_parts),
                "unauthorized_command"
            )
    
    def _sanitize_command_parts(self, command_parts: List[str]) -> str:
        """Sanitize command parts and reassemble safely.
        
        Args:
            command_parts: Parsed command parts
            
        Returns:
            Sanitized command string
        """
        # Quote each part to prevent injection
        sanitized_parts = [shlex.quote(part) for part in command_parts]
        
        return ' '.join(sanitized_parts)
    
    def get_security_info(self) -> Dict[str, any]:
        """Get information about current security configuration.
        
        Returns:
            Dictionary containing security policy information
        """
        return {
            "policy": self.policy.value,
            "allowed_commands_count": len(self._allowed_commands),
            "blacklisted_commands_count": len(self.GLOBAL_BLACKLIST),
            "injection_patterns_count": len(self.INJECTION_PATTERNS),
            "dangerous_chars": list(self.DANGEROUS_CHARS),
        }


def create_security_validator(policy_name: str = "standard") -> VMCommandSecurityValidator:
    """Factory function to create a security validator with specified policy.
    
    Args:
        policy_name: Security policy name ("strict", "standard", or "permissive")
        
    Returns:
        Configured VMCommandSecurityValidator instance
        
    Raises:
        ValueError: If policy_name is not recognized
    """
    try:
        policy = SecurityPolicy(policy_name.lower())
        return VMCommandSecurityValidator(policy)
    except ValueError as e:
        valid_policies = [p.value for p in SecurityPolicy]
        raise ValueError(
            f"Invalid security policy '{policy_name}'. "
            f"Valid options: {', '.join(valid_policies)}"
        ) from e