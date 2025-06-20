# ProxmoxMCP Project Purpose

## Overview
ProxmoxMCP is a Python-based Model Context Protocol (MCP) server that provides a clean interface for interacting with Proxmox Virtual Environment (VE) hypervisors. It enables management of nodes, VMs, containers, and storage through the MCP protocol.

## Key Features
- **MCP Protocol Compliance**: Built with the official MCP SDK for standardized tool interfaces
- **Secure Authentication**: Token-based authentication with Proxmox API
- **VM Management**: Tools for managing virtual machines, including console command execution
- **Node Operations**: Cluster node management and status monitoring  
- **Storage Management**: Storage pool information and monitoring
- **Container Support**: LXC container management capabilities
- **Rich Formatting**: Customizable output themes with emojis and color support
- **Docker Support**: Containerized deployment with security best practices

## Target Users
- System administrators managing Proxmox environments
- DevOps engineers automating virtualization tasks
- Developers building tools on top of Proxmox API
- Claude Code users seeking Proxmox integration

## Architecture
The project follows a modular architecture with:
- Core Proxmox API integration layer
- MCP tool implementations for different resource types
- Rich formatting system for consistent output
- Configuration management with encryption support
- Comprehensive error handling and logging