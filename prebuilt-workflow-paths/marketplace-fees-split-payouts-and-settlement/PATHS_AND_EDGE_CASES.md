# Paths and Edge Cases

## Supported paths
- Single-seller settlement
- Multi-party split payout
- Commission, fee, tax, and withholding deduction
- Reserve or dispute-window hold
- Payout minimum and carry-forward
- Batch payout
- Failed or returned payout retry
- Late adjustment, reversal, reconciliation, and manual repair

## Normal paths
- An eligible completed transaction produces one balanced settlement and payout
- A multi-party split allocates exact payee amounts and one deterministic rounding residual
- Amounts below payout minimum carry forward without losing ledger ownership

## Denied paths
- Transaction, gross amount, currency, payee, fee schedule, or destination is missing or invalid
- Transaction is incomplete, held, disputed, refunded, already settled, or outside policy
- Payee or payout destination is unverified, suspended, or owned elsewhere
- An unauthorized actor requests manual settlement or changes financial inputs

## Timing, concurrency, and boundaries
- Two settlement workers process the same transaction together
- Settlement eligibility or reserve releases exactly at a time boundary
- Fee schedule, tax rule, exchange rate, or payout destination changes after completion
- Provider pays but the response is lost
- Refund, dispute, chargeback, or payout return arrives after settlement

Cover valid, invalid, duplicate, expired, stale, replayed, repeated, simultaneous, partially completed, unauthorized, and recovery outcomes.

