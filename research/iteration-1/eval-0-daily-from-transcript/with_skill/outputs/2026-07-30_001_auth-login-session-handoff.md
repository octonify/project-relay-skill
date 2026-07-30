# Daily Handoff — relay-web — 2026-07-30

Project: relay-web (package version 0.3.1)
Date: 2026-07-30
Handoff ID: 2026-07-30_001
Session Scope: Auth rebuild — session storage decision, login form, sessions table; refresh tokens attempted and abandoned
Workstream: Auth rebuild (relay-web)
Prepared By: Claude, working session with Priya (engineer)
End-of-Session Status: Login path built and manually exercised in dev by Priya. Refresh tokens blocked and parked as AUTH-214. No automated tests written. Nothing committed — all new work is untracked in the working tree on `feat/auth-rebuild`.

---

## 1. Session Objective

**Intended objective:** "Get login working end to end, including refresh tokens." Signup already existed before this session.

**Actually completed:**
- Session-storage approach decided and locked (httpOnly cookie, not localStorage).
- `src/auth/session.ts` written — HS256 JWT issue/verify via `jose`, plus exported cookie config.
- `src/auth/login-form.tsx` written — email/password fields, client-side email validation, `role="alert"` error region.
- `migrations/002_add_sessions.sql` written and applied to Priya's **local dev** database.

**Not completed:**
- Refresh tokens — attempted, found unworkable, parked (see AUTH-214).
- Vitest coverage for `src/auth/session.ts` and `src/auth/login-form.tsx` — deliberately deferred mid-session.
- Final session TTL value — deferred to Sam (product/security call).
- Staging database migration — no staging access; Priya will do it herself.
- CSRF handling, which the cookie decision makes necessary.

**Scope changes during session:**
- Test-writing was pulled forward in the plan then pushed back at Priya's request ("hold off — I'd rather get refresh tokens in first while we've got the context").
- Refresh tokens were dropped from this session's scope after the rate-limit discovery and converted into ticket AUTH-214 (a dependency on Diego's team), so the session ended smaller than the stated objective.
- A proposed refactor of `src/legacy/admin.js` onto the new session helper was raised and rejected outright.

---

## 2. Completed Work

- **Action:** Implemented session issuing/verification and cookie configuration.
  - Result: `issueSession(userId)` signs an HS256 JWT via `jose`; `readSession(token)` verifies and returns `{ sub }` or `null`; module exports `COOKIE_NAME = "relay_session"` and `COOKIE_OPTS = { httpOnly: true, sameSite: "lax", secure: true, path: "/" }`.
  - Location: `src/auth/session.ts`
  - Status: Complete as written, **untested** (no unit tests, no build/typecheck run this session).
  - Evidence: File present in working tree; contents read at handoff time. TTL is a placeholder — `const TTL_SECONDS = 60 * 60 * 12;` at `src/auth/session.ts:6`, with the comment "TTL is provisional - waiting on product decision."

- **Action:** Built the login form component.
  - Result: Controlled email/password inputs, submit blocked with "Enter a valid email" when the email lacks `@`, error rendered in a `<p role="alert">` region for screen readers, `onSubmit(email, password)` called on valid input.
  - Location: `src/auth/login-form.tsx`
  - Status: Complete and accepted by Priya.
  - Evidence: Priya loaded the dev server, entered an invalid email and saw the error, entered a valid email and saw it post. Her words: "That's fine, I'm happy with the form."

- **Action:** Created the sessions table migration and applied it locally.
  - Result: `sessions` table with `id uuid PRIMARY KEY`, `user_id uuid NOT NULL REFERENCES users(id)`, `issued_at timestamptz NOT NULL DEFAULT now()`, `expires_at timestamptz NOT NULL`, plus `sessions_user_id_idx` on `(user_id)`.
  - Location: `migrations/002_add_sessions.sql`
  - Status: Applied to local dev database only.
  - Evidence: Migration ran clean against Priya's local dev database during the session. Staging was **not** touched and its state is unknown.

- **Action:** Investigated the refresh-token design and established that it is not viable as designed.
  - Result: The intended flow (rotating server-side refresh token + short-lived access token) requires a token-introspection call per request; `api.relay.example` rate-limits the introspection endpoint at 10 requests/second, which the SPA alone would exceed on page load at current traffic. Batching the introspection calls was tried and only moved the spike rather than removing it.
  - Location: No code kept. Nothing from this attempt is in the working tree.
  - Status: Abandoned this session; escalated to ticket AUTH-214.
  - Evidence: Observed rate limit on the introspection endpoint; observed behaviour of the batching attempt.

---

## 3. Decisions Made

- **Decision:** Store the session JWT in an httpOnly cookie, not in localStorage.
  - Rationale: The marketing pages carry third-party analytics scripts. A token in localStorage is readable by any injected script, so an XSS anywhere in the app becomes full account takeover. Priya: "I'm not putting a bearer token where they can reach it."
  - Options considered: JWT in localStorage (simpler to wire from the SPA) vs JWT in an httpOnly cookie.
  - Rejected: localStorage — rejected on the XSS/account-takeover exposure, not on effort.
  - Expected impact: The API must set the cookie header, and CSRF handling becomes mandatory (not yet built). `COOKIE_OPTS` in `src/auth/session.ts` is the single source for cookie flags.
  - Status: **Final** — explicitly locked in by Priya ("Lock that in").

- **Decision:** Session TTL is not ours to set; the 12-hour value stays as a flagged placeholder.
  - Rationale: It is a product/security tradeoff owned by Sam, and 12 hours was an arbitrary guess.
  - Options considered: pick a defensible value now vs wait for the owner.
  - Rejected: choosing a value in this session.
  - Expected impact: `src/auth/session.ts:6` must not be treated as settled. The sessions-table column defaults depend on it, which is why the staging migration is also waiting.
  - Status: **Pending Approval** — Sam, who is out until Monday.

- **Decision:** Park the refresh-token work; do not retry the introspection-per-request approach.
  - Rationale: Hard external limit (10 req/s on introspection at `api.relay.example`). It cannot be solved on our side; batching was already tried and failed.
  - Options considered: per-request introspection, batched introspection.
  - Rejected: both — batching moved the traffic spike rather than eliminating it.
  - Expected impact: Refresh tokens are now dependent on Diego's team either raising the rate limit or providing a bulk endpoint. Tracked as **AUTH-214** (opened by Priya).
  - Status: **Final for this session**, blocked externally.

- **Decision:** `src/legacy/` is frozen — do not touch it at all, ever.
  - Rationale: It is being removed in Q4, and the last person who "tidied" it broke billing for two days.
  - Options considered: refactoring `src/legacy/admin.js` to use the new session helper instead of its own cookie parsing.
  - Rejected: the refactor, unconditionally.
  - Expected impact: `src/legacy/admin.js` keeps its own cookie parsing and will duplicate/diverge from `src/auth/session.ts`. That duplication is accepted, not an oversight.
  - Status: **Final** — standing constraint beyond this session.

- **Decision:** Write the auth unit tests after refresh tokens rather than before.
  - Rationale: Priya wanted to use the live context for refresh tokens first.
  - Expected impact: Refresh tokens then got blocked, so the session ended with neither — the tests are now the first unblocked piece of work outstanding.
  - Status: **Provisional** — sequencing only; the tests are still wanted.

- **Decision:** `docs/SPEC.md` is the canonical API spec; `docs/SPEC-v1.md` is dead.
  - Rationale: The API team moved the document. Priya has already told the rest of the team.
  - Expected impact: Anything still pointing at `docs/SPEC-v1.md` is wrong and should be repointed.
  - Status: **Final** (superseded document).

---

## 4. What Changed

- Change: New session module created.
- Location: `src/auth/session.ts`
- Previous State: Did not exist.
- New State: HS256 JWT issue/verify via `jose` 5.9.6, exported `COOKIE_NAME` / `COOKIE_OPTS`, placeholder `TTL_SECONDS = 43200`.
- Reason: Implements the httpOnly-cookie session decision.
- Validation: Not validated — no unit test, no build, no typecheck run this session.

- Change: New login form component created.
- Location: `src/auth/login-form.tsx`
- Previous State: Did not exist.
- New State: Email/password form with client-side email validation and an `role="alert"` error region.
- Reason: Login UI for the end-to-end flow.
- Validation: Manually exercised by Priya on the dev server (invalid then valid email); accepted by her.

- Change: New database migration created and applied to local dev only.
- Location: `migrations/002_add_sessions.sql`
- Previous State: No `sessions` table in the local dev database.
- New State: `sessions` table plus `sessions_user_id_idx` present in the local dev database.
- Reason: Server-side session records.
- Validation: Migration ran clean locally. **Staging: unknown — no access.**

- Change: Source of truth for the API spec moved.
- Location: `docs/SPEC-v1.md` → `docs/SPEC.md` (API team's document).
- Previous State: `docs/SPEC-v1.md` was the referenced spec.
- New State: `docs/SPEC.md` is canonical; `docs/SPEC-v1.md` is dead.
- Reason: The API team relocated it; Priya has already informed the team.
- Validation: Stated by Priya. Note: **neither file is present in this repository** at handoff time (`docs/` contains only `ARCHITECTURE.md` and this `handoffs/` directory), so the document lives outside this repo and its location was not verified.

- Change: Project-management state — refresh tokens converted from in-session work into an external dependency.
- Location: Ticket **AUTH-214** (opened by Priya; tracker URL not captured this session).
- Previous State: Refresh tokens were in scope for today.
- New State: Blocked pending Diego's team raising the introspection rate limit or supplying a bulk endpoint.
- Reason: Hard 10 req/s rate limit.
- Validation: Ticket ID stated by Priya; ticket contents not seen.

- Change: Process constraint made explicit — `src/legacy/` is off-limits.
- Location: `src/legacy/` (currently `src/legacy/admin.js`).
- Previous State: `docs/ARCHITECTURE.md` describes it as "Frozen"; the practical boundary was informal.
- New State: Explicit standing instruction: no changes, no refactors, no tidying.
- Reason: Prior breakage of billing for two days; the directory is being deleted in Q4.
- Validation: Directive from Priya; no files under `src/legacy/` were modified (still tracked and unchanged in git).

- Change: Repository working state — three new untracked paths, zero commits.
- Location: `feat/auth-rebuild` @ `7991fb7` ("chore: baseline without session work"), no upstream tracking branch.
- Previous State: Clean tree at `7991fb7`.
- New State: `git status` shows untracked `src/auth/` and `migrations/`. All of today's work exists only in the working tree.
- Reason: Priya finished for the day without committing.
- Validation: `git status --short` at handoff time: `?? migrations/`, `?? src/auth/`.

---

## 5. Validated or Approved Items

- Item: Login form behaviour (validation error path and successful submit).
- Validation Method: Manual test by Priya against the running dev server.
- Evidence: Bad email produced the error message; a valid email posted the form. Priya: "I'm happy with the form."
- Result: **Accepted** by the engineer who owns the work.

- Item: `migrations/002_add_sessions.sql` against the local dev database.
- Validation Method: Migration executed by Claude on Priya's local dev database.
- Evidence: "It ran clean."
- Result: **Applied — local dev only.** No other environment.

- Item: The introspection rate limit that blocks the refresh-token design.
- Validation Method: Observed during implementation, plus an attempted batching mitigation.
- Evidence: `api.relay.example` limits the introspection endpoint to 10 requests/second; the SPA alone would exceed it on page load at current traffic; batching moved the spike instead of removing it.
- Result: **Verified blocker** — this is why the approach was abandoned rather than deferred.

Nothing else was validated. In particular there is no test run, no build, no typecheck, and no deployment evidence from this session.

---

## 6. Open, Uncertain, or Unverified Items

- **Session TTL final value** — Status: Waiting for Approval
  - Detail: `src/auth/session.ts:6` holds a placeholder `60 * 60 * 12` (12 hours), flagged in a code comment. Owner is Sam; he is out until Monday. The `sessions` table column defaults depend on this value, which also gates the staging migration.
  - What would resolve it: Sam's decision on the TTL.

- **Refresh tokens** — Status: Blocked
  - Detail: Tracked as AUTH-214. Needs Diego's team to raise the 10 req/s introspection limit or expose a bulk introspection endpoint. No local workaround exists (see section 11).
  - What would resolve it: An API-side change from Diego's team.

- **Staging database state** — Status: Unknown / Needs Validation
  - Detail: Claude had no staging access this session, so it is genuinely unknown whether `002_add_sessions.sql` — or anything else — has been applied to staging. Do not assume it is unapplied either. Priya will run it herself after Sam signs off on the TTL.
  - What would resolve it: Priya (or someone with staging access) inspecting the staging schema.

- **No automated tests for the new auth code** — Status: Needs Validation
  - Detail: Vitest coverage for `src/auth/session.ts` (JWT round trip, expiry, tampered-token rejection) and `src/auth/login-form.tsx` (validation path, submit path, `role="alert"` presence) was planned and deliberately not written.
  - What would resolve it: Writing the tests — see section 9.

- **The test toolchain may not run as-is** — Status: Needs Validation
  - Detail: `package.json` defines `"test": "vitest run"` but **`vitest` is not listed in `dependencies` or `devDependencies`** (only `react` 18.3.1 and `jose` 5.9.6 are), and there is no `node_modules/` in the project directory. `npm test` was not run this session.
  - What would resolve it: `npm install` plus adding vitest (and a React testing library for the component test) as devDependencies; then confirm `npm test` executes.

- **CSRF protection for cookie-based sessions** — Status: Open
  - Detail: The httpOnly-cookie decision was explicitly taken knowing it "needs CSRF handling". `sameSite: "lax"` is set, but no CSRF token flow exists in this repo. Nothing was built for it this session.
  - What would resolve it: A design + implementation for CSRF, coordinated with whoever owns the API endpoint that sets the cookie.

- **The API side of the cookie flow** — Status: Open / external
  - Detail: `COOKIE_OPTS` is exported from this repo, but the API at `api.relay.example` (not in this repo) is what must actually set the `Set-Cookie` header. No API-side change was made or confirmed this session, so "login end to end" is not actually wired end to end.
  - What would resolve it: Confirming/implementing the cookie-setting response in the API service against `docs/SPEC.md`.

- **`SESSION_SECRET` falls back to a hardcoded dev secret** — Status: Open
  - Detail: `src/auth/session.ts:3` uses `process.env.SESSION_SECRET ?? "dev-only-secret"`. Acceptable locally; must not reach any deployed environment.
  - What would resolve it: A real secret in each environment's config and a decision on whether to fail hard when it is missing.

- **`secure: true` cookie flag vs the local dev server** — Status: Needs Validation
  - Detail: `COOKIE_OPTS.secure = true` means browsers will not store the cookie over plain HTTP. Whether the Vite dev server runs HTTPS was not checked, and the full cookie round trip was never exercised — Priya's manual test confirmed the form posts, not that a session cookie was set and read back.
  - What would resolve it: Exercising a real login against the dev server and inspecting the cookie jar.

- **No typecheck or build run** — Status: Needs Validation
  - Detail: Neither `npm run build` nor a TypeScript check was run over the new files. `COOKIE_OPTS`'s `sameSite: "lax"` is inferred as `string`, which can fail to satisfy stricter cookie-option types at the call site (would need `as const`). Unconfirmed — there is no call site yet.
  - What would resolve it: Running the build/typecheck once the API integration point exists.

- **`docs/ARCHITECTURE.md` is now stale** — Status: Open
  - Detail: Line 4 still reads "Session storage approach is under active decision." That decision was made and locked today (httpOnly cookie). The file was not updated this session.
  - What would resolve it: A one-line edit recording the cookie decision.

- **AUTH-214 ticket link** — Status: Open
  - Detail: The ticket ID is known; the tracker URL was never stated and was not captured.
  - What would resolve it: Priya pasting the link.

---

## 7. Risks and Constraints

- Risk: Today's entire output is uncommitted and untracked (`src/auth/`, `migrations/`).
- Impact: High — a stash mishap, branch switch, or clean would lose the session decision's implementation, and there is no upstream copy at all.
- Likelihood: Low-moderate over a single night, but the loss is unrecoverable.
- Mitigation: Commit on `feat/auth-rebuild` first thing (section 9).
- Owner: Priya
- Status: Open

- Risk: The 12-hour TTL placeholder gets treated as the agreed value.
- Impact: Moderate-high — it is a security/product tradeoff nobody has signed off, and it drives the `sessions` column defaults, so a wrong value propagates into schema defaults and into staging.
- Likelihood: Moderate — the code compiles and works, so it looks finished.
- Mitigation: The in-code comment at `src/auth/session.ts:5-6`, this handoff, and the rule that staging is not migrated until Sam decides.
- Owner: Sam (decision), Priya (holding the line)
- Status: Waiting for Approval

- Risk: Cookie-based sessions ship without CSRF handling.
- Impact: High — CSRF was the known cost of rejecting localStorage; the cookie approach is not safe without it.
- Likelihood: Moderate, because the login flow otherwise looks complete.
- Mitigation: Recorded here as a blocking item for release; not started.
- Owner: Unassigned
- Status: Open

- Risk: Someone "helpfully" refactors `src/legacy/` onto the new session helper.
- Impact: High — the last such tidy-up broke billing for two days.
- Likelihood: Moderate — the duplication is genuinely visible and looks like a bug worth fixing.
- Mitigation: Explicit, repeated instruction (sections 3, 9, 11).
- Owner: Priya
- Status: Closed as a decision, live as a risk

- Risk: Refresh tokens stay blocked on another team.
- Impact: Moderate — the original objective ("login end to end, including refresh tokens") cannot be met without AUTH-214.
- Likelihood: Depends entirely on Diego's team.
- Mitigation: Ticket AUTH-214 raised; no attempt to work around it locally.
- Owner: Diego's team (API side), Priya (chasing)
- Status: Blocked

**Constraints:**
- No staging access from this session — staging schema state cannot be read or changed here.
- `api.relay.example` introspection endpoint: hard 10 requests/second limit. This is the binding technical constraint on any refresh-token design.
- `src/legacy/` is frozen and slated for deletion in Q4 — zero edits permitted.
- Sam (TTL owner) is unavailable until Monday; the TTL and therefore the staging migration cannot move before then.
- The API service at `api.relay.example` is a separate repository — anything requiring an API change is cross-team work.
- Signup already exists and is out of this session's scope.

---

## 8. Actual End-of-Session State

**Complete:**
- Session-storage decision (httpOnly cookie) — final.
- `src/auth/session.ts` — written, exports `issueSession`, `readSession`, `COOKIE_NAME`, `COOKIE_OPTS`.
- `src/auth/login-form.tsx` — written and manually accepted by Priya.
- `migrations/002_add_sessions.sql` — written and applied to the local dev database.

**In progress:**
- Nothing is mid-edit. No file is in a broken or half-refactored state.

**Incomplete:**
- Vitest coverage for `src/auth/session.ts` and `src/auth/login-form.tsx` — not started.
- CSRF handling — not started.
- API-side cookie issuance at `api.relay.example` — not started/not confirmed.
- `docs/ARCHITECTURE.md` update for the cookie decision — not done.

**Blocked:**
- Refresh tokens — AUTH-214, needs Diego's team.
- Final session TTL — needs Sam, back Monday.
- Staging migration — waits on the TTL decision, and Priya will run it personally.

**Ready for review:**
- `src/auth/login-form.tsx` (already accepted by Priya).
- `src/auth/session.ts` — readable and self-contained, but reviewers should know it has zero test coverage and no call site yet.

**Not ready for release/deployment:**
- The whole auth path: no tests, no CSRF, hardcoded dev secret fallback, unsettled TTL, and the API side not wired. Nothing here should go to staging or production.

**Changed since session start:**
- Branch `feat/auth-rebuild` is still at `7991fb7` ("chore: baseline without session work") with **no upstream tracking branch**; `git status --short` shows `?? migrations/` and `?? src/auth/`. Nothing was committed, staged, stashed, or pushed today.
- Local dev database now has the `sessions` table and `sessions_user_id_idx`.
- `src/legacy/admin.js` is untouched (still tracked and unmodified) — deliberately.
- A new ticket exists outside the repo: AUTH-214.
- Canonical API spec reference moved from `docs/SPEC-v1.md` to `docs/SPEC.md`.
- `SESSION-TRANSCRIPT.md` at the repo root holds the full raw session; this handoff supersedes the need to read it.

---

## 9. Exact Next Action

Next Action: Commit today's untracked auth work to `feat/auth-rebuild` so it is recoverable, then proceed to the queue below.
Start From: The project root, on branch `feat/auth-rebuild` at `7991fb7`. Run `git status --short` and confirm it still shows `?? migrations/` and `?? src/auth/` before staging anything.
Required Inputs: Only the existing working tree — `src/auth/session.ts`, `src/auth/login-form.tsx`, `migrations/002_add_sessions.sql`. No credentials, no external approvals.
Expected Output: One commit on `feat/auth-rebuild` containing exactly those three files, with a message noting that the session TTL is a placeholder pending Sam's decision.
Acceptance Criteria: `git log -1 --stat` lists the three files and nothing else; `git status --short` afterwards shows no untracked source or migration files (the new `docs/handoffs/` directory may legitimately appear).
Do Not Change:
- `src/legacy/**` — frozen, do not include it in the commit, do not "fix" its duplicate cookie parsing.
- `TTL_SECONDS` at `src/auth/session.ts:6` and the comment above it — the placeholder is deliberate and Sam's call.
- The `httpOnly` cookie approach — that decision is locked; do not reintroduce localStorage.
- Do not add refresh-token code — the design is blocked, not merely unfinished.
- Do not apply `migrations/002_add_sessions.sql` to staging — Priya does that herself after the TTL is settled.
Blocking Conditions: None. This action needs nothing from Sam, Diego, or staging.

**Prioritized queue after that (all unblocked unless noted):**
1. Write the deferred vitest coverage: `src/auth/session.ts` (JWT round trip, expiry rejection, tampered/garbage token → `null`) and `src/auth/login-form.tsx` (invalid email shows the `role="alert"` error and does not submit; valid email calls `onSubmit`). First add `vitest` (plus a React component-testing library) to `devDependencies` — `package.json` defines the `test` script but does not declare vitest, and `node_modules/` is absent, so `npm test` will not currently run.
2. Design and implement CSRF handling for the cookie session — the known, accepted cost of rejecting localStorage.
3. Confirm/implement the API-side `Set-Cookie` response at `api.relay.example` against `docs/SPEC.md`, and exercise a real login to prove the cookie is set and read back (watch `secure: true` vs a plain-HTTP dev server).
4. Update `docs/ARCHITECTURE.md` line 4 — it still says "Session storage approach is under active decision," which is now false.
5. Monday: get Sam's TTL decision, then update `src/auth/session.ts:6` and the `sessions` column defaults; only then does Priya apply the migration to staging.
6. Chase AUTH-214 with Diego's team (raised rate limit or bulk introspection endpoint) — refresh tokens stay parked until that lands.
7. Capture the AUTH-214 ticket URL in this handoff or the Master so the next reader can find it.

---

## 10. Continuation Sources

| Source | Location / Identifier | Purpose |
|---|---|---|
| Session module (cookie config + JWT) | `src/auth/session.ts` | Canonical session issue/verify and `COOKIE_NAME` / `COOKIE_OPTS`; TTL placeholder at line 6 |
| Login form component | `src/auth/login-form.tsx` | The accepted login UI |
| Sessions table migration | `migrations/002_add_sessions.sql` | Applied to local dev only; not staging |
| Frozen legacy code | `src/legacy/admin.js` | Do not modify — reference only |
| Architecture notes | `docs/ARCHITECTURE.md` | Project shape; line 4 is stale after today's decision |
| Canonical API spec | `docs/SPEC.md` (API team's document; **not present in this repo**) | Authoritative API contract. `docs/SPEC-v1.md` is dead — anything pointing at it is wrong |
| Raw session record | `SESSION-TRANSCRIPT.md` (repo root) | Full unedited session of 2026-07-30; this handoff replaces the need to read it |
| Branch | `feat/auth-rebuild`, head `7991fb7` "chore: baseline without session work", no upstream | All work sits untracked on top of this commit |
| Prior baseline commit | `fd5eced` "baseline" | Earlier baseline on the same branch |
| Refresh-token blocker ticket | **AUTH-214** (opened by Priya; URL not captured) | Tracks the API-side rate-limit dependency |
| Rate-limited dependency | `api.relay.example` token-introspection endpoint, 10 req/s | The constraint that killed the refresh-token design |
| Package/scripts | `package.json` — `dev: vite`, `test: vitest run`, `build: vite build`; deps `react@18.3.1`, `jose@5.9.6` | Note: vitest is used by the script but not declared as a dependency |
| TTL decision owner | Sam — unavailable until Monday | Owns the session TTL (product/security) |
| API-side owner | Diego's team | Owns raising the introspection limit / bulk endpoint |

---

## 11. Work That Must Not Be Repeated

- **Item:** The session-storage comparison (localStorage vs httpOnly cookie) — Reason: Settled and explicitly locked in by Priya. localStorage is rejected because third-party analytics scripts on the marketing pages mean any XSS would expose a bearer token and allow full account takeover. Do not reopen this to save CSRF work.
- **Item:** Refresh tokens via per-request token introspection — Reason: `api.relay.example` rate-limits the introspection endpoint at 10 requests/second; the SPA alone exceeds that on page load at current traffic. Not a tuning problem.
- **Item:** Batching the introspection calls — Reason: Already tried this session. It moved the traffic spike rather than reducing total request rate, so it does not clear the 10 req/s limit. Needs an API-side change (AUTH-214), full stop.
- **Item:** Refactoring `src/legacy/admin.js` (or anything under `src/legacy/`) to use the new session helper — Reason: Proposed and rejected outright. The directory is frozen and disappears in Q4, and the last person who tidied it broke billing for two days. The duplicate cookie parsing there is known and accepted.
- **Item:** Re-running `migrations/002_add_sessions.sql` against the local dev database — Reason: Already applied cleanly today; re-running would fail on the existing table. It has **not** been applied to staging, and applying it there is Priya's task after the TTL is settled — do not do it for her.
- **Item:** Choosing a session TTL — Reason: Not a technical call. Sam owns it; he is out until Monday. The 12-hour value in `src/auth/session.ts:6` is a flagged placeholder, not a proposal to defend.
- **Item:** Manual re-testing of the login form's validation and submit paths — Reason: Priya exercised both against the dev server and accepted the result. Re-check only if the component changes. This does **not** substitute for the automated tests, which were never written.
- **Item:** Repointing anything at `docs/SPEC-v1.md` — Reason: That document is dead; `docs/SPEC.md` replaced it and Priya has already notified the team.
