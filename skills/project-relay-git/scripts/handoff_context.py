#!/usr/bin/env python3
"""Gather verified repository and handoff state before a handoff is written.

Resolves the handoff directory, computes the next Daily filename, lists existing
Daily Handoffs and whether the Master has incorporated them, and dumps Git state
(branch, HEAD, staged/unstaged/untracked work, upstream divergence, stashes, tags,
recent commits). If the GitHub CLI is present and authenticated, it also reports
open pull requests and issues.

Everything printed here was observed. Everything absent from it is not evidence:
session decisions, rejected options, user corrections, and anything changed outside
the repository must come from the session itself and be labelled accordingly.

Usage:
    python handoff_context.py [--project-root PATH] [--scope SLUG] [--json] [--no-gh]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
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


def run(cmd: list[str], cwd: Path, timeout: int = 20) -> str | None:
    try:
        out = subprocess.run(
            cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if out.returncode != 0:
        return None
    return out.stdout.strip()


def run_git(root: Path, *args: str) -> str | None:
    return run(["git", *args], root)


def classify_porcelain(porcelain: str) -> dict:
    """Split `git status --porcelain` into staged / unstaged / untracked."""
    staged: list[str] = []
    unstaged: list[str] = []
    untracked: list[str] = []
    for line in porcelain.splitlines():
        if not line.strip():
            continue
        index, worktree, path = line[0], line[1], line[3:]
        if index == "?" and worktree == "?":
            untracked.append(path)
            continue
        if index not in (" ", "?"):
            staged.append(f"{index} {path}")
        if worktree not in (" ", "?"):
            unstaged.append(f"{worktree} {path}")
    return {"staged": staged, "unstaged": unstaged, "untracked": untracked}


def git_state(root: Path) -> dict:
    if run_git(root, "rev-parse", "--is-inside-work-tree") != "true":
        return {"is_repo": False}

    porcelain = run_git(root, "status", "--porcelain") or ""
    work = classify_porcelain(porcelain)
    branch = run_git(root, "rev-parse", "--abbrev-ref", "HEAD")

    ahead_behind = None
    if branch:
        upstream = run_git(root, "rev-parse", "--abbrev-ref", f"{branch}@{{upstream}}")
        if upstream:
            counts = run_git(root, "rev-list", "--left-right", "--count", f"{upstream}...HEAD")
            if counts:
                behind, ahead = counts.split()
                ahead_behind = {
                    "upstream": upstream,
                    "ahead": int(ahead),
                    "behind": int(behind),
                }

    stash = run_git(root, "stash", "list") or ""
    diffstat = run_git(root, "diff", "--stat", "HEAD") or ""

    return {
        "is_repo": True,
        "branch": branch,
        "detached_head": branch == "HEAD",
        "head_commit": run_git(root, "rev-parse", "--short", "HEAD"),
        "head_subject": run_git(root, "log", "-1", "--pretty=%s"),
        "head_date": run_git(root, "log", "-1", "--pretty=%ad", "--date=short"),
        "remote_origin": run_git(root, "config", "--get", "remote.origin.url"),
        "upstream_divergence": ahead_behind,
        "staged": work["staged"],
        "unstaged": work["unstaged"],
        "untracked": work["untracked"],
        "uncommitted_count": len(work["staged"]) + len(work["unstaged"]) + len(work["untracked"]),
        "worktree_clean": not porcelain.strip(),
        "diffstat_vs_head": diffstat.splitlines()[-1] if diffstat else None,
        "stash_count": len([s for s in stash.splitlines() if s.strip()]),
        "latest_tag": run_git(root, "describe", "--tags", "--abbrev=0"),
        "recent_commits": (
            run_git(root, "log", "-10", "--pretty=%h %ad %s", "--date=short") or ""
        ).splitlines(),
        "commits_today": (
            run_git(root, "log", "--since=midnight", "--pretty=%h %s") or ""
        ).splitlines(),
    }


def gh_state(root: Path, branch: str | None, enabled: bool) -> dict:
    """Open PRs and issues, but only when gh can actually answer."""
    if not enabled:
        return {"available": False, "reason": "disabled with --no-gh"}
    if not shutil.which("gh"):
        return {"available": False, "reason": "gh CLI not installed"}
    if run(["gh", "auth", "status"], root, timeout=15) is None:
        return {"available": False, "reason": "gh CLI not authenticated"}

    prs = run(
        ["gh", "pr", "list", "--state", "open", "--limit", "20",
         "--json", "number,title,headRefName,isDraft"],
        root, timeout=30,
    )
    issues = run(
        ["gh", "issue", "list", "--state", "open", "--limit", "20",
         "--json", "number,title"],
        root, timeout=30,
    )
    if prs is None and issues is None:
        return {"available": False, "reason": "gh could not reach the repository"}

    def parse(raw: str | None) -> list:
        try:
            return json.loads(raw) if raw else []
        except json.JSONDecodeError:
            return []

    pr_list = parse(prs)
    return {
        "available": True,
        "open_prs": pr_list,
        "pr_for_current_branch": [
            p for p in pr_list if p.get("headRefName") == branch
        ],
        "open_issues": parse(issues),
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

    # A Daily counts as incorporated when the Master names its filename, which is
    # what the Incorporated Daily Handoffs table does.
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


def build(root: Path, scope: str, use_gh: bool) -> dict:
    handoff_dir, existed = resolve_handoff_dir(root)
    dailies = scan_dailies(handoff_dir)
    git = git_state(root)
    return {
        "project_root": str(root),
        "project_name": root.name,
        "handoff_dir": str(handoff_dir),
        "handoff_dir_exists": existed,
        "handoff_dir_action": (
            "Use existing directory." if existed
            else f"Create {handoff_dir} before writing (no project convention found)."
        ),
        "existing_dailies": dailies,
        "master": master_info(handoff_dir, dailies),
        "next_daily": next_daily(handoff_dir, dailies, scope),
        "git": git,
        "github": gh_state(root, git.get("branch"), use_gh),
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
        add("GIT          not a git repository - this skill's Git sections do not apply.")
        add("             Record repository state as Not applicable, not as Unknown.")
    else:
        add(f"GIT          branch={g['branch']}  head={g['head_commit']} {g['head_subject']!r}")
        if g.get("detached_head"):
            add("             DETACHED HEAD - say so; a reader will assume a branch otherwise")
        if g.get("remote_origin"):
            add(f"             origin={g['remote_origin']}")
        else:
            add("             no origin remote configured")
        div = g.get("upstream_divergence")
        if div:
            add(f"             vs {div['upstream']}: ahead {div['ahead']}, behind {div['behind']}")
        else:
            add("             no upstream tracking branch - local work is not pushed anywhere")
        if g["worktree_clean"]:
            add("             working tree CLEAN")
        else:
            add(f"             uncommitted: {g['uncommitted_count']} entries"
                f"  (staged {len(g['staged'])}, unstaged {len(g['unstaged'])},"
                f" untracked {len(g['untracked'])})")
            for label, items in (
                ("staged", g["staged"]),
                ("unstaged", g["unstaged"]),
                ("untracked", g["untracked"]),
            ):
                for entry in items[:12]:
                    add(f"               [{label}] {entry}")
                if len(items) > 12:
                    add(f"               [{label}] ... and {len(items) - 12} more")
            if g.get("diffstat_vs_head"):
                add(f"             diff vs HEAD: {g['diffstat_vs_head']}")
        if g.get("stash_count"):
            add(f"             stashes: {g['stash_count']} - easy to abandon, say they exist")
        if g.get("latest_tag"):
            add(f"             latest tag: {g['latest_tag']}")
        today_commits = g.get("commits_today") or []
        add(f"             commits since midnight: {len(today_commits)}")
        for line in today_commits[:10]:
            add(f"               {line}")
        add("             recent commits:")
        for line in g["recent_commits"][:10]:
            add(f"               {line}")
    add("")

    gh = ctx["github"]
    if not gh.get("available"):
        add(f"GITHUB       unavailable ({gh.get('reason')})")
        add("             Do not state PR or issue status you did not observe.")
    else:
        mine = gh.get("pr_for_current_branch") or []
        if mine:
            for p in mine:
                draft = " (draft)" if p.get("isDraft") else ""
                add(f"GITHUB       PR #{p['number']} for this branch{draft}: {p['title']}")
        else:
            add("GITHUB       no open PR for the current branch")
        others = [p for p in gh.get("open_prs", []) if p not in mine]
        if others:
            add(f"             {len(others)} other open PR(s):")
            for p in others[:5]:
                add(f"               #{p['number']} {p['title']}")
        issues = gh.get("open_issues") or []
        add(f"             open issues: {len(issues)}")
        for i in issues[:5]:
            add(f"               #{i['number']} {i['title']}")
    add("")

    add("This output is repository evidence only. Session decisions, rejected options, user")
    add("corrections, build/test results you did not run, and anything changed outside the repo")
    add("are not here: recover them from the session, and label what you could not verify.")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--project-root", default=os.getcwd())
    ap.add_argument("--scope", default="project", help="short slug for the Daily filename")
    ap.add_argument("--json", action="store_true", help="emit raw JSON instead of a report")
    ap.add_argument("--no-gh", action="store_true", help="skip GitHub CLI lookups")
    args = ap.parse_args()

    root = Path(args.project_root).expanduser().resolve()
    if not root.is_dir():
        print(f"error: project root not found: {root}", file=sys.stderr)
        return 1

    ctx = build(root, args.scope, use_gh=not args.no_gh)
    print(json.dumps(ctx, indent=2) if args.json else render(ctx))
    return 0


if __name__ == "__main__":
    sys.exit(main())
