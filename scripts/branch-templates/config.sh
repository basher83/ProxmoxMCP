# ProxmoxMCP Branch Template Configuration
# This file contains configuration for branch creation scripts

# Git Configuration
MAIN_BRANCH="main"
REMOTE="origin"

# Branch Type Definitions
FEATURE_PREFIX="feature"
FIX_PREFIX="fix"
SECURITY_PREFIX="security"
CHORE_PREFIX="chore"
RELEASE_PREFIX="release"
HOTFIX_PREFIX="hotfix"

# Commit Message Prefixes (following conventional commits)
FEATURE_COMMIT_PREFIX="feat"
FIX_COMMIT_PREFIX="fix"
SECURITY_COMMIT_PREFIX="security"
CHORE_COMMIT_PREFIX="chore"
RELEASE_COMMIT_PREFIX="release"
HOTFIX_COMMIT_PREFIX="hotfix"

# Template Messages
FEATURE_TEMPLATE="feat: implement {description}

- Add {description}
- Include appropriate tests
- Update documentation if needed

Closes #{issue_number}"

FIX_TEMPLATE="fix: resolve {description}

- Fix {description}
- Add regression test
- Update related documentation

Fixes #{issue_number}"

SECURITY_TEMPLATE="security: {description}

- Address {description}
- Follow security best practices
- Update security documentation if needed

Addresses security concern"

HOTFIX_TEMPLATE="hotfix: critical fix for {description}

- Address critical {description}
- Minimal change for immediate resolution
- Requires expedited review

Critical fix required for production"

# Review Requirements by Branch Type
FEATURE_REVIEWERS=1
FIX_REVIEWERS=1
SECURITY_REVIEWERS=2  # Security changes need additional review
HOTFIX_REVIEWERS=1    # But fast-tracked
CHORE_REVIEWERS=1
RELEASE_REVIEWERS=2   # Release changes need careful review
