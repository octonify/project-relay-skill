# Research archive

Evaluation evidence produced while developing Project Relay, kept because it explains *why* the
shipped skill is shaped the way it is. **None of this is part of the installable skill.**

These iterations predate the split into project-type variants. They tested a single generic
`project-relay` skill against three fixture projects (a Git-backed web app, a Master-update
scenario, and a non-technical project). `skills/project-relay-git/` is the Git-scoped successor.

## Contents

```
research/
├── build_fixtures.py           # builds the three fixture projects, traps included
├── pre-variant/                # the generic skill these iterations actually ran
│   ├── iteration-1-skill/
│   └── iteration-2-skill/
├── iteration-1/
│   ├── benchmark.json / .md    # pass rates, timing, tokens
│   ├── feedback.json           # human review that drove iteration 2
│   └── eval-*/<config>/        # outputs/, grading.json, timing.json
├── iteration-2/
│   ├── benchmark.json / .md
│   └── eval-*/<config>/
└── project-relay-git-v0.1.0/   # variant-era evidence: pre-revision, run-A/B,
                                # dogfood, e2e-validation, post-merge
```

Per-run copies of the fixture projects were dropped; only the generated documents, grades, and
timings are kept. `iteration-1` compares the skill against no skill; `iteration-2` compares the
revised skill against the iteration-1 snapshot.

## What these runs established

**Iteration 1 — the failure mode is length, not accuracy.** With-skill outputs contained no
fabrications, but ran 8× the source material on the session-transcript case (28,896 chars from
3,605) and 20× on the non-technical case (60,185 from 2,971). Cause: the section lists read as
checklists to fill, so every heading got prose whether or not anything had happened. Fixed by
reframing them as menus and instructing deletion of empty sections.

**Iteration 2 — structure, not style.** Session-narrative bleed and repeated rationale were gone;
pass rate rose 86.7% → 92.3% and runs got faster and cheaper. Every remaining failure was size,
and the residue was structural: the risk register, constraints block, do-not-repeat list,
next-action block, and continuation-sources table appeared in *both* documents. That produced the
single-home rules now in `project-relay-git`.

## Two cautions for anyone reading the numbers

**Variance.** The iteration-1 skill produced 28,896 characters on one case in one round and
21,085 on the same case with identical input in another — 27% run-to-run variance, n=1 per cell.
Only the largest deltas here are outside noise.

**Two known eval bugs, unfixed at the time these ran:**

1. eval-1 assertions 16 and 17 conflict. #17 rewards labelling unverified claims; the natural
   phrasing "not verified this session" is exactly what #16 penalises as session narrative. Both
   arms were scored against a contradiction.
2. eval-2's no-fabrication assertion is scoped to git/build/CI state only. It passed while the
   revised Master invented a source-precedence rule that appeared in no input. That gap is why
   the shipped skill says explicitly that an undecided precedence rule is an open decision, not a
   rule.

**Also note:** eval-1 hands the baseline a well-structured existing Master to imitate, so
update-in-place cases leak the format for free and discriminate weakly between arms. Formatting
similarity is not evidence the skill helped.

The character caps added to iteration-2's assertions were deliberately **not** carried into the
shipped skill — they penalise complex projects for being complex. See
`skills/project-relay-git/CHANGELOG.md`.
