# relay-web — project constraints

Frontend: React + Vite. The API is a separate service at `api.relay.example` (not in this repo).
Test runner: `vitest` (`npm test`).

For current work-in-progress state, see `HANDOFF.md`.

## Hard rules

**Never modify anything under `src/legacy/`.** Not a refactor, not a tidy-up, not a
"while I'm in here". It is the frozen pre-2025 jQuery admin and it is being deleted in Q4. It does
its own cookie parsing and that is intentional — do **not** migrate it onto the new session helper.
The last person who tidied it broke billing for two days. If something seems to require touching
it, stop and ask.

**Session storage is a JWT in an httpOnly cookie.** This is a closed decision, not an open
question. Do not propose or switch to `localStorage`/bearer-token storage: third-party analytics
scripts run on the marketing pages, so a readable token turns any XSS into account takeover. Cookie
config lives in `COOKIE_OPTS` in `src/auth/session.ts` (`httpOnly`, `sameSite=lax`, `secure`).
Because it's a cookie, CSRF handling is required.

**Do not re-attempt per-request token introspection for refresh tokens.**
`api.relay.example` rate-limits the introspection endpoint at 10 req/s and the SPA alone exceeds
that on page load. Batching was tried; it only moves the spike. This is blocked on Diego's team
(raise the limit or ship a bulk endpoint) under ticket AUTH-214. Don't rebuild it hoping for a
different result.

**`TTL_SECONDS` in `src/auth/session.ts` is a placeholder, not a decision.** Sam owns the real
value; it's a product/security tradeoff. Leave the 12-hour placeholder and its flag comment alone
until he rules.

## Docs

`docs/SPEC-v1.md` is dead. The current API spec is `docs/SPEC.md`. Never link or refer to the `-v1`
path.

## Environments

Claude has access to the local dev database only. **No staging access** — never claim staging's
schema or migration state, and don't try to apply migrations there. Priya applies staging
migrations by hand.
