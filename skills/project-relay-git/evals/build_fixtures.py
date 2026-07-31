#!/usr/bin/env python3
"""Build the three Git-backed fixture projects the eval set runs against.

Each fixture is a real repository with real commits, so the skill's claims about
branch, HEAD, and working-tree state can be checked against `git` rather than taken
on trust. Each also contains planted traps — intentions phrased like completions,
results nobody observed, stale inherited claims — that a correct handoff must catch.

Usage:
    python build_fixtures.py --out <directory>
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

ENV = {"GIT_AUTHOR_NAME": "Fixture", "GIT_AUTHOR_EMAIL": "fixture@example.com",
       "GIT_COMMITTER_NAME": "Fixture", "GIT_COMMITTER_EMAIL": "fixture@example.com"}


def git(root: Path, *args: str) -> None:
    import os
    env = {**os.environ, **ENV}
    subprocess.run(["git", *args], cwd=root, check=True, capture_output=True, env=env)


def write(root: Path, rel: str, text: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


# ---------------------------------------------------------------- fixture G1

def build_g1(out: Path) -> Path:
    """Mid-feature session: uncommitted work, no upstream, traps in the notes."""
    root = out / "g1-rate-limit"
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    git(root, "init", "-q", "-b", "main")

    write(root, "package.json", '{\n  "name": "orders-api",\n  "version": "0.4.1"\n}\n')
    write(root, "src/server.ts", "export const start = () => console.log('up');\n")
    write(root, "README.md", "# orders-api\n\nInternal orders service.\n")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "chore: initial service skeleton")

    git(root, "checkout", "-q", "-b", "feat/rate-limit")
    write(root, "src/middleware/rate-limit.ts",
          "// token bucket, 100 req/min per API key\nexport const rateLimit = () => {};\n")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "feat: add token-bucket rate limiter skeleton")

    write(root, "src/middleware/rate-limit.ts",
          "// token bucket, 100 req/min per API key\n"
          "// TODO: burst allowance still unimplemented\n"
          "export const rateLimit = () => {};\n")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "feat: wire rate limiter into request pipeline")

    # Left in the working tree on purpose: staged, unstaged, untracked.
    write(root, "src/config/limits.ts", "export const WINDOW_MS = 60_000;\n")
    git(root, "add", "src/config/limits.ts")
    write(root, "src/server.ts",
          "import { rateLimit } from './middleware/rate-limit';\n"
          "export const start = () => console.log('up');\n")
    write(root, "notes/scratch.txt", "burst allowance: ask Priya which tier gets it\n")

    write(root, "SESSION-NOTES.md", """\
# Session notes — rate limiting

Picked up the rate-limit work on `feat/rate-limit`.

Built the token bucket in `src/middleware/rate-limit.ts` and wired it into the request
pipeline. Two commits. The burst allowance is not implemented — there's a TODO in the file.

Started on `src/config/limits.ts` to hold the window constant. It's staged but the values are
provisional; Priya has to confirm which pricing tier gets a burst allowance before they mean
anything. She hasn't answered yet.

`src/server.ts` has the import added but nothing calls it yet, and that edit isn't committed.

Tried doing the limiter as an nginx config instead of application middleware first. Dropped it:
the limits have to be per API key and nginx can't see the key without decrypting the body.
Don't retry that.

Decided the limiter goes in application middleware. Reasoning: per-key limits need application
context. Alternative considered was the gateway; rejected for the same reason.

I'll run the test suite next session. Should be fine.

Left `notes/scratch.txt` lying around, that's just a reminder to myself.
""")

    return root


# ---------------------------------------------------------------- fixture G2

def build_g2(out: Path) -> Path:
    """Master update: stale inherited claims plus two unincorporated Dailies."""
    root = out / "g2-master-update"
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    git(root, "init", "-q", "-b", "main")

    write(root, "package.json", '{\n  "name": "billing",\n  "version": "1.2.0"\n}\n')
    write(root, "src/invoice/generate.ts", "export const generate = () => {};\n")
    write(root, "src/invoice/pdf.ts", "export const render = () => {};\n")

    # The Master claims tests live at tests/invoice.spec.ts. They don't.
    write(root, "docs/handoffs/_master-handoff.md", """\
# Master Handoff — billing

Project: billing
Document Type: Master Handoff
Version: 2.0
Last Updated: 2026-06-18
Current Phase: Invoice generation
Overall Status: In progress
Canonical File: docs/handoffs/_master-handoff.md

---

## 1. Executive Summary

Billing service generating invoices for the orders platform. Invoice generation works; PDF
rendering is the current focus. No blockers.

## 4. Repository and Project Structure

Repository: billing
Default branch: main
Active branches: main, feat/pdf-render
Key directories: src/invoice/

## 9. Final Decisions

- Decision: Invoice numbers are sequential per tenant, not global.
- Date: 2026-05-30
- Rationale: Tenants read their own invoice numbers as a count of their own invoices.
- Source: 2026-05-30_001_numbering-handoff.md

## 15. Current Technical State

Repository: billing
Default branch: main
HEAD of active branch: feat/pdf-render at 4b1c9de
Uncommitted or unpushed work: none
Open PRs: #38 PDF rendering
Test status: passing (tests/invoice.spec.ts, 24 tests)
Deployment status: staging up to date

## 17. Immediate Next Action

Immediate Next Action: Finish PDF rendering on feat/pdf-render.
Start From: src/invoice/pdf.ts
Acceptance Criteria: A generated invoice renders to a single-page PDF.

## 19. Incorporated Daily Handoffs

| Date | Handoff File | Scope | Incorporated into Master |
|---|---|---|---|
| 2026-05-30 | 2026-05-30_001_numbering-handoff.md | Invoice numbering | Yes |
""")

    write(root, "docs/handoffs/2026-05-30_001_numbering-handoff.md", """\
# Daily Handoff — billing — 2026-05-30

Session Scope: Invoice numbering scheme
Branch: main
End-of-Session Status: Numbering decided and implemented

## 3. Decisions Made

- Decision: Sequential invoice numbers per tenant.
  - Rationale: Tenants read their own numbers as a count of their own invoices. Global
    sequences leak volume to competitors.
  - Options considered: global sequence, per-tenant sequence, UUID.
  - Rejected: UUID — accountants refuse unreadable invoice references.
  - Status: Final
""")

    write(root, "docs/handoffs/2026-06-20_001_pdf-render-handoff.md", """\
# Daily Handoff — billing — 2026-06-20

Session Scope: PDF rendering spike
Branch: feat/pdf-render
End-of-Session Status: Spike done, approach rejected

## 3. Decisions Made

- Decision: Do not use headless Chrome for PDF rendering.
  - Rationale: 400MB image and 6s cold start on the invoice worker.
  - Options considered: headless Chrome, wkhtmltopdf, a PDF library.
  - Status: Final

## 4. What Changed

- Change: Spike branch feat/pdf-render deleted after the spike.
- Location: branch feat/pdf-render
- Reason: Approach rejected; nothing on it worth keeping.

## 12. Work That Must Not Be Repeated

- Headless Chrome rendering — 400MB image, 6s cold start. Measured, not guessed.
""")

    write(root, "docs/handoffs/2026-06-24_001_test-suite-handoff.md", """\
# Daily Handoff — billing — 2026-06-24

Session Scope: Test suite reorganisation
Branch: main
End-of-Session Status: Suite moved, two tests failing

## 4. What Changed

- Change: Test suite moved out of the repository into the shared QA repository.
- Location: tests/ removed from billing
- Previous State: tests/invoice.spec.ts, 24 tests
- New State: qa-suite repository, billing/ directory
- Reason: Shared fixtures with the orders service.
- Validation: Suite runs in the QA repository.

## 7. Open, Uncertain, or Unverified Items

- **Item:** Two invoice tests fail after the move — Status: Open
  - Detail: Fixture paths were absolute. Not fixed.
""")

    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "feat: invoice generation and PDF stub")
    git(root, "checkout", "-q", "-b", "feat/invoice-totals")
    write(root, "src/invoice/totals.ts", "export const total = () => 0;\n")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "feat: invoice totals scaffold")

    return root


# ---------------------------------------------------------------- fixture G3

def build_g3(out: Path) -> Path:
    """Handover: work blocked on a prerequisite nobody has obtained."""
    root = out / "g3-handover"
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    git(root, "init", "-q", "-b", "main")

    write(root, "README.md", "# webhook-relay\n\nForwards partner webhooks into the event bus.\n")
    write(root, "src/relay.ts", "export const relay = () => {};\n")
    write(root, "src/verify.ts", "// signature verification\nexport const verify = () => false;\n")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "feat: webhook relay skeleton")

    git(root, "checkout", "-q", "-b", "feat/signature-verify")
    write(root, "src/verify.ts",
          "// signature verification — HMAC-SHA256 over the raw body\n"
          "// blocked: needs the partner's signing secret\n"
          "export const verify = () => false;\n")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "feat: HMAC signature verification, unverifiable without secret")

    write(root, "SESSION-NOTES.md", """\
# Session notes — signature verification

Handing this to someone else, I'm out for two weeks.

Wrote HMAC-SHA256 verification over the raw body in `src/verify.ts` and committed it on
`feat/signature-verify`. I cannot test it. The partner's signing secret is held by their
integrations team and we've asked for it twice — Dana on their side said she'd chase it. No
secret, no test vector, so the verification is unverified code.

The raw body has to be preserved before the JSON body parser runs, otherwise the signature
never matches. That's a real constraint, it cost me an afternoon before I worked it out.

Nothing is deployed. There's no PR yet.

Whoever picks this up: don't rewrite verify.ts, it's probably correct, it's just untestable
until the secret arrives.
""")

    return root


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    out = Path(args.out).expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)

    for build in (build_g1, build_g2, build_g3):
        root = build(out)
        print(f"built {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
