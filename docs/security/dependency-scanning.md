# Dependency Vulnerability Scanning

This document outlines the security scanning process for ProxmoxMCP dependencies.

## Current Security Status

✅ **All dependencies updated** as of commit b9fb0da:

- setuptools 80.9.0 (≥78.1.1 required for CVE-2025-47273)
- requests 2.32.4 (≥2.32.4 required for CVE-2024-47081)
- h11 0.16.0 (≥0.16.0 required for CVE-2025-43859)

## Manual Scanning Commands

### Using uv with pip-audit

```bash
# Install pip-audit if not available
uv add --dev pip-audit

# Scan current dependencies
uv run pip-audit

# Scan with detailed output
uv run pip-audit --format=json --output=security-report.json
```

### Using safety (alternative)

```bash
# Install safety scanner
uv add --dev safety

# Export dependencies and scan
uv export --format=requirements-txt | uv run safety check --stdin
```

## Monitoring and Prevention

### Regular Security Reviews

- Run dependency scans before each release
- Monitor security advisories for core dependencies
- Update vulnerable dependencies immediately for critical issues

### Automated Prevention (Future Enhancement)

Consider implementing:

- GitHub Dependabot for automated dependency updates
- Pre-commit hooks for security scanning
- CI/CD integration with security scanning tools

## Response Process for Vulnerabilities

1. **Assess Impact**: Determine if vulnerability affects ProxmoxMCP functionality
2. **Update Dependencies**: Use `uv add "package>=secure_version"`
3. **Test Functionality**: Run full test suite and quality checks
4. **Commit Changes**: Follow security commit message format
5. **Document Resolution**: Update this file with resolution details

## Contact and Escalation

For critical security vulnerabilities, follow responsible disclosure practices and escalate to
project maintainers immediately.
