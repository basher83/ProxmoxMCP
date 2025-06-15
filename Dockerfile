# syntax=docker/dockerfile:1

# ---- Base Arguments ----
# Build arguments for customization
ARG PYTHON_VERSION=3.10
ARG BUILD_ENV=production

# ---- Base image (for both builder and final) ----
FROM python:${PYTHON_VERSION}-slim AS base

# Set environment variables for Python
# PYTHONDONTWRITEBYTECODE: Prevents Python from writing .pyc files
# PYTHONUNBUFFERED: Ensures Python output is sent straight to terminal without buffering
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set workdir
WORKDIR /app

# ---- Builder stage ----
FROM base AS builder

# Install build dependencies (for pip, venv, and system packages needed for build)
RUN --mount=type=cache,target=/root/.cache/apt \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        git \
    && rm -rf /var/lib/apt/lists/*

# Copy only dependency files first for better cache usage
COPY --link pyproject.toml setup.py requirements.in requirements-dev.in ./

# Create virtual environment with appropriate permissions
RUN python -m venv .venv && \
    chmod -R 755 .venv/bin

# Install pip dependencies (conditionally include dev dependencies based on BUILD_ENV)
ENV PIP_CACHE_DIR=/root/.cache/pip

# Create a temporary requirements file with only public dependencies
RUN echo "proxmoxer>=2.0.1,<3.0.0\nrequests>=2.31.0,<3.0.0\npydantic>=2.0.0,<3.0.0" > public-requirements.in

# First install base tools and public dependencies
RUN --mount=type=cache,target=$PIP_CACHE_DIR \
    .venv/bin/pip install --upgrade pip setuptools wheel && \
    .venv/bin/pip install -r public-requirements.in && \
    if [ "$BUILD_ENV" = "development" ]; then \
        .venv/bin/pip install -r requirements-dev.in; \
    fi

# Install the MCP SDK from GitHub with specific version (package name is 'mcp')
RUN --mount=type=cache,target=$PIP_CACHE_DIR \
    .venv/bin/pip install git+https://github.com/modelcontextprotocol/python-sdk.git@v1.8.0#egg=mcp

# Copy source code - we'll use PYTHONPATH instead of installing the package
COPY --link src/ ./src/

# No need to copy configuration files as they will be mounted at runtime

# ---- Final stage ----
FROM base AS final

# Create a non-root user
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application code from builder
# Copy application files with appropriate permissions
COPY --from=builder --chown=appuser:appgroup /app/src /app/src

# Create necessary directories with proper permissions
RUN mkdir -p /app/proxmox-config /app/logs && \
    chown -R appuser:appgroup /app/proxmox-config /app/src /app/logs

# Set environment variables for venv and Python path
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH=/app/src

# Set workdir and switch to non-root user
WORKDIR /app
USER appuser

# Expose no ports (stdio server)
# (If you want to expose a port, add EXPOSE here)

# Add health check to verify the application is running correctly
# Check if Python process is running and the application directory structure is intact
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD ps aux | grep "[p]ython -m proxmox_mcp.server" || exit 1

# Switch back to root to create health check script
USER root

# Create a simple health script that tests basic functionality
RUN echo '#!/bin/sh\n\
if [ -z "$PROXMOX_MCP_CONFIG" ]; then\n\
  echo "PROXMOX_MCP_CONFIG not set, skipping deep health check"\n\
  exit 0\n\
fi\n\
if [ -f "$PROXMOX_MCP_CONFIG" ] && [ -d "/app/src/proxmox_mcp" ]; then\n\
  exit 0\n\
else\n\
  exit 1\n\
fi' > /app/health_check.sh && \
    chmod +x /app/health_check.sh && \
    chown appuser:appgroup /app/health_check.sh

# Switch back to appuser for runtime
USER appuser

# Entrypoint: run the MCP server (config path must be provided via env)
# Example: docker run -e PROXMOX_MCP_CONFIG=/app/proxmox-config/config.json ...
ENTRYPOINT ["python", "-m", "proxmox_mcp.server"]
