# Changelog — project-relay-git

All notable changes to this skill variant. Versions are independent of other variants in this
repository.

## [0.1.0] — 2026-07-30

First packaged, installable release. Pre-1.0: the document structure may still change between
minor versions.

### Added
- Git-scoped `SKILL.md`: repository identity, branch, HEAD, working-tree state, local/remote
  divergence, PRs and issues, and build/test/migration/deployment state when verified.
- `scripts/handoff_context.py` — resolves the handoff directory, computes the next Daily
  filename, reports which Dailies the Master has incorporated, and dumps observed Git state
  (staged/unstaged/untracked, stashes, tags, upstream divergence, recent commits). Reports open
  PRs and issues when `gh` is installed and authenticated, and says so explicitly when it is not.
- `commands/handoff.md` — `/handoff`, `/handoff master`, `/handoff full`.
- `references/` — Daily (13 sections) and Master (20 sections) section guides, plus a change
  recall checklist.
- `assets/` — starting skeletons for both documents.
- `evals/evals.json` — three behavioural test cases with assertions.

### Carried forward from the pre-variant research iterations
- **The evidence rule**, extended to inherited claims: a line in an existing Master is evidence
  of what someone believed then, not of current state. Verify, mark unverified, mark stale, or
  supersede.
- **Menu-not-checklist framing** for both section lists. Iteration 1 produced documents 8×–20×
  the size of their source material because every heading was treated as required.
- **Single-home rules.** Iteration 2 fixed session-narrative bleed but left the risk register,
  constraints, do-not-repeat list, next-action block, and continuation sources duplicated across
  both documents. Each block now has one primary home and a one-directional cross-reference.

### Deliberately not carried forward
- Character-count caps on output. Iteration 2 used them to force brevity; they penalise complex
  projects for being complex. Proportionality is judged by repetition and restated source
  material instead.

### Known limitations
- Non-Git projects are out of scope for this variant. The skill degrades by recording repository
  state as `Not applicable` rather than guessing.
- Multi-agent coordination, multi-repository programs, and long-term archive management are
  roadmap items, not implemented behaviour.
