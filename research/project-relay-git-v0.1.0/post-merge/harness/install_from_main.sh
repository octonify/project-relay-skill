#!/usr/bin/env bash
# Install project-relay-git from the default branch, using the commands in docs/installation.md
# verbatim and with no --branch flag. Nothing is copied from the local development directory.
set -euo pipefail

TARGET="${1:?usage: install_from_main.sh <project-root>}"
cd "$TARGET"

rm -rf /tmp/project-relay-skill

# --- verbatim from docs/installation.md (macOS / Linux / Git Bash) ---
git clone --depth 1 https://github.com/octonify/project-relay-skill.git /tmp/project-relay-skill
mkdir -p .claude/skills .claude/commands
cp -r /tmp/project-relay-skill/skills/project-relay-git .claude/skills/project-relay-git
cp /tmp/project-relay-skill/skills/project-relay-git/commands/handoff.md .claude/commands/handoff.md
CLONED_SHA="$(git -C /tmp/project-relay-skill rev-parse HEAD)"
CLONED_REF="$(git -C /tmp/project-relay-skill rev-parse --abbrev-ref HEAD)"
rm -rf /tmp/project-relay-skill
# --- end verbatim ---

echo "installed into: $TARGET"
echo "cloned ref:     $CLONED_REF"
echo "cloned commit:  $CLONED_SHA"
