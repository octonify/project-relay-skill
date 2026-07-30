#!/usr/bin/env python3
"""Check the mechanically verifiable assertions against a fixture after a run.

Human judgement is still needed for the assertions about extraction, duplication, and
whether a next action is genuinely executable. This covers the ones a script does
better than an eye: file naming, canonical-file discipline, whether every commit hash
and path in the document actually resolves, and placeholder residue.

Usage:
    python check_outputs.py --project-root <fixture> --expect daily|master|full
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

DAILY_RE = re.compile(r"^\d{4}-\d{2}-\d{2}_\d{3}_.+-handoff\.md$")
HASH_RE = re.compile(r"\b[0-9a-f]{7,40}\b")
PATH_RE = re.compile(r"(?<![\w/])((?:src|docs|tests|migrations|notes|qa-suite)/[\w./-]+)")
PLACEHOLDERS = [
    "None this session", "TBD", "<Project>", "<YYYY-MM-DD>", "STARTING SKELETON", "Lorem",
]
# `N/A` is a real answer when something follows it explaining why. Bare `Field: N/A` is not.
BARE_NA_RE = re.compile(r"^\s*[-*]?\s*([\w /]+):\s*n/?a\.?\s*$", re.I | re.M)
# ...except on fields where "nothing" is itself the verified finding. `Supersedes: N/A` on a
# decision says the author checked and it replaces nothing, which is more useful to a reader
# than an omitted line that leaves it ambiguous whether anyone looked.
NA_IS_AN_ANSWER = {
    "supersedes", "dependencies", "stop conditions", "do not change", "blocked",
    "blocking conditions", "deadline or trigger", "scope changes during session",
}
# Words that look like hex but are ordinary English.
HASH_FALSE_POSITIVES = {"added", "acceded", "effaced", "defaced", "decade", "facade"}
# An identifier named as gone, stale, or superseded is being handled correctly, not invented.
# Word-bounded: an unbounded `dead` matches the hash `deadbee` and excuses a fabrication.
NEGATED = re.compile(
    r"\b(?:absent|does not exist|doesn't exist|no longer|not yet|never existed|removed|"
    r"deleted|superseded|supersedes|stale|moved out|unverified|not verified|dead|former|"
    r"previously|used to|has moved|left the repository|out of the repo|no Master|"
    r"not a valid object|unreachable|do not cite|invalid|cannot be found|no longer exists|"
    r"contradiction|rewritten)\b",
    re.I,
)
# Filename patterns and globs describe a convention; they are not claims that a file exists.
PATTERN_MARKERS = ("YYYY", "NNN", "*", "<", ">", "{", "}")
# All-letter hex words are usually English. Only treat one as a hash when it is introduced as one.
COMMIT_CTX = re.compile(r"(?:commit|sha|hash|HEAD(?:\s+at)?|@)\s+`?([0-9a-f]{7,40})`?", re.I)


def git(root: Path, *args: str) -> tuple[int, str]:
    p = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True)
    return p.returncode, p.stdout.strip()


def count_tracked_dailies(root: Path) -> int | None:
    """How many Dailies existed before this run, read from Git rather than assumed.

    Returns None when the handoff directory is untracked, in which case the caller has no
    baseline to compare against and should skip the check rather than invent one.
    """
    code, out = git(root, "ls-files", "docs/handoffs", ".handoffs", "handoffs", "docs/handoff")
    if code != 0 or not out.strip():
        return None
    return sum(1 for line in out.splitlines() if DAILY_RE.match(Path(line).name))


def prior_master_version(root: Path, master: Path) -> str | None:
    """The Version line as it stood at HEAD, so the increment check needs no hard-coded value."""
    rel = master.relative_to(root).as_posix()
    code, out = git(root, "show", f"HEAD:{rel}")
    if code != 0:
        return None
    m = re.search(r"^Version:\s*(.+)$", out, re.M)
    return m.group(1).strip() if m else None


def find_docs(root: Path) -> dict:
    hd = None
    for rel in ("docs/handoffs", ".handoffs", "handoffs", "docs/handoff"):
        if (root / rel).is_dir():
            hd = root / rel
            break
    if hd is None:
        return {"handoff_dir": None, "dailies": [], "master": None, "strays": []}

    dailies, strays, master = [], [], None
    for p in sorted(hd.rglob("*.md")):
        if p.name == "_master-handoff.md":
            master = p
        elif DAILY_RE.match(p.name):
            dailies.append(p)
        else:
            strays.append(p)
    return {"handoff_dir": hd, "dailies": dailies, "master": master, "strays": strays}


def blocks_with_headings(text: str) -> list[str]:
    """Split into blank-line-separated blocks, each prefixed with its section heading.

    Block scope rather than line scope, because the qualifier that marks an identifier
    dead often wraps onto the next line or sits in a table header two rows up.
    """
    heading, current, out = "", [], []
    for line in text.splitlines():
        if line.startswith("#"):
            if current:
                out.append(heading + "\n" + "\n".join(current))
                current = []
            heading = line
        elif line.strip():
            current.append(line)
        elif current:
            out.append(heading + "\n" + "\n".join(current))
            current = []
    if current:
        out.append(heading + "\n" + "\n".join(current))
    return out


def all_mentions_negated(text: str, token: str) -> bool:
    """True when every block naming this identifier marks it gone, stale, or unverified.

    Citing a deleted branch or a superseded test path is the skill doing its job. Only an
    identifier asserted as current needs to resolve.
    """
    hits = [b for b in blocks_with_headings(text) if token in b]
    return bool(hits) and all(NEGATED.search(b) for b in hits)


def check_identifiers(root: Path, text: str) -> list[str]:
    problems = []
    candidates = {h for h in HASH_RE.findall(text) if any(c.isdigit() for c in h)}
    candidates |= set(COMMIT_CTX.findall(text))
    for h in sorted(candidates):
        if h.lower() in HASH_FALSE_POSITIVES:
            continue
        code, _ = git(root, "cat-file", "-e", f"{h}^{{commit}}")
        if code == 0 or all_mentions_negated(text, h):
            continue
        problems.append(f"commit hash does not resolve and is not marked stale: {h}")
    for rel in sorted(set(PATH_RE.findall(text))):
        rel = rel.rstrip(".,);:")
        if any(mark in rel for mark in PATTERN_MARKERS):
            continue
        if (root / rel).exists():
            continue
        # A path may legitimately refer to something deleted; accept it if git has ever seen it.
        code, out = git(root, "log", "--all", "--oneline", "--", rel)
        if (code == 0 and out) or all_mentions_negated(text, rel):
            continue
        problems.append(f"path does not exist and is not marked removed/absent: {rel}")
    return problems


PROSE_STOP = set(
    "the a an and or but of to in on at for with is are was were be been it its this that these "
    "those as by from not no if then so what which we i you they has have had will would can "
    "could should do does did there their them our your my than more most such over under after "
    "before during while each any all both".split()
)


def phrase_redundancy(text: str, n: int = 5) -> tuple[float | None, int]:
    """Fraction of content-word 5-grams that repeat somewhere in the document.

    Length-independent, which matters: a genuinely complex project earns a long handoff, and
    capping characters punishes it for being complex. Restating yourself is the actual defect,
    and it shows up here regardless of size.
    """
    words = [w for w in re.findall(r"[a-z0-9./_-]+", text.lower())
             if w not in PROSE_STOP and len(w) > 1]
    grams = [tuple(words[i:i + n]) for i in range(len(words) - n + 1)]
    if len(grams) < 100:
        return None, len(grams)
    return 1 - len(set(grams)) / len(grams), len(grams)


def sentences(text: str) -> list[str]:
    """Substantial prose only — headings, table rules, and short field lines carry no duplication."""
    out = []
    for raw in re.split(r"(?<=[.;])\s+|\n", text):
        s = re.sub(r"[`*_|#>-]", " ", raw)
        s = " ".join(s.split()).lower()
        if len(s) >= 60:
            out.append(s)
    return out


def cross_document_overlap(daily: str, master: str) -> tuple[float, list[str]]:
    """Fraction of the Master's substantial sentences that restate one from the Daily.

    Independence is meant to cost a pointer, not a copy. This measures how often the Master
    chose the copy.
    """
    from difflib import SequenceMatcher

    d_sents, m_sents = sentences(daily), sentences(master)
    if not m_sents:
        return 0.0, []
    dupes = []
    for m in m_sents:
        for d in d_sents:
            if SequenceMatcher(None, m, d).ratio() >= 0.80:
                dupes.append(m)
                break
    return len(dupes) / len(m_sents), dupes


STOPWORDS = {
    "The", "This", "That", "There", "These", "Those", "It", "If", "When", "What", "Which",
    "Not", "No", "Yes", "Status", "Date", "Project", "Branch", "Version", "Daily", "Master",
    "Handoff", "Session", "Next", "Action", "Open", "Blocked", "Unknown", "Detail", "Reason",
    "Result", "Change", "Location", "Evidence", "Item", "Risk", "Impact", "Owner", "Purpose",
    "Repository", "Commit", "HEAD", "Current", "Previous", "New", "Both", "Do", "Start", "From",
    "State", "Notes", "Note", "Test", "Tests", "Build", "Work", "Working", "Files", "File",
    "Scope", "Rationale", "Decision", "Decisions", "Validation", "Validated", "Approved",
    "Uncommitted", "Untracked", "Unstaged", "Staged", "Upstream", "Local", "Remote", "Level",
}


def salient_identifiers(text: str, limit: int = 8) -> list[str]:
    """The things this handoff turns on: commit hashes, branches, paths, and proper nouns.

    Derived rather than supplied, so the check works on any project without being told what
    matters in advance.
    """
    counts: dict[str, int] = {}

    def bump(tok: str) -> None:
        if len(tok) >= 4:
            counts[tok] = counts.get(tok, 0) + 1

    for m in re.findall(r"\b[0-9a-f]{7,40}\b", text):
        if any(c.isdigit() for c in m):
            bump(m)
    for m in re.findall(r"\b(?:feat|fix|chore|release|hotfix)/[\w./-]+", text):
        bump(m)
    for m in PATH_RE.findall(text):
        bump(m.rstrip(".,);:"))
    for m in re.findall(r"(?<![.\n>|#*-] )\b[A-Z][a-z]{3,}\b", text):
        if m not in STOPWORDS:
            bump(m)

    return [t for t, _ in sorted(counts.items(), key=lambda kv: -kv[1])[:limit]]


def identifier_spread(text: str, tokens: list[str]) -> list[tuple[str, int, int]]:
    """(token, mentions, blocks explaining it) — a fact explained in many blocks is retold."""
    blocks = blocks_with_headings(text)
    out = []
    for tok in tokens:
        mentions = len(re.findall(re.escape(tok), text, re.I))
        if not mentions:
            continue
        explaining = sum(
            1 for b in blocks
            if re.search(re.escape(tok), b, re.I) and len(b) >= 200
        )
        out.append((tok, mentions, explaining))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--project-root", required=True)
    ap.add_argument("--expect", required=True, choices=["daily", "master", "full"])
    ap.add_argument("--tokens", default="",
                    help="comma-separated identifiers to check spread for; derived if omitted")
    ap.add_argument("--verbose", action="store_true", help="print per-identifier spread")
    ap.add_argument("--baseline-dailies", type=int, default=None,
                    help="how many Daily files existed before the run (--expect master). "
                         "Defaults to counting the Dailies tracked in Git.")
    ap.add_argument("--baseline-version", default=None,
                    help="the Master's Version before the run (--expect master). "
                         "Defaults to the Version at HEAD.")
    args = ap.parse_args()

    root = Path(args.project_root).resolve()
    found = find_docs(root)
    results: list[tuple[bool, str]] = []

    def check(ok: bool, label: str) -> None:
        results.append((bool(ok), label))

    dailies, master, strays = found["dailies"], found["master"], found["strays"]

    if args.expect == "daily":
        check(len(dailies) == 1, f"exactly one Daily created (found {len(dailies)})")
        check(master is None, "no Master file created")
    elif args.expect == "master":
        check(master is not None, "Master exists")
        # These two were hard-coded to the g2 eval fixture (3 Dailies, Version 2.0), so the
        # checker reported a spurious failure on any other repository. Both baselines are now
        # supplied by the caller, and fall back to reading the pre-run state out of Git.
        baseline_n = args.baseline_dailies
        if baseline_n is None:
            baseline_n = count_tracked_dailies(root)
        if baseline_n is None:
            check(True, f"no new Daily created (not checked: no baseline available, found {len(dailies)})")
        else:
            check(len(dailies) == baseline_n,
                  f"no new Daily created (expected the {baseline_n} pre-existing, found {len(dailies)})")
        if master:
            code, out = git(root, "status", "--porcelain", str(master))
            check(bool(out.strip()), "Master was modified in place (shows as changed in git)")
            ver = re.search(r"^Version:\s*(.+)$", master.read_text(encoding="utf-8"), re.M)
            now = ver.group(1).strip() if ver else None
            prior = args.baseline_version or prior_master_version(root, master)
            if prior:
                check(bool(now) and now != prior,
                      f"Version incremented above {prior} (found {now or 'none'})")
            else:
                check(bool(now), f"Version recorded (found {now or 'none'})")
    else:
        check(len(dailies) == 1, f"exactly one Daily created (found {len(dailies)})")
        check(master is not None, "Master created")

    check(not strays, f"no stray files in the handoff directory ({[p.name for p in strays]})")

    docs = [p for p in (dailies + ([master] if master else [])) if p]
    for doc in docs:
        text = doc.read_text(encoding="utf-8")
        for problem in check_identifiers(root, text):
            check(False, f"{doc.name}: {problem}")
        hits = [ph for ph in PLACEHOLDERS if ph in text]
        hits += [f"{m.strip()}: N/A" for m in BARE_NA_RE.findall(text)
                 if m.strip().lower() not in NA_IS_AN_ANSWER]
        check(not hits, f"{doc.name}: no template placeholders left ({hits})")
        check(len(text.strip()) > 400, f"{doc.name}: not empty")

    if docs:
        check(True, f"identifier resolution checked across {len(docs)} document(s)")

    # Cross-document duplication. Only meaningful when this run produced both documents.
    if args.expect == "full" and dailies and master:
        ratio, dupes = cross_document_overlap(
            dailies[0].read_text(encoding="utf-8"), master.read_text(encoding="utf-8")
        )
        check(ratio <= 0.20,
              f"Master restates at most 20% of the Daily's prose (found {ratio:.0%})")
        for d in dupes[:5]:
            print(f"       duplicated: {d[:110]}...")

    # Phrase-level redundancy. Calibrated against hand-written prose, which sits at 0.0-0.1%;
    # generated handoffs have measured 0.4-0.9%. A document that pads by restating itself
    # climbs well above that, so this catches real repetition without capping length.
    generated = [p for p in docs if p in dailies[:1] or p is master]
    for doc in generated:
        text = doc.read_text(encoding="utf-8")
        red, ngrams = phrase_redundancy(text)
        if red is None:
            continue
        check(red <= 0.05,
              f"{doc.name}: phrase redundancy within range ({red:.1%} of {ngrams} 5-grams)")

    # Informational only. Counting how many sections name an identifier does NOT measure
    # re-explanation — a section that mentions a file in one clause counts the same as one
    # that re-argues it. Kept as a pointer for human review, never as a gate.
    if args.verbose:
        for doc in generated:
            text = doc.read_text(encoding="utf-8")
            toks = ([t.strip() for t in args.tokens.split(",") if t.strip()]
                    or salient_identifiers(text))
            for tok, mentions, blocks in identifier_spread(text, toks):
                print(f"       [spread] {doc.name}: '{tok}' {mentions} mentions across "
                      f"{blocks} substantial blocks")

    for doc in docs:
        print(f"       [size] {doc.name}: {len(doc.read_text(encoding='utf-8')):,} chars")

    failures = [label for ok, label in results if not ok]
    for ok, label in results:
        print(f"[{'PASS' if ok else 'FAIL'}] {label}")
    print(f"\n{len(results) - len(failures)}/{len(results)} mechanical checks passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
