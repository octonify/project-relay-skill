# Daily Handoff — refund flow

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
