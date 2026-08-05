# Retry and Recovery Guide

## Partial failures
- Settlement and ledger commit but provider submission fails
- Provider accepts payout but local status does not update
- One payee succeeds while another fails in a split settlement
- Transaction marks settled but seller balance or statement fails
- Payout returns after ledger marked final
- Approval commits but notification or operational event fails

## Recovery rules
- Use transaction, financial version, settlement, payout, and provider idempotency identities consistently.
- Re-read eligibility, holds, ledger, payee, destination, provider, and transaction state before retrying.
- Never submit payout again solely because acknowledgement or local status was lost.
- Keep per-payee partial outcomes and unbalanced exceptions visible.
- Reconcile provider, payout, ledger, seller balance, transaction, statement, and notification.

