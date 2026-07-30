# Daily Handoff — orders-api — 2026-07-30

Project: orders-api (`package.json` name `orders-api`, version 0.4.1)
Date: 2026-07-30
Handoff ID: 2026-07-30_001_rate-limit
Session Scope: Per-API-key rate limiting — middleware, window config, pipeline wiring
Branch: `feat/rate-limit`
Prepared By: Claude Code session (`/handoff`), from SESSION-NOTES.md plus direct repository inspection
End-of-Session Status: Limiter is still a stub; approach decided; config staged but blocked on Priya; nothing tested; nothing pushed (no remote exists)

> No Master Handoff exists yet (`docs/handoffs/_master-handoff.md` — absent, this is the first
> handoff in the repo). Standing project context that would normally live there is therefore not
> available to point at; the risks and constraints below are recorded here for now and should be
> promoted to a Master on the first `/handoff full`.

---

## 1. Session Objective

**Intended objective:** Implement per-API-key rate limiting on `feat/rate-limit`.

**Actually completed:** The design decision (application middleware, not gateway/nginx), a
middleware file and its export surface, and a staged config module holding the window constant.

**Not completed:** The limiter itself. `rateLimit()` in `src/middleware/rate-limit.ts` is an empty
function body — the token-bucket algorithm described in the file's comment is not written. Burst
allowance not implemented. The middleware is not invoked anywhere. No tests exist or were run.

**Correction to the session record:** SESSION-NOTES.md states the token bucket was "built" and
"wired into the request pipeline". The repository does not support either claim, and the next
session should not assume them:

- `src/middleware/rate-limit.ts` (3 lines) contains two comments and `export const rateLimit = () => {};`.
- Commit `471c24e`, whose message is "feat: wire rate limiter into request pipeline", changed one
  file by one line — it added the `// TODO: burst allowance still unimplemented` comment to
  `src/middleware/rate-limit.ts`. It wires nothing.
- `src/server.ts` imports `rateLimit` but never calls it, and that import is uncommitted.

---

## 2. Completed Work

- **Action:** Created the rate-limit middleware module and its export.
  - Result: `export const rateLimit = () => {}` exists and is importable; the intended contract
    ("token bucket, 100 req/min per API key") is recorded as a comment on line 1.
  - Location: `src/middleware/rate-limit.ts`
  - Status: Committed on `feat/rate-limit` in `93d5bca` and `471c24e`. Not pushed — no remote exists.
  - Evidence: `git show --stat` on both commits; file read directly.

- **Action:** Chose the implementation site for the limiter (see section 3).
  - Result: nginx/gateway route closed off; application middleware confirmed.
  - Status: Final.
  - Evidence: SESSION-NOTES.md, this session.

---

## 3. Decisions Made

- **Decision:** The rate limiter lives in application middleware, not in nginx or the gateway.
  - Rationale: Limits are per API key. The API key is not visible to nginx without decrypting the
    request body, so the edge cannot make the decision.
  - Options considered: nginx config at the edge; gateway-level limiting; application middleware.
  - Rejected: nginx config (attempted this session, then abandoned); gateway (rejected for the same
    per-key-visibility reason, not attempted).
  - Expected impact: All limiter logic stays inside this service; the request pipeline in
    `src/server.ts` must invoke it. No edge configuration is required or wanted.
  - Status: Final.

- **Decision:** The rate-limit window constant lives in a dedicated config module rather than
  inline in the middleware.
  - Rationale: The window and the tier-dependent burst allowance need one home once Priya's answer
    lands.
  - Expected impact: `src/config/limits.ts` becomes the single place limit values are set.
  - Status: Provisional — the file is created and staged, but its value is not agreed (section 7).

---

## 4. What Changed

- Change: Added the `burst allowance still unimplemented` TODO to the middleware.
- Location: `src/middleware/rate-limit.ts` (line 2)
- Previous State: File as at `93d5bca` (comment + empty `rateLimit` export).
- New State: Same code, plus the TODO comment. Committed as `471c24e`.
- Reason: Mark the unimplemented burst path so it is not mistaken for done.
- Validation: Not validated — no test, build, or type-check was run.

- Change: New config module holding the rate-limit window.
- Location: `src/config/limits.ts` — `export const WINDOW_MS = 60_000;`
- Previous State: File did not exist.
- New State: Staged as a new file (`A src/config/limits.ts`), **not committed**.
- Reason: Give the window constant a home ahead of the tier/burst values.
- Validation: Not validated. The value is provisional — see section 7.

- Change: Import of the limiter added to the server entry point.
- Location: `src/server.ts` line 1 — `import { rateLimit } from './middleware/rate-limit';`
- Previous State: File as at `4da6436` — a single line, `export const start = ...`, no import.
- New State: Import present, **unstaged and uncommitted**. `rateLimit` is imported and never
  called, so the pipeline behaviour is unchanged.
- Reason: First step of wiring the middleware into the pipeline.
- Validation: Not validated. Note this import is currently unused and will trip a
  no-unused-imports lint rule if one is configured.

- Change: Untracked working files left in the tree — `SESSION-NOTES.md`, `notes/scratch.txt`,
  and `.claude/` (the skill and command definitions).
- Location: repository root
- Previous State: Not present in `4da6436`.
- New State: Untracked, uncommitted. `notes/scratch.txt` is a personal reminder ("burst allowance:
  ask Priya which tier gets it") and is not project material.
- Reason: Working artefacts of this session.
- Validation: N/A. There is no `.gitignore` in the repository, so these will all appear in any
  future `git add -A`.

No changes were made outside the repository this session: no dependencies, CI, environment
variables, secrets, migrations, infrastructure, access rules, or third-party settings were
touched.

---

## 5. Repository State at Session End

```
Branch:               feat/rate-limit
HEAD commit:          471c24e  "feat: wire rate limiter into request pipeline"
Uncommitted:          staged   — A src/config/limits.ts
                      unstaged — M src/server.ts
                      untracked — SESSION-NOTES.md, notes/, .claude/
                      (diff vs HEAD: 2 files changed, 2 insertions)
Stashes:              none
Upstream divergence:  no origin remote configured; branch has no upstream.
                      Every commit above exists only on this machine.
Open PR:              Not verified — `gh` could not reach a repository (none is configured).
Related issues:       Not verified — same reason.
```

Commits made on this branch today: `4da6436` (initial service skeleton), `93d5bca` (token-bucket
skeleton), `471c24e` (HEAD).

The uncommitted work above does not survive a branch switch and is invisible to anyone who clones
— and because there is no remote, a clone is not possible at all.

---

## 6. Validated or Approved Items

None. Nothing was tested, built, type-checked, reviewed, or approved this session — recorded
explicitly because the session's stated plan was "run the test suite next session, should be fine",
and that plan cannot be executed as written (see section 7).

---

## 7. Open, Uncertain, or Unverified Items

- **Which pricing tier gets a burst allowance** — Status: Waiting for Input (Priya)
  - Detail: The values in `src/config/limits.ts` are provisional and meaningless until this is
    answered. The burst allowance in `src/middleware/rate-limit.ts` cannot be implemented without it.
  - What would resolve it: Priya naming the tier(s) that get a burst allowance and its size.

- **Whether Priya has actually been asked** — Status: Needs Validation
  - Detail: The session record says "she hasn't answered yet", but contains no evidence that the
    question was sent. `notes/scratch.txt` reads as a reminder to ask, not a record of asking.
  - What would resolve it: Check the thread where she would have been asked before waiting on a
    reply. If it was never sent, sending it is the next action (section 10).

- **There is no test suite in this project** — Status: Blocked / Needs Validation
  - Detail: `package.json` has no `scripts` block, no dependencies and no devDependencies; there
    are no test files anywhere in the repository. "Run the test suite" is therefore not currently a
    runnable action, and the assumption that it "should be fine" has no basis.
  - What would resolve it: Decide whether to add a test runner and a first test for the limiter, or
    confirm tests live somewhere outside this repository.

- **`rateLimit()` is an empty stub** — Status: Open
  - Detail: The token-bucket logic in the file's comment ("100 req/min per API key") is not
    implemented. Nothing enforces any limit at runtime today.

- **The middleware is not invoked** — Status: Open
  - Detail: `src/server.ts` imports it but the request pipeline never calls it. "Wired in" is not
    true regardless of what commit `471c24e`'s message says.

- **Where the API key is read from** — Status: Open
  - Detail: The decision rests on the application being able to see the per-request API key, but
    nothing in the repository yet reads one. The mechanism (header? body? auth middleware?) is
    undetermined and is a prerequisite for the token bucket's key.

---

## 8. New Risks and Constraints

- Risk: All work on `feat/rate-limit` exists on one machine only — no remote is configured, so
  nothing is pushed or backed up, and the staged/unstaged work is not even committed.
  - Impact: Total loss of the session's work if the machine or working tree is lost.
  - Likelihood: Low per day, but unbounded while it persists.
  - Mitigation: Commit `src/config/limits.ts` and `src/server.ts` (or stash deliberately), then add
    a remote and push.
  - Owner: Unassigned — nobody was named this session.
  - Status: Open.

- Constraint (discovered this session): Rate limits are per API key, and nginx cannot see the API
  key without decrypting the request body. This rules out edge-level rate limiting for this
  service, permanently, not just for this implementation.
  - Status: Final constraint — see the rejected approach in section 12.

- Risk: The repository has no `.gitignore`, and `.claude/`, `SESSION-NOTES.md` and `notes/` are
  untracked in the root.
  - Impact: A routine `git add -A` commits personal scratch notes into project history.
  - Mitigation: Add a `.gitignore` covering `notes/` and `SESSION-NOTES.md` before the next
    broad `git add`; decide deliberately whether `.claude/` should be tracked.
  - Status: Open.

- Risk: Commit `471c24e`'s message ("wire rate limiter into request pipeline") describes work the
  commit does not contain.
  - Impact: Anyone reading `git log` will believe the pipeline is wired and skip the work.
  - Mitigation: Do not trust this branch's commit subjects; verify against the files. Consider a
    follow-up commit whose message corrects the record.
  - Status: Open.

---

## 9. Actual End-of-Session State

**Complete:** The decision on where the limiter lives, and the closing-off of the nginx approach.

**In progress:** The middleware module exists as an empty stub with its intended contract in a
comment; the config module exists with one provisional constant; the server-side import is added
but unused.

**Incomplete:** Token-bucket implementation; burst allowance; the actual call into the request
pipeline; any means of reading the API key; any test.

**Blocked:** Burst allowance and the final values in `src/config/limits.ts`, on Priya's answer
about which pricing tier gets a burst.

**Ready for review:** Nothing.

**Not ready for release/deployment:** Everything on this branch. No rate limiting is enforced at
runtime today — the exported middleware is a no-op, so a reader who sees "rate limiter" in the
commit log must not assume the service is protected.

No build or dev server is running; no rebase or merge is in progress; the working tree is clean of
conflicts.

---

## 10. Exact Next Action

```
Next Action:          Get Priya's answer on which pricing tier(s) get a burst allowance and how
                      large it is. First confirm whether she was actually asked — the session
                      record shows the question was noted, not sent — and send it if not.
Start From:           notes/scratch.txt holds the question verbatim ("burst allowance: ask Priya
                      which tier gets it"). The values it unblocks live in src/config/limits.ts.
Required Inputs:      A way to reach Priya. No ticket or thread for this question is recorded, and
                      none was verified.
Expected Output:      A written answer naming the tier(s) with a burst allowance and its size,
                      recorded in src/config/limits.ts alongside WINDOW_MS.
Acceptance Criteria:  src/config/limits.ts holds non-provisional values traceable to Priya's
                      answer, and the burst TODO on line 2 of src/middleware/rate-limit.ts can be
                      written against a specific number.
Do Not Change:        Do not move the limiter to nginx or the gateway — that is a settled decision
                      with a technical reason (section 3, section 12). Do not treat
                      src/config/limits.ts values as agreed before the answer arrives.
Blocking Conditions:  Priya's availability. If the answer will not arrive quickly, do not idle —
                      start the queue below, all of which is independent of her reply.
```

Because that action depends on another person, everything below is unblocked and can proceed in
parallel, in priority order:

1. Implement the token bucket body in `src/middleware/rate-limit.ts` — it is currently
   `() => {}`. Decide first how the per-request API key is read (section 7), since it is the
   bucket key.
2. Actually invoke the middleware in the request pipeline in `src/server.ts`; the import on line 1
   is currently unused.
3. Commit the staged `src/config/limits.ts` and the unstaged `src/server.ts` so the work survives
   a branch switch, and add a remote so it survives the machine.
4. Resolve the test question: add a runner and a first limiter test, or confirm tests live
   elsewhere. `package.json` currently defines no scripts at all.
5. Add a `.gitignore` before any `git add -A`, so `notes/` and `SESSION-NOTES.md` do not land in
   history.

---

## 11. Continuation Sources

| Source | Location / Identifier | Purpose |
|---|---|---|
| Branch | `feat/rate-limit` @ `471c24e` | All work in this thread; local only, no remote |
| Limiter | `src/middleware/rate-limit.ts` | The stub to implement; line 1 states the intended contract, line 2 the open TODO |
| Config | `src/config/limits.ts` | Window constant; staged, provisional values |
| Entry point | `src/server.ts` | Where the middleware must be invoked; line 1 has the unused import |
| Session record | `SESSION-NOTES.md` (untracked, repo root) | The raw session narrative this handoff was built from; see the correction in section 1 |
| Open question | `notes/scratch.txt` (untracked) | The question outstanding with Priya |
| Master Handoff | `docs/handoffs/_master-handoff.md` | Does not exist yet — create on the first `/handoff full` |

---

## 12. Work That Must Not Be Repeated

- **Implementing the limiter as nginx configuration** — Reason: attempted and abandoned this
  session. Limits must be applied per API key, and nginx cannot read the API key without
  decrypting the request body. The same reasoning rules out a gateway-level implementation. This is
  a property of the requirement, not of the attempt, so a second attempt will fail the same way.
- **Re-reading `git log` for the state of the wiring** — Reason: commit `471c24e` claims to wire
  the limiter into the request pipeline and does not; it adds a comment. Check the files.
