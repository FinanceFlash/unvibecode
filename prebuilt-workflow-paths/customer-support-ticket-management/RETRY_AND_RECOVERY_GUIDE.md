# Retry and Recovery Guide

## Partial failures
- Ticket commits but acknowledgement fails
- Message commits but agent or customer notification fails
- Attachment storage succeeds but scanning or ticket association fails
- Assignment changes but queue or SLA projection fails
- Resolution commits but a promised refund or account action fails
- Closure commits but customer response is lost or arrives late

## Recovery rules
- Keep the ticket record authoritative; do not recreate it merely because acknowledgement is uncertain.
- Use stable external references, message identifiers, and idempotency for intake and replies.
- Re-read owner, status, SLA, tenant, and linked-action state before retrying.
- Do not repeat refunds, credits, account changes, or customer messages unintentionally.
- Reconcile ticket outcome, customer communication, and every promised linked action.

