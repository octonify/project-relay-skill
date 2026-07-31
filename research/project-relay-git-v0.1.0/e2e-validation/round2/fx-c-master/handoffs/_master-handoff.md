# Master Handoff — checkout-service

Project: checkout-service
Document Type: Master Handoff
Version: 4.0
Last Updated: 2026-07-30
Current Phase: Refunds
Overall Status: In Progress — blocked on production credentials
Canonical File: docs/handoffs/_master-handoff.md

## 2. Executive Summary

checkout-service captures card payments for the storefront. The current phase is refunds.
Idempotency shipped in April. The legacy cart rewrite was cancelled — the storefront team
kept the existing cart, and feat/legacy-cart is deleted. Refund flow is underway on
feat/refund-flow: the route is wired into the server and returns `refund_pending`, but it
does not yet call the payment provider, and the real path can't be tested until Ops issues
production refund credentials.

## 4. Locked Principles and Decisions

- Idempotency keys are scoped per merchant, not globally. Decided 2026-04-02. A global
  namespace lets one merchant probe another's keys. Source: 2026-04-02 Daily.
- Money is handled in integer minor units everywhere. No floats cross a module boundary.
  Decided 2026-02-18.
- Refunds are accepted asynchronously and return 202, not 201. The provider can take up to
  40 seconds to settle a refund; holding the HTTP connection open that long caused gateway
  timeouts in an earlier prototype. Synchronous refunding was tried and abandoned — do not
  retry it. Decided 2026-06-28. Source: 2026-06-28_001_refund-flow-handoff.md.
- Full refunds are not automated. The provider's modern API only supports partial refunds;
  full refunds go through the old admin tool. Decided 2026-06-28, documented on
  origin/feat/refund-flow in docs/refunds.md (commit 1bf1477, not yet pulled into this
  local branch).

## 5. Repository and Project Structure

Repository: checkout-service. Default branch: main.
Active branches: feat/refund-flow. feat/legacy-cart was deleted 2026-06-28 (cart rewrite
cancelled) and no longer exists locally or on origin.
`src/routes/` holds HTTP handlers, `src/lib/` shared helpers.

## 7. Sources of Truth

| Source | Location | Purpose | Authority | Status |
|---|---|---|---|---|
| Design notes | docs/design.md | Architecture decisions | Authoritative | Current |
| Master Handoff | docs/handoffs/_master-handoff.md | Project state | Authoritative | Current |
| Refund limitation note | docs/refunds.md | Documents partial-refund-only constraint | Authoritative | On origin/feat/refund-flow (commit 1bf1477); not present on local feat/refund-flow as of this update |

## 15. Risks, Constraints, and Dependencies

- The payment provider's published refund rate limit is 10/second, but 429s were observed
  in the sandbox at around 6/second. Treat 5/second as the working ceiling until the
  provider confirms the real number. Source: 2026-07-02_001_refund-provider-handoff.md.
- No staging card vault. Refund testing against staging uses provider sandbox tokens only.
- Blocked: no production refund credentials. Sandbox only — nobody can exercise the real
  refund path until Ops issues them. Source: 2026-07-02_001_refund-provider-handoff.md.

## 16. Current Technical State

Repository: checkout-service
Default branch: main
Active branch: feat/refund-flow
HEAD of active branch: c62caba (feat(refund): route partial refunds through the server)
Uncommitted or unpushed work: none tracked; untracked directories present (.claude/,
docs/handoffs/, notes/) — tooling and handoff scaffolding, not application code
Branch vs origin/feat/refund-flow: ahead by 2 commits, behind by 1 (origin has 1bf1477,
"docs: note the partial-refund limitation", not yet pulled locally)
Refund route: wired into src/server.ts, returns 202 refund_pending; not yet connected to
the provider client (src/routes/refund.ts) — deliberate scaffolding, not a finished path
Open PRs: Unknown — GitHub lookup unavailable this session (gh could not reach the repository)
Build status: Not verified this session
Test status: Not verified this session
Deployment status: Unknown — not checked this session (last known: staging deploy of the
now-cancelled cart work, 2026-06-10, no longer current)

## 18. Immediate Next Action

Immediate Next Action: Get production refund credentials from Ops so the real refund path
can be exercised end-to-end; until then, work is limited to sandbox-only wiring.
Responsible Role or Agent: whoever picks up the refund work; credentials must come from Ops
Start From: feat/refund-flow, src/routes/refund.ts (connect to the provider client once
credentials exist)

## 20. Incorporated Daily Handoffs

| Date | Handoff File | Scope | Incorporated into Master |
|---|---|---|---|
| 2026-04-02 | 2026-04-02_001_idempotency-handoff.md | Idempotency | Yes |
| 2026-06-28 | 2026-06-28_001_refund-flow-handoff.md | Refund flow | Yes |
| 2026-07-02 | 2026-07-02_001_refund-provider-handoff.md | Refund provider wiring | Yes |
