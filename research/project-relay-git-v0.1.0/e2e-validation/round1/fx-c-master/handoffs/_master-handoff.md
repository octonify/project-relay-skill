# Master Handoff — checkout-service

Project: checkout-service
Document Type: Master Handoff
Version: 4.0
Last Updated: 2026-07-30
Current Phase: Refunds
Overall Status: In Progress
Canonical File: docs/handoffs/_master-handoff.md

## 2. Executive Summary

checkout-service captures card payments for the storefront. Idempotency shipped in April. The
legacy cart rewrite on feat/legacy-cart was dropped — the storefront team chose to keep the
existing cart — so PR #31 is stale (section 13). Active work is now the refund flow on
feat/refund-flow: the `/refund` route is wired into the server but is still scaffolding — it
returns `refund_pending` without calling the payment provider. Full refunds stay on the old
admin tool; only partial refunds go through the API. Local feat/refund-flow and
origin/feat/refund-flow have diverged and need reconciling before the next push (section 16).
Biggest blocker: no production refund credentials, so the real provider path is still untested.

## 4. Locked Principles and Decisions

- Idempotency keys are scoped per merchant, not globally. Decided 2026-04-02. A global
  namespace lets one merchant probe another's keys. Source: 2026-04-02 Daily.
- Money is handled in integer minor units everywhere. No floats cross a module boundary.
  Decided 2026-02-18. Consistent with `src/lib/money.ts`.
- Refunds are accepted asynchronously and return 202, not 201. Decided 2026-06-28. The provider
  can take up to 40 seconds to settle a refund; holding the HTTP connection open that long caused
  gateway timeouts in the synchronous prototype. Do not retry the synchronous approach. Source:
  2026-06-28_001_refund-flow-handoff.md.

## 5. Repository and Project Structure

Repository: checkout-service. Default branch: main.
Active branch: feat/refund-flow (refund work). feat/legacy-cart was deleted — see section 13.
`src/routes/` holds HTTP handlers (`charge.ts`, `refund.ts`); `src/lib/` holds shared helpers
(`money.ts`). No provider-client module exists yet for refunds.

## 7. Sources of Truth

| Source | Location | Purpose | Authority | Status |
|---|---|---|---|---|
| Design notes | docs/design.md | Architecture decisions | Authoritative | Current |
| Master Handoff | docs/handoffs/_master-handoff.md | Project state | Authoritative | Current |
| Refund limitation note | docs/refunds.md | Documents the partial-refund-only limitation | Authoritative once merged | Exists only on origin/feat/refund-flow (commit 6e38064); not yet in the local working tree |

## 9. Important Project History

- 2026-06-28: Legacy cart rewrite dropped — the storefront team decided to keep the existing
  cart, and feat/legacy-cart was deleted. Work shifted fully to the refund flow; PR #31 is
  superseded (section 13). Source: 2026-06-28_001_refund-flow-handoff.md.
- 2026-06-28: Synchronous refund submission was tried and abandoned after it caused gateway
  timeouts. Source: same Daily.

## 13. Superseded or Replaced Items

| Superseded Item | Replacement | Reason | Date |
|---|---|---|---|
| feat/legacy-cart branch and PR #31 | feat/refund-flow (current active work) | Storefront team decided to keep the existing cart; the rewrite is no longer needed | 2026-06-28 |
| v3.0 Master's "Test status: passing (48 tests)" / "deployed to staging 2026-06-10" | Not applicable — no equivalent has been verified for refund work | Those results were from the deleted legacy-cart branch | 2026-07-30 |

## 15. Risks, Constraints, and Dependencies

- Provider rate limit on refund calls is worse than documented: 10/second is the published
  number, but sandbox testing on 2026-07-02 saw 429s at around 6/second. Treat 5/second as the
  working ceiling until the provider confirms otherwise. No retry-after header is returned, so
  backoff is guessed. Supersedes the "10/second" figure in v3.0. Source:
  2026-07-02_001_refund-provider-handoff.md.
- No staging card vault; refund testing must use provider sandbox tokens only.
- Full refunds are not supported through the refund API — the provider only exposes partial
  refunds through the modern API. Full refunds still go through the old admin tool, which nobody
  wants to automate. Source: 2026-06-28_001_refund-flow-handoff.md.
- Blocked: no production refund credentials. Sandbox only, so the real provider path is untested
  until Ops issues them. Still outstanding as of 2026-07-30 — an untracked local note
  (notes/todo.txt: "chase ops re: refund creds") shows the chase was still pending; no
  confirmation was found this session that credentials arrived. Source:
  2026-07-02_001_refund-provider-handoff.md.
- Local feat/refund-flow and origin/feat/refund-flow have diverged (section 16) and need
  reconciling before further refund work is pushed.

## 16. Current Technical State

Repository: checkout-service
Default branch: main
Active branch: feat/refund-flow (feat/legacy-cart deleted)
HEAD of active branch: 85e4c75 "feat(refund): route partial refunds through the server"
Local/remote divergence: local is ahead 2 / behind 1 of origin/feat/refund-flow. Local has
3791ea2 ("accept refund requests") and 85e4c75, neither on origin; origin has 6e38064 ("docs:
note the partial-refund limitation", adds docs/refunds.md), not in local history. Both sides
share 8f75289 as the common ancestor — reconcile (rebase or merge) before pushing.
Uncommitted or unpushed work: tracked files clean (no staged/unstaged changes). Untracked:
.claude/ (agent config), docs/handoffs/ (this handoff directory — not yet added to git),
notes/todo.txt (personal reminder: "chase ops re: refund creds").
Open PRs: Unknown — GitHub was not reachable this session (gh could not reach the repository).
PR #31 (legacy cart) is presumed stale per section 13 but was not independently reverified.
Build status: Not verified this session — no node_modules installed, build not run.
Test status: No automated test suite exists in this repo (package.json defines no test script).
The "passing (48 tests)" figure in v3.0 referred to the deleted legacy-cart branch.
Deployment status: Not verified for the refund flow. The "deployed to staging 2026-06-10" figure
in v3.0 referred to the legacy-cart branch and does not apply here.

## 18. Immediate Next Action

Immediate Next Action: Reconcile the diverged feat/refund-flow branches — rebase local commits
3791ea2 and 85e4c75 onto origin/feat/refund-flow (6e38064), resolving with the incoming
docs/refunds.md, then push.
Responsible Role or Agent: whoever picks up the refund work next
Start From: local branch feat/refund-flow at 85e4c75
Required Inputs: push access to origin/feat/refund-flow
Expected Deliverable: one reconciled feat/refund-flow branch containing docs/refunds.md plus
both route-wiring commits, pushed to origin
Acceptance Criteria: `git log origin/feat/refund-flow..HEAD` and
`git log HEAD..origin/feat/refund-flow` are both empty after push
Dependencies: none
Do Not Change: do not resurrect feat/legacy-cart or reopen PR #31 (section 13); do not switch
refunds back to synchronous handling (section 4)

Queue after that, in priority order:
1. Chase Ops for production refund credentials (blocked on Ops — section 15).
2. Connect `src/routes/refund.ts` to an actual provider client; it currently only returns
   scaffolding.
3. Decide whether/how to handle full refunds, which today are manual-only via the admin tool.

## 20. Incorporated Daily Handoffs

| Date | Handoff File | Scope | Incorporated into Master |
|---|---|---|---|
| 2026-04-02 | 2026-04-02_001_idempotency-handoff.md | Idempotency | Yes |
| 2026-06-28 | 2026-06-28_001_refund-flow-handoff.md | Refund flow | Yes |
| 2026-07-02 | 2026-07-02_001_refund-provider-handoff.md | Refund provider wiring | Yes |
