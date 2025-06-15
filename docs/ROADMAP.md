# ProxmoxMCP Project Roadmap

This roadmap outlines the planned development and improvement efforts for the ProxmoxMCP project, prioritized for production readiness. The phases are organized by urgency with specific implementation guidance and timelines.

## Phase 1: Critical Security Fixes (Immediate - 1-2 days)

These items address critical security vulnerabilities and must be implemented immediately:

### Secure Token Storage

- [ ] **Token Encryption**: Implement token encryption at rest in `proxmox_mcp/config/loader.py`
  ```python
  # Add cryptography.fernet for token encryption
  import os
  from cryptography.fernet import Fernet
  
  def encrypt_token(token: str, key: bytes) -> str:
      """Encrypt sensitive tokens"""
      f = Fernet(key)
      return f.encrypt(token.encode()).decode()
  ```

### SSL Security

- [x] **Enable SSL Verification**: Change default from `"verify_ssl": false` to `"verify_ssl": true` in `proxmox-config/config.example.json`

### Input Validation

- [ ] **VM Command Validation**: Add input validation and sanitization in `proxmox_mcp/tools/vm.py`
  ```python
  import shlex
  def validate_command(command: str) -> str:
      """Validate and sanitize shell commands"""
      # Implement whitelist of allowed commands
      # Escape special characters
      return shlex.quote(command)
  ```

### Configuration Security

- [ ] **Environment Variable Tokens**: Update config to use environment variables for sensitive data
  ```json
  {
      "auth": {
          "user": "mcp@pve",
          "token_name": "mcp-token", 
          "token_value": "${PROXMOX_TOKEN}"
      }
  }
  ```

## Phase 2: Docker Improvements (1 day)

Enhance Docker security and deployment:

### Docker Security

- [ ] **Non-Root User**: Run container as non-root user from start
  ```dockerfile
  # Enhanced Dockerfile with security best practices
  FROM python:3.10-slim AS base
  
  # Security: Run as non-root from the start
  RUN groupadd -r mcp && useradd -r -g mcp mcp
  ```

### Docker Secrets

- [ ] **Implement Docker Secrets**: Use Docker secrets for sensitive credentials
  ```yaml
  services:
    proxmox-mcp:
      secrets:
        - proxmox_token
      environment:
        PROXMOX_TOKEN_FILE: /run/secrets/proxmox_token
  
  secrets:
    proxmox_token:
      external: true
  ```

### Resource Management

- [ ] **Resource Limits**: Add resource limits and health checks
  ```yaml
  deploy:
    resources:
      limits:
        cpus: '1'
        memory: 512M
  restart: unless-stopped
  healthcheck:
    test: ["CMD", "python", "-m", "proxmox_mcp.health"]
    interval: 30s
    timeout: 10s
    retries: 3
  ```

## Phase 3: Enhanced Error Handling (2-3 days)

Standardize error handling across the codebase:

### Exception Hierarchy

- [ ] **Specific Exception Classes**: Create ProxmoxMCP-specific exceptions in `proxmox_mcp/tools/base.py`
  ```python
  class ProxmoxError(Exception):
      """Base exception for Proxmox operations"""
      pass
  
  class ProxmoxAuthError(ProxmoxError):
      """Authentication-related errors"""
      pass
  
  class ProxmoxResourceNotFoundError(ProxmoxError):
      """Resource not found errors"""
      pass
  ```

### Error Handling Implementation

- [ ] **Standardized Error Handling**: Implement consistent error handling patterns
  ```python
  def _handle_error(self, operation: str, error: Exception) -> None:
      if isinstance(error, proxmoxer.AuthenticationError):
          raise ProxmoxAuthError(f"Authentication failed: {error}")
      # ... more specific error handling
  ```

### Health Check Endpoint

- [ ] **Health Check Tool**: Add health check endpoint for monitoring
  ```python
  @self.mcp.tool(description="Check MCP server and Proxmox connection health")
  def health_check():
      try:
          version = self.proxmox.version.get()
          return {"status": "healthy", "proxmox_version": version}
      except Exception as e:
          return {"status": "unhealthy", "error": str(e)}
  ```

## Phase 4: Performance Improvements

Optimize performance for production workloads:

### Connection Management

- [ ] **Connection Pooling**: Implement connection pooling in `proxmox_mcp/core/proxmox.py`
  ```python
  from functools import lru_cache
  import asyncio
  
  class ProxmoxManager:
      def __init__(self, ...):
          self._connection_pool = {}
          self._cache = {}
          
      @lru_cache(maxsize=100)
      def get_cached_node_status(self, node: str):
          """Cache frequently accessed data"""
          return self.api.nodes(node).status.get()
  ```

### Async Operations

- [ ] **Enhanced Async Support**: Convert more operations to async
- [ ] **Request Throttling**: Implement request throttling to prevent API rate limiting

## Phase 5: Feature Additions

Add new functionality after core improvements:

### LXC Support

- [ ] **Container Tools**: Add LXC container support
  ```python
  # In proxmox_mcp/tools/container.py
  class ContainerTools(ProxmoxTool):
      def get_containers(self) -> List[Content]:
          """List LXC containers"""
          # Implementation similar to VM tools
  ```

### Batch Operations

- [ ] **Concurrent Operations**: Implement batch command execution
  ```python
  async def batch_execute_commands(self, commands: List[VMCommand]):
      """Execute multiple commands concurrently"""
      tasks = [self.execute_command(cmd) for cmd in commands]
      return await asyncio.gather(*tasks)
  ```

### Extended Functionality

- [ ] **Proxmox Backup Server**: Add support for Proxmox Backup Server
- [ ] **Monitoring and Alerting**: Implement resource monitoring and alerting
- [ ] **Webhook Support**: Implement webhook support for events

## Quick Wins for Immediate Impact

These can be implemented alongside the phases:

- [ ] **Secure Config Defaults**: Update `proxmox-config/config.example.json` with secure defaults
  ```json
  {
      "proxmox": {
          "host": "your-proxmox-host",
          "port": 8006,
          "verify_ssl": true,  // Changed from false
          "service": "PVE"
      },
      "auth": {
          "user": "mcp@pve",  // Use dedicated user
          "token_name": "mcp-token",
          "token_value": "${PROXMOX_TOKEN}"  // Environment variable
      }
  }
  ```
- [ ] **Dedicated User**: Use dedicated MCP user instead of root/admin
- [ ] **Docker Base Image**: Use specific version tags for base images
- [ ] **Environment Variables**: Standardize environment variable names

## Testing & Quality Assurance

Throughout all phases:

- [ ] **Expand Test Coverage**: Add comprehensive tests for new functionality
- [ ] **Security Testing**: Add security-focused tests
- [ ] **Integration Testing**: Add integration tests with mock Proxmox API
- [ ] **Container Testing**: Implement container testing

## Timeline

- **Phase 1**: 1-2 days (Critical security fixes)
- **Phase 2**: 1 day (Docker improvements)  
- **Phase 3**: 2-3 days (Error handling)
- **Phase 4**: 1-2 weeks (Performance improvements)
- **Phase 5**: 2-4 weeks (Feature additions)

## Focus Areas

**Immediate Priority**: Security fixes first, then Docker improvements and error handling
**Next Priority**: Performance optimizations and comprehensive testing
**Future Priority**: New features and extended functionality

This roadmap is a living document and will be updated as development progresses and new priorities emerge.