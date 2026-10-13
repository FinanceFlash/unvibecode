# Retry and Recovery Guide

## Partial failures
- Provisional debit succeeds but the case or ledger update fails
- Representment is submitted but the network confirmation is lost
- Case resolves won or lost but the order or customer record update fails
- Dispute-opened webhook is accepted but case creation fails
- Chargeback-ratio aggregation fails after a confirmed outcome
- Escalation to pre-arbitration succeeds but local case state is not updated

## Recovery rules
- Use the network case identifier and provider idempotency key as the stable case identity.
- Re-read authoritative payment, order, case, and network status before retrying.
- Never repeat a provisional debit or representment submission solely because a response or local update was lost.
- Distinguish opened, under-review, won, lost, accepted, expired, and withdrawn outcomes.
- Reconcile provider, case, ledger, order, and customer records to one outcome.
