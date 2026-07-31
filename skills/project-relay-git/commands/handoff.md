---
description: Write a Daily Handoff, update the canonical Master Handoff, or both
argument-hint: "[master|full]"
---

Invoke the `project-relay-git` skill and follow it for this request.

Argument given: `$ARGUMENTS`

Route on that argument:

- empty → **Daily Handoff only.** Write one dated Daily Handoff for this session. Do not touch
  the Master.
- `master` → **Master Handoff only.** Update `_master-handoff.md` in place from verified current
  state plus any Daily Handoffs not yet incorporated. Do not create a new Daily file, and do not
  create a second Master file under any name.
- `full` → **Both, in order.** Write the Daily first, then fold its verified content into the
  Master. The Daily is the evidence the Master update draws on, so the order matters.
- anything else → treat the argument as a scope hint for a Daily Handoff, and say that you did.

Before writing anything, run the skill's context helper so repository state comes from
observation rather than memory:

```bash
python .claude/skills/project-relay-git/scripts/handoff_context.py --project-root . --scope <slug>
```

Then apply the skill's evidence rule, single-home rules, and acceptance checks. Report the exact
paths you wrote and the immediate next action; do not paste the documents into the conversation
unless asked.
