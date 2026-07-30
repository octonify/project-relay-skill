#!/usr/bin/env bash
# Install project-relay-git into a project from GitHub.
#
# Follows docs/installation.md exactly, with one documented-as-necessary deviation:
# --branch feat/project-relay-git, because the skill is not on main until PR #1 merges.
# Nothing is copied from the local development directory.
set -euo pipefail

TARGET="${1:?usage: install_from_github.sh <project-root> [ref]}"
REF="${2:-feat/project-relay-git}"
TMP="$(mktemp -d)/project-relay-skill"

git clone --depth 1 --branch "$REF" \
  https://github.com/octonify/project-relay-skill.git "$TMP" 2>&1 | sed 's/^/  clone: /'

cd "$TARGET"
mkdir -p .claude/skills .claude/commands
cp -r "$TMP/skills/project-relay-git" .claude/skills/project-relay-git
cp "$TMP/skills/project-relay-git/commands/handoff.md" .claude/commands/handoff.md

CLONED_SHA="$(git -C "$TMP" rev-parse HEAD)"
rm -rf "$(dirname "$TMP")"

echo "installed into: $TARGET"
echo "source ref:     $REF"
echo "source commit:  $CLONED_SHA"
