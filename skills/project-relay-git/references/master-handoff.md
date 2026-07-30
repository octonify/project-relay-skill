# Master Handoff — section reference

Contents:
1. [Document Metadata](#1-document-metadata)
2. [Executive Summary](#2-executive-summary)
3. [Project Purpose and Definition](#3-project-purpose-and-definition)
4. [Locked Principles and Decisions](#4-locked-principles-and-decisions)
5. [Repository and Project Structure](#5-repository-and-project-structure)
6. [Architecture and Workflow](#6-architecture-and-workflow)
7. [Sources of Truth](#7-sources-of-truth)
8. [Workstream Status](#8-workstream-status)
9. [Important Project History](#9-important-project-history)
10. [Final Decisions](#10-final-decisions)
11. [Open Decisions](#11-open-decisions)
12. [Changes Since the Previous Baseline](#12-changes-since-the-previous-baseline)
13. [Superseded or Replaced Items](#13-superseded-or-replaced-items)
14. [Contradictions and Resolution](#14-contradictions-and-resolution)
15. [Risks, Constraints, and Dependencies](#15-risks-constraints-and-dependencies)
16. [Current Technical State](#16-current-technical-state)
17. [Current Project State](#17-current-project-state)
18. [Immediate Next Action](#18-immediate-next-action)
19. [New-Session Start Guide](#19-new-session-start-guide)
20. [Incorporated Daily Handoffs](#20-incorporated-daily-handoffs)

The Master Handoff must stand alone. Someone handed only this file and a clone of the repository
should be able to understand the project's purpose, reconstruct its current state, find every
authoritative source, tell final decisions from open ones, and start work — without reading a
single Daily Handoff or any chat history.

That standard is what makes the Master different from a long changelog. Length is not the goal;
sufficiency is. A Master that has swollen with session detail is *less* usable than a short one,
because the durable facts are now buried in narrative nobody needs.

**Hold the line against Daily detail.** The Master stores durable state — decisions, structure,
sources, status, constraints, the next action. It does not store how a session went. When you
integrate a Daily, extract the consequence and leave the story: the Daily records that an hour
was lost to a dead approach; the Master records only that the approach is closed and why, with a
pointer to the Daily for anyone who wants the detail.

**This section list is a menu.** Drop sections the project genuinely has no use for. Adapt rather
than delete the structural ones — a project with a single workstream folds section 8 into 17.

## How to update it

The Master is edited in place, cumulatively. Before writing, read the whole existing file — you
are integrating new information into a living document, not producing a fresh one. Do not create
a second Master file under any name; Git already holds every previous version.

- **Re-examine every inherited claim.** A line in the existing Master is evidence of what someone
  believed then, not of current state. Branches move, files get renamed, "tests passing" outlives
  the test suite. For each claim: verify and keep, mark it an unverified inherited claim, mark it
  stale with what you now know, or supersede it. Carrying stale claims forward silently is the
  single most common way a Master loses the reader's trust — and once one sentence is found to be
  false, every other sentence has to be re-checked.
- **Preserve** valid existing information. Never drop a decision, constraint, or blocker merely
  to shorten the document.
- **Place** new information in the section where it belongs. Blind appending at the end is how a
  Master turns into a pile of dated notes with no canonical state.
- **Correct** outdated statuses instead of leaving the old and new claim side by side.
- **Mark** superseded decisions and sources in section 13, with replacement and reason. A
  silently deleted decision reads as never made, and someone will re-open the argument.
- **Resolve** contradictions where you can verify the truth; where you can't, record them in
  section 14 with the evidence that would settle it.
- **Record** the Dailies you incorporated in section 20, so the next update knows where to resume.
- **Rewrite** the Executive Summary (2) and Immediate Next Action (18) last, after the body
  reflects reality.

---

## 1. Document Metadata

```markdown
Project:
Document Type: Master Handoff
Version:
Last Updated:
Current Phase:
Overall Status:
Canonical File:
```

Increment Version on every meaningful update. `Canonical File` states this document's own
authoritative path, so a copy found elsewhere can be recognized as a copy.

## 2. Executive Summary

Concise: what the project is, its primary objective, current phase, latest major progress, the
most important blocker, and the immediate next action.

Rewrite this every update. A stale summary on top of a fresh document is worse than no summary,
because it's the part people read and trust.

## 3. Project Purpose and Definition

Problem being solved, primary objective, intended final output, users or stakeholders, success
criteria, current scope, explicit out-of-scope items.

The out-of-scope list does real work — it stops a new contributor helpfully building something
that was deliberately excluded.

## 4. Locked Principles and Decisions

Stable foundations only. Per entry: decision, rationale, date, status, approval source, what it
supersedes.

Provisional decisions do not belong here. If it might change next week, it goes in section 10 or
11. The value of this section is that a reader can build on it without checking.

## 5. Repository and Project Structure

Repository or repositories with their URLs, the branching model, protected branches, release
branches, environments and which branch feeds each, key directories and what lives in them,
ownership.

Name the default branch explicitly. "Merge into main" and "merge into develop" are very different
instructions, and a new contributor cannot infer which applies.

## 6. Architecture and Workflow

Whichever apply: system architecture, data model, module boundaries; development, review,
release, and deployment workflows; CI/CD pipelines and what they gate; human and agent roles;
tools and integrations; approval gates; access restrictions.

Approval gates and access restrictions are the parts most often missing, and the parts that most
often block a new contributor on day one.

## 7. Sources of Truth

```markdown
| Source | Location | Purpose | Authority | Status |
|---|---|---|---|---|
```

When sources can conflict, state the precedence order — but only where someone actually
established it. An invented precedence rule is worse than none, because the next contributor will
follow it. If nobody has decided, that is an open decision (section 11), not a rule.

## 8. Workstream Status

Per workstream:

```markdown
## Workstream Name

Purpose:
Owner:
Current Status:
Completed:
In Progress:
Blocked:
Open Decisions:
Dependencies:
Next Action:
Relevant Sources:
```

Status values: Not Started, Planned, In Progress, Under Review, Approved, Complete, Blocked,
Deferred, Archived.

## 9. Important Project History

Only events needed to understand how the project got here: milestones, direction changes,
architecture decisions, major corrections, releases, migrations, failures and their causes,
superseded decisions.

This must not become a concatenation of Daily Handoffs. Ask of each entry: would someone
misunderstand the present state without knowing this? If no, leave it in the Daily files — they
are preserved and dated, so nothing is lost by not repeating them here. One line per event is
usually enough, with the Daily filename for anyone who needs the detail.

## 10. Final Decisions

```markdown
- Decision:
- Date:
- Rationale:                one line — the full reasoning stays in the Daily
- Impact:
- Source:                   the Daily Handoff or PR where it was made
- Supersedes:
```

## 11. Open Decisions

```markdown
- Decision Needed:
- Why It Matters:
- Available Options:
- Required Evidence:
- Decision Owner:
- Deadline or Trigger:
```

`Required Evidence` is what turns an open decision into a closable one — it tells the next session
what to go and find out. Name a real Decision Owner or write `Unassigned`; do not invent one.

## 12. Changes Since the Previous Baseline

What changed since the last valid Master: information added, statuses corrected, new decisions,
superseded decisions, architecture or scope changes, new blockers, resolved blockers.

This is the diff a returning reader checks first when they already know the older version.

## 13. Superseded or Replaced Items

```markdown
| Superseded Item | Replacement | Reason | Date |
|---|---|---|---|
```

Exists to stop someone confidently using a dead file, stale API, abandoned branch, or reversed
decision. Don't remove old information without explanation when it still matters historically.

## 14. Contradictions and Resolution

Per important conflict: the contradiction, the conflicting sources, the verified current state,
the authoritative source, the final resolution, why that source takes precedence, and any
corrective action still required.

Unresolved contradictions are not embarrassing — undocumented ones are, because the next reader
hits them with no warning.

## 15. Risks, Constraints, and Dependencies

The standing register: active risks, technical/security/access/time/budget constraints, internal
and external dependencies, failure points, mitigations.

This is the **primary home** for risks and constraints. Dailies list only what they newly
discovered; those items land here on integration.

## 16. Current Technical State

```markdown
Repository:
Default branch:
Active branches:
HEAD of active branch:
Uncommitted or unpushed work:
Open PRs:
Open issues:
Build status:
Test status:
Migration status:
Deployment status:
Environment status:
CI/CD status:
```

Verify these rather than reciting them from memory — state is the thing most likely to have moved
since anyone last looked. Anything you could not check is `Not verified as of <date>`, which is a
useful answer. "Passing" copied from the last Master is not.

## 17. Current Project State

An accurate snapshot: current phase, latest approved output, active work, completed work,
incomplete work, blockers, open decisions, readiness for the next phase, overall status.

## 18. Immediate Next Action

```markdown
Immediate Next Action:
Responsible Role or Agent:
Start From:
Required Inputs:
Expected Deliverable:
Acceptance Criteria:
Dependencies:
Stop Conditions:
Do Not Change:
```

Exactly one immediate next action, executable from the state in section 16. Everything else
belongs in a prioritized queue below it — two "immediate" actions means the reader has to pick,
and picking is the decision you were supposed to make for them.

If the action is blocked on a missing prerequisite, the next action is obtaining that
prerequisite, named concretely.

## 19. New-Session Start Guide

Tell a new contributor or agent, in order:

1. Which files to read first
2. Which source is canonical
3. What the current state is
4. Where to start
5. Which decisions are final
6. Which work must not be repeated
7. Which access is required
8. Which actions require explicit human approval

Point 8 is a safety rail. If deploying, force-pushing, running a migration, or merging to the
default branch requires sign-off, it must be impossible to miss here.

## 20. Incorporated Daily Handoffs

```markdown
| Date | Handoff File | Scope | Incorporated into Master |
|---|---|---|---|
```

This table is how the next Master update knows where to resume. Keep it accurate — a Daily marked
incorporated when it wasn't will be silently skipped forever.
