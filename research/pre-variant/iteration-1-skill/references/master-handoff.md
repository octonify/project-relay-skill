# Master Handoff — section reference

Contents:
1. [Document Metadata](#1-document-metadata)
2. [Executive Summary](#2-executive-summary)
3. [Project Purpose and Definition](#3-project-purpose-and-definition)
4. [Locked Principles and Decisions](#4-locked-principles-and-decisions)
5. [Project Structure](#5-project-structure)
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
16. [Technical or Operational State](#16-technical-or-operational-state)
17. [Current Project State](#17-current-project-state)
18. [Immediate Next Action](#18-immediate-next-action)
19. [New-Session Start Guide](#19-new-session-start-guide)
20. [Incorporated Daily Handoffs](#20-incorporated-daily-handoffs)

The Master Handoff must stand alone. Someone handed only this file should be able to understand
the project's purpose, reconstruct its current state, find every authoritative source, tell final
decisions from open ones, and start work — without reading a single Daily Handoff or any chat
history.

That standard is what makes the Master different from a long changelog. Length is not the goal;
sufficiency is.

## How to update it

The Master is edited in place, cumulatively. Before writing, read the whole existing file — you
are integrating new information into a living document, not producing a fresh one.

- **Preserve** valid existing information.
- **Place** new information in the section where it belongs. Blind appending at the end is how a
  Master turns into a pile of dated notes with no canonical state.
- **Correct** outdated statuses instead of leaving the old and new claim side by side.
- **Mark** superseded decisions and sources in section 13, with replacement and reason. A silently
  deleted decision reads as never made, and someone will re-open the argument.
- **Resolve** contradictions where you can verify the truth; where you can't, record them in
  section 14 with the evidence that would settle it.
- **Rewrite** the Executive Summary (2) and Immediate Next Action (18) last, after the body
  reflects reality.

Omit sections that genuinely don't apply to this project — a solo content project has no CI/CD
state — but replace rather than drop the structural ones: section 16 becomes an operational-state
section for non-technical work.

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

## 5. Project Structure

Workstreams, repositories, folders, environments, services, systems, platforms, how project areas
relate, and who owns each.

## 6. Architecture and Workflow

Whichever apply: technical, information, content, or data architecture; design, development,
review/approval, release/deployment, and maintenance workflows; human and agent roles; tools and
integrations; approval gates; access restrictions.

Approval gates and access restrictions are the parts most often missing, and the parts that most
often block a new contributor on day one.

## 7. Sources of Truth

```markdown
| Source | Location | Purpose | Authority | Status |
|---|---|---|---|---|
```

When sources can conflict, state the precedence order explicitly. "The spreadsheet wins over the
CMS for pricing" is the kind of sentence that prevents a week of confusion.

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

Only events needed to understand how the project got here: milestones, direction changes, audits,
architecture decisions, major corrections, releases, migrations, failures and their causes,
superseded decisions.

This must not become a concatenation of Daily Handoffs. Ask of each entry: would someone
misunderstand the present state without knowing this? If no, leave it in the Daily files.

## 10. Final Decisions

```markdown
- Decision:
- Date:
- Rationale:
- Impact:
- Source:
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
what to go and find out.

## 12. Changes Since the Previous Baseline

What changed since the last valid Master: information added, statuses corrected, new decisions,
superseded decisions, files replaced, architecture changes, scope changes, new blockers, resolved
blockers.

This is the diff a returning reader checks first when they already know the older version.

## 13. Superseded or Replaced Items

```markdown
| Superseded Item | Replacement | Reason | Date |
|---|---|---|---|
```

Exists to stop someone confidently using a dead file, stale API, or reversed decision. Don't
remove old information without explanation when it still matters historically.

## 14. Contradictions and Resolution

Per important conflict: the contradiction, the conflicting sources, the verified current state,
the authoritative source, the final resolution, why that source takes precedence, and any
corrective action still required.

Unresolved contradictions are not embarrassing — undocumented ones are, because the next reader
hits them with no warning.

## 15. Risks, Constraints, and Dependencies

Active risks, technical/security/access/time/financial constraints, internal and external
dependencies, failure points, mitigation actions.

## 16. Technical or Operational State

For technical projects: repository, branch, commit, open PRs, local state, remote state,
uncommitted changes, build status, test status, deployment status, environment status, database
status, migration status, CI/CD status, backup status, monitoring status.

For non-technical projects, replace with the equivalent operational state — live systems,
published assets, scheduled sends, account standing.

Verify these rather than reciting them from memory; state is the thing most likely to have moved
since anyone last looked.

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

Exactly one immediate next action. Everything else belongs in a prioritized queue below it —
two "immediate" actions means the reader has to pick, and picking is the decision you were
supposed to make for them.

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

Point 8 is a safety rail. If deploying, sending, or deleting requires sign-off, it must be
impossible to miss here.

## 20. Incorporated Daily Handoffs

```markdown
| Date | Handoff File | Scope | Incorporated into Master |
|---|---|---|---|
```

This table is how the next Master update knows where to resume. Keep it accurate — a Daily marked
incorporated when it wasn't will be silently skipped forever.
