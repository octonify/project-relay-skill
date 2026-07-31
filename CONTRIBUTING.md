# Contributing

## Repository model

One repository, one directory per variant under `skills/`. Variants are independently versioned
and independently installable; they are **not** long-lived branches.

Development happens on short-lived branches off `main` — `feat/…`, `fix/…`, `docs/…` — merged by
pull request and deleted afterwards.

## Adding a variant

A new variant is a new directory under `skills/`, containing at minimum:

```
skills/<variant-name>/
├── SKILL.md          # frontmatter: name, description
├── README.md         # what it produces, commands, scope boundary
├── VERSION
├── CHANGELOG.md
└── evals/evals.json
```

It must be installable and understandable on its own. `shared/continuity-contract.md` states the
principles every variant honours, but nothing in a variant should *require* reading it — a user
installs one directory, not a framework.

Do not change files inside another variant to make yours work. Shared behaviour that genuinely
needs to be shared goes in `shared/`, and only after two variants actually need it.

## Changing skill behaviour

Skills are prompts, and prompt changes are easy to believe and hard to verify. A change to
`SKILL.md`, a reference, or a template that alters what the skill produces needs evidence:

1. Run the variant's `evals/evals.json` cases before and after.
2. Save outputs, grades, and timings under `research/`.
3. Say in the pull request what changed in the output, not only what changed in the text.

Numbers from a single run per case are weak — measured run-to-run variance on identical input has
reached 27%. A small delta is not a result. Say so rather than rounding it up into one.

Bug fixes to scripts, documentation, and typos don't need eval runs.

## Pull requests

- One concern per PR. A variant change and a repository-structure change are two PRs.
- Update the variant's `CHANGELOG.md` and bump its `VERSION` when behaviour changes.
- If installation steps change, update `docs/installation.md` **and** run them in a clean fixture
  before claiming they work.
- Don't present unbuilt variants as available in the README or the repository description.

## Reporting problems with generated handoffs

The useful bug report includes the handoff the skill produced, what was wrong with it, and what
the repository state actually was. "It was too long" is hard to act on; "it repeated the risk
register in both documents, here are both files" is a fix.
