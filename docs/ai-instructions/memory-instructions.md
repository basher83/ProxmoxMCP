# Memory Management Instructions

The Serena MCP server provides memory management tools for storing and retrieving
project-specific knowledge and coding patterns.

## Available Memory Tools

### `mcp__serena__write_memory`

Store project information that can be useful for future tasks.

**Parameters:**

- `memory_name`: Meaningful name that describes the content
- `content`: Information to store (use markdown formatting)

**Usage Guidelines:**

- Keep information short and to the point
- Use meaningful memory names for easy identification
- Better to have multiple small memories than one large one
- Only read relevant memories for the current task

### `mcp__serena__read_memory`

Read the content of a memory file.

**Parameters:**

- `memory_file_name`: Name of the memory file to read
- `max_answer_chars`: Maximum characters to return (default: 200000)

**Usage Guidelines:**

- Only read memories relevant to the current task
- Infer relevance from the memory file name
- Don't read the same memory multiple times in the same conversation

### `mcp__serena__list_memories`

List all available memories.

**Usage Guidelines:**

- Use to discover what memories are available
- Review memory names to find relevant information
- Use before writing new memories to avoid duplicates

### `mcp__serena__delete_memory`

Delete a memory file.

**Parameters:**

- `memory_file_name`: Name of the memory file to delete

**Usage Guidelines:**

- Only delete when explicitly requested by user
- Delete when information is no longer correct or relevant

## Memory Management Workflow

### 1. Starting a Task

- Use `mcp__serena__list_memories` to see available memories
- Read relevant memories using `mcp__serena__read_memory`
- Determine what information might be useful for the task

### 2. During Task Execution

- Capture new learnings and patterns as they emerge
- Document important decisions and their rationale
- Store successful implementation approaches

### 3. After Task Completion

- Use `mcp__serena__write_memory` to capture:
  - New coding patterns discovered
  - Architectural decisions made
  - Security best practices learned
  - Configuration approaches that work
  - Integration patterns that are effective

## When to Write Memory

Write memory in these scenarios:

- **After resolving complex technical issues** - Document solution approach and decision rationale
- **When implementing new architectural patterns** - Store complete implementation context
- **Following security implementations** - Capture security best practices and validation methods
- **After performance optimizations** - Document performance patterns and measurement approaches
- **When discovering integration patterns** - Store MCP protocol and Proxmox API integration insights

## Memory Content Guidelines

### Structure

Use clear markdown formatting with:

- Descriptive headings
- Code examples with proper syntax highlighting
- Context about when and why to use patterns
- Dependencies and requirements
- Examples of successful implementation

### Content Types

- **Implementation Patterns**: Complete code examples with context
- **Configuration Approaches**: Working configuration patterns
- **Security Practices**: Validated security implementation methods
- **Integration Methods**: Successful API and protocol integration patterns
- **Troubleshooting Guides**: Common problems and their solutions

## Example Usage

```markdown
# Writing a new memory
mcp__serena__write_memory(
    memory_name="proxmox-api-authentication-patterns",
    content="""
    # ProxmoxMCP API Authentication Patterns
    
    ## Token-based Authentication
    ```python
    # Successful pattern for API token auth
    config = {
        "host": "proxmox.example.com",
        "user": "api-user@pam",
        "token_name": "api-token",
        "token_value": "secret-token-value"
    }
    ```
    
    ## Error Handling
    - Always validate tokens before use
    - Implement retry logic for network timeouts
    - Log authentication failures (without exposing credentials)
    """
)
```

## Integration with Development Workflow

- **Pre-Work**: Always check existing memories for relevant patterns
- **During Work**: Document new discoveries and successful approaches
- **Post-Work**: Update memories with new insights and learnings
- **Regular Maintenance**: Review and update memories to keep them current
