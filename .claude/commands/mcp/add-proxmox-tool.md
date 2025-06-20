Add new Proxmox MCP tool: $ARGUMENTS

Follow the established patterns in your ProxmoxMCP architecture:

1. Analyze the requested functionality and determine appropriate tool category
2. Create the new tool in the appropriate tools/ subdirectory (vm.py, storage.py, etc.)
3. Use Pydantic models for request/response validation following existing patterns
4. Implement Rich formatted output using the formatting/ module standards
5. Add comprehensive error handling with ProxmoxManager patterns
6. Write tests following the project's testing conventions
7. Update tool registration in server.py
8. Update CLAUDE.md documentation if this adds new capabilities

Ensure the tool follows all project coding standards from CLAUDE.md.
