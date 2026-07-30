# Master Handoff — webhook-relay

Project: webhook-relay (repository directory `g3-handover`)
Document Type: Master Handoff
Version: 1.0
Last Updated: 2026-07-30
Current Phase: Early implementation — signature verification, blocked on an external credential
Overall Status: Blocked, and being handed to a new owner cold
Canonical File: `docs/handoffs/_master-handoff.md`

---

## 1. Executive Summary

webhook-relay forwards partner webhooks into the event bus. The current and only active piece of
work is authenticating those inbound webhooks by verifying an HMAC-SHA256 signature computed over
the raw request body.

That work is blocked. The partner's signing secret is held by their integrations team, has been
requested twice, and has not arrived — so there is no secret and no test vector, and nothing about
the verification path can be validated. On top of that, the repository has no remote: both commits
exist on one machine only, so a successor currently has no way to obtain the code.

The previous owner is away for two weeks and the project has been handed over cold. There is also
an unresolved discrepancy between the owner's account of the work and what the repository actually
contains — see section 8, which the incoming owner should read before touching `src/verify.ts`.

**Immediate next action:** provision a remote and push the work, so it can be handed over at all.
Full form in section 10.

---

## 2. Project Purpose and Definition

Problem being solved: Partner webhooks need to reach the internal event bus, authenticated so that
only genuine partner traffic is relayed.

Primary objective (current): Verify inbound partner webhook signatures before relaying.

Intended final output: A relay service that authenticates and forwards partner webhooks.

Users / stakeholders: The webhook partner, whose integrations team owns the signing secret. Dana is
the named contact on the partner side. No internal stakeholders or owners are named in any source
in this repository — that is a gap, not an omission from this document.

Success criteria for the current phase: A genuine partner-signed payload verifies, a tampered one
does not, demonstrated against a real signing secret rather than a synthetic one.

Out of scope / unknown: Everything beyond signature verification and relay is undefined in the
sources available. Do not infer scope from the empty stubs in `src/`.

---

## 3. Repository and Project Structure

Repository: local Git repository only. **No `origin` remote is configured** and no branch has an
upstream. There is no hosted copy, no clone URL, and consequently no PR or issue tracker in use.

Default branch: `main`, at `470ca46`.

Active branches:
- `feat/signature-verify` — the only work branch, 1 commit ahead of `main`, at `009a397`.

Branching model: Not documented anywhere; inferred only from the single `feat/` branch present. No
`CONTRIBUTING.md` or branch policy exists. Treat the model as undecided (section 9).

Protected branches, environments, ownership: None configured, none documented. There is nothing
protecting `main` today.

Key files (the tracked tree is three files in total):

| Path | Contents |
|---|---|
| `README.md` | One line: forwards partner webhooks into the event bus |
| `src/relay.ts` | `export const relay = () => {};` — empty stub |
| `src/verify.ts` | Two comment lines plus `export const verify = () => false;` |

There is no `package.json`, no `tsconfig.json`, no test runner, and no CI configuration. TypeScript
sources exist with nothing configured to compile, run, or test them.

---

## 4. Architecture and Workflow

The intended design, as far as it has been settled: inbound partner webhook → signature
verification over the **raw** request body → relay to the event bus. Only the verification step has
been worked on; the relay step is an empty stub.

There are no CI pipelines, no approval gates, and no access restrictions configured. Nothing
currently prevents a push to `main`. Whether that should remain true is an open decision (section
9).

---

## 5. Sources of Truth

| Source | Location | Purpose | Authority | Status |
|---|---|---|---|---|
| This document | `docs/handoffs/_master-handoff.md` | Canonical project state | Authoritative | Current |
| Session detail | `docs/handoffs/2026-07-30_001_signature-verify-handoff.md` | Full account of the signature work, its blocker, and the evidence behind section 8 | Authoritative for that session | Current |
| Repository | branch `feat/signature-verify` @ `009a397` | The code itself | Authoritative over any document, for what the code does | Current |
| Owner's notes | `SESSION-NOTES.md` (untracked, will not survive a clone) | Original handover account | Superseded by the Daily above, which preserves its content | Historical |
| The signing secret | Partner's integrations team, contact Dana | Required to validate anything | External, not held | Not obtained |

Precedence: not formally decided by anyone. Where this document and the repository disagree, the
repository is what runs — section 8 exists because they currently do disagree.

---

## 6. Final Decisions

- Decision: Authenticate partner webhooks with HMAC-SHA256 over the raw request body.
  - Date: 2026-07-30
  - Rationale: The partner signs the exact bytes transmitted; a re-serialized parsed body will not
    match. Full reasoning in the Daily.
  - Impact: Makes the raw-body ordering constraint (section 7) binding, and makes the partner's
    signing secret a hard prerequisite for any validation.
  - Source: `docs/handoffs/2026-07-30_001_signature-verify-handoff.md`

- Decision: Hand over unverified code rather than validate against a synthetic secret.
  - Date: 2026-07-30
  - Rationale: A fabricated secret would only prove the code agrees with itself, and would leave a
    false green signal behind.
  - Impact: The successor knowingly inherits untested code. Do not "fix" this by inventing a test
    secret.
  - Source: as above

---

## 7. Risks, Constraints, and Dependencies

**Constraint — raw body before parsing.** The raw request body must be captured before any JSON
body parser runs. If it is parsed first, the signed bytes are gone and verification fails
regardless of how correct the HMAC code is. Discovered 2026-07-30 at a cost of about an afternoon.
Currently unimplemented: `src/relay.ts` has no middleware wiring. This failure mode presents
exactly like a bug in `verify()`, so anyone debugging a signature mismatch will suspect the wrong
file first.

**Blocking dependency — the partner's signing secret.** Held by the partner's integrations team.
Requested twice; Dana on the partner side said she would chase it. No date, no ticket, and no
internal owner for the chase. The person who was tracking it is away for two weeks, so the default
outcome is that this does not move at all. A third identical request is not the answer — two have
already failed. Ask for a signed sample payload and its expected signature header alongside the
secret; the secret alone is not enough to build a test vector.

**Risk — all work is unpushed and on one machine.** Both commits exist only in one working copy.
The exposure window is the full two weeks of the owner's absence, and the successor cannot obtain
the code until it is pushed. This is why section 10's next action is what it is.

**Risk — `verify()` rejects everything.** The exported function returns `false` unconditionally
today. Nothing may be deployed in this state, and the temptation to make it return `true` to unblock
local work would ship an unauthenticated webhook endpoint.

**Risk — no toolchain.** Even once the secret arrives, there is nothing in the repository capable of
running a test. That work is unstarted, not broken.

---

## 8. Contradictions and Resolution

- Contradiction: The outgoing owner's notes state that HMAC-SHA256 verification was written in
  `src/verify.ts` and committed to `feat/signature-verify`. The repository does not show that.
- Conflicting sources: `SESSION-NOTES.md` versus commit `009a397`.
- Verified current state: the diff of `009a397` changes comment lines only. The full current file
  is two comments plus `export const verify = () => false;`. A `git grep` over the HEAD tree finds
  no `createHmac`, no `crypto` import, and no raw-body handling anywhere in the repository. The
  working tree is clean and there are no stashes, so no uncommitted implementation is present here.
- Authoritative source: the repository, for what the code contains.
- Resolution: **Unresolved.** The implementation may exist somewhere outside this working copy — an
  editor buffer, another machine, a branch never created — or it may never have been written.
- What would settle it: a direct answer from the outgoing owner, ideally before they leave.
- Why it matters: it decides whether the remaining work is "test the implementation" or "write the
  implementation", and the owner's standing instruction *"don't rewrite verify.ts, it's probably
  correct"* cannot be followed literally against a file that contains no implementation. Settle
  this before concluding the code is broken and before starting a rewrite.

---

## 9. Open Decisions

- Decision Needed: Where this repository should live — which organisation or account owns it, and
  which remote it is pushed to.
  - Why It Matters: It blocks the immediate next action and therefore the entire handover.
  - Required Evidence: A team decision plus permission to create the repository.
  - Decision Owner: Unassigned.

- Decision Needed: Who internally owns chasing the partner's signing secret while the previous owner
  is away.
  - Why It Matters: Without a named owner the blocker will not move for two weeks by default.
  - Required Evidence: Someone accepting it, and a route to escalate past the partner's integrations
    team queue.
  - Decision Owner: Unassigned.
  - Trigger: Before the outgoing owner's absence begins.

- Decision Needed: Branching model and whether `main` should be protected.
  - Why It Matters: A second contributor is about to join a repository with no stated conventions.
  - Decision Owner: Unassigned.

---

## 10. Immediate Next Action

```
Immediate Next Action: Provision a remote for this repository and push both main and
                       feat/signature-verify to it.
Responsible Role:      the incoming owner
Start From:            the repository root, branch feat/signature-verify at 009a397
Required Inputs:       a remote the team can access, and agreement on which organisation owns
                       webhook-relay (section 9 — neither is recorded anywhere in this project)
Expected Deliverable:  an origin remote, both branches pushed, an upstream set for
                       feat/signature-verify
Acceptance Criteria:   a second person can clone the repository and see commit 009a397
Dependencies:          the ownership decision in section 9
Stop Conditions:       nobody can say which organisation should own the repository — in which
                       case getting that answer is the task
Do Not Change:         do not rewrite or force-push over commits 470ca46 and 009a397; the
                       contradiction in section 8 is anchored to 009a397 exactly as it stands
```

This is the next action because everything else in this document is either blocked on an external
credential or unreachable by anyone but the current machine's owner. Until the code is pushed,
there is no handover — only a promise of one.

**Prioritized queue after that:**

1. Resolve section 8 with the outgoing owner, if any window remains before they leave.
2. Take over the signing-secret chase: name an internal owner, set a date, find the escalation path
   past the integrations team, and request a signed sample payload as well as the secret.
3. Implement raw-body capture ahead of the JSON parser in `src/relay.ts` — independent of the
   secret and startable today.
4. Add a toolchain and a test that can be pointed at a real vector the moment the secret lands.

---

## 11. Current Technical State

```
Repository:            local only — no origin remote, no hosted copy
Default branch:        main @ 470ca46
Active branches:       feat/signature-verify @ 009a397 (1 ahead of main, no upstream)
Uncommitted work:      none staged, none unstaged
                       untracked: .claude/, SESSION-NOTES.md
Stashes:               none        Tags: none
Open PRs:              Not verified as of 2026-07-30 — gh could not reach a repository, and no
                       remote exists to host one
Open issues:           Not verified as of 2026-07-30 — same reason
Build status:          Unknown — no build tooling exists in the repository
Test status:           Unknown — no tests and no test runner exist; nothing was run
Migration status:      Not applicable — no data layer in the project
Deployment status:     Nothing deployed
Environment status:    No environment variables, secrets, or configuration are set by this project
CI/CD status:          None configured
```

---

## 12. New-Session Start Guide

1. **Read first:** this file, then `docs/handoffs/2026-07-30_001_signature-verify-handoff.md`, then
   `src/verify.ts` and `src/relay.ts` — both are three lines or fewer.
2. **Canonical source:** this file for project state; the repository for what the code does.
3. **Current state:** one unpushed local branch, verification blocked on an external secret, and an
   unresolved question about whether the verification code exists at all (section 8).
4. **Start here:** section 10.
5. **Final decisions:** section 6 — HMAC-SHA256 over the raw body, and no validation against a
   synthetic secret.
6. **Do not repeat:** re-deriving the raw-body ordering constraint (section 7, already settled at a
   cost of an afternoon); sending a third identical request for the signing secret (two have
   failed); rewriting `src/verify.ts` on the assumption it is wrong before reading section 8.
7. **Access required:** the partner's signing secret plus a signed sample payload, from the
   partner's integrations team via Dana; and permission to create the remote in section 10.
8. **Requires explicit human approval:** creating the remote and choosing its owning organisation;
   any deployment (nothing is deployable while `verify()` rejects all traffic); any force-push or
   history rewrite over `470ca46` or `009a397`.

---

## 13. Incorporated Daily Handoffs

| Date | Handoff File | Scope | Incorporated into Master |
|---|---|---|---|
| 2026-07-30 | `2026-07-30_001_signature-verify-handoff.md` | Signature verification; handover to a new owner | Yes — v1.0 |
