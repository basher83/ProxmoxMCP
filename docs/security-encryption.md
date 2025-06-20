# 🔐 Token Encryption Guide

ProxmoxMCP now supports secure encryption of API tokens and other sensitive configuration values at rest.

## Features

- **Fernet Encryption**: Industry-standard AES 128 in CBC mode with HMAC SHA256 authentication
- **Secure Key Derivation**: PBKDF2 with salt to prevent rainbow table attacks
- **Environment-based Keys**: Master keys stored separately from encrypted data
- **Backward Compatibility**: Existing plain-text configurations continue to work
- **CLI Tools**: Easy-to-use command-line utilities for encryption management

## Quick Start

### 1. Generate a Master Key

```bash
# Generate a new master key securely
python -m proxmox_mcp.utils.encrypt_config --generate-key

# Follow the prompts to securely save the generated key
# Then set it as an environment variable:
export PROXMOX_MCP_MASTER_KEY="your-generated-key"
```

> **Security Note**: The key generation process now includes enhanced security measures that
> prevent the key from being exposed in terminal history or log files during automatic generation.

### 2. Encrypt Your Configuration

```bash
# Encrypt existing config
python -m proxmox_mcp.utils.encrypt_config proxmox-config/config.json

# This creates config.encrypted.json with encrypted token values
```

### 3. Use Encrypted Configuration

```bash
# Set environment variables
export PROXMOX_MCP_CONFIG="proxmox-config/config.encrypted.json"
export PROXMOX_MCP_MASTER_KEY="your-master-key"

# Run the server
python -m proxmox_mcp.server
```

## CLI Reference

### Encrypt Configuration File

```bash
# Basic encryption
python -m proxmox_mcp.utils.encrypt_config config.json

# Specify output file
python -m proxmox_mcp.utils.encrypt_config config.json -o encrypted.json
```

### Check Encryption Status

```bash
python -m proxmox_mcp.utils.encrypt_config config.json --status
```

### Generate Master Key

```bash
# Generate a new master key with security prompts
python -m proxmox_mcp.utils.encrypt_config --generate-key

# The tool will display the key once and prompt you to save it securely
# No key exposure in logs or terminal history during automatic generation
```

### Master Key Rotation

ProxmoxMCP supports secure master key rotation for enhanced security compliance and incident response.

#### Rotate Key for Single Configuration

```bash
# Rotate master key for a specific configuration file
python -m proxmox_mcp.utils.encrypt_config --rotate-key config.encrypted.json

# The tool will:
# 1. Verify current master key can decrypt the configuration
# 2. Create a timestamped backup of the original file
# 3. Generate a new master key
# 4. Re-encrypt all tokens with the new key
# 5. Provide instructions for updating environment variables
```

#### Rotate Key for All Configurations

```bash
# Rotate master key for all configuration files in a directory
python -m proxmox_mcp.utils.encrypt_config --rotate-key-all proxmox-config/

# Bulk rotation will:
# - Process all *.json files in the directory (except examples)
# - Skip files without encrypted content
# - Use the same new master key for all files
# - Create individual backups for each rotated file
# - Provide summary of successful and failed rotations
```

#### Key Rotation Best Practices

1. **Schedule Regular Rotations**: Rotate master keys annually or after security incidents
2. **Test Before Production**: Always test rotated configurations before deploying
3. **Coordinate Updates**: Ensure all systems using the configuration are updated with the new key
4. **Secure Backup Storage**: Store configuration backups securely and separately from the new key
5. **Monitor Rotation**: Keep audit logs of key rotation activities

## Configuration Format

### Before Encryption

```json
{
  "auth": {
    "user": "root@pam",
    "token_name": "my-token",
    "token_value": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
  }
}
```

### After Encryption

```json
{
  "auth": {
    "user": "root@pam",
    "token_name": "my-token",
    "token_value": "enc:Z0FBQUFBQm9QYjUz..."
  }
}
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `PROXMOX_MCP_MASTER_KEY` | Master encryption key | Yes (for encrypted configs) |
| `PROXMOX_MCP_CONFIG` | Path to config file | Yes |

## Security Best Practices

1. **Store Keys Separately**: Never store the master key in the same location as encrypted data
2. **Use Environment Variables**: Avoid hardcoding keys in scripts or configuration files
3. **Rotate Keys Regularly**: Generate new master keys periodically and re-encrypt configurations
4. **Secure Key Storage**: Use secure key management systems in production environments
5. **Backup Safely**: Ensure encrypted backups include both data and key recovery procedures
6. **Clear Terminal History**: After key generation, consider clearing terminal history to prevent exposure
7. **Use CLI Tool**: Always use the provided CLI tool for key generation rather than manual methods
8. **Test After Rotation**: Always verify configurations work after key rotation before production use
9. **Coordinate Key Updates**: Ensure all systems are updated with new keys during rotation
10. **Audit Key Operations**: Maintain logs of key generation, rotation, and usage activities

## Migration from Plain Text

Existing configurations work without changes. To migrate:

1. **Backup Current Config**: Always backup your working configuration
2. **Generate Master Key**: Create and securely store a master key
3. **Encrypt Configuration**: Use the CLI tool to encrypt sensitive values
4. **Update Environment**: Set the master key environment variable
5. **Test Thoroughly**: Verify the server starts and connects successfully
6. **Clean Up**: Securely delete plain text configuration files

## Troubleshooting

### Common Issues

**"Token decryption failed"**

- Verify `PROXMOX_MCP_MASTER_KEY` environment variable is set correctly
- Ensure the master key matches the one used for encryption

**"Config file not found"**

- Check `PROXMOX_MCP_CONFIG` environment variable points to correct file
- Verify file permissions and path accessibility

**"Invalid encrypted token format"**

- Encrypted tokens must start with `enc:` prefix
- Verify file wasn't corrupted during transfer or storage

### Debug Mode

Enable debug logging to troubleshoot encryption issues:

```bash
# Add to your config.json
{
  "logging": {
    "level": "DEBUG"
  }
}
```

## Key Rotation Procedures

Key rotation is essential for maintaining long-term security. ProxmoxMCP provides comprehensive
tools and procedures for safely rotating encryption keys.

### When to Rotate Keys

- **Regular Schedule**: Annually or as per your organization's security policy
- **Security Incidents**: When compromise is suspected or confirmed
- **Personnel Changes**: After team member departures or role changes
- **Major Deployments**: Before critical releases or infrastructure changes
- **Compliance Requirements**: As mandated by security frameworks (SOC2, ISO27001, etc.)

### Pre-Rotation Checklist

Before starting key rotation, ensure you have:

1. **Current Access**: Ability to decrypt existing configurations
2. **Backup Strategy**: Secure backup procedures for configuration files
3. **Testing Environment**: Non-production environment for validation
4. **Downtime Window**: Planned maintenance window for service restarts
5. **Rollback Plan**: Procedures to revert if rotation fails
6. **Team Coordination**: All team members aware of the rotation schedule

### Step-by-Step Rotation Procedure

#### 1. Preparation Phase

```bash
# Verify current configuration works
export PROXMOX_MCP_CONFIG="proxmox-config/config.encrypted.json"
export PROXMOX_MCP_MASTER_KEY="your-current-key"
python -m proxmox_mcp.server --test

# Create secure backup
cp proxmox-config/config.encrypted.json proxmox-config/config.encrypted.json.backup.$(date +%Y%m%d_%H%M%S)
```

#### 2. Single Configuration Rotation

```bash
# Rotate key for one configuration file
python -m proxmox_mcp.utils.encrypt_config --rotate-key proxmox-config/config.encrypted.json

# The tool will:
# - Verify current key can decrypt the file
# - Create timestamped backup automatically
# - Generate new master key
# - Re-encrypt all sensitive values
# - Display new key for environment update
```

#### 3. Bulk Configuration Rotation

```bash
# Rotate all configurations in a directory
python -m proxmox_mcp.utils.encrypt_config --rotate-key-all proxmox-config/

# This will:
# - Process all .json files (excluding examples)
# - Use same new key for all files
# - Skip files without encrypted content
# - Create individual backups
# - Provide rotation summary
```

#### 4. Environment Update

```bash
# Update environment with new key (provided by rotation tool)
export PROXMOX_MCP_MASTER_KEY="new-generated-key"

# Test with new key
python -m proxmox_mcp.server --test
```

#### 5. Validation Phase

```bash
# Verify all functionality works
python -m proxmox_mcp.server --test

# Test actual Proxmox connectivity
# (Start server and test MCP tools)
```

### Zero-Downtime Rotation Strategies

#### Blue-Green Deployment

1. **Prepare Green Environment**: Deploy with new keys
2. **Validate Green**: Test all functionality
3. **Switch Traffic**: Update load balancer/proxy
4. **Monitor**: Ensure no errors
5. **Cleanup Blue**: Remove old environment after validation

#### Rolling Update

1. **Rotate Keys**: Generate new keys for configuration
2. **Update Environment**: Set new master key
3. **Restart Service**: Restart with new configuration
4. **Validate**: Confirm service operational
5. **Update Monitoring**: Ensure alerts still function

### Rollback Procedures

If key rotation fails, follow these steps:

#### Immediate Rollback

```bash
# Stop any running services
sudo systemctl stop proxmox-mcp  # or docker stop container

# Restore from backup
cp proxmox-config/config.encrypted.json.backup.TIMESTAMP proxmox-config/config.encrypted.json

# Restore old environment variable
export PROXMOX_MCP_MASTER_KEY="old-master-key"

# Test configuration
python -m proxmox_mcp.server --test

# Restart service
sudo systemctl start proxmox-mcp
```

#### Post-Rollback Analysis

1. **Document Issue**: Record what went wrong
2. **Preserve Evidence**: Keep failed configuration for analysis
3. **Review Logs**: Check server and application logs
4. **Plan Fix**: Address root cause before retry
5. **Schedule Retry**: Plan next rotation attempt

## Advanced Key Management

### Multi-Environment Key Management

#### Development Environment

```bash
# Use separate keys for dev
export PROXMOX_MCP_MASTER_KEY_DEV="dev-specific-key"
export PROXMOX_MCP_CONFIG="dev-config/config.encrypted.json"
```

#### Staging Environment

```bash
# Staging mirrors production procedures
export PROXMOX_MCP_MASTER_KEY_STAGING="staging-specific-key"
export PROXMOX_MCP_CONFIG="staging-config/config.encrypted.json"
```

#### Production Environment

```bash
# Production uses highest security standards
export PROXMOX_MCP_MASTER_KEY="production-master-key"
export PROXMOX_MCP_CONFIG="prod-config/config.encrypted.json"
```

### Key Management Lifecycle

#### Key Generation

- **Use CLI Tool**: Always use the provided encryption utility
- **Secure Generation**: Use cryptographically secure random generation
- **Document Creation**: Log key generation events (not the keys themselves)
- **Immediate Storage**: Store keys in secure key management systems

#### Key Storage

- **Separate Storage**: Never store keys with encrypted data
- **Access Control**: Implement strict access controls
- **Encryption at Rest**: Encrypt keys in storage systems
- **Backup Keys**: Maintain secure, encrypted backups

#### Key Distribution

- **Secure Channels**: Use encrypted communication for key distribution
- **Just-in-Time**: Provide keys only when needed
- **Audit Trail**: Log key access and distribution
- **Temporary Access**: Use short-lived keys where possible

#### Key Retirement

- **Secure Deletion**: Use cryptographic erasure techniques
- **Audit Cleanup**: Remove keys from all systems
- **Documentation**: Update key management records
- **Compliance**: Follow data retention policies

### Disaster Recovery Scenarios

#### Lost Master Key

If you lose access to your master key:

1. **Check Backups**: Look for securely stored key backups
2. **Emergency Access**: Use disaster recovery key procedures
3. **Re-encrypt Data**: Use available plain-text configurations to re-encrypt
4. **Update Systems**: Deploy new configurations with new keys
5. **Post-Incident**: Review and improve key backup procedures

#### Corrupted Configuration

If configuration files become corrupted:

1. **Stop Service**: Prevent further issues
2. **Restore Backup**: Use most recent valid backup
3. **Validate Restoration**: Test with current master key
4. **Resume Service**: Restart with restored configuration
5. **Investigate**: Determine corruption cause

#### Compromised Keys

If key compromise is suspected:

1. **Immediate Rotation**: Start emergency key rotation
2. **Revoke Access**: Disable compromised keys
3. **Audit Usage**: Review key usage logs
4. **Notify Stakeholders**: Inform relevant parties
5. **Update Procedures**: Strengthen key protection

## Troubleshooting Key Rotation

### Common Rotation Issues

#### "Current master key cannot decrypt configuration"

**Symptoms**: Rotation fails during verification phase

**Causes**:

- Wrong `PROXMOX_MCP_MASTER_KEY` environment variable
- Configuration file corrupted
- Key truncated or modified

**Solutions**:

```bash
# Verify environment variable is set correctly
echo $PROXMOX_MCP_MASTER_KEY | wc -c  # Should be 45 characters

# Test decryption manually
python -c "
from proxmox_mcp.utils.encryption import TokenEncryption
import os
enc = TokenEncryption(os.getenv('PROXMOX_MCP_MASTER_KEY'))
print('Key works!' if enc else 'Key invalid')
"

# Check configuration file integrity
python -m proxmox_mcp.utils.encrypt_config config.encrypted.json --status
```

#### "Failed to create backup"

**Symptoms**: Backup creation fails during rotation

**Causes**:

- Insufficient disk space
- Permission issues
- File system errors

**Solutions**:

```bash
# Check disk space
df -h

# Check permissions
ls -la proxmox-config/

# Create backup manually
cp config.encrypted.json config.encrypted.json.manual.backup
```

#### "Service fails to start with new key"

**Symptoms**: Server won't start after key rotation

**Causes**:

- Environment variable not updated
- Configuration cache issues
- Service configuration problems

**Solutions**:

```bash
# Verify new environment variable
echo $PROXMOX_MCP_MASTER_KEY

# Clear any cache
rm -rf ~/.proxmox_mcp_cache

# Test configuration directly
python -m proxmox_mcp.server --test

# Check service logs
journalctl -u proxmox-mcp -f
```

### Debug Mode for Rotation

Enable detailed logging during rotation:

```bash
# Enable debug logging
export PROXMOX_MCP_DEBUG=true

# Run rotation with verbose output
python -m proxmox_mcp.utils.encrypt_config --rotate-key config.encrypted.json

# Check detailed logs
tail -f /var/log/proxmox-mcp/rotation.log
```

### Validation Procedures After Rotation

#### Basic Connectivity Test

```bash
# Test server startup
python -m proxmox_mcp.server --test

# Verify MCP tools work
python -c "
import asyncio
from proxmox_mcp.core.proxmox import ProxmoxManager
# Test basic connectivity
"
```

#### Full Integration Test

```bash
# Start server in test mode
python -m proxmox_mcp.server --test-mode

# Run MCP client tests
mcp test localhost:8000

# Verify all tools respond correctly
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Key Rotation
on:
  schedule:
    - cron: '0 2 1 */3 *'  # Quarterly at 2 AM
  workflow_dispatch:

jobs:
  rotate-keys:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          pip install -e .

      - name: Rotate staging keys
        env:
          PROXMOX_MCP_MASTER_KEY: ${{ secrets.STAGING_MASTER_KEY }}
        run: |
          python -m proxmox_mcp.utils.encrypt_config --rotate-key staging-config/config.encrypted.json

      - name: Test rotated configuration
        env:
          PROXMOX_MCP_MASTER_KEY: ${{ secrets.NEW_STAGING_KEY }}
        run: |
          python -m proxmox_mcp.server --test

      - name: Update secrets
        run: |
          # Update GitHub secrets with new key
          gh secret set STAGING_MASTER_KEY --body "$NEW_KEY"
```

### GitLab CI

```yaml
stages:
  - rotate
  - test
  - deploy

rotate-keys:
  stage: rotate
  script:
    - python -m proxmox_mcp.utils.encrypt_config --rotate-key-all config/
    - echo "NEW_KEY=$NEW_MASTER_KEY" >> rotation.env
  artifacts:
    reports:
      dotenv: rotation.env
  only:
    - schedules

test-rotation:
  stage: test
  needs: [rotate-keys]
  script:
    - export PROXMOX_MCP_MASTER_KEY=$NEW_KEY
    - python -m proxmox_mcp.server --test
  dependencies:
    - rotate-keys

deploy-production:
  stage: deploy
  needs: [test-rotation]
  script:
    - kubectl create secret generic proxmox-master-key --from-literal=key=$NEW_KEY
    - kubectl rollout restart deployment/proxmox-mcp
  only:
    - schedules
```

### Automated Monitoring

```bash
# Create monitoring script for key rotation
cat > monitor-key-rotation.sh << 'EOF'
#!/bin/bash

# Monitor key age and trigger rotation
KEY_FILE="/etc/proxmox-mcp/key-metadata.json"
MAX_AGE_DAYS=365

if [ -f "$KEY_FILE" ]; then
    LAST_ROTATION=$(jq -r '.last_rotation' "$KEY_FILE")
    CURRENT_DATE=$(date +%s)
    DAYS_SINCE_ROTATION=$(( (CURRENT_DATE - LAST_ROTATION) / 86400 ))

    if [ $DAYS_SINCE_ROTATION -gt $MAX_AGE_DAYS ]; then
        echo "Key rotation required: $DAYS_SINCE_ROTATION days since last rotation"
        # Trigger automated rotation
        python -m proxmox_mcp.utils.encrypt_config --rotate-key-all /etc/proxmox-mcp/
    fi
fi
EOF

# Schedule with cron
echo "0 2 * * 0 /usr/local/bin/monitor-key-rotation.sh" | sudo crontab -
```

## Integration Examples

### Docker Compose

```yaml
services:
  proxmox-mcp:
    environment:
      - PROXMOX_MCP_CONFIG=/app/config/config.encrypted.json
      - PROXMOX_MCP_MASTER_KEY=${MASTER_KEY}
    volumes:
      - ./config:/app/config
    healthcheck:
      test: ["CMD", "python", "-m", "proxmox_mcp.server", "--test"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Docker Swarm with Secrets

```yaml
version: '3.8'
services:
  proxmox-mcp:
    image: proxmox-mcp:latest
    environment:
      - PROXMOX_MCP_CONFIG=/app/config/config.encrypted.json
    secrets:
      - master_key
    volumes:
      - ./config:/app/config
    deploy:
      replicas: 2
      update_config:
        parallelism: 1
        delay: 10s

secrets:
  master_key:
    external: true
```

### Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: proxmox-mcp
spec:
  replicas: 2
  selector:
    matchLabels:
      app: proxmox-mcp
  template:
    metadata:
      labels:
        app: proxmox-mcp
    spec:
      containers:
      - name: proxmox-mcp
        image: proxmox-mcp:latest
        env:
        - name: PROXMOX_MCP_CONFIG
          value: "/app/config/config.encrypted.json"
        - name: PROXMOX_MCP_MASTER_KEY
          valueFrom:
            secretKeyRef:
              name: proxmox-master-key
              key: key
        volumeMounts:
        - name: config
          mountPath: /app/config
        readinessProbe:
          exec:
            command:
            - python
            - -m
            - proxmox_mcp.server
            - --test
          initialDelaySeconds: 5
          periodSeconds: 10
      volumes:
      - name: config
        configMap:
          name: proxmox-config
---
apiVersion: v1
kind: Secret
metadata:
  name: proxmox-master-key
type: Opaque
data:
  key: <base64-encoded-master-key>
```

### Systemd Service

```ini
[Unit]
Description=Proxmox MCP Server
After=network.target

[Service]
Type=simple
User=proxmox-mcp
Group=proxmox-mcp
Environment=PROXMOX_MCP_CONFIG=/etc/proxmox-mcp/config.encrypted.json
EnvironmentFile=/etc/proxmox-mcp/environment
ExecStart=/usr/bin/python -m proxmox_mcp.server
ExecReload=/bin/kill -HUP $MAINPID
Restart=always
RestartSec=10

# Security hardening
NoNewPrivileges=yes
PrivateTmp=yes
ProtectSystem=strict
ProtectHome=yes
ReadWritePaths=/var/log/proxmox-mcp

[Install]
WantedBy=multi-user.target
```

Environment file (`/etc/proxmox-mcp/environment`):

```bash
PROXMOX_MCP_MASTER_KEY=your-master-key
```

For more information, see the main [README.md](../README.md) or [security documentation](./security.md).
