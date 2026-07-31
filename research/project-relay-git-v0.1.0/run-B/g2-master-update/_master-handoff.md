# Master Handoff — billing

Project: billing
Document Type: Master Handoff
Version: 3.0
Last Updated: 2026-07-30
Current Phase: Invoice totals (PDF rendering paused on an undecided approach)
Overall Status: In progress — active work uncommitted to any remote
Canonical File: docs/handoffs/_master-handoff.md

---

## 1. Executive Summary

Billing service generating invoices for the orders platform. Active work has moved off PDF
rendering and onto invoice totals: branch `feat/invoice-totals` at `5107edd` carries a scaffold of
`src/invoice/totals.ts`.

PDF rendering is paused, not in progress: headless Chrome was measured and rejected on 2026-06-20,
the spike branch `feat/pdf-render` was deleted, and no replacement renderer has been chosen (open
decision, section 10). The previous Master's "no blockers" no longer holds.

Two facts a reader must not skip: this clone has **no Git remote**, so every commit here exists
only on this machine; and the test suite no longer lives in this repository — it moved to the
`qa-suite` repo on 2026-06-24 with two invoice tests failing, unfixed.

Immediate next action: implement `src/invoice/totals.ts` on `feat/invoice-totals` (section 17).

## 4. Repository and Project Structure

Repository: billing (`package.json` name `billing`, version `1.2.0`)
Remote: none configured — `git remote -v` is empty as of 2026-07-30
Default branch: main
Active branches: `main` at `8cd79f9`, `feat/invoice-totals` at `5107edd` (1 commit ahead of main)
Deleted branch: `feat/pdf-render` — spike branch, removed 2026-06-20, nothing on it worth keeping
Key directories: `src/invoice/` — `generate.ts`, `pdf.ts`, `totals.ts`
Tests: not in this repository; see `qa-suite`, `billing/` directory (section 14)

## 9. Final Decisions

- Decision: Invoice numbers are sequential per tenant, not global.
- Date: 2026-05-30
- Rationale: Tenants read their own invoice numbers as a count of their own invoices.
- Source: `2026-05-30_001_numbering-handoff.md`

- Decision: Do not use headless Chrome for PDF rendering.
- Date: 2026-06-20
- Rationale: 400MB image and 6s cold start on the invoice worker — measured, not estimated.
- Impact: `src/invoice/pdf.ts` has no renderer behind it; see open decision below.
- Source: `2026-06-20_001_pdf-render-handoff.md`

## 10. Open Decisions

- Decision Needed: Which PDF rendering approach replaces headless Chrome.
- Why It Matters: `src/invoice/pdf.ts` is a stub and cannot be implemented until this is settled.
- Available Options: `wkhtmltopdf`, a PDF library. (Headless Chrome is closed — section 9.)
- Required Evidence: image size and cold-start cost on the invoice worker, measured the same way
  the Chrome spike was, so the numbers are comparable.
- Decision Owner: Unassigned — nobody named in any handoff or commit.
- Deadline or Trigger: Blocks any further work on PDF rendering.

## 11. Changes Since the Previous Baseline (Master 2.0, 2026-06-18)

- Incorporated `2026-06-20_001_pdf-render-handoff.md` and `2026-06-24_001_test-suite-handoff.md`,
  neither of which had reached the Master.
- Corrected repository state wholesale: branch, HEAD, test location, and the absence of a remote
  (section 15). Every field of the old section 15 was stale or unverifiable.
- New work not covered by any Daily: commits `8cd79f9` and `5107edd`, both dated 2026-07-30.
  Recorded here from repository evidence only; there is no session record of their intent.
- New blocker: PDF rendering has no chosen approach (section 10).
- Carried-over blocker, previously unrecorded in the Master: two failing invoice tests in
  `qa-suite` (section 14).
- Phase changed from "Invoice generation" to invoice totals, following the branch and commits.

## 12. Superseded or Replaced Items

| Superseded Item | Replacement | Reason | Date |
|---|---|---|---|
| Branch `feat/pdf-render` (`4b1c9de` in Master 2.0) | None — approach abandoned | Headless Chrome rejected; branch deleted | 2026-06-20 |
| `tests/invoice.spec.ts` in this repo, "24 tests passing" | `qa-suite` repo, `billing/` directory | Shared fixtures with the orders service | 2026-06-24 |
| Next action "Finish PDF rendering on feat/pdf-render" | Section 17 | Named a branch that no longer exists | 2026-07-30 |

## 13. Contradictions and Resolution

Both open contradictions share one likely root: **this working copy may not be the canonical
billing repository.** It has no remote and contains only stubs. That is unconfirmed — treat it as
the first thing to settle.

- Contradiction: Master 2.0 recorded "Open PRs: #38 PDF rendering", but this clone has no remote
  and `gh` could not reach any repository on 2026-07-30.
  - Verified current state: unknown. PR #38 was neither confirmed nor refuted this session.
  - Evidence that would settle it: locating the canonical repository and running `gh pr view 38`.

- Contradiction: Master 2.0 said "Invoice generation works", but at `5107edd` all three modules are
  one-line no-ops — `generate.ts` returns nothing, `pdf.ts` returns nothing, `totals.ts` returns 0.
  - Verified current state: stubs only, in this clone.
  - Evidence that would settle it: the same repository question above.

## 14. Risks, Constraints, and Dependencies

- **No remote.** Every commit in this clone exists on one machine only, unbacked and unshared.
  Verified 2026-07-30. Configuring a remote is queued in section 17.
- **Untracked tooling.** `.claude/` (skill and slash-command definitions) is untracked and not
  ignored. It will follow no clone of this repo.
- **External test dependency.** The billing test suite lives in the `qa-suite` repository,
  `billing/` directory (URL not recorded anywhere; not verified this session). Nothing in this
  repository can be validated by tests without access to it.
- **Two failing invoice tests** in `qa-suite`, caused by absolute fixture paths, open since
  2026-06-24 and not fixed. Detail: `2026-06-24_001_test-suite-handoff.md`.
- **PDF renderer constraint.** Any candidate must beat 400MB / 6s cold start on the invoice
  worker — that is the bar Chrome failed.

## 15. Current Technical State

Verified 2026-07-30 by direct inspection of this working copy.

Repository: billing (local only, no remote)
Default branch: main
Active branches: `main` `8cd79f9`, `feat/invoice-totals` `5107edd`
HEAD of active branch: `feat/invoice-totals` at `5107edd` "feat: invoice totals scaffold"
Uncommitted or unpushed work: nothing staged or modified; `.claude/` untracked. No remote exists,
so **both branches are unpushed in their entirety**.
Stashes / tags: none
Open PRs / issues: Unknown — `gh` unavailable, no remote to query. See section 13.
Build status: Not verified — no build run this session
Test status: Not run, and not runnable from this repository (suite lives in `qa-suite`). Last
observed result: two invoice tests failing, 2026-06-24.
Deployment status: Unverified inherited claim — "staging up to date" as of Master 2.0, 2026-06-18;
nothing has confirmed it since.
Migration / environment / CI state: Unknown — no evidence in this repository

## 17. Immediate Next Action

Immediate Next Action: Implement invoice totals in `src/invoice/totals.ts`, replacing the scaffold
committed at `5107edd`.
Responsible Role or Agent: Unassigned
Start From: `src/invoice/totals.ts` on branch `feat/invoice-totals` (currently
`export const total = () => 0;`)
Required Inputs: The totals rules to apply — not recorded in any handoff or commit; confirm them
before coding rather than inferring them from the scaffold.
Expected Deliverable: A `total` implementation on `feat/invoice-totals`.
Acceptance Criteria: `total` computes from invoice input instead of returning the constant `0`,
and per-tenant sequential numbering (section 9) is not disturbed.
Dependencies: Verification requires the `qa-suite` repository — this repo has no tests.
Do Not Change: `src/invoice/pdf.ts` — it is stubbed pending the open renderer decision, not
half-finished. Do not re-create `feat/pdf-render`.

**Prioritized queue after that:**

1. Configure a remote and push both branches — until then all work is unbacked (section 14).
2. Settle the PDF renderer decision with measured numbers (section 10).
3. Fix the two failing invoice tests in `qa-suite` (absolute fixture paths).
4. Resolve whether this clone is the canonical billing repository (section 13), which also
   answers the PR #38 question.

## 18. New-Session Start Guide

1. Read first: this file, then `2026-06-20_001_pdf-render-handoff.md` and
   `2026-06-24_001_test-suite-handoff.md` if you touch PDF rendering or tests.
2. Canonical source: this file. The Dailies hold detail; where they disagree with a verified
   state field in section 15, section 15 wins.
3. Current state: section 15. Do not assume anything is pushed — nothing is.
4. Start here: section 17.
5. Final decisions: section 9 — per-tenant invoice numbering, and no headless Chrome.
6. Do not repeat: the headless Chrome spike (measured and rejected), and do not look for
   `tests/` or `feat/pdf-render` in this repository — both are gone.
7. Access required: the `qa-suite` repository, for any test run.
8. Requires explicit human approval: adding a remote or pushing, since where this code belongs is
   itself unresolved (section 13).

## 19. Incorporated Daily Handoffs

| Date | Handoff File | Scope | Incorporated into Master |
|---|---|---|---|
| 2026-05-30 | 2026-05-30_001_numbering-handoff.md | Invoice numbering | Yes |
| 2026-06-20 | 2026-06-20_001_pdf-render-handoff.md | PDF rendering spike | Yes — 3.0 |
| 2026-06-24 | 2026-06-24_001_test-suite-handoff.md | Test suite move | Yes — 3.0 |

No Daily exists for the 2026-07-30 commits (`8cd79f9`, `5107edd`); the Master covers them from
repository evidence alone.
