# Context Instructions

The Context7 server provides tools for conducting research and fetching up-to-date library documentation.

## Tools

`resolve-library-id`: Resolves a general library name into a Context7-compatible library ID.

    - libraryName (required): The name of the library to search for

`get-library-docs`: Fetches documentation for a library using a Context7-compatible library ID.

    - context7CompatibleLibraryID (required): Exact Context7-compatible library ID
      (e.g., /mongodb/docs, /vercel/next.js)
    - topic (optional): Focus the docs on a specific topic (e.g., "routing", "hooks")
    - tokens (optional, default 10000): Max number of tokens to return

## Workflow

1. **Research Phase**: Use `resolve-library-id` to find the correct library
   identifier when working with external dependencies
2. **Documentation Retrieval**: Use `get-library-docs` to fetch current
   documentation before implementing features or troubleshooting
3. **Focused Queries**: Specify `topic` parameter to get targeted documentation
   for specific functionality

## When to Use

- Before implementing new libraries or frameworks
- When troubleshooting integration issues
- To verify current API syntax and best practices
- For exploring library capabilities and features
