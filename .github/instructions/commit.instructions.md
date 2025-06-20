---
description: "Instructions for GitHub Copilot to generate commit messages in ProxmoxMCP format"
applyTo: "**"
---

# GitHub Copilot Commit Message Instructions

GitHub Copilot should follow the ProxmoxMCP commit message format defined in the
[gitignore](.gitmessage) file when generating commit messages.

Follow these steps exactly when making a commit:

1) Pull latest changes from main branch and resolve any conflicts.
2) Stage your changes using `git add <file>` or `git add .` for all files.
3) Commit using the repos .gitmessage template.
4) Push your changes to main branch.
