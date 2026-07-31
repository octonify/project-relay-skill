# Master Handoff - relay-web

Project: relay-web
Document Type: Master Handoff
Version: 3.0
Last Updated: 2026-07-30
Current Phase: Auth rebuild
Overall Status: In Progress - blocked on CSRF strategy
Canonical File: docs/handoffs/_master-handoff.md

---

## 1. Executive Summary

relay-web is the customer-facing React SPA for Relay. The current phase is a rebuild of
authentication, replacing the legacy jQuery admin's ad-hoc cookie handling with a single shared
session module.

Since v2.0 the storage decision was reversed: on 2026-07-28 security review rejected localStorage
bearer tokens and locked in an httpOnly, secure, sameSite=lax session cookie. The API contract
document moved from `docs/SPEC-v1.md` (deleted) to `docs/SPEC.md`. A session module now exists at
`src/auth/session.ts` with `jose`-based JWT issue/verify plus cookie name and option constants —
but nothing yet sets that cookie on a response, and no CSRF protection exists anywhere in the repo.

Most important blocker: the cookie approach requires CSRF protection and no strategy has been
chosen. Session TTL is also still undecided (hard-coded to a provisional 12h). Immediate next
action: finish cookie issuance in `src/auth/session.ts` (section 17).

Note for returning readers: several v2.0 claims did not survive verification against the repo.
See sections 13 and 15 — treat the previous "build/test passing" and commit `7c21ab4` lines as
withdrawn.

## 2. Project Purpose and Definition

Problem: authentication logic is duplicated across the SPA and the legacy admin, and neither is
audited.
Objective: one shared, reviewed session module used by all surfaces.
Final output: shipped auth stack + decommission path for `src/legacy/`.
Stakeholders: Priya (engineering), Sam (product/security), Diego (API team).
Success criteria: single session module, passing tests, security review sign-off.
Scope: relay-web SPA and its API contract.
Out of scope: rewriting `src/legacy/admin.js`. It is frozen and scheduled for removal in Q4 2026.

## 3. Locked Principles and Decisions

- Decision: Design tokens live in `packages/tokens` and are the only source of colour and spacing
  values. No hard-coded hex in components.
  - Rationale: three surfaces drifted apart in 2025; a single token package stopped it.
  - Date: 2026-05-12
  - Status: Final. **Unverified inherited claim** — `packages/tokens` is not present in this
    working tree at commit `a3549a9`; the decision itself is not in doubt, its location is.
  - Approval source: Priya + design review
  - Supersedes: per-app SCSS variables

- Decision: `src/legacy/` is frozen. No refactors, no renames, no "tidying".
  - Rationale: a cleanup in March 2026 broke billing for two days.
  - Date: 2026-03-30
  - Status: Final. The directory is not present in this working tree at `a3549a9`; the freeze
    still governs wherever that code lives.
  - Approval source: Priya

- Decision: The session JWT is stored in an httpOnly, secure, sameSite=lax cookie. Do **not** use
  localStorage, and do **not** send a bearer header from the SPA.
  - Rationale: third-party analytics scripts run on marketing pages, so a token readable from
    localStorage makes any XSS equivalent to account takeover.
  - Date: 2026-07-28
  - Status: Final
  - Approval source: Sam (security, written sign-off in AUTH-201) + Priya (engineering)
  - Supersedes: the 2026-07-20 localStorage/bearer-header decision recorded in Master v2.0
  - Consequence: the API must set the cookie, and CSRF protection is now mandatory (section 10).

## 4. Project Structure

Repository: relay-web (this repo). API lives in a separate repo owned by Diego's team.
Workstreams: Auth rebuild (Priya, active), Design tokens (Complete), Legacy decommission (Not
Started).
Environments: local, staging, production.

## 5. Architecture and Workflow

React + Vite SPA. API at api.relay.example. Migrations applied by hand per environment.
Session transport: httpOnly cookie set by the API; the SPA never reads the token.
Approval gate: security-sensitive changes need Sam's sign-off before they reach staging.
Access restriction: only Priya has staging and production database access.

## 6. Sources of Truth

| Source | Location | Purpose | Authority | Status |
|---|---|---|---|---|
| API spec | `docs/SPEC.md` | Endpoint, session cookie contract, error envelope | Diego's team | Current (verified present at `a3549a9`) |
| Design tokens | `packages/tokens` | Colour/spacing values | Design review | Unverified — path not present in this repo |
| This document | `docs/handoffs/_master-handoff.md` | Project state | Canonical | Current |

Precedence: `docs/SPEC.md` wins over this document for anything about the API contract.
`docs/SPEC-v1.md` is deleted — any link to it is dead (section 12).

## 7. Workstream Status

### Auth rebuild

Purpose: one shared session module.
Owner: Priya
Current Status: In Progress
Completed: signup flow with argon2id password hashing, approved by Priya 2026-07-22 (inherited
claim — no `src/auth/signup.ts` exists in this working tree at `a3549a9`, so the code's location
is unverified); security review of session storage, closed 2026-07-28; API spec migration to
`docs/SPEC.md`.
In Progress: cookie-based session module, `src/auth/session.ts` — JWT sign/verify via `jose` and
`COOKIE_NAME` / `COOKIE_OPTS` constants exist; no code sets the cookie on a response.
Blocked: CSRF protection — required by the cookie decision, no strategy chosen.
Open Decisions: session TTL; CSRF strategy (section 10).
Dependencies: API team (Diego) must set the session cookie server-side.
Next Action: see section 17.
Relevant Sources: `src/auth/session.ts`, `docs/SPEC.md`

### Design tokens

Current Status: Complete (closed 2026-05-12). No further work planned.

### Legacy decommission

Current Status: Not Started. Scheduled Q4 2026. `src/legacy/` frozen until then.

## 8. Important Project History

- 2026-03-30 - legacy cleanup broke billing; `src/legacy/` frozen as a result.
- 2026-05-12 - design tokens consolidated into `packages/tokens`.
- 2026-07-18 - auth rebuild started.
- 2026-07-28 - security review rejected localStorage session storage; httpOnly cookie adopted.
  This reversed a decision that was Final in Master v2.0 and invalidated the planned SPA bearer
  header work.
- 2026-07-28 - `docs/SPEC-v1.md` deleted; `docs/SPEC.md` is the API contract.

## 9. Final Decisions

- Decision: use `jose` for JWT signing rather than `jsonwebtoken`.
- Date: 2026-07-19
- Rationale: ESM-native, works in edge runtimes.
- Impact: `jose@5.9.6` in `package.json`; in use at `src/auth/session.ts`.
- Source: Priya
- Status: Verified in repo at `a3549a9`.

(The session-storage decision is locked and lives in section 3.)

## 10. Open Decisions

- Decision Needed: session TTL
- Why It Matters: determines re-login frequency and the sessions table column defaults. Currently
  hard-coded to 12h at `src/auth/session.ts` line 6, marked provisional in a code comment — that
  constant is what must change once decided.
- Available Options: 1h / 12h / 30d with sliding renewal
- Required Evidence: support-ticket volume for re-login complaints
- Decision Owner: Sam
- Deadline or Trigger: before staging deploy. As of 2026-07-28 Sam was away, expected back Monday.

- Decision Needed: CSRF protection strategy for the cookie approach
- Why It Matters: sameSite=lax alone does not cover all state-changing requests; this is the
  blocker on finishing the auth rebuild and it spans both repos.
- Available Options: not yet enumerated (double-submit token, synchroniser token, origin checks)
- Required Evidence: what the API can support — needs Diego's team
- Decision Owner: Sam (security sign-off) with Diego (API feasibility)
- Deadline or Trigger: before any cookie-authenticated write endpoint ships

## 11. Changes Since the Previous Baseline (v2.0, 2026-07-24)

- Session storage reversed from localStorage/bearer to httpOnly cookie; v2.0's section 3 entry is
  superseded, not merely edited.
- `docs/SPEC-v1.md` deleted, replaced by `docs/SPEC.md`; Sources of Truth updated.
- New blocker: CSRF strategy (was not a concern under the bearer-header approach).
- New open decision recorded: CSRF strategy. Session TTL remains open, now with the code location
  that encodes it.
- Immediate Next Action replaced: "implement signup email verification" is superseded — it pointed
  at `src/auth/signup.ts`, which does not exist in this working tree.
- Technical state corrected against the repo: commit is `a3549a9`, not `7c21ab4`; build, test and
  CI statuses are withdrawn as unverifiable (section 15).
- Contradictions section populated (was "None recorded").
- Daily 2026-07-28_001 incorporated.

## 12. Superseded or Replaced Items

| Superseded Item | Replacement | Reason | Date |
|---|---|---|---|
| per-app SCSS variables | `packages/tokens` | drift across surfaces | 2026-05-12 |
| localStorage + bearer header session storage (Master v2.0 §3) | httpOnly sameSite=lax cookie | XSS makes a readable token equivalent to account takeover; rejected in security review | 2026-07-28 |
| `docs/SPEC-v1.md` (deleted) | `docs/SPEC.md` | Diego's team restructured the spec and dropped the version suffix | 2026-07-28 |
| Next action "implement signup email verification" | Cookie issuance in `src/auth/session.ts` (section 17) | storage reversal changed the critical path | 2026-07-28 |

## 13. Contradictions and Resolution

- **Commit identity.** Master v2.0 recorded commit `7c21ab4`. `git log` on branch
  `feat/auth-rebuild` contains exactly one commit, `a3549a9 "baseline"`. Resolution: the repo
  wins; `a3549a9` is current. `7c21ab4` is not reachable in this repository. Likely this working
  copy was reconstructed from a squashed or re-created history — unconfirmed.
- **Missing Daily.** Master v2.0's incorporated-handoffs table lists
  `2026-07-24_001_tokens-handoff.md`. No such file exists in `docs/handoffs/`. Its content is
  presumed already folded into the Master (design tokens are recorded as complete); the file
  itself is gone. What would settle it: the file in someone's local copy or in a prior commit —
  neither exists in this repo's single-commit history.
- **Paths referenced but absent.** `packages/tokens`, `src/legacy/`, and `src/auth/signup.ts` are
  all referenced by inherited claims but are not present at `a3549a9`. The only source file in
  the tree is `src/auth/session.ts`. Not treated as "work undone" — more likely this checkout is
  partial — but no one should assume they can open those paths here. Settling evidence: a full
  clone of relay-web.

## 14. Risks, Constraints, and Dependencies

- Risk (new, active): the cookie decision creates a CSRF exposure that nothing currently mitigates.
  Mitigation: no cookie-authenticated write endpoint ships until section 10's CSRF decision closes.
- Risk (new, active): `src/auth/session.ts` line 3 falls back to the literal `"dev-only-secret"`
  when `SESSION_SECRET` is unset. If that reaches staging or production, every session token is
  forgeable. Mitigation: make the fallback fail loudly outside local, and confirm `SESSION_SECRET`
  is set per environment before any deploy.
- Risk (inherited, active): API team's rate limits are undocumented; we may hit them under load.
- Constraint: only Priya can touch staging/production databases.
- Constraint: no dependencies are installed in this checkout, so nothing here can currently be
  built or tested (section 15).
- Dependency: Diego's team must set the session cookie API-side; the SPA cannot do it.
- Dependency: Sam's sign-off gates anything security-sensitive reaching staging.

## 15. Technical or Operational State

Verified 2026-07-30 against the working tree unless marked otherwise.

Repository: relay-web
Branch: `feat/auth-rebuild` (also present locally: `master`)
Commit: `a3549a9` "baseline" — the only commit in this repo's history
Remote: no upstream tracking branch configured; nothing has been pushed from here
Uncommitted changes: none — clean tree
Open PRs: none known (not checkable from this checkout)
Tracked files: `package.json`, `src/auth/session.ts`, `docs/SPEC.md`, `docs/handoffs/*`
Dependencies: not installed — no `node_modules`
Build status: Unknown. Not run; cannot run without dependencies.
Test status: Unknown. `npm test` fails with `'vitest' is not recognized` and there are no test
files in the tree. v2.0's "passing (signup only)" is withdrawn as unverifiable here.
CI/CD status: Unknown. No `.github/` or other CI configuration in this checkout. v2.0's "GitHub
Actions, passing" is withdrawn as unverifiable here.
Deployment status: not deployed (inherited, unchanged)
Database status: migration 001 applied to local and staging (inherited, not verifiable from this
repo — no migration files present)
Migration status: 002 not written. The cookie switch and any TTL decision may change what 002 must
contain.
Backup status: nightly, last verified 2026-07-20 (inherited, unverified since)

## 16. Current Project State

Signup is done and approved. Session storage is decided and locked as an httpOnly cookie. The
session module exists in skeleton form — it can sign and verify a JWT and declares the cookie name
and options, but no code path actually sets or clears the cookie, and login is still not started.
The auth rebuild cannot complete until CSRF is decided. TTL remains provisional at 12h in code.

## 17. Immediate Next Action

Immediate Next Action: complete cookie-based session issuance in `src/auth/session.ts` — add the
helpers that set and clear the session cookie using the existing `COOKIE_NAME` and `COOKIE_OPTS`,
and cover them with tests.
Responsible Role or Agent: Priya
Start From: `src/auth/session.ts` (`issueSession` / `readSession` already exist)
Required Inputs: `docs/SPEC.md` for the cookie contract; `SESSION_SECRET` set locally; run
`npm install` first — dependencies are not installed in this checkout.
Expected Deliverable: session cookie set on successful auth and cleared on logout, plus tests.
Acceptance Criteria: cookie carries the `jose`-signed JWT with `httpOnly`, `secure`,
`sameSite=lax`, `path=/`; no token is ever exposed to JavaScript; tests pass locally.
Dependencies: Diego's team owns the API-side cookie set; coordinate the contract before shipping.
Stop Conditions: stop and escalate before shipping any cookie-authenticated write endpoint — CSRF
is undecided (section 10). Do not invent a TTL; leave the provisional 12h constant until Sam
decides.
Do Not Change: `src/legacy/`; the `httpOnly` cookie decision.

Queue after that, in order:
1. Close the CSRF strategy decision with Sam and Diego, then implement it.
2. Close the session TTL decision with Sam and update `src/auth/session.ts` line 6.
3. Start the login flow.
4. Write migration 002 once TTL is known.

## 18. New-Session Start Guide

1. Read this document, then `docs/SPEC.md`. Do not look for `docs/SPEC-v1.md` — it was deleted.
2. Canonical source: this document. `docs/SPEC.md` outranks it on API contract details.
3. Current state: signup done; session module partially built; login not started; blocked on CSRF.
4. Start at `src/auth/session.ts` (section 17). Run `npm install` before anything else.
5. Final decisions: sections 3 and 9. Open ones: section 10.
6. Do not repeat: the design token consolidation; the legacy cleanup; **do not re-propose
   localStorage for session storage** — formally rejected by security review 2026-07-28 with
   written sign-off in AUTH-201.
7. Access required: repo write, local database. Staging/production database access is Priya's only.
8. Requires explicit human approval: anything security-sensitive reaching staging (Sam); the CSRF
   strategy (Sam + Diego); the session TTL (Sam).

## 19. Incorporated Daily Handoffs

| Date | Handoff File | Scope | Incorporated into Master |
|---|---|---|---|
| 2026-07-22 | `2026-07-22_001_signup-handoff.md` | signup flow | Yes (v2.0) |
| 2026-07-24 | `2026-07-24_001_tokens-handoff.md` | design tokens | Yes (v2.0) — file no longer present, see section 13 |
| 2026-07-28 | `2026-07-28_001_spec-move-handoff.md` | API spec relocation, session storage reversal | Yes (v3.0) |
