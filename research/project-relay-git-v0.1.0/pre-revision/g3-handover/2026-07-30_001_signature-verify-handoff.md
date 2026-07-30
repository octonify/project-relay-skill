# Daily Handoff — webhook-relay — 2026-07-30

Project: webhook-relay (`g3-handover`)
Date: 2026-07-30
Handoff ID: 2026-07-30_001_signature-verify
Session Scope: Partner webhook signature verification on `feat/signature-verify`
Branch: `feat/signature-verify`
Prepared By: Claude Code session, from `SESSION-NOTES.md`. The notes are unsigned — the outgoing
owner is not named in any source I read.
End-of-Session Status: One commit on an unpushed local branch; verification is untestable and, on
the evidence in the repository, not yet implemented (see section 6). Owner is away for two weeks
and the project is being taken over cold.

Standing project context: `docs/handoffs/_master-handoff.md`.

---

## 1. Session Objective

**Intended objective:** Implement HMAC-SHA256 signature verification of inbound partner webhooks,
computed over the raw request body, and hand the project to a successor.

**Actually completed:** Commit `009a397` on `feat/signature-verify`, which annotates
`src/verify.ts` with the intended scheme and the reason it is blocked. The raw-body ordering
constraint was worked out (section 8).

**Not completed:** No test or verification of the signature logic — the partner's signing secret
never arrived, so there is no secret and no test vector. No PR. Nothing deployed. See also the
discrepancy in section 6: the tracked code does not contain an HMAC implementation.

**Scope changes during session:** The session ended as a handover rather than as delivery, because
the owner is out for two weeks.

---

## 2. Completed Work

- **Action:** Committed the signature-verification work in progress.
  - Result: Commit `009a397` — *"feat: HMAC signature verification, unverifiable without secret"*.
  - Location: `src/verify.ts`, branch `feat/signature-verify`.
  - Status: Committed locally. **Not pushed** — there is no `origin` remote and no upstream
    tracking branch, so this commit exists on one machine only.
  - Evidence: `git log`, `git show 009a397`, `git remote -v` (no remotes) run this session.

- **Action:** Established the raw-body ordering constraint (section 8).
  - Result: A named constraint that must shape the relay's middleware order.
  - Location: Not yet expressed in code — `src/relay.ts` is still `export const relay = () => {};`.
  - Status: Understood and recorded; unimplemented.
  - Evidence: `SESSION-NOTES.md`; confirmed by reading `src/relay.ts` — no body-parser wiring exists.

---

## 3. Decisions Made

- **Decision:** Verify partner webhooks with HMAC-SHA256 computed over the **raw** request body.
  - Rationale: The partner signs the exact bytes they transmit. Any re-serialization of a parsed
    JSON body changes those bytes and the signature will never match.
  - Options considered: Not recorded in the session notes. Do not read this as "none were
    considered" — the alternatives simply were not written down.
  - Expected impact: Binds the relay's middleware order (section 8) and makes the partner's signing
    secret a hard prerequisite for any test.
  - Status: Final as the intended scheme; the implementation of it is unverified.

- **Decision:** Commit and hand over rather than block, and do not attempt to fake or stub around
  the missing secret.
  - Rationale: The code cannot be honestly validated without the real secret; a synthetic secret
    would prove only that the code agrees with itself.
  - Expected impact: The successor inherits unverified code, knowingly, rather than code with a
    false green signal.
  - Status: Final.

---

## 4. What Changed

- Change: Annotated the signature-verification stub with the intended scheme and its blocker.
- Location: `src/verify.ts` (commit `009a397`).
- Previous State: `470ca46` — file contained `// signature verification` plus
  `export const verify = () => false;`.
- New State: Comment expanded to `// signature verification — HMAC-SHA256 over the raw body` and
  `// blocked: needs the partner's signing secret`. **The exported function body is unchanged and
  still returns `false` unconditionally.**
- Reason: Record the intended design and the blocker at the site of the work.
- Validation: Not validated. Diff read this session via `git show 009a397`; no test exists to run.

Nothing changed outside the repository that I could observe: no environment variables, no CI
configuration, no secrets, no deployment, no third-party settings. The signing secret was
*requested* twice but never received, so nothing was rotated or installed.

---

## 5. Repository State at Session End

```
Branch:               feat/signature-verify
HEAD commit:          009a397 "feat: HMAC signature verification, unverifiable without secret"
Position vs main:     1 commit ahead of main (main is at 470ca46); no divergence
Uncommitted:          staged 0, unstaged 0
                      untracked 2 — .claude/ (skill install), SESSION-NOTES.md
Stashes:              none
Upstream divergence:  no origin remote configured; no upstream tracking branch
Open PR:              Not verified — gh could not reach a repository (no remote exists to host one)
Related issues:       Not verified — same reason
```

Two consequences worth stating plainly, because the successor is taking this over cold:

1. **There is nowhere to clone from.** All work — both commits — lives only in this working copy.
   Until a remote exists and the branch is pushed, a handover cannot actually complete.
2. `SESSION-NOTES.md` is untracked, so it would not survive a fresh clone either. Its content is
   preserved in this handoff.

---

## 6. Open, Uncertain, or Unverified Items

- **Item: The committed code does not contain an HMAC implementation.** — Status: Open, and the
  most important thing in this document.
  - Detail: `SESSION-NOTES.md` records "Wrote HMAC-SHA256 verification over the raw body in
    `src/verify.ts` and committed it on `feat/signature-verify`." The diff of `009a397` changes
    **comment lines only**. The current file, in full, is three lines: two comments and
    `export const verify = () => false;`. `git grep` across the HEAD tree finds no `createHmac`, no
    `crypto` import, and no raw-body handling anywhere. `verify()` currently rejects every request
    unconditionally.
  - What would resolve it: Ask the outgoing owner where the implementation is — an unpushed branch,
    another machine, an editor buffer, or a stash elsewhere. It is not in this working copy: the
    tree is clean and `git stash list` is empty. If it does not exist, the implementation is still
    to be written, and the estimate for the remaining work changes accordingly.
  - Note: this does not necessarily contradict the owner's "don't rewrite verify.ts" instruction —
    but that instruction cannot be followed literally against the file as it currently stands,
    because there is nothing there to preserve. Resolve this before deciding whether to write it.

- **Item: Signature verification is untested.** — Status: Blocked.
  - Detail: No signing secret and no test vector, so nothing can be exercised end to end.
  - What would resolve it: The partner's signing secret, plus at least one signed sample payload
    with its expected signature header.

- **Item: The partner's signing secret has not arrived.** — Status: Waiting for Input.
  - Detail: Held by the partner's integrations team. Requested twice. Dana, on the partner side,
    said she would chase it. No date, no ticket, and no internal owner for the chase was recorded.
  - What would resolve it: The secret itself, delivered through whatever secure channel the partner
    uses. Dana's contact details and the two prior requests are not in the repository — get them
    from the outgoing owner or from the partner thread before re-asking a third time.

- **Item: No build or test tooling exists in the repository.** — Status: Open.
  - Detail: Tracked files are only `README.md`, `src/relay.ts`, `src/verify.ts`. There is no
    `package.json`, no `tsconfig.json`, no test runner, no CI configuration. TypeScript sources
    exist with nothing configured to compile or run them. Stated because its absence is
    operationally significant: even with the secret in hand, there is currently no way to run a
    test.
  - What would resolve it: Adding the toolchain — which is unstarted work, not a regression.

- **Item: Build, test, and deployment status.** — Status: Needs Validation.
  - Detail: No build was run, no test was run, nothing was deployed this session. Reported as
    unknown rather than passing.

---

## 7. Actual End-of-Session State

**Complete:** Nothing is complete in a shippable sense.

**In progress:** Signature verification on `feat/signature-verify` — design settled, implementation
in the state described in section 6, validation blocked.

**Incomplete:** The raw-body preservation in `src/relay.ts` (still an empty stub). Any test
harness. Any toolchain.

**Blocked:** All validation of `verify()`, on the partner's signing secret.

**Ready for review:** Nothing. There is no PR, and no remote to open one against.

**Not ready for release/deployment:** Everything. Nothing is deployed and nothing should be —
`verify()` currently returns `false` for every request, which would reject all inbound webhooks.

---

## 8. New Risks and Constraints

- **Constraint: The raw request body must be captured before the JSON body parser runs.**
  - Impact: If the body is parsed first, the bytes the signature was computed over are gone and the
    signature will never match, no matter how correct the HMAC code is.
  - Discovered: This session, at a cost of roughly an afternoon.
  - Status: Active. Unimplemented — `src/relay.ts` has no middleware wiring at all yet.
  - This is the single most valuable thing in this handoff, because the failure mode it describes
    looks exactly like a bug in `verify()`. Anyone debugging a mismatched signature will suspect
    the HMAC code first and lose the same afternoon.

- **Risk: All work exists on one machine and is unpushed.**
  - Impact: Total loss of both commits if that machine is lost, and a successor cannot obtain the
    code at all in the meantime.
  - Likelihood: Low per day, but the owner is away for two weeks, so the exposure window is long.
  - Mitigation: Create a remote and push `feat/signature-verify`. See section 9.
  - Owner: Unassigned — no one has been named.
  - Status: Active.

- **Risk: The blocker has no internal owner or deadline.**
  - Impact: "Dana said she'd chase it" is the entire escalation path, and the person who was
    tracking it is away for two weeks. The default outcome is that nothing moves until they return.
  - Mitigation: Name an internal owner for the chase before the handover completes.
  - Status: Active.

---

## 9. Exact Next Action

Next Action: **Get the code somewhere the successor can reach it** — create a remote for this
repository and push both `main` and `feat/signature-verify` to it. Until this is done, no other
task in this handoff can be started by anyone but the current machine's owner, and the work is one
disk failure from gone.

```
Start From:           the repository root, on branch feat/signature-verify at 009a397
Required Inputs:      a remote the team can access, and permission to create it under the
                      organisation that should own webhook-relay — neither is recorded anywhere
                      I could read, so the successor must confirm both before creating anything
Expected Output:      git remote -v shows an origin; feat/signature-verify and main both exist on
                      the remote; git status reports an upstream for feat/signature-verify
Acceptance Criteria:  a second person can clone the repository and see commit 009a397
Do Not Change:        do not rewrite the two existing commits or force-push over them; the
                      outgoing owner's account of the work is anchored to 009a397 and section 6
                      still needs to be resolved against that exact commit
Blocking Conditions:  no remote has been provisioned, or nobody can say which organisation should
                      own the repository
```

**Then, in priority order:**

1. Resolve section 6 with the outgoing owner before they leave, if there is any window at all:
   *is there an HMAC implementation that never made it into `009a397`?* The answer determines
   whether the remaining work is "test it" or "write it", and it cannot be answered from the
   repository.
2. Take over chasing the signing secret. Name an internal owner and a date. The request has gone
   out twice already; a third identical ask from a new person is unlikely to move it — establish
   who at the partner can escalate past the integrations team's queue. Ask for a signed sample
   payload and its expected signature header at the same time, not just the secret.
3. Implement raw-body capture ahead of the JSON parser in `src/relay.ts` (section 8). This is
   independent of the secret and can proceed while it is outstanding.
4. Add a toolchain and a test that can be pointed at a real vector the moment the secret lands.

---

## 10. Continuation Sources

| Source | Location / Identifier | Purpose |
|---|---|---|
| Verification code | `src/verify.ts` @ `009a397` | The file this thread is about; see section 6 before editing |
| Relay entry point | `src/relay.ts` | Where raw-body capture must go; currently an empty stub |
| Work branch | `feat/signature-verify` (local only) | Contains all signature work |
| Baseline | `main` @ `470ca46` | The point this branch diverged from |
| Owner's notes | `SESSION-NOTES.md` (untracked) | Original account; content preserved here |
| Standing context | `docs/handoffs/_master-handoff.md` | Project-wide state and next action |

---

## 11. Work That Must Not Be Repeated

- **Do not re-derive the raw-body ordering constraint.** It is settled and recorded in section 8.
  It cost an afternoon once; the notes are explicit that it is real.
- **Do not rewrite `src/verify.ts` on the assumption it is wrong.** The outgoing owner's explicit
  instruction: *"don't rewrite verify.ts, it's probably correct, it's just untestable until the
  secret arrives."* Read section 6 first — the instruction and the file's observed contents do not
  line up, and that question must be settled before anyone concludes the code is broken.
- **Do not send a third identical request for the signing secret.** Two have already gone to the
  partner's integrations team. Escalate or change the ask; repeating it is the approach that has
  already failed twice.
- **Do not treat `verify()` returning `false` as a bug to patch out.** It rejects everything today.
  Making it return `true` to unblock local work would ship an unauthenticated webhook endpoint.
