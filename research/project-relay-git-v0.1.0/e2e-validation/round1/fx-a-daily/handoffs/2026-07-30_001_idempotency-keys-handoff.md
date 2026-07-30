# Daily Handoff — checkout-service — 2026-07-30

Project: checkout-service (fx-a-daily)
Date: 2026-07-30
Handoff ID: 2026-07-30_001
Session Scope: Idempotency-Key replay for the charge route, scoped per merchant
Branch: feat/idempotency-keys
Prepared By: Claude Code session agent
End-of-Session Status: Replay lookup wired into the charge route (reads via `recall`); the write side (`remember`) is not called anywhere yet, which is consistent with the open blocker below, not an oversight. `src/lib/keyscope.ts` is staged, `src/routes/charge.ts` is unstaged, nothing is committed beyond `f0f39fb`/`6e45468`, and there is no remote to push to.

---

## 1. Session Objective

**Intended objective:** A repeated `Idempotency-Key` on the charge route should replay the original response instead of charging the card twice.

**Actually completed:** In-memory key store; per-merchant key scoping (design decision + helper); `recall`-side wiring into the charge route so a known key short-circuits to the stored response.

**Not completed:** The `remember`-side wiring (storing the response after a successful charge) is not implemented — `remember()` in `src/lib/idempotency.ts` has no caller anywhere in the tree. Per `SESSION-NOTES.md`, this is deliberately blocked: whether the stored entry needs to carry the webhook payload depends on Marta's answer (see §7).

**Scope changes during session:** A middleware-based approach to the replay check was attempted and abandoned mid-session (see §12).

---

## 2. Completed Work

- **Action:** Built the idempotency key store.
  - Result: `store: Map<string, Entry>` with `remember`/`recall`, `Entry = { responseBody, statusCode, createdAt }`.
  - Location: `src/lib/idempotency.ts` (new), commit `f0f39fb`.
  - Status: Committed.
  - Evidence: `git show f0f39fb`.

- **Action:** Scoped idempotency keys per merchant instead of globally.
  - Result: `scopedKey(req)` combines `X-Merchant-Id` and `Idempotency-Key` headers into `"${merchant}:${raw}"`; returns `null` if either header is missing.
  - Location: `src/lib/keyscope.ts` (new, staged, not committed).
  - Status: Staged only.
  - Evidence: `git diff --cached -- src/lib/keyscope.ts`.

- **Action:** Wired the replay check into the charge route.
  - Result: `chargeRoute` now computes `scopedKey`, calls `recall`, and short-circuits with the stored status/body on a hit, before the amount/currency validation.
  - Location: `src/routes/charge.ts` (unstaged).
  - Status: Working tree only, not committed.
  - Evidence: `git diff HEAD -- src/routes/charge.ts`.

---

## 3. Decisions Made

- **Decision:** Idempotency keys are scoped per merchant (`merchant:key`), not global.
  - Rationale: Two merchants could independently generate the same UUID v4; a global namespace would also let one merchant probe another's key space.
  - Options considered: Global key namespace (the initial approach).
  - Rejected: Global namespace — collision risk plus cross-merchant key-space probing.
  - Expected impact: `Entry` lookups are keyed as `"${merchant}:${raw}"` everywhere; any future store (Redis included) must preserve this scoping.
  - Status: Final. Recorded in `docs/design.md` and committed at `6e45468`.

- **Decision:** Idempotency key storage stays in-memory (`Map`) for now, not Redis.
  - Rationale: The entry shape is still moving (see the webhook-payload question in §7); committing to a Redis schema now would mean migrating it again shortly.
  - Options considered: Redis-backed store.
  - Rejected: Redis now — premature given the unsettled `Entry` shape.
  - Expected impact: Store does not survive a process restart and is not shared across instances; acceptable as a deliberate placeholder, not yet acceptable for production.
  - Status: Provisional — expected to change once the `Entry` shape settles.

---

## 4. What Changed

- Change: New idempotency key store.
  - Location: `src/lib/idempotency.ts`
  - Previous State: Did not exist.
  - New State: `remember`/`recall` against an in-memory `Map`.
  - Reason: Foundation for replay support.
  - Validation: Not independently verified this session (see §7 — test suite claim).

- Change: New per-merchant key scoping helper.
  - Location: `src/lib/keyscope.ts`
  - Previous State: Did not exist (an earlier global-scope version was written and superseded before being committed — no artifact of it remains in history).
  - New State: `scopedKey(req)` — see §2.
  - Reason: Per-merchant decision above.
  - Validation: Not independently verified this session.

- Change: Charge route now checks for a replayable response.
  - Location: `src/routes/charge.ts`
  - Previous State: Validated `amountCents`/`currency` and returned `201` unconditionally (see commit `8f75289`'s baseline).
  - New State: Checks `scopedKey` + `recall` first and returns the stored response on a hit; falls through to the original validation/charge logic otherwise.
  - Reason: Implements the replay behavior.
  - Validation: Not independently verified this session; also incomplete — nothing ever calls `remember`, so no response is actually stored yet (confirmed via `grep -rn "remember("`, only match is the definition).

- Change: Design doc updated with the per-merchant scoping rationale.
  - Location: `docs/design.md`
  - Previous State: Described idempotency intent without specifying scoping.
  - New State: States keys are scoped per merchant and why.
  - Reason: Record the decision in §3.
  - Validation: N/A (documentation).

---

## 5. Repository State at Session End

Branch: feat/idempotency-keys
HEAD commit: `6e45468` "docs: record the per-merchant key scoping decision"
Uncommitted:
  - staged: `src/lib/keyscope.ts` (A)
  - unstaged: `src/routes/charge.ts` (M)
  - untracked: `SESSION-NOTES.md`, `notes/` (contains `scratch.md`), `.claude/` (tooling/config, not feature work)
Stashes: None observed.
Upstream divergence: No remote configured (`git remote -v` empty) and no upstream tracking branch — this branch exists on this machine only.
Open PR: `SESSION-NOTES.md` states PR #14 was opened for this work. Not independently verified — `gh` could not reach the repository this session, so PR existence/status/reviewers are unknown.
Related issues: None found/verified.

---

## 6. Open, Uncertain, or Unverified Items

- **Item:** Whether a replayed charge should re-emit the payment webhook. — Status: Blocked
  - Detail: Answer determines whether `Entry` needs a webhook-payload field, which in turn determines how `remember()` gets wired into `chargeRoute`. This is why the write side of the replay path is still missing.
  - What would resolve it: Marta's answer (see §9, Next Action).

- **Item:** "Ran the test suite, all green" (claim in `SESSION-NOTES.md`). — Status: Needs Validation
  - Detail: No `test` script exists in `package.json` (`scripts` has only `build` and `start`), and no `*.test.*`/`*spec*` files were found anywhere in the tree outside `node_modules`/`.git`. This contradicts the note as written — either the claim refers to a suite that isn't present in this checkout, or the note is inaccurate.
  - What would resolve it: Ask whoever wrote `SESSION-NOTES.md` what suite was run and where; or, if none exists, treat the claim as unverifiable and drop it from future summaries.

- **Item:** PR #14 status. — Status: Needs Validation
  - Detail: `gh` was unavailable this session (could not reach the repository). No remote is even configured locally, so it's also unclear what repository the PR would live in.
  - What would resolve it: Run `gh pr view 14` from an environment with repository access, or confirm the intended GitHub remote.

- **Item:** TTL for stored idempotency entries. — Status: Open
  - Detail: `notes/scratch.md` flags "TTL? 24h feels arbitrary" — no TTL is implemented in `src/lib/idempotency.ts` (entries never expire).
  - What would resolve it: A decision on retention policy, likely alongside the Redis migration.

---

## 7. New Risks and Constraints

- Risk: Replay path is read-only right now — `recall` is wired in but nothing ever calls `remember`, so no charge response is actually being stored yet. A client retrying with the same key today will not get a replay; it will re-run the charge logic every time.
  - Impact: The feature does not yet prevent double-charging, which is the stated purpose of the work.
  - Likelihood: Certain given current code — not a probability, a fact of the current diff.
  - Mitigation: Intentionally deferred pending Marta's webhook-re-emission answer (§6); do not wire `remember()` ahead of that answer, since the `Entry` shape may need to change.
  - Owner: Unassigned beyond "whoever resumes this branch."
  - Status: Open, tracked via §6 blocker.

---

## 8. Actual End-of-Session State

**Complete:** In-memory key store (`src/lib/idempotency.ts`, committed); per-merchant scoping decision and doc (`docs/design.md`, committed).

**In progress:** Replay wiring in `src/routes/charge.ts` (unstaged) and `src/lib/keyscope.ts` (staged) — read side only.

**Incomplete:** Write side of the replay path (`remember()` never called); TTL/expiry for stored entries.

**Blocked:** Finishing the replay path — waiting on Marta re: webhook re-emission on replay.

**Not ready for review/merge:** Nothing is committed for the route wiring or the key-scope helper beyond staging; PR #14 status unverified.

---

## 9. Exact Next Action

Next Action: Get Marta's answer on whether a replayed charge should re-emit the payment webhook.
Start From: `SESSION-NOTES.md:29-33` for the exact question and why it's blocking; `docs/design.md` for current design context.
Required Inputs: Marta's decision (yes/no on webhook re-emission).
Expected Output: If yes — extend `Entry` in `src/lib/idempotency.ts` with a webhook-payload field and wire `remember()` into `src/routes/charge.ts` accordingly. If no — wire `remember()` as-is against the current `Entry` shape.
Acceptance Criteria: A second request with the same `Idempotency-Key` + `X-Merchant-Id` returns the stored response without re-running the charge logic, and (if applicable) without re-emitting the webhook.
Do Not Change: Per-merchant key scoping (`merchant:key` format) — settled decision, §3. Do not reintroduce a middleware-based replay check (§10) — already tried and rejected.
Blocking Conditions: Cannot finish without Marta's answer.

---

## 10. Continuation Sources

| Source | Location / Identifier | Purpose |
|---|---|---|
| Session notes | `SESSION-NOTES.md` | Narrative of this session, the Marta question, TTL note |
| Scratch notes | `notes/scratch.md` | Open questions (Marta, TTL) |
| Design doc | `docs/design.md` | Current idempotency design, per-merchant scoping rationale |
| Key store | `src/lib/idempotency.ts` | `remember`/`recall`, `Entry` type to extend |
| Key scoping | `src/lib/keyscope.ts` | `scopedKey` helper (staged) |
| Charge route | `src/routes/charge.ts` | Replay wiring (unstaged) |
| PR | #14 (per SESSION-NOTES.md, not independently verified) | Review thread, if reachable |

---

## 11. Work That Must Not Be Repeated

- **Item:** Doing the replay check in Express middleware, ahead of the route handler. — Reason: Middleware runs before the JSON body parser, but the replay decision needs both the merchant header and the request body (amount). Fighting that ordering wasn't worth it; the check was moved into the route handler instead. Do not retry the middleware approach without first solving the body-parser ordering problem.
