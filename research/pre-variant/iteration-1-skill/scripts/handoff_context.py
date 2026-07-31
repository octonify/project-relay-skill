#!/usr/bin/env python3
"""Gather everything a handoff needs to know before it is written.

Resolves the handoff directory, computes the next Daily filename, lists existing
Daily Handoffs and whether the Master has incorporated them, and dumps repository
state. Read the output, then fill the gaps that only the session itself knows.

Usage:
    python handoff_context.py [--project-root PATH] [--scope SLUG] [--json]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

# Checked in order; first existing directory wins so a project's own convention
# beats our default.
CANDIDATE_DIRS = [
    "docs/handoffs",
    ".handoffs",
    "handoffs",
    "docs/handoff",
]
DEFAULT_DIR = "docs/handoffs"
MASTER_NAME = "_master-handoff.md"
DAILY_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})_(\d{3})_(.+)-handoff\.md$")


def run_git(root: Path, *args: str) -> str | None:
    try:
        out = subprocess.run(
            ["git", *args],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=20,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if out.returncode != 0:
        return None
    return out.stdout.strip()


def git_state(root: Path) -> dict:
    if run_git(root, "rev-parse", "--is-inside-work-tree") != "true":
        return {"is_repo": False}

    porcelain = run_git(root, "status", "--porcelain") or ""
    changed = [line for line in porcelain.splitlines() if line.strip()]
    log = run_git(root, "log", "-10", "--pretty=%h %ad %s", "--date=short") or ""
    remote_url = run_git(root, "config", "--get", "remote.origin.url")
    branch = run_git(root, "rev-parse", "--abbrev-ref", "HEAD")
    ahead_behind = None
    if branch:
        upstream = run_git(root, "rev-parse", "--abbrev-ref", f"{branch}@{{upstream}}")
        if upstream:
            counts = run_git(root, "rev-list", "--left-right", "--count", f"{upstream}...HEAD")
            if counts:
                behind, ahead = counts.split()
                ahead_behind = {"upstream": upstream, "ahead": int(ahead), "behind": int(behind)}

    return {
        "is_repo": True,
        "branch": branch,
        "head_commit": run_git(root, "rev-parse", "--short", "HEAD"),
        "head_subject": run_git(root, "log", "-1", "--pretty=%s"),
        "remote_origin": remote_url,
        "upstream_divergence": ahead_behind,
        "uncommitted_count": len(changed),
        "uncommitted": changed[:40],
        "recent_commits": log.splitlines(),
        "commits_today": (
            run_git(root, "log", "--since=midnight", "--pretty=%h %s") or ""
        ).splitlines(),
    }


def resolve_handoff_dir(root: Path) -> tuple[Path, bool]:
    """Return (dir, existed). Does not create anything."""
    for rel in CANDIDATE_DIRS:
        candidate = root / rel
        if candidate.is_dir():
            return candidate, True
    return root / DEFAULT_DIR, False


def scan_dailies(handoff_dir: Path) -> list[dict]:
    if not handoff_dir.is_dir():
        return []
    found = []
    for path in sorted(handoff_dir.iterdir()):
        m = DAILY_RE.match(path.name)
        if m:
            found.append(
                {
                    "file": path.name,
                    "date": m.group(1),
                    "seq": m.group(2),
                    "scope": m.group(3),
                }
            )
    return found


def master_info(handoff_dir: Path, dailies: list[dict]) -> dict:
    master = handoff_dir / MASTER_NAME
    if not master.is_file():
        return {"exists": False, "path": str(master)}
    text = master.read_text(encoding="utf-8", errors="replace")

    def field(label: str) -> str | None:
        m = re.search(rf"^{re.escape(label)}:\s*(.+)$", text, re.MULTILINE)
        return m.group(1).strip() if m else None

    # A Daily is treated as incorporated when the Master mentions its filename,
    # which is what section 20's table does.
    not_incorporated = [d["file"] for d in dailies if d["file"] not in text]
    return {
        "exists": True,
        "path": str(master),
        "version": field("Version"),
        "last_updated": field("Last Updated"),
        "current_phase": field("Current Phase"),
        "overall_status": field("Overall Status"),
        "line_count": len(text.splitlines()),
        "dailies_not_yet_incorporated": not_incorporated,
    }


def next_daily(handoff_dir: Path, dailies: list[dict], scope: str) -> dict:
    today = date.today().isoformat()
    used = [int(d["seq"]) for d in dailies if d["date"] == today]
    seq = max(used) + 1 if used else 1
    slug = re.sub(r"[^a-z0-9]+", "-", scope.lower()).strip("-") or "project"
    name = f"{today}_{seq:03d}_{slug}-handoff.md"
    return {
        "date": today,
        "sequence": f"{seq:03d}",
        "filename": name,
        "full_path": str(handoff_dir / name),
        "note": "Replace the scope slug with a short kebab-case hint at this session's subject.",
    }


def build(root: Path, scope: str) -> dict:
    handoff_dir, existed = resolve_handoff_dir(root)
    dailies = scan_dailies(handoff_dir)
    return {
        "project_root": str(root),
        "project_name": root.name,
        "handoff_dir": str(handoff_dir),
        "handoff_dir_exists": existed,
        "handoff_dir_action": (
            "Use existing directory." if existed
            else f"Create {handoff_dir} before writing (project convention not found)."
        ),
        "existing_dailies": dailies,
        "master": master_info(handoff_dir, dailies),
        "next_daily": next_daily(handoff_dir, dailies, scope),
        "git": git_state(root),
    }


def render(ctx: dict) -> str:
    out: list[str] = []
    add = out.append
    add(f"PROJECT      {ctx['project_name']}  ({ctx['project_root']})")
    add(f"HANDOFF DIR  {ctx['handoff_dir']}")
    add(f"             {ctx['handoff_dir_action']}")
    add("")
    nd = ctx["next_daily"]
    add(f"NEXT DAILY   {nd['filename']}")
    add(f"             -> {nd['full_path']}")
    add(f"             {nd['note']}")
    add("")

    m = ctx["master"]
    if m["exists"]:
        add(f"MASTER       {m['path']}")
        add(f"             version={m['version']}  last_updated={m['last_updated']}")
        add(f"             phase={m['current_phase']}  status={m['overall_status']}")
        add(f"             {m['line_count']} lines - read it fully before updating in place")
        pending = m["dailies_not_yet_incorporated"]
        if pending:
            add(f"             NOT yet incorporated: {', '.join(pending)}")
        else:
            add("             All existing Daily Handoffs appear incorporated")
    else:
        add(f"MASTER       none yet - would be created at {m['path']}")
        add("             start from assets/master-handoff-template.md, Version: 1.0")
    add("")

    dailies = ctx["existing_dailies"]
    if dailies:
        add(f"EXISTING DAILIES ({len(dailies)}), newest last:")
        for d in dailies[-8:]:
            add(f"  {d['file']}")
    else:
        add("EXISTING DAILIES  none")
    add("")

    g = ctx["git"]
    if not g.get("is_repo"):
        add("GIT          not a git repository - record repository state as Unknown/N-A")
    else:
        add(f"GIT          branch={g['branch']}  head={g['head_commit']} {g['head_subject']!r}")
        if g.get("remote_origin"):
            add(f"             origin={g['remote_origin']}")
        div = g.get("upstream_divergence")
        if div:
            add(
                f"             vs {div['upstream']}: ahead {div['ahead']}, behind {div['behind']}"
            )
        else:
            add("             no upstream tracking branch")
        add(f"             uncommitted files: {g['uncommitted_count']}")
        for line in g["uncommitted"][:20]:
            add(f"               {line}")
        if g["uncommitted_count"] > 20:
            add(f"               ... and {g['uncommitted_count'] - 20} more")
        today_commits = g.get("commits_today") or []
        add(f"             commits since midnight: {len(today_commits)}")
        for line in today_commits[:10]:
            add(f"               {line}")
        add("             recent commits:")
        for line in g["recent_commits"][:10]:
            add(f"               {line}")
    add("")
    add("Repository state is only part of the story. Session decisions, rejected options,")
    add("user corrections, and anything you changed outside the repo are not in this output:")
    add("recover those from the session itself, and mark what you could not verify.")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--project-root", default=os.getcwd())
    ap.add_argument("--scope", default="project", help="short slug for the Daily filename")
    ap.add_argument("--json", action="store_true", help="emit raw JSON instead of a report")
    args = ap.parse_args()

    root = Path(args.project_root).expanduser().resolve()
    if not root.is_dir():
        print(f"error: project root not found: {root}", file=sys.stderr)
        return 1

    ctx = build(root, args.scope)
    print(json.dumps(ctx, indent=2) if args.json else render(ctx))
    return 0


if __name__ == "__main__":
    sys.exit(main())
