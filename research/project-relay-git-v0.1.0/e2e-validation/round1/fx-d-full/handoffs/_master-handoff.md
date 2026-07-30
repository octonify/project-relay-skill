# Master Handoff — checkout-service

Project: checkout-service
Document Type: Master Handoff
Version: 1.0
Last Updated: 2026-07-30
Current Phase: Webhook signature verification — early/incomplete, despite commit history suggesting otherwise (see section 13)
Overall Status: Baseline checkout API working. Webhook verification not yet functional: no route exists, no signature-checking code exists, and there is no signing secret to test against even once written.
Canonical File: docs/handoffs/_master-handoff.md

---

## 2. Executive Summary

What the project is: `checkout-service` — a Node + TypeScript payment checkout API for the storefront (`README.md`).

Primary objective (current workstream): Add inbound webhook handling from the payment provider, with HMAC signature verification, so the service stops accepting unauthenticated payment-event payloads.

Current phase: Scaffolding only. A stub `handleWebhook()` exists but performs no verification and is not wired to any HTTP route.

Latest major progress: Baseline checkout service (`POST /charge`) is committed on `main` at `7bef393`. A `feat/webhook-verify` branch exists with two more commits, but see the blocker below before trusting their messages.

Most important blocker: No provider signing secret (inherited, unverified claim — someone named Dana is reportedly chasing it; not confirmed this session). Independently of the secret, the webhook route itself has not been built yet either.

Immediate next action: See section 18.

---

## 4. Locked Principles and Decisions

- **Decision:** Signature verification must run against the raw request body, before `express.json()` parses it, because the provider signs the exact bytes sent.
  - Rationale: JSON re-serialization changes byte-for-byte content, so a signature computed over parsed-then-reserialized JSON will never match. (Inherited from `SESSION-NOTES.md`; not yet implemented or independently tested — see section 15.)
  - Date: Discovered before 2026-07-30 (exact date unknown; not recorded).
  - Status: Locked as a design constraint, not yet realized in code.
  - Approval source: Inherited note, no named approver.
  - Supersedes: N/A
- **Decision:** `express.raw()` for the webhook path must be scoped to that route only, never applied globally in `src/server.ts`.
  - Rationale: Every other route (currently `POST /charge`) needs `express.json()`; a global raw-body parser would break it.
  - Date: Not recorded.
  - Status: Locked as a design constraint, not yet implemented (no webhook route exists yet at all).
  - Approval source: Inherited note.
  - Supersedes: N/A
- **Decision:** Do not rewrite `src/lib/webhook.ts` from scratch; extend it in place.
  - Rationale: The file is intended to be the structural home of the raw-body ordering constraint above. As of 2026-07-30 the file is a small stub with no functional logic to lose, but it remains the designated extension point.
  - Date: Not recorded.
  - Status: Locked (procedural).
  - Approval source: Inherited note.
  - Supersedes: N/A

---

## 5. Repository and Project Structure

Repository / URL: Local only — no `origin` remote is configured (verified 2026-07-30).

Default branch: `main`, currently at `7bef393` ("chore: baseline checkout service").

Branching model: Not documented anywhere in the repo; observed pattern is a feature branch (`feat/webhook-verify`) off `main`.

Protected branches: Unknown — no remote, so no branch protection could exist to check.

Environments and the branch that feeds each: Not documented; no deployment configuration found in the repo.

Key directories (from `README.md` and direct observation):
- `src/routes/` — HTTP handlers (currently just `charge.ts`)
- `src/lib/` — shared helpers (`money.ts`, `webhook.ts`)
- `docs/` — design notes (`design.md`, and now `handoffs/`)

Ownership: Not documented. "Dana" is referenced in an inherited note as chasing the provider's integrations team, but no role or ownership over this codebase is stated anywhere.

---

## 7. Sources of Truth

| Source | Location | Purpose | Authority | Status |
|---|---|---|---|---|
| This Master Handoff | `docs/handoffs/_master-handoff.md` | Canonical current project state | Authoritative | Current |
| Daily Handoffs | `docs/handoffs/*-handoff.md` | Session-level detail behind Master entries | Authoritative for their session | Current |
| Design notes | `docs/design.md` | Design rationale (currently: charges are synchronous, idempotency is a known gap) | Authoritative for what it covers | Current, narrow scope |
| `SESSION-NOTES.md` (repo root, untracked) | Informal handover note | Superseded — its claims about HMAC being implemented do not match the code; reconciled into this Master and the 2026-07-30 Daily | Superseded, kept for reference | Do not treat as current |
| `notes/handover.md` (untracked) | One-line note | Corroborates the "two weeks off from Friday" absence window | Minor, corroborating | Current |

Precedence when sources conflict: Not established by anyone. Where `SESSION-NOTES.md` conflicted with the actual repository state this session, the repository state (git history + file contents) was treated as authoritative — see section 13 for the specific contradiction and its resolution.

---

## 8. Workstream Status

### Webhook Signature Verification

Purpose: Verify inbound provider webhook payloads via HMAC signature so the service stops accepting unauthenticated payment events.

Owner: Unassigned in the repo. "Dana" is chasing the signing secret from the partner's integrations team (inherited, unverified claim).

Current Status: Blocked / early — far less complete than the branch's commit messages suggest.

Completed: Nothing functional. A stub `handleWebhook(rawBody)` exists in `src/lib/webhook.ts` that only checks the body is non-empty; it performs no signature check.

In Progress: Nothing actively — no route wiring, no verification logic written.

Blocked: HMAC verification logic cannot be tested end-to-end without the provider's signing secret. The route + raw-body wiring, however, does **not** depend on the secret and could be built now.

Open Decisions: None new; the design constraints in section 4 are locked, just not yet implemented.

Dependencies: Provider's signing secret (external, via Dana / partner integrations team — unverified).

Next Action: See section 18.

Relevant Sources: `src/lib/webhook.ts`, `src/server.ts`, Daily `docs/handoffs/2026-07-30_001_webhook-verify-handoff.md`.

---

## 9. Important Project History

- **2026-07-30 —** Baseline checkout service established on `main` (`7bef393`): `POST /charge`, `toMinorUnits` helper.
- **2026-07-30 —** `feat/webhook-verify` branch created; `handleWebhook()` stub added (`ea172e1`) and a comment documenting the raw-body ordering constraint added (`a6269c1`). Neither commit's message accurately reflects its diff — see section 13. Detail: Daily `docs/handoffs/2026-07-30_001_webhook-verify-handoff.md`.

---

## 13. Superseded or Replaced Items

| Superseded Item | Replacement | Reason | Date |
|---|---|---|---|
| `SESSION-NOTES.md` claim: "Wrote the HMAC verification and committed it." | This Master (sections 2, 8) + Daily `2026-07-30_001_webhook-verify-handoff.md` | Verified against `git show a6269c1 -- src/lib/webhook.ts`: the commit adds only two comment lines, no signature-checking logic, no crypto import. The function `handleWebhook` is functionally unchanged from the previous commit. | 2026-07-30 |
| Commit message `a6269c1` "feat(webhook): implement HMAC signature verification" (as a description of actual progress) | Same as above | Message overstates the diff; do not amend the commit (do not rewrite shared history), but do not trust the message as a progress indicator either. | 2026-07-30 |
| Commit message `ea172e1` "feat(webhook): inbound webhook entry point" (as a description of actual progress) | Same as above | No route is registered anywhere in `src/server.ts` or `src/routes/` that calls `handleWebhook`; only a bare function was added. There is no actual HTTP entry point yet. | 2026-07-30 |

---

## 14. Contradictions and Resolution

- Contradiction: `SESSION-NOTES.md` states HMAC verification was written and committed. The actual diff at `a6269c1` shows only two added comment lines.
- Conflicting sources: `SESSION-NOTES.md` (untracked note) vs. `git show a6269c1 -- src/lib/webhook.ts` and the current content of `src/lib/webhook.ts`.
- Verified current state: `src/lib/webhook.ts` contains no signature verification; `handleWebhook(rawBody)` returns `{ ok: true }` for any non-empty body.
- Authoritative source: Git history and current file content (directly observed 2026-07-30).
- Resolution: Treat HMAC verification as **not implemented**. Section 13 above records the supersession.
- Reason for precedence: Git diffs and live file contents are directly verifiable; the note is a secondhand narrative that was not cross-checked before being written.
- Corrective action required: Implement the actual verification logic (see section 18). No corrective action needed on the note itself — it's left in place per source-of-truth table in section 7, but marked superseded.

---

## 15. Risks, Constraints, and Dependencies

Active risks:
- Commit messages on `feat/webhook-verify` overstate completed work (see sections 13–14). Anyone relying on `git log` alone would believe verification is implemented when it is not.
- No test framework exists in this repository at all (`package.json` has only `build` and `start` scripts) — even once the signing secret arrives, verification logic will need a test setup built from nothing.

Constraints:
- Signature verification must run against the raw request body, before `express.json()` — see locked decision in section 4. Not yet implemented.
- Any raw-body middleware must be scoped to the webhook route only, not applied globally — see locked decision in section 4.

Dependencies:
- Provider's HMAC signing secret, external, via the partner's integrations team (inherited, unverified claim that Dana is chasing this).

Failure points:
- If the webhook route is built and deployed before verification logic exists, the service would accept unauthenticated payment events — the exact problem this workstream exists to fix. Do not deploy the route ahead of verification.

Mitigations:
- This Master and the 2026-07-30 Daily now state the accurate implementation status, correcting the inherited note.

---

## 16. Current Technical State

Repository: Local git repo, no `origin` remote configured (verified 2026-07-30).
Default branch: `main`, at `7bef393`.
Active branches: `feat/webhook-verify` (local only, no upstream), at `a6269c1`, 2 commits ahead of `main`.
HEAD of active branch: `a6269c1` "feat(webhook): implement HMAC signature verification" (message inaccurate, see section 13).
Uncommitted or unpushed work: 3 untracked entries on `feat/webhook-verify`: `.claude/` (tooling), `SESSION-NOTES.md`, `notes/`. No staged or unstaged changes to tracked files. Nothing is pushed anywhere (no remote).
Open PRs: Not verified — no remote configured, `gh` could not look anything up.
Open issues: Not verified, same reason.
Build status: Not verified this session — `npm run build` (`tsc -p .`) was not run.
Test status: Not applicable — no test framework or test script exists in the project.
Migration status: Not applicable — no migrations found in the repo.
Deployment status: Nothing deployed (inherited claim from `SESSION-NOTES.md`, consistent with there being no deployment configuration found in the repo).
Environment status: Not documented anywhere in the repo.
CI/CD status: Not applicable — no CI/CD configuration found in the repo.

---

## 17. Current Project State

Current phase: Webhook verification workstream is in early scaffolding, not the near-complete state its commit messages imply.

Latest approved output: None — nothing has been reviewed or approved for this workstream.

Active work: None in progress at session end; work is paused pending the signing secret and, independently, pending someone building the actual route.

Completed work: Baseline checkout service on `main` (`POST /charge`, `toMinorUnits`).

Incomplete work: Webhook route registration, raw-body middleware scoping, HMAC verification logic, tests (no framework exists yet).

Blockers: Provider signing secret (inherited/unverified — see section 15). Note the route + wiring work is not blocked by this and could proceed independently.

Open decisions: None new — see Locked Principles (section 4) for what's already settled.

Readiness for next phase: Not ready. No route exists to receive a webhook at all yet.

Overall status: Blocked / early, with the added complication that the existing commit history and an informal note both overstate progress — corrected in this document.

---

## 18. Immediate Next Action

Immediate Next Action: Build the webhook HTTP route: register it in `src/server.ts` scoped with `express.raw()` (not global), have it call `src/lib/webhook.ts`'s `handleWebhook` (extend, don't rewrite). This does not require the signing secret and can start immediately. In parallel, confirm with Dana (or whoever owns the partner relationship) whether the signing secret has arrived.
Responsible Role or Agent: Unassigned.
Start From: `src/server.ts` (route registration) and `src/lib/webhook.ts` (verification logic).
Required Inputs: Provider's HMAC signing secret — required only for the verification logic itself, not for the route/wiring.
Expected Deliverable: A registered webhook route receiving the raw body correctly, plus (once the secret is available) real HMAC verification replacing the current stub.
Acceptance Criteria: Valid provider signature → accepted. Invalid or missing signature → rejected. `POST /charge` continues to receive parsed JSON as before (no regression from scoping the raw-body parser).
Dependencies: Signing secret, for the verification-logic portion only.
Stop Conditions: Do not deploy the route until verification logic is actually in place (see Failure Points, section 15) — a route with no working verification would be worse than no route.
Do Not Change: Do not rewrite `src/lib/webhook.ts` from scratch (section 4). Do not apply `express.raw()` globally.

**Prioritized queue after that:**

1. Once verification works against a real or provided test signature, add a test framework and at least one test proving invalid signatures are rejected (none exists today).
2. Open a PR once there's a remote to open it against, and once the route + verification are both real (not just scaffolding) — there is no PR today.

---

## 19. New-Session Start Guide

1. Read first: This Master, then the latest Daily (`docs/handoffs/2026-07-30_001_webhook-verify-handoff.md`) for how the discrepancy in section 13/14 was found.
2. Canonical source: This file, `docs/handoffs/_master-handoff.md`.
3. Current state: Section 16 above — verify branch/HEAD again before acting, since state may have moved.
4. Start here: Section 18, Immediate Next Action.
5. Final decisions: Section 4 (locked design constraints — raw body ordering, scoped `express.raw()`, extend-not-rewrite).
6. Do not repeat: Don't trust `a6269c1` / `ea172e1` commit messages as progress indicators (section 13). Don't treat `SESSION-NOTES.md` as current state without cross-checking — it has already been found inaccurate once.
7. Access required: None identified for the route/wiring work. The provider's signing secret is required for the verification-logic portion; source unknown beyond "Dana is chasing the partner's integrations team" (unverified).
8. Requires explicit human approval: Deploying the webhook route to any environment, and merging `feat/webhook-verify` — neither should happen before verification logic is real and at least minimally tested.

---

## 20. Incorporated Daily Handoffs

| Date | Handoff File | Scope | Incorporated into Master |
|---|---|---|---|
| 2026-07-30 | `2026-07-30_001_webhook-verify-handoff.md` | Verify webhook-verification branch state; reconcile against `SESSION-NOTES.md` | Yes — sections 2, 4, 5, 7, 8, 9, 13, 14, 15, 16, 17, 18 |
