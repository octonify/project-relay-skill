---
name: project-relay
description: Creates operational handoff documents that let any person or agent continue a project accurately without reading the conversation history — a dated Daily Handoff for a session plus a cumulative canonical Master Handoff. Use this skill whenever the user runs /handoff, /handoff master, or /handoff full, and also whenever they mention a handoff, handover, session wrap-up, end-of-day summary, continuity doc, status snapshot, project state document, onboarding another agent or contributor, "picking this up tomorrow", "so the next session knows where we left off", or transferring a project to someone else — even if they never say the word "handoff". Prefer this skill over writing an ad-hoc summary: a summary recounts a conversation, a handoff records verified state, exact next action, and authoritative sources.
---

# Project Relay

## Why this exists

A conversation summary tells someone what was talked about. A handoff tells them what is
*true right now* and what to do next. The difference matters because the reader has no access
to the conversation — they have only your document, the repo, and whatever systems it points at.

Every handoff is judged by one test: **can a competent stranger continue this project correctly,
without asking questions and without repeating finished work?** If yes, it's good. If they'd have
to guess at a path, a status, or a decision, it isn't.

Three habits carry most of that weight:

- **Separate what happened from what was hoped for.** Completed, planned, attempted, failed,
  blocked, approved, assumed, and unverified are eight different things. Collapsing them is the
  most damaging thing a handoff can do, because the reader acts on "done" and finds it isn't.
- **Prefer an honest gap to a smooth guess.** `Status: Unknown — not verified this session` is
  useful. An invented value is worse than nothing, because it looks verified.
- **Write it once, at the size the work earns.** A handoff nobody finishes reading has failed at
  the only job it had.

## The evidence rule

Every factual claim — a file path, commit, test result, approval, owner, ticket, deployment,
schema, or system state — must trace to something you actually saw: the session itself, a file
you read, a command you ran, a person's explicit confirmation. If you didn't see it, you have
two honest moves: go verify it, or label it `Unknown`, `Not verified`, or `Pending validation`.

**This applies to claims you inherit.** A line in an existing Master Handoff is evidence of what
someone believed when they wrote it, not evidence of current state. Documents rot silently: the
branch moved, the file was renamed, the test suite that was "passing" no longer exists. When you
carry a claim forward, you are re-asserting it in the reader's eyes. So for each inherited claim,
do one of four things — verify it and keep it, mark it an unverified inherited claim, mark it
stale with what you know, or supersede it. Never let it ride unexamined.

This matters more than it sounds. The value of a handoff is that a reader can act on it without
re-checking. That trust is all-or-nothing: once someone finds one confident sentence that wasn't
true, they have to re-verify everything, and the document has cost them more than it saved.

## What goes where

| | Daily Handoff | Master Handoff |
|---|---|---|
| Scope | One session or day | Whole project |
| Job | Record what changed | Hold durable state after change is integrated |
| Storage | New dated file, kept forever | One stable canonical file, updated in place |
| Reader need | Continue tomorrow | Take over the project cold |

A fact belongs in **one** of them. Repeat it only where repetition is genuinely load-bearing for
safe continuation — a "do not touch `src/legacy/`" line earns its place in both, a paragraph of
rationale does not.

Integrating a Daily into the Master is **extraction, not copying**. You are pulling out the
durable consequence and leaving the session narrative behind:

> Daily: "Spent about an hour drafting the loyalty email off the 2024 terms before Marcus
> mentioned the scheme is being replaced in September and the new terms aren't drafted."
>
> Master: "Loyalty email blocked — new scheme terms not drafted. Do not build on the 2024 terms."

The Daily keeps the hour and the reason it was lost, because that's what stops a repeat. The
Master keeps the blocker and the constraint, because that's what shapes the next decision.

## Proportionality

The section lists in `references/` are a **menu of what can matter**, not a checklist to fill.
Filling every heading on a quiet session produces a document that is mostly scaffolding, and
scaffolding is what makes readers skim — which is how they miss the one line that mattered.

- **Omit sections with nothing real in them.** Delete the heading entirely rather than writing
  "N/A" or "None this session". An empty heading costs the reader attention and returns nothing.
  Note an absence only when the absence is itself operationally significant ("no tests were run"
  belongs; "no infrastructure changes" on a copywriting project does not).
- **Reference sources instead of restating them.** `See brief.md for scope` beats a paraphrase,
  which can drift out of sync with the thing it paraphrases and then quietly contradict it.
- **Record rationale once**, where the decision lives. Not again under changes, risks, and state.
- **Keep active risks; drop resolved ones.** A resolved risk is history, and only belongs in the
  Master's history section if it explains something about the present.

The size test: **if your handoff is longer than the material it saves the reader from reading,
you have inverted its purpose.** A three-file session is a one-page Daily. Match the work.

## Commands

- **`/handoff`** → one Daily Handoff for this session. Nothing else changes.
- **`/handoff master`** → update the Master in place from verified current state and any Dailies
  not yet incorporated. No new Daily file.
- **`/handoff full`** → Daily first, then fold its verified content into the Master. Order
  matters: the Daily is the evidence the Master update draws on.

Plain-language continuity requests ("wrap up so I can resume tomorrow") are `/handoff`. If the
user is passing the project to someone else, they need the Master too — that's `/handoff full`.

## Workflow

### 1. Gather context before writing a word

Run the bundled helper first — it resolves the target directory, computes the next filename, and
dumps repository state so you don't hand-assemble any of it:

```bash
python <skill-dir>/scripts/handoff_context.py --project-root <project-root>
```

It reports the handoff directory, next sequence number, existing Dailies and which are already
incorporated, current branch/commit/uncommitted files, and recent commits. Then fill the gaps it
can't see:

- Re-read the session for decisions, rejected options, and corrections the user made. User
  corrections are high-value — they usually encode a constraint written nowhere else.
- Check anything you intend to call validated. A test you never ran is not a passing test.
- Note what you touched but didn't verify. That belongs in Open/Unverified, not Completed.

If the project isn't a git repo or the helper fails, gather what you can and say which state you
couldn't verify. Missing tooling is a reason to mark things unknown, not to skip the handoff.

### 2. Decide the honest scope

Name the session's actual scope, not its ambition. If the objective was "ship auth" and you got
as far as the login form, the scope is the login form — and the gap between objective and outcome
is itself information the reader needs.

### 3. Write the document

Daily → read `references/daily-handoff.md`. Master → read `references/master-handoff.md`.
Templates in `assets/` are starting skeletons: **delete every section you don't fill.**

When recording changes, skim `references/change-categories.md` to catch change types that leave
no trace in a diff — a rotated secret, a renamed spreadsheet column, a new approval gate. It's a
prompt for recall; include only categories where something actually changed.

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
one place to look. Archive a dated snapshot only when someone genuinely needs a frozen copy, and
say why in the document.

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
7. Rewrite the Executive Summary and the single Immediate Next Action last, once the body
   reflects reality.

Never replace the old Master until valid existing information has been carried forward.

## Quality rules

**Exact identifiers.** "The main file", "the latest version", "the current branch" are unusable
to someone who wasn't there. Write `src/auth/session.ts`, `PR #412`, `branch feat/auth-relay`,
`commit a3f9c21`. If you don't know the identifier, say so — a marked gap can be filled, a vague
reference silently misleads.

**Validated means evidenced.** An item is Validated/Approved only if something outside your own
expectation confirmed it: a test run, an observed result, a build, a human approval. "Should
work" is Open/Unverified.

**Next action must be executable.** "Continue development" isn't an instruction. Give the action,
where to start, required inputs, expected output, acceptance criteria, what must not be changed,
and what would block them. Exactly one immediate next action; the rest goes in a prioritized queue.

**Record what must not be repeated.** Finished reviews, locked decisions, rejected approaches and
*why* they failed. This quietly saves the most time, because a fresh agent's default behavior is
to try the obvious thing that was already tried.

## Acceptance check before you finish

Read your own document as the stranger. It's ready when they could:

- Tell what is done from what is merely planned
- Find every file, branch, ticket, or system you mention
- See which decisions are final and which are still open
- Know the real current state, including what's broken or blocked
- Execute the next action without asking a question
- Avoid re-doing finished work and re-trying failed approaches

Then two final passes:

- **Evidence:** every confident sentence traces to something you saw. Anything else is labelled.
- **Proportion:** every section earns its space, no fact appears twice without cause, and the
  document is shorter than what it saves the reader from reading.

If any check fails, fix that section rather than adding prose elsewhere.
