# Implementation report — `project-relay-git` v0.1.0

Date: 2026-07-30
Branch: `feat/project-relay-git`
Status: implementation complete, behaviour validation in progress at time of writing

---

## 1. Audit findings

Three locations were inspected before any change.

**`D:\Projects\Skills\project-relay`** — the working skill. Eight files: `SKILL.md`, three
references, two templates, one script, one eval set. Not under version control. Scope was generic
across project types: the Master reference told the writer to substitute an "operational state"
section for non-technical work, and the change checklist covered content, media, and campaign
categories alongside code. Nothing in it was Git-specific beyond one paragraph.

**`D:\Projects\Skills\project-relay-workspace`** — 3.3 MB of evaluation evidence: fixture
builders, two iterations of runs (with-skill vs baseline), grades, timings, benchmarks, one
human feedback file, and two generated review pages. Each run directory contained a full copy of
its fixture project, including nested `.git` directories — unsuitable for committing as-is.

**`github.com/octonify/project-relay-skill`** — public, default branch `main`, one commit
(`7d623d2 Initial commit`), containing a 21-byte `README.md` and nothing else. No branches beyond
`main`, no releases, no issues. No remote history was at risk.

**Conclusion:** the skill was real and tested but generically scoped, unversioned, uninstallable,
and entirely absent from the repository that was supposed to distribute it.

---

## 2. Final repository structure

```
project-relay-skill/
├── README.md                      purpose, install, usage, status, structure, roadmap
├── CONTRIBUTING.md                branch model, how to add a variant, evidence rules
├── LICENSE                        MIT
├── shared/
│   └── continuity-contract.md     8 principles common to every future variant
├── skills/
│   └── project-relay-git/         the installable unit
│       ├── SKILL.md               frontmatter + 274-line body
│       ├── README.md, VERSION, CHANGELOG.md
│       ├── commands/handoff.md    /handoff, /handoff master, /handoff full
│       ├── references/            daily (13 sections), master (20), change categories
│       ├── assets/                two starting skeletons
│       ├── scripts/
│       │   └── handoff_context.py observed repo + handoff state
│       └── evals/
│           ├── evals.json         3 cases, 14 assertions each
│           ├── build_fixtures.py  builds 3 real Git fixtures with planted traps
│           └── check_outputs.py   mechanical assertion checker
├── docs/
│   └── installation.md            prerequisites, install, verify, update, uninstall, troubleshooting
├── research/                      iteration 1 + 2 evidence, not part of the install
└── reports/                       this file
```

A future variant is a new directory under `skills/`. It does not require a branch, a change inside
`project-relay-git`, or anything in `shared/` beyond what already exists.

---

## 3. What was preserved from iterations 1 and 2

Evidence is archived under `research/`, pruned of per-run fixture copies (which carried nested
`.git` directories) and of the two generated review pages. What remains: generated documents,
`grading.json`, `timing.json`, `eval_metadata.json`, both benchmarks, and the human feedback file
that drove iteration 2. `research/README.md` explains what each iteration established.

Three findings were carried into the shipped skill:

1. **The evidence rule, extended to inherited claims.** Iteration 1's with-skill outputs contained
   no fabrications; what they did was carry forward stale claims planted in the fixture Master.
   The rule now says explicitly that an inherited line is evidence of past belief, not of current
   state, and gives four permitted responses.
2. **Menu-not-checklist framing.** Iteration 1's real failure was length: 8× the source material
   on one case, 20× on another, because every heading was treated as required. Both section
   references now open by saying the list is a menu and that deleting a heading is correct.
3. **Single-home rules.** Iteration 2 fixed narrative bleed but left five blocks duplicated across
   both documents. `SKILL.md` now carries a table assigning each block a primary home, with
   one-directional cross-references: Master points back at Dailies, Daily points forward at the
   Master.

**Deliberately not carried forward:** the character caps added to iteration 2's assertions. They
forced brevity by penalising complex projects for being complex, and they conflict with the
instruction never to drop a decision or blocker to shorten a document. Proportionality is now
judged by repetition and restated source material.

Two known eval bugs are documented in `research/README.md` rather than silently inherited: a pair
of mutually contradictory assertions in the old eval-1, and a fabrication check narrow enough that
an invented source-precedence rule passed it. The second directly shaped the shipped skill, which
now says an undecided precedence rule is an open decision, not a rule.

---

## 4. What changed

**Scope narrowed to Git.** `SKILL.md` has an explicit scope section. Non-Git projects are out of
scope and degrade to `Not applicable` rather than `Unknown` — the reader should not go looking for
a repository that doesn't exist.

**Repository state became first-class.** The Daily reference gained a *Repository State at Session
End* section (branch, HEAD, staged/unstaged/untracked with paths, stashes, upstream divergence,
PR, issues). The Master's technical-state section was rewritten around the same fields.

**The helper script was extended.** It now separates staged from unstaged from untracked, detects
detached HEAD, reports stash count, latest tag, and diffstat, and — when `gh` is installed and
authenticated — open PRs and issues, including any PR for the current branch. When `gh` is
missing it says so, and the skill records PR state as `Not verified` rather than "none".

**A slash command was added.** `/handoff` was previously only a phrase in the skill description.
`commands/handoff.md` makes it a real command with argument routing.

**Fabrication guards were made specific.** The evidence rule now names the things most often
invented: an issue or PR nobody looked up, a test suite nobody ran, an approval nobody gave, an
owner nobody named, a precedence rule nobody stated.

**Next actions must clear a prerequisite test.** When the intended step depends on a missing
input, access, decision, or answer, obtaining that prerequisite *is* the next action, named
concretely.

---

## 5. Installation method

Project-local, plain `git clone` plus `cp`. No installer script: the copy is two commands, and a
script would add a thing to maintain and test on two platforms without removing a step anyone
finds hard.

```bash
git clone --depth 1 https://github.com/octonify/project-relay-skill.git /tmp/project-relay-skill
mkdir -p .claude/skills .claude/commands
cp -r /tmp/project-relay-skill/skills/project-relay-git .claude/skills/project-relay-git
cp /tmp/project-relay-skill/skills/project-relay-git/commands/handoff.md .claude/commands/handoff.md
rm -rf /tmp/project-relay-skill
```

A PowerShell equivalent, verification steps, update and uninstall procedures, and a
troubleshooting table are in `docs/installation.md`.

---

<!-- Sections 6-9 completed after the validation runs. -->
