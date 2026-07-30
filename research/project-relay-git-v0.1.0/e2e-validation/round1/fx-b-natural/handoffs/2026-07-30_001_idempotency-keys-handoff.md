# Daily Handoff — checkout-service — 2026-07-30

Project: checkout-service
Date: 2026-07-30
Handoff ID: 2026-07-30_001_idempotency-keys
Session Scope: Idempotency-key replay for the charge route, scoped per merchant
Branch: feat/idempotency-keys
Prepared By: Relay Fixture (assistant-prepared from repo state + SESSION-NOTES.md)
End-of-Session Status: Key store and per-merchant scoping built; charge route wired to replay; blocked on a product answer before the replay path can be finished

---

## 1. Session Objective

**Intended objective:** a repeated `Idempotency-Key` should replay the original response instead of charging the card twice.

**Actually completed:** in-memory key store, per-merchant key scoping (decided and documented), and route wiring so a replayed key short-circuits to the stored response.

**Not completed:** the replay path cannot be finished until it's known whether a replay should re-emit the payment webhook (see §6). TTL for stored entries is also undecided.

**Scope changes during session:** an express-middleware approach to the replay check was tried and abandoned in favor of doing it inline in the route (see §10).

---

## 2. Completed Work

- **Action:** Built the idempotency key store
  - Result: `src/lib/idempotency.ts` — `Map`-backed store with `remember(key, statusCode, responseBody)` / `recall(key)`, deliberately in-memory (Redis is the intended eventual backend, deferred until the `Entry` shape settles)
  - Location: `src/lib/idempotency.ts`
  - Status: Committed (`f0f39fb`)

- **Action:** Scoped idempotency keys per merchant
  - Result: `src/lib/keyscope.ts` — `scopedKey(req)` combines `X-Merchant-Id` and `Idempotency-Key` headers into `${merchant}:${raw}`, returns `null` if either header is missing
  - Location: `src/lib/keyscope.ts`
  - Status: Staged, not committed

- **Action:** Wired replay check into the charge route
  - Result: `chargeRoute` now computes `scopedKey(req)` and, if a prior entry exists in the store, returns the stored status/body instead of processing the charge
  - Location: `src/routes/charge.ts`
  - Status: Unstaged (working-tree edit only)

- **Action:** Recorded the per-merchant scoping decision
  - Result: `docs/design.md` updated with the Idempotency section
  - Location: `docs/design.md`
  - Status: Committed (`6e45468`)

---

## 3. Decisions Made

- **Decision:** Idempotency keys are scoped per merchant (`merchant:key`), not global.
  - Rationale: two merchants could independently generate the same UUID v4; a global namespace would also let one merchant probe another merchant's key space.
  - Options considered: global key namespace (the original approach).
  - Rejected: global namespace — collision risk plus cross-merchant probing.
  - Expected impact: `scopedKey` returns `null` (no replay lookup) when either header is absent, so requests missing `X-Merchant-Id` never get replay protection — worth confirming that's acceptable for all charge callers.
  - Status: Final — documented in `docs/design.md`, committed at `6e45468`.

- **Decision:** Key store stays in-memory for now rather than Redis.
  - Rationale: the `Entry` shape is still moving (see §6, webhook question), so committing to a persistence schema now would mean migrating it again shortly.
  - Status: Provisional — explicitly a placeholder, not a gap.

---

## 4. What Changed

- Change: New idempotency key store
  - Location: `src/lib/idempotency.ts`
  - Previous State: did not exist
  - New State: `Map`-backed `remember`/`recall`
  - Reason: foundation for replay behavior
  - Validation: Not verified this session (see §6 — no test script exists in `package.json` to confirm SESSION-NOTES' claim that the suite was run)

- Change: New per-merchant key scoping helper
  - Location: `src/lib/keyscope.ts`
  - Previous State: did not exist
  - New State: `scopedKey(req)`, staged but not committed
  - Reason: implements the per-merchant decision above
  - Validation: Not verified this session

- Change: Charge route now checks for and replays prior responses
  - Location: `src/routes/charge.ts`
  - Previous State: always processed the charge
  - New State: looks up `scopedKey(req)` via `recall()` before charging; short-circuits with the stored status/body on a hit
  - Reason: core of the idempotency feature
  - Validation: Not verified this session

---

## 5. Repository State at Session End

Branch: feat/idempotency-keys
HEAD commit: `6e45468` — "docs: record the per-merchant key scoping decision"
Uncommitted:
- staged: `src/lib/keyscope.ts` (new file)
- unstaged: `src/routes/charge.ts` (modified — replay check added)
- untracked: `.claude/`, `SESSION-NOTES.md`, `notes/` (contains `notes/scratch.md`)

Stashes: none observed
Upstream divergence: no upstream configured — no origin remote at all; this work exists only on this machine
Open PR: SESSION-NOTES.md claims "Opened PR #14 for review," but no git remote is configured and `gh` could not reach a repository — this claim is **unverified and currently unverifiable** from this checkout
Related issues: none observed

---

## 6. Open, Uncertain, or Unverified Items

- **Item:** Should a replayed charge re-emit the payment webhook, or stay silent? — Status: Blocked
  - Detail: blocks finishing the replay path. If it must re-emit, the stored `Entry` type (`src/lib/idempotency.ts`) needs to carry the webhook payload too, which is an interface change.
  - What would resolve it: Marta's answer (named in SESSION-NOTES.md as the person to ask).

- **Item:** TTL for stored idempotency entries — Status: Open
  - Detail: noted in `notes/scratch.md` as "24h feels arbitrary," no decision made.
  - What would resolve it: a deliberate TTL decision once the Entry shape (see above) is settled.

- **Item:** Test suite status — Status: Needs Validation
  - Detail: SESSION-NOTES.md states "Ran the test suite, all green," but `package.json` defines no `test` script, so this could not be confirmed by inspection this session.
  - What would resolve it: locate how tests are actually run in this repo (or confirm none exist yet) and re-run before trusting this claim.

- **Item:** PR #14 — Status: Needs Validation
  - Detail: claimed opened in SESSION-NOTES.md; repository has no configured remote, so its existence/location can't be checked from here.
  - What would resolve it: confirming which remote/host the PR would live on, or correcting the note if no PR actually exists.

---

## 7. Actual End-of-Session State

**Complete:** key store (`src/lib/idempotency.ts`), per-merchant scoping decision and doc update — both committed.

**In progress:** `src/lib/keyscope.ts` staged but uncommitted; `src/routes/charge.ts` edited but unstaged. Neither survives a branch switch as-is.

**Blocked:** the replay path's handling of the webhook re-emission question (§6) — the Entry type may still change shape depending on the answer, so committing the current `charge.ts`/`keyscope.ts` work now is reasonable, but the feature isn't done.

**Not ready for release/deployment:** whole feature — webhook behavior and TTL both unresolved.

---

## 8. Exact Next Action

Next Action: Get Marta's decision on whether a replayed charge must re-emit the payment webhook.
Start From: ask Marta directly (per `SESSION-NOTES.md`); the open question is recorded in `notes/scratch.md` and §6 above.
Required Inputs: Marta's answer (re-emit vs. stay silent).
Expected Output: a decision that determines whether `Entry` in `src/lib/idempotency.ts` needs a webhook-payload field.
Acceptance Criteria: answer obtained and recorded (e.g., in `docs/design.md` alongside the existing Idempotency section).
Do Not Change: the per-merchant scoping decision (§3) — settled, do not re-litigate.
Blocking Conditions: replay path (and the Entry type) cannot be finalized until this answer arrives.

---

## 9. Continuation Sources

| Source | Location / Identifier | Purpose |
|---|---|---|
| Design notes | `docs/design.md` | Documents the per-merchant scoping decision |
| Session scratch notes | `notes/scratch.md` | Marta question + TTL question, in the author's own words |
| Prior session log | `SESSION-NOTES.md` | Narrative of this session; contains the PR/test claims flagged as unverified in §6 |
| Key store | `src/lib/idempotency.ts` | `remember`/`recall`, the piece whose shape depends on the webhook answer |
| Scoping helper | `src/lib/keyscope.ts` | Staged, uncommitted |
| Charge route | `src/routes/charge.ts` | Unstaged, uncommitted |

---

## 10. Work That Must Not Be Repeated

- **Item:** Doing the replay check in express middleware ahead of the route handler — Reason: middleware runs before the JSON body parser, but deciding whether a replay matches requires both the merchant header *and* the request body (amount); the ordering can't be fought without restructuring the middleware stack. Do inline in the route, as currently implemented.
- **Item:** Global (non-merchant-scoped) idempotency keys — Reason: rejected due to cross-merchant UUID collision risk and key-space probing (§3). This decision is Final; don't revert to a global namespace without revisiting that rationale.
