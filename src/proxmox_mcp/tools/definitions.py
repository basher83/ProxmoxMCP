"""
Tool descriptions for Proxmox MCP tools.
"""

# Node tool descriptions
GET_NODES_DESC = """List all nodes in the Proxmox cluster with their status, CPU, memory, 
and role information.

Example:
{"node": "pve1", "status": "online", "cpu_usage": 0.15, 
"memory": {"used": "8GB", "total": "32GB"}}"""

GET_NODE_STATUS_DESC = """Get detailed status information for a specific Proxmox node.

Parameters:
node* - Name/ID of node to query (e.g. 'pve1')

Example:
{"cpu": {"usage": 0.15}, "memory": {"used": "8GB", "total": "32GB"}}"""

# VM tool descriptions
GET_VMS_DESC = """List all virtual machines across the cluster with their status and resource usage.

Example:
{"vmid": "100", "name": "ubuntu", "status": "running", "cpu": 2, "memory": 4096}"""

EXECUTE_VM_COMMAND_DESC = """Execute commands in a VM via QEMU guest agent.

Parameters:
node* - Host node name (e.g. 'pve1')
vmid* - VM ID number (e.g. '100')
command* - Shell command to run (e.g. 'uname -a')

Example:
{"success": true, "output": "Linux vm1 5.4.0", "exit_code": 0}"""

# Container tool descriptions
GET_CONTAINERS_DESC = """List all LXC containers across the cluster with their status 
and configuration.

Example:
{"vmid": "200", "name": "nginx", "status": "running", "template": "ubuntu-20.04"}"""

# Storage tool descriptions
GET_STORAGE_DESC = """List storage pools across the cluster with their usage and configuration.

Example:
{"storage": "local-lvm", "type": "lvm", "used": "500GB", "total": "1TB"}"""

# Cluster tool descriptions
GET_CLUSTER_STATUS_DESC = """Get overall Proxmox cluster health and configuration status.

Example:
{"name": "proxmox", "quorum": "ok", "nodes": 3, "ha_status": "active"}"""

# AI Diagnostic tool descriptions
ANALYZE_CLUSTER_HEALTH_DESC = """AI-powered comprehensive cluster health analysis using Claude Code SDK.

Analyzes all cluster components (nodes, VMs, storage, network) and provides intelligent 
insights, recommendations, and actionable solutions for:
- Performance bottlenecks and optimization opportunities
- Security concerns and hardening recommendations  
- Capacity planning and resource utilization analysis
- Critical issues requiring immediate attention
- Long-term maintenance recommendations

Returns detailed AI analysis with prioritized action items, specific configuration 
changes, and implementation guidance.

Example output includes performance metrics, security assessments, and optimization 
recommendations with expected impact and implementation complexity."""

DIAGNOSE_VM_ISSUES_DESC = """AI-powered VM issue diagnosis and troubleshooting using Claude Code SDK.

Parameters:
node* - Proxmox node name hosting the VM (e.g. 'pve1')
vmid* - Virtual machine ID to diagnose (e.g. '100')

Performs comprehensive VM analysis including:
- Performance issues and resource constraints
- Configuration problems and optimization opportunities
- Network connectivity troubleshooting
- Storage performance analysis
- Guest OS issues (when guest agent available)
- Hardware compatibility concerns

Returns detailed diagnostic report with root cause analysis, specific solution steps, 
implementation commands, and prevention measures.

Example:
{"vm": "100", "issues": ["High CPU usage", "Network latency"], "solutions": [...]}"""

SUGGEST_RESOURCE_OPTIMIZATION_DESC = """AI-powered resource optimization recommendations using Claude Code SDK.

Analyzes cluster-wide resource utilization patterns and provides intelligent 
recommendations for:
- Overprovisioned VMs that can be downsized
- Underutilized nodes that could host additional workloads
- Storage optimization (thin provisioning, compression, deduplication)
- Network optimization and traffic analysis
- Cost-saving opportunities with ROI calculations
- Performance improvement strategies

Returns comprehensive optimization report with specific configuration changes, 
expected resource savings, implementation complexity ratings, and success metrics.

Example output includes resource reallocation suggestions, performance improvements, 
and cost optimization with quantified benefits."""

ANALYZE_SECURITY_POSTURE_DESC = """AI-powered security posture analysis using Claude Code SDK.

Performs comprehensive security assessment of the Proxmox environment including:
- Authentication and access control evaluation
- Network security configuration review
- VM isolation and security group analysis
- Backup and disaster recovery security assessment
- Compliance with security frameworks (SOC2, ISO27001)
- Potential attack vectors and threat analysis
- Encryption and data protection measures
- Audit logging and monitoring capabilities

Returns detailed security analysis with risk-prioritized recommendations, specific 
remediation steps, compliance implications, and implementation guidance.

Example output includes security findings by risk level, remediation commands, 
and prevention strategies with compliance mapping."""
