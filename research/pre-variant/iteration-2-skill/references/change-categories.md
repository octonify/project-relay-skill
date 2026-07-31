# Change categories — recall checklist

Use this while writing "What Changed" in a Daily Handoff, or section 12 of a Master Handoff.

It is a memory aid, not a template. Skim it, note where something actually moved this session,
and write only those. Reproducing every heading with "n/a" underneath makes the document longer
and less trustworthy — the reader can no longer tell effort from coverage.

Why bother with a list this broad: the reflex is to record code and file edits, because those are
visible in the editor. The changes that break the next session are usually elsewhere — a rotated
secret, an approval gate someone added, a spreadsheet column renamed, a DNS TTL. Those leave no
trace in a diff.

## Files and documents
Created, edited, deleted, moved, renamed. Documents replaced, versions superseded. Exact paths.

## Code and repository state
Code files changed, branches created or used, commits, merges, pull requests, dependencies,
configuration, tests, builds, migrations, local vs remote repository divergence.

## Systems and infrastructure
Environment configuration, servers, containers, databases, storage, DNS, CDN, hosting, deployment,
CI/CD, secrets and environment variables, access control, backup and recovery.

## Data
Data created, updated, migrated, deleted. Schemas, fields, records, imports and exports,
validation, data mapping, data quality, source-of-truth changes, snapshots.

Irreversible data operations deserve a line in "Work That Must Not Be Repeated" as well.

## Product and user experience
Features, user flows, screens, components, prototypes, design systems, interactions,
accessibility, responsive behavior, user journeys, acceptance criteria.

## Content and media
Copy, pages, articles, assets, images, video, metadata, search optimization fields, structured
data, internal links, calls to action, translations, content status (draft/review/published).

## Process and operations
Workflows, roles and responsibilities, approval gates, standard operating procedures, automations,
agent instructions, skills, tool access, reporting structure, naming conventions, handoff
procedures.

A process change is invisible to a code reader and binding on them anyway — record it.

## External tools and platforms
Third-party service settings, accounts, integrations, APIs, plugins, applications, analytics,
advertising platforms, CRM, email, calendar, cloud services.

## Project management state
Scope, priority, timeline, milestones, owners, dependencies, budget, risks, approval status.

---

## Recording format

```markdown
- Change:
- Location:
- Previous State:
- New State:
- Reason:
- Validation:
```

`Previous State` is the field most often guessed and the most harmful to guess — it's what someone
will use to roll back. If you didn't observe it, write `Unknown — not captured before change`.

`Validation` says how you know the change took effect, or `Not validated` if you don't. Both are
acceptable answers; silence is not.
