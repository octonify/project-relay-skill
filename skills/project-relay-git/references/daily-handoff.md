# Daily Handoff — section reference

Contents:
1. [Handoff Metadata](#1-handoff-metadata)
2. [Session Objective](#2-session-objective)
3. [Completed Work](#3-completed-work)
4. [Decisions Made](#4-decisions-made)
5. [What Changed](#5-what-changed)
6. [Repository State at Session End](#6-repository-state-at-session-end)
7. [Validated or Approved Items](#7-validated-or-approved-items)
8. [Open, Uncertain, or Unverified Items](#8-open-uncertain-or-unverified-items)
9. [New Risks and Constraints](#9-new-risks-and-constraints)
10. [Actual End-of-Session State](#10-actual-end-of-session-state)
11. [Exact Next Action](#11-exact-next-action)
12. [Continuation Sources](#12-continuation-sources)
13. [Work That Must Not Be Repeated](#13-work-that-must-not-be-repeated)

A Daily Handoff answers one question: *what happened this session, why, what changed in the
repository and around it, what was validated, what is still unresolved, and what must happen
next?*

Cover the session scope only. Standing project context — purpose, architecture, the full risk
register, project-wide sources of truth — lives in the Master. Point at it rather than restating
it: `Project constraints: docs/handoffs/_master-handoff.md`. A Daily that drifts into background
buries the operational detail the next session actually needs.

**This list is a menu, not a checklist.** Delete any section you have nothing real to put in,
heading and all. A quiet session produces a short Daily, and that is a correct outcome rather
than a lazy one — the reader's attention is the scarce resource you're spending.

The one exception: state an absence when the absence is itself operationally significant. "No
tests were run this session" changes what tomorrow must do. "No migrations" on a docs-only
change does not.

---

## 1. Handoff Metadata

```markdown
Project:
Date:
Handoff ID:
Session Scope:
Branch:
Prepared By:
End-of-Session Status:
```

Session Scope is a phrase, not a paragraph — the reader uses it to decide whether this file is
relevant to them. End-of-Session Status is a short verdict (`Login form working, tests not
written, nothing committed`), not a mood.

## 2. Session Objective

Separate four things that are easy to blur together:

- The intended objective
- What was actually completed
- What was not completed
- Scope changes that happened mid-session

The gap between intent and outcome is information, not an admission. Someone planning the next
session needs to know the work was larger than expected.

## 3. Completed Work

Only work that is actually finished. Per item, where relevant:

- Action completed
- Result
- Location or affected scope — exact paths, commits
- Final status
- Supporting evidence or reference

Planned work never appears here. If something is 90% done, it goes in section 10 (end state) with
the remaining 10% named. Written, committed, pushed, and merged are four different states; say
which one you reached.

## 4. Decisions Made

Every meaningful decision, with its reasoning — the reasoning is what stops the decision being
reversed by accident later. This is the decision's **primary home**; the Master carries only the
decision and its status, pointing back here.

- Decision
- Rationale
- Options considered
- Rejected option
- Expected impact
- Status: `Final` / `Provisional` / `Pending Approval` / `Superseded`

Keep decisions separate from the actions that implemented them. A decision outlives its first
implementation, and conflating them makes it look like changing the code changes the decision.

## 5. What Changed

The factual record of everything that moved. Use `change-categories.md` as a recall checklist so
you don't default to only code and files — CI settings, environment variables, secrets,
migrations, and access rules are just as real and get forgotten most often.

Record each change once, here. If a change also drives a risk or an open item, cross-reference it
rather than restating the whole thing — duplicated detail is how two copies of a fact drift apart
and start contradicting each other.

Per important change:

```markdown
- Change:
- Location:            src/auth/session.ts, migrations/003_tokens.sql
- Previous State:
- New State:
- Reason:
- Validation:
```

When the previous state is unknown, write `Unknown` and why. A guessed previous state is actively
dangerous — someone will use it to "restore" the wrong thing. For tracked files the previous
state is usually recoverable: name the commit it was last good at.

## 6. Repository State at Session End

A snapshot taken from `scripts/handoff_context.py` rather than from memory. This section decides
whether tomorrow starts with five minutes of orientation or forty of archaeology.

```markdown
Branch:
HEAD commit:
Uncommitted:          staged / unstaged / untracked, with paths
Stashes:
Upstream divergence:  ahead N, behind M — or "no upstream"
Open PR:
Related issues:
```

State only what you saw. If uncommitted work exists, say so explicitly — it does not survive a
branch switch and it is invisible to anyone who clones. If the branch has no upstream, say that
too: the work exists on exactly one machine. If `gh` was unavailable, record PR and issue state
as `Not verified`, never as "none".

## 7. Validated or Approved Items

Only items confirmed by evidence, testing, observation, or human approval.

```markdown
- Item:
- Validation Method:
- Evidence:
- Result:
```

Statuses that fit here: Tested, Reviewed, Approved, Merged, Verified, Deployed, Build Passed,
Migration Applied.

Expected or assumed outcomes do not belong in this section, however confident you feel. This is
the section a reader trusts without checking, which is exactly why it must stay clean. "The build
should pass now" belongs in section 8.

## 8. Open, Uncertain, or Unverified Items

Open decisions, unanswered questions, assumptions you made, tests not run, contradictions
noticed, missing data, pending approvals and reviews, dependencies, blockers, things needing
investigation.

Statuses: `Open` / `Blocked` / `Waiting for Input` / `Waiting for Approval` / `Needs Validation`
/ `Deferred` / `Out of Scope`.

Be generous here. An item listed as unverified costs the next session five minutes to check; an
item wrongly implied as solid can cost a day.

## 9. New Risks and Constraints

Only risks and constraints **discovered or changed this session**. The standing register lives in
the Master — repeating it here creates a second copy that will fall out of date.

```markdown
- Risk:
- Impact:
- Likelihood:
- Mitigation:
- Owner:
- Status:
```

## 10. Actual End-of-Session State

The real state, not the planned one. Cover what is complete, in progress, incomplete, blocked,
ready for review, and not ready to ship.

Write this so a new contributor can pick up without guessing. If a dev server is running on a
port, if a migration is half-applied, if a file is mid-refactor and won't compile, if a rebase or
merge is in progress — say it here. This is the section that prevents a confusing first ten
minutes tomorrow.

## 11. Exact Next Action

```markdown
Next Action:
Start From:           branch + file + line, or the command to run
Required Inputs:
Expected Output:
Acceptance Criteria:
Do Not Change:
Blocking Conditions:
```

Vague entries ("continue development", "review the project", "finish the remaining work") make
the whole document ornamental — the reader still has to reconstruct the plan. Name the file, the
command, the branch, the issue.

The action must be startable from the state described in section 6. If it depends on something
missing — an access grant, a decision, an answer from a named person — then getting that is the
next action, and say who is being asked. `Do Not Change` is worth filling in whenever something
looks wrong but is deliberate; that's how you stop a well-meaning fix from undoing a decision.

## 12. Continuation Sources

Only what is needed to continue **this thread**: the branch, the files in flight, the issue or PR,
the one document that explains the piece being built. Project-wide sources of truth live in the
Master's table — point at it instead of copying it.

Paths must be copy-pasteable. `src/lib/auth/session.ts`, not "the session file".

## 13. Work That Must Not Be Repeated

What **this session** closed off: reviews completed, approaches tried and rejected, actions that
must not be rerun (a migration, a bulk import, a force-push), files that must not be reverted.
Project-wide items belong in the Master.

The reason matters more than the fact. "Tried X, didn't work" invites a second attempt; "tried X,
fails because the API rate-limits at 10 req/s" closes it.
