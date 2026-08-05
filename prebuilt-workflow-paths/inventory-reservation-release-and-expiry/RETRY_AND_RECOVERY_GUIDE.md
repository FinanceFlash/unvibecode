# Retry and Recovery Guide

## Partial failures
- Quantity decrements but reservation record does not commit
- Reservation commits but expiry scheduling fails
- Multi-line request reserves only some items before failure
- Conversion commits in order service but inventory update fails
- Release updates one inventory store but not another
- Expiry applies but response, event, or downstream projection fails

## Recovery rules
- Use reservation identity and demand idempotency key as stable operation identities.
- Re-read authoritative reservation version, inventory quantities, owner, order, and time before retrying.
- Never reserve, release, expire, or convert solely because a response was lost.
- Apply explicit atomic rollback or compensating release for partial multi-line work.
- Reconcile database, cache, warehouse, order, fulfilment, and audit quantities.

