# The Project Relay continuity contract

The small set of principles every Project Relay variant honours, whatever kind of project it
serves. Everything else — sections, file names, tooling, vocabulary — belongs to the variant.

This document is deliberately short. A variant must be installable and understandable without it;
it exists so that future variants stay recognisably the same product, not so that they share a
framework.

## 1. A handoff records state, not conversation

A summary recounts what was discussed. A handoff states what is true now and what to do next. The
reader has no access to the session — only the document and the systems it points at.

## 2. Evidence or a label, never a guess

Every factual claim traces to something observed: a file read, a command run, a person's explicit
confirmation. Anything else is `Unknown`, `Not verified`, `Pending Confirmation`, or `Proposed`.

An invented value is worse than a missing one, because it looks verified. Trust in a handoff is
all-or-nothing: one confident sentence found false forces the reader to re-check every other
sentence.

## 3. Inherited claims are not evidence

A line in an existing canonical document records what someone believed when they wrote it. When
you carry it forward you are re-asserting it. For each inherited claim: verify and keep, mark it
unverified, mark it stale with what you now know, or supersede it.

## 4. States stay distinct

Completed, planned, attempted, blocked, approved, superseded, unknown, and unverified are eight
different things. Collapsing them is the most damaging thing a handoff can do, because the reader
acts on "done" and finds it isn't.

## 5. Two documents, one home per fact

A **session document** records what materially changed and how the session ended. A **canonical
document** holds current project state after verified changes are integrated. Both must be
independently understandable — which is satisfied by a line of context plus a pointer, not by a
second copy that will drift.

## 6. The next action must be executable

One immediate next action, startable from the state the document describes. If it depends on a
missing input, access, decision, or answer from a named person, then obtaining that prerequisite
is the next action.

## 7. Proportion, without deletion of substance

Documents match the project's real complexity. Cut repetition, scaffolding, and restated source
material. Never cut a decision, constraint, or blocker to make the document shorter.

## 8. One canonical file, updated in place

The canonical document keeps its filename permanently and carries its version inside. Versioned
filenames produce four candidates and no canonical one.

---

## Variants

| Variant | Project type | Status |
|---|---|---|
| `project-relay-git` | Git-backed software projects | In development |

Future variants (design, research, operations) are not designed yet. They will be defined from
validated experience with `project-relay-git`, not in advance of it.
