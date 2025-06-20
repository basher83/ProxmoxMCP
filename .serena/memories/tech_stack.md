# ProxmoxMCP Technology Stack

## Core Technologies
- **Python 3.10+**: Primary programming language, with support for 3.11 and 3.12
- **MCP SDK**: Model Context Protocol SDK from GitHub (python-sdk)
- **Proxmoxer**: Python wrapper for Proxmox VE API (>=2.0.1,<3.0.0)
- **Pydantic**: Data validation and settings management (>=2.0.0,<3.0.0)
- **Requests**: HTTP library for API communications (>=2.32.0,<3.0.0)
- **Cryptography**: Encryption support for secure configuration (>=45.0.0,<46.0.0)

## Development Tools
- **UV**: Modern Python package manager (recommended for dependency management)
- **Pytest**: Testing framework with async support (>=7.0.0,<9.0.0)
- **Black**: Code formatting (>=23.0.0,<26.0.0)
- **Mypy**: Static type checking (>=1.0.0,<2.0.0)
- **Ruff**: Fast Python linter (>=0.1.0,<0.12.0)
- **Yamllint**: YAML file linting (>=1.32.0,<2.0.0)

## Infrastructure
- **Docker**: Containerization with multi-stage builds
- **Docker Compose**: Container orchestration
- **Taskfile**: Task automation and workflow management
- **Git**: Version control with project-specific configuration

## Key Libraries and Frameworks
- **FastMCP**: Built on MCP SDK for tool registration and request handling
- **Asyncio**: Asynchronous programming for VM operations
- **Logging**: Python's built-in logging with customizable formatters
- **JSON**: Configuration file handling
- **Environment Variables**: Runtime configuration support

## Build and Package Management
- **setuptools**: Package building (>=61.0.0)
- **wheel**: Wheel format support
- **uv.lock**: Dependency lock file for reproducible builds
- **pyproject.toml**: Modern Python project configuration