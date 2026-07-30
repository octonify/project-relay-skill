# Daily Handoff — orders-api — 2026-07-30

Project: orders-api (`package.json` v0.4.1)
Date: 2026-07-30
Handoff ID: 2026-07-30_001_rate-limit-handoff
Session Scope: Per-API-key rate limiting — approach decision and first middleware commits
Branch: `feat/rate-limit`
Prepared By: Claude Code session agent, from `SESSION-NOTES.md` plus repository inspection
End-of-Session Status: Approach decided and committed as a stub; limiter body not implemented, nothing called at runtime, no tests run, config values blocked on Priya, nothing pushed anywhere.

---

## 1. Session Objective

**Intended objective:** Implement per-API-key rate limiting for orders-api.

**Actually completed:** Chose the implementation approach (application middleware, not nginx/gateway) and committed a placeholder module at `src/middleware/rate-limit.ts`. Began the config module `src/config/limits.ts`.

**Not completed:** The token-bucket algorithm itself, the burst allowance, calling the limiter from the request pipeline, and any testing.

**Scope note — read this before trusting the commit log:** commit messages `feat: add token-bucket rate limiter skeleton` and `feat: wire rate limiter into request pipeline`, and the session notes phrase "built the token bucket … and wired it into the request pipeline", overstate what exists. Verified contents of `src/middleware/rate-limit.ts` at `b4897b3`:

```ts
// token bucket, 100 req/min per API key
// TODO: burst allowance still unimplemented
export const rateLimit = () => {};
```

That is an empty function and two comments. No bucket, no counters, no storage. And "wired into the request pipeline" is not true in any commit: `b4897b3` touched only `src/middleware/rate-limit.ts` (it added the TODO comment). The only wiring that exists is an unstaged `import` line in `src/server.ts`, and nothing calls `rateLimit()`. Treat the whole feature as not started in behaviour, only in structure.

---

## 2. Completed Work

- **Action:** Created the rate-limit middleware module as a stub.
  - Result: `src/middleware/rate-limit.ts` exists on `feat/rate-limit` exporting `rateLimit = () => {}`, with the intended spec recorded in a comment as "token bucket, 100 req/min per API key".
  - Location: `src/middleware/rate-limit.ts`; commits `c4f971a` (file created, 2 lines) and `b4897b3` (TODO comment, 1 line).
  - Status: Committed locally. Not pushed — see section 5.
  - Evidence: `git show c4f971a`, `git show b4897b3`, file read.

- **Action:** Recorded the approach decision (section 3).
  - Result: nginx/gateway route closed off; middleware route adopted.
  - Status: Final, and the only durable output of the session.
  - Evidence: `SESSION-NOTES.md`.

Nothing else reached a finished state.

---

## 3. Decisions Made

- **Decision:** The rate limiter lives in application middleware.
  - Rationale: limits are per API key, and the key is not visible outside the application — nginx would have to decrypt the request body to see it.
  - Options considered: nginx configuration (attempted first); an API gateway; application middleware.
  - Rejected: nginx config, and the gateway, both for the same reason — no access to the API key.
  - Expected impact: rate-limit state and configuration stay inside the service; `src/middleware/rate-limit.ts` is the single home for the algorithm.
  - Status: Final.

- **Decision:** The rate-limit window constant lives in `src/config/limits.ts` rather than inline in the middleware.
  - Rationale: the tier-dependent values need one place to change once Priya answers.
  - Expected impact: the middleware will import from config rather than hard-code numbers.
  - Status: Provisional — the file's current value is a placeholder, see section 7.

---

## 4. What Changed

- Change: Rate-limit middleware module created (stub only).
- Location: `src/middleware/rate-limit.ts`
- Previous State: File did not exist before `c4f971a`.
- New State: 3 lines — spec comment, TODO comment, empty exported `rateLimit` function.
- Reason: Landing the agreed middleware approach as a placeholder.
- Validation: Not validated. Not executed, not tested, not called.

- Change: Config module created, holding the rate-limit window.
- Location: `src/config/limits.ts` — `export const WINDOW_MS = 60_000;`
- Previous State: File did not exist.
- New State: Staged, not committed.
- Reason: Somewhere to hold window/tier constants.
- Validation: Not validated, and the value is provisional — see section 7.

- Change: Import of the limiter added to the server entrypoint.
- Location: `src/server.ts` line 1 — `import { rateLimit } from './middleware/rate-limit';`
- Previous State: Single-line file as committed at `4c32a44`.
- New State: Unstaged working-tree edit. The import is unused; `start()` does not call `rateLimit()`.
- Reason: First step toward wiring; not finished.
- Validation: Not validated. An unused import may fail lint or a `noUnusedLocals` TypeScript build — no build or lint was run this session, so this is unverified either way.

No changes to dependencies, CI, environment variables, secrets, migrations, access rules, or external services. No issues or PRs were opened or touched.

---

## 5. Repository State at Session End

```
Branch:               feat/rate-limit
HEAD commit:          b4897b3  "feat: wire rate limiter into request pipeline"
Uncommitted:          staged   — A src/config/limits.ts
                      unstaged — M src/server.ts
                      untracked — .claude/, notes/, SESSION-NOTES.md
Stashes:              none
Upstream divergence:  none possible — no `origin` remote is configured and the branch has
                      no upstream. All three commits and all uncommitted work exist only on
                      this machine. Nothing is backed up or visible to anyone else.
Open PR:              Not verified — `gh` could not reach a repository.
Related issues:       Not verified — same reason.
```

Source: `.claude/skills/project-relay-git/scripts/handoff_context.py`, confirmed with `git status`, `git diff`, `git stash list`.

Untracked paths are untracked because the repository has no `.gitignore`. `notes/scratch.txt` is a personal reminder ("burst allowance: ask Priya which tier gets it"), not project material — it duplicates section 7 and can be deleted once Priya answers.

---

## 6. Validated or Approved Items

None. Stated explicitly because it changes what tomorrow must do: no test was run, no build was run, no lint was run, and no human approved anything. Every claim about the limiter working is expectation, not evidence.

The session note "I'll run the test suite next session. Should be fine." is not actionable as written — **there is no test suite**. `package.json` contains only `name` and `version`: no `scripts` block, no dependencies, no test runner. `git ls-files` lists five tracked files and no test file. `node_modules/` does not exist. Standing up a test setup is itself unscoped work, not a command to run.

---

## 7. Open, Uncertain, or Unverified Items

- **Which pricing tier gets a burst allowance** — Status: Blocked / Waiting for Input
  - Detail: Priya was asked during the session and has not answered. Until she does, the burst allowance cannot be implemented, and the values in `src/config/limits.ts` are placeholders that mean nothing. `WINDOW_MS = 60_000` was chosen as a plausible default, not as a confirmed requirement.
  - What would resolve it: Priya naming the tier(s) that receive a burst allowance and its size.
  - Note: no channel, thread, or date for the original ask was recorded, so tomorrow may have to re-ask rather than follow up.

- **Burst allowance unimplemented** — Status: Blocked (on the item above)
  - Detail: `TODO: burst allowance still unimplemented` in `src/middleware/rate-limit.ts`.

- **Token-bucket algorithm unimplemented** — Status: Open, not blocked
  - Detail: `rateLimit()` is an empty function. The non-burst path (100 req/min per API key, fixed window from `WINDOW_MS`) does not depend on Priya's answer and can be written now.

- **Limiter not invoked** — Status: Open
  - Detail: `src/server.ts` imports `rateLimit` but never calls it. Even a complete implementation would have zero runtime effect today.

- **No test suite exists** — Status: Open, needs a decision
  - Detail: See section 6. Someone has to decide on a runner and add it before "run the tests" is a real instruction.

- **Whether the unused import breaks build or lint** — Status: Needs Validation
  - Detail: Nothing was compiled this session; there is no `tsconfig.json` in the repository either.

---

## 8. New Risks and Constraints

- Risk: All work — 3 commits plus uncommitted changes — exists on one machine with no remote configured.
  - Impact: Total loss of the session's work if the machine is lost. Also invisible to Priya or any reviewer, so no one can act on it.
  - Likelihood: Low per day, but the exposure grows every session it stays unpushed.
  - Mitigation: Add a remote and push `feat/rate-limit`.
  - Owner: Unassigned — nobody was named.
  - Status: Open.

- Constraint (discovered this session): Per-key rate limiting cannot be done at the edge. nginx and an API gateway both sit outside the boundary where the API key is readable. This constrains any future "move it to the edge for performance" suggestion.
  - Status: Standing. See section 3 for the reasoning and section 12.

---

## 9. Actual End-of-Session State

**Complete:** The approach decision. Nothing else.

**In progress:** `src/middleware/rate-limit.ts` — stub committed, algorithm not written. `src/config/limits.ts` — staged, values provisional. `src/server.ts` — import added, call not added, edit uncommitted.

**Incomplete:** Token-bucket implementation, invocation from the request pipeline, tests of any kind.

**Blocked:** Burst allowance and the final values in `src/config/limits.ts`, both on Priya.

**Ready for review:** Nothing. No PR exists and there is no remote to open one against.

**Not ready for release/deployment:** The entire feature. `rateLimit()` is a no-op — deploying today would ship a rate limiter that limits nothing while the commit log claims otherwise.

Working tree is not mid-rebase, mid-merge, or mid-conflict; it compiles as far as anyone knows, but nobody checked. No dev server was left running.

---

## 10. Exact Next Action

```
Next Action:          Implement the non-burst token-bucket body in `rateLimit()` — per-API-key
                      bucket, 100 requests per WINDOW_MS, importing WINDOW_MS from
                      `src/config/limits.ts` — then call it from `src/server.ts` so the
                      existing import is actually used.
Start From:           branch `feat/rate-limit` at `b4897b3`;
                      `src/middleware/rate-limit.ts` line 3 (`export const rateLimit = () => {};`)
Required Inputs:      None. The spec for the non-burst path is already fixed in the file's own
                      comment (100 req/min per API key). Priya's answer is NOT required for this
                      — it governs only the burst allowance.
Expected Output:      A `rateLimit` middleware that tracks a bucket per API key and rejects over
                      quota, invoked from the server entrypoint; the `src/server.ts` import no
                      longer unused.
Acceptance Criteria:  Requests beyond 100 in a WINDOW_MS window for one API key are rejected;
                      a different key is unaffected. Verify by executing it, not by reading it —
                      if no test runner is added, a throwaway script driving the function
                      directly is acceptable, but record what you actually ran.
Do Not Change:        - Do not move the limiter to nginx or a gateway (section 12).
                      - Do not treat `WINDOW_MS = 60_000` as confirmed; it is a placeholder.
                      - Do not delete the `TODO: burst allowance` comment until Priya answers.
                      - Do not commit `notes/`, `.claude/`, or `SESSION-NOTES.md`.
Blocking Conditions:  None for this action.
```

**Then, in priority order:**

1. Re-ask Priya which pricing tier gets a burst allowance and how large it is — blocking two items, and no record exists of when or where she was first asked, so treat it as a fresh ask and note the channel this time.
2. Configure a remote and push `feat/rate-limit` — the work is single-copy today (section 8).
3. Decide on a test runner and add it to `package.json`, so "run the tests" becomes a real command.
4. Implement the burst allowance once (1) returns.
5. Consider amending or annotating the misleading commit subjects `c4f971a` / `b4897b3` before this branch is ever shared — safe to rewrite now only because nothing is pushed.

---

## 11. Continuation Sources

| Source | Location / Identifier | Purpose |
|---|---|---|
| Limiter implementation | `src/middleware/rate-limit.ts` | The stub to fill in; its comments hold the intended spec |
| Rate-limit config | `src/config/limits.ts` | Provisional `WINDOW_MS`; staged, uncommitted |
| Server entrypoint | `src/server.ts` | Holds the unused, uncommitted import |
| Branch | `feat/rate-limit` @ `b4897b3` | All work; local only, no remote |
| Raw session notes | `SESSION-NOTES.md` (untracked) | The unedited account this handoff was built from |
| Priya | Named in `SESSION-NOTES.md`; no channel recorded | Owner of the burst-allowance answer |

No Master Handoff exists yet (`docs/handoffs/_master-handoff.md` is absent), so there is no standing project context to point at. If this project is handed to someone else, run `/handoff full` to create one.

---

## 12. Work That Must Not Be Repeated

- **Do not implement rate limiting as nginx configuration.** Tried this session and abandoned: limits are per API key, and nginx cannot read the key without decrypting the request body. The same objection rules out an API gateway. This is the default idea a fresh contributor will reach for, so it is closed on purpose, not by oversight.

- **Do not re-derive the middleware decision.** Settled with rationale in section 3; status Final.

- **Do not read the commit subjects as a statement of what works.** `c4f971a` and `b4897b3` describe a token bucket and pipeline wiring that do not exist in the code (section 1). Anyone auditing this branch should check the file, not the log.
