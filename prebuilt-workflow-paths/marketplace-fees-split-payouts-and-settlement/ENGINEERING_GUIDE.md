# Engineering Guide

## Trace the implementation
1. Settlement scheduler, transaction event, calculate, approve, hold, release, submit, callback, retry, reverse, and support entry points
2. Transaction completion, tenant, seller, payee, eligibility, reserve, dispute, refund, fraud, and compliance checks
3. Gross, currency, financial version, commission, fee, tax, withholding, reserve, adjustment, split, exchange, and rounding calculations
4. Settlement, batch, payout, idempotency, uniqueness, version, transaction, and concurrency controls
5. Payee and destination verification, payout minimum, netting, negative balance, and carry-forward
6. Provider request, credentials, timeout, reference, callback, return, and status mapping
7. Ledger, seller balance, transaction status, statement, notification, and reconciliation effects
8. Approval, audit, privacy, monitoring, manual adjustment, support tools, and tests

## Rules the code should protect
- One transaction and financial version must settle at most once
- Gross value must be exactly conserved under documented rounding and residual policy
- Every payout must bind the intended tenant, seller, payee, destination, currency, and settlement
- Only eligible completed and released value may be paid
- Fee, tax, split, exchange, reserve, and adjustment inputs must be versioned and reproducible
- Uncertain provider outcome must not trigger blind duplicate payout
- Provider, ledger, balance, transaction, and statement state must converge
- Financial and personal data must remain protected

## Build or change safely
1. Confirm product decisions before relying on framework or provider defaults.
2. Follow existing authorization, state, financial, storage, logging, monitoring, and test conventions.
3. Bind every action to the authoritative actor, object, evidence or amount, version, state, and scope.
4. Enforce permission, current-state, uniqueness, ordering, and time rules at the write.
5. Make retries and replays safe after partial failure and lost responses.
6. Keep eligibility, access, payout, ledger, and provider inconsistency visible and repairable.
7. Add the core 20 tests.

