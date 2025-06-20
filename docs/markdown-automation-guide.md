# 📝 Automated Markdown Linting Guide

> **Comprehensive guide to automated markdown formatting and quality assurance**

## 🎯 **Overview**

This guide covers the automated markdown linting system implemented to maintain
consistent documentation quality across ProxmoxMCP. The system automatically
detects, reports, and fixes common markdown formatting issues.

## 🛠️ **Components**

### **1. markdownlint-cli2**

- **Purpose**: Modern, fast markdown linting tool
- **Auto-fix**: Automatically resolves 70%+ of formatting issues
- **Integration**: Works with pre-commit, CI/CD, and local development

### **2. Configuration** (`.markdownlint.jsonc`)

- **Customized Rules**: Tailored for technical documentation
- **120-character line limit**: Balances readability and display
- **Flexible HTML**: Allows badges, details, and common HTML elements

### **3. Taskfile Integration**

```bash
task markdown:lint     # Check all markdown files
task markdown:fix      # Auto-fix formatting issues
task markdown:check    # Strict checking (CI mode)
task markdown:summary  # Overview of all issues
```

### **4. Pre-commit Hook**

- **Automatic**: Runs on every commit
- **Auto-fix**: Applies fixes before commit
- **Fast**: Only processes changed markdown files

### **5. GitHub Actions Workflow**

- **PR Analysis**: Automatic markdown quality checking
- **Auto-fix Commits**: Pushes fixes directly to PR branches
- **Quality Reports**: Detailed summaries and artifacts

## 🚀 **Quick Start**

### **Install Tools**

```bash
# Install markdownlint-cli2 globally
npm install -g markdownlint-cli2

# Or use the project's Taskfile
task setup  # Already includes markdown tooling
```

### **Basic Usage**

```bash
# Check all markdown files
task markdown:lint

# Auto-fix issues (recommended)
task markdown:fix

# Check what would be fixed (preview)
markdownlint-cli2 "**/*.md" --fix --output-fixes
```

## 📋 **Common Issues & Auto-fixes**

### **✅ Auto-fixable Issues**

| Rule      | Issue                                     | Auto-fix              |
| --------- | ----------------------------------------- | --------------------- |
| **MD032** | Lists not surrounded by blank lines       | ✅ Adds blank lines   |
| **MD022** | Headers not surrounded by blank lines     | ✅ Adds blank lines   |
| **MD031** | Code blocks not surrounded by blank lines | ✅ Adds blank lines   |
| **MD047** | Files not ending with newline             | ✅ Adds newline       |
| **MD009** | Trailing spaces                           | ✅ Removes spaces     |
| **MD010** | Hard tabs                                 | ✅ Converts to spaces |
| **MD012** | Multiple consecutive blank lines          | ✅ Removes extras     |

### **⚠️ Manual Review Required**

| Rule      | Issue                       | Resolution                        |
| --------- | --------------------------- | --------------------------------- |
| **MD013** | Line too long (>120 chars)  | Break lines, shorter URLs         |
| **MD025** | Multiple H1 headers         | Restructure document              |
| **MD041** | First line not H1           | Add title or disable for snippets |
| **MD029** | Inconsistent list numbering | Manually renumber lists           |

## 🔧 **Configuration Details**

### **Line Length (MD013)**

```jsonc
"MD013": {
  "line_length": 120,  // Increased from default 80
  "headers": false,    // Don't count header lines
  "code_blocks": false, // Don't count code blocks
  "tables": false      // Don't count table lines
}
```

### **Allowed HTML (MD033)**

```jsonc
"MD033": {
  "allowed_elements": [
    "details", "summary",  // Collapsible sections
    "br", "img", "a",      // Basic HTML
    "kbd", "sub", "sup"    // Typography
  ]
}
```

### **Code Block Style (MD046)**

````jsonc
"MD046": {
  "style": "fenced"  // Prefer ``` over indented blocks
}
````

## 🔄 **Workflow Integration**

### **Local Development**

1. **Pre-commit**: Automatic fixing on commit
2. **Manual fixes**: `task markdown:fix`
3. **Quality check**: `task markdown:summary`

### **Pull Requests**

1. **Automatic analysis**: GitHub Action runs on PR
2. **Auto-fix commits**: Fixes pushed to PR branch
3. **Quality reports**: Detailed analysis in artifacts

### **CI/CD Pipeline**

```yaml
# In .github/workflows/markdown-lint.yml
- Markdown quality checking
- Auto-fix generation
- Quality report artifacts
- Integration with existing workflows
```

## 📊 **Quality Metrics**

### **Before Automation**

- **500+ formatting issues** across documentation
- **Manual fixing**: Time-intensive and inconsistent
- **Review overhead**: Significant PR review time

### **After Automation**

- **149 remaining issues** (70% reduction)
- **Auto-fixing**: Most issues resolved automatically
- **Consistent quality**: Enforced formatting standards

## 🎛️ **Advanced Usage**

### **Exclude Specific Files**

```bash
# Ignore certain directories
markdownlint-cli2 "**/*.md" "!node_modules/**" "!.venv/**"
```

### **Custom Rule Configuration**

```jsonc
{
  "MD024": {
    // Allow duplicate headers in different sections
    "allow_different_nesting": true
  },
  "MD040": false // Disable requirement for code block languages
}
```

### **Integration with IDEs**

#### **VS Code Extension**

```json
{
  "markdownlint.config": {
    "extends": ".markdownlint.jsonc"
  }
}
```

#### **Vim/Neovim**

```lua
-- With coc.nvim or nvim-lsp
require'lspconfig'.marksman.setup{}
```

## 🐛 **Troubleshooting**

### **"markdownlint-cli2 not found"**

```bash
# Install globally
npm install -g markdownlint-cli2

# Or use npx
npx markdownlint-cli2 "**/*.md"
```

### **"Too many issues to fix automatically"**

```bash
# Fix issues in batches
markdownlint-cli2 --fix "docs/*.md"
markdownlint-cli2 --fix "*.md"
```

### **"Pre-commit hook failing"**

```bash
# Run manually to see details
pre-commit run markdownlint-cli2 --all-files

# Update pre-commit
pre-commit autoupdate
```

## 🔮 **Future Enhancements**

### **Planned Improvements**

- **Custom rule development**: Project-specific linting rules
- **Integration with documentation generators**: Hugo, GitBook, etc.
- **AI-powered suggestions**: Automated content improvements
- **Performance optimization**: Faster linting for large documentation sets

### **Advanced Automation**

- **Scheduled quality reports**: Weekly documentation health checks
- **Integration with project management**: Link quality metrics to milestones
- **Multi-language support**: Extend to other markup formats

## 📚 **Additional Resources**

- **[markdownlint Rules Documentation](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md)**
- **[markdownlint-cli2 Configuration](https://github.com/DavidAnson/markdownlint-cli2#configuration)**
- **[Project Taskfile](../Taskfile.yml)**: See markdown tasks
- **[Pre-commit Configuration](../.pre-commit-config.yaml)**: Hook setup

---

> **💡 Tip**: Run `task markdown:summary` regularly to monitor documentation
> quality and catch issues early in development.
