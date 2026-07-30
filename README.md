# Project Relay

**Installable project continuity skills for reliable Daily and Master handoffs, starting with
Git-backed projects.**

## The problem

Work on a project rarely happens in one sitting. It moves between sessions, between people, and
increasingly between agents. What survives that gap is usually a conversation summary — and a
summary recounts what was discussed, not what is true.

So the next session starts by re-deriving state. It repeats work that was already finished,
re-argues a decision that was already settled, retries an approach that already failed, and
inherits confident sentences that quietly stopped being true weeks ago.

## What Project Relay does

Project Relay produces two documents and keeps them honest.

- A **Daily Handoff** records what materially changed in one session and how it ended. New dated
  file each time, kept forever.
- A **Master Handoff** holds the canonical current project state after verified session changes
  are integrated. One file, updated in place.

The rules that make them trustworthy:

- Completed, planned, attempted, blocked, approved, superseded, unknown, and unverified stay
  distinct.
- Every claim traces to something observed, or is labelled `Unknown` / `Not verified` /
  `Pending Confirmation` / `Proposed`. A guess that looks verified is worse than a gap.
- Inherited claims are re-examined, not copied forward.
- Each fact has one home; the other document points rather than repeats.
- The next action is executable from the state described. If it's blocked on a missing input,
  getting that input *is* the next action.
- Length follows the project's real complexity — but no decision, constraint, or blocker is ever
  dropped to make a document shorter.

Those principles are stated once in [`shared/continuity-contract.md`](shared/continuity-contract.md).

## Current focus: `project-relay-git`

The first variant covers projects whose source of truth is a Git repository: repository identity,
branch, HEAD, working-tree state, local/remote divergence, file changes, pull requests and issues,
and build/test/migration/deployment state **when verified**.

→ [`skills/project-relay-git/`](skills/project-relay-git/)

## Installation

Run from the root of the project you want handoffs for:

```bash
git clone --depth 1 https://github.com/octonify/project-relay-skill.git /tmp/project-relay-skill
mkdir -p .claude/skills .claude/commands
cp -r /tmp/project-relay-skill/skills/project-relay-git .claude/skills/project-relay-git
cp /tmp/project-relay-skill/skills/project-relay-git/commands/handoff.md .claude/commands/handoff.md
rm -rf /tmp/project-relay-skill
```

Windows PowerShell, verification steps, updating, and uninstalling are in
[`docs/installation.md`](docs/installation.md).

## Usage

| Command | Effect |
|---|---|
| `/handoff` | One Daily Handoff for this session |
| `/handoff master` | Update the Master in place |
| `/handoff full` | Daily first, then integrate it into the Master |

Plain language works too — "wrap this up so I can resume tomorrow", "hand this over to someone
else". Documents land in `docs/handoffs/`, or in whatever handoff directory the project already
uses.

## Status

**Pre-release — `project-relay-git` v0.1.0.** Installable, and tested against fixture projects.
Not yet validated across a range of real long-running repositories, so document structure may
still change between minor versions. Existing handoff documents are not migrated automatically.

There is no stable release yet, and no variant other than `project-relay-git` exists.

## Repository structure

```
project-relay-skill/
├── README.md
├── shared/
│   └── continuity-contract.md     ← principles common to every variant
├── skills/
│   └── project-relay-git/         ← the installable skill: SKILL.md + references, assets, scripts, evals
├── docs/
│   └── installation.md
├── research/                      ← evaluation evidence from development; not part of the install
│   ├── iteration-1/
│   └── iteration-2/
└── reports/                       ← implementation reports
```

Each variant is self-contained: its own `SKILL.md`, `VERSION`, `CHANGELOG.md`, docs, and evals. A
future variant is a new directory under `skills/`, not a branch and not a change inside
`project-relay-git`.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). Short version: short-lived branches off `main`, one
variant per pull request, and behavioural changes to a skill need eval evidence — a claim that
output improved should come with the runs that show it.

## Roadmap

1. **Stabilise and validate `project-relay-git`** — the current cycle.
2. **Test it on real Git-backed workflows**, not only fixtures: long-running repositories,
   multiple contributors, handoffs read by someone who wasn't there.
3. **Release the first stable Git variant** (v1.0) once the structure holds steady across real use.
4. **Design separate project-type variants** — design, research, operations — from that validated
   experience rather than in advance of it.
5. **Evaluate cross-cutting capabilities** last: multi-agent coordination, multi-workstream
   scaling, long-term archive management.

Items 3–5 are not built. Nothing in this repository other than `project-relay-git` is installable.

## Licence

MIT — see [`LICENSE`](LICENSE).
