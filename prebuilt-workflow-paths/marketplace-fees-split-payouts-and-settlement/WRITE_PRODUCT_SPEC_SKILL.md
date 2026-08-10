---
name: write-marketplace-settlement-spec
description: Write or review a product specification for Commission, Fee, Split Payout, and Seller Settlement. Use when defining financial rules, states, permissions, edge cases, recovery, or business risks.
---

# Write a Marketplace Split Payout and Settlement Specification

Use application-native terms. Decide:
- What makes a transaction complete and settlement eligible
- Settlement delay, reserve, dispute window, fraud hold, and compliance hold
- Authoritative gross amount, currency, fee schedule, tax, withholding, and version
- Split percentages, fixed fees, minimums, caps, rounding, and residual allocation
- Currency-conversion source, timestamp, spread, and payout currency
- Payee identity, tenant, seller, destination verification, and status requirements
- Batching, payout minimum, negative balance, carry-forward, and netting policy
- Provider idempotency, status, timeout, callback, return, and reversal meanings
- How refunds, disputes, chargebacks, and adjustments affect unpaid or paid settlement
- Approval, dual control, retry, privacy, audit, monitoring, and manual repair

Write scope, actors, objects, states, paths, financial outcomes, permissions, recovery, privacy, misuse, acceptance criteria, and unanswered decisions.

