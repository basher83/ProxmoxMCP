# Quick branch hygiene check

Quick branch hygiene check and immediate improvements: $ARGUMENTS

Execute rapid branch analysis focusing on immediate wins and obvious improvements. Use this for daily/weekly branch maintenance.

**IMPORTANT**: Always verify branch state against GitHub API to catch stale local branches that no longer exist remotely.

## Rapid Analysis Mode

**Step 1: Quick Branch Overview**

```bash
# Get all local branches with recent activity
git for-each-ref --format='%(refname:short) %(committerdate:relative) %(authorname)' refs/heads/ --sort=-committerdate | head -10

# Get all remote branches for comparison
git branch -r

# Verify against GitHub API for authoritative source
gh api repos/OWNER/REPO/branches | jq '.[].name'
```

**Step 1.1: Stale Branch Detection**

```bash
# Identify local branches that don't exist on GitHub
local_branches=$(git branch --format='%(refname:short)' | grep -v '^main$')
github_branches=$(gh api repos/$(gh repo view --json owner,name --jq '.owner.login + "/" + .name')/branches | jq -r '.[].name')

echo "=== STALE BRANCH DETECTION ==="
for branch in $local_branches; do
  if ! echo "$github_branches" | grep -q "^$branch$"; then
    echo "🗑️  STALE: $branch (not on GitHub)"
  fi
done
```

**Step 1.2: Safe Stale Branch Cleanup**

```bash
# Interactive cleanup of stale branches (with safety checks)
for branch in $local_branches; do
  if ! echo "$github_branches" | grep -q "^$branch$"; then
    echo "Branch '$branch' not found on GitHub"
    echo "Last commit: $(git log -1 --format='%h %s' $branch 2>/dev/null || echo 'Invalid branch')"
    read -p "Delete local branch '$branch'? [y/N] " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
      git branch -D "$branch" && echo "✅ Deleted: $branch"
    else
      echo "⏭️  Skipped: $branch"
    fi
  fi
done
```

**Step 1.3: Automated Safe Cleanup (Non-Interactive)**

```bash
# Safer automated cleanup with explicit confirmation
echo "=== AUTOMATED STALE BRANCH CLEANUP ==="
stale_branches=()
for branch in $local_branches; do
  if ! echo "$github_branches" | grep -q "^$branch$"; then
    # Additional safety check: ensure branch is not current branch
    if [ "$(git branch --show-current)" != "$branch" ]; then
      stale_branches+=("$branch")
    fi
  fi
done

if [ ${#stale_branches[@]} -gt 0 ]; then
  echo "Found ${#stale_branches[@]} stale local branches:"
  printf "  - %s\n" "${stale_branches[@]}"
  read -p "Delete all stale branches? [y/N] " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    for branch in "${stale_branches[@]}"; do
      git branch -D "$branch" && echo "✅ Deleted: $branch"
    done
    echo "🧹 Cleanup completed"
  else
    echo "❌ Cleanup cancelled"
  fi
else
  echo "✅ No stale branches found"
fi
```

**Step 2: Identify Low-Hanging Fruit**
Focus on GitHub-verified branches with these patterns for immediate merge candidates:

**A. Universal Improvements (Merge Immediately)**

- `.eslintrc`, `prettier.config.js`, `.github/workflows/` changes
- `package.json` dependency updates
- `CONTRIBUTING.md`, `README.md` improvements  
- `pyproject.toml`, `requirements.txt` updates
- General bug fixes in shared utilities

**B. ProxmoxMCP-Specific Quick Wins**

- Updates to `CLAUDE.md` that improve development guidance
- Improvements to `formatting/` module that benefit all tools
- Enhancements to `core/proxmox.py` error handling
- Quality improvements to existing tools in `tools/` directory
- Test infrastructure improvements

**Step 3: Execute Quick Merge Strategy**
For each identified improvement (only from GitHub-verified branches):

```bash
# Ensure we're working with clean state after stale branch cleanup
git checkout main && git pull origin main

# Verify target branch exists on GitHub before proceeding
target_branch="feature/example-branch"
if gh api repos/$(gh repo view --json owner,name --jq '.owner.login + "/" + .name')/branches/$target_branch >/dev/null 2>&1; then
  echo "✅ Branch verified on GitHub: $target_branch"
  
  # Create quality improvement branch
  git checkout -b chore/quality-improvements-$(date +%Y%m%d)
  
  # Cherry-pick specific improvements
  git cherry-pick -x [commit-hash] # Add meaningful commit messages
else
  echo "❌ Branch not found on GitHub: $target_branch (skipping)"
fi
```

**Step 4: Generate Quick PR**
Create immediate PR for quality improvements:

- Title: "Quality improvements from feature branches [DATE]"
- Description: List source branches and specific improvements
- Label: `enhancement`, `code-quality`
- Assign to `claude-code-bot` for automated review

## Focus Areas for ProxmoxMCP

**High-Value Immediate Merges:**

- Improvements to ProxmoxManager error handling
- Rich formatting enhancements in `formatting/` module
- Test utilities that benefit multiple tools
- Documentation improvements that clarify current functionality
- CI/CD improvements from `.github/workflows/`

**Keep in Feature Branches:**

- Incomplete MCP server implementations
- New Proxmox API endpoints under development
- Experimental authentication methods
- WIP tool implementations in `tools/` directory

**Red Flags (Need Attention):**

- Feature branches modifying core authentication without clear purpose
- Changes to existing tool interfaces without feature justification
- Configuration changes that might break existing setups

## Quick Decision Matrix

**Immediate Merge If:**

- ✅ Improves code quality for existing functionality
- ✅ Fixes bugs in current stable features
- ✅ Enhances development experience (linting, testing, docs)
- ✅ Security improvements with no breaking changes
- ✅ Performance optimizations with no API changes

**Keep in Branch If:**

- 🔄 Implements new Proxmox functionality
- 🔄 Changes existing tool APIs
- 🔄 Adds new MCP server capabilities
- 🔄 Experimental or incomplete implementations
- 🔄 Breaking changes requiring coordination

**Needs Investigation If:**

- ⚠️ Mixes feature work with quality improvements
- ⚠️ Large changes without clear branch purpose
- ⚠️ Modifications to stable core components
- ⚠️ Configuration changes affecting authentication
- ⚠️ Cross-cutting changes affecting multiple tool categories

## Output Quick Summary

Generate immediate actionable summary:

```markdown
## Quick Branch Hygiene - [Date]

### Immediate Merge Candidates (< 30 min effort)
- Branch: feature/vm-snapshot-tools
  - File: `formatting/table_formatter.py` (performance improvement)
  - Action: Cherry-pick commit abc123

### This Week's Focus Branches
- feature/mcp-claude-sdk-integration: 75% complete, ETA 1 week
- bugfix/authentication-retry-logic: Ready for review

### Cleanup Needed
- feature/old-experiment: No activity 30+ days, consider closing
- hotfix/temp-fix: Changes should be in main, needs immediate merge

### Stale Branch Cleanup Results
- 🗑️ Deleted stale local branches: [list branches removed]
- ✅ Verified GitHub branches: [list remaining branches] 
- ⚠️ Manual review needed: [list branches requiring attention]

### Next Actions
1. Create quality improvement PR with 3 identified commits
2. Review feature/mcp-claude-sdk-integration for completion
3. Close stale experimental branches
4. Run stale branch cleanup weekly to maintain repository hygiene
```

## Safety Guidelines for Stale Branch Cleanup

**CRITICAL SAFETY CHECKS:**

1. **Never delete the current branch** - Script automatically checks this
2. **Always verify against GitHub API** - Local branches may be outdated
3. **Show last commit info** - Allow user to verify branch content before deletion
4. **Interactive confirmation** - Require explicit user approval for each deletion
5. **Backup option** - Consider creating backup branches for important-looking commits

**When NOT to delete local branches:**
- Branches with uncommitted work that might be valuable
- Branches that were recently rebased (GitHub state may lag)
- Branches that are work-in-progress but not yet pushed
- Branches with cherry-picked commits that aren't in main yet

**Best Practices:**
- Run `git fetch --prune` first to sync remote tracking branches
- Use `git branch -D` (force delete) only after verification
- Consider `git branch --merged` and `git branch --no-merged` for additional context
- Keep logs of deleted branches for recovery if needed

**Integration Note:** Use this command weekly before your automated GitHub issue processing to maintain clean branch state for your automation workflows. The stale branch cleanup should be the first step in any branch hygiene workflow to ensure accurate analysis of remaining branches.
