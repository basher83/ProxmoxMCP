#!/bin/bash
# ProxmoxMCP Branch Template Configuration
# This file contains configuration for branch creation scripts
# shellcheck disable=SC2034  # Variables are used when sourced by other scripts

# Git Configuration
export MAIN_BRANCH="main"
export REMOTE="origin"

# Branch Type Definitions
export FEATURE_PREFIX="feature"
export FIX_PREFIX="fix"
export SECURITY_PREFIX="security"
export CHORE_PREFIX="chore"
export RELEASE_PREFIX="release"
export HOTFIX_PREFIX="hotfix"

# Commit Message Prefixes (following conventional commits)
export FEATURE_COMMIT_PREFIX="feat"
export FIX_COMMIT_PREFIX="fix"
export SECURITY_COMMIT_PREFIX="security"
export CHORE_COMMIT_PREFIX="chore"
export RELEASE_COMMIT_PREFIX="release"
export HOTFIX_COMMIT_PREFIX="hotfix"

# Template Messages
export FEATURE_TEMPLATE="feat: implement {description}

- Add {description}
- Include appropriate tests
- Update documentation if needed

Closes #{issue_number}"

export FIX_TEMPLATE="fix: resolve {description}

- Fix {description}
- Add regression test
- Update related documentation

Fixes #{issue_number}"

export SECURITY_TEMPLATE="security: {description}

- Address {description}
- Follow security best practices
- Update security documentation if needed

Addresses security concern"

export HOTFIX_TEMPLATE="hotfix: critical fix for {description}

- Address critical {description}
- Minimal change for immediate resolution
- Requires expedited review

Critical fix required for production"

# Review Requirements by Branch Type
export FEATURE_REVIEWERS=1
export FIX_REVIEWERS=1
export SECURITY_REVIEWERS=2 # Security changes need additional review
export HOTFIX_REVIEWERS=1   # But fast-tracked
export CHORE_REVIEWERS=1
export RELEASE_REVIEWERS=2 # Release changes need careful review
