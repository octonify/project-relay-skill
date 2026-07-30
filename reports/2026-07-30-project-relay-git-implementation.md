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

## 6. Test scenarios executed

Three fixtures, built by `evals/build_fixtures.py` as real Git repositories so every claim about
branch, HEAD, and working tree can be checked against `git` rather than believed. Each carries
planted traps: intentions phrased as completions, results nobody observed, stale inherited claims.

| Fixture | Command | What it tests |
|---|---|---|
| `g1-rate-limit` | `/handoff` | Mid-feature session: 3 commits, staged + unstaged + untracked work, no remote, a rejected approach, a blocker on a named person |
| `g2-master-update` | `/handoff master` | Cumulative update: a v2.0 Master full of stale claims, two unincorporated Dailies, a deleted branch, a test suite that left the repository |
| `g3-handover` | `/handoff full` | Cold handover: work blocked on a prerequisite nobody obtained, one hard constraint learned the expensive way |

Every run installed the skill **from the GitHub branch**, not from the working directory: clone
`feat/project-relay-git`, copy `skills/project-relay-git/` into `.claude/skills/`, copy the
command into `.claude/commands/`, then run the scenario in that project.

Three rounds were executed:

- **Pre-revision** — first behaviour runs, which found the defect described in §7.
- **Run A** — after the revision, on freshly built fixtures.
- **Run B** — again on freshly built fixtures, to satisfy the two-consecutive-clean-runs bar.

Checking is split deliberately. `evals/check_outputs.py` covers what a script does better than an
eye — file naming, canonical-file discipline, whether every commit hash and path resolves or is
explicitly marked stale, template residue, and phrase redundancy. The semantic assertions in
`evals/evals.json` were checked against the produced documents. A **negative control** (a planted
fake commit hash and fake test path appended to a passing document) confirms the checker is not
vacuous: it fails, as it should.

## 7. Acceptance results

| Criterion | Result |
|---|---|
| Clear, limited Git-backed scope | Pass — stated in `SKILL.md`; non-Git degrades to `Not applicable` |
| Production skill separated from research | Pass — `skills/` vs `research/` |
| Installable from GitHub into a clean project | Pass — verified on Bash and PowerShell paths |
| Claude discovers and invokes the skill | **Partial** — see limitations |
| `/handoff` creates one accurate dated Daily | Pass, both runs |
| `/handoff master` updates in place, no clutter | Pass, both runs — v2.0 → v3.0, no second Master, no new Daily |
| `/handoff full` performs both coherently | Pass, both runs — Daily first, Master extracted from it |
| Git state recorded accurately and only when verified | Pass — every hash and path resolves or is marked stale |
| Intended actions not presented as completed | Pass — all six runs caught the planted contradictions |
| Unsupported information clearly labelled | Pass — `gh` unavailable produced `Not verified`, never "none" |
| Immediate next action genuinely executable | Pass — where blocked, obtaining the prerequisite became the action |
| Daily and Master independently useful without duplication | Pass — literal overlap 2–7%, phrase redundancy 0.3–0.8% |
| Decisions and constraints preserved, not cut for length | Pass — numbering decision, Chrome rejection, raw-body constraint all survived |
| Output depth proportionate | **Unresolved judgement call** — see limitations |
| README explains purpose, install, usage, scope, roadmap | Pass |
| Structure supports independent future variants | Pass — a variant is a new directory, not a branch |
| Two consecutive clean fixture runs | Pass — runs A and B |
| Branch pushed, PR prepared | Pass |
| Working tree left in a known state | Pass |

Mechanical checks, runs A and B: **33/33** and **33/33**. Semantic assertions: **26/26** and
**28/28**.

**What the runs actually caught.** In every round, all three scenarios found that the repository
contradicts the session notes — a commit titled "wire rate limiter into request pipeline" whose
diff wires nothing, source files that are one-line stubs under a Master claiming the feature
works, and a "written and committed" HMAC implementation whose commit changes only comments. This
is the behaviour the skill exists for, and it is the strongest result here.

### A defect found, and a correction to how it was diagnosed

The pre-revision runs produced correct, honest, well-sourced documents that were also large:
60,839 characters across the three scenarios, including 30,296 from a 790-character session note
and a four-file repository. I initially diagnosed this as unnecessary duplication and revised the
skill accordingly.

**Measurement did not support that diagnosis, and the revision should not be credited with fixing
it.** Literal Daily-to-Master overlap measured 4–7%; content 5-gram redundancy measured 0.4–0.9%
against 0.0–0.1% for hand-written reference prose. The documents were not restating themselves.
The length came from findings the runs genuinely made. My first metric — counting how many
sections mention an identifier — conflated *mentioned in a long section* with *re-explained in
it*; it failed all three fixtures including outputs that were fine, and it has been demoted to
informational output. The gate is now the calibrated redundancy measure.

Totals across rounds: 60,839 pre-revision → 49,950 (run A) → 53,244 (run B). The reduction is
real but modest, and the A-to-B spread on identical inputs (the `g2` Master alone moved 13,268 →
9,733, and the `g3` Master moved 11,105 → 16,860) is comparable to the 27% run-to-run variance
measured in earlier iterations. **The honest reading is that the revision improved clarity and
probably trims some length, but the size deltas are not distinguishable from noise at n=2.**

One eval assertion was also wrong and has been fixed: it required signature verification to be
recorded as "implemented but untested", which encoded the fixture's own false claim. A run that
catches the contradiction and records it as *not implemented* is more correct, and now passes.

## 8. Remaining limitations

- **Skill discovery is verified structurally, not end to end.** The frontmatter parses, `name`
  matches the directory, and the files sit where Claude Code scans. Every behaviour run was
  driven by pointing an agent at the installed files, which exercises the skill's content and the
  command's routing but not automatic description-matched triggering in a live session. Running
  `/handoff` in a real session in an installed project is the remaining check, and it needs a
  human.
- **Proportionality is unresolved.** Roughly 10–17k characters per document on small fixtures may
  or may not be right. Measured repetition is low, so it is not padding — but whether this depth
  serves a reader is a judgement call. Pre-revision, run A, and run B outputs are archived side by
  side at `research/project-relay-git-v0.1.0/` for exactly this comparison.
- **n=2 per scenario.** Given known variance, treat any single number here as indicative.
- **Fixtures only.** No long-running repository, no multiple contributors, no handoff yet read by
  someone who wasn't there. That is roadmap item 2.
- **`gh` paths are lightly tested.** Every fixture ran without a reachable repository, so the
  labelled-gap behaviour is well covered but the populated PR/issue path is not.
- **No non-Git variant**, no multi-agent coordination, no archive management. Out of scope by
  design, recorded as roadmap.

## 9. Branch, commits, and pull request

Branch `feat/project-relay-git`, pushed to `origin`. Three commits:

1. `18272c8` — restructure as a variant repository, add `project-relay-git`
2. `3312ac2` — attack re-narration, not just cross-document copying
3. `f0a1e2b` — replace the re-narration gate with a calibrated redundancy measure

Plus this report and the archived run evidence. The pull request is open for review and
**has not been merged**.

## 10. Decisions still requiring approval

1. **Merging the PR.** Not done; awaiting review.
2. **Tagging `project-relay-git-v0.1.0`.** No release was cut. The install docs describe pinning
   to a tag, which will only work once one exists.
3. **Whether current output depth is acceptable**, or whether the skill should push harder toward
   brevity at the risk of dropping detail. This is the one open product question, and the archived
   documents are the evidence for deciding it.
4. **Whether to keep `research/`** (~860 KB of prior-iteration evidence) in the repository long
   term, or move it out once it stops informing the work.

