---
name: understand-marketplace-settlement-code
description: Trace and explain Commission, Fee, Split Payout, and Seller Settlement across an existing codebase. Use when locating entry points, calculations, eligibility, payout effects, retries, recovery, monitoring, and tests.
---

# Understand Marketplace Split Payout and Settlement Code

Trace:
1. Settlement scheduler, transaction event, calculate, approve, hold, release, submit, callback, retry, and reverse entry points
2. Transaction completion, tenant, seller, payee, reserve, dispute, refund, fraud, and compliance checks
3. Gross, currency, version, commission, fee, tax, withholding, reserve, adjustment, exchange, and rounding calculations
4. Settlement, batch, payout, idempotency, uniqueness, version, transaction, and concurrency controls
5. Payee and destination verification, payout minimum, netting, negative balance, and carry-forward
6. Provider request, credentials, timeout, reference, callback, return, and status mapping
7. Ledger, seller balance, transaction status, statement, notification, and reconciliation effects
8. Approval, audit, privacy, monitoring, manual adjustment, support tools, and tests

Explain actors, ownership, money, states, transitions, effects, failures, retries, security boundaries, monitoring, tests, and areas needing verification. Cite files and symbols.

