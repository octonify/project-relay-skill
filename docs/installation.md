# Installing `project-relay-git`

This installs the skill **into one project**, so it is available in that project only and travels
with the repository if you commit it.

## Prerequisites

- [Claude Code](https://claude.com/claude-code) (CLI, desktop, web, or IDE extension)
- `git`
- Python 3.9+ on `PATH` — used by the bundled context helper (`python` or `python3`)
- Optional: the [GitHub CLI](https://cli.github.com/) (`gh`), authenticated. Without it the skill
  records pull-request and issue state as `Not verified` instead of looking it up.

## Install

Run from the root of the project you want handoffs for.

**macOS / Linux / Git Bash:**

```bash
git clone --depth 1 https://github.com/octonify/project-relay-skill.git /tmp/project-relay-skill
mkdir -p .claude/skills .claude/commands
cp -r /tmp/project-relay-skill/skills/project-relay-git .claude/skills/project-relay-git
cp /tmp/project-relay-skill/skills/project-relay-git/commands/handoff.md .claude/commands/handoff.md
rm -rf /tmp/project-relay-skill
```

**Windows PowerShell:**

```powershell
$tmp = Join-Path $env:TEMP 'project-relay-skill'
Remove-Item -Recurse -Force $tmp -ErrorAction SilentlyContinue
git clone --depth 1 https://github.com/octonify/project-relay-skill.git $tmp
New-Item -ItemType Directory -Force .claude\skills, .claude\commands | Out-Null
Copy-Item -Recurse -Force "$tmp\skills\project-relay-git" .claude\skills\project-relay-git
Copy-Item -Force "$tmp\skills\project-relay-git\commands\handoff.md" .claude\commands\handoff.md
Remove-Item -Recurse -Force $tmp
```

### Where it lands

```
your-project/
├── .claude/
│   ├── skills/
│   │   └── project-relay-git/     ← the skill: SKILL.md, references, assets, scripts
│   └── commands/
│       └── handoff.md             ← makes /handoff, /handoff master, /handoff full work
└── docs/handoffs/                 ← created on first run, holds the documents produced
```

### How Claude finds it

Claude Code scans `.claude/skills/*/SKILL.md` in the current project at session start and reads
the `name` and `description` from each file's frontmatter. When your request matches the
description, the skill body loads. `.claude/commands/handoff.md` registers `/handoff` as a slash
command in the same project.

Start a new Claude Code session after installing — an already-running session will not pick up a
newly added skill.

## Verify

Three checks, in increasing strength.

**1. Files are in place:**

```bash
ls .claude/skills/project-relay-git/SKILL.md .claude/commands/handoff.md
```

**2. The helper runs against your repository:**

```bash
python .claude/skills/project-relay-git/scripts/handoff_context.py --project-root . --scope check
```

It should print your branch, HEAD commit, and working-tree state. If it prints
`not a git repository`, you are outside the repo root or this project isn't Git-backed — this
variant expects a Git-backed project.

**3. Claude actually uses it.** In a new session in this project, run:

```
/handoff
```

Expected: Claude runs the context helper, then writes one file named
`docs/handoffs/YYYY-MM-DD_001_<scope>-handoff.md` and reports the path. If `/handoff` is not
recognised as a command, the command file is missing or the session predates the install.

## Update

Re-run the install commands. They overwrite in place. Check
`skills/project-relay-git/CHANGELOG.md` in this repository first — section names can change
between pre-1.0 versions, and existing handoff documents are not migrated automatically.

To pin a specific release instead of tracking `main`, clone a tag:

```bash
git clone --depth 1 --branch project-relay-git-v0.1.0 https://github.com/octonify/project-relay-skill.git /tmp/project-relay-skill
```

## Uninstall

```bash
rm -rf .claude/skills/project-relay-git .claude/commands/handoff.md
```

Handoff documents under `docs/handoffs/` are your project's content and are left alone. Delete
them separately if you want them gone.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `/handoff` not recognised | Command file missing, or session started before install | Confirm `.claude/commands/handoff.md` exists, then start a new session |
| Claude writes a summary instead of a handoff | Skill not discovered | Confirm `.claude/skills/project-relay-git/SKILL.md` exists and its frontmatter is intact |
| Helper reports `not a git repository` | Run from outside the repo root | `cd` to the repository root, or pass `--project-root <path>` |
| PR and issue state comes back `Not verified` | `gh` missing or not authenticated | `gh auth login`, or accept the labelled gap — it is honest, not broken |
| Handoffs appear somewhere other than `docs/handoffs/` | The project already had `.handoffs/`, `handoffs/`, or `docs/handoff/` | Expected: an existing project convention wins over the default |
