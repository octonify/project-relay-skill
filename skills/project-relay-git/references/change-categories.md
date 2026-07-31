# Change categories — recall checklist

Use this while writing "What Changed" in a Daily Handoff, or "Changes Since the Previous Baseline"
in a Master Handoff.

It is a memory aid, not a template. Skim it, note where something actually moved this session,
and write only those. Reproducing every heading with "n/a" underneath makes the document longer
and less trustworthy — the reader can no longer tell effort from coverage.

Why a list this broad: the reflex is to record code and file edits, because those show up in the
diff. The changes that break the next session are usually the ones that don't — a rotated secret,
a new required environment variable, a branch protection rule, a CI step someone added.

## Repository and version control
Files created, edited, deleted, moved, renamed — with exact paths. Branches created, switched,
merged, deleted, rebased. Commits, amends, reverts, cherry-picks, force-pushes. Tags. Stashes
left behind. Submodules. `.gitignore` and `.gitattributes`. Remote added or changed. Work left
uncommitted or unpushed.

Force-pushes and history rewrites deserve a line in "Work That Must Not Be Repeated" as well —
anyone with an older clone is now diverged and needs to know.

## Code and dependencies
Modules, APIs, interfaces, and contracts changed. Dependencies added, removed, upgraded, pinned.
Lockfiles. Build configuration. Language or runtime version. Feature flags. Public API breakage.

## Tests, builds, and CI
Tests added, changed, skipped, or deleted. Test results actually observed. Build outcome. CI
workflow files, required checks, branch protection, secrets used by CI, cache behaviour, matrix
changes.

Record what you ran and saw. A test file you wrote but never executed is a change, not a result.

## Data and migrations
Schema changes, migrations written, migrations applied and to which environment, seed data,
imports and exports, data corrections, backfills.

Applied migrations and bulk data operations are irreversible enough to belong in "Work That Must
Not Be Repeated" with the environment named.

## Infrastructure and environments
Environment variables and configuration, secrets rotated, containers and images, services,
databases, storage, DNS, CDN, hosting, deployment targets, scaling settings, monitoring, alerts,
backups.

## Access and process
Repository permissions, review requirements, approval gates, code owners, agent instructions and
skills, tool access, naming and branching conventions, release process.

A process change is invisible to a code reader and binding on them anyway — record it.

## External services and tickets
Issues and PRs opened, closed, merged, or relabelled. Third-party service settings, integrations,
API keys, webhooks, analytics, deploy hooks.

Only what you looked up. An issue number you remember is not an issue you verified.

## Project management state
Scope, priority, milestones, owners, dependencies, timeline, approval status.

---

## Recording format

```markdown
- Change:
- Location:
- Previous State:
- New State:
- Reason:
- Validation:
```

`Previous State` is the field most often guessed and the most harmful to guess — it's what someone
will use to roll back. For tracked files, name the commit it was last good at. If you didn't
observe it, write `Unknown — not captured before change`.

`Validation` says how you know the change took effect, or `Not validated` if you don't. Both are
acceptable answers; silence is not.
