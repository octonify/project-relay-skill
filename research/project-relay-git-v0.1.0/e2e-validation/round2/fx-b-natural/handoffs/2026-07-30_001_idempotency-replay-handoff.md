# Daily Handoff — fx-b-natural — 2026-07-30

Project: fx-b-natural (checkout service)
Date: 2026-07-30
Handoff ID: 2026-07-30_001
Session Scope: Idempotency-key replay for the charge route
Branch: feat/idempotency-keys
Prepared By: Relay Fixture
End-of-Session Status: Key store and per-merchant scoping decision committed; replay wiring into the charge route is uncommitted in the working tree; blocked on a webhook-behavior answer from Marta before the replay path can be finished.

---

## 1. Session Objective

**Intended objective:** A repeated `Idempotency-Key` must replay the original response instead of charging the card twice.

**Actually completed:** In-memory key store, the per-merchant key-scoping decision (documented and committed), and a first pass at wiring the replay check into the charge route.

**Not completed:** Whether a replayed charge should re-emit the payment webhook (blocks finishing the replay path), TTL policy for stored entries, committing the route change.

**Scope changes during session:** None — an in-process middleware approach was attempted and abandoned (see §3), but the overall objective didn't change.

---

## 2. Completed Work

- **Action:** Built an in-memory idempotency key store.
  - Result: `remember(key, statusCode, responseBody)` / `recall(key)` over a `Map`.
  - Location: `src/lib/idempotency.ts`
  - Status: Committed at `b7af058` (`feat(idempotency): in-memory key store`).

- **Action:** Documented and committed the per-merchant key-scoping decision.
  - Result: `docs/design.md` states keys are scoped per merchant, not globally.
  - Location: `docs/design.md`
  - Status: Committed at `157434f` (`docs: record the per-merchant key scoping decision`).

---

## 3. Decisions Made

- **Decision:** Idempotency keys are scoped per merchant (`X-Merchant-Id` + `Idempotency-Key`), not globally.
  - Rationale: Two merchants could independently generate a colliding UUIDv4; a global namespace also lets one merchant probe another's key space.
  - Options considered: global key namespace.
  - Rejected: global key namespace — for the reasons above.
  - Expected impact: `scopedKey()` (see §4) is the only path routes should use to derive a store key.
  - Status: **Final** — documented in `docs/design.md`, committed at `157434f`.

- **Decision:** Idempotency entries are stored in-memory (`Map`), not Redis, for now.
  - Rationale: the `Entry` shape (`src/lib/idempotency.ts:2`) is still moving — pinning a Redis schema now would just mean migrating it next week. Deliberate placeholder, not an oversight.
  - Status: **Provisional** — expected to move to Redis once the `Entry` shape settles (see open webhook question, §7).

- **Decision:** Replay detection must not live in Express middleware.
  - Rationale: middleware runs before the JSON body parser; merchant id lives in a header but amount lives in the body, and both are needed to judge whether a replay is really the same request. Not worth fighting the ordering.
  - Rejected: middleware-based replay check.
  - Status: **Final** — see §12, do not retry this approach.

---

## 4. What Changed

- Change: Added `scopedKey(req)` helper.
  - Location: `src/lib/keyscope.ts` (new file)
  - Previous State: did not exist.
  - New State: reads `Idempotency-Key` and `X-Merchant-Id` headers, returns `` `${merchant}:${raw}` `` or `null` if either is missing.
  - Reason: implements the per-merchant scoping decision (§3).
  - Validation: Not run this session — see §7.
  - Git state: **staged**, not committed.

- Change: Wired replay short-circuit into the charge route.
  - Location: `src/routes/charge.ts`
  - Previous State: as committed at `HEAD` (`157434f`) — no idempotency check, went straight to validating `amountCents`/`currency`.
  - New State: computes `scopedKey(req)`, and if a prior `recall(key)` entry exists, returns its stored `statusCode`/`responseBody` instead of processing the charge again.
  - Reason: closes the double-charge gap that is the point of this work.
  - Validation: Not run this session — see §7.
  - Git state: **unstaged** (modified, not staged, not committed).

---

## 5. Repository State at Session End

Branch: `feat/idempotency-keys`
HEAD commit: `157434f` — "docs: record the per-merchant key scoping decision"
Uncommitted:
  - staged: `src/lib/keyscope.ts` (new file)
  - unstaged: `src/routes/charge.ts` (modified)
  - untracked: `.claude/`, `SESSION-NOTES.md`, `notes/`
Stashes: none observed.
Upstream divergence: no remote configured (`git remote -v` empty) and no upstream tracking branch — this work exists on this machine only.
Open PR: `SESSION-NOTES.md` states "Opened PR #14 for review," but no remote is configured for this repo and GitHub lookup was unavailable. This claim is **unverified and likely stale/inconsistent** with the observed remote state — see §7.
Related issues: Not verified.

---

## 6. Validated or Approved Items

None. `SESSION-NOTES.md` states "Ran the test suite, all green," but no test files (`*.test.ts`, `*.spec.ts`, or a `test/` directory) exist anywhere in the repo as of this session, so that claim could not be corroborated and is **not** listed here as validated — see §7.

---

## 7. Open, Uncertain, or Unverified Items

- **Item:** Webhook re-emission on replay — Status: **Blocked / Waiting for Input**
  - Detail: Marta needs to say whether a replayed charge should re-emit the payment webhook or stay silent. If it re-emits, the stored `Entry` type (`src/lib/idempotency.ts:2`) needs a webhook-payload field, which is why the Redis migration is also on hold.
  - What would resolve it: Marta's answer.

- **Item:** TTL for stored idempotency entries — Status: **Open**
  - Detail: Flagged in `notes/scratch.md` as "24h feels arbitrary." No decision made.
  - What would resolve it: A deliberate TTL decision, recorded like the scoping decision was.

- **Item:** "Ran the test suite, all green" (per `SESSION-NOTES.md`) — Status: **Needs Validation**
  - Detail: No test files matching `*.test.ts`, `*.spec.ts`, or under a `test/` directory were found in the repo. Either tests run through a mechanism this search didn't cover, or the note is stale/inaccurate.
  - What would resolve it: Locate and re-run the actual test command, or confirm none exists yet.

- **Item:** PR #14 (per `SESSION-NOTES.md`) — Status: **Needs Validation**
  - Detail: No git remote is configured for this repository, which is hard to reconcile with a PR having been opened. Could not verify via `gh` (no reachable repository).
  - What would resolve it: Confirm whether a remote/fork exists elsewhere that this local clone isn't wired to, or treat the PR claim as stale.

- **Item:** Uncommitted route/helper changes — Status: **Open**
  - Detail: `src/lib/keyscope.ts` (staged) and `src/routes/charge.ts` (unstaged) are not committed and will not survive a branch switch or discard.
  - What would resolve it: Commit once the webhook question (above) is settled, since the answer may still change `Entry` and thus the surrounding code.

---

## 8. Actual End-of-Session State

**Complete:** In-memory key store (`src/lib/idempotency.ts`, committed `b7af058`); per-merchant scoping decision and its documentation (`docs/design.md`, committed `157434f`).

**In progress:** Replay short-circuit wired into `src/routes/charge.ts` using `scopedKey()` from `src/lib/keyscope.ts` — present in the working tree, functionally connected, but not committed and not validated this session.

**Incomplete:** Webhook re-emission behavior on replay; TTL policy for entries; eventual Redis migration (waiting on `Entry` shape to settle).

**Blocked:** Finishing the replay path — waiting on Marta's webhook answer.

**Not ready for review/deployment:** The charge-route change is uncommitted, and the PR status referenced in session notes could not be verified against this repo's remote configuration.

---

## 9. Exact Next Action

Next Action: Get Marta's answer on whether a replayed charge should re-emit the payment webhook or stay silent.
Start From: The open question as recorded in `notes/scratch.md:1` and `SESSION-NOTES.md:29-33`.
Required Inputs: Marta's decision.
Expected Output: If re-emit — add a webhook-payload field to `Entry` (`src/lib/idempotency.ts:2`) and update `remember`/`recall` call sites accordingly. If silent — no `Entry` change needed.
Acceptance Criteria: Decision recorded (e.g. in `docs/design.md` alongside the scoping decision); `src/lib/keyscope.ts` and `src/routes/charge.ts` committed; TTL decision made or explicitly deferred.
Do Not Change: Do not reintroduce a middleware-based replay check (§3, §12). Do not move idempotency keys to a global, non-merchant-scoped namespace (§3).
Blocking Conditions: Cannot finish the replay path or commit the route change with confidence until Marta answers.

---

## 10. Continuation Sources

| Source | Location / Identifier | Purpose |
|---|---|---|
| Session narrative | `SESSION-NOTES.md` | Full first-person account of this session, including the PR/test claims flagged in §7 |
| Open questions | `notes/scratch.md` | Webhook re-emission question, TTL question |
| Design decision | `docs/design.md` | Per-merchant key scoping (committed) |
| Key store | `src/lib/idempotency.ts` | `Entry` type, `remember`/`recall` |
| Scoping helper | `src/lib/keyscope.ts` | `scopedKey()` (staged, uncommitted) |
| Route wiring | `src/routes/charge.ts` | Replay short-circuit (unstaged, uncommitted) |

---

## 11. Work That Must Not Be Repeated

- **Item:** Middleware-based replay check — Reason: Express middleware runs before the JSON body parser, so merchant id (header) and amount (body) aren't both available yet; both are needed to judge whether a replay is the same request. Not worth fighting the ordering.
- **Item:** Global (non-merchant-scoped) idempotency key namespace — Reason: two merchants can independently generate colliding UUIDv4 keys, and a shared namespace lets one merchant probe another's key space. Settled in `docs/design.md`.
