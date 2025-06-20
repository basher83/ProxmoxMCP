# Branch Templates Integration

Add this section to your main README.md or CONTRIBUTING.md to document the new branch templates:

## 🌿 Branch Creation Templates

To ensure consistent branch naming and streamlined development workflow, use the
provided branch creation templates located in `scripts/branch-templates/`.

### Quick Start

```bash
# Navigate to branch templates
cd scripts/branch-templates

# Interactive mode (recommended for beginners)
./interactive.sh

# Command line mode (faster for experienced users)
./create-branch.sh feature "add-vm-monitoring" 123
./feature.sh "add-vm-monitoring" 123  # Quick shortcut
```

### Available Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `interactive.sh` | Guided branch creation | `./interactive.sh` |
| `create-branch.sh` | Full-featured creation | `./create-branch.sh <type> <desc> [issue]` |
| `feature.sh` | Quick feature branches | `./feature.sh <desc> [issue]` |
| `fix.sh` | Quick fix branches | `./fix.sh <desc> [issue]` |
| `security.sh` | Security branches | `./security.sh <desc>` |
| `hotfix.sh` | Emergency fixes | `./hotfix.sh <desc>` |
| `validate.sh` | Check branch names | `./validate.sh [branch-name]` |

### Integration with Existing Workflow

These templates work seamlessly with:

- ✅ **autofix.ci**: Automatic code formatting
- ✅ **Claude Code**: AI-assisted development  
- ✅ **Dependabot**: Dependency management
- ✅ **GitHub Issues**: Automatic issue linking
- ✅ **Pull Request templates**: Consistent PR creation

For complete documentation, see [Branch Templates README](scripts/branch-templates/README.md).
