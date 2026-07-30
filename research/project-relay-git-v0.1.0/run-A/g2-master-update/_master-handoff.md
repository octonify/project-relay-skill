# Master Handoff — billing

Project: billing
Document Type: Master Handoff
Version: 3.0
Last Updated: 2026-07-30
Current Phase: Invoice totals; PDF rendering paused pending an approach decision
Overall Status: In progress — test suite is red and lives outside this repository
Canonical File: docs/handoffs/_master-handoff.md

---

## 1. Executive Summary

Billing service generating invoices for the orders platform. Invoice generation and a PDF stub are
in place (`src/invoice/generate.ts`, `src/invoice/pdf.ts`); active work has moved to invoice totals
on `feat/invoice-totals`.

Two things have changed since Master v2.0 and both are load-bearing. PDF rendering is no longer in
progress: the headless-Chrome approach was measured and rejected on 2026-06-20, the spike branch
`feat/pdf-render` was deleted, and no replacement renderer has been chosen — that is now an open
decision (§10). The test suite was moved out of this repository into the shared `qa-suite`
repository on 2026-06-24 and two invoice tests fail there; v2.0's "tests passing, 24 tests" is
false (§13).

Most important blocker: nothing in this repository can be validated. The tests are elsewhere, two
of them are failing, and no location or access route for `qa-suite` is recorded anywhere in this
repo. Immediate next action is therefore to obtain that location and fix the two failing tests
(§17).

---

## 4. Repository and Project Structure

Repository: billing. **No remote is configured in this clone** (`git remote -v` is empty), so no
repository URL can be stated as verified.

Default branch: main.

Active branches (verified 2026-07-30): `main`, `feat/invoice-totals` (checked out). `feat/pdf-render`
no longer exists — see §12.

Key directories:

- `src/invoice/` — `generate.ts`, `pdf.ts`, `totals.ts`. All three are one-line stubs as of
  `1c1706b`; there is no implementation behind any of them yet.
- `docs/handoffs/` — this Master plus dated Daily Handoffs.

Tests are **not** in this repository. They live in the `qa-suite` repository under `billing/`
(reported 2026-06-24; see §6).

Ownership: no owner is named in any file in this repository. Unknown.

---

## 6. Sources of Truth

| Source | Location | Purpose | Authority | Status |
|---|---|---|---|---|
| Master Handoff | `docs/handoffs/_master-handoff.md` | Canonical project state | Authoritative | Current (this file) |
| Daily Handoffs | `docs/handoffs/YYYY-MM-DD_NNN_*.md` | Session detail, rationale, chase history | Authoritative for the session they describe | Three files, all incorporated (§19) |
| Billing source | `src/invoice/` | Implementation | Authoritative for code state | Verified at `1c1706b` |
| `qa-suite` repository | Unknown — location not recorded in this repo | Test suite for billing (`billing/` directory) | Authoritative for test status | **Not reachable from here**; see §17 |

Precedence when sources conflict: not established by anyone. Where the Master and a later Daily
disagreed, this update resolved it in the Daily's favour on evidence, not on a standing rule —
see §13.

---

## 9. Final Decisions

- Decision: Invoice numbers are sequential per tenant, not global.
- Date: 2026-05-30
- Rationale: Tenants read their own invoice numbers as a count of their own invoices.
- Status: Final. Not re-verified against code this session — `src/invoice/generate.ts` is still a
  stub, so nothing implements it yet.
- Source: `2026-05-30_001_numbering-handoff.md` (also records why UUIDs were rejected).

- Decision: Do not use headless Chrome for PDF rendering.
- Date: 2026-06-20
- Rationale: 400MB image and 6s cold start on the invoice worker — measured, not estimated.
- Impact: Closed the approach and the spike branch; left the renderer choice open (§10).
- Source: `2026-06-20_001_pdf-render-handoff.md`

- Decision: The billing test suite lives in the shared `qa-suite` repository, not in this repo.
- Date: 2026-06-24
- Rationale: Shared fixtures with the orders service.
- Impact: Test status can no longer be verified from this repository (§14).
- Source: `2026-06-24_001_test-suite-handoff.md`

---

## 10. Open Decisions

- Decision Needed: Which PDF rendering approach replaces headless Chrome.
- Why It Matters: PDF output is the deliverable of the invoice-generation phase and
  `src/invoice/pdf.ts` cannot be written past a stub until this is settled.
- Available Options: `wkhtmltopdf`, or a PDF library. Both were named on 2026-06-20; neither was
  evaluated. Headless Chrome is excluded (§9).
- Required Evidence: image size and cold-start time on the invoice worker for each candidate — the
  same two measurements that ruled out headless Chrome.
- Decision Owner: Unassigned — nobody is named in any source in this repository.
- Deadline or Trigger: blocks resuming the PDF workstream.

---

## 11. Changes Since the Previous Baseline

Against Master v2.0 (2026-06-18):

- Statuses corrected: repository state, test status, PR status, and the immediate next action were
  all stale (§13, §15).
- New decisions: PDF renderer approach rejected; test suite relocated (§9).
- New blockers: two failing invoice tests in `qa-suite`; `qa-suite` location unrecorded (§14).
- Scope change: PDF rendering paused; invoice totals started on `feat/invoice-totals`.

---

## 12. Superseded or Replaced Items

| Superseded Item | Replacement | Reason | Date |
|---|---|---|---|
| Branch `feat/pdf-render` (Master v2.0 called it active, HEAD `4b1c9de`) | None | Spike branch deleted after the approach was rejected; confirmed absent from this clone | 2026-06-20 |
| Headless Chrome as the renderer | Undecided — see §10 | 400MB image, 6s cold start | 2026-06-20 |
| `tests/invoice.spec.ts` in this repository | `qa-suite` repository, `billing/` directory | Shared fixtures with the orders service; confirmed absent from `git ls-files` | 2026-06-24 |
| Next action "Finish PDF rendering on `feat/pdf-render`" (Master v2.0) | §17 | Target branch no longer exists and the approach it assumed was rejected | 2026-07-30 |

---

## 13. Contradictions and Resolution

- Contradiction: Master v2.0 recorded "Test status: passing (`tests/invoice.spec.ts`, 24 tests)";
  the 2026-06-24 Daily records the suite moved out of the repo with two invoice tests failing.
  - Verified current state: `git ls-files` shows no `tests/` directory in this repository, which
    corroborates the move. The two failures are reported by the Daily and were **not** re-run this
    session.
  - Resolution: v2.0's line is superseded. Treat billing test status as **failing, unverified**
    until someone runs the suite in `qa-suite`.

- Contradiction: Master v2.0 recorded "Open PRs: #38 PDF rendering".
  - Verified current state: this clone has no remote, so `gh` cannot reach any repository, and the
    branch the PR was raised from was deleted on 2026-06-20.
  - Resolution: unresolved. PR #38 is an **unverified inherited claim** — most likely stale, but
    not confirmed either way. Evidence that would settle it: `gh pr view 38` against the real
    billing remote, or the PR page on the hosting service.

- Contradiction: Master v2.0 recorded HEAD at `4b1c9de`.
  - Verified current state: `git cat-file -t 4b1c9de` → "Not a valid object name". This clone
    contains exactly two commits, the earliest being the initial commit `96a6a2b`.
  - Resolution: `4b1c9de` is unreachable from here. Either this clone is not the history v2.0 was
    written against, or that history was rewritten. Do not cite `4b1c9de` as a recoverable state.

---

## 14. Risks, Constraints, and Dependencies

- **All work is local only.** No remote and no upstream tracking branch. Commits `96a6a2b` and
  `1c1706b`, and therefore every file in `src/`, exist in this working copy alone. Losing the
  directory loses the project. Verified 2026-07-30.
- **Test status cannot be verified from this repository.** The suite is in `qa-suite` and its
  location is not recorded here — a dependency with no documented access route.
- **Two billing invoice tests are failing** in `qa-suite` (reported 2026-06-24, not re-verified;
  cause and detail in `2026-06-24_001_test-suite-handoff.md`). Any claim that billing code works is
  unbacked until they pass.
- The PDF workstream is stalled on the open renderer decision (§10).
- `.claude/` is untracked and there is no `.gitignore`, so it will be swept into the next
  `git add -A`.

---

## 15. Current Technical State

Verified 2026-07-30 unless marked otherwise.

```
Repository:               billing (no remote configured)
Default branch:           main
Active branches:          main, feat/invoice-totals (checked out)
HEAD of active branch:    1c1706b "feat: invoice totals scaffold"
                          feat/invoice-totals is 1 commit ahead of main, 0 behind
Uncommitted work:         untracked .claude/ only; nothing staged or modified
Unpushed work:            everything — no remote, no upstream
Stashes / tags:           none
Open PRs:                 Unknown — unverified inherited claim of PR #38, see §13
Open issues:              Unknown — no remote to query
Build status:             Not verified as of 2026-07-30 — no build run
Test status:              Failing and off-repo — 2 invoice tests in qa-suite, see §13/§14
Migration status:         Not applicable — no migrations in this repository
Deployment status:        Not verified as of 2026-07-30 — v2.0's "staging up to date"
                          (2026-06-18) has not been rechecked and predates two sessions
CI/CD status:             None found in this repository
```

Both commits in this clone are dated 2026-07-30 and the initial one contains the May and June
handoff documents, so `git log` dates do not indicate when the work described was done. Use the
Daily filenames for chronology.

---

## 17. Immediate Next Action

```
Immediate Next Action:    Obtain the qa-suite repository location and access, then fix the two
                          failing billing invoice tests in its billing/ directory.
Responsible Role or Agent: Next session
Start From:               Ask the billing project owner for the qa-suite repository URL and read
                          access. No owner is named anywhere in this repository, so identifying
                          who to ask is part of this step. Once cloned, start at the billing/
                          fixture setup: the reported cause is fixture paths left absolute after
                          the 2026-06-24 move.
Required Inputs:          qa-suite repository URL and credentials — Unknown, not recorded here.
Expected Deliverable:     Both invoice tests passing, and the qa-suite location recorded in §6 of
                          this document so the next session does not repeat this search.
Acceptance Criteria:      A test run observed by you, green, with the run output cited.
Dependencies:             Access to qa-suite. Nothing else blocks it.
Stop Conditions:          If the fix needs changes to billing source rather than fixtures, stop and
                          record it — that changes the scope from a test fix to a code defect.
Do Not Change:            Do not re-add a tests/ directory to this repository; the move was a final
                          decision (§9). Do not force-push or rewrite history — there is no remote
                          copy to recover from.
```

**Prioritized queue after that:**

1. Configure a remote and push `main` and `feat/invoice-totals`. The project currently exists in
   one directory (§14).
2. Settle the PDF renderer decision (§10) by measuring image size and cold start for `wkhtmltopdf`
   and a PDF library, then resume `src/invoice/pdf.ts`.
3. Implement `src/invoice/totals.ts` beyond the `1c1706b` scaffold.
4. Confirm or close PR #38 (§13).

---

## 18. New-Session Start Guide

1. Read first: this file, then `2026-06-20_001_pdf-render-handoff.md` and
   `2026-06-24_001_test-suite-handoff.md` for the two changes that invalidated the old Master.
2. Canonical source: this file. Dailies are authoritative for the sessions they describe.
3. Current state: §15. Verify it rather than trusting it — it is several sessions old the moment
   it is written.
4. Start here: §17.
5. Final decisions: §9. Per-tenant invoice numbering, no headless Chrome, tests live in `qa-suite`.
6. Do not repeat: headless-Chrome PDF rendering, already measured and rejected (§9); do not look
   for the deleted `feat/pdf-render` branch or commit `4b1c9de` (§13); do not move tests back into
   this repository (§9).
7. Access required: `qa-suite` repository — not currently held (§17).
8. Requires explicit human approval: adding a remote and pushing this history anywhere; any history
   rewrite or force-push, since no remote copy exists to recover from.

---

## 19. Incorporated Daily Handoffs

| Date | Handoff File | Scope | Incorporated into Master |
|---|---|---|---|
| 2026-05-30 | 2026-05-30_001_numbering-handoff.md | Invoice numbering | Yes (v2.0) |
| 2026-06-20 | 2026-06-20_001_pdf-render-handoff.md | PDF rendering spike; approach rejected | Yes (v3.0) |
| 2026-06-24 | 2026-06-24_001_test-suite-handoff.md | Test suite moved to qa-suite | Yes (v3.0) |

No Daily exists for the work on `feat/invoice-totals` (`1c1706b`); it is recorded here from
repository state only.
