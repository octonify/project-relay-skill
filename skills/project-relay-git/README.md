# project-relay-git

Project continuity and handoff generation for **Git-backed projects**.

Version: see `VERSION` · Changes: see `CHANGELOG.md` · Install: see
[`docs/installation.md`](../../docs/installation.md)

## What it produces

| Document | Path | Lifecycle |
|---|---|---|
| **Daily Handoff** | `docs/handoffs/YYYY-MM-DD_NNN_<scope>-handoff.md` | New dated file per session, kept forever |
| **Master Handoff** | `docs/handoffs/_master-handoff.md` | One canonical file, updated in place |

If the project already uses `.handoffs/`, `handoffs/`, or `docs/handoff/`, that convention wins
over the default.

## Commands

| Command | Effect |
|---|---|
| `/handoff` | One Daily Handoff for this session |
| `/handoff master` | Update the Master in place; no new Daily, no second Master file |
| `/handoff full` | Daily first, then fold its verified content into the Master |

Plain-language requests work too — "wrap up so I can resume tomorrow", "hand this over to
someone else", "so the next session knows where we left off".

## What it records

Repository identity, branch, HEAD, staged/unstaged/untracked work, upstream divergence, stashes,
tags, recent commits, open PRs and issues, plus decisions, blockers, dependencies, sources of
truth, validation evidence, work that must not be repeated, and one executable next action.

Everything is either observed or labelled. `Unknown`, `Not verified`, `Pending validation`, and
`Proposed` are correct answers; a plausible guess is not.

## Layout

```
project-relay-git/
├── SKILL.md                       ← what Claude loads
├── VERSION
├── CHANGELOG.md
├── commands/handoff.md            ← slash-command definition
├── references/                    ← section guides, read on demand
│   ├── daily-handoff.md
│   ├── master-handoff.md
│   └── change-categories.md
├── assets/                        ← starting skeletons
│   ├── daily-handoff-template.md
│   └── master-handoff-template.md
├── scripts/handoff_context.py     ← observed repository + handoff state
└── evals/evals.json               ← behavioural test cases
```

## Helper script

```bash
python scripts/handoff_context.py --project-root . --scope auth
python scripts/handoff_context.py --project-root . --json      # machine-readable
python scripts/handoff_context.py --project-root . --no-gh     # skip GitHub lookups
```

Standard library only, no dependencies. Read-only: it inspects the repository and never writes,
commits, or pushes.

## Scope boundary

In scope: Git-backed projects, single repository, one or more workstreams.

Out of scope for this variant: non-Git projects, multi-agent coordination protocols, program-scale
archival systems, and design or research document semantics. Those are roadmap items — see the
repository README.
