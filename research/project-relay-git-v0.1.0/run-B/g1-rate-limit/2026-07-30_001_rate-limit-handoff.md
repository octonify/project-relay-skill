# Daily Handoff — orders-api — 2026-07-30

Project: orders-api (`package.json` v0.4.1) — internal orders service
Date: 2026-07-30
Handoff ID: 2026-07-30_001
Session Scope: Per-API-key rate limiting middleware
Branch: `feat/rate-limit`
Prepared By: Claude Code, from `SESSION-NOTES.md` plus repository state verified via
`.claude/skills/project-relay-git/scripts/handoff_context.py`
End-of-Session Status: Limiter file committed but its body is empty; `src/config/limits.ts`
staged with provisional values; `src/server.ts` import uncommitted and unused; nothing tested;
nothing pushed (no remote exists).

> No Master Handoff exists for this project yet. `docs/handoffs/_master-handoff.md` has not been
> created — run `/handoff master` to establish it. Until then this file is the only handoff
> record, so it carries a little standing context that would normally live in the Master.

---

## 1. Session Objective

**Intended objective:** Implement per-API-key rate limiting for the orders service.

**Actually completed:** Two commits on `feat/rate-limit` adding `src/middleware/rate-limit.ts`,
and one architectural decision (application middleware, not nginx or a gateway) with the
alternative closed off for a stated reason.

**Not completed:** Burst allowance (explicit `TODO` in the file); the limiter is not actually
invoked by the server; the window/limit constants are provisional pending Priya; no tests were
written or run.

**Scope changes during session:** Started as an nginx configuration task, moved to application
middleware once the per-key requirement was understood. See Decision D1.

---

## 2. Completed Work

- **Action:** Created the rate limiter module.
  - Result: `src/middleware/rate-limit.ts` exists on `feat/rate-limit`, declaring
    `export const rateLimit = () => {}` with a header comment stating the intended policy
    (token bucket, 100 req/min per API key) and a `TODO` for the burst allowance.
  - Location: `src/middleware/rate-limit.ts`; commits `453f6b2` ("feat: add token-bucket rate
    limiter skeleton") and `7f5bbb9` ("feat: wire rate limiter into request pipeline").
  - Status: Committed locally. Not pushed — the repository has no `origin` remote and
    `feat/rate-limit` has no upstream.
  - Evidence: `git show --stat` on both commits; file read directly.
  - **Caveat, read before building on this:** the function body is empty and nothing was in fact
    wired. See O1.

---

## 3. Decisions Made

- **D1 — Rate limiting is implemented as application middleware, not at the edge.**
  - Rationale: limits are per API key, and the key is not visible to nginx without decrypting
    the request body.
  - Options considered: nginx configuration (attempted first), an API gateway, application
    middleware.
  - Rejected: nginx and the gateway, both for the same reason — neither has the application
    context needed to identify the API key.
  - Expected impact: limiting runs in-process; capacity and per-instance state become an
    application concern rather than an infrastructure one.
  - Status: Final.

- **D2 — The rate-limit window constant lives in `src/config/limits.ts`.**
  - Rationale: keep the tunable value out of the middleware.
  - Current value: `WINDOW_MS = 60_000`.
  - Status: Provisional. The value is a placeholder and carries no agreed meaning until Priya
    confirms which pricing tier receives a burst allowance (Open Item O2). Do not treat the
    committed number as approved.

---

## 4. What Changed

- Change: Rate limiter module added.
  - Location: `src/middleware/rate-limit.ts`
  - Previous State: Did not exist before `453f6b2`.
  - New State: Three lines — policy comment, `TODO` for burst allowance, empty exported
    `rateLimit` function.
  - Reason: D1.
  - Validation: Not validated. No test runner exists in this project (see O4).

- Change: Configuration file for limit constants added.
  - Location: `src/config/limits.ts`
  - Previous State: Did not exist.
  - New State: `export const WINDOW_MS = 60_000;` — **staged, not committed**.
  - Reason: D2.
  - Validation: Not validated; value is provisional (O2).

- Change: Import of the limiter added to the server entry point.
  - Location: `src/server.ts`
  - Previous State: `export const start = () => console.log('up');` at commit `7f5bbb9`.
  - New State: Same, plus `import { rateLimit } from './middleware/rate-limit';` —
    **unstaged, not committed**. The import is unused; nothing calls `rateLimit`.
  - Reason: First step of wiring, left unfinished.
  - Validation: Not validated. Depending on lint/TS settings this unused import may fail a
    build; no build was run this session.

- Change: Personal reminder file left in the working tree.
  - Location: `notes/scratch.txt` — one line, "burst allowance: ask Priya which tier gets it".
  - New State: Untracked, deliberately left by the repository owner. Not a project document;
    do not commit or delete it.

No CI, environment variable, secret, dependency, migration, deployment, or access/permission
changes were made or observed this session. `package.json` was not modified.

Note on untracked noise: the repository has **no `.gitignore`**, so `.claude/`,
`SESSION-NOTES.md` and `notes/` all appear as untracked changes. That is expected, not
work-in-progress.

---

## 5. Repository State at Session End

```
Branch:               feat/rate-limit
HEAD commit:          7f5bbb9  "feat: wire rate limiter into request pipeline"
Uncommitted:          staged   — A  src/config/limits.ts
                      unstaged — M  src/server.ts
                      untracked — .claude/, SESSION-NOTES.md, notes/
                      (diff vs HEAD: 2 files changed, 2 insertions)
Stashes:              none
Upstream divergence:  no origin remote configured; no upstream tracking branch.
                      This work exists on one machine only and is invisible to any clone.
Open PR:              Not verified — `gh` could not reach a repository (none is configured).
Related issues:       Not verified — same reason.
Commits today:        7f5bbb9, 453f6b2, 260de56 ("chore: initial service skeleton")
```

---

## 6. Validated or Approved Items

None. Nothing was tested, built, reviewed, or approved this session.

This absence is operationally significant: `SESSION-NOTES.md` ends with "I'll run the test suite
next session. Should be fine." There is no test suite to run — see O4 — so that expectation is
unfounded and the limiter has never been executed.

---

## 7. Open, Uncertain, or Unverified Items

- **O1 — The limiter is neither implemented nor wired, despite the session notes and the commit
  message.** — Status: Open
  - Detail: `SESSION-NOTES.md` says the token bucket was "built" and "wired into the request
    pipeline". Observed: `rateLimit` has an empty body, commit `7f5bbb9` changed only
    `src/middleware/rate-limit.ts`, and the only link to the server is an unused import sitting
    uncommitted in `src/server.ts`. Both sources are recorded here; the repository is the
    stronger evidence.
  - What would resolve it: implementing the bucket in `src/middleware/rate-limit.ts` and calling
    `rateLimit()` from `start()` in `src/server.ts`, then observing a request being limited.

- **O2 — Which pricing tier receives a burst allowance is unanswered by Priya.** — Status:
  Blocked / Waiting for Input
  - Detail: asked this session, no reply. Blocks the burst allowance implementation (the `TODO`
    in `src/middleware/rate-limit.ts`) and makes the staged value in `src/config/limits.ts`
    meaningless until confirmed.
  - What would resolve it: Priya naming the tier(s) and the burst size. See Next Action.

- **O3 — Burst allowance unimplemented.** — Status: Blocked on O2. Marked by a `TODO` in
  `src/middleware/rate-limit.ts`.

- **O4 — There is no test suite, and no test runner is configured.** — Status: Needs Validation
  - Detail: `package.json` contains only `name` and `version` — no `scripts`, no dependencies.
    No test or spec files exist anywhere in the tree, and `node_modules/` is absent. Verified by
    reading `package.json` and searching the working tree.
  - What would resolve it: adding a test runner and a `test` script, or confirming that tests
    live in a system outside this repository.

- **O5 — `src/config/limits.ts` is staged but uncommitted, and `src/server.ts` is modified but
  unstaged.** — Status: Open. Neither survives a branch switch, and neither is visible to anyone
  else. Committing `limits.ts` before O2 resolves would publish a provisional number as if it
  were settled.

---

## 8. New Risks and Constraints

- Risk: All rate-limit work exists only in this working copy.
  - Impact: total loss of the session's work if the machine or directory is lost; no one else can
    review or continue it.
  - Likelihood: Low per day, but permanent while it holds.
  - Mitigation: configure a remote and push `feat/rate-limit`, or accept it explicitly.
  - Owner: repository owner.
  - Status: Open.

- Constraint (discovered this session): per-API-key limiting cannot be done at the edge, because
  the key is only readable after body decryption. This is the binding reason behind D1 and it
  rules out any future "just do it in nginx" simplification.

---

## 9. Actual End-of-Session State

**Complete:** Decision D1, and the closing-off of the nginx and gateway approaches.

**In progress:** `src/middleware/rate-limit.ts` — file and policy comment exist, implementation
does not. `src/server.ts` — import added, call site missing.

**Incomplete:** Burst allowance; wiring; any form of testing.

**Blocked:** Burst allowance and the final values in `src/config/limits.ts`, both on Priya (O2).

**Ready for review:** Nothing.

**Not ready for release/deployment:** Everything. The service currently imports a limiter that
does nothing and is never invoked, so requests are unlimited — no behaviour has changed in the
running service, which is the safe failure mode but not the intended one.

---

## 10. Exact Next Action

```
Next Action:          Get Priya's answer on which pricing tier(s) receive a burst allowance,
                      and the burst size for each. Ask explicitly and record the reply in
                      this file's O2 or in tomorrow's Daily.
Start From:           Whatever channel the original ask went out on (not recorded in
                      SESSION-NOTES.md — check your own sent messages first, do not re-ask
                      in a new place and split the thread).
Required Inputs:      None. This action is startable immediately.
Expected Output:      A named tier list plus burst size, written down in the repository.
Acceptance Criteria:  O2 can be marked resolved with Priya's answer quoted, and
                      src/config/limits.ts values can be set to agreed numbers rather than
                      placeholders.
Do Not Change:        Do not commit src/config/limits.ts with WINDOW_MS = 60_000 as if
                      approved (D2 is Provisional). Do not delete notes/scratch.txt — it is
                      the owner's own reminder. Do not revisit the edge/nginx approach
                      (section 12).
Blocking Conditions:  None to send the ask. The downstream work in queue items 2 and 3 stays
                      blocked until Priya replies.
```

The ask is asynchronous, so send it first and then work the queue below while waiting.

**Prioritized queue after that:**

1. Implement the token bucket body in `src/middleware/rate-limit.ts` (100 req/min per API key,
   per the file's own comment) and call `rateLimit()` from `start()` in `src/server.ts`. This is
   not blocked by O2 — only the burst allowance is. Resolves O1 and clears the unused import.
2. Once Priya replies: implement the burst allowance (removes the `TODO`), set the real values
   in `src/config/limits.ts`, and commit it. Resolves O2, O3, O5.
3. Decide what "run the test suite" means here — add a runner and a `test` script to
   `package.json`, or point at wherever tests actually live. Resolves O4. Until this exists, no
   claim about the limiter working can be validated.
4. Configure a remote and push `feat/rate-limit`, or record a decision that this stays local.

---

## 11. Continuation Sources

| Source | Location / Identifier | Purpose |
|---|---|---|
| Branch | `feat/rate-limit` @ `7f5bbb9` | All session work; local only, no upstream |
| Limiter module | `src/middleware/rate-limit.ts` | Policy comment, `TODO`, empty `rateLimit` |
| Limit constants | `src/config/limits.ts` (staged) | `WINDOW_MS`; values provisional per D2 |
| Server entry | `src/server.ts` (unstaged) | Unused import; call site to add |
| Session record | `SESSION-NOTES.md` (untracked) | The raw session account this handoff verifies against |
| Owner's reminder | `notes/scratch.txt` (untracked) | The Priya question, as originally noted |

---

## 12. Work That Must Not Be Repeated

- **Do not re-attempt rate limiting as nginx configuration.** — Reason: limits are per API key,
  and nginx cannot read the API key without decrypting the request body. Tried and dropped this
  session. The same reasoning rules out an API gateway (D1).
- **Do not read the commit log as evidence that limiting works.** — Reason: `7f5bbb9`'s message
  overstates what it did (O1).
