# Master Handoff — billing

Project: billing
Document Type: Master Handoff
Version: 3.0
Last Updated: 2026-07-30
Current Phase: Invoice totals (PDF rendering paused — approach undecided)
Overall Status: In progress, unvalidated
Canonical File: docs/handoffs/_master-handoff.md

---

## 1. Executive Summary

Billing service that generates invoices for the orders platform (purpose inherited from Master
v2.0; not independently verified this session).

Against the repository at `08ac70d`, the code is still scaffolding: `src/invoice/generate.ts`,
`src/invoice/pdf.ts`, and `src/invoice/totals.ts` are one-line stubs. Master v2.0's claim that
"invoice generation works" is not supported by the tracked source and has been superseded — see
section 13.

Current work is invoice totals on branch `feat/invoice-totals`. PDF rendering is paused: the
headless-Chrome approach was measured and rejected on 2026-06-20, the spike branch
`feat/pdf-render` was deleted, and no replacement approach has been chosen.

Most important constraint: this repository can no longer validate anything on its own. The test
suite was moved to a shared QA repository on 2026-06-24, two invoice tests have been failing there
since the move, and `package.json` defines no scripts. There is also **no Git remote configured**,
so both commits on this branch exist only in this working copy.

Immediate next action: implement line-item totalling in `src/invoice/totals.ts` (section 17).

---

## 4. Repository and Project Structure

Repository: `billing` (local Git repository; **no remote configured** — verified 2026-07-30 with
`git remote -v`, which returned nothing). No canonical URL is recorded anywhere in the repository
or in any handoff.

Default branch: `main` (at `e5c2f57`).

Active branches (verified 2026-07-30, `git branch -a`):

| Branch | HEAD | Note |
|---|---|---|
| `feat/invoice-totals` | `08ac70d` | Currently checked out; the active work |
| `main` | `e5c2f57` | Default branch |

`feat/pdf-render` no longer exists — deleted after the rejected spike (see section 12).

Key directories:

- `src/invoice/` — `generate.ts`, `pdf.ts`, `totals.ts`, all stubs as of `08ac70d`.
- `docs/handoffs/` — this Master plus dated Daily Handoffs.
- Tests: **not in this repository.** They live in the `qa-suite` repository under `billing/`. The
  location, URL, and access path of `qa-suite` are not recorded anywhere; see section 14.

Ownership: not recorded. Nobody has been named as owner in any handoff.

Untracked in the working copy: `.claude/` (agent skill and command install; not project source).

---

## 8. Important Project History

- **2026-05-30 —** Invoice numbering fixed as per-tenant sequential; UUIDs rejected as unreadable
  to accountants (Daily: `2026-05-30_001_numbering-handoff.md`).
- **2026-06-20 —** Headless Chrome rejected for PDF rendering on measured cost; spike branch
  `feat/pdf-render` deleted, leaving PDF rendering with no chosen approach (Daily:
  `2026-06-20_001_pdf-render-handoff.md`).
- **2026-06-24 —** Test suite moved out of `billing` into the shared `qa-suite` repository to share
  fixtures with the orders service; two invoice tests broke in the move and were left failing
  (Daily: `2026-06-24_001_test-suite-handoff.md`).
- **2026-07-30 —** Two commits landed locally: `e5c2f57` (invoice generation and PDF stubs, plus
  the handoff docs) and `08ac70d` (totals scaffold). Neither is pushed anywhere.

---

## 9. Final Decisions

- Decision: Invoice numbers are sequential per tenant, not global.
- Date: 2026-05-30
- Rationale: Tenants read their own invoice numbers as a count of their own invoices; a global
  sequence leaks volume to competitors.
- Impact: Numbering is per-tenant state; a global counter must not be introduced.
- Source: `2026-05-30_001_numbering-handoff.md`
- Status: Final. **Not verified in code** — no numbering implementation exists in `src/invoice/`
  as of `08ac70d`, so this is a decision awaiting implementation, not an implemented behaviour.

---

- Decision: Do not use headless Chrome for PDF rendering.
- Date: 2026-06-20
- Rationale: Measured at a 400MB image and 6s cold start on the invoice worker.
- Impact: PDF rendering has no chosen approach; see section 10. `src/invoice/pdf.ts` is a stub.
- Source: `2026-06-20_001_pdf-render-handoff.md`
- Status: Final. Measured, not estimated — do not re-spike it.

---

## 10. Open Decisions

- Decision Needed: Which PDF rendering approach replaces headless Chrome.
- Why It Matters: `src/invoice/pdf.ts` cannot be implemented until this is settled, and it was the
  project's stated focus before the rejection.
- Available Options: `wkhtmltopdf`, or a PDF library (both listed as considered in
  `2026-06-20_001_pdf-render-handoff.md`; neither was evaluated).
- Required Evidence: image size and cold-start time on the invoice worker, measured the same way
  as the headless-Chrome baseline of 400MB / 6s, so the numbers are comparable.
- Decision Owner: Unassigned.
- Deadline or Trigger: Before any further work on `src/invoice/pdf.ts`.

---

## 11. Changes Since the Previous Baseline

Baseline: Master v2.0, 2026-06-18. Dailies incorporated in this update:
`2026-06-20_001_pdf-render-handoff.md`, `2026-06-24_001_test-suite-handoff.md`.

Statuses corrected:

- Active branch was `feat/pdf-render` at `4b1c9de`; that branch no longer exists. The active branch
  is `feat/invoice-totals` at `08ac70d`.
- "Test status: passing (tests/invoice.spec.ts, 24 tests)" is dead — that file is no longer in the
  repository. Last known status is two invoice tests failing in `qa-suite` (2026-06-24), not
  re-checked since.
- "Uncommitted or unpushed work: none" is wrong in a way that matters: there is no remote, so
  `e5c2f57` and `08ac70d` are unpushed by definition.
- "No blockers" replaced — the missing validation path and the undecided PDF approach are recorded
  in sections 10 and 14.

New decisions: headless Chrome rejected (section 9).

Superseded: PDF-rendering next action, `feat/pdf-render`, the in-repo test suite (section 12).

Architecture / scope changes: testing moved out of this repository into `qa-suite`; the phase moved
from PDF rendering to invoice totals by default, not by a recorded decision.

New blockers: no way to validate changes from inside this repository; `qa-suite` location and
access unrecorded.

Resolved blockers: none.

---

## 12. Superseded or Replaced Items

| Superseded Item | Replacement | Reason | Date |
|---|---|---|---|
| Branch `feat/pdf-render` (`4b1c9de`) | None | Spike branch deleted after the approach was rejected; nothing on it was worth keeping | 2026-06-20 |
| Headless Chrome PDF rendering | Undecided — see section 10 | 400MB image, 6s cold start, measured | 2026-06-20 |
| `tests/invoice.spec.ts` in `billing` (24 tests) | `qa-suite` repository, `billing/` directory | Shared fixtures with the orders service | 2026-06-24 |
| Master v2.0 next action ("Finish PDF rendering on feat/pdf-render") | Section 17 below | Both the branch and the approach are gone | 2026-07-30 |
| Master v2.0 "Invoice generation works" | Section 13 | Contradicted by the tracked source | 2026-07-30 |

---

## 13. Contradictions and Resolution

- Contradiction: Master v2.0 states "Invoice generation works; PDF rendering is the current focus",
  but every file in `src/invoice/` is a one-line stub.
- Conflicting sources: Master v2.0 (2026-06-18) vs. the tracked source at `08ac70d`.
- Verified current state: `generate.ts` is `export const generate = () => {};`, `pdf.ts` is
  `export const render = () => {};`, `totals.ts` is `export const total = () => 0;`. Read directly
  on 2026-07-30. `main` at `e5c2f57` carries the same stubs.
- Authoritative source: the repository.
- Resolution: treat invoice generation as **not implemented**. No working implementation exists in
  any branch of this working copy.
- Reason for precedence: code observed now outranks a document written six weeks ago.
- Corrective action required: if a working implementation exists in a clone or fork that this
  working copy cannot see, record where — there is no remote to look at, so nobody can find it from
  this repository alone.

---

- Contradiction: Master v2.0 lists "Open PRs: #38 PDF rendering", but there is no remote and no
  GitHub repository reachable from here.
- Conflicting sources: Master v2.0 vs. `git remote -v` (empty) and `gh` (could not reach any
  repository), both checked 2026-07-30.
- Verified current state: unresolvable from this working copy.
- Resolution: PR #38 is recorded as an **unverified inherited claim**. Its branch was deleted and
  its approach rejected, so if it still exists it should probably be closed — but that has not been
  observed, and nobody should assume it either way.
- Corrective action required: whoever has the hosting URL should check #38 and close it if it is
  still open against the deleted `feat/pdf-render`.

---

## 14. Risks, Constraints, and Dependencies

Active risks:

- **Local-only history.** No remote is configured, so `e5c2f57` and `08ac70d` — the entire project
  history — exist in one working copy. Losing the directory loses the project.
- **Nothing can be validated here.** The test suite left the repository and `package.json` declares
  no scripts, so no change made in `billing` can be shown to work without the `qa-suite` repository.
- **Two invoice tests have been failing since 2026-06-24** in `qa-suite`, caused by absolute fixture
  paths that survived the move. Not fixed. Not re-checked this session, so the count could now be
  different.

Constraints:

- PDF rendering must not reintroduce headless Chrome (section 9).
- Invoice numbering must remain per-tenant sequential (section 9).

Dependencies:

- `qa-suite` repository, `billing/` directory — the only place the tests live. Its URL, host, and
  access requirements are **not recorded anywhere**; obtaining them is a prerequisite for any
  validation work.
- Orders platform — shares fixtures with the billing suite, which is why the suite moved.

---

## 15. Current Technical State

All values below were verified on 2026-07-30 unless the line says otherwise.

Repository: `billing`, local Git repository, **no remote configured**
Default branch: `main` at `e5c2f57`
Active branches: `feat/invoice-totals` (checked out), `main`
HEAD of active branch: `08ac70d` — "feat: invoice totals scaffold"
Uncommitted or unpushed work: working tree clean apart from untracked `.claude/`; no upstream
tracking branch exists, so **both commits are unpushed**
Open PRs: Unknown — no remote, `gh` could not reach a repository. Master v2.0's "#38 PDF rendering"
is an unverified inherited claim; see section 13
Open issues: Unknown — same reason
Build status: Unknown — not run this session. `package.json` (name `billing`, version 1.2.0)
declares no scripts and no dependencies, so there is no build command to run
Test status: **No tests in this repository.** Last known result, from
`2026-06-24_001_test-suite-handoff.md`: two invoice tests failing in `qa-suite` due to absolute
fixture paths. Not re-run since 2026-06-24
Migration status: Not applicable — no migrations exist in the repository
Deployment status: Unknown. Master v2.0 said "staging up to date" on 2026-06-18; that is an
unverified inherited claim and predates every commit in the current history
Environment status: Unknown — not checked
CI/CD status: Unknown — no CI configuration is tracked in the repository

---

## 17. Immediate Next Action

Immediate Next Action: Implement line-item totalling in `src/invoice/totals.ts`, replacing the
stub `export const total = () => 0;`.
Responsible Role or Agent: Next session on `billing`.
Start From: branch `feat/invoice-totals` at `08ac70d` — already checked out. File:
`src/invoice/totals.ts`.
Required Inputs: the totals rules — tax handling, discounts, rounding, currency. **None of these
are recorded in this repository or in any handoff.** Implement the plain sum of line items only,
and stop before anything that needs a rule you cannot cite.
Expected Deliverable: a commit on `feat/invoice-totals` in which `total` sums line items, plus a
note in the next Daily Handoff naming exactly which rules were assumed and which were left out.
Acceptance Criteria: `total` returns the sum of the supplied line items; no rounding, tax, or
discount behaviour is invented. Note that this **cannot be proven by a test run from this
repository** — there is no test harness here (section 14).
Dependencies: none for the plain sum. Anything beyond it depends on the missing rules above.
Stop Conditions: stop and ask if the work requires tax, rounding, or currency semantics; stop
before touching `src/invoice/pdf.ts`, which is blocked on the open decision in section 10.
Do Not Change: `docs/handoffs/` history files; per-tenant invoice numbering; do not re-add a test
directory to `billing` (it was deliberately moved out); do not revive headless Chrome.

**Prioritized queue after that:**

1. Obtain the `qa-suite` repository location and access, then fix the two failing invoice tests
   (absolute fixture paths, broken since 2026-06-24). Until this is done, nothing in `billing` can
   be validated. Ask whoever owns the orders-platform QA repository — no name is recorded, so
   identifying that person is part of the task.
2. Decide the PDF rendering approach (section 10), gathering the image-size and cold-start numbers
   that make it comparable to the rejected 400MB / 6s baseline.
3. Configure a Git remote and push `main` and `feat/invoice-totals`. The entire history is
   currently local-only.
4. Establish who owns this project; several sections above say "Unassigned" only because nobody has
   ever been named.

---

## 18. New-Session Start Guide

1. **Read first:** this file, then `src/invoice/` (three files, one line each — read them, they set
   expectations correctly).
2. **Canonical source:** this file, `docs/handoffs/_master-handoff.md`. Daily Handoffs hold session
   detail and rationale; they are historical records and are never edited after the fact.
3. **Current state:** on `feat/invoice-totals` at `08ac70d`; the code is scaffolding; no remote;
   no local tests.
4. **Start here:** section 17.
5. **Final decisions:** per-tenant sequential invoice numbering; no headless Chrome for PDF.
6. **Do not repeat:** the headless-Chrome PDF spike — 400MB image, 6s cold start, measured not
   guessed (`2026-06-20_001_pdf-render-handoff.md`). Do not look for `feat/pdf-render`; it was
   deleted. Do not look for `tests/` in this repository; it moved to `qa-suite`.
7. **Access required:** the `qa-suite` repository (location unrecorded — see section 14), and a Git
   host for `billing` if one exists.
8. **Requires explicit human approval:** configuring a remote and pushing this history for the
   first time; any change to the per-tenant numbering decision; choosing the PDF rendering
   approach.

---

## 19. Incorporated Daily Handoffs

| Date | Handoff File | Scope | Incorporated into Master |
|---|---|---|---|
| 2026-05-30 | `2026-05-30_001_numbering-handoff.md` | Invoice numbering | Yes (v2.0) |
| 2026-06-20 | `2026-06-20_001_pdf-render-handoff.md` | PDF rendering spike, approach rejected | Yes (v3.0) |
| 2026-06-24 | `2026-06-24_001_test-suite-handoff.md` | Test suite moved to `qa-suite` | Yes (v3.0) |
