# Master Handoff — webhook-relay

Project: webhook-relay
Document Type: Master Handoff
Version: 1.0
Last Updated: 2026-07-30
Current Phase: Early implementation — signature verification
Overall Status: Blocked
Canonical File: `docs/handoffs/_master-handoff.md`

This is the first Master for this project; there is no previous baseline to diff against.

---

## 1. Executive Summary

webhook-relay forwards partner webhooks into an internal event bus (`README.md`). The current and only active piece of work is verifying the signature on incoming partner webhooks before relaying them.

Progress so far: two commits, a relay skeleton on `main` and a signature-verification placeholder on `feat/signature-verify`. Nothing runs end to end, nothing is deployed, nothing is pushed anywhere.

Most important blocker: the partner's HMAC signing secret has never been received, so verification cannot be tested — and, separately, `src/verify.ts` does not yet contain an implementation to test (section 6).

Immediate next action: obtain the signing secret and a signed sample payload from the partner's integrations team (section 9).

The project's only contributor to date is away for two weeks from 2026-07-30 and is not reachable for questions.

---

## 2. Project Purpose and Definition

Problem: partner webhooks must be authenticated before their payloads are trusted and forwarded onward.

Objective: relay partner webhooks into the event bus, rejecting any request whose signature does not verify.

Current scope: HMAC-SHA256 signature verification of inbound partner webhooks.

Not verified: users, stakeholders, success criteria, deadlines, and explicit out-of-scope items are not recorded anywhere in the repository or the session record. A successor should establish these rather than assume them.

---

## 3. Repository and Project Structure

Repository: local Git repository only. **No remote is configured** — `main` and `feat/signature-verify` exist on one machine and nowhere else. Configuring a remote and pushing is an unowned risk (section 7).

Default branch: `main` (`00f7c89`). Note `init.defaultBranch` in this environment is `master`; the branch that actually exists and holds the skeleton is `main`.

Active branch: `feat/signature-verify` (`b8d285b`), branched from `main` at `00f7c89`, 1 ahead / 0 behind.

Branching model, protected branches, environments, ownership, review and release process: **not established.** Nothing in the repository defines them, and no CONTRIBUTING or CI configuration exists.

Key files: `src/relay.ts` (relay entry point, currently an empty function), `src/verify.ts` (signature verification, currently a placeholder), `docs/handoffs/` (this document and the dated Dailies).

---

## 4. Sources of Truth

| Source | Location | Purpose | Authority | Status |
|---|---|---|---|---|
| This document | `docs/handoffs/_master-handoff.md` | Canonical project state | Authoritative for current state | Current as of 2026-07-30 |
| Daily Handoffs | `docs/handoffs/YYYY-MM-DD_NNN_*.md` | Per-session detail and rationale | Authoritative for what happened in a session | See section 11 |
| Git history | `git log`, `git show <sha>` | What is actually committed | Authoritative over any prose, including this file | Current |
| Outgoing owner's raw notes | `SESSION-NOTES.md` (untracked, not in Git) | Origin of the 2026-07-30 handoff | Recollection, not evidence — see section 6 | Superseded by the Daily |
| Partner signing scheme | Not held. No partner documentation exists in the repository. | Would define the signature format | — | Missing |

Precedence: where the repository and any prose disagree, the repository wins. This is a rule applied by the 2026-07-30 handoff, not a policy anyone has ratified.

---

## 5. Decisions

**Final**

- **Capture the raw request body before any JSON body parser runs.** A parsed-and-re-serialized body no longer matches the bytes the partner signed, so the HMAC never matches. Binding on the HTTP layer, which does not exist yet. Date: 2026-07-30. Source: `2026-07-30_001_signature-verify-handoff.md`.
- **Do not redesign the verification approach, and do not delete the explanatory comments in `src/verify.ts`.** They are the only record of the decided approach. Date: 2026-07-30. Same source.

**Provisional**

- **HMAC-SHA256 over the raw body** is the verification scheme. Taken from the outgoing owner's account of the partner's scheme; no partner documentation was read and no test vector has ever been checked. It stays provisional until a signed sample payload verifies against it.

**Open**

- Decision needed: whether to write the HMAC implementation now, unverified, or wait for the secret. Why it matters: it decides whether the next two weeks produce anything. Required evidence: whether an implementation already exists uncommitted (only the outgoing owner can answer). Owner: Unassigned. Trigger: the secret arriving, or the owner returning circa 2026-08-13.
- Decision needed: whether `feat/signature-verify` should be pushed to a remote at all, and which. Owner: Unassigned.

---

## 6. Contradictions and Resolution

- Contradiction: `SESSION-NOTES.md` states HMAC-SHA256 verification was written and committed in `src/verify.ts`. The committed file is `export const verify = () => false;`, and `git show b8d285b` shows that commit changed only comments.
- Verified current state: no verification logic exists in the repository.
- Authoritative source: Git, over the note.
- Resolution: treat the implementation as **not written**. The instruction "don't rewrite `verify.ts`" is preserved as "don't redesign the approach or delete its comments" (section 5), not as "the code is done".
- Corrective action still required: confirm with the outgoing owner, on their return, whether an implementation exists uncommitted somewhere. Detail: `2026-07-30_001_signature-verify-handoff.md`.

---

## 7. Risks, Constraints, and Dependencies

**Active risks**

- All project history exists on a single machine with no remote. Loss of that machine loses everything. Owner: Unassigned. Unmitigated.
- The only contributor is unavailable until roughly 2026-08-13, and several facts — the partner contact route, the scope, the ownership model — exist only in that person's head.
- A successor may read "don't rewrite verify.ts" and idle for two weeks without noticing there is nothing to test. Mitigated only by section 6 of this document.

**Constraints**

- Raw body must be preserved before JSON parsing (section 5).
- No test infrastructure exists: no `package.json`, no test runner, no CI. Even once the secret arrives, a harness must be written before anything can be verified.

**External dependency (the blocker)**

- The partner's integrations team holds the signing secret. Two requests are unanswered; Dana, on the partner side, was chasing it as of 2026-07-30. Without the secret and a signed sample payload, verification is untestable. Chase history and what to send next: `2026-07-30_001_signature-verify-handoff.md`.

---

## 8. Current Technical State

Verified 2026-07-30 via `scripts/handoff_context.py` and direct `git` inspection.

Repository: local only, no remote
Default branch: `main` @ `00f7c89`
Active branch: `feat/signature-verify` @ `b8d285b`, 1 ahead of `main`
Uncommitted / unpushed: working tree clean apart from untracked `.claude/`, `SESSION-NOTES.md`, and `docs/handoffs/`. **Both branches are unpushed — there is nowhere to push to.**
Open PRs / open issues: **Not verified** — `gh` could not reach a repository. This is not a claim that none exist.
Build status: no build system exists
Test status: no tests exist and none were run
Migration / deployment / environment / CI status: none exist. Nothing has ever been deployed.

Current state of the work itself: `src/relay.ts` is `export const relay = () => {};`. `src/verify.ts` returns `false` unconditionally, under comments describing the intended HMAC-SHA256-over-raw-body scheme. Effectively, the relay currently rejects everything.

---

## 9. Immediate Next Action

Immediate Next Action: Obtain the partner's HMAC signing secret **and** one signed sample payload (raw body plus signature header) from the partner's integrations team, escalating past Dana, who has already been chasing it.

Responsible Role or Agent: Unassigned — no internal owner for the partner relationship is recorded anywhere. Identifying that person is part of this action.

Start From: Two prior requests, both undated and unanswered. Send a third with an explicit deadline and an internal escalation path.

Required Inputs: Dana's contact route and the partner escalation path — neither is recorded in the repository or the session notes, so both must be recovered from whoever owns the partner relationship.

Expected Deliverable: the secret, held outside version control, plus a sample payload usable as a test vector.

Acceptance Criteria: HMAC-SHA256 of the sample raw body under the received secret equals the signature the partner sent with it.

Stop Conditions: If the secret cannot be obtained, stop and escalate rather than inventing a test vector — a self-generated vector proves only that the code agrees with itself.

Do Not Change: the comments in `src/verify.ts`; the raw-body-before-parsing constraint.

**Prioritized queue after that:**

1. Confirm with the outgoing owner whether an HMAC implementation exists uncommitted (section 6). If not, write it.
2. Configure a remote and push `main` and `feat/signature-verify`. The work is currently one disk failure from gone.
3. Stand up minimal test infrastructure so the sample payload can actually be run against `verify`.
4. Wire raw-body capture into the request path in `src/relay.ts`, ahead of any body parser.

---

## 10. New-Session Start Guide

1. Read first: this file, then `docs/handoffs/2026-07-30_001_signature-verify-handoff.md`.
2. Canonical source: this file for state; Git for anything the prose and the code disagree about.
3. Current state: one placeholder commit on `feat/signature-verify`, blocked on an external secret, nothing pushed, nothing deployed, no tests.
4. Start here: section 9.
5. Final decisions: section 5 — raw body before parsing; do not redesign the verification approach.
6. Do not repeat: re-deriving the raw-body/JSON-parser failure (it cost an afternoon), re-designing the scheme, or sending a third unescalated request to the partner. Detail in the Daily's final section.
7. Access required: the partner's signing secret, and the contact route to reach the partner's integrations team. Neither is currently held.
8. Requires explicit human approval: nothing is defined. No branch protection, review requirement, or deploy gate exists in this repository — do not read that as permission to merge to `main`, push history, or deploy unilaterally. Establish the rule with a human before the first such action.

---

## 11. Incorporated Daily Handoffs

| Date | Handoff File | Scope | Incorporated into Master |
|---|---|---|---|
| 2026-07-30 | `2026-07-30_001_signature-verify-handoff.md` | Partner webhook signature verification | Yes — v1.0 |
