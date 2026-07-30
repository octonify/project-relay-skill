# Master Handoff - relay-web

Project: relay-web
Document Type: Master Handoff
Version: 3.0
Last Updated: 2026-07-30
Current Phase: Auth rebuild
Overall Status: In Progress - blocked on CSRF strategy and session TTL
Canonical File: docs/handoffs/_master-handoff.md
Supersedes: v2.0 (2026-07-24)

---

## 1. Executive Summary

relay-web is the customer-facing React SPA for Relay. The current phase is a rebuild of
authentication, replacing the legacy jQuery admin's ad-hoc cookie handling with a single shared
session module.

Latest progress: signup flow shipped and approved; security review of session storage completed;
the API spec document was relocated to docs/SPEC.md.

Most important change since v2.0: the session storage decision was **reversed**. localStorage +
bearer header was formally rejected by security review on 2026-07-28. Sessions now go in an
httpOnly, secure, sameSite=lax cookie. This invalidates the v2.0 storage decision and adds a CSRF
work item that did not previously exist.

Immediate next action: implement cookie-based session issuing in src/auth/session.ts.

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

- Decision: src/legacy/ is frozen. No refactors, no renames, no "tidying".
  - Rationale: a cleanup in March 2026 broke billing for two days.
  - Date: 2026-03-30
  - Status: Final
  - Approval source: Priya
  - Supersedes: n/a

- Decision: The session JWT is stored in an httpOnly, secure, sameSite=lax cookie. Do not use
  localStorage. Do not send a bearer header from the SPA.
  - Rationale: third-party analytics scripts run on marketing pages; a token in localStorage is
    readable by any injected script, which makes any XSS equivalent to account takeover.
  - Options considered: localStorage bearer token, httpOnly cookie, in-memory only.
  - Rejected: localStorage (XSS exposure), in-memory only (breaks refresh on page reload).
  - Date: 2026-07-28
  - Status: Final
  - Approval source: Sam (security) + Priya (engineering), written sign-off in AUTH-201
  - Supersedes: the 2026-07-20 localStorage + bearer header decision recorded in v2.0
  - Consequence: the API must set the cookie, and CSRF protection is now required.

- Decision: use `jose` for JWT signing rather than jsonwebtoken.
  - Rationale: ESM-native, works in edge runtimes.
  - Date: 2026-07-19
  - Status: Final
  - Approval source: Priya
  - Supersedes: n/a

## 4. Project Structure

Repository: relay-web (this repo). API lives in a separate repo owned by Diego's team.
Workstreams: Auth rebuild (Priya), Design tokens (complete), Legacy decommission (not started).
Environments: local, staging, production.

## 5. Architecture and Workflow

React + Vite SPA. API at api.relay.example. Migrations applied by hand per environment.
Session transport: httpOnly cookie set by the API (see section 3). CSRF protection is required as
a result and is not yet designed.
Approval gate: security-sensitive changes need Sam's sign-off before they reach staging.
Access restriction: only Priya has staging and production database access.

## 6. Sources of Truth

| Source | Location | Purpose | Authority | Status |
|---|---|---|---|---|
| API spec | docs/SPEC.md | Endpoint and auth contract, session cookie contract, error envelope | Diego's team | Current |
| API spec (old) | docs/SPEC-v1.md | - | - | Deleted 2026-07-28, do not cite |
| Design tokens | packages/tokens | Colour/spacing values | Design review | Current |
| This document | docs/handoffs/_master-handoff.md | Project state | Canonical | Current |

Note: every reference to docs/SPEC-v1.md in v2.0 of this document has been repointed to
docs/SPEC.md. The old path 404s in the wiki.

## 7. Workstream Status

### Auth rebuild

Purpose: one shared session module.
Owner: Priya
Current Status: In Progress
Completed: signup flow (approved by Priya 2026-07-22), argon2id password hashing, session storage
security review (2026-07-28)
In Progress: cookie-based session issuing in src/auth/session.ts. The module currently signs and
verifies JWTs via `jose` and exports `COOKIE_NAME` / `COOKIE_OPTS` matching the approved cookie
attributes, but nothing yet attaches the cookie to a response.
Not Started: login flow, CSRF protection, signup email verification
Blocked: CSRF strategy is undecided and gates the cookie work reaching staging.
Open Decisions: session TTL (Sam), CSRF strategy
Dependencies: API team (Diego) must set the session cookie server-side
Next Action: implement cookie-based session issuing in src/auth/session.ts
Relevant Sources: src/auth/session.ts, docs/SPEC.md

### Design tokens

Current Status: Complete (2026-05-12). No further work planned.

### Legacy decommission

Current Status: Not started. src/legacy/ is frozen; removal scheduled Q4 2026.

## 8. Important Project History

- 2026-03-30 - legacy cleanup broke billing; src/legacy/ frozen as a result.
- 2026-05-12 - design tokens consolidated into packages/tokens.
- 2026-07-18 - auth rebuild started.
- 2026-07-19 - `jose` selected for JWT signing.
- 2026-07-20 - localStorage chosen for session storage (later reversed).
- 2026-07-22 - signup flow completed and approved.
- 2026-07-28 - security review rejected localStorage; httpOnly cookie adopted. docs/SPEC-v1.md
  deleted and replaced by docs/SPEC.md.

## 9. Final Decisions

- Decision: use `jose` for JWT signing rather than jsonwebtoken.
  - Date: 2026-07-19
  - Rationale: ESM-native, works in edge runtimes.
  - Impact: dependency added to package.json (jose 5.9.6).
  - Source: Priya
  - Supersedes: n/a

- Decision: session JWT stored in an httpOnly, secure, sameSite=lax cookie; no localStorage, no
  SPA-sent bearer header.
  - Date: 2026-07-28
  - Rationale: XSS via third-party analytics scripts on marketing pages would otherwise equal
    account takeover.
  - Impact: API must set the cookie; CSRF protection becomes mandatory; SPA fetch calls must send
    credentials rather than an Authorization header.
  - Source: Sam (security) + Priya, written sign-off in AUTH-201
  - Supersedes: the 2026-07-20 localStorage decision

- Decision: docs/SPEC.md replaces docs/SPEC-v1.md as the API contract source of truth.
  - Date: 2026-07-28
  - Rationale: Diego's team restructured the spec and dropped the version suffix.
  - Impact: all internal links repointed; old file deleted.
  - Source: Diego's team
  - Supersedes: docs/SPEC-v1.md

## 10. Open Decisions

- Decision Needed: session TTL
  - Why It Matters: determines re-login frequency and the sessions table column defaults.
  - Available Options: 1h / 12h / 30d with sliding renewal
  - Required Evidence: support-ticket volume for re-login complaints
  - Decision Owner: Sam
  - Deadline or Trigger: before staging deploy. Sam is back Monday (2026-08-03).
  - Current placeholder: src/auth/session.ts hard-codes 12h (`TTL_SECONDS = 60 * 60 * 12`) with a
    comment marking it provisional. Do not treat this as the decision.

- Decision Needed: CSRF strategy for the cookie approach
  - Why It Matters: the httpOnly cookie decision removed the implicit CSRF protection that a
    bearer header provided. Without a strategy, the cookie work cannot pass security review.
  - Available Options: double-submit cookie token, synchroniser token from the API, strict
    sameSite only (weakest)
  - Required Evidence: whether Diego's API can issue and validate a CSRF token; whether any flow
    needs sameSite=none
  - Decision Owner: Sam (security) with Diego (API)
  - Deadline or Trigger: before cookie session issuing reaches staging
  - Status: Open. Nothing implemented.

## 11. Changes Since the Previous Baseline

Changes since v2.0 (2026-07-24):

1. Session storage decision reversed. localStorage + bearer header (2026-07-20, v2.0 section 3)
   was formally rejected by security review on 2026-07-28. httpOnly + secure + sameSite=lax cookie
   is now Final with written sign-off from Sam and Priya.
2. New blocking work item: CSRF protection, created directly by the storage reversal. Now tracked
   in section 10.
3. API spec relocated. docs/SPEC-v1.md deleted, docs/SPEC.md is the source of truth. All
   references in this document updated.
4. Session module partially built. src/auth/session.ts now exists with `issueSession`,
   `readSession`, `COOKIE_NAME`, and `COOKIE_OPTS`.
5. Immediate next action changed. v2.0 said "implement signup email verification"; that was not
   done and has been superseded by cookie-based session issuing. Email verification is retained as
   a deferred item (section 14).
6. Commit reference corrected. v2.0 recorded 7c21ab4; the current HEAD is a3549a9.
7. Login flow: still not started. Two consecutive sessions intended to start it and did not.

## 12. Superseded or Replaced Items

| Superseded Item | Replacement | Reason | Date |
|---|---|---|---|
| per-app SCSS variables | packages/tokens | drift across surfaces | 2026-05-12 |
| localStorage session token + bearer header (2026-07-20) | httpOnly secure sameSite=lax cookie | XSS via third-party scripts equals account takeover | 2026-07-28 |
| docs/SPEC-v1.md | docs/SPEC.md | Diego's team restructured the spec, version suffix dropped | 2026-07-28 |
| v2.0 next action "implement signup email verification" | "implement cookie-based session issuing" | storage reversal took priority | 2026-07-28 |
| v2.0 commit reference 7c21ab4 | a3549a9 | stale | 2026-07-30 |

## 13. Contradictions and Resolution

- Contradiction: v2.0 section 3 recorded localStorage session storage as Final; the 2026-07-28
  handoff records httpOnly cookies as Final.
  - Resolution: the cookie decision wins. It is later, it has security sign-off, and it explicitly
    names the localStorage decision as superseded. localStorage is dead and must not be
    re-proposed.

- Contradiction: v2.0 cited docs/SPEC-v1.md as a current source of truth; that file no longer
  exists.
  - Resolution: docs/SPEC.md is the only API spec. SPEC-v1.md references are stale.

- Discrepancy (unresolved, low risk): v2.0 section 19 lists
  2026-07-24_001_tokens-handoff.md as incorporated, but that file is not present in
  docs/handoffs/. Its content is reflected in the design-token decision, so nothing appears lost.
  Flagged in case someone goes looking for it.

- Discrepancy (unresolved, needs confirmation): v2.0 records the signup flow as complete and
  approved and points new sessions at src/auth/signup.ts, but the only file under src/auth/ in the
  working tree is session.ts. Either signup lives elsewhere, was never committed to this branch,
  or the path is wrong. Confirm with Priya before assuming signup code exists.

## 14. Risks, Constraints, and Dependencies

- Risk: no CSRF protection exists while the cookie approach is being implemented. This is now the
  main gate on reaching staging.
- Risk: API team's rate limits are undocumented; we may hit them under load.
- Risk: session TTL is hard-coded to a provisional 12h in src/auth/session.ts. If the decision
  lands differently, the sessions table defaults and the constant both need changing.
- Risk: login flow has slipped twice. It is the largest remaining unstarted piece of the phase.
- Deferred item: signup email verification. Was the v2.0 next action, never started, displaced by
  the storage reversal. Owner Priya. Acceptance criteria previously agreed: a new account cannot
  log in until verified. Needs transactional email credentials.
- Constraint: only Priya can touch staging/production databases.
- Constraint: security-sensitive changes need Sam's sign-off before staging. The cookie and CSRF
  work is squarely in that category.
- Dependency: Diego's team must set the session cookie on the API side; the SPA cannot do it.
- Dependency: Sam's return (Monday 2026-08-03) for the TTL and CSRF decisions.

## 15. Technical or Operational State

Repository: relay-web
Branch: feat/auth-rebuild
Commit: a3549a9 (branch is level with master; no divergent commits)
Open PRs: none
Uncommitted changes: none (working tree clean)
Build status: not verified this session (no dependencies installed in the working tree)
Test status: not verified this session. Last known: passing, signup only.
Deployment status: not deployed
Database status: migrations 001 applied to local and staging (as of 2026-07-24; not re-verified)
Migration status: 001 applied everywhere; 002 not written. 002 will need to cover the session TTL
column defaults once the TTL decision lands.
CI/CD status: GitHub Actions. Last known passing; not re-verified.
Backup status: nightly, verified 2026-07-20
Key dependency versions: react 18.3.1, jose 5.9.6

## 16. Current Project State

Signup shipped and approved (see the section 13 caveat about the missing signup.ts). Session
storage is settled as httpOnly cookies after a security-review reversal. src/auth/session.ts signs
and verifies JWTs and declares the correct cookie attributes, but nothing wires the cookie into a
response yet. Login flow not started. CSRF unimplemented and undesigned. Session TTL still awaiting
Sam. The API spec now lives at docs/SPEC.md.

## 17. Immediate Next Action

Immediate Next Action: implement cookie-based session issuing in src/auth/session.ts, so a signed
session JWT is set as a cookie using the existing `COOKIE_NAME` and `COOKIE_OPTS` rather than
returned as a bare token string.
Responsible Role or Agent: Priya
Start From: src/auth/session.ts
Required Inputs: docs/SPEC.md session cookie contract; confirmation from Diego on which side sets
the cookie
Expected Deliverable: session issued as an httpOnly secure sameSite=lax cookie; no token exposed
to JavaScript
Acceptance Criteria: no session value readable from document.cookie or localStorage; readSession
works from the cookie
Dependencies: Diego's team for the API-side cookie set
Stop Conditions: stop before merging to staging. Sam's sign-off and a CSRF decision are required
first.
Do Not Change: src/legacy/

## 18. New-Session Start Guide

1. Read this document, then docs/SPEC.md. Do not look for docs/SPEC-v1.md; it was deleted.
2. Canonical source: this document.
3. Current state: signup done, session storage decided as httpOnly cookies, cookie issuing
   partially built, login not started, CSRF not designed.
4. Start at src/auth/session.ts.
5. Final decisions: sections 3 and 9. Open decisions: section 10.
6. Do not repeat: the design token consolidation, the legacy cleanup, and above all do not
   re-propose localStorage for session storage. It was formally rejected on 2026-07-28 with
   written security sign-off.
7. Access required: repo write, local database.
8. Requires approval: anything security-sensitive reaching staging needs Sam's sign-off. The
   current cookie work qualifies.

## 19. Incorporated Daily Handoffs

| Date | Handoff File | Scope | Incorporated into Master |
|---|---|---|---|
| 2026-07-22 | 2026-07-22_001_signup-handoff.md | signup flow | Yes |
| 2026-07-24 | 2026-07-24_001_tokens-handoff.md | design tokens | Yes (file not present in docs/handoffs/, see section 13) |
| 2026-07-28 | 2026-07-28_001_spec-move-handoff.md | API spec relocation, session storage decision reversal | Yes (v3.0) |
