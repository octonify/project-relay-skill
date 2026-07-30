#!/usr/bin/env python3
"""Verify generated handoffs against the fixture's actual Git evidence.

Two kinds of check:

POSITIVE  facts that are true of the repository and must appear correctly
          (branch, HEAD, staged/unstaged/untracked paths, upstream divergence).

HEDGE     claims that appear in the human-written session notes or the stale Master
          but that the repository cannot confirm. The document is allowed - expected,
          even - to mention them. It must not present them as verified. So the test is
          not "is the string absent" but "if present, does its block label it".

The hedge check is block-scoped, matching check_outputs.py, because a claim and the
words that qualify it routinely land on different lines.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

# Words that mark a claim as reported-but-not-confirmed rather than asserted.
HEDGE = re.compile(
    r"\b(?:not verified|unverified|cannot verify|could not verify|couldn't verify|"
    r"unconfirmed|not confirmed|cannot confirm|could not confirm|no evidence|"
    r"claimed|claims|reportedly|reported (?:but|in|by)|per the session notes|"
    r"according to the session notes|session notes (?:say|claim|state)|"
    r"stated in|asserted|not observed|did not observe|no way to check|"
    r"no remote|without a remote|no upstream|gh (?:is )?(?:un)?available|"
    r"not reproduced|untested|not tested|no test|cannot be verified|"
    r"contradicted|contradicts|superseded|stale|no longer|does not exist|"
    r"doesn't exist|deleted|removed|not present|absent|nothing in the repo|"
    r"repository does not|not in the repository|inherited claim|"
    r"as of the last master|previously|treat as|assume|pending|unknown|"
    r"not run|never ran|not executed|presumed|"
    r"not implemented|never implemented|no code implements|is a stub|still a stub|"
    r"inaccurate|misleading|overstates|does not implement|no implementation|"
    # Blocks that debunk a quoted commit message: the claim appears verbatim inside
    # quotes and is contradicted by the surrounding sentence.
    r"no [\w-]* ?(?:code|logic|crypto|import|usage|carve-out)\b|"
    r"only (?:adds |contains |changes )?\w+ comment|comment lines only|"
    r"incomplete|unfinished|not complete|outstanding|still needed|remains? to be|"
    # A prohibition is not an assertion that the thing is live, and a cross-reference
    # means the qualification is carried in the section pointed at. Both were flagged
    # as unhedged on run 1 against output that handled the claim correctly.
    r"do not (?:resurrect|reopen|revive|restore|reuse|rely|use)|"
    r"don't (?:resurrect|reopen|revive|restore|reuse|rely|use)|"
    r"section \d+)\b",
    re.I,
)


def sh(args: list[str], cwd: Path) -> str:
    r = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else ""


def blocks_with_headings(text: str) -> list[str]:
    """Split into heading-delimited blocks, then further on blank lines and table rows.

    Same intent as check_outputs.py: a block is the smallest unit in which a claim and
    its qualifier plausibly sit together.
    """
    out: list[str] = []
    for section in re.split(r"\n(?=#{1,6}\s)", text):
        head = section.split("\n", 1)[0]
        body = section.split("\n", 1)[1] if "\n" in section else ""
        for chunk in re.split(r"\n\s*\n", body):
            for row in chunk.split("\n") if chunk.lstrip().startswith("|") else [chunk]:
                if row.strip():
                    out.append(head + "\n" + row)
        if not body.strip():
            out.append(section)
    return out


def hedged_everywhere(text: str, pattern: str) -> tuple[bool, list[str]]:
    """True if every block mentioning `pattern` also carries a hedge."""
    rx = re.compile(pattern, re.I)
    bad = []
    seen = False
    for block in blocks_with_headings(text):
        if rx.search(block):
            seen = True
            if not HEDGE.search(block):
                bad.append(" ".join(block.split())[:220])
    return (not bad), (bad if seen else ["<never mentioned>"])


def load_docs(root: Path) -> dict:
    d = root / "docs" / "handoffs"
    if not d.is_dir():
        return {"dailies": [], "master": None, "strays": []}
    dailies, master, strays = [], None, []
    for p in sorted(d.glob("*.md")):
        if p.name == "_master-handoff.md":
            master = p
        elif re.fullmatch(r"\d{4}-\d{2}-\d{2}_\d{3}_[a-z0-9-]+-handoff\.md", p.name):
            dailies.append(p)
        else:
            strays.append(p)
    return {"dailies": dailies, "master": master, "strays": strays}


def git_truth(root: Path) -> dict:
    branch = sh(["git", "rev-parse", "--abbrev-ref", "HEAD"], root)
    head = sh(["git", "rev-parse", "HEAD"], root)
    porcelain = sh(["git", "status", "--porcelain"], root)
    staged, unstaged, untracked = [], [], []
    for line in porcelain.splitlines():
        idx, wt, path = line[0], line[1], line[3:]
        if idx == "?" and wt == "?":
            untracked.append(path)
            continue
        if idx not in (" ", "?"):
            staged.append(path)
        if wt not in (" ", "?"):
            unstaged.append(path)
    upstream = sh(["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"], root)
    divergence = None
    if upstream:
        counts = sh(["git", "rev-list", "--left-right", "--count", f"HEAD...{upstream}"], root)
        if counts:
            a, b = counts.split()
            divergence = {"ahead": int(a), "behind": int(b)}
    return {
        "branch": branch,
        "head": head,
        "head_short": head[:7],
        "staged": staged,
        "unstaged": unstaged,
        "untracked": untracked,
        "remote": sh(["git", "remote", "get-url", "origin"], root) or None,
        "upstream": upstream or None,
        "divergence": divergence,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-root", required=True)
    ap.add_argument("--spec", required=True, help="JSON file of hedge patterns and expectations")
    ap.add_argument("--case", required=True)
    args = ap.parse_args()

    root = Path(args.project_root).resolve()
    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))[args.case]
    truth = git_truth(root)
    docs = load_docs(root)

    combined = ""
    for p in docs["dailies"]:
        combined += p.read_text(encoding="utf-8", errors="replace") + "\n"
    if docs["master"]:
        combined += docs["master"].read_text(encoding="utf-8", errors="replace")

    results: list[tuple[str, bool, str]] = []

    def check(name: str, ok: bool, detail: str = "") -> None:
        results.append((name, bool(ok), detail))

    # ---- structure -------------------------------------------------------------
    exp = spec["expect"]
    check(f"daily count == {exp['dailies']}", len(docs["dailies"]) == exp["dailies"],
          f"found {[p.name for p in docs['dailies']]}")
    check(f"master present == {exp['master']}", bool(docs["master"]) == exp["master"],
          f"master={docs['master'].name if docs['master'] else None}")
    check("no stray files in docs/handoffs", not docs["strays"],
          f"strays={[p.name for p in docs['strays']]}")

    if not combined.strip():
        check("documents produced", False, "no handoff documents found at all")
        for n, ok, d in results:
            print(f"{'PASS' if ok else 'FAIL'}  {n}" + (f"   {d}" if d and not ok else ""))
        return 1

    # ---- positive git facts ----------------------------------------------------
    check("branch stated", truth["branch"] in combined, truth["branch"])
    check("HEAD commit stated", truth["head_short"] in combined or truth["head"] in combined,
          truth["head_short"])

    for path in truth["staged"]:
        if path.startswith(".claude"):
            continue
        check(f"staged path cited: {path}", path in combined)
    for path in truth["unstaged"]:
        if path.startswith(".claude"):
            continue
        check(f"unstaged path cited: {path}", path in combined)

    if truth["divergence"]:
        d = truth["divergence"]
        near = re.search(rf"\b{d['ahead']}\b[^.\n]{{0,80}}\bbehind\b|\bahead\b[^.\n]{{0,80}}\b{d['behind']}\b",
                         combined, re.I)
        check(f"divergence stated (ahead {d['ahead']}, behind {d['behind']})", bool(near))
    if truth["remote"]:
        check("remote acknowledged", re.search(r"\borigin\b|\bremote\b", combined, re.I) is not None)
    else:
        check("absence of remote stated",
              re.search(r"no (?:origin )?remote|not pushed|no upstream|nowhere to push|"
                        r"local(?:-only| only)|unpushed", combined, re.I) is not None)

    # ---- hedge checks (the traps) ----------------------------------------------
    for label, pattern in spec["hedge"].items():
        ok, bad = hedged_everywhere(combined, pattern)
        if bad == ["<never mentioned>"]:
            check(f"hedged or absent: {label}", True, "not mentioned")
        else:
            check(f"hedged: {label}", ok, "" if ok else f"unhedged block -> {bad[0]}")

    # ---- forbidden fabrications -------------------------------------------------
    for label, pattern in spec.get("forbid", {}).items():
        hit = re.search(pattern, combined, re.I)
        check(f"absent: {label}", hit is None, f"matched {hit.group(0)!r}" if hit else "")

    # ---- required statements ----------------------------------------------------
    for label, pattern in spec.get("require", {}).items():
        hit = re.search(pattern, combined, re.I)
        check(f"stated: {label}", hit is not None, "" if hit else f"no match for {pattern!r}")

    failed = [r for r in results if not r[1]]
    for n, ok, d in results:
        print(f"{'PASS' if ok else 'FAIL'}  {n}" + (f"\n        {d}" if d and not ok else ""))
    print(f"\n{len(results) - len(failed)}/{len(results)} checks passed")
    if docs["dailies"] or docs["master"]:
        print("sizes: " + ", ".join(
            f"{p.name}={len(p.read_text(encoding='utf-8', errors='replace'))}"
            for p in docs["dailies"] + ([docs["master"]] if docs["master"] else [])))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
