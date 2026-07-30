#!/usr/bin/env python3
"""Build eval fixture projects for the project-relay skill.

Each fixture is a self-contained project directory that a test subagent is pointed at.
Fixtures are rebuilt from scratch each time so with_skill and baseline runs get byte-identical
starting state.

Usage: python build_fixtures.py <fixtures-root>
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

FILES: dict[str, dict[str, str]] = {}

# ---------------------------------------------------------------- fixture A: relay-web session
FILES["a-webapp-session"] = {
"package.json": """{
  "name": "relay-web",
  "version": "0.3.1",
  "scripts": {
    "dev": "vite",
    "test": "vitest run",
    "build": "vite build"
  },
  "dependencies": {
    "react": "18.3.1",
    "jose": "5.9.6"
  }
}
""",
"docs/ARCHITECTURE.md": """# relay-web architecture

Frontend: React + Vite. API: separate service at api.relay.example (not in this repo).
Auth: see src/auth/. Session storage approach is under active decision.

`src/legacy/` contains the pre-2025 jQuery admin. Frozen.
""",
"src/auth/session.ts": """import { jwtVerify, SignJWT } from "jose";

const SECRET = new TextEncoder().encode(process.env.SESSION_SECRET ?? "dev-only-secret");

// TTL is provisional - waiting on product decision.
const TTL_SECONDS = 60 * 60 * 12;

export async function issueSession(userId: string): Promise<string> {
  return new SignJWT({ sub: userId })
    .setProtectedHeader({ alg: "HS256" })
    .setIssuedAt()
    .setExpirationTime(`${TTL_SECONDS}s`)
    .sign(SECRET);
}

export async function readSession(token: string): Promise<{ sub: string } | null> {
  try {
    const { payload } = await jwtVerify(token, SECRET);
    return { sub: String(payload.sub) };
  } catch {
    return null;
  }
}

export const COOKIE_NAME = "relay_session";
export const COOKIE_OPTS = { httpOnly: true, sameSite: "lax", secure: true, path: "/" };
""",
"src/auth/login-form.tsx": """import { useState } from "react";

export function LoginForm({ onSubmit }: { onSubmit: (e: string, p: string) => void }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);

  return (
    <form
      onSubmit={(ev) => {
        ev.preventDefault();
        if (!email.includes("@")) return setError("Enter a valid email");
        setError(null);
        onSubmit(email, password);
      }}
    >
      <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
      />
      {error && <p role="alert">{error}</p>}
      <button type="submit">Sign in</button>
    </form>
  );
}
""",
"src/legacy/admin.js": """// Frozen pre-2025 admin. Do not modify.
window.RelayAdmin = { init: function () { /* ... */ } };
""",
"migrations/002_add_sessions.sql": """CREATE TABLE sessions (
  id uuid PRIMARY KEY,
  user_id uuid NOT NULL REFERENCES users(id),
  issued_at timestamptz NOT NULL DEFAULT now(),
  expires_at timestamptz NOT NULL
);
CREATE INDEX sessions_user_id_idx ON sessions (user_id);
""",
"SESSION-TRANSCRIPT.md": """# Working session transcript - 30 July 2026

Participants: Priya (engineer), Claude.
Workstream: Auth rebuild (relay-web).
Objective at start of session: "get login working end to end, including refresh tokens".

---

**Priya:** Right, today I want login working end to end. Signup already exists. Start with how we
store the session.

**Claude:** Two realistic options: JWT in localStorage, or JWT in an httpOnly cookie. localStorage
is easier to wire from the SPA but readable by any injected script, so an XSS anywhere in the app
becomes full account takeover. httpOnly cookie needs the API to set the header and needs CSRF
handling, but the token is unreachable from JS.

**Priya:** Cookie. We've got third-party analytics scripts on the marketing pages, I'm not putting
a bearer token where they can reach it. Lock that in.

**Claude:** Locking it in. I'll add COOKIE_NAME / COOKIE_OPTS to src/auth/session.ts with
httpOnly, sameSite=lax, secure.

**Priya:** Good.

**Claude:** session.ts now issues and verifies HS256 JWTs via `jose`, and exports the cookie
config. TTL is set to 12 hours as a placeholder.

**Priya:** 12 hours is a guess. Sam owns that call - it's a product/security tradeoff, and he's out
until Monday. Leave the placeholder, flag it.

**Claude:** Flagged. Building the login form next.

**Claude:** src/auth/login-form.tsx is in. Email/password fields, client-side email validation,
error region with role="alert" for screen readers.

**Priya:** Let me look... loaded the dev server, typed a bad email, got the error. Typed a real one,
it posts. That's fine, I'm happy with the form.

**Claude:** I'll write vitest coverage for session.ts and the form next.

**Priya:** Hold off - I'd rather get refresh tokens in first while we've got the context.

**Claude:** OK, tests not written then. Starting refresh tokens: rotating refresh token stored
server-side, short-lived access token.

**Claude:** Problem. The refresh flow needs a token-introspection call per request and
api.relay.example rate-limits us at 10 requests/second on the introspection endpoint. At our
current traffic the SPA alone would blow through that on page load. I tried batching the calls;
that just moved the spike. This approach doesn't work without an API-side change.

**Priya:** Ugh. Park it. Don't try that again, it needs Diego's team to raise the limit or give us
a bulk endpoint. I'll open a ticket - it's AUTH-214.

**Claude:** Parked. Should I refactor src/legacy/admin.js to use the new session helper? It still
does its own cookie parsing.

**Priya:** No. Don't touch src/legacy/ at all, ever. It's frozen, it's going away in Q4, and the
last person who "tidied" it broke billing for two days.

**Claude:** Understood, leaving it alone.

**Priya:** Did you do the sessions table?

**Claude:** Yes - migrations/002_add_sessions.sql, and I applied it to your local dev database. It
ran clean. I have no access to staging, so staging's database has not had it applied and I can't
tell you what state staging is in.

**Priya:** Fine, I'll do staging myself when Sam signs off on the TTL, since the column defaults
depend on it.

**Priya:** Last thing - the API team's spec doc moved. docs/SPEC-v1.md is dead, it's docs/SPEC.md
now, and I've already told the rest of the team. Anything that points at the old one is wrong.

**Claude:** Noted.

**Priya:** I'm done for the day. Nothing is committed yet - it's all sitting in my working tree.
Wrap it up so I can pick this up tomorrow morning without re-reading any of this.
""",
}

# ------------------------------------------------------- fixture B: existing stale master handoff
FILES["b-master-update"] = {
"package.json": FILES["a-webapp-session"]["package.json"],
"docs/SPEC.md": """# relay-web API spec (current)

Supersedes docs/SPEC-v1.md, which was deleted on 2026-07-28.
Auth endpoints, session cookie contract, error envelope.
""",
"src/auth/session.ts": FILES["a-webapp-session"]["src/auth/session.ts"],
"docs/handoffs/_master-handoff.md": """# Master Handoff - relay-web

Project: relay-web
Document Type: Master Handoff
Version: 2.0
Last Updated: 2026-07-24
Current Phase: Auth rebuild
Overall Status: In Progress
Canonical File: docs/handoffs/_master-handoff.md

---

## 1. Executive Summary

relay-web is the customer-facing React SPA for Relay. The current phase is a rebuild of
authentication, replacing the legacy jQuery admin's ad-hoc cookie handling with a single shared
session module. Latest progress: signup flow shipped and approved. Most important blocker: the
session storage decision was contested by security review. Immediate next action: implement
signup email verification.

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

- Decision: Session tokens are stored in browser localStorage and attached as a bearer header.
  - Rationale: simplest integration for the SPA; no CSRF work required.
  - Date: 2026-07-20
  - Status: Final
  - Approval source: Priya
  - Supersedes: n/a

## 4. Project Structure

Repository: relay-web (this repo). API lives in a separate repo owned by Diego's team.
Workstreams: Auth rebuild (Priya), Design tokens (complete), Legacy decommission (not started).
Environments: local, staging, production.

## 5. Architecture and Workflow

React + Vite SPA. API at api.relay.example. Migrations applied by hand per environment.
Approval gate: security-sensitive changes need Sam's sign-off before they reach staging.
Access restriction: only Priya has staging and production database access.

## 6. Sources of Truth

| Source | Location | Purpose | Authority | Status |
|---|---|---|---|---|
| API spec | docs/SPEC-v1.md | Endpoint and auth contract | Diego's team | Current |
| Design tokens | packages/tokens | Colour/spacing values | Design review | Current |
| This document | docs/handoffs/_master-handoff.md | Project state | Canonical | Current |

## 7. Workstream Status

### Auth rebuild

Purpose: one shared session module.
Owner: Priya
Current Status: In Progress
Completed: signup flow, password hashing
In Progress: login flow
Blocked: nothing
Open Decisions: session TTL
Dependencies: API team for token endpoints
Next Action: implement signup email verification
Relevant Sources: src/auth/, docs/SPEC-v1.md

## 8. Important Project History

- 2026-03-30 - legacy cleanup broke billing; src/legacy/ frozen as a result.
- 2026-05-12 - design tokens consolidated into packages/tokens.
- 2026-07-18 - auth rebuild started.

## 9. Final Decisions

- Decision: use `jose` for JWT signing rather than jsonwebtoken.
- Date: 2026-07-19
- Rationale: ESM-native, works in edge runtimes.
- Impact: dependency added to package.json.
- Source: Priya
- Supersedes: n/a

## 10. Open Decisions

- Decision Needed: session TTL
- Why It Matters: determines re-login frequency and the sessions table column defaults.
- Available Options: 1h / 12h / 30d with sliding renewal
- Required Evidence: support-ticket volume for re-login complaints
- Decision Owner: Sam
- Deadline or Trigger: before staging deploy

## 11. Changes Since the Previous Baseline

Signup flow completed and approved. Session storage decision recorded. Design token work closed.

## 12. Superseded or Replaced Items

| Superseded Item | Replacement | Reason | Date |
|---|---|---|---|
| per-app SCSS variables | packages/tokens | drift across surfaces | 2026-05-12 |

## 13. Contradictions and Resolution

None recorded.

## 14. Risks, Constraints, and Dependencies

- Risk: API team's rate limits are undocumented; we may hit them under load.
- Constraint: only Priya can touch staging/production databases.
- Dependency: Diego's team for any API-side change.

## 15. Technical or Operational State

Repository: relay-web
Branch: feat/auth-rebuild
Commit: 7c21ab4
Open PRs: none
Uncommitted changes: none
Build status: passing
Test status: passing (signup only)
Deployment status: not deployed
Database status: migrations 001 applied to local and staging
Migration status: 001 applied everywhere; 002 not written
CI/CD status: GitHub Actions, passing
Backup status: nightly, verified 2026-07-20

## 16. Current Project State

Signup shipped and approved. Login not started. No blockers recorded. Awaiting TTL decision.

## 17. Immediate Next Action

Immediate Next Action: implement signup email verification
Responsible Role or Agent: Priya
Start From: src/auth/signup.ts
Required Inputs: transactional email credentials
Expected Deliverable: verification email sent on signup
Acceptance Criteria: new account cannot log in until verified
Dependencies: none
Stop Conditions: n/a
Do Not Change: src/legacy/

## 18. New-Session Start Guide

1. Read this document, then docs/SPEC-v1.md.
2. Canonical source: this document.
3. Current state: signup done, login not started.
4. Start at src/auth/signup.ts.
5. Final decisions: sections 3 and 9.
6. Do not repeat: the design token consolidation, the legacy cleanup.
7. Access required: repo write, local database.
8. Requires approval: anything security-sensitive reaching staging needs Sam's sign-off.

## 19. Incorporated Daily Handoffs

| Date | Handoff File | Scope | Incorporated into Master |
|---|---|---|---|
| 2026-07-22 | 2026-07-22_001_signup-handoff.md | signup flow | Yes |
| 2026-07-24 | 2026-07-24_001_tokens-handoff.md | design tokens | Yes |
""",
"docs/handoffs/2026-07-22_001_signup-handoff.md": """# Daily Handoff - relay-web - 2026-07-22

Project: relay-web
Date: 2026-07-22
Handoff ID: 2026-07-22_001
Session Scope: signup flow
Workstream: Auth rebuild
Prepared By: Claude (with Priya)
End-of-Session Status: signup complete and approved

## Completed Work
- Signup endpoint and form built; argon2id password hashing. Approved by Priya in review.

## Exact Next Action
Next Action: decide session storage approach before building login.
""",
}

FILES["b-master-update"]["docs/handoffs/2026-07-28_001_spec-move-handoff.md"] = """# Daily Handoff - relay-web - 2026-07-28

Project: relay-web
Date: 2026-07-28
Handoff ID: 2026-07-28_001
Session Scope: API spec relocation, session storage decision reversal
Workstream: Auth rebuild
Prepared By: Claude (with Priya and Sam)
End-of-Session Status: storage decision reversed; spec doc replaced

## 1. Session Objective
Intended: start the login flow.
Actually completed: security review of session storage, decision reversal, spec doc migration.
Not completed: any login code.
Scope change: Sam joined the session and re-opened the storage decision.

## 2. Completed Work
- Action: security review of session storage with Sam.
  - Result: localStorage approach rejected.
  - Status: Complete
  - Evidence: Sam's written sign-off in AUTH-201.
- Action: replaced docs/SPEC-v1.md with docs/SPEC.md.
  - Result: old file deleted, all internal links updated.
  - Location: docs/SPEC.md
  - Status: Complete

## 3. Decisions Made
- Decision: store the session JWT in an httpOnly, secure, sameSite=lax cookie. Do not use
  localStorage and do not send a bearer header from the SPA.
  - Rationale: third-party analytics scripts run on marketing pages; a token in localStorage is
    readable by any injected script, making XSS equivalent to account takeover.
  - Options considered: localStorage bearer token, httpOnly cookie, in-memory only.
  - Rejected: localStorage (XSS exposure), in-memory only (breaks refresh on reload).
  - Expected impact: API must set the cookie; CSRF protection now required.
  - Status: Final
  - Approval: Sam (security), Priya (engineering)
  - Supersedes: the 2026-07-20 localStorage decision recorded in the Master Handoff v2.0.

## 4. What Changed
- Change: docs/SPEC-v1.md deleted, replaced by docs/SPEC.md
- Location: docs/
- Previous State: docs/SPEC-v1.md was the API contract source of truth
- New State: docs/SPEC.md is the API contract source of truth
- Reason: Diego's team restructured the spec; version suffix dropped
- Validation: file present at docs/SPEC.md; old path 404s in the wiki

## 6. Open, Uncertain, or Unverified Items
- Session TTL - Status: Waiting for Approval (Sam, back Monday)
- CSRF strategy for the cookie approach - Status: Open. Nothing implemented yet.

## 9. Exact Next Action
Next Action: implement cookie-based session issuing in src/auth/session.ts
Start From: src/auth/session.ts
Do Not Change: src/legacy/

## 11. Work That Must Not Be Repeated
- Do not re-propose localStorage for session storage. It was formally rejected by security review
  on 2026-07-28 with written sign-off.
"""

# ------------------------------------------------------------- fixture C: non-technical project
FILES["c-nontechnical-full"] = {
"brief.md": """# Northwind Coffee - brand refresh content workstream

Client: Northwind Coffee (12 cafes, Manchester and Leeds).
Engagement: refresh all customer-facing copy for the new brand, launching 2026-09-01.

Deliverables:
- Rewritten website copy (8 pages)
- 6 in-store printed cards
- Launch email sequence (3 emails)
- Tone-of-voice one-pager

Client contact: Marcus Bell (Marketing Lead). All published copy needs Marcus's written sign-off
before it goes live - no exceptions, this was a condition of the contract after the 2025 incident
where a price was published wrong.

Budget: 40 hours. Tracked in the shared sheet.
""",
"content-calendar.csv": """asset,owner,status,due,notes
homepage,Aisha,approved,2026-07-24,signed off by Marcus 24 Jul
about-page,Aisha,draft,2026-08-03,
menu-page,Aisha,in review,2026-07-31,with Marcus since 29 Jul
sourcing-page,Aisha,not started,2026-08-07,blocked - waiting on farm names from Northwind ops
store-card-1,Tom,approved,2026-07-22,printed
store-card-2,Tom,draft,2026-08-05,
email-1-welcome,Aisha,draft,2026-08-10,
email-2-offer,Aisha,not started,2026-08-12,offer amount not agreed
email-3-loyalty,Aisha,not started,2026-08-14,
tone-of-voice,Aisha,approved,2026-07-18,locked
""",
"tone-of-voice.md": """# Northwind tone of voice (LOCKED 2026-07-18)

Warm, plain, specific. Never "artisanal", "curated", or "journey".
Second person. Short sentences. Prices always written as "GBP 3.20", never "3.20 GBP".
""",
"session-notes.md": """# Session notes - 30 July 2026 - Aisha

Worked the menu page and the about page today. Rough notes, not tidied.

- Menu page: finished the rewrite this morning. Sent to Marcus 29 Jul, still sitting with him,
  no response yet. Can't call it done.
- About page: wrote the founder story section. Northwind's ops team gave us two different founding
  years - the website says 2011, the deck Marcus sent says 2009. I've used 2011 for now because
  that's what's currently published, but flagged it. Nobody has confirmed which is right.
- Sourcing page: still stuck. We need the actual farm names and I've asked Northwind ops twice
  (24 Jul and 29 Jul). No reply. This is now the critical path item - it's the longest page and
  it's due 7 Aug.
- Email 2: we can't write it until someone agrees the offer. Marcus said "probably 20% off first
  order" verbally on a call but nothing in writing. Treating that as unconfirmed.
- Tried writing the loyalty email using the old 2024 loyalty terms as a base. Wasted about an hour
  before Marcus mentioned the loyalty scheme is being replaced in September and the new terms
  aren't drafted. Don't build on the 2024 terms.
- Tom's store card 2 draft came in. I reviewed it and it uses "curated" twice, which the tone
  doc bans. Sent back to Tom, not yet fixed.
- Updated the tracker sheet to reflect all of the above.
- Budget: roughly 26 of the 40 hours used. Not formally checked against the sheet.

Handing this to Dan on Monday - I'm on leave all next week. He has never worked on Northwind.
""",
}


def write_fixture(root: Path, name: str, files: dict[str, str], git: bool) -> None:
    target = root / name
    if target.exists():
        shutil.rmtree(target)
    for rel, content in files.items():
        path = target / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    if git:
        subprocess.run(["git", "init", "-q"], cwd=target, check=True)
        subprocess.run(["git", "add", "-A"], cwd=target, check=True)
        subprocess.run(
            ["git", "-c", "user.email=fixture@example.com", "-c", "user.name=Fixture",
             "commit", "-q", "-m", "baseline"],
            cwd=target, check=True,
        )


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    root.mkdir(parents=True, exist_ok=True)

    write_fixture(root, "a-webapp-session", FILES["a-webapp-session"], git=True)
    # Leave the session's work uncommitted so the handoff has real working-tree state to report.
    a = root / "a-webapp-session"
    subprocess.run(["git", "rm", "-q", "--cached", "src/auth/session.ts",
                    "src/auth/login-form.tsx", "migrations/002_add_sessions.sql"],
                   cwd=a, check=True)
    subprocess.run(["git", "-c", "user.email=f@example.com", "-c", "user.name=F",
                    "commit", "-q", "-m", "chore: baseline without session work"],
                   cwd=a, check=True)
    subprocess.run(["git", "checkout", "-q", "-b", "feat/auth-rebuild"], cwd=a, check=True)

    write_fixture(root, "b-master-update", FILES["b-master-update"], git=True)
    b = root / "b-master-update"
    subprocess.run(["git", "checkout", "-q", "-b", "feat/auth-rebuild"], cwd=b, check=True)

    write_fixture(root, "c-nontechnical-full", FILES["c-nontechnical-full"], git=False)

    print(f"fixtures built under {root}")
    for d in sorted(p.name for p in root.iterdir() if p.is_dir()):
        print(f"  {d}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
