# Daily Handoff — relay-web (Auth rebuild) — 2026-07-30

Project: relay-web (package.json version 0.3.1)
Date: 2026-07-30
Handoff ID: 2026-07-30_001_auth-login
Session Scope: Session-storage decision, login form, sessions table migration; refresh tokens attempted and parked
Workstream: Auth rebuild (relay-web)
Prepared By: Claude, working session with Priya (engineer)
End-of-Session Status: Session helper + login form written and **uncommitted** on `feat/auth-rebuild`; login is not yet wired end to end; refresh tokens blocked on AUTH-214; no automated tests written or run

---

## 1. Session Objective

**Intended objective:** "Get login working end to end, including refresh tokens." Signup already existed before this session.

**Actually completed:**
- Session-storage approach decided and locked (httpOnly cookie).
- `src/auth/session.ts` written: HS256 JWT issue/verify via `jose`, plus exported cookie config.
- `src/auth/login-form.tsx` written and manually accepted by Priya.
- `migrations/002_add_sessions.sql` written and applied to Priya's **local dev** database.

**Not completed:**
- Refresh tokens — attempted, hit an external rate limit, parked (see §6, §11).
- Automated tests (vitest) for `session.ts` and the login form — deliberately deferred mid-session.
- End-to-end login. Nothing in this repo calls `issueSession()` or applies `COOKIE_OPTS`; `LoginForm`'s `onSubmit` prop has no caller in the repo. The pieces exist, the flow does not.
- CSRF handling, which the cookie decision requires.

**Scope changes during session:** Test-writing was pulled forward-then-dropped at Priya's request in favour of starting refresh tokens; refresh tokens were then parked as blocked. Net effect: neither landed, and tests are now the first unblocked item.

---

## 2. Completed Work

- **Action:** Wrote session helper
  - Result: HS256 JWT issue/verify via `jose@5.9.6`; exports `COOKIE_NAME = "relay_session"` and `COOKIE_OPTS = { httpOnly: true, sameSite: "lax", secure: true, path: "/" }`; `TTL_SECONDS = 60 * 60 * 12` marked provisional in a code comment.
  - Location: `src/auth/session.ts` (new, untracked)
  - Status: Written, not tested, not integrated
  - Evidence: File present on disk; `git status` shows `src/auth/` untracked.

- **Action:** Wrote login form
  - Result: Email/password fields, client-side email validation (`email.includes("@")`), error region with `role="alert"` for screen readers.
  - Location: `src/auth/login-form.tsx` (new, untracked)
  - Status: Complete for this session's purpose and accepted by Priya
  - Evidence: Priya ran the dev server, entered a bad email (error shown), then a valid one (submits). Her words: "That's fine, I'm happy with the form."

- **Action:** Created and applied sessions table migration
  - Result: `sessions` table (`id uuid` PK, `user_id uuid` FK → `users(id)`, `issued_at timestamptz default now()`, `expires_at timestamptz`) plus `sessions_user_id_idx`.
  - Location: `migrations/002_add_sessions.sql` (new, untracked)
  - Status: Applied to **local dev DB only** — ran clean. Staging: not applied, state unknown (no staging access this session).
  - Evidence: Migration run reported clean during the session; no staging verification possible.

---

## 3. Decisions Made

- **Decision:** Store the session as an httpOnly cookie, not a JWT in `localStorage`.
  - Rationale: Third-party analytics scripts run on the marketing pages; any XSS would turn a JS-readable bearer token into full account takeover.
  - Options considered: JWT in `localStorage` (simpler SPA wiring) vs JWT in httpOnly cookie.
  - Rejected: `localStorage`. Explicitly rejected on security grounds, not convenience.
  - Expected impact: The API must set the cookie header; CSRF handling becomes mandatory.
  - Status: **Final** — Priya: "Cookie... Lock that in."

- **Decision:** Session TTL of 12 hours is a placeholder only.
  - Rationale: It is a product/security tradeoff, not an engineering one. Sam owns the call and is out until Monday (expected back 2026-08-03).
  - Expected impact: Staging migration is gated on this, because the column defaults depend on the chosen TTL.
  - Status: **Pending Approval** (owner: Sam).

- **Decision:** Do not write tests this session; start refresh tokens instead.
  - Rationale: Priya wanted refresh tokens tackled while the context was fresh.
  - Status: **Final for this session** — but its premise is gone now that refresh is blocked, so tests are the next action.

- **Decision:** Abandon the per-request token-introspection refresh design.
  - Rationale: `api.relay.example` rate-limits introspection at 10 req/s; the SPA alone would exceed that on page load. Batching was tried and only moved the spike.
  - Rejected: Batching introspection calls.
  - Expected impact: Refresh tokens cannot proceed without an API-side change (raised limit or a bulk endpoint) from Diego's team.
  - Status: **Final** — Priya: "Park it. Don't try that again."

- **Decision:** `src/legacy/` is frozen — do not touch, ever.
  - Rationale: It is being removed in Q4, and the last person who "tidied" it broke billing for two days. A proposal to refactor `src/legacy/admin.js` onto the new session helper was explicitly refused.
  - Status: **Final**, standing constraint beyond this session.

- **Decision:** `docs/SPEC.md` supersedes `docs/SPEC-v1.md` as the API team's spec.
  - Rationale: The API team moved the doc; Priya has already told the rest of the team.
  - Expected impact: Anything pointing at `docs/SPEC-v1.md` is wrong.
  - Status: **Final**.

- **Decision:** Priya applies the staging migration herself, after Sam signs off on the TTL.
  - Rationale: Column defaults depend on TTL; Claude has no staging access.
  - Status: **Final** (owner: Priya).

---

## 4. What Changed

- Change: New session helper module
  - Location: `src/auth/session.ts`
  - Previous State: Did not exist
  - New State: HS256 JWT issue/verify via `jose`; cookie name and options exported; 12h TTL placeholder; `SECRET` falls back to the literal `"dev-only-secret"` when `process.env.SESSION_SECRET` is unset
  - Reason: Implements the httpOnly-cookie session decision
  - Validation: **Not validated.** No tests written, no test run, no integration exercised.

- Change: New login form component
  - Location: `src/auth/login-form.tsx`
  - Previous State: Did not exist
  - New State: Controlled email/password form, client-side email check, `role="alert"` error region
  - Reason: Session objective
  - Validation: Manual check by Priya in the dev server (bad email → error, valid email → submits). Accepted.

- Change: New database migration, applied to local dev
  - Location: `migrations/002_add_sessions.sql`; target = Priya's local dev database
  - Previous State: No `sessions` table in local dev
  - New State: `sessions` table + `sessions_user_id_idx` present in local dev
  - Reason: Server-side session records
  - Validation: Migration ran clean locally. **Staging: unknown** — not applied, and no access to inspect it.

- Change: Source-of-truth document moved (external to this repo)
  - Location: `docs/SPEC-v1.md` → `docs/SPEC.md` (API team's doc)
  - Previous State: `docs/SPEC-v1.md` treated as the spec
  - New State: `docs/SPEC.md` is the spec; the old path is dead
  - Reason: API team relocated it; Priya has already informed the team
  - Validation: Grepped this repo — **no in-repo references to `SPEC-v1.md` exist**, so no repo fix is needed. Note that neither `docs/SPEC.md` nor `docs/SPEC-v1.md` is present in this repository; the file lives with the API team.

- Change: Project-management state
  - Location: Issue tracker, ticket **AUTH-214**
  - Previous State: No ticket for the introspection rate limit
  - New State: Priya said she would open AUTH-214 for Diego's team to raise the limit or provide a bulk endpoint
  - Reason: Unblocks refresh tokens
  - Validation: **Not verified** — stated as an intention at the end of the session; ticket existence not confirmed.

- Change: Repository state
  - Location: branch `feat/auth-rebuild`, HEAD `7991fb7` ("chore: baseline without session work")
  - Previous State: Same commit, clean tree
  - New State: `migrations/` and `src/auth/` untracked; **nothing from this session is committed**; branch has no upstream tracking branch, so nothing is pushed either
  - Reason: Session ended before committing
  - Validation: `git status` at end of session.

- Stale, not changed: `docs/ARCHITECTURE.md` still says "Session storage approach is under active decision." That is now false — the cookie decision is final. The file was not updated this session.

---

## 5. Validated or Approved Items

- Item: Login form behaviour
  - Validation Method: Manual test by a human
  - Evidence: Priya ran the dev server, typed an invalid email and saw the error, typed a valid one and saw it post
  - Result: **Accepted** by Priya

- Item: httpOnly-cookie session storage approach
  - Validation Method: Human decision/approval
  - Evidence: Priya: "Cookie... Lock that in."
  - Result: **Approved, final**

- Item: `migrations/002_add_sessions.sql` against local dev DB
  - Validation Method: Migration execution
  - Evidence: Ran clean on Priya's local dev database
  - Result: **Applied successfully (local dev only)**

Nothing else is validated. No automated test was written or executed this session; `npm test` was not run.

---

## 6. Open, Uncertain, or Unverified Items

- **Session TTL (currently 12h placeholder in `src/auth/session.ts`)** — Status: Waiting for Approval
  - Detail: Product/security call owned by Sam, who is out until Monday (expected 2026-08-03). Staging migration defaults depend on it.
  - What would resolve it: Sam's decision on TTL.

- **Refresh tokens** — Status: Blocked
  - Detail: Per-request introspection exceeds the 10 req/s limit on `api.relay.example`; batching failed. Needs Diego's team to raise the limit or ship a bulk endpoint. Ticket AUTH-214.
  - What would resolve it: An API-side change; then a fresh design that does not introspect per request.

- **Automated tests for `session.ts` and `login-form.tsx`** — Status: Deferred → now the next action
  - Detail: Never written. `package.json` has `"test": "vitest run"` but **vitest is not listed in dependencies or devDependencies**, so `npm test` will likely fail until it is installed. Not verified — no install or test run was attempted.
  - What would resolve it: `npm i -D vitest` (plus a DOM environment / testing-library if the form test needs rendering), then write and run the tests.

- **Login is not wired end to end** — Status: Open
  - Detail: No code in this repo calls `issueSession()`, reads `COOKIE_NAME`, or applies `COOKIE_OPTS`; `LoginForm` receives `onSubmit` from a caller that does not exist here. The API that must set the cookie is a separate service (`api.relay.example`, not in this repo).
  - What would resolve it: Confirming where the cookie is actually set (API service vs this SPA) and building that call path.

- **CSRF protection** — Status: Open
  - Detail: A direct consequence of the cookie decision, called out when the decision was made. `sameSite: "lax"` is the only mitigation present; no CSRF token flow exists.
  - What would resolve it: A CSRF design agreed with the API team, then implementation.

- **`SESSION_SECRET`** — Status: Needs Validation
  - Detail: `session.ts` falls back to the literal `"dev-only-secret"` if the env var is missing. No environment was checked this session.
  - What would resolve it: Confirm the var is set in every non-local environment; consider failing fast instead of falling back.

- **Staging database state** — Status: Unknown / Blocked
  - Detail: Migration 002 was **not** applied to staging and staging could not be inspected (no access). Do not assume it is either applied or unapplied.
  - What would resolve it: Priya applying it after the TTL sign-off, or someone with access checking.

- **AUTH-214** — Status: Needs Validation
  - Detail: Priya said she would open it; not confirmed created, and the number was quoted before creation.
  - What would resolve it: Look it up in the tracker.

- **`docs/ARCHITECTURE.md` is stale** — Status: Open
  - Detail: Claims session storage is "under active decision"; it is decided.
  - What would resolve it: One-line edit once the auth work is committed.

---

## 7. Risks and Constraints

- Risk: All of this session's work is uncommitted and unpushed
  - Impact: Total loss of the session's output if the working tree is lost
  - Likelihood: Low per day, but non-zero and cheap to eliminate
  - Mitigation: Commit `src/auth/` and `migrations/` on `feat/auth-rebuild` first thing; the branch also has no upstream, so push it
  - Owner: Priya
  - Status: Open

- Risk: `SESSION_SECRET` fallback to a hardcoded dev secret
  - Impact: If it ever reaches a real environment, session tokens are forgeable — full account takeover
  - Likelihood: Medium (silent fallback, no startup check)
  - Mitigation: Throw on missing secret outside local dev; verify env config
  - Owner: Unassigned
  - Status: Open

- Risk: Cookie auth without CSRF handling
  - Impact: State-changing requests become cross-site forgeable; this was the known cost of the cookie decision
  - Likelihood: Medium — `sameSite: "lax"` blunts but does not close it
  - Mitigation: Agree a CSRF approach with the API team before login ships
  - Owner: Unassigned
  - Status: Open

- Risk: Staging schema drift
  - Impact: Staging lacks the `sessions` table; when the TTL changes column defaults, an out-of-order apply could produce different defaults in staging vs local
  - Likelihood: Medium
  - Mitigation: Apply migration 002 to staging only after Sam's TTL decision, as agreed
  - Owner: Priya
  - Status: Blocked on TTL

**Constraints:**
- `api.relay.example` rate-limits token introspection at **10 requests/second**. This is a hard external ceiling and it is what killed the refresh design.
- No staging access from this session — anything about staging is unverifiable here.
- `src/legacy/` is **frozen**. Not to be refactored, tidied, or touched, in any session.
- Sam (TTL owner) is unavailable until Monday; Diego's team owns the API-side change for refresh.
- The API is a separate service not in this repo, so parts of "end to end login" cannot be built or verified from here alone.

---

## 8. Actual End-of-Session State

**Complete:** Session-storage decision (cookie, final). Login form, accepted by Priya. Migration file written and applied to local dev DB.

**In progress:** Auth module as a whole — `src/auth/session.ts` exists and compiles as a standalone module but is not called by anything.

**Incomplete:** End-to-end login (no wiring, no cookie actually set anywhere in this repo). Tests. CSRF. TTL confirmation. `docs/ARCHITECTURE.md` update.

**Blocked:** Refresh tokens (AUTH-214 / 10 req/s introspection limit). Staging migration (waiting on Sam's TTL).

**Ready for review:** `src/auth/login-form.tsx` — already reviewed and accepted informally by Priya.

**Not ready for release/deployment:** Everything. Uncommitted, untested, unwired, no CSRF, dev-secret fallback in place.

**Changed since session start:** Three new untracked files (`src/auth/session.ts`, `src/auth/login-form.tsx`, `migrations/002_add_sessions.sql`); local dev DB now has the `sessions` table; git HEAD unchanged at `7991fb7` on `feat/auth-rebuild`.

**Prioritized queue after the next action (§9):**
1. Commit and push the auth work on `feat/auth-rebuild` (do this first if you want the safety, it takes a minute).
2. Wire the login flow: establish where the cookie is set and connect `LoginForm` → session issuance.
3. Agree and implement CSRF handling with the API team.
4. Chase Sam on TTL (Monday), then Priya applies migration 002 to staging.
5. Confirm AUTH-214 exists and is with Diego's team; only revisit refresh tokens after the API-side change lands.
6. Fix the `SESSION_SECRET` fallback; update the stale line in `docs/ARCHITECTURE.md`.

---

## 9. Exact Next Action

Next Action: Write and run vitest coverage for `src/auth/session.ts` and `src/auth/login-form.tsx` — the work deferred mid-session, and now the only unblocked item on the critical path.
Start From: `D:\Projects\Skills\project-relay-workspace\iteration-2\eval-0-daily-from-transcript\old_skill\project`, branch `feat/auth-rebuild` (HEAD `7991fb7`). Read `src/auth/session.ts` first; its exported surface is `issueSession`, `readSession`, `COOKIE_NAME`, `COOKIE_OPTS`.
Required Inputs: vitest — `"test": "vitest run"` exists in `package.json` but vitest is **not** in dependencies/devDependencies, so install it (`npm i -D vitest`, plus jsdom/testing-library if you render the form). `jose@5.9.6` is already a dependency.
Expected Output: New test files under `src/auth/` (e.g. `session.test.ts`, `login-form.test.tsx`) covering: a token issued by `issueSession` round-trips through `readSession` and returns the right `sub`; `readSession` returns `null` for a tampered/garbage token; an expired token is rejected; `COOKIE_OPTS` has `httpOnly` and `secure` true; the form shows the `role="alert"` error for an email without `@` and calls `onSubmit` for a valid one.
Acceptance Criteria: `npm test` passes locally, and the run is recorded in the next handoff as evidence — this session produced zero test evidence, do not repeat that.
Do Not Change: `src/legacy/` — anything, ever (frozen, removed in Q4, previously broke billing). `TTL_SECONDS = 60 * 60 * 12` in `session.ts` — it is a deliberate placeholder awaiting Sam; test around it, don't "fix" it. `COOKIE_OPTS` httpOnly/secure/sameSite — these encode the locked security decision. Do not re-run `migrations/002_add_sessions.sql` against the local dev DB; it is already applied.
Blocking Conditions: None for the tests. If the vitest install is not possible in your environment, write the test files anyway and record explicitly that they were not run.

---

## 10. Continuation Sources

| Source | Location / Identifier | Purpose |
|---|---|---|
| Repository root | `D:\Projects\Skills\project-relay-workspace\iteration-2\eval-0-daily-from-transcript\old_skill\project` | All work below lives here |
| Branch / commit | `feat/auth-rebuild` @ `7991fb7` "chore: baseline without session work"; no upstream | Baseline; session work is untracked on top of it |
| Session helper | `src/auth/session.ts` | JWT issue/verify, cookie name and options, TTL placeholder |
| Login form | `src/auth/login-form.tsx` | Accepted UI component |
| Migration | `migrations/002_add_sessions.sql` | `sessions` table; applied to local dev only |
| Frozen code | `src/legacy/admin.js` | Do not touch — has its own cookie parsing, deliberately left alone |
| Architecture note | `docs/ARCHITECTURE.md` | Repo overview; its session-storage line is now stale |
| API spec (external) | `docs/SPEC.md` in the API team's docs — **not** `docs/SPEC-v1.md`, which is dead; neither file exists in this repo | Contract for the separate API service |
| Ticket | **AUTH-214** | Raise the introspection rate limit or add a bulk endpoint; owner Diego's team; creation unconfirmed |
| External service | `api.relay.example` | Separate API; 10 req/s introspection limit; must set the session cookie |
| Scripts | `package.json` → `dev` (vite), `test` (vitest run), `build` | Local commands |
| Raw session record | `SESSION-TRANSCRIPT.md` (repo root) | Full transcript, only if this handoff leaves a question open |
| People | Sam — TTL decision, back Monday 2026-08-03. Diego's team — API rate limit. Priya — staging migration, AUTH-214 | Owners of the blocked items |

---

## 11. Work That Must Not Be Repeated

- **Per-request token introspection for refresh tokens** — Reason: `api.relay.example` rate-limits introspection at 10 req/s; the SPA alone exceeds that on page load. Explicitly banned by Priya ("Don't try that again"). Needs an API-side change first.
- **Batching the introspection calls** — Reason: Already tried this session; it moved the traffic spike rather than removing it. It does not solve the limit.
- **Re-opening localStorage vs cookie for session storage** — Reason: Decided and locked. Third-party analytics scripts on the marketing pages make a JS-readable token unacceptable.
- **Touching `src/legacy/` in any way, including the tempting `admin.js` refactor onto the new session helper** — Reason: Frozen, removed in Q4, and the last cleanup broke billing for two days. This was proposed this session and refused.
- **Re-running `migrations/002_add_sessions.sql` against the local dev database** — Reason: Already applied, ran clean. Re-running it will fail on the existing table.
- **Applying migration 002 to staging** — Reason: Not yours to do. Priya applies it after Sam's TTL sign-off, because column defaults depend on the TTL.
- **Manually re-testing the login form's validation** — Reason: Priya already exercised it and accepted it. Only re-test if the component changes.
- **Pointing anything at `docs/SPEC-v1.md`** — Reason: Dead path, superseded by `docs/SPEC.md`; the team has already been told.
