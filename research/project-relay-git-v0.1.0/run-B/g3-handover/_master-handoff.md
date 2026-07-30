# Master Handoff — webhook-relay

Project: webhook-relay (repository directory `g3-handover`)
Document Type: Master Handoff
Version: 1.0
Last Updated: 2026-07-30
Current Phase: Early implementation — skeleton only
Overall Status: Blocked, and in transfer. The original developer is away for two weeks; a successor is taking over cold.
Canonical File: `docs/handoffs/_master-handoff.md`

First edition of this Master. There is no previous baseline to diff against, so it is built entirely from repository inspection on 2026-07-30 plus one Daily Handoff (§19).

---

## 1. Executive Summary

**What this is:** a service that forwards partner webhooks into an internal event bus (`README.md`). It exists as two source stubs and nothing else.

**Objective of current work:** verify the HMAC-SHA256 signature on incoming partner webhooks before relaying them.

**Latest progress:** the approach was chosen and one hard constraint was learned (§14). No working verification code exists — see §13, which is the first thing a new reader should absorb.

**Most important blocker:** the repository has no remote and is not pushed anywhere, so the successor cannot obtain the code at all. Behind that, the partner's signing secret has not arrived, which blocks interop confirmation.

**Immediate next action:** publish the repository where the successor can reach it — §17.

---

## 2. Project Purpose and Definition

Problem being solved: partner webhooks need to reach the internal event bus, authenticated.

Primary objective (current): reject any webhook whose HMAC-SHA256 signature over the raw body does not verify, and relay the rest.

Intended final output: Unknown — no specification, ticket, or design document exists in the repository.

Users / stakeholders: an unnamed partner organization sends the webhooks; their integrations team holds the signing secret. No internal stakeholders, owners, or reviewers are named in any record.

Success criteria: Unknown — not stated anywhere. Nobody has defined what "done" means for this service beyond the verification behaviour above.

Out of scope: Unknown — nothing has been explicitly excluded.

These gaps are real and worth closing early; they are not an artifact of the handoff. A successor should expect to have to ask.

---

## 3. Repository and Project Structure

Repository: local Git repository only. **No remote is configured** (`git remote -v` returns nothing), so no canonical URL exists and no clone of this work exists anywhere else.

Default branch: `main` @ `c84ee86`.

Active branches: `feat/signature-verify` @ `7151400` — 1 ahead of `main`, 0 behind. This is where all current work lives.

Branching model: inferred from the single `feat/` branch — not documented, not confirmed by anyone. Treat as convention, not policy.

Protected branches / environments / ownership: none configured and none documented. No `CONTRIBUTING.md`, no `CODEOWNERS`, no environments observed.

Key directories:

| Path | Contents |
|---|---|
| `src/verify.ts` | Signature verification — a stub returning `false` (§13) |
| `src/relay.ts` | Relay entry point — `export const relay = () => {};`, an empty stub |
| `docs/handoffs/` | This Master and dated Daily Handoffs |
| `.claude/` | The `project-relay-git` skill and the `/handoff` command. Untracked. |

---

## 4. Architecture and Workflow

Architecture: none yet beyond the two stubs. There is no HTTP server, no framework, no body parser, and no event-bus client in the repository — the relay path described in `README.md` is not implemented.

Build / test / CI: **none exists.** No `package.json`, no lockfile, no `tsconfig.json`, no test runner, no CI workflow. The project cannot currently be built, typechecked, or tested by any means present in the repository. Standing one up is a prerequisite for validating anything, and it does not depend on the partner.

Review, release, deployment, approval gates, access restrictions: none observed, none documented. Nothing has been deployed and no deployment target is named anywhere.

---

## 5. Sources of Truth

| Source | Location | Purpose | Authority | Status |
|---|---|---|---|---|
| The repository at `feat/signature-verify` | local only, no remote | Actual state of the code | **Highest** — verified by inspection 2026-07-30 | Current |
| This Master | `docs/handoffs/_master-handoff.md` | Durable project state, constraints, next action | Canonical for project state | Current |
| Daily Handoffs | `docs/handoffs/YYYY-MM-DD_NNN_*.md` | Per-session detail and evidence | Historical record, dated | Current |
| `SESSION-NOTES.md` | project root, **untracked** | Outgoing developer's first-hand account of the blocker | First-hand for the partner chase; **not authoritative on code state** (§13) | Superseded on code state |
| Partner webhook specification | does not exist locally | Header name, digest encoding, payload framing | Would be authoritative | **Missing — must be obtained** |

Precedence: the repository outranks any document about the repository. This is not an inherited rule — it is stated here because a documented claim was found to contradict the code on day one (§13), and the contradiction was resolved by reading the code. No other precedence has been established by anyone.

---

## 6. Important Project History

- **2026-07-30 —** `c84ee86` created the project skeleton: `README.md`, `src/relay.ts`, `src/verify.ts`.
- **2026-07-30 —** `7151400` recorded the HMAC-over-raw-body approach and the secret blocker in comments on `src/verify.ts`. No executable change. (Daily: `2026-07-30_001_signature-verify-handoff.md`)
- **2026-07-30 —** the project passed to a successor for a two-week absence. The handover surfaced that the verification believed to be written does not exist (§13).

The project is one day old; this is its entire history.

---

## 7. Final Decisions

- **Decision:** Verify partner webhooks with HMAC-SHA256 computed over the raw request body.
  - Date: 2026-07-30
  - Rationale: the partner's scheme, as understood by the outgoing developer.
  - Impact: constrains the transport layer permanently — see the raw-body constraint in §14.
  - Source: `SESSION-NOTES.md`; commit `7151400`.
  - Status: Final as the chosen approach. Unimplemented, and unconfirmed against the partner's actual scheme, which is undocumented (§8).

- **Decision:** Hand the project over unmerged, with no PR, rather than finish it.
  - Date: 2026-07-30
  - Rationale: the signing secret had not arrived and the developer's absence began.
  - Impact: `feat/signature-verify` stays open and unreviewed for at least two weeks.
  - Source: Daily `2026-07-30_001_signature-verify-handoff.md`.

## 8. Open Decisions

- **Decision Needed:** Whether to implement and unit-test the HMAC path now, using a locally generated secret, rather than waiting for the partner.
  - Why it matters: it determines whether two weeks are spent blocked or productive. HMAC is symmetric, so the algorithm may be fully exercisable without the partner's secret, leaving only interop confirmation blocked.
  - Required evidence: confirmation that a self-signed test vector exercises the same code path the partner's request will. Reasoning and caveats: Daily `2026-07-30_001_signature-verify-handoff.md` §6 item 5 — an assessment, not something tried.
  - Decision Owner: Unassigned — no successor is named in any record.
  - Trigger: at successor onboarding, before any waiting begins.

- **Decision Needed:** Where the repository should be hosted, and who administers access.
  - Why it matters: it is the gating step for the entire handover (§17) and no remote exists to default to.
  - Decision Owner: Unassigned.
  - Trigger: immediately.

---

## 9. Contradictions and Resolution

- **Contradiction:** `SESSION-NOTES.md` states that HMAC-SHA256 verification was written in `src/verify.ts` and committed, and advises the successor not to rewrite it because "it's probably correct". The file contains no HMAC implementation.
- **Verified current state:** `src/verify.ts` is `export const verify = () => false;` under two descriptive comments. Commit `7151400` changed comments only — `git show 7151400` is `2 insertions(+), 1 deletion(-)`, entirely within comment lines. Verified by direct inspection on 2026-07-30.
- **Authoritative source:** the repository (§5).
- **Resolution:** signature verification is **not started in code**. The approach and the raw-body constraint are the real assets from that session; the implementation is not. The advice not to rewrite the file is void — there is nothing there to preserve.
- **Corrective action required:** implement `verify()` (§17 queue item 3). Until then, `verify()` fails closed: wiring it into the relay path as-is silently rejects every partner webhook.
- Detail and evidence: Daily `2026-07-30_001_signature-verify-handoff.md` §4.

---

## 10. Risks, Constraints, and Dependencies

**Constraints**

- **Raw body before parsing.** The signature is computed over the exact bytes received. The raw body must be captured before any JSON body parser runs; once parsed and re-serialized, the bytes differ and no correct HMAC implementation can ever match. Binding on whatever transport layer is built — `src/relay.ts` is currently empty, so nothing in the code enforces or hints at this today. Discovered at the cost of an afternoon: Daily `2026-07-30_001_signature-verify-handoff.md` §7.
- **No build or test toolchain** (§4). Nothing can be validated until one exists.

**Active risks**

| Risk | Impact | Mitigation | Owner | Status |
|---|---|---|---|---|
| Source exists on one unattended machine for two weeks — no remote, no backup, no stash | Total loss of both branches and all context | §17 — publish the repository | Outgoing developer, before leaving | Open |
| `verify()` returns `false` unconditionally but reads as implemented | Every partner webhook silently rejected if wired up as-is | §9; do not wire the relay path to `verify()` until it is implemented | Unassigned | Open |
| Handoff context lives in untracked files (`SESSION-NOTES.md`, `docs/handoffs/`) | Successor receives two stubs and no context | Commit them with the push in §17 | Outgoing developer | Open |

**Dependencies**

- **Partner signing secret — not received.** Held by the partner's integrations team; interop verification is untested until it arrives. Requests to date, who is chasing, and what to reference when following up: Daily `2026-07-30_001_signature-verify-handoff.md` §6 item 1 and §11. Status: Blocked, with **no internal owner assigned** while the requester is away.
- **Partner webhook specification — not held.** Header name, digest encoding (hex vs base64), any `sha256=` prefix, replay/timestamp scheme, and exact signed payload are all unknown. Needed alongside the secret; asking only for the secret will leave the implementation guessing.

---

## 11. Current Technical State

Verified by inspection and `.claude/skills/project-relay-git/scripts/handoff_context.py` on 2026-07-30.

```
Repository:           local Git only — no remote configured
Default branch:       main @ c84ee86
Active branch:        feat/signature-verify @ 7151400 (1 ahead of main, 0 behind)
Unpushed work:        all of it — no remote, no upstream tracking branch
Uncommitted:          untracked: SESSION-NOTES.md, .claude/, docs/handoffs/
                      (staged 0, unstaged 0, no stashes, no tags)
Open PRs:             Not verified — gh could not reach a repository; no remote exists to host one
Open issues:          Not verified — same reason
Build status:         Not applicable — no build tooling exists in the repository
Test status:          Not applicable — no test tooling exists; nothing was run
Migration status:     Not applicable — no data layer
Deployment status:    Nothing deployed; no deployment target observed
Environment status:   No environment variables, secrets, or configuration present
CI/CD status:         None configured
```

---

## 12. Current Project State

Current phase: skeleton, pre-first-feature, mid-transfer.

Completed: project skeleton (`c84ee86`); approach chosen; raw-body constraint learned.

Active work: signature verification on `feat/signature-verify` — design intent only, no working code.

Incomplete: the HMAC implementation; the transport layer; all build and test tooling.

Blockers: repository not reachable by the successor (gating); partner signing secret and specification not received (blocks interop, and possibly nothing else — §8).

Readiness for next phase: not ready. Nothing has been built, tested, reviewed, pushed, or deployed.

---

## 13. Immediate Next Action

```
Immediate Next Action:  Publish the repository to a remote the successor can read, pushing both
                        main and feat/signature-verify, and committing SESSION-NOTES.md and
                        docs/handoffs/ first so the context travels with the code. Then have the
                        successor clone it and confirm access in writing.
Responsible:            Outgoing developer, before the two-week absence begins. Nobody else can
                        do it — the only copy is on their machine.
Start From:             branch feat/signature-verify @ 7151400, in the project root.
Required Inputs:        A hosting destination and an access administrator — neither is decided
                        (§8). The successor's account identity.
Expected Deliverable:   A remote containing both branches, all handoff documents, and a
                        successor who has cloned it.
Acceptance Criteria:    The successor clones from the remote and sees 7151400 as the head of
                        feat/signature-verify, plus docs/handoffs/_master-handoff.md. Confirmed
                        by the successor, not assumed by the pusher.
Dependencies:           None technical. Only the hosting decision.
Stop Conditions:        Do not force-push, and do not rewrite the two existing commits — their
                        messages are the only inline record of intent on this work.
Do Not Change:          Nothing in src/ needs to change for this action. Leave feat/signature-verify
                        unmerged; it is not reviewed and it does not work.
```

**Prioritized queue after that:**

1. **Name an internal owner for the partner chase.** With the requester away and nobody assigned, the secret request stalls for two weeks by default. Follow-ups must reference the two prior requests (Daily §11) rather than starting cold, and should ask for the webhook specification and a sample signed request alongside the secret — not the secret alone.
2. **Stand up a minimal build and test toolchain.** Nothing can be validated without it, and it depends on no external party.
3. **Implement `verify()` in `src/verify.ts`** — HMAC-SHA256 over the raw body, with a timing-safe comparison. Unit-test it against a self-generated secret if §8 resolves that way. It is currently a `false` stub (§9), not the "probably correct" code the session notes describe.
4. **Build the transport layer in `src/relay.ts`**, capturing the raw body before any JSON parser (§10). Do not wire `verify()` into the relay path until item 3 is done — it fails closed.

---

## 14. New-Session Start Guide

1. **Read first:** this file, then `docs/handoffs/2026-07-30_001_signature-verify-handoff.md`, then `src/verify.ts` and `src/relay.ts` — both are short. `SESSION-NOTES.md` is worth reading for the partner-chase history, but read §9 above before trusting it on code state.
2. **Canonical source:** this file for project state; the repository itself outranks every document, including this one (§5).
3. **Current state:** two stubs, one blocked dependency, nothing built or tested, nothing pushed (§11).
4. **Start here:** §13.
5. **Final decisions:** §7 — HMAC-SHA256 over the raw body is the approach; the branch stays unmerged.
6. **Do not repeat:** do not re-derive the raw-body ordering constraint (§10, an afternoon already spent); do not cold-request the partner secret as a first ask (Daily §11); do not assume `src/verify.ts` is implemented (§9).
7. **Access required:** the partner's signing secret and webhook specification, from their integrations team — neither is held. Plus repository access once §13 is done.
8. **Requires explicit human approval:** no approval gates are configured anywhere in this project, and none are documented. Treat merges to `main`, any first deployment, and any handling of the partner secret as requiring a named human's sign-off until someone establishes an actual policy — this is a stated caution here, not an inherited rule.

---

## 15. Incorporated Daily Handoffs

| Date | Handoff File | Scope | Incorporated into Master |
|---|---|---|---|
| 2026-07-30 | `2026-07-30_001_signature-verify-handoff.md` | Signature verification; transfer to successor | Yes — Version 1.0 |
