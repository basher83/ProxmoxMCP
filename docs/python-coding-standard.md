# ProxmoxMCP Python Coding Standard

**Version:** 1.0  
**Last Updated:** June 2025  
**Repository:** [ProxmoxMCP](https://github.com/basher83/ProxmoxMCP)

## Table of Contents

1. [Overview](#overview)
2. [Tool Configuration](#tool-configuration)
3. [Type Safety & Annotations](#type-safety--annotations)
4. [Code Style & Formatting](#code-style--formatting)
5. [Security Standards](#security-standards)
6. [Complexity & Design Limits](#complexity--design-limits)
7. [Function & Class Design](#function--class-design)
8. [Error Handling](#error-handling)
9. [Import Organization](#import-organization)
10. [Documentation Standards](#documentation-standards)
11. [Testing Standards](#testing-standards)
12. [Pre-commit Enforcement](#pre-commit-enforcement)
13. [Common Violations & Fixes](#common-violations--fixes)

## Overview

This document defines the Python coding standards for the ProxmoxMCP project. These standards are
enforced through automated tools integrated with our CI/CD pipeline and are based on our current
Codacy "Default coding standard" configuration.

### Enforcement Tools

Our coding standards are automatically enforced using:

- **Type Checking**: `mypy` (strict mode)
- **Code Formatting**: `black` (88 character line limit)
- **Linting**: `ruff` + `pylint`
- **Security Analysis**: `bandit` + `semgrep`
- **Complexity Analysis**: `lizard`
- **Multi-tool Analysis**: `prospector`

## Tool Configuration

### Current Status ✅

- **mypy**: All type annotation issues resolved (Issue #39 ✅)
- **black**: Code formatting standardized
- **ruff**: Configured but disabled in Codacy
- **bandit**: Active security scanning
- **semgrep**: Advanced security pattern detection
- **lizard**: Complexity monitoring
- **pylint**: 96 patterns enabled in Codacy

### Recommended Actions

1. Enable Ruff in Codacy to complement existing tools
2. Address current security violations flagged by Bandit/Semgrep
3. Refactor methods exceeding complexity thresholds

## Type Safety & Annotations

### Requirements ✅ COMPLETED

All functions must include type hints for parameters and return values:

```python
# ✅ Good
def get_vm_status(vm_id: str, node: str) -> Dict[str, Any]:
    """Get VM status from Proxmox node."""
    return {"status": "running", "uptime": 12345}

# ✅ Good - Complex types
from typing import List, Optional, Union

def process_vms(vm_list: List[Dict[str, Any]],
                timeout: Optional[int] = None) -> List[str]:
    """Process multiple VMs with optional timeout."""
    return [vm["name"] for vm in vm_list]

# ❌ Bad - No type hints
def get_vm_status(vm_id, node):
    return {"status": "running"}
```

### mypy Configuration

- Strict mode enabled
- No `Any` types without justification
- All imports must be typed or have type stubs

## Code Style & Formatting

### Automatic Formatting

- **Line Length**: 88 characters (Black standard)
- **String Quotes**: Prefer double quotes
- **Trailing Commas**: Required in multi-line structures

### Pylint Style Rules (Currently Enforced)

```python
# ✅ Good - No trailing whitespace
def function_name():
    return "value"

# ✅ Good - Use isinstance() for type checking
if isinstance(value, str):
    process_string(value)

# ✅ Good - Use enumerate() instead of range(len())
for index, item in enumerate(items):
    print(f"{index}: {item}")

# ❌ Bad - Trailing whitespace (flagged by C0303)
def function_name():  
    return "value"  

# ❌ Bad - type() comparison (flagged by C0123)
if type(value) == str:
    process_string(value)

# ❌ Bad - range(len()) pattern (flagged by C0200)
for i in range(len(items)):
    print(f"{i}: {items[i]}")
```

## Security Standards

### 🚨 Critical Security Issues (Currently in Codebase)

Based on Bandit and Semgrep findings, the following patterns must be avoided:

#### Subprocess Security

```python
# ❌ NEVER - subprocess with shell=True (HIGH RISK)
subprocess.run(f"git {command}", shell=True)
subprocess.call(user_input, shell=True)

# ✅ ALWAYS - Use shell=False with command lists
subprocess.run(["git", "status"], shell=False, check=True)
subprocess.run(["ssh", "-o", "BatchMode=yes", host], shell=False)
```

#### Credential Management

```python
# ❌ NEVER - Hardcoded credentials (even in tests)
API_KEY = "pk_test_12345"  # Flagged by Bandit
PASSWORD = "admin123"     # Security violation

# ✅ ALWAYS - Environment variables or secure config
API_KEY = os.getenv("PROXMOX_API_KEY")
if not API_KEY:
    raise ValueError("PROXMOX_API_KEY environment variable required")

# ✅ ALWAYS - Use secure random for tokens
import secrets
token = secrets.token_urlsafe(32)
```

#### Input Validation

```python
# ✅ Always validate and sanitize inputs
def validate_vm_id(vm_id: str) -> str:
    """Validate VM ID to prevent injection attacks."""
    if not re.match(r'^[a-zA-Z0-9_-]+$', vm_id):
        raise ValueError(f"Invalid VM ID format: {vm_id}")
    return vm_id
```

## Complexity & Design Limits

### Lizard Complexity Thresholds (Currently Enforced)

- **Maximum lines per method**: 50 lines
- **Maximum cyclomatic complexity**: 8
- **Maximum parameters per function**: 6

### Examples

```python
# ✅ Good - Under complexity limits
def create_vm(name: str, template: str, memory: int) -> Dict[str, Any]:
    """Create VM with specified parameters."""
    if not name or len(name) > 50:
        raise ValueError("Invalid VM name")

    config = {
        "name": name,
        "template": template,
        "memory": memory,
    }

    return proxmox_api.create_vm(config)

# ❌ Bad - Too many parameters, high complexity
def create_vm(name, template, memory, cpu, disk, network, backup,
              monitoring, tags, description, auto_start, protection):
    # 50+ lines of complex conditional logic...
    pass
```

### Refactoring Large Functions

```python
# ✅ Good - Break down complex functions
class VMManager:
    def create_vm(self, config: VMConfig) -> VM:
        """Create VM with validation and setup."""
        self._validate_config(config)
        vm = self._create_base_vm(config)
        self._configure_network(vm, config.network)
        self._setup_monitoring(vm, config.monitoring)
        return vm

    def _validate_config(self, config: VMConfig) -> None:
        """Validate VM configuration."""
        # Focused validation logic

    def _create_base_vm(self, config: VMConfig) -> VM:
        """Create base VM instance."""
        # Focused creation logic
```

## Function & Class Design

### Function Signatures

```python
# ✅ Good - Clear, typed, documented
def backup_vm(vm_id: str,
             backup_type: BackupType = BackupType.FULL,
             compression: bool = True) -> BackupResult:
    """Backup VM with specified options.

    Args:
        vm_id: Unique identifier for the VM
        backup_type: Type of backup to perform
        compression: Whether to compress backup data

    Returns:
        BackupResult containing backup metadata

    Raises:
        VMNotFoundError: If VM doesn't exist
        BackupError: If backup operation fails
    """
    vm = self._get_vm(vm_id)
    return self._perform_backup(vm, backup_type, compression)
```

### Class Design

```python
# ✅ Good - Single responsibility, clear interface
class ProxmoxConnection:
    """Manages connection to Proxmox VE API."""

    def __init__(self, host: str, username: str, password: str) -> None:
        self._host = host
        self._auth = (username, password)
        self._session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self) -> "ProxmoxConnection":
        """Enter async context manager."""
        self._session = aiohttp.ClientSession()
        await self._authenticate()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit async context manager."""
        if self._session:
            await self._session.close()
```

## Error Handling

### Exception Hierarchy

```python
# ✅ Good - Custom exception hierarchy
class ProxmoxError(Exception):
    """Base exception for Proxmox operations."""
    pass

class ProxmoxConnectionError(ProxmoxError):
    """Connection-related errors."""
    pass

class VMNotFoundError(ProxmoxError):
    """VM not found errors."""

    def __init__(self, vm_id: str) -> None:
        super().__init__(f"VM not found: {vm_id}")
        self.vm_id = vm_id
```

### Exception Handling Patterns

```python
# ✅ Good - Specific exceptions, proper logging
import logging

logger = logging.getLogger(__name__)

def get_vm_info(vm_id: str) -> Dict[str, Any]:
    """Get VM information with proper error handling."""
    try:
        response = proxmox_api.get_vm(vm_id)
        return response.json()
    except aiohttp.ClientError as e:
        logger.error(f"Network error getting VM {vm_id}: {e}")
        raise ProxmoxConnectionError(f"Failed to connect: {e}") from e
    except KeyError as e:
        logger.error(f"Invalid response format for VM {vm_id}: {e}")
        raise ProxmoxError(f"Invalid API response: {e}") from e

# ❌ Bad - Bare except, no logging
def get_vm_info(vm_id):
    try:
        return proxmox_api.get_vm(vm_id).json()
    except:
        return None
```

## Import Organization

### Standard Import Order

```python
# 1. Standard library imports (alphabetical)
import asyncio
import logging
import os
import re
from typing import Any, Dict, List, Optional

# 2. Third-party imports (alphabetical)
import aiohttp
import click
import pydantic

# 3. Local imports (alphabetical)
from .config import ProxmoxConfig
from .exceptions import ProxmoxError, VMNotFoundError
from .models import VM, BackupResult
from .utils import validate_vm_id
```

## Documentation Standards

### Docstring Format (Google Style)

```python
def migrate_vm(vm_id: str, target_node: str,
              live: bool = False) -> MigrationResult:
    """Migrate VM to another Proxmox node.

    This function performs a VM migration between Proxmox nodes,
    optionally using live migration to minimize downtime.

    Args:
        vm_id: Unique identifier of the VM to migrate
        target_node: Name of the destination Proxmox node
        live: Whether to perform live migration (default: False)

    Returns:
        MigrationResult object containing migration status and metadata

    Raises:
        VMNotFoundError: If the specified VM doesn't exist
        NodeNotFoundError: If the target node is unavailable
        MigrationError: If migration fails for any reason

    Example:
        >>> result = migrate_vm("vm-100", "pve-node2", live=True)
        >>> print(f"Migration {result.status}: {result.duration}s")
        Migration completed: 45.2s
    """
```

### Module Documentation

```python
"""Proxmox VM management module.

This module provides high-level interfaces for managing VMs in a Proxmox VE
cluster, including creation, deletion, migration, and monitoring operations.

Example:
    Basic VM operations:

    >>> async with ProxmoxConnection(host, user, password) as conn:
    ...     vm_manager = VMManager(conn)
    ...     vm = await vm_manager.create_vm("test-vm", "ubuntu-template")
    ...     status = await vm_manager.get_status(vm.id)

Attributes:
    DEFAULT_TIMEOUT (int): Default timeout for API operations
    MAX_RETRIES (int): Maximum retry attempts for failed operations
"""
```

## Testing Standards

### Test Structure

```python
# tests/test_vm_manager.py
import pytest
from unittest.mock import AsyncMock, Mock, patch

from proxmox_mcp.vm_manager import VMManager
from proxmox_mcp.exceptions import VMNotFoundError


class TestVMManager:
    """Test suite for VMManager class."""

    @pytest.fixture
    def vm_manager(self):
        """Create VMManager instance with mocked connection."""
        mock_connection = AsyncMock()
        return VMManager(mock_connection)

    @pytest.mark.asyncio
    async def test_create_vm_success(self, vm_manager):
        """Test successful VM creation."""
        # Arrange
        vm_config = {"name": "test-vm", "template": "ubuntu"}
        expected_vm_id = "vm-100"

        vm_manager._connection.post.return_value.json.return_value = {
            "data": {"vmid": expected_vm_id}
        }

        # Act
        result = await vm_manager.create_vm(vm_config)

        # Assert
        assert result.vm_id == expected_vm_id
        vm_manager._connection.post.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_vm_not_found(self, vm_manager):
        """Test VM not found error handling."""
        # Arrange
        vm_manager._connection.get.side_effect = aiohttp.ClientResponseError(
            request_info=Mock(), history=(), status=404
        )

        # Act & Assert
        with pytest.raises(VMNotFoundError, match="VM not found: vm-999"):
            await vm_manager.get_vm("vm-999")
```

### Test Coverage Requirements

- **Minimum Coverage**: 80% line coverage
- **Critical Paths**: 100% coverage for security-sensitive code
- **Error Handling**: All exception paths must be tested

## Pre-commit Enforcement

Our pre-commit configuration ensures code quality:

```yaml
# .pre-commit-config.yaml (current)
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.1.8
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]

  - repo: https://github.com/adrienverge/yamllint.git
    rev: v1.33.0
    hooks:
      - id: yamllint
```

## Common Violations & Fixes

### Current Issues in Codebase

Based on recent Codacy analysis, these issues need attention:

#### 1. Security Issues (HIGH PRIORITY)

```python
# ❌ Current violation - subprocess with shell=True
subprocess.run(f"git {command}", shell=True)

# ✅ Fix
subprocess.run(["git", command], shell=False, check=True)
```

#### 2. Complexity Issues

```python
# ❌ Current violation - method too long (>50 lines)
def process_vm_configuration(self, vm_config):
    # 70+ lines of complex logic
    pass

# ✅ Fix - break into smaller methods
def process_vm_configuration(self, vm_config: VMConfig) -> None:
    """Process VM configuration in manageable steps."""
    self._validate_configuration(vm_config)
    self._apply_base_settings(vm_config)
    self._configure_networking(vm_config)
    self._setup_monitoring(vm_config)
```

#### 3. Style Issues

```python
# ❌ Current violation - trailing whitespace
def function():  
    return "value"  

# ✅ Fix - no trailing whitespace
def function():
    return "value"
```

### Automated Fixes

Many issues can be automatically fixed:

```bash
# Format code
black .

# Fix lint issues
ruff --fix .

# Check types
mypy .

# Run all pre-commit checks
pre-commit run --all-files
```

## Adoption Guidelines

### For New Code

- All new code must pass pre-commit checks
- All functions require type hints and docstrings
- Security patterns must be followed from day one

### For Existing Code

1. **Phase 1**: Fix all security violations (HIGH PRIORITY)
2. **Phase 2**: Reduce complexity violations
3. **Phase 3**: Address style and documentation gaps

### Code Review Checklist

- [ ] All pre-commit checks pass
- [ ] Type hints present and accurate
- [ ] Security patterns followed
- [ ] Complexity under thresholds
- [ ] Documentation complete
- [ ] Tests provide adequate coverage
- [ ] No hardcoded credentials or security issues

---

**Questions or suggestions?** Please open an issue or submit a PR to improve this standard.

**Last Review**: This document should be reviewed quarterly and updated as tools and practices evolve.
