# Daily Handoff — webhook-relay — 2026-07-30

Project: webhook-relay (`g3-handover` working copy)
Date: 2026-07-30
Handoff ID: 2026-07-30_001_signature-verify
Session Scope: Partner webhook signature verification (`src/verify.ts`)
Branch: `feat/signature-verify` @ `b8d285b`
Prepared By: Claude Code (`project-relay-git` skill), from the outgoing owner's `SESSION-NOTES.md`. The owner is not named in the session record.
End-of-Session Status: Signature verification designed and committed as an intent-bearing placeholder, not a working implementation. Blocked on the partner's signing secret. Nothing pushed, no PR, nothing deployed. Owner away for two weeks from 2026-07-30.

Standing project context, risk register and project-level next action: `docs/handoffs/_master-handoff.md`.

---

## 1. Session Objective

**Intended objective:** Implement and test HMAC-SHA256 verification of partner webhook signatures over the raw request body.

**Actually completed:** The verification approach was decided and the raw-body ordering constraint was worked out. `src/verify.ts` was committed on `feat/signature-verify` at `b8d285b`.

**Not completed:** No verification logic actually runs. `src/verify.ts` is a placeholder returning `false` (see section 4 and section 7). Nothing was tested, and no test harness exists in the repository.

---

## 2. Completed Work

- **Action:** Committed the signature-verification intent and its blocker onto `feat/signature-verify`.
  - Result: Commit `b8d285b` "feat: HMAC signature verification, unverifiable without secret".
  - Location: `src/verify.ts`.
  - Status: Committed locally. Not pushed (no remote exists), no PR, not merged.
  - Evidence: `git show b8d285b` — a two-line comment change; `export const verify = () => false;` is unchanged from `00f7c89`.

- **Action:** Established the algorithm and the input the signature is computed over.
  - Result: HMAC-SHA256 over the **raw** request body. See section 3.
  - Status: Decided, unimplemented.

---

## 3. Decisions Made

- **Decision:** Verify partner webhooks with HMAC-SHA256 computed over the raw request body.
  - Rationale: Matches the partner's stated signing scheme, per the outgoing owner.
  - Options considered: Not recorded in the session.
  - Expected impact: Determines both the verification code and the request-handling order (see the next decision).
  - Status: Provisional — no partner-supplied test vector has ever been checked against it, because no secret has arrived.

- **Decision:** The raw request body must be captured *before* the JSON body parser runs.
  - Rationale: Once the body is parsed and re-serialized it no longer matches byte-for-byte, so the HMAC never matches. The outgoing owner lost an afternoon to this before identifying it.
  - Expected impact: Constrains how the HTTP layer is wired, not just `verify.ts`. Nothing in the repository implements this yet — `src/relay.ts` is `export const relay = () => {};` and there is no HTTP framework or body parser in the tree.
  - Status: Final as a constraint; unimplemented.

- **Decision:** Do not rewrite `src/verify.ts`; the approach is believed correct and is simply untestable until the secret arrives.
  - Rationale: The outgoing owner's explicit instruction, to stop a successor from burning the same afternoon re-deriving the approach.
  - Status: Final as an instruction, but read it together with section 7 — the file does not currently contain an implementation to preserve. What must be preserved is the **approach and the comments recording it**, not working code.

---

## 4. What Changed

- Change: Recorded the verification algorithm and its blocker in source comments.
- Location: `src/verify.ts`.
- Previous State: `// signature verification` + `export const verify = () => false;` at `00f7c89`.
- New State: `// signature verification — HMAC-SHA256 over the raw body` / `// blocked: needs the partner's signing secret` + the same unchanged `export const verify = () => false;`.
- Reason: Capture the decided approach and the reason work stopped.
- Validation: Not validated. No build, lint, or test was run this session, and the repository contains no `package.json`, test runner, or CI configuration to run one with.

- Change: New branch `feat/signature-verify` created off `main` at `00f7c89`.
- Location: Local repository only — there is no remote.
- Validation: Observed via `git branch` and `git merge-base main feat/signature-verify`.

Also on today's log but outside the session narrative: `00f7c89` "feat: webhook relay skeleton" (`README.md`, `src/relay.ts`, `src/verify.ts`), which is the current tip of `main`.

No changes to dependencies, CI, migrations, infrastructure, secrets, environment variables, access rules, or external tickets — none of these exist in the repository yet.

---

## 5. Repository State at Session End

Branch: `feat/signature-verify`
HEAD commit: `b8d285b` — "feat: HMAC signature verification, unverifiable without secret"
Uncommitted: staged 0, unstaged 0, untracked 2 — `.claude/` and `SESSION-NOTES.md`. (This handoff adds a third untracked path, `docs/handoffs/`.)
Stashes: none
Upstream divergence: **no remote and no upstream tracking branch.** Both `main` and `feat/signature-verify` exist only on this machine; a clone elsewhere would find nothing.
Open PR: **Not verified** — `gh` could not reach a repository, so no PR or issue state was observed. This is not the same as "none".
Related issues: Not verified, same reason.
`main`: `00f7c89`. `feat/signature-verify` is 1 commit ahead of `main` and 0 behind.

---

## 6. Open, Uncertain, or Unverified Items

- **Partner signing secret not received** — Status: Blocked.
  - Detail: Held by the partner's integrations team. Requested twice. Dana, on the partner side, said she would chase it. No further response recorded, and no date is recorded for either request.
  - What would resolve it: the secret itself, plus a signed sample payload to use as a test vector.

- **`src/verify.ts` contains no HMAC implementation** — Status: Needs Validation.
  - Evidence: `SESSION-NOTES.md` says HMAC-SHA256 verification "over the raw body" was written and committed. The committed file is `export const verify = () => false;` with two descriptive comments, and `git show b8d285b` shows that commit changed only comments. Either the implementation was never committed, or "wrote" described designing the approach rather than coding it.
  - Recorded as a contradiction with its resolution and the corrective action in `docs/handoffs/_master-handoff.md`.

- **Raw-body ordering constraint is unimplemented and unverified** — Status: Open.
  - Detail: No HTTP server, framework, or body parser exists in the tree, so the constraint currently binds future code rather than describing present code. It has never been demonstrated against a real signed request.

- **No tests were run and no test infrastructure exists** — Status: Open. Operationally significant: the successor cannot "just run the tests" once the secret arrives; a harness has to be built first.

- **Every claim in section 3 about the partner's signing scheme is second-hand**, taken from `SESSION-NOTES.md`. No partner documentation was read this session and none is referenced in the repository. Status: Waiting for Input.

---

## 7. New Risks and Constraints

- Risk: All work exists on one unpushed local machine with no remote configured, while the only person who knows the context is away for two weeks.
  - Impact: Total loss of `feat/signature-verify` and `main` if that machine is lost or wiped.
  - Mitigation: Configure a remote and push both branches before relying on the work. Not done this session.
  - Owner: Unassigned.
  - Status: Open.

- Constraint (discovered this session): raw request body must be preserved before JSON parsing — see section 3. Carried into the Master's standing register.

- Risk: The successor follows "don't rewrite `verify.ts`" literally and waits for the secret, without noticing there is no implementation to test.
  - Impact: Two weeks of no progress, then the real work starts.
  - Mitigation: This handoff; section 6 states the discrepancy explicitly.
  - Status: Open.

---

## 8. Actual End-of-Session State

**Complete:** The algorithm decision and the raw-body ordering constraint, both recorded.

**In progress:** `src/verify.ts` on `feat/signature-verify` — comments describing the intended verification, with a stub body.

**Incomplete:** The HMAC implementation itself; raw-body capture in the request path; any test.

**Blocked:** End-to-end verification, blocked on the partner signing secret and a signed sample payload.

**Ready for review:** Nothing. No PR exists and the branch is unpushed.

**Not ready for release/deployment:** Everything. Nothing has been deployed at any point.

---

## 9. Exact Next Action

Next Action: Obtain the partner's HMAC signing secret **and** one signed sample payload (raw body plus its signature header) from the partner's integrations team, escalating through Dana, who was already chasing it as of this session.

Start From: The two prior requests are unanswered and undated. Re-send with an explicit deadline, and ask a named internal owner to escalate if Dana does not respond — this handoff cannot name that internal owner, because the session never did.

Required Inputs: Dana's contact route (not recorded in the repository or session notes); the partner's integration documentation, if any exists.

Expected Output: The secret stored somewhere the project can use without committing it, and a sample payload usable as a test vector.

Acceptance Criteria: A recorded HMAC-SHA256 of the sample raw body under the received secret matches the signature the partner sent with it.

Do Not Change: Do not delete or rewrite the comments in `src/verify.ts` — they are the only record of the decided approach. Do not "fix" the JSON-parse ordering by parsing first; see section 3.

Blocking Conditions: Without the secret, nothing downstream can be validated. Writing the HMAC implementation is possible in the meantime, but it cannot be confirmed correct, so it stays unverified work.

---

## 10. Continuation Sources

| Source | Location / Identifier | Purpose |
|---|---|---|
| Verification code and its blocker comments | `src/verify.ts` on `feat/signature-verify` @ `b8d285b` | The file in flight |
| Request handler | `src/relay.ts` | Where raw-body capture must eventually be wired |
| Outgoing owner's raw notes | `SESSION-NOTES.md` (untracked) | The source this handoff was built from |
| Standing project state | `docs/handoffs/_master-handoff.md` | Project-level state, risks, and next action |

---

## 11. Work That Must Not Be Repeated

- **Re-deriving why HMAC comparison fails after JSON parsing.** It cost the outgoing owner an afternoon: the parser re-serializes the body, so the bytes no longer match what the partner signed. Capture the raw body first.
- **Re-designing the verification approach from scratch.** HMAC-SHA256 over the raw body is settled; the gap is the secret and the implementation, not the design.
- **Asking the partner's integrations team through the normal channel a third time without escalation.** Two requests have already gone unanswered.
