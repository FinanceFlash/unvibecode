# Retry and Recovery Guide

## Partial failures
- Provider authorizes but local attempt update fails
- Payment captures but order update fails
- Order marks paid but ledger or fulfilment handoff fails
- Provider accepts but the response is lost
- Receipt or customer notification fails after capture
- Void or cancellation state differs between provider and local records

## Recovery rules
- Use the payment-attempt and provider idempotency keys as stable identities.
- Re-read authoritative order, amount, attempt, authorization, and provider state before retrying.
- Never repeat capture solely because a response or local update was lost.
- Distinguish decline, authorization, capture, pending, and uncertain outcomes.
- Reconcile provider, payment, order, ledger, fulfilment, and receipt records.

