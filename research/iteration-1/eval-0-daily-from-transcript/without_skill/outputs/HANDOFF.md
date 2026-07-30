# Handoff — auth rebuild (relay-web)

**Session:** Thursday 30 July 2026 (Priya + Claude)
**Picking up:** Friday 31 July 2026
**Branch:** `feat/auth-rebuild` — HEAD `7991fb7 chore: baseline without session work`
**Nothing is committed.** All of today's work is uncommitted in the working tree.

Read this file only. You do not need `SESSION-TRANSCRIPT.md`; everything durable from it is
captured here or in `CLAUDE.md`.

---

## Start here tomorrow

Write the vitest coverage for `src/auth/session.ts` and `src/auth/login-form.tsx`.

This was the next task in the queue and got bumped mid-session (Priya wanted refresh tokens
attempted first while the context was fresh). Refresh tokens are now parked and blocked, so tests
are the top unblocked item. `vitest` is already the configured test runner (`npm test` →
`vitest run`) but is **not yet in `package.json` dependencies** — it will need adding.

Nothing else on the auth critical path can move forward tomorrow without Sam or Diego's team (see
Blocked, below).

---

## What landed today

All three files below are **untracked** (`git status` shows `?? src/auth/` and `?? migrations/`).

### `src/auth/session.ts` — new
Issues and verifies HS256 JWTs via `jose`. Exports:
- `issueSession(userId)` / `readSession(token)`
- `COOKIE_NAME = "relay_session"`
- `COOKIE_OPTS = { httpOnly: true, sameSite: "lax", secure: true, path: "/" }`

Secret comes from `process.env.SESSION_SECRET`, falling back to `"dev-only-secret"`.

**Verification status: none.** No tests exist; this has only been exercised indirectly by the login
form posting successfully.

### `src/auth/login-form.tsx` — new
Email + password fields, client-side email validation, error region with `role="alert"` for screen
readers.

**Verification status: manually accepted by Priya.** She ran the dev server, entered a bad email
and saw the error, entered a valid one and saw it post. She explicitly said she's happy with the
form — treat it as done and don't rework it unprompted.

### `migrations/002_add_sessions.sql` — new
Creates `sessions` (`id`, `user_id` FK → `users(id)`, `issued_at`, `expires_at`) plus
`sessions_user_id_idx` on `user_id`.

**Applied to Priya's local dev database — ran clean.**
**NOT applied to staging.** Claude has no staging access, so staging's actual schema state is
unknown and cannot be checked from here. Priya is doing staging herself, and is deliberately
waiting until Sam signs off on the TTL because the column defaults depend on that number. Do not
try to apply or verify this against staging.

---

## Decisions locked in (do not relitigate)

**Session storage = JWT in an httpOnly cookie.** Closed.
The alternative considered was JWT in `localStorage`. Rejected because the marketing pages carry
third-party analytics scripts, so any XSS anywhere in the app would hand those scripts a bearer
token and become full account takeover. The cookie is unreachable from JS. The accepted cost is
that the API must set the header and CSRF handling is needed.

CSRF handling is a known, unstarted consequence of this decision — it is not in today's code.

---

## Blocked / parked

### Refresh tokens — PARKED, needs another team
The intended design was a rotating server-side refresh token with a short-lived access token. It
does not work as-is: the flow needs a token-introspection call per request, and
`api.relay.example` rate-limits introspection at **10 requests/second**. At current traffic the SPA
alone would exceed that on page load. Batching the calls was tried and only moved the spike.

**Do not re-attempt this approach.** It cannot be fixed on our side. It needs Diego's team to
either raise the limit or give us a bulk introspection endpoint.

Ticket: **AUTH-214** (Priya was opening it at end of session).

### Session TTL — blocked on Sam, back Monday 3 August 2026
`TTL_SECONDS` in `src/auth/session.ts` is **12 hours as a placeholder**. That number is a guess and
is not a decision. The real call is a product/security tradeoff that Sam owns. He is out until
Monday.

Leave the placeholder in place and leave it flagged. Don't pick a "better" number.
This also gates the staging migration (column defaults depend on it).

---

## Housekeeping done

- `docs/ARCHITECTURE.md` updated — it previously said the session storage approach was "under
  active decision", which is now stale. It records the httpOnly-cookie decision.
- `CLAUDE.md` created — durable project constraints (frozen directories, locked decisions, doc
  paths) so they survive past this handoff.
- Checked for stale references to `docs/SPEC-v1.md`: **there are none in the codebase.** The only
  mention was inside `SESSION-TRANSCRIPT.md` itself. Note that `docs/SPEC.md` does not exist in
  this repo either — the spec is the API team's doc and lives outside it.

---

## Who owns what

| Item | Owner | Unblocks when |
|---|---|---|
| Session TTL value | Sam | Monday 3 Aug 2026 |
| Introspection rate limit / bulk endpoint (AUTH-214) | Diego's team | ticket picked up |
| Staging migration | Priya | after Sam's TTL call |
| Tests, CSRF handling | us | now |
