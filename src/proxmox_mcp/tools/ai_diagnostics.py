"""
AI-powered diagnostic tools for ProxmoxMCP using Claude Code SDK.

This module provides intelligent diagnostic capabilities by integrating Claude Code SDK
with Proxmox infrastructure data. It offers four main diagnostic tools:

1. Cluster Health Analysis - Comprehensive cluster health assessment
2. VM Issue Diagnosis - Specific VM problem diagnosis and solutions
3. Resource Optimization - AI-powered resource usage optimization recommendations
4. Security Posture Analysis - Security configuration analysis and recommendations

All tools inherit from the ProxmoxTool base class and follow existing patterns for
error handling, logging, and output formatting.
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional

from mcp.types import TextContent as Content
from proxmoxer import ProxmoxAPI

from .base import ProxmoxTool

try:
    from claude_code_sdk import query, ClaudeCodeOptions

    CLAUDE_SDK_AVAILABLE = True
except ImportError:
    CLAUDE_SDK_AVAILABLE = False
    logging.warning(
        "Claude Code SDK not available. AI diagnostic features will be disabled."
    )


class AIProxmoxDiagnostics(ProxmoxTool):
    """AI-powered diagnostic tools using Claude Code SDK.

    This class provides intelligent analysis of Proxmox infrastructure using
    Claude Code SDK for advanced insights and recommendations. It includes
    comprehensive data collection, AI analysis, and formatted output generation.

    Features:
    - Cluster health analysis with actionable insights
    - VM-specific issue diagnosis and troubleshooting
    - Resource optimization recommendations
    - Security posture analysis and improvements

    All methods are async and handle errors gracefully, falling back to
    basic analysis when Claude Code SDK is unavailable.
    """

    def __init__(self, proxmox_api: ProxmoxAPI):
        """Initialize AI diagnostics tool.

        Args:
            proxmox_api: Initialized ProxmoxAPI instance for data collection
        """
        super().__init__(proxmox_api)
        self.claude_available = CLAUDE_SDK_AVAILABLE

        if self.claude_available:
            self.claude_options = ClaudeCodeOptions(
                system_prompt="""You are an expert Proxmox VE administrator and infrastructure analyst. 
                Analyze the provided Proxmox data and provide actionable insights, recommendations, 
                and solutions. Focus on performance, security, and best practices.
                
                Always provide:
                1. Clear, prioritized recommendations
                2. Specific configuration changes or commands when applicable
                3. Expected impact and benefits
                4. Risk assessment for suggested changes
                5. Implementation timeline and difficulty level
                
                Format responses with clear sections and bullet points for easy reading.""",
                max_turns=1,
            )
        else:
            self.claude_options = None
            self.logger.warning("Claude Code SDK unavailable - AI features disabled")

    async def analyze_cluster_health(self) -> List[Content]:
        """Analyze overall cluster health using AI insights.

        Collects comprehensive cluster data including nodes, VMs, storage,
        and cluster status, then uses Claude Code SDK to provide intelligent
        analysis and recommendations.

        Returns:
            List[Content]: Formatted cluster health analysis with recommendations
        """
        try:
            self.logger.info("Starting AI cluster health analysis")

            # Gather comprehensive cluster data
            cluster_data = await self._collect_cluster_metrics()

            if not self.claude_available:
                return await self._basic_cluster_analysis(cluster_data)

            # Use Claude Code SDK for intelligent analysis
            analysis_prompt = f"""
            Analyze this Proxmox cluster data and provide a comprehensive health assessment:
            
            {json.dumps(cluster_data, indent=2)}
            
            Please provide:
            1. Overall health status and critical issues (High/Medium/Low priority)
            2. Performance bottlenecks and optimization recommendations
            3. Security concerns and suggestions
            4. Capacity planning insights and resource utilization analysis
            5. Immediate action items prioritized by urgency
            6. Long-term maintenance recommendations
            
            Focus on actionable insights with specific commands or configuration changes where applicable.
            """

            ai_response = await self._query_claude(analysis_prompt)

            formatted_response = f"""🤖 **AI Cluster Health Analysis**

{ai_response}

---
📊 **Analysis Summary**
- Nodes analyzed: {len(cluster_data.get('nodes', []))}
- VMs analyzed: {len(cluster_data.get('vms', []))}
- Storage pools: {len(cluster_data.get('storage', []))}
- Analysis powered by Claude Code SDK with Proxmox expertise

💡 **Next Steps**: Review high-priority recommendations first, then implement suggested optimizations during maintenance windows.
            """

            return [Content(type="text", text=formatted_response)]

        except Exception as e:
            self._handle_error("AI cluster health analysis", e)
            return [
                Content(
                    type="text",
                    text="❌ AI cluster analysis failed. Please check logs for details.",
                )
            ]

    async def diagnose_vm_issues(self, node: str, vmid: str) -> List[Content]:
        """Diagnose specific VM issues using AI analysis.

        Collects detailed VM diagnostic data including configuration, status,
        performance metrics, and logs, then provides AI-powered diagnosis
        and solution recommendations.

        Args:
            node: Proxmox node name hosting the VM
            vmid: Virtual machine ID to diagnose

        Returns:
            List[Content]: Detailed VM diagnostic report with solutions
        """
        try:
            self.logger.info(f"Starting AI VM diagnosis for VM {vmid} on node {node}")

            # Gather VM-specific diagnostic data
            vm_data = await self._collect_vm_diagnostics(node, vmid)

            if not self.claude_available:
                return await self._basic_vm_analysis(vm_data, node, vmid)

            diagnosis_prompt = f"""
            Diagnose issues with this Proxmox VM and provide specific solutions:
            
            VM ID: {vmid}
            Node: {node}
            Diagnostic Data: {json.dumps(vm_data, indent=2)}
            
            Analyze and provide solutions for:
            1. Performance issues and resource constraints
            2. Configuration problems and optimization opportunities
            3. Network connectivity issues
            4. Storage performance problems
            5. Guest OS issues (if data available)
            6. Hardware compatibility concerns
            
            For each issue found, provide:
            - Problem description and root cause
            - Specific solution steps with commands
            - Expected resolution time
            - Prevention measures for the future
            """

            ai_response = await self._query_claude(diagnosis_prompt)

            vm_status = vm_data.get("status", {})
            formatted_response = f"""🔧 **AI VM Diagnostic Report - VM {vmid}**

**VM Overview**
- Node: {node}
- Status: {vm_status.get('status', 'unknown')}
- CPU Cores: {vm_status.get('cpus', 'N/A')}
- Memory: {vm_status.get('maxmem', 'N/A')} bytes
- Uptime: {vm_status.get('uptime', 'N/A')} seconds

**AI Analysis & Recommendations**

{ai_response}

---
💡 **Diagnostic powered by Claude Code SDK with Proxmox expertise**
🔍 **VM Configuration**: Review VM configuration file for additional optimization opportunities
⚠️  **Safety**: Test configuration changes in a non-production environment first
            """

            return [Content(type="text", text=formatted_response)]

        except Exception as e:
            self._handle_error(f"AI VM diagnosis for VM {vmid}", e)
            return [
                Content(
                    type="text",
                    text=f"❌ AI VM diagnosis failed for VM {vmid}. Please check logs for details.",
                )
            ]

    async def suggest_resource_optimization(self) -> List[Content]:
        """Provide AI-powered resource optimization recommendations.

        Analyzes cluster resource utilization patterns and provides intelligent
        recommendations for optimizing CPU, memory, storage, and network resources.

        Returns:
            List[Content]: Comprehensive resource optimization recommendations
        """
        try:
            self.logger.info("Starting AI resource optimization analysis")

            # Collect resource utilization data
            resource_data = await self._collect_resource_metrics()

            if not self.claude_available:
                return await self._basic_resource_analysis(resource_data)

            optimization_prompt = f"""
            Analyze this Proxmox resource utilization data and suggest optimizations:
            
            {json.dumps(resource_data, indent=2)}
            
            Provide optimization recommendations for:
            1. Overprovisioned VMs that can be downsized (with specific recommendations)
            2. Underutilized nodes that could host more VMs
            3. Storage optimization opportunities (thin provisioning, compression, etc.)
            4. Network optimization suggestions
            5. Cost-saving recommendations and ROI calculations
            6. Performance improvement strategies
            7. Resource allocation best practices
            
            For each recommendation, include:
            - Specific configuration changes needed
            - Expected resource savings or performance improvements
            - Implementation complexity (Easy/Medium/Hard)
            - Risk level and mitigation strategies
            - Monitoring metrics to track success
            """

            ai_response = await self._query_claude(optimization_prompt)

            resource_summary = resource_data.get("resource_summary", {})
            formatted_response = f"""⚡ **AI Resource Optimization Report**

**Current Resource Overview**
- Total CPU Cores: {resource_summary.get('total_cpu_cores', 'N/A')}
- Total Memory: {self._format_bytes(resource_summary.get('total_memory', 0))}
- Memory Utilization: {resource_summary.get('memory_utilization_percent', 0):.1f}%
- Active VMs: {len(resource_data.get('vms', []))}

**AI Optimization Recommendations**

{ai_response}

---
📈 **Optimization Analysis powered by Claude Code SDK**
📊 **Implementation**: Start with "Easy" recommendations for quick wins
⚠️  **Testing**: Validate changes in staging environment before production
🔄 **Monitoring**: Set up alerts to track optimization success metrics
            """

            return [Content(type="text", text=formatted_response)]

        except Exception as e:
            self._handle_error("AI resource optimization analysis", e)
            return [
                Content(
                    type="text",
                    text="❌ AI resource optimization analysis failed. Please check logs for details.",
                )
            ]

    async def analyze_security_posture(self) -> List[Content]:
        """Analyze cluster security posture using AI.

        Evaluates security configuration across the cluster including authentication,
        network security, access controls, and compliance with security best practices.

        Returns:
            List[Content]: Comprehensive security analysis and recommendations
        """
        try:
            self.logger.info("Starting AI security posture analysis")

            # Collect security-relevant data
            security_data = await self._collect_security_metrics()

            if not self.claude_available:
                return await self._basic_security_analysis(security_data)

            security_prompt = f"""
            Perform a comprehensive security analysis of this Proxmox environment:
            
            {json.dumps(security_data, indent=2)}
            
            Analyze and provide recommendations for:
            1. Authentication and access control weaknesses
            2. Network security configuration issues
            3. VM isolation and security groups
            4. Backup and disaster recovery security
            5. Compliance with security frameworks (SOC2, ISO27001, etc.)
            6. Potential attack vectors and mitigations
            7. Encryption and data protection measures
            8. Audit logging and monitoring gaps
            
            For each security finding, provide:
            - Risk level (Critical/High/Medium/Low)
            - Potential impact if exploited
            - Specific remediation steps with commands
            - Prevention and detection strategies
            - Compliance implications
            """

            ai_response = await self._query_claude(security_prompt)

            user_count = len(security_data.get("users", []))
            formatted_response = f"""🔒 **AI Security Posture Analysis**

**Security Overview**
- User Accounts: {user_count}
- Firewall Status: {security_data.get('firewall_options', {}).get('enable', 'Unknown')}
- Datacenter Config: {'Available' if security_data.get('datacenter_config') else 'Limited'}

**AI Security Assessment**

{ai_response}

---
🛡️  **Security Analysis powered by Claude Code SDK with cybersecurity expertise**
🔐 **Priority**: Address Critical and High-risk items immediately
📋 **Compliance**: Review recommendations against your organization's security policies
🔍 **Audit**: Implement continuous security monitoring for ongoing protection
            """

            return [Content(type="text", text=formatted_response)]

        except Exception as e:
            self._handle_error("AI security posture analysis", e)
            return [
                Content(
                    type="text",
                    text="❌ AI security analysis failed. Please check logs for details.",
                )
            ]

    async def _query_claude(self, prompt: str) -> str:
        """Query Claude Code SDK with error handling and streaming.

        Args:
            prompt: Analysis prompt to send to Claude

        Returns:
            str: AI-generated response text
        """
        if not self.claude_available:
            raise RuntimeError("Claude Code SDK not available")

        try:
            ai_response = ""
            async for message in query(prompt=prompt, options=self.claude_options):
                if hasattr(message, "content"):
                    for block in message.content:
                        if hasattr(block, "text"):
                            ai_response += block.text

            return ai_response.strip() if ai_response else "No response generated"

        except Exception as e:
            self.logger.error(f"Claude Code SDK query failed: {e}")
            raise RuntimeError(f"AI analysis failed: {e}")

    async def _collect_cluster_metrics(self) -> Dict[str, Any]:
        """Collect comprehensive cluster metrics for AI analysis.

        Returns:
            Dict[str, Any]: Complete cluster state including nodes, VMs, storage
        """
        data: Dict[str, Any] = {}

        try:
            # Collect node information
            nodes = self.proxmox.nodes.get()
            data["nodes"] = []
            for node in nodes:
                try:
                    node_status = self.proxmox.nodes(node["node"]).status.get()
                    data["nodes"].append(
                        {
                            "name": node["node"],
                            "status": node["status"],
                            "cpu_usage": node_status.get("cpu", 0),
                            "memory_usage": node_status.get("memory", {}),
                            "uptime": node_status.get("uptime", 0),
                            "load_average": node_status.get("loadavg", []),
                            "cpu_info": node_status.get("cpuinfo", {}),
                            "kernel_version": node_status.get("kversion", "unknown"),
                        }
                    )
                except Exception as e:
                    self.logger.warning(
                        f"Failed to get status for node {node['node']}: {e}"
                    )
                    data["nodes"].append(
                        {
                            "name": node["node"],
                            "status": node.get("status", "unknown"),
                            "error": str(e),
                        }
                    )

            # Collect VM information
            data["vms"] = []
            for node in nodes:
                try:
                    vms = self.proxmox.nodes(node["node"]).qemu.get()
                    for vm in vms:
                        vm_info = {
                            "vmid": vm["vmid"],
                            "name": vm.get("name", "unnamed"),
                            "node": node["node"],
                            "status": vm["status"],
                            "cpu_usage": vm.get("cpu", 0),
                            "memory_usage": vm.get("mem", 0),
                            "max_memory": vm.get("maxmem", 0),
                            "disk_read": vm.get("diskread", 0),
                            "disk_write": vm.get("diskwrite", 0),
                            "network_in": vm.get("netin", 0),
                            "network_out": vm.get("netout", 0),
                        }
                        data["vms"].append(vm_info)
                except Exception as e:
                    self.logger.warning(
                        f"Failed to get VMs for node {node['node']}: {e}"
                    )

            # Collect storage information
            try:
                storage = self.proxmox.storage.get()
                data["storage"] = storage
            except Exception as e:
                self.logger.warning(f"Failed to get storage information: {e}")
                data["storage"] = []

            # Collect cluster status
            try:
                cluster_status = self.proxmox.cluster.status.get()
                data["cluster_status"] = cluster_status
            except Exception as e:
                self.logger.warning(f"Failed to get cluster status: {e}")
                data["cluster_status"] = []

        except Exception as e:
            self.logger.error(f"Failed to collect cluster metrics: {e}")
            raise

        return data

    async def _collect_vm_diagnostics(self, node: str, vmid: str) -> Dict[str, Any]:
        """Collect detailed VM diagnostic data.

        Args:
            node: Proxmox node name
            vmid: VM ID to analyze

        Returns:
            Dict[str, Any]: Comprehensive VM diagnostic information
        """
        data: Dict[str, Any] = {}

        try:
            # VM status and configuration
            vm_status = self.proxmox.nodes(node).qemu(vmid).status.current.get()
            vm_config = self.proxmox.nodes(node).qemu(vmid).config.get()

            data["status"] = vm_status
            data["config"] = vm_config

            # Try to get VM statistics if running
            if vm_status.get("status") == "running":
                try:
                    # Get RRD data for performance metrics
                    rrd_data = (
                        self.proxmox.nodes(node).qemu(vmid).rrd.get(timeframe="hour")
                    )
                    data["performance_metrics"] = rrd_data
                except Exception as e:
                    self.logger.warning(
                        f"Failed to get performance metrics for VM {vmid}: {e}"
                    )
                    data["performance_metrics"] = None

                # Try to get guest agent info if available
                try:
                    agent_info = self.proxmox.nodes(node).qemu(vmid).agent.info.get()
                    data["guest_agent"] = agent_info
                except Exception as e:
                    self.logger.debug(f"Guest agent not available for VM {vmid}: {e}")
                    data["guest_agent"] = None

            # Get VM snapshots
            try:
                snapshots = self.proxmox.nodes(node).qemu(vmid).snapshot.get()
                data["snapshots"] = snapshots
            except Exception as e:
                self.logger.warning(f"Failed to get snapshots for VM {vmid}: {e}")
                data["snapshots"] = []

        except Exception as e:
            self.logger.error(f"Failed to collect VM diagnostics for {vmid}: {e}")
            raise

        return data

    async def _collect_resource_metrics(self) -> Dict[str, Any]:
        """Collect resource utilization metrics for optimization analysis.

        Returns:
            Dict[str, Any]: Resource utilization data with calculations
        """
        # Start with cluster metrics
        data = await self._collect_cluster_metrics()

        # Add resource utilization calculations
        nodes = data.get("nodes", [])
        total_cpu_cores = 0
        total_memory = 0
        used_memory = 0

        for node in nodes:
            if "error" not in node:
                cpu_info = node.get("cpu_info", {})
                total_cpu_cores += cpu_info.get("cpus", 0)

                memory_info = node.get("memory_usage", {})
                node_total_mem = memory_info.get("total", 0)
                node_used_mem = memory_info.get("used", 0)

                total_memory += node_total_mem
                used_memory += node_used_mem

        data["resource_summary"] = {
            "total_cpu_cores": total_cpu_cores,
            "total_memory": total_memory,
            "used_memory": used_memory,
            "memory_utilization_percent": (
                (used_memory / total_memory * 100) if total_memory > 0 else 0
            ),
            "total_vms": len(data.get("vms", [])),
            "running_vms": len(
                [vm for vm in data.get("vms", []) if vm.get("status") == "running"]
            ),
        }

        return data

    async def _collect_security_metrics(self) -> Dict[str, Any]:
        """Collect security-relevant configuration data.

        Returns:
            Dict[str, Any]: Security configuration and status information
        """
        data: Dict[str, Any] = {}

        # Get user and permission information
        try:
            users = self.proxmox.access.users.get()
            data["users"] = users
        except Exception as e:
            self.logger.warning(f"Failed to get user information: {e}")
            data["users"] = []

        # Get datacenter configuration
        try:
            datacenter_config = self.proxmox.cluster.datacenter.get()
            data["datacenter_config"] = datacenter_config
        except Exception as e:
            self.logger.warning(f"Failed to get datacenter configuration: {e}")
            data["datacenter_config"] = {}

        # Get firewall configuration if available
        try:
            firewall_options = self.proxmox.cluster.firewall.options.get()
            data["firewall_options"] = firewall_options
        except Exception as e:
            self.logger.warning(f"Failed to get firewall options: {e}")
            data["firewall_options"] = {}

        # Get cluster information
        try:
            cluster_info = self.proxmox.cluster.status.get()
            data["cluster_info"] = cluster_info
        except Exception as e:
            self.logger.warning(f"Failed to get cluster info: {e}")
            data["cluster_info"] = []

        return data

    async def _basic_cluster_analysis(
        self, cluster_data: Dict[str, Any]
    ) -> List[Content]:
        """Provide basic cluster analysis when Claude SDK is unavailable."""
        nodes = cluster_data.get("nodes", [])
        vms = cluster_data.get("vms", [])
        storage = cluster_data.get("storage", [])

        analysis = f"""📊 **Basic Cluster Analysis** (AI features unavailable)

**Cluster Overview:**
- Nodes: {len(nodes)} total
- VMs: {len(vms)} total
- Storage pools: {len(storage)}

**Node Status:**
"""

        for node in nodes:
            if "error" not in node:
                cpu_usage = node.get("cpu_usage", 0) * 100
                memory_info = node.get("memory_usage", {})
                memory_used = memory_info.get("used", 0)
                memory_total = memory_info.get("total", 1)
                memory_percent = (
                    (memory_used / memory_total) * 100 if memory_total > 0 else 0
                )

                analysis += f"- {node['name']}: {node['status']} | CPU: {cpu_usage:.1f}% | Memory: {memory_percent:.1f}%\n"
            else:
                analysis += f"- {node['name']}: Error - {node['error']}\n"

        analysis += f"""
**VM Status Summary:**
- Running: {len([vm for vm in vms if vm.get('status') == 'running'])}
- Stopped: {len([vm for vm in vms if vm.get('status') == 'stopped'])}
- Other: {len([vm for vm in vms if vm.get('status') not in ['running', 'stopped']])}

ℹ️ For detailed AI-powered analysis, please install and configure Claude Code SDK.
"""

        return [Content(type="text", text=analysis)]

    async def _basic_vm_analysis(
        self, vm_data: Dict[str, Any], node: str, vmid: str
    ) -> List[Content]:
        """Provide basic VM analysis when Claude SDK is unavailable."""
        status = vm_data.get("status", {})
        config = vm_data.get("config", {})

        analysis = f"""🔧 **Basic VM Analysis** (AI features unavailable)

**VM {vmid} on {node}:**
- Status: {status.get('status', 'unknown')}
- CPU: {status.get('cpus', 'N/A')} cores
- Memory: {self._format_bytes(status.get('maxmem', 0))}
- Uptime: {status.get('uptime', 'N/A')} seconds

**Configuration:**
- Boot disk: {config.get('bootdisk', 'N/A')}
- Network: {len([k for k in config.keys() if k.startswith('net')])} interface(s)
- OS Type: {config.get('ostype', 'N/A')}

ℹ️ For detailed AI-powered diagnosis, please install and configure Claude Code SDK.
"""

        return [Content(type="text", text=analysis)]

    async def _basic_resource_analysis(
        self, resource_data: Dict[str, Any]
    ) -> List[Content]:
        """Provide basic resource analysis when Claude SDK is unavailable."""
        summary = resource_data.get("resource_summary", {})

        analysis = f"""⚡ **Basic Resource Analysis** (AI features unavailable)

**Resource Summary:**
- Total CPU Cores: {summary.get('total_cpu_cores', 'N/A')}
- Total Memory: {self._format_bytes(summary.get('total_memory', 0))}
- Memory Utilization: {summary.get('memory_utilization_percent', 0):.1f}%
- Total VMs: {summary.get('total_vms', 0)}
- Running VMs: {summary.get('running_vms', 0)}

**Basic Recommendations:**
- Monitor memory usage if above 80%
- Review VM resource allocation for optimization opportunities
- Consider load balancing if node utilization varies significantly

ℹ️ For detailed AI-powered optimization recommendations, please install and configure Claude Code SDK.
"""

        return [Content(type="text", text=analysis)]

    async def _basic_security_analysis(
        self, security_data: Dict[str, Any]
    ) -> List[Content]:
        """Provide basic security analysis when Claude SDK is unavailable."""
        users = security_data.get("users", [])
        firewall = security_data.get("firewall_options", {})

        analysis = f"""🔒 **Basic Security Analysis** (AI features unavailable)

**Security Overview:**
- User accounts: {len(users)}
- Firewall enabled: {firewall.get('enable', 'Unknown')}

**Basic Security Checklist:**
- ✓ Review user accounts and remove unused accounts
- ✓ Enable firewall if not already enabled
- ✓ Use strong passwords and consider two-factor authentication
- ✓ Regular security updates and patches
- ✓ Monitor access logs for suspicious activity

ℹ️ For detailed AI-powered security analysis, please install and configure Claude Code SDK.
"""

        return [Content(type="text", text=analysis)]

    def _format_bytes(self, bytes_value: int) -> str:
        """Format bytes into human-readable format."""
        if bytes_value == 0:
            return "0 B"

        units = ["B", "KB", "MB", "GB", "TB"]
        unit_index = 0
        size = float(bytes_value)

        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024
            unit_index += 1

        return f"{size:.1f} {units[unit_index]}"
