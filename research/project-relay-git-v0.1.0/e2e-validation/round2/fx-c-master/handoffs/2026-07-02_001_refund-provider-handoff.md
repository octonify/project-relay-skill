# Daily Handoff — refund provider wiring

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
