---
name: Performance Issue
about: Report performance problems with ProxmoxMCP
title: '[PERFORMANCE] '
labels: performance, needs-investigation
assignees: ''
---

## Performance Issue Description
<!-- A clear and concise description of the performance problem -->

## Performance Metrics
<!-- Please provide specific metrics where possible -->

### Response Times

- **Expected Response Time**: <!-- e.g., < 2 seconds -->
- **Actual Response Time**: <!-- e.g., 15-30 seconds -->
- **Tool/Operation Affected**: <!-- e.g., get_vms, execute_vm_command -->

### Resource Usage

- **CPU Usage**: <!-- e.g., High/Normal/Low -->
- **Memory Usage**: <!-- e.g., 500MB, increasing over time -->
- **Network Latency**: <!-- e.g., 50ms to Proxmox server -->

## Environment Details

- **ProxmoxMCP Version**: <!-- e.g., 1.0.0 -->
- **Proxmox Version**: <!-- e.g., 7.4-3 -->
- **Python Version**: <!-- e.g., 3.10.4 -->
- **Deployment Method**: <!-- e.g., Docker, pip install, development -->
- **Operating System**: <!-- e.g., Ubuntu 22.04, Windows 11 -->
- **Hardware**: <!-- e.g., 4 CPU cores, 8GB RAM -->

## Proxmox Environment

- **Number of Nodes**: <!-- e.g., 3 -->
- **Total VMs**: <!-- e.g., 25 -->
- **Total Containers**: <!-- e.g., 10 -->
- **Network Setup**: <!-- e.g., Local network, VPN, WAN -->
- **Proxmox Load**: <!-- e.g., Normal operation, High CPU usage -->

## Steps to Reproduce
<!-- Detailed steps to reproduce the performance issue -->
1.
2.
3.

## Performance Impact
<!-- How does this affect your usage? -->
- [ ] Cannot use the tool at all
- [ ] Significantly slows down workflow
- [ ] Occasional delays but usable
- [ ] Minor inconvenience

## Frequency

- [ ] Always occurs
- [ ] Occurs most of the time (>75%)
- [ ] Occurs sometimes (25-75%)
- [ ] Occurs rarely (<25%)

## Additional Performance Data
<!-- Include any additional performance data you have -->

### Logs
<!-- Include relevant log entries showing timing or performance issues -->
```
Paste logs here
```

### Network Analysis
<!-- If network-related, include traceroute, ping times, etc. -->
```
Paste network diagnostics here
```

### Profiling Data
<!-- If you have profiling data, include it here -->
```
Paste profiling data here
```

## Workarounds
<!-- Any workarounds you've found -->

## Possible Causes
<!-- If you suspect specific causes, list them here -->
- [ ] Network latency to Proxmox server
- [ ] Large number of VMs/containers
- [ ] Proxmox server performance
- [ ] ProxmoxMCP inefficient API calls
- [ ] Memory leaks
- [ ] Database/cache issues
- [ ] Other:

## Additional Context
<!-- Add any other context about the performance issue -->

## Benchmarking
<!-- If you've done any benchmarking, include results -->
- **Baseline Performance**: <!-- Performance in ideal conditions -->
- **Current Performance**: <!-- Current degraded performance -->
- **Performance Regression**: <!-- When did you first notice the issue? -->
