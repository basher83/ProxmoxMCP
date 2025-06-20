# ProxmoxMCP Code Style and Conventions

## Code Formatting

- **Black**: Automatic code formatting with line length of 100 characters
- **Ruff**: Linting with rules E (pycodestyle errors), F (pyflakes), B (bugbear), I (import sorting)
- **Import Organization**:
  - Force sort within sections
  - Known first-party: `proxmox_mcp`
  - Known third-party: `mcp`, `proxmoxer`, `pydantic`, `cryptography`, `requests`
  - Section order: future, standard-library, third-party, first-party, local-folder

## Type Annotations

- **Mypy Configuration**: Strict type checking enabled
  - `disallow_untyped_defs = true`
  - `disallow_incomplete_defs = true`
  - `disallow_untyped_decorators = true`
  - `no_implicit_optional = true`
- **Type Hints Required**: All functions and methods must have type annotations
- **Python Version Target**: 3.10 for mypy checking

## Documentation Standards

- **Docstrings**: Required for all public functions and classes
- **Module Docstrings**: Comprehensive module-level documentation explaining purpose and key features
- **Class Documentation**: Detailed class docstrings explaining responsibility and usage patterns
- **Method Documentation**: Args, Returns, Raises documentation where applicable

## Naming Conventions

- **Classes**: PascalCase (e.g., `ProxmoxManager`, `ProxmoxTool`)
- **Functions/Methods**: snake_case (e.g., `load_config`, `execute_command`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `DEFAULT_PORT`, `CONFIG_FILE_NAME`)
- **Private Methods**: Leading underscore (e.g., `_setup_api`, `_create_config`)

## File and Directory Structure

- **Module Organization**: Clear separation by functionality
  - `core/`: Core Proxmox API integration
  - `config/`: Configuration management and models
  - `tools/`: MCP tool implementations
  - `formatting/`: Output formatting and themes
  - `utils/`: Utility functions and helpers
- **File Naming**: snake_case for Python files
- **Test Organization**: Mirror source structure in `tests/` directory

## Architecture Patterns

- **Pydantic Models**: All configuration and data validation uses Pydantic
- **Error Handling**: Comprehensive exception handling with specific error types
- **Logging**: Structured logging with configurable levels and formatters
- **Async Support**: Proper async/await patterns for I/O operations
- **Dependency Injection**: Clean dependency management in constructors
