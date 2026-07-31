#!/usr/bin/env python3
"""Build disposable Git fixtures for the project-relay-git end-to-end validation.

Deliberately a different project domain from skills/project-relay-git/evals/build_fixtures.py
so these runs are independent evidence rather than a repeat of the eval suite.

Each fixture plants at least one trap: a claim in the human-written session notes that the
repository itself contradicts, or a piece of state that cannot be verified from inside the
fixture. A correct handoff must not promote either into verified fact.
"""
from __future__ import annotations

import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path


def rmtree(path) -> None:
    """shutil.rmtree that survives Windows read-only Git object files."""
    def on_error(func, target, _exc):
        os.chmod(target, stat.S_IWRITE)
        func(target)

    shutil.rmtree(path, onexc=on_error)

ROOT = Path(__file__).resolve().parent / "fixtures"

ENV_NAME = "Relay Fixture"
ENV_EMAIL = "fixture@example.invalid"


def run(args: list[str], cwd: Path) -> str:
    res = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    if res.returncode != 0:
        raise SystemExit(f"FAILED {' '.join(args)} in {cwd}\n{res.stdout}\n{res.stderr}")
    return res.stdout.strip()


def write(base: Path, rel: str, text: str) -> None:
    p = base / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def git_init(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    run(["git", "init", "-q", "-b", "main"], path)
    run(["git", "config", "user.name", ENV_NAME], path)
    run(["git", "config", "user.email", ENV_EMAIL], path)
    run(["git", "config", "commit.gpgsign", "false"], path)


def commit(path: Path, message: str) -> str:
    run(["git", "add", "-A"], path)
    run(["git", "commit", "-q", "-m", message], path)
    return run(["git", "rev-parse", "HEAD"], path)


# --------------------------------------------------------------------------------------
# Shared base: a small checkout service. Used by fixtures A, B and D.
# --------------------------------------------------------------------------------------

def base_checkout_service(path: Path) -> None:
    git_init(path)
    write(path, "README.md", """# checkout-service

Payment checkout API for the storefront. Node + TypeScript.

- `src/routes/` — HTTP handlers
- `src/lib/` — shared helpers
- `docs/` — design notes
""")
    write(path, "package.json", """{
  "name": "checkout-service",
  "version": "0.4.1",
  "private": true,
  "scripts": {
    "build": "tsc -p .",
    "start": "node dist/index.js"
  }
}
""")
    write(path, "src/index.ts", """import { createServer } from "./server";

const port = Number(process.env.PORT ?? 8080);
createServer().listen(port, () => console.log(`checkout-service on ${port}`));
""")
    write(path, "src/server.ts", """import express from "express";
import { chargeRoute } from "./routes/charge";

export function createServer() {
  const app = express();
  app.use(express.json());
  app.post("/charge", chargeRoute);
  return app;
}
""")
    write(path, "src/routes/charge.ts", """import type { Request, Response } from "express";

export async function chargeRoute(req: Request, res: Response) {
  const { amountCents, currency } = req.body ?? {};
  if (typeof amountCents !== "number" || amountCents <= 0) {
    return res.status(400).json({ error: "amountCents must be a positive number" });
  }
  return res.status(201).json({ status: "captured", amountCents, currency });
}
""")
    write(path, "src/lib/money.ts", """export function toMinorUnits(major: number): number {
  return Math.round(major * 100);
}
""")
    write(path, "docs/design.md", """# Design notes

Charges are captured synchronously. Retries are the client's responsibility today,
which is the problem the idempotency work is meant to fix.
""")
    commit(path, "chore: baseline checkout service")


def fixture_daily(path: Path) -> dict:
    """Fixture for Test A (/handoff) and Test B (natural language).

    Traps:
      - session notes claim "opened PR #14"; there is no remote and no gh remote to check
      - session notes claim "test suite is green"; the repo has no tests and no test script
      - a decision was reversed mid-session; both the decision and the reversal are in the notes
    """
    base_checkout_service(path)
    run(["git", "checkout", "-q", "-b", "feat/idempotency-keys"], path)

    write(path, "src/lib/idempotency.ts", """// Idempotency key storage. In-memory for now; Redis once the shape settles.
type Entry = { responseBody: unknown; statusCode: number; createdAt: number };

const store = new Map<string, Entry>();

export function remember(key: string, statusCode: number, responseBody: unknown): void {
  store.set(key, { responseBody, statusCode, createdAt: Date.now() });
}

export function recall(key: string): Entry | undefined {
  return store.get(key);
}
""")
    c1 = commit(path, "feat(idempotency): in-memory key store")

    write(path, "docs/design.md", """# Design notes

Charges are captured synchronously. Retries are the client's responsibility today,
which is the problem the idempotency work is meant to fix.

## Idempotency

Clients send `Idempotency-Key`. A repeated key replays the stored response rather than
charging again. Keys are scoped per merchant, not globally, so two merchants cannot
collide on a shared UUID.
""")
    c2 = commit(path, "docs: record the per-merchant key scoping decision")

    # staged
    write(path, "src/lib/keyscope.ts", """import type { Request } from "express";

export function scopedKey(req: Request): string | null {
  const raw = req.header("Idempotency-Key");
  const merchant = req.header("X-Merchant-Id");
  if (!raw || !merchant) return null;
  return `${merchant}:${raw}`;
}
""")
    run(["git", "add", "src/lib/keyscope.ts"], path)

    # unstaged modification to a tracked file
    write(path, "src/routes/charge.ts", """import type { Request, Response } from "express";
import { scopedKey } from "../lib/keyscope";
import { recall } from "../lib/idempotency";

export async function chargeRoute(req: Request, res: Response) {
  const key = scopedKey(req);
  if (key) {
    const prior = recall(key);
    if (prior) return res.status(prior.statusCode).json(prior.responseBody);
  }
  const { amountCents, currency } = req.body ?? {};
  if (typeof amountCents !== "number" || amountCents <= 0) {
    return res.status(400).json({ error: "amountCents must be a positive number" });
  }
  return res.status(201).json({ status: "captured", amountCents, currency });
}
""")

    # untracked
    write(path, "notes/scratch.md", """- ask Marta whether replay should re-emit the webhook
- TTL? 24h feels arbitrary
""")

    write(path, "SESSION-NOTES.md", """Session notes, Thursday
=======================

Picked up the idempotency work. Goal: a repeated Idempotency-Key must replay the
original response instead of charging the card twice.

Built the key store first (in-memory Map). Redis is the obvious end state but the
entry shape is still moving, so committing to a schema now would just mean migrating
it next week. In-memory is a deliberate placeholder, not an oversight.

Big decision of the day: keys are scoped **per merchant**, not globally. Started off
global, then realised two merchants can independently generate the same UUID v4 in
theory, and more importantly a global namespace means one merchant can probe another's
key space. Wrote it up in docs/design.md. This one is settled.

Tried doing the replay check in express middleware so the route stayed clean. Abandoned
it — the middleware runs before the JSON body parser, and the merchant id lives in a
header but the amount lives in the body, and we need both to decide whether a replay is
actually the same request. Not worth fighting the ordering. Do not try the middleware
approach again.

Wired scopedKey into the charge route. Staged the new helper, route change is still
loose in the working tree.

Ran the test suite, all green.

Opened PR #14 for review.

Blocked: Marta needs to say whether a replayed charge should re-emit the payment webhook
or stay silent. Cannot finish the replay path until that is answered — if it re-emits,
the stored entry needs the webhook payload too, which changes the Entry type.

Next: get Marta's answer on webhook re-emission.
""")

    head = run(["git", "rev-parse", "HEAD"], path)
    return {
        "branch": "feat/idempotency-keys",
        "head": head,
        "commits": [c1, c2],
        "staged": ["src/lib/keyscope.ts"],
        "unstaged": ["src/routes/charge.ts"],
        "untracked": ["notes/scratch.md", "SESSION-NOTES.md"],
        "remote": None,
    }


def fixture_master(path: Path) -> dict:
    """Fixture for Test C (/handoff master).

    Has a real (local, bare) remote so upstream divergence is verifiable, an existing
    stale Master, and one Daily that the Master has not incorporated.

    Traps:
      - Master claims feat/legacy-cart is active work; that branch was deleted
      - Master claims "Test status: passing (48 tests)"; there is no test directory at all
      - Master claims a staging deployment; nothing in the fixture can confirm or deny it
      - Master's Canonical File line is correct and must survive
    """
    remote = path.parent / (path.name + "-remote.git")
    if remote.exists():
        rmtree(remote)
    remote.mkdir(parents=True)
    run(["git", "init", "-q", "--bare", "-b", "main"], remote)

    base_checkout_service(path)
    run(["git", "remote", "add", "origin", str(remote)], path)
    run(["git", "push", "-q", "-u", "origin", "main"], path)

    # A branch that existed and was deleted.
    run(["git", "checkout", "-q", "-b", "feat/legacy-cart"], path)
    write(path, "src/routes/cart.ts", "export const cart = () => { throw new Error('wip'); };\n")
    commit(path, "wip: legacy cart route")
    run(["git", "checkout", "-q", "main"], path)
    run(["git", "branch", "-q", "-D", "feat/legacy-cart"], path)

    run(["git", "checkout", "-q", "-b", "feat/refund-flow"], path)
    run(["git", "push", "-q", "-u", "origin", "feat/refund-flow"], path)

    write(path, "src/routes/refund.ts", """import type { Request, Response } from "express";

export async function refundRoute(req: Request, res: Response) {
  const { chargeId, amountCents } = req.body ?? {};
  if (!chargeId) return res.status(400).json({ error: "chargeId required" });
  return res.status(202).json({ status: "refund_pending", chargeId, amountCents });
}
""")
    commit(path, "feat(refund): accept refund requests")

    write(path, "src/server.ts", """import express from "express";
import { chargeRoute } from "./routes/charge";
import { refundRoute } from "./routes/refund";

export function createServer() {
  const app = express();
  app.use(express.json());
  app.post("/charge", chargeRoute);
  app.post("/refund", refundRoute);
  return app;
}
""")
    commit(path, "feat(refund): route partial refunds through the server")

    # Divergence: remote has a commit the local branch does not.
    other = path.parent / (path.name + "-other")
    if other.exists():
        rmtree(other)
    run(["git", "clone", "-q", str(remote), str(other)], path.parent)
    run(["git", "config", "user.name", ENV_NAME], other)
    run(["git", "config", "user.email", ENV_EMAIL], other)
    run(["git", "checkout", "-q", "feat/refund-flow"], other)
    write(other, "docs/refunds.md", "Partial refunds only. Full refunds go through the old admin tool.\n")
    commit(other, "docs: note the partial-refund limitation")
    run(["git", "push", "-q", "origin", "feat/refund-flow"], other)
    rmtree(other)
    run(["git", "fetch", "-q", "origin"], path)

    write(path, "docs/handoffs/_master-handoff.md", """# Master Handoff — checkout-service

Project: checkout-service
Document Type: Master Handoff
Version: 3.0
Last Updated: 2026-06-11
Current Phase: Refunds
Overall Status: In Progress
Canonical File: docs/handoffs/_master-handoff.md

## 2. Executive Summary

checkout-service captures card payments for the storefront. The current phase is refunds.
Idempotency shipped in April. Active work is the legacy cart rewrite on feat/legacy-cart,
with refunds queued behind it.

## 4. Locked Principles and Decisions

- Idempotency keys are scoped per merchant, not globally. Decided 2026-04-02. A global
  namespace lets one merchant probe another's keys. Source: 2026-04-02 Daily.
- Money is handled in integer minor units everywhere. No floats cross a module boundary.
  Decided 2026-02-18.

## 5. Repository and Project Structure

Repository: checkout-service. Default branch: main.
Active branches: feat/legacy-cart (cart rewrite), main.
`src/routes/` holds HTTP handlers, `src/lib/` shared helpers.

## 7. Sources of Truth

| Source | Location | Purpose | Authority | Status |
|---|---|---|---|---|
| Design notes | docs/design.md | Architecture decisions | Authoritative | Current |
| Master Handoff | docs/handoffs/_master-handoff.md | Project state | Authoritative | Current |

## 15. Risks, Constraints, and Dependencies

- The payment provider rate-limits refund calls to 10/second. Exceeding it returns 429
  with no retry-after header, so backoff has to be guessed.
- No staging card vault. Refund testing against staging uses provider sandbox tokens only.

## 16. Current Technical State

Repository: checkout-service
Default branch: main
Active branches: feat/legacy-cart
HEAD of active branch: 9f2c1ab
Uncommitted or unpushed work: none
Open PRs: #31 (legacy cart), awaiting review
Build status: passing
Test status: passing (48 tests)
Deployment status: deployed to staging 2026-06-10

## 18. Immediate Next Action

Immediate Next Action: finish the cart rewrite on feat/legacy-cart and get PR #31 reviewed.
Responsible Role or Agent: whoever picks up the cart work
Start From: feat/legacy-cart

## 20. Incorporated Daily Handoffs

| Date | Handoff File | Scope | Incorporated into Master |
|---|---|---|---|
| 2026-04-02 | 2026-04-02_001_idempotency-handoff.md | Idempotency | Yes |
""")

    write(path, "docs/handoffs/2026-06-28_001_refund-flow-handoff.md", """# Daily Handoff — refund flow

Date: 2026-06-28
Branch: feat/refund-flow

## What happened

Started the refund flow. The provider only supports partial refunds through the modern
API; full refunds still have to go through the old admin tool, which nobody wants to
automate. Recorded that as a constraint rather than a bug.

Decision: refunds are accepted asynchronously and return 202, not 201. The provider can
take up to 40 seconds to settle a refund and holding the HTTP connection open that long
was causing gateway timeouts in the earlier prototype. This is settled.

Tried refunding synchronously first. Abandoned it after the timeouts. Do not retry the
synchronous approach.

The legacy cart work was dropped — the storefront team decided to keep the existing cart
and the branch was deleted. Cart is out of scope for us now.

## Next

Wire the refund route into the provider client.
""")

    write(path, "docs/handoffs/2026-07-02_001_refund-provider-handoff.md", """# Daily Handoff — refund provider wiring

Date: 2026-07-02
Branch: feat/refund-flow

## What happened

Wired the route through to the server. The provider client itself is not connected yet —
the route currently returns refund_pending without calling anything downstream. That is
deliberate scaffolding, not a finished path.

Found that the provider rate-limits refunds harder than documented: 10/second is the
published number but we saw 429s at around 6/second in the sandbox. Treat 5/second as the
working ceiling until someone gets a straight answer from the provider.

Blocked: we do not have production refund credentials. Sandbox only. Nobody can test the
real path until Ops issues them.

## Next

Get production refund credentials from Ops.
""")

    write(path, "notes/todo.txt", "chase ops re: refund creds\n")

    head = run(["git", "rev-parse", "HEAD"], path)
    return {
        "branch": "feat/refund-flow",
        "head": head,
        "remote": str(remote),
        "divergence": "ahead 2, behind 1",
        "untracked": ["docs/handoffs/", "notes/todo.txt"],
    }


def fixture_full(path: Path) -> dict:
    """Fixture for Test D (/handoff full): Daily + new Master, no Master exists yet.

    Trap: the session notes claim the webhook signature check is "done and committed",
    but the only commit on the branch changes a comment. Nothing verifies.
    """
    base_checkout_service(path)
    run(["git", "checkout", "-q", "-b", "feat/webhook-verify"], path)

    write(path, "src/lib/webhook.ts", """// Verify inbound provider webhooks.
// TODO: signature verification. Needs the provider's signing secret.
export function handleWebhook(rawBody: string): { ok: boolean } {
  if (!rawBody) return { ok: false };
  return { ok: true };
}
""")
    commit(path, "feat(webhook): inbound webhook entry point")

    write(path, "src/lib/webhook.ts", """// Verify inbound provider webhooks.
// Signature verification must run against the raw body, before any JSON parsing,
// because the provider signs the exact bytes it sent.
// TODO: signature verification. Needs the provider's signing secret.
export function handleWebhook(rawBody: string): { ok: boolean } {
  if (!rawBody) return { ok: false };
  return { ok: true };
}
""")
    commit(path, "feat(webhook): implement HMAC signature verification")

    write(path, "notes/handover.md", "two weeks off from friday\n")

    write(path, "SESSION-NOTES.md", """Session notes
=============

Handing this over — out for two weeks from Friday, someone else picks it up cold.

Webhook verification. The provider POSTs payment events and we currently accept anything,
which is obviously not shippable.

Hard constraint discovered the hard way: signature verification has to run against the
**raw request body**, before express.json() touches it. The provider signs the exact bytes.
Once the JSON parser has reserialised the payload the signature never matches. Lost most of
an afternoon to this before working it out. The fix is app.use(express.raw()) on the webhook
route specifically, not globally, because every other route wants parsed JSON.

Wrote the HMAC verification and committed it.

Cannot test any of it: we do not have the provider's signing secret. Dana is chasing the
partner's integrations team for it. Until that arrives verification is unverifiable —
there is no way to generate a valid test signature.

Do not rewrite src/lib/webhook.ts from scratch. The raw-body ordering constraint is baked
into how it is structured and a rewrite will lose it.

Nothing is deployed. No PR yet.

Next: Dana gets the signing secret from the partner's integrations team.
""")

    head = run(["git", "rev-parse", "HEAD"], path)
    return {"branch": "feat/webhook-verify", "head": head, "remote": None}


def main() -> int:
    if ROOT.exists():
        rmtree(ROOT)
    ROOT.mkdir(parents=True)

    built = {}
    built["fx-a-daily"] = fixture_daily(ROOT / "fx-a-daily")
    built["fx-b-natural"] = fixture_daily(ROOT / "fx-b-natural")
    built["fx-c-master"] = fixture_master(ROOT / "fx-c-master")
    built["fx-d-full"] = fixture_full(ROOT / "fx-d-full")

    for name, facts in built.items():
        print(f"\n=== {name} ===")
        for k, v in facts.items():
            print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
