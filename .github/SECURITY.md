# Security Policy

## Supported Versions

We actively support the following versions of ProxmoxMCP with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of ProxmoxMCP seriously. If you discover a security vulnerability, please report it responsibly.

### How to Report

**🔒 For security vulnerabilities, please do NOT create a public GitHub issue.**

Instead, please:

1. **Use GitHub Security Advisories**: Go to the
   [Security tab](https://github.com/basher83/ProxmoxMCP/security/advisories) and
   click "Report a vulnerability"
2. **Email**: Send details to the project maintainers at [INSERT_EMAIL]
3. **Use our Security Issue Template**: If you must use issues, use the
   [Security Vulnerability template](https://github.com/basher83/ProxmoxMCP/issues/new?template=security_vulnerability.md)

### What to Include

Please include the following information:

- **Description**: Clear description of the vulnerability
- **Impact**: Potential impact and affected components
- **Steps to Reproduce**: Detailed reproduction steps
- **Environment**: ProxmoxMCP version, Proxmox version, deployment method
- **Suggested Fix**: Any proposed solutions (if available)

### Response Timeline

- **Initial Response**: Within 48 hours
- **Assessment**: Within 1 week
- **Fix Development**: Based on severity (Critical: 1-7 days, High: 1-2 weeks, Medium: 2-4 weeks)
- **Public Disclosure**: After fix is released and users have time to update

### Security Best Practices

When using ProxmoxMCP, please follow these security guidelines:

#### Authentication & Authorization

- ✅ Use dedicated API tokens (never root password)
- ✅ Enable SSL/TLS verification (`verify_ssl: true`)
- ✅ Use least-privilege API tokens
- ✅ Rotate API tokens regularly
- ❌ Don't store tokens in plaintext
- ❌ Don't commit tokens to version control

#### Deployment Security

- ✅ Run in containerized environments when possible
- ✅ Use non-root users in containers
- ✅ Keep dependencies updated
- ✅ Monitor logs for suspicious activity
- ❌ Don't expose unnecessary ports
- ❌ Don't run as root in production

#### Network Security

- ✅ Use secure networks for Proxmox communication
- ✅ Implement network segmentation
- ✅ Use VPNs for remote access
- ❌ Don't expose Proxmox API to the internet
- ❌ Don't use unencrypted connections

### Known Security Considerations

- **Command Execution**: VM commands are executed via QEMU Guest Agent
- **API Access**: Requires Proxmox API token with appropriate permissions
- **Network Access**: Needs network access to Proxmox server
- **Configuration**: Sensitive data in configuration files should be protected

### Security Updates

Security updates will be:

- Released as patch versions (e.g., 1.0.1)
- Documented in release notes with CVE numbers when applicable
- Announced via GitHub Releases and Security Advisories

### Acknowledgments

We appreciate responsible disclosure and will acknowledge security researchers who
report vulnerabilities to us (unless they prefer to remain anonymous).

---

**Last Updated**: January 30, 2025
**Next Review**: June 30, 2025
