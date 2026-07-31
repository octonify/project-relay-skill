# Master Handoff - relay-web

Project: relay-web
Document Type: Master Handoff
Version: 3.0
Last Updated: 2026-07-30
Current Phase: Auth rebuild - cookie-based session module
Overall Status: In Progress - session storage decision reversed; staging blocked on CSRF strategy
Canonical File: docs/handoffs/_master-handoff.md

---

## 1. Executive Summary

relay-web is the customer-facing React SPA for Relay. The current phase is a rebuild of
authentication, replacing the legacy jQuery admin's ad-hoc cookie handling with a single shared
session module.

Latest major progress: on 2026-07-28 a security review with Sam **reversed** the session storage
decision. Session tokens are no longer stored in localStorage and no longer sent as a bearer
header; the session JWT now lives in an httpOnly, secure, sameSite=lax cookie. In the same
session, `docs/SPEC-v1.md` was deleted and replaced by `docs/SPEC.md`, which is now the API
contract source of truth.

Most important blocker: the reversal created a CSRF requirement that has no strategy and no
implementation, and cookie issuing depends on Diego's API team. Staging cannot be reached until
both are settled — plus Sam's sign-off, which the approval gate requires.

Immediate next action: finish cookie-based session handling in `src/auth/session.ts` (see
section 17). The previously advertised next action, "implement signup email verification", is
**superseded** — it predates the storage reversal and pointed at `src/auth/signup.ts`, a file
that is not present in this checkout (section 13).

Confidence note: this update integrates the 2026-07-28 Daily Handoff and directly verified
repository state. There is no session record for 2026-07-29 or 2026-07-30, so any work done on
those days outside the repo is not reflected here.

## 2. Project Purpose and Definition

Problem: authentication logic is duplicated across the SPA and the legacy admin, and neither is
audited.
Objective: one shared, reviewed session module used by all surfaces.
Final output: shipped auth stack + decommission path for src/legacy/.
Stakeholders: Priya (engineering), Sam (product/security), Diego (API team).
Success criteria: single session module, passing tests, security review sign-off. As of
2026-07-28 this also requires CSRF protection, because the cookie transport decision makes it
mandatory.
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

- Decision: src/legacy/ is frozen. No refactors, no renames, no "tidying".
  - Rationale: a cleanup in March 2026 broke billing for two days.
  - Date: 2026-03-30
  - Status: Final
  - Approval source: Priya
  - Supersedes: n/a

- Decision: The session JWT is stored in an httpOnly, secure, sameSite=lax cookie. Do **not**
  use localStorage and do **not** send a bearer header from the SPA.
  - Rationale: third-party analytics scripts run on marketing pages; a token in localStorage is
    readable by any injected script, making XSS equivalent to account takeover.
  - Options considered: localStorage bearer token, httpOnly cookie, in-memory only.
  - Rejected: localStorage (XSS exposure), in-memory only (breaks refresh on reload).
  - Impact: the API must set the cookie; CSRF protection is now required.
  - Date: 2026-07-28
  - Status: Final
  - Approval source: Sam (security) + Priya (engineering); written sign-off in ticket AUTH-201
  - Supersedes: the 2026-07-20 localStorage + bearer-header decision recorded in Master v2.0

- Decision: Session tokens are stored in browser localStorage and attached as a bearer header.
  - Date: 2026-07-20
  - Status: **SUPERSEDED on 2026-07-28** by the httpOnly cookie decision above. Retained here so
    the reversal is visible rather than looking like it never happened. Do not re-propose it
    (section 18, point 6).

## 4. Project Structure

Repository: relay-web (this repo). API lives in a separate repo owned by Diego's team.
Workstreams: Auth rebuild (Priya), Design tokens (complete), Legacy decommission (not started).
Environments: local, staging, production.

## 5. Architecture and Workflow

React + Vite SPA. API at api.relay.example. Migrations applied by hand per environment.

Session transport (as of 2026-07-28): the session JWT is carried in the `relay_session` cookie
with `httpOnly`, `secure`, `sameSite=lax`, `path=/`. Constants are exported from
`src/auth/session.ts` as `COOKIE_NAME` and `COOKIE_OPTS`. The cookie is to be set by the API,
which means CSRF protection is required and does not yet exist in any form.

Signing: `jose` (HS256), keyed from `process.env.SESSION_SECRET` with a `"dev-only-secret"`
fallback in `src/auth/session.ts`. The fallback is acceptable locally and must never reach
staging or production.

Approval gate: security-sensitive changes need Sam's sign-off before they reach staging. The
cookie/CSRF work is security-sensitive by definition, so this gate is on the critical path.
Access restriction: only Priya has staging and production database access.

## 6. Sources of Truth

| Source | Location | Purpose | Authority | Status |
|---|---|---|---|---|
| API spec | docs/SPEC.md | Endpoint and auth contract, session cookie contract, error envelope | Diego's team | Current (verified present 2026-07-30) |
| API spec (old) | docs/SPEC-v1.md | Former API contract | Diego's team | **Superseded / deleted 2026-07-28** - path 404s in the wiki; do not cite |
| Security sign-off | ticket AUTH-201 | Written rejection of localStorage; approval of cookie approach | Sam | Current. Gap: the tracker URL was never recorded - resolve on first contact with Sam |
| Design tokens | packages/tokens | Colour/spacing values | Design review | Current (not re-verified this session; directory is not present in this checkout) |
| This document | docs/handoffs/_master-handoff.md | Project state | Canonical | Current |

Precedence: `docs/SPEC.md` wins over this document for endpoint and auth-contract detail. This
document wins for project state, status, and decision history. AUTH-201 wins over both for what
security actually approved.

## 7. Workstream Status

### Auth rebuild

Purpose: one shared session module.
Owner: Priya
Current Status: In Progress
Completed:
- Signup endpoint and form, argon2id password hashing - approved by Priya in review 2026-07-22.
  (Caveat: no signup source file is present in this checkout - see section 13.)
- Security review of session storage with Sam, 2026-07-28. Result: localStorage rejected,
  httpOnly cookie adopted. Evidence: written sign-off in AUTH-201.
- API spec migration: docs/SPEC-v1.md deleted, docs/SPEC.md adopted, internal links updated.
In Progress:
- Cookie-based session handling in `src/auth/session.ts`. Partially done: `issueSession` /
  `readSession` (jose, HS256) and the `COOKIE_NAME` / `COOKIE_OPTS` constants exist. Not done:
  anything that actually sets or reads the cookie, and removal of any remaining bearer-header
  or localStorage path.
Blocked:
- Staging deploy. Blocked by three things: no CSRF strategy, API-side cookie support owed by
  Diego's team, and Sam's approval gate for security-sensitive changes.
Open Decisions: session TTL; CSRF strategy; which side issues the cookie (section 10).
Dependencies: Diego's API team must set the session cookie and agree the CSRF scheme.
Next Action: see section 17.
Relevant Sources: src/auth/session.ts, docs/SPEC.md, AUTH-201.

### Design tokens

Purpose: single source of colour and spacing values.
Owner: Priya + design review
Current Status: Complete (closed 2026-05-12; confirmed closed in Master v2.0)
Next Action: none. Do not re-open - see section 18, point 6.
Relevant Sources: packages/tokens.

### Legacy decommission

Purpose: remove src/legacy/admin.js.
Owner: unassigned
Current Status: Not Started - scheduled for Q4 2026.
Blocked: depends on the auth rebuild shipping first.
Next Action: none before the auth stack ships. src/legacy/ is frozen meanwhile.

## 8. Important Project History

- 2026-03-30 - legacy cleanup broke billing; src/legacy/ frozen as a result.
- 2026-05-12 - design tokens consolidated into packages/tokens.
- 2026-07-18 - auth rebuild started.
- 2026-07-20 - localStorage + bearer header chosen for session storage (later reversed).
- 2026-07-22 - signup flow completed and approved by Priya.
- 2026-07-28 - security review with Sam **reversed** the storage decision: localStorage rejected
  as XSS-equivalent-to-account-takeover, httpOnly cookie adopted. This is the single most
  consequential change since v2.0 - it added a CSRF requirement and a new API-team dependency,
  and it means any code or doc written before this date that assumes a bearer token is wrong.
- 2026-07-28 - docs/SPEC-v1.md deleted; docs/SPEC.md became the API contract source of truth.

## 9. Final Decisions

- Decision: use `jose` for JWT signing rather than jsonwebtoken.
- Date: 2026-07-19
- Rationale: ESM-native, works in edge runtimes.
- Impact: dependency added to package.json (verified: `jose` 5.9.6).
- Source: Priya
- Supersedes: n/a

- Decision: store the session JWT in an httpOnly, secure, sameSite=lax cookie; no localStorage,
  no bearer header from the SPA.
- Date: 2026-07-28
- Rationale: third-party analytics on marketing pages makes a localStorage token readable by any
  injected script; XSS would equal account takeover.
- Impact: API must set the cookie; CSRF protection required; bearer-header integration work from
  before 2026-07-28 is void.
- Source: Sam (security) + Priya (engineering), written sign-off in AUTH-201.
- Supersedes: the 2026-07-20 localStorage decision (Master v2.0, section 3).

## 10. Open Decisions

- Decision Needed: session TTL
- Why It Matters: determines re-login frequency and the sessions table column defaults.
- Available Options: 1h / 12h / 30d with sliding renewal
- Required Evidence: support-ticket volume for re-login complaints
- Decision Owner: Sam
- Deadline or Trigger: before staging deploy
- Status as of 2026-07-30: still open. The 2026-07-28 handoff recorded "waiting for approval,
  Sam back Monday"; whether Sam has since responded was not verified. Note that
  `src/auth/session.ts` already hardcodes `TTL_SECONDS = 60 * 60 * 12` (12h) with a comment
  marking it provisional - the code has quietly pre-committed to one option.

- Decision Needed: CSRF strategy for the cookie session
- Why It Matters: created directly by the 2026-07-28 cookie decision. sameSite=lax alone does
  not cover top-level POST navigations, and this is a security-gated release.
- Available Options: double-submit cookie token; synchronizer token issued by the API;
  sameSite=strict plus strict Origin/Referer checks.
- Required Evidence: Diego's team's position on what the API can enforce, and Sam's acceptance
  of the chosen scheme.
- Decision Owner: Sam (security) with Diego (API)
- Deadline or Trigger: before staging deploy. Nothing is implemented today.

- Decision Needed: which side issues the session cookie
- Why It Matters: the 2026-07-28 decision says "the API must set the cookie", yet
  `src/auth/session.ts` in this repo contains the JWT signing code (`issueSession`). Both cannot
  be the issuer. Until this is settled, the scope of the next action is ambiguous and signing
  code may be in the wrong repository.
- Available Options: API signs and sets the cookie and relay-web only reads it; relay-web signs
  and the API sets; keep signing in relay-web for a server-side route.
- Required Evidence: Diego's confirmation of what the API endpoint returns, checked against
  docs/SPEC.md's session cookie contract.
- Decision Owner: Priya with Diego
- Deadline or Trigger: before the cookie wiring in section 17 is finished.

## 11. Changes Since the Previous Baseline

Diff from Master v2.0 (2026-07-24) to v3.0 (2026-07-30):

- **Reversed decision:** localStorage + bearer header → httpOnly/secure/sameSite=lax cookie
  (2026-07-28, Sam + Priya, AUTH-201). Recorded in sections 3, 5, 9, 12; the old decision is
  retained and marked superseded rather than deleted.
- **New requirement:** CSRF protection, and a new open decision for its strategy (section 10).
- **New dependency:** Diego's API team must set the session cookie - now on the critical path.
- **Source of truth replaced:** docs/SPEC-v1.md deleted → docs/SPEC.md (sections 6, 12).
- **Statuses corrected:** commit 7c21ab4 → a3549a9; "no blockers" → staging blocked; test status
  "passing (signup only)" → unverified, no test files present; build status → unverified.
- **Next action replaced:** "implement signup email verification" → finish cookie-based session
  handling in src/auth/session.ts. The old action also pointed at a file that is not present.
- **Contradictions recorded** (section 13): a missing Daily Handoff that v2.0 claims was
  incorporated; a missing signup source file; a commit hash not in this clone's history; a test
  claim with no tests.
- **Workstream Status expanded** from one workstream to all three named in section 4.
- **Gap:** no session record exists for 2026-07-29 or 2026-07-30. Work done on those days that
  did not land in the repo is not captured in this version.
- **Incorporated:** 2026-07-28_001_spec-move-handoff.md (was outstanding at v2.0).

## 12. Superseded or Replaced Items

| Superseded Item | Replacement | Reason | Date |
|---|---|---|---|
| per-app SCSS variables | packages/tokens | drift across surfaces | 2026-05-12 |
| localStorage session storage + bearer header (2026-07-20 decision) | httpOnly, secure, sameSite=lax cookie | localStorage token readable by injected third-party scripts; XSS equals account takeover | 2026-07-28 |
| docs/SPEC-v1.md | docs/SPEC.md | Diego's team restructured the spec; version suffix dropped. Old path 404s in the wiki | 2026-07-28 |
| Next action "implement signup email verification" (Master v2.0 s17) | Finish cookie-based session handling in src/auth/session.ts | predates the storage reversal; also pointed at src/auth/signup.ts, which is absent | 2026-07-30 |

## 13. Contradictions and Resolution

1. **Storage decision recorded twice, in opposite directions.** Master v2.0 section 3 recorded
   localStorage as Final; the 2026-07-28 Daily Handoff records httpOnly cookies as Final.
   - Verified current state: httpOnly cookie.
   - Authoritative source: AUTH-201 (Sam's written security sign-off), corroborated by
     `COOKIE_NAME` / `COOKIE_OPTS` in src/auth/session.ts.
   - Why it wins: later date, security authority, written approval, and code already reflects it.
   - Resolution: applied throughout this document; old decision marked superseded, not deleted.

2. **A Daily Handoff claimed as incorporated does not exist.** Master v2.0 section 19 lists
   `2026-07-24_001_tokens-handoff.md` as incorporated, but that file is not in
   `docs/handoffs/` and not in `git ls-files`.
   - Verified current state: only two Daily files exist - 2026-07-22_001 and 2026-07-28_001.
   - Resolution: **unresolved.** Its content is presumed to be the design-token closure already
     captured in sections 3 and 8, so nothing is believed lost.
   - Evidence that would settle it: git history for that path (unavailable - this clone has a
     single squashed `baseline` commit) or Priya's local copy.

3. **Signup work is claimed complete, but no signup source file is present.** v2.0 and the
   2026-07-22 Daily both report the signup endpoint, form, and argon2id hashing as complete and
   approved; v2.0's next action said to start from `src/auth/signup.ts`. The only source file
   tracked at HEAD a3549a9 is `src/auth/session.ts`.
   - Verified current state: `git ls-files` returns docs/SPEC.md, three handoff files,
     package.json, src/auth/session.ts. No signup file, no argon2 dependency in package.json.
   - Resolution: **unresolved.** Do not assume signup exists in code. Treat "signup complete" as
     an unverified inherited claim until the file is located.
   - Evidence that would settle it: the signup PR, or Priya's working tree.

4. **Recorded commit is not in this clone.** v2.0 section 15 records commit `7c21ab4`. Actual
   HEAD is `a3549a9 "baseline"`, and it is the only commit in the repository.
   - Resolution: section 15 corrected to a3549a9. The v2.0 hash cannot be resolved here; the
     history appears to have been squashed or re-created.

5. **Test status claimed passing with no tests present.** v2.0 recorded "passing (signup only)".
   `package.json` defines `"test": "vitest run"`, but vitest is not in `dependencies` and no test
   file exists in the repo.
   - Resolution: section 15 now records test status as unverified/not runnable as checked out.
     Do not treat "tests pass" as true.

## 14. Risks, Constraints, and Dependencies

- Risk: **no CSRF protection exists** while the session moves to a cookie. Until a scheme is
  chosen and implemented, cookie-based auth must not reach staging. Mitigation: section 10's CSRF
  decision is a release blocker, not a nice-to-have.
- Risk: `SESSION_SECRET` falls back to the literal `"dev-only-secret"` in src/auth/session.ts.
  If that fallback ships, every session token is forgeable. Mitigation: fail fast on a missing
  env var before any deploy.
- Risk: API team's rate limits are undocumented; we may hit them under load.
- Risk: repository history is a single `baseline` commit, so pre-2026-07-30 work cannot be
  recovered or audited from git. Written handoffs and AUTH-201 are the only record.
- Risk: inherited claims (signup complete, migrations applied, backups verified, tokens package)
  could not be verified in this checkout. Re-verify before depending on any of them.
- Constraint: only Priya can touch staging/production databases.
- Constraint: security-sensitive changes require Sam's sign-off before staging.
- Dependency: Diego's team for any API-side change - now including setting the session cookie
  and agreeing the CSRF scheme.
- Dependency: Sam for the TTL decision and CSRF acceptance.

## 15. Technical or Operational State

Verified directly on 2026-07-30 unless marked otherwise.

Repository: relay-web
Branch: feat/auth-rebuild
Commit: a3549a9 ("baseline") - the only commit in this clone
Remote state: **Unknown** - no upstream tracking branch is configured, so nothing was pushed or
compared this session
Open PRs: Unknown - not checked this session
Uncommitted changes: none (0 files)
Tracked files: docs/SPEC.md, docs/handoffs/ (3 files), package.json, src/auth/session.ts
Build status: **Unknown** - dependencies are not installed in this checkout; `npm run build` was
not run
Test status: **Unknown / not runnable** - no test files exist and vitest is absent from
package.json dependencies, though `npm test` invokes `vitest run`. Supersedes v2.0's
"passing (signup only)" (section 13, item 5)
Deployment status: not deployed (inherited from v2.0; not re-verified)
Database status: migrations 001 applied to local and staging (inherited from v2.0; **not
verified** - no migrations directory exists in this checkout)
Migration status: 001 applied everywhere, 002 not written (inherited from v2.0; not verified)
CI/CD status: GitHub Actions (inherited from v2.0; **not verified** - no workflow file is
tracked in this checkout)
Backup status: nightly, verified 2026-07-20 (inherited; not re-verified)

## 16. Current Project State

Phase: auth rebuild, mid-flight, immediately after a security-driven direction change.

Latest approved output: the httpOnly cookie session decision (Sam + Priya, 2026-07-28,
AUTH-201). Signup was approved on 2026-07-22 but its code could not be located in this checkout.

Active work: cookie-based session handling in src/auth/session.ts - signing, verification, and
cookie constants are in place; the actual cookie set/read path is not.

Completed: signup flow (approved, code unverified), password hashing, design token
consolidation, session storage security review, API spec migration to docs/SPEC.md.

Incomplete: login flow (not started), CSRF protection (not started), email verification (not
started), migration 002 (not written), tests (none present).

Blockers: no CSRF strategy; API-side cookie support owed by Diego's team; Sam's approval gate
for anything security-sensitive reaching staging.

Open decisions: session TTL, CSRF strategy, which side issues the cookie.

Readiness for next phase: **not ready for staging.** Ready for local implementation work on
section 17 only.

Overall status: In Progress, direction stable but dependency-bound.

## 17. Immediate Next Action

Immediate Next Action: finish cookie-based session handling in `src/auth/session.ts` - make the
session token travel only via the `relay_session` cookie, and remove every remaining
localStorage or bearer-header path in the SPA.
Responsible Role or Agent: Priya (or an agent working under her review)
Start From: `src/auth/session.ts` - `COOKIE_NAME` and `COOKIE_OPTS` are already exported at the
bottom of the file; wire them into the request/response path and read the session from the
cookie instead of a header.
Required Inputs: `docs/SPEC.md` (session cookie contract), AUTH-201 (approved scheme), Diego's
confirmation of which side sets the cookie (section 10, third open decision).
Expected Deliverable: session issued and read via the httpOnly cookie, with no token ever
written to localStorage and no `Authorization: Bearer` header sent from the SPA.
Acceptance Criteria:
- Grep the repo for `localStorage` and `Bearer` and find zero session-related hits.
- Cookie attributes match exactly: httpOnly, secure, sameSite=lax, path=/.
- `readSession` resolves a session from the cookie, and returns null rather than throwing on a
  bad or absent token (current behaviour - preserve it).
- The 12h `TTL_SECONDS` value stays flagged as provisional until Sam decides (section 10).
Dependencies: Diego's team for the API-side cookie; no code in this repo should assume the API
already sets it.
Stop Conditions:
- Stop and escalate to Priya + Diego if it turns out the API is the issuer - do not delete
  `issueSession` on your own initiative; that is an open decision, not a cleanup.
- Do not deploy to staging. Cookie auth without CSRF protection must not reach staging, and the
  approval gate requires Sam's sign-off regardless.
Do Not Change: `src/legacy/` (frozen); the cookie attributes approved in AUTH-201; the choice of
`jose`.

Prioritized queue after that:
1. Settle the CSRF strategy with Sam and Diego, then implement it (blocks staging).
2. Get the session TTL decision from Sam and replace the provisional 12h constant.
3. Locate the signup implementation and resolve contradiction 3 in section 13; only then pick up
   signup email verification, which was the pre-reversal next action.
4. Add a test for session issue/read - there are currently no tests, and vitest is not installed.
5. Make `SESSION_SECRET` mandatory (drop the `"dev-only-secret"` fallback) before any deploy.
6. Then the login flow.

## 18. New-Session Start Guide

1. Read this document, then `docs/SPEC.md`. Do **not** look for `docs/SPEC-v1.md` - it was
   deleted on 2026-07-28 and its wiki path 404s.
2. Canonical source: this document for project state; docs/SPEC.md for the API contract;
   AUTH-201 for what security approved.
3. Current state: session storage reversed to httpOnly cookies on 2026-07-28. Signup approved
   but its code is not present in this checkout. Login not started. No CSRF protection exists.
   Nothing is deployed.
4. Start at `src/auth/session.ts` and follow section 17 exactly.
5. Final decisions: sections 3 and 9. The cookie decision is final and security-signed.
6. Do not repeat: the design token consolidation; the legacy cleanup; **do not re-propose
   localStorage for session storage** - it was formally rejected by security review on
   2026-07-28 with written sign-off in AUTH-201; do not re-litigate `jose` vs `jsonwebtoken`.
7. Access required: repo write, local database. Staging and production database access is
   Priya's only.
8. Requires explicit human approval: anything security-sensitive reaching staging needs Sam's
   sign-off - the entire cookie/CSRF workstream falls under this. Any change to the approved
   cookie attributes needs Sam. Any staging or production database or migration action needs
   Priya, who alone has access.

## 19. Incorporated Daily Handoffs

| Date | Handoff File | Scope | Incorporated into Master |
|---|---|---|---|
| 2026-07-22 | 2026-07-22_001_signup-handoff.md | signup flow | Yes (v2.0) |
| 2026-07-24 | 2026-07-24_001_tokens-handoff.md | design tokens | Claimed Yes in v2.0, but **the file does not exist** in docs/handoffs/ or in git - see section 13, item 2 |
| 2026-07-28 | 2026-07-28_001_spec-move-handoff.md | API spec relocation, session storage decision reversal | Yes (v3.0) |

No Daily Handoff exists for 2026-07-29 or 2026-07-30. If work happened on those days, it is not
represented in v3.0 beyond what is visible in the repository at commit a3549a9.
