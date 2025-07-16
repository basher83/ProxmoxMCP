# Developer Guide

This guide provides detailed information for developers working on ProxmoxMCP.

## Development Setup

### Prerequisites

- Python 3.10 or higher
- UV package manager (`pip install uv`)
- Git
- Docker (optional, for containerized development)
- Access to a Proxmox test environment

### Setting Up Your Development Environment

1. **Clone the repository**:

   ```bash
   git clone https://github.com/basher83/ProxmoxMCP.git
   cd ProxmoxMCP
   ```

2. **Configure Git** (for contributors):

   ```bash
   cp example.gitconfig .git/config
   git config user.name "Your Name"
   git config user.email "your.email@example.com"
   ```

3. **Create virtual environment**:

   ```bash
   uv venv
   source .venv/bin/activate  # Linux/macOS
   # OR
   .\.venv\Scripts\Activate.ps1  # Windows
   ```

4. **Install development dependencies**:

   ```bash
   uv pip install -e ".[dev]"
   ```

## Code Quality

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=proxmox_mcp

# Run specific test file
pytest tests/test_server.py

# Run tests in watch mode (requires pytest-watch)
ptw
```

### Code Formatting and Linting

```bash
# Format code
ruff format .

# Check linting
ruff check .

# Type checking
mypy .
```

### Using Taskfile (Recommended)

We provide a Taskfile for common development tasks:

```bash
# Install task runner
brew install go-task/tap/go-task  # macOS
# Or see https://taskfile.dev/installation/

# Run all quality checks
task pre-commit

# Run tests with coverage
task test:coverage

# Run security tests
task test:security

# Watch mode for continuous testing
task test:watch
```

## Project Structure

```
src/proxmox_mcp/
├── server.py          # Main MCP server entry point
├── config/            # Configuration models and loading
│   ├── loader.py      # Config file loading logic
│   └── models.py      # Pydantic models for config
├── core/              # Core functionality
│   ├── logging.py     # Logging setup
│   └── proxmox.py     # Proxmox API connection manager
├── formatting/        # Rich output formatting
│   ├── theme.py       # Color themes and styles
│   └── formatters.py  # Output formatting functions
├── tools/             # MCP tool implementations
│   ├── base.py        # Base tool class
│   ├── node.py        # Node management tools
│   ├── vm.py          # VM operation tools
│   ├── storage.py     # Storage tools
│   ├── cluster.py     # Cluster status tools
│   └── ai_diagnostics.py # AI-powered diagnostics
└── utils/             # Utilities
    ├── auth.py        # Authentication helpers
    └── encryption.py  # Config encryption support
```

## Testing Guidelines

### Test Organization

- Unit tests: `tests/test_*.py`
- Integration tests: `tests/integration/`
- Fixtures: `tests/conftest.py`

### Writing Tests

```python
# Example test structure
import pytest
from proxmox_mcp.tools.node import NodeTools

class TestNodeTools:
    @pytest.fixture
    def node_tools(self, mock_proxmox):
        return NodeTools(mock_proxmox)
    
    def test_get_nodes(self, node_tools):
        result = node_tools.get_nodes()
        assert len(result) > 0
        assert result[0].type == "text"
```

### Coverage Requirements

- Aim for >90% test coverage
- All new features must include tests
- Bug fixes should include regression tests

## Contributing Workflow

1. **Create a feature branch**:

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following our coding standards

3. **Run quality checks**:

   ```bash
   task pre-commit
   # Or manually:
   pytest && ruff format . && mypy . && ruff check .
   ```

4. **Commit with descriptive message**:

   ```bash
   git commit -m "feat: add new feature description"
   ```

5. **Push and create PR**:

   ```bash
   git push origin feature/your-feature-name
   ```

## Debugging

### Running the Server in Debug Mode

```bash
# Set debug logging
export PROXMOX_MCP_LOG_LEVEL=DEBUG
export PROXMOX_MCP_CONFIG="proxmox-config/config.json"
python -m proxmox_mcp.server
```

### Using VS Code

1. Create `.vscode/launch.json`:

   ```json
   {
     "version": "0.2.0",
     "configurations": [
       {
         "name": "Debug MCP Server",
         "type": "python",
         "request": "launch",
         "module": "proxmox_mcp.server",
         "env": {
           "PROXMOX_MCP_CONFIG": "${workspaceFolder}/proxmox-config/config.json",
           "PROXMOX_MCP_LOG_LEVEL": "DEBUG"
         }
       }
     ]
   }
   ```

## Release Process

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md
3. Create a git tag: `git tag v0.1.0`
4. Push tag: `git push origin v0.1.0`
5. GitHub Actions will build and publish

## Additional Resources

- [MCP SDK Documentation](https://github.com/modelcontextprotocol/sdk)
- [Proxmoxer Documentation](https://proxmoxer.github.io/docs/)
- [Pydantic Documentation](https://docs.pydantic.dev/)