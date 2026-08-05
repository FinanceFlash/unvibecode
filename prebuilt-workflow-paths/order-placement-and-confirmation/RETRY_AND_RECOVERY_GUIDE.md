# Retry and Recovery Guide

## Partial failures
- Order commits but payment reference or result does not attach
- Payment succeeds but order commit fails
- Order commits but inventory reservation or conversion fails
- Order confirms but fulfilment handoff fails
- Order commits but customer confirmation or receipt fails
- Order commit succeeds but client response is lost

## Recovery rules
- Use checkout identity and order idempotency key as stable placement identities.
- Re-read checkout snapshot, order, payment, inventory, and fulfilment state before retrying.
- Never create a second order solely because confirmation or response was lost.
- Keep immutable accepted values separate from later cart, profile, or catalog changes.
- Reconcile order, payment, inventory, fulfilment, ledger, receipt, and communication.

