---
name: implement-marketplace-settlement
description: Implement or modify Commission, Fee, Split Payout, and Seller Settlement. Use when adding or changing validation, authorization, state transitions, eligibility or financial effects, retries, recovery, privacy controls, monitoring, or tests.
---

# Implement Marketplace Split Payout and Settlement

Confirm:
- What makes a transaction complete and settlement eligible
- Settlement delay, reserve, dispute window, fraud hold, and compliance hold
- Authoritative gross amount, currency, fee schedule, tax, withholding, and version
- Split percentages, fixed fees, minimums, caps, rounding, and residual allocation
- Currency conversion source, timestamp, spread, and payout currency
- Payee identity, tenant, seller, bank or wallet verification, and status requirements
- Batching, payout minimum, negative balance, carry-forward, and netting policy
- Provider idempotency, status, timeout, callback, return, and reversal meanings
- How refunds, disputes, chargebacks, and adjustments affect unpaid or paid settlement
- Approval, dual control, retry, privacy, audit, monitoring, and manual-repair policy

Follow project conventions and protect:
- One transaction and financial version must settle at most once
- Gross value must be exactly conserved under documented rounding and residual policy
- Every payout must bind the intended tenant, seller, payee, destination, currency, and settlement
- Only eligible completed and released value may be paid
- Fee, tax, split, exchange, reserve, and adjustment inputs must be versioned and reproducible
- Uncertain provider outcome must not trigger blind duplicate payout
- Provider, ledger, balance, transaction, and statement state must converge
- Financial and personal data must remain protected

Add all core tests and summarize decisions, files, state changes, recovery, privacy and security controls, and remaining gaps.

