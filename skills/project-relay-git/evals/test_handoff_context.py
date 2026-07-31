#!/usr/bin/env python3
"""Regression tests for the context helper's reading of Git state.

Run with: python -m unittest discover -s skills/project-relay-git/evals -p 'test_*.py'

These cover the parts of handoff_context.py where a wrong answer is worse than no answer,
because the handoff presents them as verified fact.
"""
from __future__ import annotations

import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from handoff_context import classify_porcelain, git_state  # noqa: E402


def rmtree(path: Path) -> None:
    """shutil.rmtree that survives Windows read-only Git object files."""
    def on_error(func, target, _exc):
        os.chmod(target, stat.S_IWRITE)
        func(target)

    if sys.version_info >= (3, 12):
        shutil.rmtree(path, onexc=on_error)
    else:
        shutil.rmtree(path, onerror=on_error)


class ClassifyPorcelainTest(unittest.TestCase):
    def test_leading_space_means_working_tree_only(self):
        work = classify_porcelain(" M src/a.py\nM  src/b.py\n?? notes.md\n")
        self.assertEqual(work["unstaged"], ["M src/a.py"])
        self.assertEqual(work["staged"], ["M src/b.py"])
        self.assertEqual(work["untracked"], ["notes.md"])

    def test_both_columns_set_counts_twice(self):
        work = classify_porcelain("MM src/a.py\n")
        self.assertEqual(work["staged"], ["M src/a.py"])
        self.assertEqual(work["unstaged"], ["M src/a.py"])

    def test_paths_are_not_truncated(self):
        work = classify_porcelain(" D inventory/adapters/warehouse.py\n")
        self.assertEqual(work["unstaged"], ["D inventory/adapters/warehouse.py"])


class GitStateTest(unittest.TestCase):
    """The bug this guards against only appeared through a real `git status` call.

    `run()` used to strip the whole of stdout, which removed the significant leading space
    from the *first* porcelain line. It was invisible whenever a staged path happened to sort
    first, so the parser unit tests above are not enough on their own.
    """

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="relay-git-test-"))
        self.repo = self.tmp / "repo"
        self.repo.mkdir()
        self._git("init", "-q", "-b", "main")
        self._git("config", "user.name", "Relay Test")
        self._git("config", "user.email", "test@example.invalid")
        self._git("config", "commit.gpgsign", "false")

    def tearDown(self):
        rmtree(self.tmp)

    def _git(self, *args: str) -> None:
        subprocess.run(
            ["git", *args], cwd=self.repo, check=True, capture_output=True, text=True
        )

    def _write(self, rel: str, text: str) -> None:
        p = self.repo / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")

    def test_unstaged_file_sorting_first_is_not_reported_as_staged(self):
        self._write("aaa.py", "original\n")
        self._write("zzz.py", "original\n")
        self._git("add", "-A")
        self._git("commit", "-q", "-m", "baseline")

        self._write("aaa.py", "working tree only\n")   # unstaged, sorts first
        self._write("zzz.py", "staged\n")
        self._git("add", "zzz.py")

        state = git_state(self.repo)
        self.assertEqual(state["staged"], ["M zzz.py"])
        self.assertEqual(state["unstaged"], ["M aaa.py"])
        self.assertEqual(state["uncommitted_count"], 2)


if __name__ == "__main__":
    unittest.main()
