# ProxmoxMCP Development Guidelines

## Architecture Principles

### MCP Protocol Compliance
- All new tools must follow MCP protocol standards
- Use FastMCP patterns for tool registration
- Implement proper tool descriptions in `tools/definitions.py`
- Maintain consistent request/response patterns

### ProxmoxMCP-Specific Patterns
- **Inherit from ProxmoxTool**: All tools inherit from base classes in `tools/base.py`
- **Pydantic Validation**: Use Pydantic models for all configuration and API parameters
- **Rich Formatting**: Implement consistent formatting via ProxmoxTheme and ProxmoxFormatters
- **Error Handling**: Comprehensive error handling with specific exception types
- **Async Support**: Use proper async patterns for VM operations

### Security Best Practices
- **No Secrets in Code**: Use environment variables or encrypted configuration
- **Input Validation**: Validate all user inputs and API parameters
- **Secure Authentication**: Token-based authentication with Proxmox API
- **Encryption Support**: Use cryptography library for sensitive data
- **Docker Security**: Run containers as non-root user

## Coding Standards

### Type Safety
- Type hints required for all functions and methods
- Strict mypy configuration must pass without errors
- Use Pydantic models for data validation
- Proper async type annotations for coroutines

### Documentation Requirements
- Comprehensive module docstrings explaining purpose and key features
- Class docstrings describing responsibility and usage patterns
- Method documentation with Args, Returns, Raises where applicable
- Tool descriptions for MCP tool registration

### Testing Requirements
- Comprehensive test coverage for new functionality
- Mock Proxmox API calls to avoid live server dependencies
- Test error conditions and edge cases
- Follow existing test patterns from the test suite

## Component-Specific Guidelines

### Server Component (`server.py`)
- Follow FastMCP patterns for tool registration
- Maintain clean dependency injection
- Add proper signal handling for new services
- Update tool descriptions in imports

### Tools Component (`tools/`)
- Inherit from ProxmoxTool base class
- Use consistent error handling patterns
- Implement rich formatting via templates
- Add tool descriptions to `definitions.py`

### Configuration (`config/`)
- Use Pydantic models for validation
- Support environment variable fallbacks
- Maintain backward compatibility
- Add field documentation

### Formatting (`formatting/`)
- Use ProxmoxTheme for consistent styling
- Add reusable formatting functions
- Support emoji and color toggles
- Follow existing template patterns

## Development Workflow

### Before Starting
1. Review existing patterns in similar components
2. Check memory for relevant coding preferences
3. Understand MCP protocol requirements
4. Plan for backward compatibility

### During Development
1. Follow type-safe implementation practices
2. Add comprehensive error handling
3. Implement proper logging
4. Write tests alongside implementation

### Before Completion
1. Run complete quality check pipeline
2. Test with realistic Proxmox scenarios
3. Verify configuration loading
4. Update documentation appropriately

## Common Patterns to Follow

### Error Handling Pattern
```python
try:
    # Proxmox API operation
    result = await api_call()
    return formatted_result
except ProxmoxAPIException as e:
    logger.error(f"Proxmox API error: {e}")
    raise ToolError(f"Failed to execute operation: {e}")
except Exception as e:
    logger.exception("Unexpected error")
    raise ToolError(f"Unexpected error: {e}")
```

### Tool Implementation Pattern
```python
class NewTool(ProxmoxTool):
    """Tool description for MCP registration."""
    
    async def execute(self, params: NewToolParams) -> str:
        """Execute the tool with validated parameters."""
        # Validate inputs
        # Call Proxmox API
        # Format output with rich formatting
        # Return formatted result
```

### Configuration Pattern
```python
class NewConfig(BaseModel):
    """Configuration model with validation."""
    
    field: str = Field(..., description="Field description")
    optional_field: Optional[int] = Field(None, description="Optional field")
    
    @validator("field")
    def validate_field(cls, v):
        # Custom validation logic
        return v
```

## Integration Considerations

### Proxmox API Integration
- Use ProxmoxManager for all API operations
- Handle authentication and connection errors
- Implement proper retry logic for transient failures
- Test with different Proxmox VE versions

### MCP Integration
- Follow tool registration patterns
- Implement proper tool descriptions
- Handle MCP protocol errors gracefully
- Test tool discovery and execution

### Docker Integration
- Maintain container security practices
- Test configuration mounting
- Verify health check functionality
- Document environment variable requirements