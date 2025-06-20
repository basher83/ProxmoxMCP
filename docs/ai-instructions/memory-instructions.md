# docs

> **Warning**: The mem0 server is not accessible in Codex. These instructions are informational only.

The mem0 server provides three main tools for managing code preferences:

`add_coding_preference`: Store code snippets, implementation details, and coding patterns with comprehensive context including:

Complete code with dependencies
Language/framework versions
Setup instructions
Documentation and comments
Example usage
Best practices

`get_all_coding_preferences`: Retrieve all stored coding preferences to analyze
patterns, review implementations, and ensure no relevant information is missed.

`search_coding_preferences`: Semantically search through stored coding preferences to find relevant:

Code implementations
Programming solutions
Best practices
Setup guides
Technical documentation

# Rules

1. Always utilize `get_all_coding_preferences` to retrieve all coding preferences before starting any tasks.
2. Use `search_coding_preferences` to find specific coding preferences related to the task at hand.
3. When adding new coding preferences, ensure they are comprehensive and include all relevant context.
4. Maintain clear and consistent documentation for all coding preferences to facilitate understanding and reuse.
5. Regularly review and update coding preferences to keep them relevant and useful.
6. Update coding preferences with new insights, optimizations, or changes in best practices after any major changes.
