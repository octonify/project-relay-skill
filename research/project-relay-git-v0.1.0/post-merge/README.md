# Post-merge verification of the public install path

Evidence for `reports/2026-07-30-project-relay-git-post-merge-report.md`. **Not part of the
installable skill.**

Everything here installs `project-relay-git` from `main` using the commands in
`docs/installation.md` verbatim, with no `--branch` flag, into a throwaway Git repository built
fresh for each run. Nothing is copied from the development tree.

## Fixture

A fourth project domain — `inventory-sync`, a Python service reconciling warehouse counts
against an order ledger — chosen to be distinct from the eval fixtures and the pre-merge
end-to-end fixtures, so these runs are independent evidence rather than a repeat.

State at handoff time: branch `feat/stock-reconcile`, three commits, one staged file
(`inventory/reconcile.py`), one unstaged file (`inventory/adapters/warehouse.py`), three
untracked paths, and no remote. Four claims are planted in an untracked `SESSION-NOTES.md` that
the repository contradicts or cannot support: 62 passing tests, a 3× speedup, a staging deploy,
and a spot-check request sent to a colleague.

The unstaged path sorts *before* the staged path. That ordering is deliberate — see below.

## Contents

```
post-merge/
├── harness/
│   ├── build_fixture.py       # builds the fixture, traps included
│   ├── install_from_main.sh   # the documented clone/copy, no --branch flag
│   └── verify_daily.py        # scores the produced Daily against real Git state
├── defect-discovery/          # the run that surfaced the porcelain bug (pre-fix)
├── round1/                    # first clean round: handoff, session log, verify output
└── round2/                    # second clean round, same rules
```

## What these runs established

**The documented install from `main` works.** `git clone --depth 1 <repo>` with no branch flag
resolves to `main`, both `.claude/skills/project-relay-git/SKILL.md` and
`.claude/commands/handoff.md` land, the context helper reports correct repository state, and
`/handoff` in a fresh Claude Code process writes exactly one correctly-named dated Daily.

**A shipped defect was found, and the skill did not propagate it.** The first run's context
helper reported `staged 2, unstaged 0` and printed `[staged] M nventory/adapters/warehouse.py`
— one file misclassified, one path missing its first character. Cause: `run()` in
`handoff_context.py` returned `out.stdout.strip()`, which removes the significant leading space
from the *first* line of `git status --porcelain`. Fixed in #2.

The bug is invisible whenever a staged path happens to sort first, which is why every earlier
fixture missed it — hence this fixture's deliberate path ordering.

Worth recording separately: the `/handoff` run over the broken helper output cross-checked it
against `git status --porcelain`, used the correct reading in the document, and filed the
discrepancy as an open item. The helper was wrong; the handoff was not.

**Two consecutive clean rounds**, 34/34 checks each, scored by the same `verify_daily.py`. The
score covers branch, HEAD, every commit, the staged/unstaged/untracked sets and their labels,
absence of invented remotes, PRs and issues, and one hedging check per planted trap.

## Caution on the scorer

`verify_daily.py` is a heuristic. Its hedge pattern was widened four times against correct
skill output — a denial, a cross-reference, an interrogative, and a claim attributed to its
source were each initially misread as assertions. A rule widened that often can end up
accepting anything, so the scorer plants five assertions of its own on every run and fails if
any survives. All five are caught in both rounds; that check is one of the 34.

Round 1's first scoring pass used an earlier revision of the scorer. Both rounds here were
re-scored under the final rules against preserved fixtures, so the two passes are comparable.
