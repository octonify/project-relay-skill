# Daily Handoff — section reference

Contents:
1. [Handoff Metadata](#1-handoff-metadata)
2. [Session Objective](#2-session-objective)
3. [Completed Work](#3-completed-work)
4. [Decisions Made](#4-decisions-made)
5. [What Changed](#5-what-changed)
6. [Validated or Approved Items](#6-validated-or-approved-items)
7. [Open, Uncertain, or Unverified Items](#7-open-uncertain-or-unverified-items)
8. [Risks and Constraints](#8-risks-and-constraints)
9. [Actual End-of-Session State](#9-actual-end-of-session-state)
10. [Exact Next Action](#10-exact-next-action)
11. [Continuation Sources](#11-continuation-sources)
12. [Work That Must Not Be Repeated](#12-work-that-must-not-be-repeated)

A Daily Handoff answers one question: *what happened this session, why, what changed, what was
validated, what is still unresolved, and what must happen next?*

Cover the session scope only. Don't restate project history or project purpose — that's the
Master's job, and a Daily that drifts into background buries the operational detail the next
session actually needs.

**This list is a menu, not a checklist.** Delete any section you have nothing real to put in,
heading and all. A quiet session produces a short Daily, and that is a correct outcome rather
than a lazy one — the reader's attention is the scarce resource you're spending.

The one exception: state an absence when the absence is itself operationally significant. "No
tests were run this session" changes what tomorrow must do. "No infrastructure changes" on a
copywriting project does not.

---

## 1. Handoff Metadata

```markdown
Project:
Date:
Handoff ID:
Session Scope:
Workstream:
Prepared By:
End-of-Session Status:
```

Session Scope is a phrase, not a paragraph — the reader uses it to decide whether this file is
relevant to them. End-of-Session Status is a short verdict (`Login form working, tests not
written`), not a mood.

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
- Location or affected scope
- Final status
- Supporting evidence or reference

Planned work never appears here. If something is 90% done, it goes in section 9 (end state) with
the remaining 10% named.

## 4. Decisions Made

Every meaningful decision, with its reasoning — the reasoning is what stops the decision being
reversed by accident later.

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
you don't default to only code and files — infrastructure, data, process, and external-tool
changes are just as real and get forgotten most often.

Record each change once, here. If a change also drives a risk or an open item, cross-reference it
rather than restating the whole thing — duplicated detail is how two copies of a fact drift apart
and start contradicting each other.

Per important change:

```markdown
- Change:
- Location:
- Previous State:
- New State:
- Reason:
- Validation:
```

When the previous state is unknown, write `Unknown` and why. A guessed previous state is
actively dangerous — someone will use it to "restore" the wrong thing.

## 6. Validated or Approved Items

Only items confirmed by evidence, testing, observation, or human approval.

```markdown
- Item:
- Validation Method:
- Evidence:
- Result:
```

Statuses that fit here: Tested, Reviewed, Approved, Accepted, Verified, Published, Deployed,
Synchronized, Build Passed, QA Passed.

Expected or assumed outcomes do not belong in this section, however confident you feel. This is
the section a reader trusts without checking, which is exactly why it must stay clean.

## 7. Open, Uncertain, or Unverified Items

Open decisions, unanswered questions, assumptions you made, tests not run, contradictions
noticed, missing data, pending approvals, dependencies, blockers, things needing investigation.

Statuses: `Open` / `Blocked` / `Waiting for Input` / `Waiting for Approval` / `Needs Validation`
/ `Deferred` / `Out of Scope`.

Be generous here. An item listed as unverified costs the next session five minutes to check; an
item wrongly implied as solid can cost a day.

## 8. Risks and Constraints

```markdown
- Risk:
- Impact:
- Likelihood:
- Mitigation:
- Owner:
- Status:
```

Also record hard constraints that shape what the next session can even attempt: access limits,
time, budget, technical limits, security restrictions, scope boundaries, external dependencies.

## 9. Actual End-of-Session State

The real state, not the planned one. Cover what is complete, in progress, incomplete, blocked,
ready for review, and not ready to ship; what must not be repeated; and what changed since the
session started.

Write this so a new contributor can pick up without guessing. If a service is running locally on
a port, if a migration is half-applied, if a file is mid-refactor and won't compile — say it
here. This is the section that prevents a confusing first ten minutes tomorrow.

## 10. Exact Next Action

```markdown
Next Action:
Start From:
Required Inputs:
Expected Output:
Acceptance Criteria:
Do Not Change:
Blocking Conditions:
```

Vague entries ("continue development", "review the project", "finish the remaining work") make
the whole document ornamental — the reader still has to reconstruct the plan. Name the file, the
command, the ticket. `Do Not Change` is worth filling in whenever something looks wrong but is
deliberate; that's how you stop a well-meaning fix from undoing a decision.

## 11. Continuation Sources

Everything needed to continue, with exact identifiers: sources of truth, canonical files,
decision records, reports, repo paths, branches, commits, datasets, prototypes, design sources,
packages, dashboards, tickets, issues, PRs, external system links.

Paths must be copy-pasteable. `src/lib/auth/session.ts`, not "the session file".

## 12. Work That Must Not Be Repeated

Reviews already done, decisions already final, approaches already rejected, actions that must
not be rerun (a migration, a bulk import, an email send), files that must not be renamed or
replaced, tests that only need rerunning if conditions change, and failed approaches with the
reason they failed.

The reason matters more than the fact. "Tried X, didn't work" invites a second attempt; "tried X,
fails because the API rate-limits at 10 req/s" closes it.
