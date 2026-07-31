---
name: project-relay
description: Creates operational handoff documents that let any person or agent continue a project accurately without reading the conversation history — a dated Daily Handoff for a session plus a cumulative canonical Master Handoff. Use this skill whenever the user runs /handoff, /handoff master, or /handoff full, and also whenever they mention a handoff, handover, session wrap-up, end-of-day summary, continuity doc, status snapshot, project state document, onboarding another agent or contributor, "picking this up tomorrow", "so the next session knows where we left off", or transferring a project to someone else — even if they never say the word "handoff". Prefer this skill over writing an ad-hoc summary: a summary recounts a conversation, a handoff records verified state, exact next action, and authoritative sources.
---

# Project Relay

## Why this exists

A conversation summary tells someone what was talked about. A handoff tells them what is
*true right now* and what to do next. The difference matters because the reader has no access
to the conversation — they have only your document, the repo, and whatever systems it points at.

Every handoff you produce is judged by one test: **can a competent stranger continue this
project correctly, without asking questions and without repeating finished work?** If yes, the
handoff is good. If they would have to guess at a path, a status, or a decision, it is not.

This drives two habits that run through everything below:

- **Separate what happened from what was hoped for.** Completed, planned, attempted, failed,
  blocked, approved, assumed, and unverified are eight different things. Collapsing them is the
  single most damaging thing a handoff can do, because the reader will act on "done" and find
  it isn't.
- **Prefer an honest gap to a smooth guess.** `Status: Unknown — not verified this session` is
  useful. An invented previous-state value is worse than nothing, because it looks verified.

## Two documents

| | Daily Handoff | Master Handoff |
|---|---|---|
| Scope | One session or day | Whole project |
| Job | Record what changed | Integrate change into full project state |
| Storage | New dated file, kept forever | One stable canonical file, updated in place |
| History | This session only | Only history needed to understand the path here |
| Reader need | Continue tomorrow | Take over the project cold |

The Daily Handoff is the session's operational memory. The Master Handoff is the project's
canonical memory. Neither is a chat log.

## Commands

Route on what the user typed:

- **`/handoff`** → one Daily Handoff for this session. Nothing else changes.
- **`/handoff master`** → update the Master Handoff in place from verified current state and
  any Daily Handoffs not yet incorporated. No new Daily file.
- **`/handoff full`** → Daily Handoff first, then fold its verified content into the Master.
  Order matters: the Daily is the evidence the Master update draws on.

If the user asked for continuity in plain language ("wrap up so I can resume tomorrow"), treat
it as `/handoff`. If they say they're passing the project to someone else, they need the Master
too — that's `/handoff full`.

## Workflow

### 1. Gather context before writing a word

Run the bundled helper first — it resolves the target directory, computes the next filename,
and dumps repository state so you don't hand-assemble any of it:

```bash
python <skill-dir>/scripts/handoff_context.py --project-root <project-root>
```

It prints the handoff directory, the next sequence number for today, existing Daily files and
which are already incorporated in the Master, current branch/commit/uncommitted files, and
recent commits. Read its output, then fill gaps yourself:

- Re-read the session for decisions, rejected options, and corrections the user made. User
  corrections are high-value: they usually encode a constraint that isn't written anywhere else.
- Check the things you claim to have validated. A test you never ran is not a passing test.
- Note what you touched but did not verify. That list belongs in Open/Unverified, not in
  Completed.

If the project isn't a git repo, or the helper fails, gather what you can by hand and say in
the document which state you could not verify. Missing tooling is a reason to mark items
unknown, not a reason to skip the handoff.

### 2. Decide the honest scope

Name the session's actual scope, not its ambition. If the objective was "ship auth" and you
got as far as the login form, the scope is the login form and the objective/outcome gap is
itself information the reader needs.

### 3. Write the document

For a Daily Handoff, read `references/daily-handoff.md` for the twelve sections and what
belongs in each. Start from `assets/daily-handoff-template.md`.

For a Master Handoff, read `references/master-handoff.md` for the twenty sections and the
cumulative update rules. If no Master exists yet, start from `assets/master-handoff-template.md`.

When recording changes, `references/change-categories.md` is a checklist across files, code,
infrastructure, data, product, content, process, external tools, and project management. Skim
it to catch change types you'd otherwise forget — a DNS record or an approval-gate change is as
real as a code edit. It is a prompt for recall, not a set of headings to reproduce; only include
categories where something actually changed.

### 4. Deliver, don't paste

Write the `.md` file(s) and tell the user the exact paths. Don't dump full file contents into
the conversation unless they ask — the document's purpose is to exist at a stable location, and
a wall of text in chat competes with the file for authority. A short confirmation is right:
what you wrote, where, and the one next action you recorded.

## Storage and naming

Default location is `docs/handoffs/` under the project root. If the project already has a
handoff directory somewhere else, use that instead — an existing convention beats this default,
and the helper script reports what it found.

```
docs/handoffs/
├── _master-handoff.md              ← canonical, updated in place
├── 2026-07-29_001_setup-handoff.md
└── 2026-07-30_001_auth-handoff.md
```

Daily files: `YYYY-MM-DD_NNN_<scope>-handoff.md`. Dated and zero-padded so they sort
chronologically; `NNN` increments for multiple handoffs on one date; `<scope>` is a short
kebab-case hint at the session's subject.

The Master keeps the filename `_master-handoff.md` permanently and records its version inside:

```markdown
Version: 3.0
Last Updated: 2026-07-30
```

Resist `_master-handoff-v2.md` or `-final-new.md`. Versioned filenames are how a project ends up
with four Masters and no canonical one — the whole value of the Master is that there is exactly
one place to look. Archive a dated snapshot only when someone genuinely needs a frozen copy
(an audit, a contract milestone), and say why in the document.

## Updating the Master safely

The Master is the one document a reader trusts completely, so a careless update does real
damage. Before writing:

1. Read the existing Master fully. You are integrating, not regenerating.
2. Place new information in the section where it belongs. Appending everything to the end is
   how a Master decays into a pile of dated notes.
3. Correct stale statuses rather than leaving both the old and new claim standing.
4. Mark superseded decisions and sources as superseded, with what replaced them and why. A
   silently deleted decision looks like it was never made, and someone will re-litigate it.
5. Resolve contradictions if you can verify which side is true; if you can't, record the
   contradiction, both sources, and what evidence would settle it.
6. Rewrite the Executive Summary and the single Immediate Next Action last, once the rest
   reflects reality.

Never replace the old Master until valid existing information has been carried forward.

## Quality rules

**Exact identifiers.** "The main file", "the report", "the latest version", "the current branch"
are unusable to someone who wasn't there. Write `src/auth/session.ts`, `PR #412`,
`branch feat/auth-relay`, `commit a3f9c21`. If you don't know the identifier, say so — a marked
gap can be filled, a vague reference silently misleads.

**Validated means evidenced.** Only put an item in Validated/Approved if something outside your
own expectation confirmed it: a test run, an observed result, a build, a human approval. "Should
work" belongs in Open/Unverified.

**Next action must be executable.** "Continue development" isn't an instruction. The reader
needs the action, where to start, required inputs, expected output, acceptance criteria, what
must not be changed, and what would block them. Exactly one immediate next action; anything
else goes in a prioritized queue.

**Record what must not be repeated.** Finished reviews, locked decisions, rejected approaches
and *why* they failed. This section quietly saves the most time, because the default behavior of
a fresh agent is to try the obvious thing that was already tried.

## Acceptance check before you finish

Read your own document as the stranger. It's ready when they could:

- Tell what is done from what is merely planned
- Find every file, branch, ticket, or system you mention
- See which decisions are final and which are still open
- Know the real current state, including what's broken or blocked
- Execute the next action without asking a question
- Avoid re-doing finished work and re-trying failed approaches

If any of those fails, fix that section rather than adding prose elsewhere.
