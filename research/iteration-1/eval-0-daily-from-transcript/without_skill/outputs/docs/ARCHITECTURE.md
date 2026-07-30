# relay-web architecture

Frontend: React + Vite. API: separate service at api.relay.example (not in this repo).
Auth: see src/auth/.

Session storage: **decided 30 July 2026 — HS256 JWT in an httpOnly cookie**, not localStorage.
Third-party analytics scripts run on the marketing pages, so a JS-readable token would turn any XSS
into full account takeover. Cookie name and options are exported from `src/auth/session.ts`
(`httpOnly`, `sameSite=lax`, `secure`). Consequence: the API sets the cookie header, and CSRF
handling is required.

Refresh tokens are not implemented — blocked on an introspection rate limit at the API side
(AUTH-214). See HANDOFF.md.

`src/legacy/` contains the pre-2025 jQuery admin. Frozen.
