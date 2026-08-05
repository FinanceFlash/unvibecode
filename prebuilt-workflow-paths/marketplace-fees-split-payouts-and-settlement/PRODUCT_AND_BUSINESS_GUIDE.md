# Product and Business Guide

## Boundary
Starts when a marketplace transaction is complete and eligible for settlement. Ends when gross value is conserved across fees, taxes, reserves, adjustments, and payee amounts and each payout is held, submitted, paid, failed, or reversed exactly once with ledger and transaction state reconciled.

## People and systems
- Seller, provider, partner, or other payee
- Marketplace transaction and settlement services
- Commission, pricing, tax, and withholding services
- Ledger and finance systems
- Payout provider, bank, or wallet
- Risk, reserve, dispute, and compliance services
- Operations, support, security, and audit teams

## Things created or changed
- Completed marketplace transaction and settlement eligibility
- Gross amount, currency, exchange rate, and financial version
- Commission, platform fee, partner split, tax, withholding, reserve, refund, and adjustment
- Payee, payout destination reference, and eligibility
- Settlement, batch, payout instruction, idempotency key, and provider reference
- Ledger entries, balances, reconciliation exception, statement, and audit record

## Stages
- Transaction: completed → settlement pending → eligible, held, settled, or exception
- Settlement: uncalculated → calculated → approved → submitted → paid, failed, held, reversed, or partially settled
- Payout: pending → provider accepted → paid, failed, returned, or uncertain
- Ledger: pending → posted, reversed, or exception

## Product decisions
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

## Happy paths
- An eligible completed transaction produces one balanced settlement and payout
- A multi-party split allocates exact payee amounts and one deterministic rounding residual
- Amounts below payout minimum carry forward without losing ledger ownership

## Negative paths
- Transaction, gross amount, currency, payee, fee schedule, or destination is missing or invalid
- Transaction is incomplete, held, disputed, refunded, already settled, or outside policy
- Payee or payout destination is unverified, suspended, or owned elsewhere
- An unauthorized actor requests manual settlement or changes financial inputs

## Edge cases
- Two settlement workers process the same transaction together
- Settlement eligibility or reserve releases exactly at a time boundary
- Fee schedule, tax rule, exchange rate, or payout destination changes after completion
- Provider pays but the response is lost
- Refund, dispute, chargeback, or payout return arrives after settlement

## Acceptance criteria
1. Only a complete eligible transaction may settle
2. Transaction, tenant, seller, payees, amount, currency, version, and payout destinations must remain bound
3. Gross value must equal fees, taxes, reserves, adjustments, and payee amounts under explicit rounding policy
4. One transaction and financial version must not settle or pay more than once
5. Fee, tax, split, exchange-rate, and withholding versions must be reproducible
6. Held, disputed, refunded, reversed, or ineligible value cannot be paid outside explicit policy
7. Payout provider, ledger, seller balance, transaction, and statement must converge
8. Repeated, simultaneous, callback, or lost-response execution must return one settlement outcome
9. Financial approval and manual adjustment must use scoped authority and immutable audit
10. Bank references, tax data, balances, provider secrets, and personal data must remain protected

## Business risks
| Risk | Business consequence |
|---|---|
| Duplicate payout | Concurrency, replay, or lost responses pay a seller more than once |
| Wrong payee | Seller, tenant, or destination mapping sends funds elsewhere |
| Incorrect commission or split | Fee version, percentage, tax, rounding, or currency errors misallocate value |
| Unbalanced settlement | Gross, fees, taxes, reserves, adjustments, and payouts do not conserve money |
| Premature payout | Incomplete, disputed, refundable, fraudulent, or held transactions release funds |
| Ledger–provider divergence | Money moves externally while internal balances or transaction status disagree |
| Unauthorized manual adjustment | A privileged action changes fees, payees, holds, or payout state improperly |
| Sensitive-data exposure | Bank, tax, balance, transaction, or provider data reaches unsafe logs |

