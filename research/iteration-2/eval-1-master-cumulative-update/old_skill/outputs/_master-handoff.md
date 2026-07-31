# Master Handoff - relay-web

Project: relay-web
Document Type: Master Handoff
Version: 3.0
Last Updated: 2026-07-30
Current Phase: Auth rebuild
Overall Status: In Progress
Canonical File: docs/handoffs/_master-handoff.md

---

## 1. Executive Summary

relay-web is the customer-facing React SPA for Relay. The current phase is a rebuild of
authentication, replacing the legacy jQuery admin's ad-hoc cookie handling with a single shared
session module.

Latest major progress: the session storage decision was reversed on 2026-07-28 after security
review — session JWTs now go in an httpOnly, secure, sameSite=lax cookie, not localStorage. The
shared session module `src/auth/session.ts` now exists and implements JWT issue/verify with `jose`
plus the cookie name and options. The API spec moved from `docs/SPEC-v1.md` to `docs/SPEC.md`.

Most important blocker: the cookie decision made CSRF protection mandatory and nothing has been
implemented — no CSRF token, check, or middleware exists anywhere in this repo. Secondary open
item: session TTL is still undecided and is currently hardcoded to 12h in `src/auth/session.ts`
with a "provisional" comment.

Immediate next action: implement CSRF protection for the cookie-based session, starting from
`src/auth/session.ts`. See section 17.

## 2. Project Purpose and Definition

Problem: authentication logic is duplicated across the SPA and the legacy admin, and neither is
audited.
Objective: one shared, reviewed session module used by all surfaces.
Final output: shipped auth stack + decommission path for src/legacy/.
Stakeholders: Priya (engineering), Sam (product/security), Diego (API team).
Success criteria: single session module, passing tests, security review sign-off.
Scope: relay-web SPA and its API contract.
Out of scope: rewriting src/legacy/admin.js. It is frozen and scheduled for removal in Q4 2026.

## 3. Locked Principles and Decisions

- Decision: Design tokens live in packages/tokens and are the only source of colour and spacing
  values. No hard-coded hex in components.
  - Rationale: three surfaces drifted apart in 2025; a single token package stopped it.
  - Date: 2026-05-12
  - Status: Final
  - Approval source: Priya + design review
  - Supersedes: per-app SCSS variables
  - Note: `packages/tokens` is not present in the working tree at commit a3549a9 — see section 13.

- Decision: src/legacy/ is frozen. No refactors, no renames, no "tidying".
  - Rationale: a cleanup in March 2026 broke billing for two days.
  - Date: 2026-03-30
  - Status: Final
  - Approval source: Priya
  - Supersedes: n/a

- Decision: The session JWT is stored in an httpOnly, secure, sameSite=lax cookie. The SPA must
  not use localStorage for the token and must not send a bearer header.
  - Rationale: third-party analytics scripts run on marketing pages; a token in localStorage is
    readable by any injected script, which makes any XSS equivalent to account takeover.
  - Options considered: localStorage bearer token, httpOnly cookie, in-memory only.
  - Rejected: localStorage (XSS exposure), in-memory only (breaks refresh on page reload).
  - Date: 2026-07-28
  - Status: Final
  - Approval source: Sam (security, written sign-off in AUTH-201) + Priya (engineering)
  - Supersedes: the 2026-07-20 localStorage + bearer-header decision recorded in Master v2.0.
  - Consequence: the API must set the cookie, and CSRF protection is now required (open — see
    sections 10 and 14).

- Decision (SUPERSEDED, retained for the record): Session tokens are stored in browser
  localStorage and attached as a bearer header.
  - Date: 2026-07-20
  - Status: Superseded on 2026-07-28 by the httpOnly-cookie decision above. Do not re-propose.

## 4. Project Structure

Repository: relay-web (this repo). API lives in a separate repo owned by Diego's team.
Workstreams: Auth rebuild (Priya), Design tokens (complete), Legacy decommission (not started).
Environments: local, staging, production.

## 5. Architecture and Workflow

React + Vite SPA. API at api.relay.example. Migrations applied by hand per environment.
Session transport: httpOnly + secure + sameSite=lax cookie named `relay_session`, set by the API,
never read by SPA JavaScript. JWTs are HS256, signed with `jose` using `process.env.SESSION_SECRET`
(falls back to a `dev-only-secret` literal in `src/auth/session.ts` when the env var is absent —
that fallback must not reach staging or production).
Approval gate: security-sensitive changes need Sam's sign-off before they reach staging. The
cookie/CSRF work is security-sensitive and falls under this gate.
Access restriction: only Priya has staging and production database access.

## 6. Sources of Truth

| Source | Location | Purpose | Authority | Status |
|---|---|---|---|---|
| API spec | docs/SPEC.md | Endpoint and auth contract, session cookie contract, error envelope | Diego's team | Current (since 2026-07-28) |
| API spec (old) | docs/SPEC-v1.md | Former API contract | Diego's team | Deleted 2026-07-28 — do not cite; wiki path 404s |
| Design tokens | packages/tokens | Colour/spacing values | Design review | Referenced but not present in this checkout — see section 13 |
| This document | docs/handoffs/_master-handoff.md | Project state | Canonical | Current |
| Security sign-off | ticket AUTH-201 | Written approval of the cookie decision | Sam | Current |

Precedence: for the auth/session contract, `docs/SPEC.md` wins over anything in this document; if
they disagree, update this document. For security posture, Sam's sign-off in AUTH-201 wins.

## 7. Workstream Status

### Auth rebuild

Purpose: one shared session module.
Owner: Priya
Current Status: In Progress
Completed: signup flow and password hashing (reported approved by Priya on 2026-07-22; not
verifiable in this checkout — see section 13); security review of session storage (2026-07-28,
rejected localStorage); API spec migration to docs/SPEC.md.
In Progress: cookie-based session module. `src/auth/session.ts` exists with `issueSession`,
`readSession`, `COOKIE_NAME = "relay_session"` and `COOKIE_OPTS` (httpOnly, secure, sameSite=lax).
No call site in this repo actually attaches the cookie to a response.
Blocked: nothing is hard-blocked, but CSRF protection cannot be considered done without Sam's
sign-off, and the API-side cookie set depends on Diego's team.
Open Decisions: session TTL (Sam); CSRF strategy (Priya + Sam).
Dependencies: API team for token endpoints and for actually setting the session cookie.
Next Action: implement CSRF protection for the cookie session (section 17).
Relevant Sources: src/auth/session.ts, docs/SPEC.md, ticket AUTH-201.

### Design tokens

Owner: design review. Current Status: Complete (2026-05-12). No further action expected.

### Legacy decommission

Owner: unassigned. Current Status: Not Started. Scheduled for Q4 2026. src/legacy/ is frozen
until then.

## 8. Important Project History

- 2026-03-30 - legacy cleanup broke billing; src/legacy/ frozen as a result.
- 2026-05-12 - design tokens consolidated into packages/tokens.
- 2026-07-18 - auth rebuild started.
- 2026-07-19 - `jose` chosen over `jsonwebtoken` for JWT signing.
- 2026-07-20 - localStorage + bearer header chosen for session storage (later reversed).
- 2026-07-22 - signup flow reported complete and approved.
- 2026-07-28 - security review with Sam reversed the storage decision: httpOnly cookie replaces
  localStorage, because analytics scripts on marketing pages make XSS an account-takeover path.
  This is the single most important direction change in the auth rebuild so far — it adds CSRF
  work and an API-side change that did not exist in the v2.0 plan.
- 2026-07-28 - `docs/SPEC-v1.md` deleted and replaced by `docs/SPEC.md` after Diego's team
  restructured the spec and dropped the version suffix.

## 9. Final Decisions

- Decision: use `jose` for JWT signing rather than jsonwebtoken.
- Date: 2026-07-19
- Rationale: ESM-native, works in edge runtimes.
- Impact: dependency added to package.json (verified: `jose` 5.9.6, and it is imported by
  src/auth/session.ts).
- Source: Priya
- Supersedes: n/a

- Decision: store the session JWT in an httpOnly, secure, sameSite=lax cookie; no localStorage,
  no bearer header from the SPA.
- Date: 2026-07-28
- Rationale: XSS via third-party analytics on marketing pages would otherwise equal account
  takeover.
- Impact: API must set the cookie; CSRF protection becomes mandatory; SPA fetch calls need
  credentials-included instead of an Authorization header.
- Source: Sam (security sign-off in AUTH-201), Priya
- Supersedes: the 2026-07-20 localStorage decision (Master v2.0, section 3).

- Decision: `docs/SPEC.md` replaces `docs/SPEC-v1.md` as the API contract source of truth.
- Date: 2026-07-28
- Rationale: Diego's team restructured the spec and dropped the version suffix.
- Impact: all internal links updated; the old path 404s in the wiki.
- Source: Diego's team, applied during the 2026-07-28 session.
- Supersedes: docs/SPEC-v1.md.

## 10. Open Decisions

- Decision Needed: session TTL
- Why It Matters: determines re-login frequency and the sessions table column defaults. Currently
  hardcoded as `TTL_SECONDS = 60 * 60 * 12` (12h) in src/auth/session.ts, marked provisional in a
  code comment — shipping without deciding means the placeholder becomes the default by accident.
- Available Options: 1h / 12h / 30d with sliding renewal
- Required Evidence: support-ticket volume for re-login complaints
- Decision Owner: Sam
- Deadline or Trigger: before staging deploy. As of the 2026-07-28 session Sam was away and due
  back Monday; still unresolved as of 2026-07-30.

- Decision Needed: CSRF strategy for the cookie-based session
- Why It Matters: sameSite=lax alone does not cover all cross-origin state-changing requests, and
  the cookie decision explicitly made CSRF protection a requirement. Nothing is implemented, so
  the auth stack is currently less safe than either of the two designs discussed.
- Available Options: double-submit cookie token, synchroniser token issued per session, strict
  Origin/Referer verification on state-changing routes, or sameSite=strict (rejected so far
  because it breaks inbound links from marketing pages).
- Required Evidence: which routes are state-changing per docs/SPEC.md; whether the API team can
  set a second (readable) CSRF cookie; whether any non-browser client uses the same endpoints.
- Decision Owner: Priya, with Sam's sign-off required (security gate)
- Deadline or Trigger: before any staging deploy of cookie auth.

## 11. Changes Since the Previous Baseline

Since Master v2.0 (2026-07-24):

- Reversed: session storage. localStorage + bearer header (v2.0 section 3, "Final") is superseded
  by an httpOnly/secure/sameSite=lax cookie, following security review on 2026-07-28.
- Added: CSRF protection is now a required, unstarted workstream item and a new open decision.
- Replaced: `docs/SPEC-v1.md` → `docs/SPEC.md` as the API contract source of truth; the source of
  truth table and the start guide were updated accordingly.
- Added: `src/auth/session.ts` now exists and implements JWT issue/verify plus cookie constants.
- Corrected: immediate next action. v2.0 said "implement signup email verification"; that work is
  not evidenced in the repo and has been demoted to the prioritised queue behind CSRF, which the
  2026-07-28 decision made a prerequisite for any staging deploy.
- Corrected: technical state. Commit was recorded as 7c21ab4; HEAD is a3549a9 on
  branch feat/auth-rebuild with a clean tree.
- Corrected: test and build status. v2.0 recorded both as "passing". Neither was verified this
  session and neither can be run in this checkout (no node_modules; `npm test` fails with
  "'vitest' is not recognized"). Both are now recorded as Unknown.
- Added: contradictions between v2.0's claims and the observable repository, recorded in
  section 13 rather than silently dropped.
- Incorporated: 2026-07-28_001_spec-move-handoff.md (was outstanding).

## 12. Superseded or Replaced Items

| Superseded Item | Replacement | Reason | Date |
|---|---|---|---|
| per-app SCSS variables | packages/tokens | drift across surfaces | 2026-05-12 |
| localStorage session token + bearer header (2026-07-20 decision) | httpOnly/secure/sameSite=lax cookie `relay_session` | XSS via third-party analytics equals account takeover; rejected by security review | 2026-07-28 |
| docs/SPEC-v1.md | docs/SPEC.md | Diego's team restructured the spec, version suffix dropped; old path 404s | 2026-07-28 |
| Master Handoff v2.0 next action "implement signup email verification" | "implement CSRF protection for the cookie session" | cookie decision created a prerequisite that gates staging | 2026-07-30 |

## 13. Contradictions and Resolution

- Contradiction: this document has claimed since v2.0 that the signup flow and argon2id password
  hashing are complete and approved, but the working tree at commit a3549a9 contains no
  `src/auth/signup.ts` and package.json has no argon2 dependency — only `react` and `jose`.
  - Conflicting sources: Master v2.0 section 7 and 2026-07-22_001_signup-handoff.md, versus the
    repository at a3549a9.
  - Verified current state: unresolved. The repository has a single squashed commit ("baseline",
    2026-07-30) whose history cannot corroborate or refute the earlier work.
  - Evidence that would settle it: the branch or PR containing the signup implementation, or
    Priya's review record from 2026-07-22.
  - Corrective action required: confirm with Priya before treating signup as done. Do not rebuild
    signup on the assumption it is missing until this is checked.

- Contradiction: sections 3 and 6 reference `packages/tokens`, and sections 2/17 reference
  `src/legacy/`; neither path exists in this checkout.
  - Verified current state: the working tree contains only `docs/`, `src/auth/session.ts` and
    `package.json`.
  - Evidence that would settle it: whether this checkout is a partial/squashed export of the full
    relay-web repo. Most likely explanation, but not verified this session.
  - Corrective action required: verify against the canonical relay-web remote. The "src/legacy/ is
    frozen" rule stays in force regardless — treat it as binding wherever the directory exists.

- Contradiction: the incorporated-dailies table has listed `2026-07-24_001_tokens-handoff.md` as
  incorporated since v2.0, but no such file exists in docs/handoffs/.
  - Verified current state: docs/handoffs/ contains only the 2026-07-22 and 2026-07-28 dailies
    plus this Master.
  - Corrective action required: none urgent — its content (design tokens complete) is already
    reflected here. The row is retained in section 19 with the file marked missing so nobody
    hunts for it.

## 14. Risks, Constraints, and Dependencies

- Risk (new, high): no CSRF protection exists for the cookie session. Until it lands, the cookie
  design is implemented only halfway and must not reach staging.
- Risk (new): `src/auth/session.ts` falls back to the literal `"dev-only-secret"` when
  `SESSION_SECRET` is unset. If that reaches a deployed environment, every session token is
  forgeable. Needs a fail-fast check before deploy.
- Risk (new): `TTL_SECONDS` is a hardcoded 12h placeholder; without a TTL decision the placeholder
  ships by default.
- Risk: API team's rate limits are undocumented; we may hit them under load.
- Constraint: only Priya can touch staging/production databases.
- Constraint: security-sensitive changes require Sam's sign-off before staging. The cookie and
  CSRF work is in scope for that gate.
- Dependency (new): the API must set the `relay_session` cookie; that is Diego's team's repo, not
  this one. Cookie auth cannot work end-to-end until they ship it.
- Dependency: Diego's team for any API-side change.

## 15. Technical or Operational State

Verified 2026-07-30 unless marked otherwise.

Repository: relay-web
Branch: feat/auth-rebuild (also present: master; no upstream tracking branch configured)
Commit: a3549a9 "baseline" (2026-07-30). Was 7c21ab4 in v2.0 — that commit is not in this
history.
Open PRs: none known — not verified this session (no remote configured to check).
Uncommitted changes: none; working tree clean.
Build status: Unknown — not verified this session. Dependencies are not installed.
Test status: Unknown — not verified this session. `npm test` fails immediately with "'vitest' is
not recognized"; there is no node_modules directory and no test file in the tree. v2.0's
"passing (signup only)" is not currently reproducible.
Deployment status: not deployed.
Database status: migrations 001 applied to local and staging as of v2.0 — not re-verified this
session, and only Priya can check staging.
Migration status: 001 applied per v2.0; 002 not written. A sessions table change may be needed
once the TTL decision lands.
CI/CD status: GitHub Actions per v2.0 — not verified this session; no workflow file exists in
this checkout.
Backup status: nightly, last verified 2026-07-20 (per v2.0; not re-verified).
Key files: src/auth/session.ts (session module), docs/SPEC.md (API contract),
package.json (react 18.3.1, jose 5.9.6, version 0.3.1).

## 16. Current Project State

Phase: auth rebuild, mid-flight, after a significant design reversal.

Done: signup flow (reported approved 2026-07-22, see the caveat in section 13); design tokens;
the security review that settled session storage; the spec migration to docs/SPEC.md.

Active: the shared session module. `src/auth/session.ts` issues and verifies HS256 JWTs with
`jose` and exports the cookie name and options, but nothing in this repo attaches the cookie to a
response, and there is no CSRF layer.

Not started: CSRF protection, signup email verification, login flow, legacy decommission.

Blockers and gates: CSRF must exist and be signed off by Sam before staging; the API team must set
the cookie for end-to-end auth; TTL awaits Sam.

Readiness for next phase: not ready for staging. Ready for continued local implementation.

## 17. Immediate Next Action

Immediate Next Action: implement CSRF protection for the cookie-based session, and record the
chosen strategy as a decision in this document.
Responsible Role or Agent: Priya (implementation), Sam (sign-off)
Start From: src/auth/session.ts, alongside the existing `COOKIE_NAME` / `COOKIE_OPTS` exports.
Required Inputs: docs/SPEC.md (which routes are state-changing); confirmation from Diego's team
that the API can set a second, JS-readable CSRF cookie if the double-submit option is chosen;
ticket AUTH-201 for the security constraints already agreed.
Expected Deliverable: a CSRF token issued alongside the session cookie and verified on every
state-changing request, plus the strategy written into section 9 of this document and into
docs/SPEC.md.
Acceptance Criteria: a cross-origin state-changing request without a valid CSRF token is rejected;
a same-origin request from the SPA succeeds; Sam signs off in writing before it reaches staging.
Dependencies: Diego's team for the API-side cookie behaviour.
Stop Conditions: stop and ask if the chosen strategy requires an API change Diego's team has not
agreed to, or if implementing it would require the SPA to read the session cookie (it must not —
that would defeat the 2026-07-28 decision).
Do Not Change: src/legacy/. Do not revert to localStorage or a bearer header. Do not weaken the
cookie flags (httpOnly, secure, sameSite=lax) without Sam's sign-off.

Prioritised queue after that:

1. Fail-fast on a missing `SESSION_SECRET` instead of falling back to `"dev-only-secret"`.
2. Close the TTL decision with Sam, then replace the provisional `TTL_SECONDS` and write
   migration 002 if the sessions table needs it.
3. Signup email verification (previous v2.0 next action — start from the signup implementation
   once its status is confirmed per section 13; deliverable: verification email on signup, and a
   new account cannot log in until verified).
4. Login flow, against the cookie contract in docs/SPEC.md.

## 18. New-Session Start Guide

1. Read this document, then docs/SPEC.md, then src/auth/session.ts.
2. Canonical source: this document. For the auth/session contract, docs/SPEC.md wins.
3. Current state: signup reported done (see section 13 caveat); session module partly built on the
   cookie design; CSRF not started; login not started.
4. Start at src/auth/session.ts — see section 17.
5. Final decisions: sections 3 and 9. Note that section 3's localStorage entry is superseded.
6. Do not repeat: the design token consolidation, the legacy cleanup, and above all do not
   re-propose localStorage or a bearer header for the session token — it was formally rejected by
   security review on 2026-07-28 with written sign-off in AUTH-201. Do not re-litigate the
   `jose` vs `jsonwebtoken` choice.
7. Access required: repo write, local database. Staging/production database access is Priya's
   only. `SESSION_SECRET` must be set locally.
8. Requires explicit human approval: anything security-sensitive reaching staging needs Sam's
   sign-off — this explicitly includes the CSRF implementation and any change to the session
   cookie flags. Migrations against staging or production must go through Priya.

## 19. Incorporated Daily Handoffs

| Date | Handoff File | Scope | Incorporated into Master |
|---|---|---|---|
| 2026-07-22 | 2026-07-22_001_signup-handoff.md | signup flow | Yes (v2.0) |
| 2026-07-24 | 2026-07-24_001_tokens-handoff.md | design tokens | Yes (v2.0) — file not present in docs/handoffs/; see section 13 |
| 2026-07-28 | 2026-07-28_001_spec-move-handoff.md | API spec relocation, session storage decision reversal | Yes (v3.0, 2026-07-30) |
