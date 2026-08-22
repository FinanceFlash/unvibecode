---
name: review-marketplace-settlement-risk
description: Review customer, revenue, permission, privacy, and operational risks in Commission, Fee, Split Payout, and Seller Settlement. Use when founders, PMs, or engineering managers need prioritized consequences, controls, tests, and release concerns.
---

# Review Marketplace Split Payout and Settlement Risk

Review entry, evidence or money, authorization, state, timing, concurrency, external effects, retry, recovery, privacy, and support paths. Prioritize:
- Duplicate payout — Concurrency, replay, or lost responses pay a seller more than once
- Wrong payee — Seller, tenant, or destination mapping sends funds elsewhere
- Incorrect commission or split — Fee version, percentage, tax, rounding, or currency errors misallocate value
- Unbalanced settlement — Gross, fees, taxes, reserves, adjustments, and payouts do not conserve money
- Premature payout — Incomplete, disputed, refundable, fraudulent, or held transactions release funds
- Ledger–provider divergence — Money moves externally while internal balances or transaction status disagree
- Unauthorized manual adjustment — A privileged action changes fees, payees, holds, or payout state improperly
- Sensitive-data exposure — Bank, tax, balance, transaction, or provider data reaches unsafe logs

For each material risk, explain trigger, behavior, business consequence, protection, decision or test, and acceptance condition. Also state Required Skills: the specific developer expertise (for example, programming language, framework or library, database technology, authentication/authorization, concurrency, idempotency, transaction management, webhook handling, queue processing, caching, external integration, API design, or infrastructure/deployment concern) needed to understand and fix the risk. Derive Required Skills only from the trigger, behavior, and affected code or workflow already identified for that risk; do not invent technologies or expertise the evidence does not support, and keep the list concise. If no specialised expertise beyond general application development is evident, say so instead of guessing.

