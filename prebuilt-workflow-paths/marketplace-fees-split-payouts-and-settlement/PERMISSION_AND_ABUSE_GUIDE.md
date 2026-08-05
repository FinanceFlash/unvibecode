# Permission and Abuse Guide

## Permission boundaries
- One transaction and financial version must settle at most once
- Gross value must be exactly conserved under documented rounding and residual policy
- Every payout must bind the intended tenant, seller, payee, destination, currency, and settlement
- Only eligible completed and released value may be paid
- Fee, tax, split, exchange, reserve, and adjustment inputs must be versioned and reproducible

## Misuse paths
- Duplicate payout — Concurrency, replay, or lost responses pay a seller more than once
- Wrong payee — Seller, tenant, or destination mapping sends funds elsewhere
- Incorrect commission or split — Fee version, percentage, tax, rounding, or currency errors misallocate value
- Unbalanced settlement — Gross, fees, taxes, reserves, adjustments, and payouts do not conserve money
- Premature payout — Incomplete, disputed, refundable, fraudulent, or held transactions release funds
- Ledger–provider divergence — Money moves externally while internal balances or transaction status disagree
- Unauthorized manual adjustment — A privileged action changes fees, payees, holds, or payout state improperly
- Sensitive-data exposure — Bank, tax, balance, transaction, or provider data reaches unsafe logs

Protect actor identity, tenant scope, application or transaction records, financial and identity data, provider proof, support tools, and audit records. Deny uncertain ownership or permission.

