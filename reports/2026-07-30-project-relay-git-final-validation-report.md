# `project-relay-git` — final validation report

Date: 2026-07-30
Branch: `feat/project-relay-git`
Pull request: [#1](https://github.com/octonify/project-relay-skill/pull/1) — open, not merged
Scope: end-to-end installation and behaviour validation of the first Project Relay variant

Evidence labels used throughout:

| Label | Meaning |
|---|---|
| **Verified** | Observed directly this session by running a command or reading the produced file |
| **Reported** | Stated by a generated document or a tool, and cross-checked against the repository |
| **Inferred** | A conclusion drawn from evidence, not a direct observation |
| **Unverified** | Could not be checked with the access available |
| **Blocked** | Requires a decision or action that is not mine to take |

---

## 1. Executive conclusion

`project-relay-git` installs from GitHub into a clean project and behaves correctly in genuinely
fresh Claude Code sessions. All four behaviour tests passed in **two consecutive rounds**, against
freshly rebuilt fixtures, with the skill reinstalled from the pushed branch between rounds.
Combined: **148/148** fact checks and **76/76** mechanical checks across the two rounds.

The single largest open question from the previous report is now closed. **Natural-language
discovery works** — a fresh session given only `Wrap this up so I can resume tomorrow.`, with no
slash command and no mention of the word "handoff", selected the skill and produced a correct
Daily Handoff. It did this in both rounds. *(Verified.)*

Three defects were found and fixed. **None were in the skill's behaviour.** All three were in the
material around it: a bundled evaluation script hard-coded to its own test fixture, an
installation document describing a state the repository is not in yet, and a Git Bash argument
mangling issue worth documenting. The skill's runtime files — `SKILL.md`, `references/`,
`assets/`, `scripts/`, `commands/` — **were not modified during this validation at all**, so both
rounds exercised byte-identical behaviour. *(Verified: `git log -- <those paths>` shows the last
change at `3312ac2`, three commits before this work began.)*

On output depth: the documents are long, and the length is **justified**. Measured phrase
redundancy across all 23 generated documents ranges 0.0%–2.4% against a 5% gate and a 0.0%–0.1%
hand-written-prose baseline. The length is carrying findings, not repetition — see section 10.

**Recommendation: ready to merge, not yet ready to tag.** Details and reasoning in section 17.

---

## 2. Work performed

1. Confirmed no background validation work was outstanding. The previous live-remote dogfood run
   had completed and is committed at `8f0b00b`. *(Verified: `TaskList` empty.)*
2. Built four disposable Git projects in a scratch directory outside the development repository,
   in a different problem domain (`checkout-service`) from the existing eval fixtures, so the
   results are independent evidence rather than a rerun of the eval suite.
3. Ran the documented installation procedure verbatim to test its accuracy in the current
   pre-merge state.
4. Installed the skill into all four fixtures from the pushed GitHub branch and verified the
   installed bytes matched the pushed commit.
5. Ran four behaviour tests, each in its own fresh headless Claude Code process with the fixture
   as project root.
6. Verified every generated document against the fixture's real Git state with a purpose-built
   checker, plus the skill's own bundled checker.
7. Built a negative control to prove the fact checker was not vacuous.
8. Fixed three defects, committed and pushed them.
9. Rebuilt all fixtures from scratch, reinstalled from the updated branch, and reran everything
   for a second consecutive clean round.
10. Assessed output depth against all prior rounds.

Harness and outputs are archived under
`research/project-relay-git-v0.1.0/e2e-validation/` (`harness/`, `round1/`, `round2/`).

### Fixtures

Each fixture plants at least one trap — a claim in a human-written note that the repository
itself contradicts, or state that cannot be verified from inside the fixture.

| Fixture | Used by | Git state | Planted traps |
|---|---|---|---|
| `fx-a-daily` | Test A | branch `feat/idempotency-keys`, 2 commits, 1 staged / 1 unstaged / 2 untracked, **no remote** | Session notes claim "ran the test suite, all green" (no test script or test file exists) and "Opened PR #14" (no remote to check) |
| `fx-b-natural` | Test B | identical build to `fx-a-daily`, separate directory | same |
| `fx-c-master` | Test C | branch `feat/refund-flow`, **local bare remote**, deliberately diverged **ahead 2 / behind 1**, stale Master v3.0, 2 unincorporated Dailies | Master claims `feat/legacy-cart` active (deleted), "passing (48 tests)" (no tests exist), "deployed to staging" (uncheckable), PR #31 |
| `fx-d-full` | Test D | branch `feat/webhook-verify`, 2 commits, no remote, no Master | HEAD commit message says "implement HMAC signature verification"; its diff changes **comment lines only** |

Builder: `research/project-relay-git-v0.1.0/e2e-validation/harness/build_e2e_fixtures.py`.
Fixtures were deleted after evidence was preserved.

---

## 3. Installation method tested

Installed from the **pushed GitHub branch**, never copied from the development directory.

```bash
git clone --depth 1 --branch feat/project-relay-git \
  https://github.com/octonify/project-relay-skill.git "$TMP"
mkdir -p .claude/skills .claude/commands
cp -r "$TMP/skills/project-relay-git" .claude/skills/project-relay-git
cp "$TMP/skills/project-relay-git/commands/handoff.md" .claude/commands/handoff.md
```

Script: `harness/install_from_github.sh`.

**Provenance is proven, not assumed.** Every one of the 14 installed files was compared by Git
blob hash against the same path at the pushed commit:

```
files compared: 14   mismatches: 0
```

Round 1 installed from `8f0b00b`; round 2 from `ad84868`. *(Verified.)*

### The documented procedure is inaccurate pre-merge — now fixed

Running `docs/installation.md` verbatim fails today. The documented `git clone` targets the
default branch, and `main` currently contains only `README.md`:

```
=== what did we get? ===
README.md
=== does skills/ exist? ===
ls: cannot access '/tmp/project-relay-skill/skills': No such file or directory
```

*(Verified by running the documented commands unmodified.)* The `cp` step then fails. This was
previously noted as a PR comment; it is now fixed in the document itself with a delete-on-merge
marker. See section 11.

### Verification checks from the document

| Check | Result |
|---|---|
| 1. Files in place | **Pass** — `SKILL.md` and `handoff.md` present |
| 2. Helper runs against the repository | **Pass** — correct branch, HEAD, and staged/unstaged/untracked split |
| 3. Claude actually uses it | **Pass** — see sections 4–7 |

---

## 4. Fresh-session discovery results

Each test ran as a separate `claude -p` process with the fixture as its project root — a real
Claude Code session, not a subagent. User-level settings were excluded (`--setting-sources
project,local`) so no globally installed skill, plugin, or hook could contaminate the result.
Isolation was confirmed by asking a session to enumerate what it could see: only the fixture's own
skills appeared, with no user-global entries.

**Both skill and command are discovered.** A fresh session in an installed fixture listed:

```
Skills:
- project-relay-git
- handoff
```

*(Verified.)*

### Test B — natural-language discovery: **PASS, twice**

The prompt was exactly `Wrap this up so I can resume tomorrow.` — no slash command, no mention of
"handoff", no other instruction, and no prior conversation.

| Round | Skill selected | File produced | Fact checks | Mechanical |
|---|---|---|---|---|
| 1 | Yes | `docs/handoffs/2026-07-30_001_idempotency-keys-handoff.md` | 18/18 | 7/7 |
| 2 | Yes | `docs/handoffs/2026-07-30_001_idempotency-replay-handoff.md` | 18/18 | 7/7 |

It also caught both planted traps unprompted. From the round-1 session:

> two claims from `SESSION-NOTES.md` — "tests all green" and "PR #14 opened" — couldn't be
> verified from this checkout (no test script in `package.json`, no git remote configured) and
> are flagged as unverified rather than stated as fact

**This closes the limitation carried in the previous report.** No description change was needed,
so the section 7 correction loop in the brief was never entered. *(Verified.)*

---

## 5. `/handoff` result — Test A

Fixture `fx-a-daily`. Expected: exactly one dated Daily, no Master.

| Round | Daily | Chars | Fact checks | Mechanical | Redundancy |
|---|---|---|---|---|---|
| 1 | `2026-07-30_001_idempotency-keys-handoff.md` | 11,479 | 18/18 | 7/7 | 0.2% |
| 2 | `2026-07-30_001_idempotency-keys-handoff.md` | 11,775 | 18/18 | 7/7 | 0.2% |

Correctly recorded: branch, both commit hashes, the staged/unstaged/untracked split, absence of a
remote, the per-merchant scoping decision, the abandoned middleware approach as do-not-repeat,
Marta as the blocker owner, and an executable next action. No Master was created.

**It found something no input contained.** From the round-1 session:

> A gap I verified in code but wasn't in the session notes: `remember()` is defined but never
> called anywhere — so no replay actually works yet.

That is true of the fixture, was not in the session notes, and materially changes what the next
person does. *(Verified: `remember` appears only in its own definition in
`src/lib/idempotency.ts`.)*

---

## 6. `/handoff master` result — Test C

Fixture `fx-c-master`. Expected: the existing Master updated in place, no new Daily, no second
Master file, stale claims corrected, both Dailies folded in.

| Round | Master | Version | Chars | Fact checks | Mechanical | Redundancy |
|---|---|---|---|---|---|---|
| 1 | modified in place | 3.0 → 4.0 | 7,709 | 21/21 | 13/13 | 0.4% |
| 2 | modified in place | 3.0 → 4.0 | 4,851 | 21/21 | 13/13 | 0.0% |

Verified in both rounds: no second Master under any name; both pre-existing Dailies untouched and
marked incorporated; the async-202 decision and the observed 5/second rate ceiling carried across
from the Dailies; the synchronous-refund approach preserved as do-not-repeat; production refund
credentials recorded as the blocker.

**All four stale inherited claims were handled correctly**, none carried forward silently:

| Stale claim in v3.0 | How the update handled it |
|---|---|
| `feat/legacy-cart` is active | "was deleted — see section 13" |
| "Test status: passing (48 tests)" | "No automated test suite exists in this repo (package.json defines no test script). The 'passing (48 tests)' figure in v3.0 referred to the deleted legacy-cart branch." |
| "deployed to staging 2026-06-10" | "Not verified for the refund flow … does not apply here." |
| PR #31 open | "presumed stale per section 13 but was not independently reverified" |

**Upstream divergence was detected and stated correctly** — this is the first run in the project's
history to exercise a populated upstream. The fixture was built ahead 2 / behind 1, and the
document reported exactly that, naming the diverging commit and making reconciliation the
immediate next action. *(Verified against `git rev-list --left-right --count`.)*

---

## 7. `/handoff full` result — Test D

Fixture `fx-d-full`. Expected: one dated Daily plus a new Master at Version 1.0, coherent with
each other, with no block duplicated in full across both.

| Round | Daily | Master | Fact checks | Mechanical | Daily / Master redundancy | Cross-doc overlap |
|---|---|---|---|---|---|---|
| 1 | 11,855 | 16,134 (v1.0) | 17/17 | 11/11 | 0.4% / 1.3% | 7% |
| 2 | 9,075 | 13,011 (v1.0) | 17/17 | 11/11 | 1.1% / 1.5% | 11% |

Cross-document overlap is well inside the 20% gate in both rounds, so the two documents are
genuinely different views rather than one document written twice.

**The planted contradiction was caught in both rounds.** The HEAD commit message claims HMAC
verification was implemented; the diff changes only comment lines. From the round-2 session:

> `a6269c1` ("implement HMAC signature verification") only adds two comment lines — no
> verification logic exists … I verified against the actual diffs and marked that claim superseded
> rather than carrying it forward.

The Master's Contradictions section names the conflicting sources, the verified state, the
authoritative source, and why it takes precedence. Also correctly preserved: the
raw-body-before-JSON-parser constraint as durable, "do not rewrite `src/lib/webhook.ts`", Dana and
the signing secret as the blocker, and that nothing is deployed and no PR exists.

Worth noting as a sign the skill's own rules are being followed rather than recited — the Master's
Sources of Truth section states:

> Precedence when sources conflict: Not established by anyone.

That is exactly the behaviour `references/master-handoff.md` asks for: an invented precedence rule
is worse than none.

---

## 8. Live remote and pull-request detection

The three original eval fixtures are local repositories with no remote, so every earlier run
recorded PR and issue state as `Not verified`. That exercised the labelled-gap path only. Two runs
have now exercised the populated path:

**This repository, via PR #1** *(Verified, re-confirmed this session):*

```
GITHUB       PR #1 for this branch: Add project-relay-git: the first installable Project Relay variant
             open issues: 0
GIT          origin=https://github.com/octonify/project-relay-skill.git
             vs origin/feat/project-relay-git: ahead 0, behind 0
```

The earlier dogfood run recorded PR #1 as verified fact with number, state and counts, and
recorded `reviewDecision` as "no review submitted" rather than reading an empty value as approval
— the distinction the evidence rule exists for. Archived at
`research/project-relay-git-v0.1.0/dogfood-live-remote/`.

**`fx-c-master`, via a local bare remote** — covered in section 6. This is the stronger of the two
for upstream reporting, because the divergence was constructed to a known value and the document
reproduced it exactly.

Remaining gap: no run has exercised a repository with **open issues** or **multiple open PRs**;
both fixtures had zero issues and at most one PR. *(Unverified — low risk, since the same `gh`
code path produces both, but not claimed as tested.)*

---

## 9. Factual-reliability findings

Every generated document was checked against the fixture's actual Git state.
Checker: `harness/verify_facts.py` with `harness/spec.json`.

| Category | Result |
|---|---|
| Branch | **Verified correct** in all 8 document sets |
| HEAD commit | **Verified correct** in all 8 |
| Remote | Correct in all 8 — present and named where one exists, absence stated where not |
| Upstream tracking | Correct — `ahead 2, behind 1` reproduced exactly; "no upstream" stated where absent |
| Staged changes | Correct, and distinguished from unstaged in all 8 |
| Unstaged changes | Correct in all 8 |
| Untracked files | Correct in all 8 |
| Commits | No invented hashes; every cited hash resolves via `git cat-file` |
| Pull requests | Correct — PR #1 reported as fact where real; PR #14 and PR #31 labelled unverified/stale |
| Issues | No invented issues |
| Tests | **No document claimed tests were run or passing.** Both "all green" claims labelled |
| Builds | No invented build status |
| Migrations | Not present in any fixture; recorded as "Not applicable — no migrations found in the repo" |
| Deployments | No invented deployments; inherited claims labelled |
| Approvals | **No invented approvals** — the highest-risk category, clean in all 8 |
| Owners | Only Marta and Dana, both named in the session notes; neither invented |
| Intended vs completed actions | Kept distinct throughout; planned work stayed planned |
| Unknown state | Labelled rather than guessed |

**A planned action remained planned, and a reported action never became verified, in every
document.** *(Verified.)*

A separate sweep over all generated documents for claims about infrastructure that does not exist
in any fixture — stashes, tags, migrations, CI pipelines, build status, deployments, approvals —
returned **zero unhedged claims**. Every match was a correct negation ("No automated test suite
exists", "Not applicable — no migrations found in the repo", "Nothing is deployed"), a template
section heading, or the Redis migration genuinely discussed in the session notes.

### The checker is not vacuous

The hedge vocabulary was widened five times while chasing false positives on correct output.
Widening a rule until nothing fails is indistinguishable from deleting it, so a negative control
plants claims that genuinely should fail and confirms they still do:

| Injected claim | Caught |
|---|---|
| "PR #14 is open and has been reviewed and approved by the platform team." | Yes — 2 checks |
| "The test suite was executed this session and all tests are passing." | Yes |
| "This branch was deployed to staging and verified end to end." | Yes |
| "feat/legacy-cart is the current focus and PR #31 is awaiting review." | Yes — 2 checks |
| "HMAC signature verification works and was confirmed against a sample payload." | Yes — 2 checks |

```
controls caught: 5   controls missed: 0
```

Script: `harness/negative_control.sh`. *(Verified, re-run after the final checker change.)*

---

## 10. Handoff-depth assessment

**Verdict: the current depth is justified. No revision made.**

Phrase redundancy across all 23 archived generated documents, against a 5% gate and a hand-written
prose baseline of 0.0%–0.1%:

| Run | Documents | Total chars | Redundancy range |
|---|---|---|---|
| pre-revision | 4 | 60,839 | 0.4% – 0.9% |
| run A | 4 | 49,950 | 0.0% – 0.8% |
| run B | 4 | 53,244 | 0.3% – 0.8% |
| dogfood (live remote) | 1 | 12,999 | 0.0% |
| e2e round 1 | 5 generated | 56,306 | 0.2% – 1.3% |
| e2e round 2 | 5 generated | 48,711 | 0.0% – 2.4% |

Cross-document overlap on the `full` case: 7% (round 1) and 11% (round 2), against a 20% gate.

**The documents are not repeating themselves.** The highest value observed anywhere is 2.4%, less
than half the gate.

Structural evidence, from the round-1 `fx-d-full` Master (16,134 chars, the largest document
produced):

- 15 of the reference's 20 sections used; **5 dropped as not applicable**. The "menu, not
  checklist" framing is being followed.
- Largest section 1,793 chars; mean ~1,075. No section is padded — each is roughly a paragraph.
- Pointers are used instead of restatement: the Workstream section ends `Next Action: See section
  18` rather than repeating it.
- The length carries findings absent from every input: the commit-message-versus-diff
  contradiction, the fact that `handleWebhook` is wired to no route, and that the raw-body
  constraint is documented in a comment but implemented nowhere.

**A caution against reading the size trend as improvement.** Between rounds 1 and 2 the *inputs
were identical* and the skill was byte-identical, yet sizes moved substantially:

| Document | Round 1 | Round 2 | Change |
|---|---|---|---|
| A Daily | 11,479 | 11,775 | +2.6% |
| B Daily | 9,129 | 9,999 | +9.5% |
| C Master | 7,709 | 4,851 | **−37%** |
| D Daily | 11,855 | 9,075 | −23% |
| D Master | 16,134 | 13,011 | −19% |

This matches the ~27% run-to-run variance measured earlier in the project. It means the apparent
shrinkage from pre-revision (60,839) to run A (49,950) **cannot be attributed to the revision** at
these sample sizes, and I am not claiming it. It also means any future length tuning needs more
than one run per condition to detect.

Applying the brief's principles: facts required to resume safely are present; decisions,
constraints, blockers, evidence and a first executable next action are present; no source file or
transcript is reproduced; explanations are not repeated across sections (measured); no fixed
character limit was introduced; and nothing was removed to hit a number.

---

## 11. Corrections made

All in commit `ad84868`. **No skill behaviour file was touched.**

### 11.1 `check_outputs.py` was hard-coded to its own test fixture

`skills/project-relay-git/evals/check_outputs.py:261` asserted `len(dailies) == 3` and a prior
Version of literally `"2.0"` — both specific to the `g2` eval fixture. This script **ships inside
the skill**, so a user running it on their own repository after `/handoff master` got a failure
that said nothing about their output. Found when it reported `expected the 3 fixture Dailies,
found 2` against `fx-c-master`, which correctly has 2.

Fixed by deriving both baselines from Git — `count_tracked_dailies()` and
`prior_master_version()` — with `--baseline-dailies` and `--baseline-version` overrides, and by
skipping the count check rather than inventing a baseline when the handoff directory is untracked.

Regression-checked against the original fixture: the derived values are **3 and 2.0**, reproducing
the previous behaviour exactly. *(Verified.)*

### 11.2 Bare `Supersedes: N/A` was reported as unfilled template residue

On a decision entry that is a real answer — it says someone checked and this decision replaces
nothing, which tells a reader more than an omitted line does. Added a small allowlist of fields
where emptiness is itself the finding (`supersedes`, `dependencies`, `stop conditions`,
`do not change`, and similar). Bare `N/A` is still flagged everywhere else.

### 11.3 `docs/installation.md` described a state the repository is not in

Three corrections, all evidence-backed:

- A pre-release note that the skill is on `feat/project-relay-git` until #1 merges, with the
  branch flag and a delete-on-merge marker. *(The documented clone was verified to fail.)*
- A note that the pin-to-a-tag example names a tag that does not exist yet. *(Verified: `git tag
  -l` is empty.)*
- A troubleshooting row for MSYS rewriting a scripted `claude -p "/handoff"` into
  `C:/Program Files/Git/handoff` on Git Bash. This is a **harness artifact, not a skill defect** —
  it bit this validation before `MSYS_NO_PATHCONV=1` was set, and typing `/handoff` inside an
  interactive session is unaffected. Notably, even when handed the mangled path the session did
  not invent a document; it asked what was meant.

### Corrections considered and rejected

- **Widening the fact checker's hedge vocabulary further.** Four of the five e2e "failures" in
  round 1 were my checker's vocabulary gaps, not skill defects. The fifth revealed a design error
  in the check itself: requiring every mention of `signature verification` to be hedged is wrong,
  because that phrase is the *name of the workstream* and appears in objective statements that are
  goals, not claims. Replaced with a positive requirement that the not-implemented finding be
  stated, plus the existing prohibition on success claims — the negative control confirms this
  still catches a document asserting it works. The "hedge every mention" shape is right for
  discrete identifiers (a PR number, a branch, a hash) and wrong for topic phrases.
- **Shortening the output.** Not supported by the measurements — see section 10.
- **Changing the skill description.** Natural-language discovery passed twice without it.

---

## 12. Tests repeated and consecutive-pass evidence

Round 2 rebuilt all four fixtures from scratch (new commit hashes), reinstalled the skill from the
updated branch, and reran all four tests in fresh processes.

| Test | Command | R1 facts | R1 mech | R2 facts | R2 mech |
|---|---|---|---|---|---|
| A | `/handoff` | 18/18 | 7/7 | 18/18 | 7/7 |
| B | *(natural language)* | 18/18 | 7/7 | 18/18 | 7/7 |
| C | `/handoff master` | 21/21 | 13/13 | 21/21 | 13/13 |
| D | `/handoff full` | 17/17 | 11/11 | 17/17 | 11/11 |
| **Total** | | **74/74** | **38/38** | **74/74** | **38/38** |

Negative control: 5/5 caught, both before and after the final checker change.

**Two honest caveats about what "consecutive" means here.**

1. The round-1 mechanical scores for C (13/13) and D (11/11) are **post-fix re-evaluations**. As
   first run they were 12/13 and 10/11, and both failures were the checker defects in sections
   11.1 and 11.2. The round-1 *documents* were not regenerated — the checker was corrected and
   rerun against the same unchanged files. The fact-check scores (21/21, 17/17) are also
   post-fix, for the checker-design reasons in section 11.
2. Because `check_outputs.py` is not invoked by the skill at runtime (*verified*: no reference to
   it in `SKILL.md`, `commands/`, or `references/`) and no runtime file changed, **both rounds
   exercised byte-identical skill behaviour**. The two rounds are therefore a genuine repeat of
   the same behaviour against freshly built inputs.

---

## 13. Remaining limitations

- **Interactive sessions are untested.** All runs used `claude -p` (headless). Interactive
  behaviour is *inferred* to be the same — the same skill-loading path — but not observed.
- **A single model and platform.** Windows, Git Bash and PowerShell, one model. Cross-platform
  behaviour is *unverified*.
- **No repository with open issues or multiple open PRs** has been exercised (section 8).
- **No repository with stashes, tags, or submodules.** The helper has code paths for stashes and
  tags that no run has populated. *(Unverified.)*
- **Two rounds is a small sample.** Given the ~27% size variance measured on identical inputs,
  two rounds establishes that the behaviour is repeatable, not that it is reliable at a
  quantified rate.
- **Long-horizon Master behaviour is untested.** The most a Master has been updated is once, from
  v3.0 to v4.0. How it holds up over dozens of updates — whether it accretes or stays usable — is
  *unverified* and is the kind of thing only real use will show.
- **`user`-level settings were excluded** for isolation. A user with conflicting global skills or
  hooks might see different triggering behaviour. *(Unverified.)*
- The MSYS path-mangling issue is documented but **not fixed**, because it is not the skill's to
  fix.

---

## 14. Files changed

Commit `ad84868` (2 files, +68 / −5):

| File | Change |
|---|---|
| `skills/project-relay-git/evals/check_outputs.py` | Fixture-independent Master baselines; `N/A` allowlist; two new CLI flags |
| `docs/installation.md` | Pre-release branch note; tag-does-not-exist note; MSYS troubleshooting row |

This commit, adding evidence and this report:

| Path | Change |
|---|---|
| `reports/2026-07-30-project-relay-git-final-validation-report.md` | New — this document |
| `research/project-relay-git-v0.1.0/e2e-validation/harness/` | New — fixture builder, installer, fact checker, spec, negative control |
| `research/project-relay-git-v0.1.0/e2e-validation/round1/` | New — round-1 documents and session logs |
| `research/project-relay-git-v0.1.0/e2e-validation/round2/` | New — round-2 documents and session logs |

Research evidence is kept under `research/`, separate from the production skill under `skills/`.

---

## 15. Branch and commit state

```
Branch:   feat/project-relay-git
Upstream: origin/feat/project-relay-git
Remote:   https://github.com/octonify/project-relay-skill.git
```

Commits on the branch, oldest first:

| Commit | Summary |
|---|---|
| `18272c8` | feat: restructure as a variant repository, add project-relay-git |
| `3312ac2` | fix: attack re-narration, not just cross-document copying |
| `61d9408` | fix: replace the re-narration gate with a calibrated redundancy measure |
| `e5d1d37` | docs: implementation report and archived validation evidence |
| `9b89f78` | docs: correct a commit hash in the implementation report |
| `8f0b00b` | test: close the gh-populated gap with a live-remote dogfood run |
| `ad84868` | fix: decouple the checker from its own fixture, correct pre-merge install docs |

Last skill **behaviour** change: `3312ac2`. Everything after it is evaluation, documentation, or
evidence.

---

## 16. PR #1 status

| Field | Value |
|---|---|
| URL | https://github.com/octonify/project-relay-skill/pull/1 |
| State | **OPEN — not merged** |
| Base ← Head | `main` ← `feat/project-relay-git` |
| Draft | No |
| Review decision | None submitted |
| Tag `project-relay-git-v0.1.0` | **Does not exist** |

No merge was performed, no tag created, no release published, per the standing instruction that
those require explicit approval. *(Blocked — awaiting your decision.)*

---

## 17. Recommendation

### Ready to merge, but not yet ready to tag.

**Why merge.** The variant does what it claims, from a clean install, in fresh sessions, twice.
Both discovery paths work. Factual reliability held across every category, including the ones
where a wrong answer is most damaging — approvals, test results, deployments. The skill found
genuine defects it was not looking for: an uncalled function, a commit message contradicting its
own diff, a stale Master claim about a deleted branch. Merging also **removes the largest
remaining install defect by itself**, because the documented `git clone` of `main` starts working
the moment #1 lands.

**Why not tag yet.** Tagging `v0.1.0` is a promise of a stable surface, and two things argue for
waiting:

1. **Section names are still moving.** `CHANGELOG.md` already warns that section names change
   between pre-1.0 versions and that existing documents are not migrated. A tag invites people to
   pin, and pinning to a surface that is still settling creates upgrade pain that does not exist
   yet.
2. **Nobody has used it for real.** Every run so far is a fixture I built or this repository
   dogfooding itself. The long-horizon Master question in section 13 — whether a Master stays
   usable after twenty updates — cannot be answered by any test I can construct, only by use.

**Suggested sequence:**

1. Merge #1. Then delete the pre-release note in `docs/installation.md` (it carries a
   delete-on-merge marker) and confirm the documented install now works from `main`.
2. Use it on one real project for a week or two.
3. Tag `project-relay-git-v0.1.0` once the section names have survived contact with real use.

If you would rather tag now to make the pinning instructions honest immediately, that is a
reasonable call and the evidence does not argue against it — but the reasoning above is why I am
not recommending it.

**Both actions remain blocked pending your explicit approval.**
