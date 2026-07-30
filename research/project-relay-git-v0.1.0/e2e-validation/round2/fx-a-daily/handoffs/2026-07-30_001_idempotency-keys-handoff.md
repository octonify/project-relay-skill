# Daily Handoff — checkout-service — 2026-07-30

Project: checkout-service (repo root: fx-a-daily)
Date: 2026-07-30
Handoff ID: 2026-07-30_001
Session Scope: Idempotency-Key replay for the charge route
Branch: feat/idempotency-keys
Prepared By: Session agent (from SESSION-NOTES.md and repository inspection)
End-of-Session Status: Key store and per-merchant scoping wired into the charge route, but the store is never written to (see §7) — replay cannot work yet even for a first charge. Blocked on a webhook-semantics answer from Marta.

---

## 1. Session Objective

**Intended objective:** A repeated `Idempotency-Key` should replay the original response instead of charging the card twice.

**Actually completed:** In-memory key store (`src/lib/idempotency.ts`), per-merchant key scoping (`src/lib/keyscope.ts`, design decision recorded), and a replay-check read path wired into `src/routes/charge.ts`.

**Not completed:** The write side — nothing in the route calls `remember()`, so no response is ever stored (§7). Also open: webhook re-emission semantics on replay, and the store's TTL.

**Scope changes during session:** An express-middleware approach was attempted for the replay check and abandoned mid-session (§12) in favor of an inline check in the route handler.

---

## 2. Completed Work

- **Action:** Built in-memory idempotency key store.
  - Result: `remember(key, statusCode, responseBody)` and `recall(key)` against a `Map`.
  - Location: `src/lib/idempotency.ts`, committed at `b8c8197` ("feat(idempotency): in-memory key store").
  - Status: Committed.
  - Evidence: file content read this session; matches commit diff (+12 lines).

- **Action:** Added per-merchant key scoping and recorded the decision.
  - Result: `scopedKey(req)` in `src/lib/keyscope.ts` returns `` `${merchant}:${raw}` `` from `X-Merchant-Id` + `Idempotency-Key` headers, or `null` if either is missing.
  - Location: `src/lib/keyscope.ts` (staged, uncommitted), decision written up in `docs/design.md` (committed at `032ba42`).
  - Status: Code staged, not committed; decision doc committed.
  - Evidence: `git diff --cached` and `docs/design.md` read this session.

- **Action:** Wired the replay-check read path into the charge route.
  - Result: `chargeRoute` now computes `scopedKey(req)`, calls `recall(key)`, and short-circuits with the prior `statusCode`/`responseBody` on a hit.
  - Location: `src/routes/charge.ts` (unstaged, uncommitted).
  - Status: In working tree, not staged.
  - Evidence: `git diff HEAD` read this session.

---

## 3. Decisions Made

- **Decision:** Idempotency keys are scoped per merchant (`merchant:key`), not global.
  - Rationale: two merchants could independently generate the same UUID v4; a global namespace would also let one merchant probe another's key space.
  - Options considered: global key namespace (the original approach).
  - Rejected: global namespace, for the collision/probing reasons above.
  - Expected impact: every idempotency lookup must carry both `Idempotency-Key` and `X-Merchant-Id`; a request missing either cannot be deduplicated (see `scopedKey` returning `null`, §2).
  - Status: Final — recorded in `docs/design.md`, committed at `032ba42`.

- **Decision:** Key store stays in-memory (`Map`) for now; Redis is deferred.
  - Rationale: the entry shape (`Entry` type) is still moving — e.g. it may need to grow a webhook payload field depending on Marta's answer (§7). Committing to a persistent schema now risks a migration next week.
  - Options considered: Redis-backed store.
  - Rejected: Redis, for now — not ruled out long-term.
  - Expected impact: idempotency state does not survive a process restart and is not shared across instances.
  - Status: Provisional — explicitly a placeholder, revisit once the `Entry` shape settles.

---

## 4. What Changed

- Change: New module `scopedKey()` for per-merchant key derivation.
  - Location: `src/lib/keyscope.ts`
  - Previous State: did not exist.
  - New State: staged, added, not yet committed.
  - Reason: implements the per-merchant scoping decision (§3).
  - Validation: not verified (no test files exist in the repo; see §7).

- Change: `chargeRoute` gained a replay-check read path.
  - Location: `src/routes/charge.ts`
  - Previous State: `c281ab2` — validated `amountCents`/`currency` and captured directly, no idempotency awareness.
  - New State: checks `scopedKey` + `recall` before processing; unstaged in the working tree.
  - Reason: implements Idempotency-Key replay (session objective).
  - Validation: not verified; also incomplete — see the write-side gap in §7.

---

## 5. Repository State at Session End

Branch: feat/idempotency-keys
HEAD commit: 032ba42 "docs: record the per-merchant key scoping decision"
Uncommitted:
- staged: `src/lib/keyscope.ts` (new file, added)
- unstaged: `src/routes/charge.ts` (modified)
- untracked: `.claude/`, `SESSION-NOTES.md`, `notes/` (includes `notes/scratch.md`)
Stashes: none observed
Upstream divergence: no upstream tracking branch configured — this work exists only on this local machine
Open PR: SESSION-NOTES.md states PR #14 was opened — **not verified** this session (`gh` could not reach the repository; see §7)
Related issues: none observed

---

## 6. Validated or Approved Items

None. Nothing in this session was independently confirmed by a test run, build, or human approval that this session directly observed — see §7 for why the session notes' testing/PR claims aren't included here.

---

## 7. Open, Uncertain, or Unverified Items

- **Item:** `remember()` is never called anywhere in the codebase. — Status: Open
  - Detail: `src/lib/idempotency.ts` exports `remember()` but a repo-wide search found only its own definition as a match. `chargeRoute` calls `recall()` on the way in but never stores the response on the way out. As wired, a first-time charge is never remembered, so a genuine retry with the same key will not replay — it will fall through and charge again. This is the opposite of the session objective.
  - What would resolve it: add a `remember(key, statusCode, responseBody)` call in `src/routes/charge.ts` after the response is computed (before or as part of the `res.status(...).json(...)` call), scoped by the same `key` from `scopedKey(req)`.

- **Item:** "Ran the test suite, all green" (per SESSION-NOTES.md line 25). — Status: Needs Validation
  - Detail: `package.json` defines no `test` script, and no `*.test.*` / `*.spec.*` files exist anywhere in the repo. This claim could not be reproduced or corroborated from repository evidence — it may refer to a suite that isn't checked in, or the note may be inaccurate.
  - What would resolve it: confirm what "test suite" refers to (a script, an external CI job, manual curl checks) and where it lives; if none exists, treat the feature as untested.

- **Item:** PR #14 (per SESSION-NOTES.md line 27). — Status: Needs Validation
  - Detail: repo has no `origin` remote and no upstream tracking branch; `gh` could not reach a repository this session. The PR's existence, contents, and review state are not verified.
  - What would resolve it: confirm the remote this repo pushes to, then check PR #14 there directly.

- **Item:** Whether a replayed charge should re-emit the payment webhook. — Status: Blocked, Waiting for Input
  - Detail: owner is Marta. If the answer is "re-emit," the stored `Entry` type in `src/lib/idempotency.ts` needs to grow to carry the webhook payload — changing the in-memory schema before Redis migration. The replay path cannot be considered finished until this is answered.
  - What would resolve it: Marta's decision, then updating `Entry` and the replay logic accordingly.

- **Item:** Idempotency entry TTL. — Status: Open
  - Detail: no TTL is implemented yet; `notes/scratch.md` flags "24h feels arbitrary" as an open question with no decision made.
  - What would resolve it: pick and justify a TTL (or confirm 24h) once the `Entry` shape is settled post-Marta.

---

## 8. New Risks and Constraints

- Risk: The replay mechanism currently cannot work end-to-end because nothing populates the store (§7).
  - Impact: if merged as-is, duplicate-charge protection silently does nothing — worse than no feature, because a reviewer skimming the read-side code could assume it works.
  - Likelihood: certain, given current code (not a hypothetical — confirmed by reading the route).
  - Mitigation: add the missing `remember()` call before this branch is considered done; do not merge on the strength of "wired into the charge route" alone.
  - Owner: unassigned.
  - Status: Open.

---

## 9. Actual End-of-Session State

**Complete:** In-memory key store module; per-merchant scoping module and design-doc decision (committed).

**In progress:** Charge-route integration — read side only wired, write side missing; `keyscope.ts` staged but not committed, `charge.ts` change not even staged.

**Incomplete:** Write-side `remember()` call; webhook re-emission behavior; TTL policy.

**Blocked:** Finishing the replay path is blocked on Marta's answer about webhook re-emission (§7), since that determines the `Entry` shape.

**Ready for review:** Nothing — the current working tree does not implement working replay (§7), and the claimed test run and PR could not be corroborated this session.

**Not ready for release/deployment:** Entire idempotency feature — replay does not function as wired (§7), and it is untracked in any remote (no upstream).

---

## 10. Exact Next Action

Next Action: Get Marta's decision on whether a replayed charge should re-emit the payment webhook.
Start From: Whoever owns PR #14 (unverified — confirm this is the current session's author) reaches out to Marta directly, referencing the open question in `notes/scratch.md` line 1.
Required Inputs: Marta's answer (re-emit vs. stay silent).
Expected Output: A yes/no decision recorded in `docs/design.md`, driving whether `Entry` in `src/lib/idempotency.ts` gains a webhook-payload field.
Acceptance Criteria: Decision is written down; `Entry` type updated to match if needed.
Do Not Change: The per-merchant scoping decision (§3) — it's final. Do not reintroduce the express-middleware approach for the replay check (§12) — already tried and abandoned for a structural reason, not a bug.
Blocking Conditions: Cannot finish the replay path (nor safely add the `remember()` call's response shape) until Marta answers, since the answer changes what gets stored.

Separately, and not blocked on Marta: add the missing `remember()` call in `src/routes/charge.ts` (§7) — the replay feature is non-functional without it regardless of the webhook answer.

---

## 11. Continuation Sources

| Source | Location / Identifier | Purpose |
|---|---|---|
| Session narrative (source for this handoff) | `SESSION-NOTES.md` | Original first-person account of the session |
| Open-question scratch notes | `notes/scratch.md` | Marta question + TTL question, in the author's own words |
| Design decisions | `docs/design.md` | Idempotency scoping decision, current as of `032ba42` |
| Key store | `src/lib/idempotency.ts` | `remember`/`recall`, `Entry` type — needs the write-side fix (§7) |
| Key scoping | `src/lib/keyscope.ts` | `scopedKey()`, staged not committed |
| Charge route | `src/routes/charge.ts` | Integration point, unstaged not committed |

---

## 12. Work That Must Not Be Repeated

- **Item:** Doing the replay check in express middleware. — Reason: middleware runs before the JSON body parser; the merchant id is available (header) but the amount is not yet (body), and both are needed to judge whether a replay is genuinely the same request. Abandoned for this structural ordering reason, not because it was buggy — do not retry without first solving the parser-ordering problem.
