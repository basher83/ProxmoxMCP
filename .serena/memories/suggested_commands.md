# ProxmoxMCP Development Commands

## Environment Setup
```bash
# Create and activate virtual environment
uv venv
source .venv/bin/activate  # Linux/macOS
.\.venv\Scripts\Activate.ps1  # Windows

# Install dependencies with development tools
uv pip install -e ".[dev]"

# Frozen install (no dependency updates)
task setup:frozen
# Install with dependency updates
task setup:update
```

## Code Quality Commands
```bash
# Format code
black .
# OR with task
task format

# Check formatting without changes
task format:check

# Lint code  
ruff .
# OR with task
task lint

# Auto-fix linting issues
task lint:fix

# Type checking
mypy .
# OR with task
task type:check

# Run all quality checks
task check
```

## Testing Commands
```bash
# Run all tests
pytest
# OR with task
task test

# Run with verbose output
pytest -v --tb=short

# Run specific test categories
task test:security    # Security-focused tests
task test:tools       # MCP tools tests  
task test:config      # Configuration tests
task test:unit        # Unit tests only

# Coverage testing (if pytest-cov installed)
task test:coverage

# Watch mode testing (if pytest-watch installed)
task test:watch
```

## Development Server
```bash
# Set config and run server
export PROXMOX_MCP_CONFIG="proxmox-config/config.json"
python -m proxmox_mcp.server

# OR with task
task dev
```

## Docker Commands
```bash
# Build Docker image
docker compose build
# OR with task
task docker:build

# Run with Docker Compose
docker compose up --build

# Run container directly
task docker:run
```

## YAML Linting
```bash
# Lint all YAML files
task yaml:lint

# Lint development YAML only (excludes .github/.codacy)
task yaml:lint:dev

# Auto-fix YAML issues
task yaml:autofix

# Check YAML in strict mode
task yaml:check
```

## Combined Workflows
```bash
# Pre-commit workflow
task pre-commit

# Quick development check
task quick

# CI simulation
task ci

# Auto-fix all issues
task fix
```

## Dependency Management
```bash
# Update dependencies
task deps:update

# Sync without upgrades
task deps:sync

# Update lock file
task deps:lock
```

## Cleanup
```bash
# Clean generated files
task clean

# Deep clean including venv
task clean:all
```

## Utility Commands
```bash
# Show project info
task info

# List all available tasks
task --list-all

# Build package
task build
```