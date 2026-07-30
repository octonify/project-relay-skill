# Master Handoff — checkout-service

Project: checkout-service
Document Type: Master Handoff
Version: 1.0
Last Updated: 2026-07-30
Current Phase: Webhook signature verification — early implementation, blocked on external input
Overall Status: Blocked
Canonical File: docs/handoffs/_master-handoff.md

---

## 1. Executive Summary

What the project is: `checkout-service` — a Node/TypeScript payment checkout API for the storefront (see `README.md`), currently exposing a synchronous `POST /charge` route.

Primary objective (current workstream): Verify inbound provider payment webhooks via HMAC signature checking. Today the endpoint concept accepts anything, which is not shippable.

Current phase: Design decided, scaffold committed, no verification logic written yet.

Latest major progress: `src/lib/webhook.ts` stub created and commented (commits `70206b0`, `0e8f943` on branch `feat/webhook-verify`). No route wiring, no HMAC code, no test coverage exist yet — see §13 for a correction to what the commit history itself claims.

Most important blocker: No provider signing secret. Without it, no valid test signature can be constructed, so verification cannot be written and confirmed correct in the same step. Dana is chasing the partner's integrations team for it (status of that chase not verifiable from this repo).

Immediate next action: See §17.

---

## 2. Project Purpose and Definition

Problem being solved: Inbound provider webhooks for payment events are currently unauthenticated/unverified.

Primary objective: Implement HMAC-based signature verification on the webhook endpoint before it can be trusted or shipped.

Intended final output: A webhook route that verifies the provider's signature against the raw request body and rejects invalid/tampered requests.

Success criteria: A genuine provider signature validates; a tampered payload or signature is rejected. (Stated by outgoing engineer this session; not yet formally reviewed.)

Current scope: Signature verification for the webhook endpoint only.

Out of scope: Idempotency handling for `/charge` retries — noted as a separate, pending concern in `docs/design.md`, not part of this workstream.

---

## 3. Locked Principles and Decisions

- **Decision:** Signature verification must run against the raw request body, before `express.json()` parses it.
  - Rationale: The provider signs the exact bytes sent; once JSON-parsed and reserialised, the signature no longer matches.
  - Date: 2026-07-30
  - Status: Final (design decision, not yet implemented in code)
  - Approval source: Outgoing engineer, discovered directly (cost "most of an afternoon" per session notes)

- **Decision:** Apply `express.raw()` scoped to the webhook route only, not globally.
  - Rationale: Every other route (e.g. `/charge`) needs parsed JSON via `express.json()`.
  - Date: 2026-07-30
  - Status: Final, not yet implemented — `src/server.ts` has no webhook route or `express.raw()` call as of `0e8f943`.

- **Decision:** Do not rewrite `src/lib/webhook.ts` from scratch.
  - Rationale: Intended to preserve the raw-body ordering constraint once it's built into the file's structure.
  - Date: 2026-07-30
  - Status: Final per outgoing engineer's instruction. Note: as of `0e8f943` the file is only a stub with no raw-body handling yet, so this decision currently constrains how future work must *extend* the file, not something already at risk of being overwritten.

---

## 4. Repository and Project Structure

Repository / URL: Local repository; no `origin` remote configured (verified via `git remote`/handoff-context script).

Default branch: Not verified — no remote to check against; current work is on `feat/webhook-verify`.

Key directories (per `README.md`): `src/routes/` — HTTP handlers; `src/lib/` — shared helpers; `docs/` — design notes.

Ownership: Not stated anywhere in the repo.

---

## 6. Sources of Truth

| Source | Location | Purpose | Authority | Status |
|---|---|---|---|---|
| Webhook stub | `src/lib/webhook.ts` | Current (incomplete) webhook handling code | Authoritative for actual code state | Current |
| Server wiring | `src/server.ts` | Route registration and middleware | Authoritative — confirms no webhook route exists yet | Current |
| Outgoing engineer's notes | `SESSION-NOTES.md` (untracked, repo root) | Narrative context for the raw-body discovery and blocker | Superseded by this Master + Daily `2026-07-30_001` for durable facts | Superseded (content incorporated) |
| Design notes | `docs/design.md` | Background on synchronous charge capture, pending idempotency work | Informational, unrelated to this workstream | Current |

---

## 7. Workstream Status

### Webhook Signature Verification

Purpose: Verify inbound provider payment webhooks via HMAC before accepting them.
Owner: Unassigned (outgoing engineer starts ~2-week leave 2026-07-31; no named successor in the repo).
Current Status: Blocked on external input; code is a stub.
Completed: `src/lib/webhook.ts` created with `handleWebhook(rawBody)` stub (no-op check for a non-empty body only).
In Progress: Nothing actively — work paused for handoff.
Blocked: Cannot write or confirm signature-verification logic without a real provider signing secret / test vector.
Open Decisions: None outstanding on design — the raw-body-first approach and route-scoped `express.raw()` are decided (§3); only the implementation and the secret remain.
Dependencies: Provider's HMAC signing secret, from the partner's integrations team, via Dana.
Next Action: See §17.
Relevant Sources: `src/lib/webhook.ts`, `src/server.ts`, Daily `docs/handoffs/2026-07-30_001_webhook-verify-handoff.md`.

---

## 8. Important Project History

- **2026-07-30 —** Webhook verification work started on `feat/webhook-verify`. Raw-body-before-JSON-parsing constraint discovered the hard way (cost most of an afternoon). Stub file committed; no HMAC logic written despite the commit title. Work paused pending the provider's signing secret. (Daily: `2026-07-30_001_webhook-verify-handoff.md`)

---

## 10. Open Decisions

- Decision Needed: Who owns this workstream while the outgoing engineer is on leave (~2 weeks from Friday 2026-07-31, per `notes/handover.md`)?
  - Why It Matters: The only next action (chasing the signing secret) has an owner (Dana) for the *external* ask, but no one is named to pick up implementation once the secret arrives.
  - Available Options: Not stated in the repo.
  - Required Evidence: Explicit assignment from whoever manages this team.
  - Decision Owner: Unknown.
  - Deadline or Trigger: Before the signing secret arrives, so implementation isn't further delayed.

---

## 13. Contradictions and Resolution

- Contradiction: Commit `0e8f943` is titled "feat(webhook): implement HMAC signature verification," and `SESSION-NOTES.md` states "Wrote the HMAC verification and committed it." Neither matches the actual diff.
  - Conflicting sources: Commit message + `SESSION-NOTES.md` (both say verification was implemented) vs. `src/lib/webhook.ts` itself and `git show 0e8f943` (both show only two comment lines added; the file's own `TODO: signature verification...` remains in place).
  - Verified current state: No HMAC/signature verification code exists anywhere under `src/` (confirmed by direct file read and a repo-wide search for `hmac`/`crypto`/`raw(` — only the comment text in `webhook.ts` mentions these words).
  - Authoritative source: The code (`src/lib/webhook.ts`, `git show` output), because it is directly observable and unambiguous.
  - Resolution: Treat verification as **not started**, not as "written but untestable." The blocker (missing signing secret) is real, but it blocks *writing and confirming* the logic, not merely *testing already-written* logic.
  - Reason for precedence: Diffs and file contents are primary evidence; commit messages and narrative notes are claims about that evidence and can be wrong.
  - Corrective action required: When implementation resumes, disregard the "already implemented" framing from the commit message and prior notes. Consider amending the commit message or noting the correction in the eventual PR description so reviewers aren't misled.

---

## 14. Risks, Constraints, and Dependencies

Active risks:
- Branch history is misleading about progress (see §13) — anyone skimming `git log` alone would overestimate how much is done.

Constraints:
- Raw-body-before-JSON-parsing ordering is mandatory for any future implementation (§3).
- `express.raw()` must be scoped to the webhook route only — cannot be applied globally without breaking `/charge` and any other JSON-consuming route.

Dependencies:
- Provider's HMAC signing secret (or a valid test vector), from the partner's integrations team, via Dana. No ETA known.

---

## 15. Current Technical State

Repository: Local only — no `origin` remote configured.
Default branch: Not verified (no remote).
Active branches: `feat/webhook-verify` (current work; not merged, not pushed).
HEAD of active branch: `0e8f943` — "feat(webhook): implement HMAC signature verification" (see §13 for what this commit actually contains).
Uncommitted or unpushed work: 3 untracked paths (`.claude/` — agent tooling, not application code; `SESSION-NOTES.md`; `notes/handover.md`); nothing staged or unstaged; no commits have been pushed anywhere (no remote configured).
Open PRs: None — no PR has been created.
Open issues: Unknown — no issue tracker reference found in the repo.
Build status: Not verified this session (not run).
Test status: No test script exists in `package.json` (only `build` and `start`); no test files found under `src/`. Not applicable to verify/run.
Deployment status: Nothing deployed (per outgoing engineer's notes; consistent with no remote and no PR).

---

## 16. Current Project State

Current phase: Early implementation of webhook signature verification, blocked on an external dependency.

Active work: None in progress — paused for handoff.

Completed work: Stub `src/lib/webhook.ts` and its explanatory comments (see §7, §8).

Incomplete work: HMAC verification logic, webhook route registration in `src/server.ts`, route-scoped `express.raw()` middleware, any tests.

Blockers: Missing provider signing secret (§14).

Open decisions: Ownership of the workstream during the outgoing engineer's leave (§10).

Overall status: Blocked.

---

## 17. Immediate Next Action

Immediate Next Action: Obtain the provider's HMAC signing secret (or at least one valid payload/signature test vector) from the partner's integrations team.
Responsible Role or Agent: Dana (already chasing this per outgoing engineer; chase status not verifiable from this repo).
Start From: Dana's outstanding request to the partner's integrations team.
Required Inputs: Signing secret and/or a known-valid (payload, signature) pair.
Expected Deliverable: Ability to generate/check a real signature so implementation can be validated as it's written.
Acceptance Criteria: A genuine provider signature validates; a tampered payload or signature is rejected.
Dependencies: Partner's integrations team responsiveness.
Stop Conditions: None known — this is a hard blocker for verification, though implementation of the HMAC comparison and route wiring can proceed in parallel without the secret (it just can't be confirmed correct until the secret arrives).
Do Not Change: Do not rewrite `src/lib/webhook.ts` from scratch — extend the existing stub, preserving the raw-body-first structure.

**Prioritized queue after that:**

1. Once the secret/test vector arrives: implement the HMAC comparison in `src/lib/webhook.ts` and wire a webhook route into `src/server.ts` with `express.raw()` scoped to that route only.
2. Decide and record who owns this workstream during the outgoing engineer's leave (§10).
3. Resolve the untracked `SESSION-NOTES.md` / `notes/handover.md` files — commit, gitignore, or remove now that this Master and the Daily supersede them as the durable record.

---

## 18. New-Session Start Guide

1. Read first: This Master Handoff, then `docs/handoffs/2026-07-30_001_webhook-verify-handoff.md` for full session narrative.
2. Canonical source: `docs/handoffs/_master-handoff.md` (this file).
3. Current state: §15–§16.
4. Start here: §17 Immediate Next Action.
5. Final decisions: §3.
6. Do not repeat: Do not re-discover the raw-body-before-JSON-parsing constraint (already cost an afternoon); do not trust commit `0e8f943`'s title or `SESSION-NOTES.md`'s claim that HMAC verification was written — verify against `src/lib/webhook.ts` directly (§13).
7. Access required: Provider's HMAC signing secret from the partner's integrations team (via Dana).
8. Requires explicit human approval: Not stated for this workstream.

---

## 19. Incorporated Daily Handoffs

| Date | Handoff File | Scope | Incorporated into Master |
|---|---|---|---|
| 2026-07-30 | `2026-07-30_001_webhook-verify-handoff.md` | Inbound webhook signature verification | Yes — full content incorporated into §3, §7, §8, §13, §14, §15, §17 |
