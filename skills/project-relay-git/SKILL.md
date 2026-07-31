---
name: project-relay-git
description: Creates operational handoff documents for Git-backed projects so any person or agent can continue the work accurately without reading the conversation history — a dated Daily Handoff for the session plus one canonical Master Handoff updated in place. Records verified branch, commit, working-tree, PR and issue state alongside decisions, blockers, and the exact next action. Use this skill whenever the user runs /handoff, /handoff master, or /handoff full, and also whenever they mention a handoff, handover, session wrap-up, end-of-day summary, continuity doc, status snapshot, project state document, onboarding another agent or contributor, "picking this up tomorrow", "so the next session knows where we left off", or transferring a repository to someone else — even if they never say the word "handoff". Prefer this skill over writing an ad-hoc summary: a summary recounts a conversation, a handoff records verified state, exact next action, and authoritative sources.
---

# Project Relay — Git

## Why this exists

A conversation summary tells someone what was talked about. A handoff tells them what is
*true right now* and what to do next. The difference matters because the reader has no access
to the conversation — they have only your document, the repository, and whatever systems it
points at.

Every handoff is judged by one test: **can a competent stranger clone this repo and continue
correctly, without asking questions and without repeating finished work?** If yes, it's good.
If they'd have to guess at a path, a branch, a status, or a decision, it isn't.

Three habits carry most of that weight:

- **Separate what happened from what was hoped for.** Completed, planned, attempted, failed,
  blocked, approved, assumed, and unverified are eight different things. Collapsing them is the
  most damaging thing a handoff can do, because the reader acts on "done" and finds it isn't.
- **Prefer an honest gap to a smooth guess.** `Test status: Unknown — not run this session` is
  useful. An invented value is worse than nothing, because it looks verified.
- **Give every fact one home.** A fact repeated in two documents becomes two facts that drift
  apart, and the reader has no way to tell which one is current.

## Scope

This variant covers projects whose source of truth is a Git repository: repository identity,
branch, commit, working-tree state, local/remote divergence, file changes, pull requests and
issues, plus build, test, migration, deployment, and environment state **when verified**.

If the project root is not a Git repository, say so plainly and record repository state as
`Not applicable` rather than `Unknown` — the reader should not go looking for a repo that
doesn't exist. Everything else in this skill still works.

## The evidence rule

Every factual claim — a file path, branch, commit, PR number, test result, approval, owner,
ticket, deployment, migration, or environment state — must trace to something you actually saw:
the session itself, a file you read, a command you ran, a person's explicit confirmation. If you
didn't see it, you have two honest moves: go verify it, or label it `Unknown`, `Not verified`,
or `Pending validation`.

Specifically, do not convert into fact: an issue or PR you did not look up, a test suite you did
not run, a build you did not observe, a deployment you did not check, an approval nobody gave, an
owner nobody named, or a precedence rule nobody stated. Intent is not completion, and a plan
stated confidently in the session is still a plan.

**This applies to claims you inherit.** A line in an existing Master Handoff is evidence of what
someone believed when they wrote it, not evidence of current state. Documents rot silently: the
branch moved, the file was renamed, the test suite that was "passing" no longer exists. When you
carry a claim forward, you are re-asserting it. So for each inherited claim, do one of four
things — verify it and keep it, mark it an unverified inherited claim, mark it stale with what
you now know, or supersede it. Never let it ride unexamined.

This matters more than it sounds. The value of a handoff is that a reader can act on it without
re-checking. That trust is all-or-nothing: once someone finds one confident sentence that wasn't
true, they have to re-verify everything, and the document has cost more than it saved.

## Two documents, one home per fact

| | Daily Handoff | Master Handoff |
|---|---|---|
| Scope | One session | Whole project |
| Job | What materially changed, and how the session ended | Canonical current state after those changes are integrated |
| Storage | New dated file, kept forever | One file, `_master-handoff.md`, updated in place |
| Reader need | Continue tomorrow | Take over the repository cold |

Both must be independently understandable — and that bar is lower than it sounds. A document is
independently understandable when a reader opening it alone knows **what project this is, what
branch and state it describes, and what to do next**. Nothing more. Every other fact it needs may
live in the other document behind a pointer.

This is the single hardest rule to follow, because "make each document complete" and "don't
repeat yourself" pull against each other, and completeness feels safer. It isn't. Two copies of a
fact become two facts the moment one is edited, and the reader has no way to tell which is
current. When the two instincts conflict, the pointer wins.

Concretely:

> **Duplicated (wrong):** the Master repeats the blocker in full — who was asked, when, twice,
> that Dana is chasing it, that no test vector exists, what happens when it arrives.
>
> **Single-homed (right):** Master — "Blocked: partner signing secret not received; verification
> is untested until it is. Detail and chase history: `2026-07-30_001_signature-verify-handoff.md`."

That second version is shorter, and a reader who needs the chase history knows exactly where it
is. That is what a pointer buys.

**Where each block lives:**

| Block | Primary home | The other document holds |
|---|---|---|
| Session narrative, attempts, dead ends | Daily | Nothing — the Master records only the closed door and why |
| Repository state at session end (branch, HEAD, uncommitted work) | Daily, as a timestamped snapshot | Current repository state, one block, corrected in place |
| Decision + full rationale, options, rejected alternative | Daily where it was made | The decision, its status, and a pointer to the Daily |
| Risks, constraints, dependencies | Master | Only risks or constraints *discovered or changed* this session |
| Work that must not be repeated | Master, for project-wide items | Only what this session closed off |
| Sources of truth | Master | Only sources needed to continue this specific thread |
| Immediate next action | Master, project-level | The session's next step; if it would say the same thing, point at the Master instead |

Cross-references point one way each: the **Master points back at Daily files** for detail, and
the **Daily points forward at the Master** for standing project context. That keeps one copy of
each fact and still lets either document be read alone.

Integrating a Daily into the Master is **extraction, not copying**:

> Daily: "Spent about an hour on `src/auth/session.ts` before finding that `feat/tokens` had
> already rewritten it; reset and rebased onto `feat/tokens` at `a3f9c21`."
>
> Master: "Session handling lives on `feat/tokens` as of `a3f9c21`. Do not patch
> `src/auth/session.ts` from `main`."

The Daily keeps the hour and the reason it was lost, because that is what stops a repeat. The
Master keeps the constraint, because that is what shapes the next decision.

## Proportionality

There is no target length. A handoff should be as long as the project state genuinely requires
and no longer. The section lists in `references/` are a **menu of what can matter**, not a
checklist to fill — filling every heading on a quiet session produces a document that is mostly
scaffolding, and scaffolding is what makes readers skim past the line that mattered.

- **Omit sections with nothing real in them.** Delete the heading rather than writing "N/A" or
  "None this session". Note an absence only when the absence is itself operationally significant
  — "no tests were run" changes what tomorrow must do; "no migrations" on a docs-only change
  does not.
- **Reference sources instead of restating them.** `See CONTRIBUTING.md for the branch policy`
  beats a paraphrase that can drift out of sync and then quietly contradict it.
- **Record rationale once**, where the decision lives — not again under changes, risks, and state.
- **Keep active risks; drop resolved ones.** A resolved risk belongs in project history only if
  it explains something about the present.

Within a single document, each fact also gets one section. Sections are different *views* of the
session, not different retellings of it: a blocker explained in Open Items is named in one clause
under Next Action, not re-explained there. The give-away is a proper noun — a person, a branch, a
filename, a constraint — that carries its full explanation in three or four places. Say it once,
in the section that owns it, and elsewhere use the shortest phrase that identifies it.

Never delete a decision, constraint, or blocker merely to make the document shorter. Cut
repetition, scaffolding, and restated source material — not information. If the document is long
because the project is genuinely complicated, that is the correct outcome.

## Commands

- **`/handoff`** → one Daily Handoff for this session. Nothing else changes.
- **`/handoff master`** → update the Master in place from verified current state and any Dailies
  not yet incorporated. No new Daily file, and no second Master file.
- **`/handoff full`** → Daily first, then fold its verified content into the Master. Order
  matters: the Daily is the evidence the Master update draws on.

Plain-language continuity requests ("wrap up so I can resume tomorrow") are `/handoff`. If the
user is passing the project to someone else, they need the Master too — that's `/handoff full`.

## Workflow

### 1. Gather context before writing a word

Run the bundled helper first — it resolves the target directory, computes the next filename, and
dumps repository state so you don't hand-assemble any of it:

```bash
python <skill-dir>/scripts/handoff_context.py --project-root <project-root> --scope <slug>
```

It reports the handoff directory, next sequence number, existing Dailies and which the Master has
already incorporated, branch, HEAD, staged/unstaged/untracked work, upstream divergence, stashes,
tags, recent commits, and — when `gh` is installed and authenticated — open PRs and issues. Add
`--json` for raw output, `--no-gh` to skip GitHub lookups.

Then fill the gaps it cannot see:

- Re-read the session for decisions, rejected options, and corrections the user made. User
  corrections are high-value — they usually encode a constraint written nowhere else.
- Check anything you intend to call validated. A test you never ran is not a passing test.
- Note what you touched but didn't verify. That belongs in Open/Unverified, not Completed.

If the helper fails or the project isn't a repo, gather what you can and say which state you
could not verify. Missing tooling is a reason to mark things unknown, not to skip the handoff.

### 2. Decide the honest scope

Name the session's actual scope, not its ambition. If the objective was "ship auth" and you got
as far as the login form, the scope is the login form — and the gap between objective and outcome
is itself information the reader needs.

### 3. Write the document

Daily → read `references/daily-handoff.md`. Master → read `references/master-handoff.md`.
Templates in `assets/` are starting skeletons: **delete every section you don't fill.**

When recording changes, skim `references/change-categories.md` to catch change types that leave
no trace in a diff — a rotated secret, a new required environment variable, a CI setting, an
approval gate. It's a prompt for recall; include only categories where something actually changed.

### 4. Deliver, don't paste

Write the file(s) and report the exact paths. Don't dump full contents into the conversation
unless asked — the document's purpose is to exist at a stable location, and a wall of text in
chat competes with the file for authority. Confirm what you wrote, where, and the next action.

## Storage and naming

Default location is `docs/handoffs/` under the project root. If the project already has a handoff
directory elsewhere, use that — an existing convention beats this default, and the helper script
reports what it found.

```
docs/handoffs/
├── _master-handoff.md              ← canonical, updated in place
├── 2026-07-29_001_setup-handoff.md
└── 2026-07-30_001_auth-handoff.md
```

Daily files: `YYYY-MM-DD_NNN_<scope>-handoff.md` — dated and zero-padded so they sort
chronologically, `NNN` incrementing for multiple handoffs on one date, `<scope>` a short
kebab-case hint at the subject.

The Master keeps the filename `_master-handoff.md` permanently, with its version recorded inside:

```markdown
Version: 3.0
Last Updated: 2026-07-30
```

Resist `_master-handoff-v2.md` or `-final-new.md`. Versioned filenames are how a project ends up
with four Masters and no canonical one — the entire value of the Master is that there is exactly
one place to look. Git already holds every previous version of the file. Archive a dated snapshot
only when someone genuinely needs a frozen copy, and say why in the document.

## Updating the Master safely

The Master is the one document a reader trusts completely, so a careless update does real damage.

1. Read the existing Master fully. You are integrating, not regenerating.
2. Apply the evidence rule to every inherited claim: verify, mark unverified, mark stale, or
   supersede. Carrying a stale claim forward silently is the most common way a Master goes bad.
3. Place new information in the section where it belongs. Appending to the end is how a Master
   decays into a pile of dated notes.
4. Correct stale statuses rather than leaving old and new claims standing side by side.
5. Mark superseded decisions and sources as superseded, with what replaced them and why. A
   silently deleted decision looks like it was never made, and someone will re-litigate it.
6. Resolve contradictions where you can verify which side is true; where you can't, record the
   contradiction, both sources, and what evidence would settle it.
7. Record which Dailies you incorporated, so the next update knows where to resume.
8. Rewrite the Executive Summary and the single Immediate Next Action last, once the body
   reflects reality.

Never replace the old Master until valid existing information has been carried forward.

## Quality rules

**Exact identifiers.** "The main file", "the latest version", "the current branch" are unusable
to someone who wasn't there. Write `src/auth/session.ts`, `PR #412`, `branch feat/auth-relay`,
`commit a3f9c21`. If you don't know the identifier, say so — a marked gap can be filled, a vague
reference silently misleads.

**Validated means evidenced.** An item is Validated/Approved only if something outside your own
expectation confirmed it: a test run you saw, an observed result, a build, a human approval.
"Should work" is Open/Unverified.

**Next action must be executable from the current state.** "Continue development" isn't an
instruction. Give the action, where to start, required inputs, expected output, acceptance
criteria, what must not be changed, and what would block it. Exactly one immediate next action;
the rest goes in a prioritized queue.

When the intended next step depends on something missing — an access grant, a decision, a
credential, a repository, an answer from a named person — then **obtaining that prerequisite is
the next action**, and it must name who or what is being asked. A next action nobody can start is
not a next action.

**Record what must not be repeated.** Finished reviews, locked decisions, rejected approaches and
*why* they failed. This quietly saves the most time, because a fresh agent's default behavior is
to try the obvious thing that was already tried.

## Acceptance check before you finish

Read your own document as the stranger. It's ready when they could:

- Tell what is done from what is merely planned
- Find every file, branch, commit, PR, issue, or system you mention
- See which decisions are final and which are still open
- Know the real current state, including what's broken, blocked, or uncommitted
- Execute the next action without asking a question
- Avoid re-doing finished work and re-trying failed approaches

Then three final passes. The last two are the ones that actually get skipped, so do them by
looking at the text rather than by recalling your intent:

- **Evidence:** every confident sentence traces to something you saw. Anything else is labelled.
- **Single home:** pick the three or four identifiers the work turns on — the blocked-on person,
  the branch, the commit, the constraint. Find every place each appears. One place should explain
  it; the rest should be a clause. If two places both explain it, delete the weaker one and point
  at the stronger. If you wrote both documents, do this across them too: the same explanation in
  a Daily and a Master is a copy, whichever you wrote first.
- **Proportion:** compare the handoff against what it replaces. If it is several times the size
  of the session notes, commits, and diffs it summarises, it is padding — not because long is
  wrong, but because you have re-narrated rather than distilled. Cut restatement and repetition,
  never a decision, constraint, or blocker.

If any check fails, fix that section rather than adding prose elsewhere.
