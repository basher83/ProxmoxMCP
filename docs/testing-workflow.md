# Testing Workflow Documentation

This document describes the comprehensive testing capabilities available in ProxmoxMCP through the
enhanced Taskfile.yml configuration.

## Overview

ProxmoxMCP provides a sophisticated testing workflow that supports different testing scenarios,
intelligent dependency management, and developer-friendly output. The testing system is designed to
accommodate both rapid development cycles and comprehensive validation.

## Testing Tasks

### Primary Testing Commands

#### `task test`

**Description**: Run all tests with enhanced validation and informative output.

```bash
task test
```

**Features**:

- Comprehensive test suite execution (71 tests)
- Enhanced output with progress indicators
- Improved error reporting with `--tb=short`
- Clear completion summary

**Use Cases**:

- Pre-commit validation
- Full codebase testing
- CI/CD pipeline execution

#### `task test:unit`

**Description**: Run unit tests only with focused output.

```bash
task test:unit
```

**Features**:

- Explicit unit test execution
- Focused on `tests/` directory
- Short traceback format for faster debugging

**Use Cases**:

- Development workflow testing
- Quick validation during coding
- Focused debugging sessions

### Specialized Testing Commands

#### `task test:coverage`

**Description**: Run tests with coverage reporting (intelligent dependency handling).

```bash
task test:coverage
```

**Features**:

- Automatic pytest-cov detection
- Graceful fallback when coverage tools unavailable
- HTML and terminal coverage reports
- 80% coverage threshold enforcement
- Helpful installation guidance

**Dependencies**:

```bash
uv add pytest-cov --group dev
```

**Use Cases**:

- Code coverage analysis
- Quality assurance validation
- Identifying untested code paths

#### `task test:watch`

**Description**: Run tests in watch mode for continuous development.

```bash
task test:watch
```

**Features**:

- Automatic pytest-watch detection
- Graceful fallback to single test run
- Installation guidance for watch mode
- Continuous testing during development

**Dependencies**:

```bash
uv add pytest-watch --group dev
```

**Use Cases**:

- Test-driven development (TDD)
- Continuous validation during coding
- Rapid feedback loops

#### `task test:security`

**Description**: Run security-focused test subset.

```bash
task test:security
```

**Features**:

- Filters tests with security keywords (`encrypt`, `security`, `auth`)
- Focuses on authentication and encryption functionality
- Faster execution for security validation
- 42 security-related tests

**Use Cases**:

- Security-focused development
- Encryption feature validation
- Authentication flow testing

#### `task test:tools`

**Description**: Run MCP tools tests.

```bash
task test:tools
```

**Features**:

- Tests MCP server functionality
- Validates VM console operations
- Focuses on tool implementations
- Quick validation of MCP protocol compliance

**Use Cases**:

- MCP tool development
- API integration validation
- Tool functionality verification

#### `task test:config`

**Description**: Run configuration and encryption tests.

```bash
task test:config
```

**Features**:

- Tests configuration loading and validation
- Validates encryption/decryption functionality
- Focuses on config management
- Covers 42 configuration-related tests

**Use Cases**:

- Configuration system development
- Encryption feature development
- Config validation testing

#### `task test:integration`

**Description**: Placeholder for integration tests (future implementation).

```bash
task test:integration
```

**Features**:

- Guidance for integration test setup
- Proxmox connection requirements
- Future implementation roadmap
- Clear setup instructions

**Use Cases**:

- End-to-end testing (when implemented)
- Real Proxmox API validation
- Integration verification

## Testing Workflow Patterns

### Development Workflow

#### Rapid Development Cycle

```bash
# 1. Start watch mode for continuous testing
task test:watch

# 2. Make code changes
# 3. Tests run automatically

# 4. Run focused tests for specific areas
task test:security  # For security features
task test:tools     # For MCP tools
task test:config    # For configuration
```

#### Pre-Commit Workflow

```bash
# 1. Run comprehensive pre-commit checks
task pre-commit

# This includes:
# - Code formatting (black)
# - Linting with auto-fix (ruff)
# - Type checking (mypy)
# - Development YAML linting
# - All tests pass validation
```

#### Coverage Analysis Workflow

```bash
# 1. Install coverage dependencies
uv add pytest-cov --group dev

# 2. Run coverage analysis
task test:coverage

# 3. Review HTML coverage report
open htmlcov/index.html  # macOS/Linux
start htmlcov/index.html # Windows
```

### CI/CD Integration

#### Local CI Simulation

```bash
# Simulate full CI pipeline locally
task ci

# This runs:
# - All code quality checks (task check)
# - Complete test suite (task test)
# - Comprehensive validation
```

#### Component-Specific Testing

```bash
# Test specific components during development
task test:security   # Security features
task test:tools      # MCP tools
task test:config     # Configuration system
```

## Test Configuration

### Pytest Configuration

Located in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
asyncio_mode = "strict"
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = "-v"
```

### Test Discovery

- **Test Directory**: `tests/`
- **Test Files**: `test_*.py`
- **Test Functions**: `test_*`
- **Async Support**: Full async/await support enabled

### Current Test Coverage

#### Covered Components (71 tests)

- ✅ Configuration loading and validation
- ✅ Encryption and security functionality
- ✅ MCP server implementation
- ✅ VM console operations
- ✅ Authentication flows

#### Components Needing Coverage (Future)

- ❌ AI diagnostic tools (`tools/ai_diagnostics.py`)
- ❌ Formatting modules (`formatting/`)
- ❌ Core Proxmox functionality (`core/proxmox.py`)
- ❌ Additional tool modules (`tools/node.py`, `tools/storage.py`, etc.)

## Intelligent Dependency Management

### Automatic Dependency Detection

The testing system automatically detects optional dependencies and provides helpful fallbacks:

#### pytest-cov Detection

```bash
# Automatic detection and fallback
if uv run python -c "import pytest_cov" 2>/dev/null; then
  # Run with coverage
  uv run pytest --cov=src --cov-report=html
else
  # Fallback with installation hint
  echo "💡 Install with: uv add pytest-cov --group dev"
  uv run pytest -v
fi
```

#### pytest-watch Detection

```bash
# Automatic detection and fallback
if uv run python -c "import pytest_watch" 2>/dev/null; then
  # Run in watch mode
  uv run pytest-watch
else
  # Fallback with guidance
  echo "🔄 Running tests once instead..."
  uv run pytest -v
fi
```

### Installation Commands

When dependencies are missing, the system provides exact installation commands:

```bash
# Coverage tools
uv add pytest-cov --group dev

# Watch mode tools
uv add pytest-watch --group dev

# Future performance testing
uv add pytest-benchmark --group dev
```

## Integration with Development Tools

### VS Code Integration

The testing workflow integrates seamlessly with VS Code:

- Test discovery works automatically
- Debugging support for individual tests
- Coverage highlighting with coverage extensions

### Git Hooks Integration

Testing is integrated into git workflows:

- Pre-commit hooks run quality checks
- Push hooks can run full test suite
- CI/CD integration validates all changes

### Docker Integration

Testing works in Docker environments:

```bash
# Build and test in Docker
docker compose up --build
docker compose exec app task test
```

## Performance Considerations

### Test Execution Times

- **Full test suite**: ~6-8 seconds (71 tests)
- **Security subset**: ~2-3 seconds (42 tests)
- **Tools subset**: ~1-2 seconds (focused tests)
- **Config subset**: ~3-4 seconds (42 tests)

### Optimization Strategies

- Use focused test subsets during development
- Leverage watch mode for continuous testing
- Run full suite only for pre-commit/CI
- Use coverage analysis periodically, not continuously

## Troubleshooting

### Common Issues

#### Tests Not Found

```bash
# Ensure you're in the project root
cd /path/to/ProxmoxMCP
task test
```

#### Missing Dependencies

```bash
# Install all development dependencies
uv sync --extra dev

# Install specific testing dependencies
uv add pytest-cov pytest-watch --group dev
```

#### Coverage Tool Issues

```bash
# Manually install coverage tools
uv add pytest-cov --group dev

# Verify installation
uv run python -c "import pytest_cov; print('Coverage tools installed')"
```

#### Async Test Issues

```bash
# Ensure asyncio mode is configured in pyproject.toml
[tool.pytest.ini_options]
asyncio_mode = "strict"
```

### Environment Issues

#### PYTHONPATH Configuration

The Taskfile automatically configures PYTHONPATH:

```yaml
env:
  PYTHONPATH: "src:{{.PYTHONPATH}}"
```

#### Virtual Environment

Ensure you're using the correct environment:

```bash
# Activate UV environment
source .venv/bin/activate  # Linux/macOS
.\.venv\Scripts\Activate.ps1  # Windows

# Or use UV directly
uv run task test
```

## Future Enhancements

### Planned Improvements

- Integration test implementation
- Performance benchmarking
- Load testing capabilities
- Enhanced security testing
- API contract testing

### Roadmap Alignment

Testing improvements align with project roadmap:

- **Phase 1**: Core component coverage expansion
- **Phase 2**: Integration testing implementation
- **Phase 3**: Performance and load testing
- **Phase 4**: Advanced security testing

For detailed future improvements, see [GitHub Issue #75](https://github.com/basher83/ProxmoxMCP/issues/75).

## Best Practices

### Development Testing

1. Use `task test:watch` during active development
2. Run focused subsets (`test:security`, `test:tools`) for quick feedback
3. Use `task test:coverage` periodically to identify coverage gaps
4. Run `task pre-commit` before committing changes

### CI/CD Testing

1. Use `task ci` for comprehensive local validation
2. Ensure all dependencies are properly locked in `uv.lock`
3. Test in clean environments to catch dependency issues
4. Monitor test execution times and optimize as needed

### Team Collaboration

1. Share testing patterns and workflows with team members
2. Document any new test categories or patterns
3. Keep testing dependencies up to date
4. Contribute to test coverage improvements

This comprehensive testing workflow ensures high code quality, rapid development feedback, and
reliable validation of ProxmoxMCP functionality across all components.
