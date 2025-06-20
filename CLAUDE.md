# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Additional Instructions

- memory workflow @/workspaces/ProxmoxMCP/docs/ai-instructions/memory-instructions.md
- context workflow @/workspaces/ProxmoxMCP/docs/ai-instructions/context-instructions.md
- github workflow @/workspaces/ProxmoxMCP/docs/ai-instructions/github-instructions.md
- issue creation workflow @/workspaces/ProxmoxMCP/docs/ai-instructions/issue-creation-instructions.md
- issue resolution workflow @/workspaces/ProxmoxMCP/docs/ai-instructions/issue-resolution-instructions.md
- pr workflow @/workspaces/ProxmoxMCP/docs/ai-instructions/pr-instructions.md
- milestone workflow @/workspaces/ProxmoxMCP/docs/ai-instructions/milestone-instructions.md

## Development Commands

### Environment Setup

```bash
# Set up git configuration (recommended for development)
cp example.gitconfig .git/config
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Create and activate virtual environment
uv venv
source .venv/bin/activate  # Linux/macOS
.\.venv\Scripts\Activate.ps1  # Windows

# Install dependencies with development tools
uv pip install -e ".[dev]"
```

### Testing and Quality Assurance

#### Standardized Quality Assurance Workflow

The ProxmoxMCP project uses a comprehensive, standardized quality assurance workflow that must be
followed for all code changes. This workflow includes automated checks, error recovery procedures, and
ProxmoxMCP-specific validations.

#### Pre-Commit Quality Pipeline

**Phase 1: Core Quality Checks (Parallel Execution)**

```bash
# Run core quality checks in parallel for efficiency
pytest & black . & mypy . & ruff . && wait

# If any check fails, stop and address issues before proceeding
echo "Core quality checks completed"
```

**Phase 2: ProxmoxMCP-Specific Validation**

```bash
# Configuration validation
export PROXMOX_MCP_CONFIG="proxmox-config/config.json"
python -c "from proxmox_mcp.config.loader import load_config; load_config()" || {
    echo "❌ Configuration validation failed"
    exit 1
}

# MCP server startup validation
python -m proxmox_mcp.server --validate-only || {
    echo "❌ MCP server validation failed"
    exit 1
}

# Dependency consistency check
uv pip check || {
    echo "❌ Dependency validation failed"
    exit 1
}
```

**Phase 3: Security and Integration Validation**

```bash
# Run security validation checklist
./scripts/security-check.sh || {
    echo "❌ Security validation failed"
    exit 1
}

# Docker build validation (if Docker changes made)
if git diff --name-only HEAD~1 | grep -E "(Dockerfile|compose\.yaml|\.dockerignore)"; then
    docker compose build || {
        echo "❌ Docker build validation failed"
        exit 1
    }
fi
```

#### Error Recovery Procedures

When quality checks fail, follow these specific recovery procedures:

#### pytest Failures

```bash
# Step 1: Get detailed failure information
pytest -v --tb=short

# Step 2: Run specific failed tests for faster iteration
pytest path/to/failed_test.py::test_function_name -v

# Step 3: Common pytest failure patterns and solutions
# - Import errors: Check PYTHONPATH and virtual environment activation
# - Configuration errors: Verify test configuration files exist
# - Dependency errors: Run `uv pip install -e ".[dev]"` to reinstall dependencies
# - Proxmox API errors: Ensure mock fixtures are properly configured

# Step 4: If tests pass individually but fail in suite
pytest --lf  # Run only last failed tests
pytest --maxfail=1  # Stop on first failure for easier debugging
```

#### black Formatting Failures

```bash
# Step 1: Auto-format code (this usually resolves all issues)
black .

# Step 2: Verify formatting was applied
git diff --name-only

# Step 3: Review changes and commit formatting fixes
git add .
git commit -m "format: apply black code formatting

Automated formatting applied by black code formatter.

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"

# Note: black failures are rare and usually indicate file permissions or encoding issues
```

#### mypy Type Checking Failures

```bash
# Step 1: Get detailed type error information
mypy . --show-error-codes --show-error-context

# Step 2: Common mypy error patterns and solutions

# Missing type annotations
# Error: Function is missing a return type annotation
# Solution: Add return type hints
def function_name() -> ReturnType:

# Import type errors
# Error: Cannot find implementation or library stub
# Solution: Add type ignore comment or install type stubs
import proxmoxer  # type: ignore[import]
# OR
pip install types-requests types-urllib3

# Configuration type errors
# Error: Incompatible types in assignment
# Solution: Update Pydantic models or add proper type annotations

# Step 3: Gradual typing approach for large errors
mypy --ignore-missing-imports .  # Temporary workaround
# Then gradually fix import issues one by one
```

#### ruff Linting Failures

```bash
# Step 1: Get detailed linting information
ruff check . --show-fixes

# Step 2: Auto-fix issues where possible
ruff check . --fix

# Step 3: Review remaining issues
ruff check . --diff  # Show what would be changed

# Step 4: Common ruff error patterns and solutions

# Unused imports (F401)
# Solution: Remove unused imports or add noqa comment if needed
import unused_module  # noqa: F401  # Used by dynamic import

# Line too long (E501)
# Solution: Break long lines or use parentheses
very_long_string = (
    "This is a very long string that needs to be "
    "broken across multiple lines for readability"
)

# Missing docstrings (D100)
# Solution: Add docstrings to public functions and classes
def public_function() -> None:
    """Brief description of what this function does."""
    pass

# Step 5: Configuration-specific ignores
# Add to pyproject.toml if needed, but prefer fixing the code
```

#### Configuration Validation Failures

```bash
# Step 1: Check configuration file syntax
python -c "import json; json.load(open('proxmox-config/config.json'))" || {
    echo "Invalid JSON in config file"
    exit 1
}

# Step 2: Validate required environment variables
python -c "
import os
required_vars = ['PROXMOX_MCP_CONFIG']
missing = [var for var in required_vars if not os.getenv(var)]
if missing:
    print(f'Missing environment variables: {missing}')
    exit(1)
print('Environment variables validated')
"

# Step 3: Test configuration loading
python -c "
from proxmox_mcp.config.loader import load_config
try:
    config = load_config()
    print('✅ Configuration loaded successfully')
    print(f'Host: {config.host}')
    print(f'User: {config.user}')
except Exception as e:
    print(f'❌ Configuration error: {e}')
    exit(1)
"

# Step 4: Common configuration issues and solutions
# - Missing config file: Copy from example and customize
# - Invalid credentials: Check Proxmox API token validity
# - Network issues: Verify Proxmox host accessibility
# - SSL issues: Check certificate configuration
```

#### MCP Server Validation Failures

```bash
# Step 1: Check MCP tool registration
python -c "
from proxmox_mcp.tools.definitions import get_tool_definitions
tools = get_tool_definitions()
print(f'Registered tools: {len(tools)}')
for tool in tools:
    print(f'  - {tool.name}')
"

# Step 2: Validate tool implementations
python -c "
from proxmox_mcp.server import create_server
try:
    server = create_server()
    print('✅ MCP server created successfully')
except Exception as e:
    print(f'❌ MCP server error: {e}')
    exit(1)
"

# Step 3: Test individual tool functionality
python -c "
from proxmox_mcp.tools.node import get_nodes
# Test with mock or development configuration
print('Tool validation would run here')
"
```

#### Dependency Validation Failures

```bash
# Step 1: Check for dependency conflicts
uv pip check

# Step 2: Rebuild environment if conflicts found
rm -rf .venv
uv venv
source .venv/bin/activate  # Linux/macOS
uv pip install -e ".[dev]"

# Step 3: Verify specific dependency issues
pip show problematic-package
pip index versions problematic-package

# Step 4: Update constraints if needed (following version verification process)
# See "Dependency Management and Version Verification" section above
```

#### Docker Build Validation Failures

```bash
# Step 1: Clean Docker environment
docker system prune -f
docker compose down --volumes

# Step 2: Build with verbose output
docker compose build --no-cache --progress=plain

# Step 3: Test container functionality
docker compose up -d
docker compose logs

# Step 4: Validate container security
docker compose exec proxmox-mcp id  # Should not be root
docker compose exec proxmox-mcp ls -la /app  # Check file permissions
```

#### Complete Quality Assurance Command

For development workflow efficiency, use this comprehensive command that includes error recovery:

```bash
#!/bin/bash
# comprehensive-qa.sh - Complete quality assurance with error recovery

set -e  # Exit on any error

echo "🚀 Starting ProxmoxMCP Quality Assurance Pipeline"

# Phase 1: Core Quality Checks
echo "📋 Phase 1: Core Quality Checks"
echo "Running pytest..."
pytest || { echo "❌ Tests failed - run 'pytest -v' for details"; exit 1; }

echo "Running black formatter..."
black . || { echo "❌ Formatting failed"; exit 1; }

echo "Running mypy type checker..."
mypy . || { echo "❌ Type checking failed - run 'mypy . --show-error-codes' for details"; exit 1; }

echo "Running ruff linter..."
ruff check . || { echo "❌ Linting failed - run 'ruff check . --show-fixes' for details"; exit 1; }

# Phase 2: ProxmoxMCP Validation
echo "📋 Phase 2: ProxmoxMCP-Specific Validation"
export PROXMOX_MCP_CONFIG="proxmox-config/config.json"

echo "Validating configuration..."
python -c "from proxmox_mcp.config.loader import load_config; load_config()" || {
    echo "❌ Configuration validation failed"
    exit 1
}

echo "Validating MCP server..."
python -m proxmox_mcp.server --validate-only || {
    echo "❌ MCP server validation failed"
    exit 1
}

echo "Checking dependencies..."
uv pip check || {
    echo "❌ Dependency validation failed"
    exit 1
}

# Phase 3: Security Validation
echo "📋 Phase 3: Security Validation"
echo "Running security checks..."
# Security validation would be implemented here

echo "✅ All quality assurance checks passed!"
echo "🎉 Code is ready for commit"
```

### Dependency Management and Version Verification

Before modifying dependencies in `pyproject.toml`, `requirements.in`, or `requirements-dev.in`,
ALWAYS verify actual package versions to prevent uninstallable packages:

#### Version Research Commands

```bash
# Research PyPI package versions
pip index versions <package-name>
pip show <package-name>  # For currently installed packages

# Alternative research methods
uv pip show <package-name>  # If using uv
python -m pip install <package-name>==nonexistent 2>&1 | grep "from versions"

# Check package compatibility with Python versions
python -c "import sys; print(sys.version_info)"
pip install --dry-run <package-name>==<version>
```

#### GitHub Release Verification

```bash
# For packages sourced from GitHub (like MCP SDK)
gh release list --repo modelcontextprotocol/python-sdk
gh release view <tag> --repo modelcontextprotocol/python-sdk

# Check specific commit or branch availability
gh api repos/modelcontextprotocol/python-sdk/commits/<commit-hash>
gh api repos/modelcontextprotocol/python-sdk/branches/<branch-name>
```

#### Version Constraint Best Practices

Use these patterns when setting dependency versions:

```bash
# Recommended constraint patterns for ProxmoxMCP:

# Core runtime dependencies - conservative ranges
"pydantic>=2.0.0,<3.0.0"      # Major version boundary
"requests>=2.32.0,<3.0.0"      # Security-conscious minimum

# Development tools - broader ranges for flexibility
"pytest>=7.0.0,<9.0.0"        # Allow multiple major versions
"black>=23.0.0,<26.0.0"       # Formatting tool compatibility

# Security-critical packages - narrower ranges  
"cryptography>=45.0.0,<46.0.0" # Strict for security updates

# Git dependencies - use specific tags/commits
"mcp @ git+https://github.com/modelcontextprotocol/python-sdk.git@v1.0.0"
```

#### Dependency Validation Workflow

Before committing dependency changes:

```bash
# 1. Research actual versions available
pip index versions pydantic
pip index versions cryptography
pip index versions pytest

# 2. Test installation in clean environment
uv venv test-deps
source test-deps/bin/activate
uv pip install -e ".[dev]"  # Test all dependencies resolve

# 3. Validate constraint logic
python -c "
import pkg_resources
try:
    pkg_resources.require(['pydantic>=2.0.0,<3.0.0'])
    print('✓ Pydantic constraint valid')
except:
    print('✗ Pydantic constraint invalid')
"

# 4. Check for known vulnerabilities
pip audit  # If available
safety check  # Alternative security scanner

# 5. Clean up test environment
deactivate
rm -rf test-deps
```

#### Dependency Update Process

When updating dependencies:

```bash
# 1. Check current versions
uv pip list --outdated

# 2. Research latest versions and compatibility
pip index versions <package-name>

# 3. Update constraints based on research
# Edit pyproject.toml, requirements.in, or requirements-dev.in

# 4. Regenerate lock files if using uv
uv pip compile requirements.in -o requirements.txt
uv pip compile requirements-dev.in -o requirements-dev.txt

# 5. Test installation and functionality
uv venv fresh-test
source fresh-test/bin/activate
uv pip install -e ".[dev]"
pytest  # Verify functionality
deactivate && rm -rf fresh-test

# 6. Document breaking changes in commit message
git add .
git commit -m "deps: update pydantic to 2.x.x

- Verify compatibility with Python 3.10+
- Test all MCP tool functionality
- Update type annotations as needed

Closes #issue-number"
```

#### Common Version Constraint Mistakes to Avoid

```bash
# ❌ WRONG: Unverified constraints that may not exist
"pydantic>=99.0.0,<100.0.0"  # Version 99.x.x doesn't exist

# ❌ WRONG: Overly restrictive constraints
"requests==2.32.0"  # Pins to exact version, prevents security updates

# ❌ WRONG: Conflicting constraints
"black>=24.0.0,<25.0.0"  # When 24.x.x was never released

# ❌ WRONG: Missing upper bounds for major versions
"pydantic>=2.0.0"  # Could install v3.x.x with breaking changes

# ✅ CORRECT: Research-verified constraints
"pydantic>=2.0.0,<3.0.0"    # Verified that 2.x.x exists
"requests>=2.32.0,<3.0.0"   # Allows security updates within v2.x
"black>=23.0.0,<26.0.0"     # Verified version range exists
```

#### ProxmoxMCP-Specific Dependency Considerations

```bash
# MCP SDK - use specific tagged releases
# Research: gh release list --repo modelcontextprotocol/python-sdk
"mcp @ git+https://github.com/modelcontextprotocol/python-sdk.git@v1.0.0"

# Proxmoxer - check compatibility with Proxmox VE API versions
# Research API changes between versions
"proxmoxer>=2.0.1,<3.0.0"

# Cryptography - security-critical, use narrow ranges
# Research: pip index versions cryptography
"cryptography>=45.0.0,<46.0.0"

# FastMCP or MCP dependencies - verify protocol compatibility
# Check MCP protocol version requirements
```

### Running the Server

```bash
# Set config path and run server
export PROXMOX_MCP_CONFIG="proxmox-config/config.json"
python -m proxmox_mcp.server

# Or with Docker
docker compose up --build
```

### Configuration Setup

```bash
# Create config directory and copy template
mkdir -p proxmox-config
cp proxmox-config/config.example.json proxmox-config/config.json
# Edit config.json with your Proxmox credentials
```

## Architecture Overview

### Core Components

- **server.py**: Main MCP server implementation using FastMCP, handles tool registration and request routing
- **core/proxmox.py**: ProxmoxManager class that manages API connections and authentication
- **config/**: Configuration loading and validation using Pydantic models
- **tools/**: Individual tool implementations (node, VM, storage, cluster operations)
- **formatting/**: Rich output formatting with themes, colors, and structured display

### Key Design Patterns

- **Tool-based Architecture**: Each Proxmox operation is implemented as a separate MCP tool
- **Pydantic Validation**: All configuration and API parameters use Pydantic models for type safety
- **Centralized Formatting**: All output uses consistent formatting through the formatting module
- **Async Support**: VM command execution supports async operations via QEMU guest agent

### Tool Categories

1. **Node Tools**: `get_nodes`, `get_node_status` - Cluster node management
2. **VM Tools**: `get_vms`, `execute_vm_command` - Virtual machine operations
3. **Storage Tools**: `get_storage` - Storage pool information
4. **Cluster Tools**: `get_cluster_status` - Overall cluster health

### Configuration Requirements

- Requires `PROXMOX_MCP_CONFIG` environment variable pointing to config JSON file
- Config must include Proxmox connection details (host, port, SSL settings) and authentication (user, token_name, token_value)
- Supports both file-based and environment variable configuration

### Authentication

- Uses Proxmox API tokens (not passwords) for secure authentication
- Tokens must have appropriate permissions for the operations being performed
- Connection is tested during server startup

### Output Formatting

- Rich formatted output with emojis, colors, and structured layout
- Consistent formatting across all tools using theme system
- Human-readable resource usage (bytes, percentages, uptime)

## Important Implementation Notes

### VM Command Execution

- Requires QEMU Guest Agent to be installed and running in target VMs
- Commands execute asynchronously and return both stdout and stderr
- Returns proper exit codes and handles command failures gracefully

### Error Handling

- Connection failures during startup cause server to exit with detailed error messages
- API operation failures are caught and returned as formatted error responses
- SSL verification can be disabled for self-signed certificates via config

### Testing

- Uses pytest with async support for testing MCP operations
- Test configuration should use mock Proxmox API to avoid requiring live server
- Tests are located in `tests/` directory

### Dependencies

- Built on Model Context Protocol (MCP) SDK for tool interface
- Uses `proxmoxer` library for Proxmox API communication
- Requires Python 3.10+ with modern async/await support

#### Dependency Version Management

All dependency versions MUST be verified before setting constraints:

1. **Research actual versions** using `pip index versions <package>` or GitHub releases
2. **Test constraints** in clean environments before committing
3. **Use appropriate constraint patterns** based on package type and stability
4. **Validate installation** using `uv pip check` and functionality tests
5. **Document breaking changes** when updating major versions

See the "Dependency Management and Version Verification" section above for detailed procedures.

## Security Validation and Best Practices

### Comprehensive Security Checklist

Before committing any code changes, validate security implementations using this checklist:

#### Credential Management Validation

- [ ] **No credentials in code**: Verify no hardcoded passwords, tokens, or API keys in source code
- [ ] **No credentials in logs**: Ensure credentials are not logged in error messages or debug output
- [ ] **Environment variables used**: All sensitive configuration uses environment variables
- [ ] **Credential encryption**: API tokens and sensitive data encrypted at rest when stored
- [ ] **No credentials in error outputs**: Error messages don't expose credential information

#### ProxmoxMCP-Specific Security Validation

- [ ] **Proxmox API authentication**: Token-based authentication properly implemented
- [ ] **API token rotation**: Token rotation procedures documented and tested
- [ ] **SSL/TLS validation**: Certificate validation properly configured for Proxmox connections
- [ ] **Connection timeouts**: Appropriate timeouts set for API connections
- [ ] **Rate limiting**: API rate limiting and quota management implemented

#### Input Validation and Sanitization

- [ ] **VM command sanitization**: All VM commands sanitized against injection attacks
- [ ] **File path validation**: File paths validated against directory traversal attacks
- [ ] **API parameter validation**: All API parameters validated using Pydantic models
- [ ] **Configuration validation**: Configuration inputs validated with schema enforcement
- [ ] **Command execution security**: VM command execution uses safe parameter passing

#### Network and Communication Security

- [ ] **TLS configuration**: All external communications use TLS/SSL
- [ ] **Certificate verification**: SSL certificates properly verified (not disabled)
- [ ] **Secure headers**: Appropriate security headers implemented where applicable
- [ ] **Connection pooling security**: Connection pooling doesn't leak credentials
- [ ] **API endpoint security**: All API endpoints require proper authentication

#### Container and Deployment Security

- [ ] **Non-root containers**: Docker containers run as non-root user
- [ ] **File permissions**: Proper file permissions set for configuration and data files
- [ ] **Environment variable security**: Sensitive environment variables properly scoped
- [ ] **Health check security**: Health check endpoints don't expose sensitive information
- [ ] **Image security**: Base images are from trusted sources and regularly updated

#### Audit and Monitoring

- [ ] **Security event logging**: Security-relevant events properly logged
- [ ] **No sensitive data in logs**: Logs don't contain passwords, tokens, or personal data
- [ ] **Audit trail**: Changes to security-critical configuration create audit trails
- [ ] **Monitoring integration**: Security events integrated with monitoring systems
- [ ] **Incident response**: Clear procedures for security incident response

### Security Implementation Patterns

#### Secure Configuration Loading

```python
# Correct: Use environment variables with validation
from pydantic import BaseModel, Field
import os

class SecureConfig(BaseModel):
    proxmox_host: str = Field(..., env="PROXMOX_HOST")
    api_token: str = Field(..., env="PROXMOX_API_TOKEN")
    
    class Config:
        # Never log sensitive fields
        json_encoders = {
            str: lambda v: "***" if "token" in str(v).lower() else v
        }
```

#### Secure API Communication

```python
# Correct: Proper SSL verification and error handling
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def create_secure_session():
    session = requests.Session()
    
    # Configure retries and timeouts
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    
    # Always verify SSL certificates
    session.verify = True
    
    return session
```

#### Secure Command Execution

```python
# Correct: Safe parameter passing for VM commands
import shlex
from typing import List

def execute_vm_command(vm_id: int, command: List[str]) -> dict:
    # Validate VM ID
    if not isinstance(vm_id, int) or vm_id < 1:
        raise ValueError("Invalid VM ID")
    
    # Use list form to prevent injection
    safe_command = [str(arg) for arg in command]
    
    # Log command execution (without sensitive data)
    logger.info(f"Executing command on VM {vm_id}: {safe_command[0]}")
    
    # Execute with proxmox API
    return proxmox_api.execute_command(vm_id, safe_command)
```

### Security Testing Requirements

#### Pre-Commit Security Validation

```bash
# Security validation script to run before commits
#!/bin/bash

echo "Running security validation..."

# Check for hardcoded secrets
if grep -r -E "(password|token|key|secret).*=.*['\"][^'\"]*['\"]" src/ --exclude-dir=tests; then
    echo "❌ Potential hardcoded secrets found"
    exit 1
fi

# Validate SSL configuration
python -c "
import ssl
from proxmox_mcp.config.loader import load_config
config = load_config()
if hasattr(config, 'verify_ssl') and not config.verify_ssl:
    print('❌ SSL verification disabled')
    exit(1)
print('✅ SSL verification enabled')
"

# Check environment variable usage
if ! grep -q "os.environ\|getenv\|Field.*env=" src/proxmox_mcp/config/; then
    echo "❌ No environment variable usage found in config"
    exit 1
fi

echo "✅ Security validation passed"
```

#### Security Integration Testing

- **Authentication testing**: Verify all authentication flows work correctly
- **Authorization testing**: Test proper permission enforcement
- **Input validation testing**: Test all input validation and sanitization
- **Error handling testing**: Ensure errors don't leak sensitive information
- **SSL/TLS testing**: Verify secure communication channels

### Security Incident Response

#### Immediate Actions for Security Issues

1. **Assess severity**: Determine if issue affects production systems
2. **Contain impact**: Isolate affected systems if necessary
3. **Document incident**: Record timeline and actions taken
4. **Notify stakeholders**: Inform relevant team members
5. **Implement fix**: Deploy security patch following change management
6. **Verify resolution**: Confirm vulnerability is properly addressed
7. **Post-incident review**: Document lessons learned and improve processes

#### Security Issue Escalation

- **Critical**: Immediate response required (credential exposure, RCE)
- **High**: Response within 24 hours (privilege escalation, data exposure)
- **Medium**: Response within 72 hours (DoS, information disclosure)
- **Low**: Address in next release cycle (security hardening opportunities)

## Repository Hygiene and Maintenance

### Overview

Repository hygiene involves proactive maintenance procedures to prevent accumulation of stale
references, outdated analysis, and technical debt. These procedures should be integrated into regular
development workflows to ensure repository health and accuracy.

### Pre-Work Hygiene Procedures

Before starting any development task, perform these validation steps:

```bash
# Validate current branch state and clean workspace
git status && git fetch origin && git log --oneline -5

# Check for stale analysis files and outdated references
find .claude/reports -name "*.md" -type f -mtime +30 -ls
find docs/ -name "*.md" -type f -exec grep -l "TODO\|FIXME\|outdated" {} \;

# Verify configuration and dependency consistency
python -c "from proxmox_mcp.config.loader import load_config; load_config()" 2>/dev/null || echo "Config validation failed"
```

### Regular Maintenance Schedule

#### Daily (During Active Development)

- **Memory Updates**: Capture new learnings and patterns immediately after completing tasks
- **Branch Cleanup**: Remove merged feature branches and stale references
- **Issue Synchronization**: Update issue status and remove stale labels

```bash
# Daily branch cleanup
git branch --merged main | grep -v main | xargs -n 1 git branch -d
git remote prune origin

# Validate current memory state alignment
get_all_coding_preferences # Review for outdated patterns
```

#### Weekly Maintenance

- **Analysis Validation**: Review and update repository analysis against current state
- **Documentation Accuracy**: Verify instruction files reflect current codebase structure
- **Dependency Updates**: Check for security updates and compatibility issues

```bash
# Weekly maintenance routine
pytest && black . && mypy . && ruff .
uv pip list --outdated
docker system prune -f
```

#### Monthly Deep Cleaning

- **Comprehensive Memory Audit**: Review all stored coding preferences for accuracy
- **Architecture Documentation**: Update component descriptions and design patterns
- **Security Review**: Validate security practices and credential management

### Memory Management Hygiene

#### When to Capture New Learnings

Immediately capture patterns in these scenarios:

- **After resolving complex technical issues** - Document solution approach and decision rationale
- **When implementing new architectural patterns** - Store complete implementation context
- **Following security implementations** - Capture security best practices and validation methods
- **After performance optimizations** - Document performance patterns and measurement approaches
- **When discovering integration patterns** - Store MCP protocol and Proxmox API integration insights

#### Memory Update Timing

```python
# Capture immediately after significant implementations
add_coding_preference(
    content="""
    ProxmoxMCP Tool Implementation Pattern:
    - Inherit from ProxmoxTool base class
    - Use Pydantic models for validation
    - Implement rich formatting via ProxmoxTheme
    - Add comprehensive error handling
    - Include tool registration in definitions.py
    """,
    context="Complete implementation with dependencies and examples"
)
```

### Analysis Accuracy Validation

#### Pre-Task Validation

Before starting any analysis or implementation:

1. **Current State Verification**: Use LS, Glob, and Grep tools to verify actual codebase structure
2. **Reference Validation**: Check that all file references and paths are current and accurate
3. **Component Status**: Verify component descriptions match actual implementation state
4. **Integration Points**: Validate that described integration patterns still exist and function

#### Post-Task Validation

After completing implementation work:

1. **Architecture Alignment**: Verify changes align with documented architectural patterns
2. **Reference Updates**: Update any documentation that references modified components
3. **Integration Consistency**: Ensure new implementations follow established integration patterns

### Repository Health Metrics

#### Key Health Indicators

- **Test Coverage**: Maintain >90% coverage for core components
- **Code Quality**: Zero mypy errors, consistent black formatting
- **Documentation Currency**: No references to non-existent files or outdated patterns
- **Memory Accuracy**: Stored coding preferences reflect current implementation patterns
- **Security Posture**: No exposed secrets, current security practices documented

## Memories

- "When tasked are completed you must commit changes to github"
- When submitting PR reviews with complex text containing special shell characters, it's better to:
  1. Use simpler review text, or
  2. Escape special characters properly, or
  3. Submit reviews through the GitHub web interface for complex formatting
- ALWAYS verify package versions exist before setting dependency constraints using
  `pip index versions <package>` or GitHub releases to prevent uninstallable packages
- ALWAYS treat GitHub API as authoritative source for repository state; verify branch existence before analysis
- Perform stale branch cleanup before any repository analysis to ensure accuracy
