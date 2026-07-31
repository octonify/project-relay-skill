# `project-relay-git` — post-merge report

Companion to `reports/2026-07-30-project-relay-git-final-validation-report.md`. That report
recommended merging PR #1 without tagging. This one records what happened when that was carried
out, and what the public install path from `main` actually does.

The filename carries the date of the approving brief. The work itself ran on **2026-07-31**;
every timestamp and generated document below is from that date.

**Bottom line.** PR #1 merged cleanly. The documented install from `main` works, and produced an
accurate dated Daily Handoff in two consecutive clean rounds. Verification also surfaced a real
defect in a shipped script, which was fixed and merged separately (#2), and the pre-release note
in the install docs was removed (#3). No tag exists. No release exists.

---

## 1. PR #1 merge result

**Verified.**

| | |
|---|---|
| State before merge | `OPEN`, `mergeable: MERGEABLE`, `mergeStateStatus: CLEAN`, not a draft |
| Head at merge | `86a7b02f94d6b62ad3c3dbdec62ea48efc4172f1` |
| Head at validation | `86a7b02` — identical, so the validated tree is the merged tree |
| Base | `main` at `7d623d2` (contained `README.md` only) |
| Checks | none configured on the repository |
| Local tree before merge | clean, no uncommitted changes at risk |
| Report present on the remote branch | `reports/2026-07-30-project-relay-git-final-validation-report.md`, confirmed via `git ls-tree -r origin/feat/project-relay-git` |
| Merge method | merge commit, preserving the branch's individual commits |
| Result | `MERGED` at 2026-07-31T12:33:28Z |

Diff merged: **119 files changed, 19,861 insertions, 1 deletion.**

No stop condition was met at any point: the PR stayed mergeable, the head was unchanged from what
the validation covered, there were no conflicts, and no credential or permission problem arose.

## 2. Merge commit

```
9cc328b3696acdbebd62cb9e26103d4aa16a016c
Merge pull request #1 from octonify/feat/project-relay-git
```

## 3. Final `main` state

**Verified.** Local `main` fast-forwarded from `7d623d2` to the merged state, then to the two
follow-up merges below.

```
c8b60af  Merge pull request #3 from octonify/chore/post-merge-install-docs
aee0b6c  docs: drop the pre-release branch note now that #1 is merged
77f7637  Merge pull request #2 from octonify/fix/porcelain-leading-status-column
3a0b8d4  fix: keep the leading status column when reading git status --porcelain
9cc328b  Merge pull request #1 from octonify/feat/project-relay-git
86a7b02  test: end-to-end install and discovery validation, two clean rounds
```

`main` HEAD is **`c8b60af`**. Local `main` matches `origin/main`. Working tree clean apart from
this report and its evidence, which are committed in the pull request named in §7.

Top level: `.gitignore`, `CONTRIBUTING.md`, `LICENSE`, `README.md`, `docs/`, `reports/`,
`research/`, `shared/`, `skills/`.

The merged feature branch `feat/project-relay-git` still exists locally and on the remote. It was
left in place deliberately — it is the branch the validation report cites throughout, and nothing
required its removal. Delete it whenever you prefer; `main` contains all of it.

## 4. Installation from `main`

**Verified.** Test method, per the approving brief:

- A disposable Git repository built fresh for each run, in a scratch directory outside the
  development tree — a fourth project domain (`inventory-sync`, a Python stock-reconciliation
  service) chosen to be distinct from both the eval fixtures and the pre-merge end-to-end
  fixtures.
- Install by running the **Git Bash block in `docs/installation.md` verbatim, with no `--branch`
  flag**. Nothing copied from the development directory.
- `/handoff` invoked in a **fresh** `claude -p` process per run, with
  `--setting-sources project,local --strict-mcp-config --no-session-persistence`, so no
  user-global skill, plugin, or hook can supply the behaviour.
- The produced document scored mechanically against the fixture's real Git state.

Results:

| Step | Outcome |
|---|---|
| Clone default branch, no branch flag | resolves to `main`; source commit recorded per run |
| `.claude/skills/project-relay-git/SKILL.md` | present |
| `.claude/commands/handoff.md` | present |
| Context helper (`--scope check`) | correct branch, HEAD, commits, staged/unstaged/untracked, and `no origin remote configured` |
| `/handoff` in a fresh process | wrote exactly one Daily, correctly named `2026-07-31_001_stock-reconcile-handoff.md` |
| Master Handoff | correctly **not** created — the bare `/handoff` scope does not touch it |
| Mechanical score | **34/34** in each of two consecutive rounds |

Both rounds installed from `main` at `c8b60af`. Evidence:
`research/project-relay-git-v0.1.0/post-merge/`.

What the 34 checks cover: the filename pattern; the branch; the HEAD short SHA and subject; every
commit on the branch by SHA; the exact staged, unstaged, and untracked sets; that each modified
file carries the *correct* staged/unstaged label rather than a transposed one; that no upstream
branch, pull request, or issue is invented for a repository that has no remote; and that each of
four claims planted in the fixture's session notes is engaged with but never asserted as fact.

The documents came in at 14,864 and 11,506 characters for a fixture with three commits and two
modified files — consistent with the depth findings in the final validation report, and with the
~27% run-to-run size variance recorded there.

### 4.1 A defect this found

**Verified, and fixed.** The first install-from-`main` run produced this from the context helper:

```
uncommitted: 5 entries  (staged 2, unstaged 0, untracked 3)
  [staged] M nventory/adapters/warehouse.py
  [staged] M inventory/reconcile.py
```

The real state was one staged file and one unstaged file. Two errors: `warehouse.py`
misclassified as staged, and its path missing the leading `i`.

Cause: `run()` in `skills/project-relay-git/scripts/handoff_context.py` returned
`out.stdout.strip()`. In `git status --porcelain` the first column is significant — a change
existing only in the working tree is reported as `" M path"` — and stripping removed that leading
space from the **first line only**, shifting it one character left.

The bug is invisible whenever a staged path happens to sort first, which is why every earlier
fixture missed it. This fixture's unstaged path sorts first by deliberate choice.

Fixed in **PR #2** (§7): `rstrip()` instead of `strip()`, plus `evals/test_handoff_context.py` —
three parser cases and one that builds a real temporary repository with the unstaged path sorting
first. Reverting the one-line change makes that last test fail, so it is not a vacuous test.

**Worth recording on its own.** The `/handoff` run that consumed the *broken* helper output did
not propagate the error. It cross-checked against `git status --porcelain`, used the correct
reading in the document, and filed the discrepancy as an open item for the next session. The
helper was wrong; the handoff was not. That is the behaviour the skill exists to provide, observed
against an error nobody planted.

## 5. Cleanup performed

**Verified.** `docs/installation.md` carried a pre-release blockquote instructing readers to add
`--branch feat/project-relay-git` because `main` held only `README.md`. Both halves became false
at `9cc328b`.

Removed: those six lines, and nothing else — the diff is 1 file, 0 insertions, 6 deletions.

Deliberately kept, per the brief: the warning in the Update section that
`project-relay-git-v0.1.0` does not exist and that pinning to it fails with
`Remote branch project-relay-git-v0.1.0 not found in upstream origin`. That is still true.

Also untouched and still valid: the install blocks for both platforms, the "Where it lands" and
"How Claude finds it" sections, all three verification steps, the update and uninstall
instructions, and every row of the troubleshooting table — including the MSYS `/handoff`
path-mangling row, which this session's harness relied on again.

## 6. Repository changes made after the merge

Two, each in its own focused pull request:

| PR | Purpose | Merge commit |
|---|---|---|
| #2 | Fix the `git status --porcelain` leading-column bug; add regression tests | `77f7637b55ef475a1a22a3c90f5398df14e3a3cb` |
| #3 | Post-merge docs cleanup (§5) | `c8b60afaca8e7e640c1ed95a2c36c391cfb3e7b9` |

Both were validated before merging — #2 at 3 files / +116 / −1 with the new tests passing (`Ran 4
tests ... OK`), #3 at 1 file / +0 / −6. Both merged as merge commits with `MERGEABLE` / `CLEAN`
status. Their branches were deleted on merge.

PR #2 is a code change, not cleanup, so it was kept out of the cleanup PR rather than folded into
it. It also means what shipped in `9cc328b` is not quite what `main` ships now:
`skills/project-relay-git/CHANGELOG.md` records the difference under **Unreleased**, and `VERSION`
still reads `0.1.0` because 0.1.0 was never tagged or released.

## 7. This report's own pull request

This report and its evidence directory were committed on `docs/post-merge-report` and opened as
**PR #4**. A document cannot record the commit that merges it, so that one SHA is the single fact
here you will need to read from `git log main` rather than from this page. Everything else is
stated with its evidence.

## 8. Remaining limitations

1. **No tag, no release** — deliberate, and unchanged. `git ls-remote --tags origin` returns
   nothing and `gh release list` is empty. The install docs still tell readers that pinning fails.
   Until a tag exists, every installation tracks `main`, which now moves under users. **Verified.**
2. **Nothing has been used on a real project yet.** Every run to date is a fixture built for the
   purpose. The final validation report says this and it is still true; §4.1 is a reminder that
   fixtures only catch what their design happens to expose. **Verified.**
3. **The `check_outputs.py` / `test_handoff_context.py` gap.** `handoff_context.py` now has
   regression tests. Nothing else in the skill does, and `check_outputs.py` grades documents
   rather than testing code. The porcelain bug lived in the one function every Git reading passes
   through. **Verified.**
4. **`gh` was unavailable in the fixtures.** Both rounds ran against repositories with no remote,
   so the helper's GitHub path reported `unavailable` and the documents correctly recorded PR and
   issue state as unverified. The populated-`gh` path was exercised pre-merge (the live-remote
   dogfood run in `research/project-relay-git-v0.1.0/dogfood-live-remote/`), not here. **Verified
   for the pre-merge run; not re-exercised post-merge.**
5. **The scorer is a heuristic.** `verify_daily.py`'s hedge pattern was widened four times against
   *correct* skill output — a denial, a cross-reference, an interrogative, and a claim attributed
   to its source were each initially misread as assertions. To guard against a rule that accepts
   anything, the scorer plants five assertions of its own on every run and fails if any survives;
   all five are caught in both rounds. It remains a heuristic, not a proof. **Verified as
   described; the underlying judgement is not mechanical.**
6. **Round 1 was first scored by an earlier revision of the scorer.** Both rounds were re-scored
   under the final rules against preserved fixtures, so the two clean passes are comparable.
   **Verified.**
7. **`feat/project-relay-git` still exists** on the remote. Harmless, but it will drift from
   `main` now that `main` has moved. **Verified.**
8. **Section names are still pre-1.0.** `CHANGELOG.md` warns that they can change between minor
   versions and that existing documents are not migrated. Unchanged by this merge. **Verified.**

## 9. Tag and release status

**No tag was created. No release was published.**

```
$ git ls-remote --tags origin | wc -l
0
$ git tag -l | wc -l
0
$ gh release list
(no output)
```

Both remain available and both remain your call.

## 10. Evidence index

| What | Where |
|---|---|
| Post-merge harness, runs, and logs | `research/project-relay-git-v0.1.0/post-merge/` |
| Fixture builder, install script, scorer | `research/project-relay-git-v0.1.0/post-merge/harness/` |
| The run that surfaced the porcelain bug | `research/project-relay-git-v0.1.0/post-merge/defect-discovery/` |
| Round 1 — document, session log, score | `research/project-relay-git-v0.1.0/post-merge/round1/` |
| Round 2 — document, session log, score, helper output | `research/project-relay-git-v0.1.0/post-merge/round2/` |
| Pre-merge validation | `reports/2026-07-30-project-relay-git-final-validation-report.md` |
| Design history | `reports/2026-07-30-project-relay-git-implementation.md` |

## 11. Recommendation for the next phase

**Use it on one real project before tagging anything.**

The case for waiting is now stronger than it was in the final validation report, and §4.1 is why.
Eleven fixture runs across two reports missed a defect that a twelfth caught by accident of
alphabetical ordering — the class of bug fixtures are worst at finding is the one where the
fixture's own shape hides it. A real repository has messy paths, renames, submodules, detached
heads, and merge states that no fixture author thinks to build.

Concretely, for the next phase:

1. **Install from `main` into one project you actually work in**, and run `/handoff` at the end of
   real sessions for a week or two. The failure to watch for is not fabrication — the evidence is
   consistent that the skill does not fabricate — but proportionality on a repository far larger
   than any fixture, and whether the Master stays useful as Dailies accumulate.
2. **Then tag.** A tag is a promise that section names will hold, and one real project's worth of
   use is what would make that promise safe to give. Tagging now would pin users to a surface that
   `CHANGELOG.md` itself says is still moving.
3. **Consider whether `evals/` belongs in the installed payload.** It is copied into every
   project's `.claude/skills/` directory. Round 2's `/handoff` run noticed
   `test_handoff_context.py` in the tree while searching for the fixture's test suite, correctly
   excluded it as belonging to the skill, and said so in the document — the right answer, but it
   is search noise the skill creates for itself in every project it is installed into.
