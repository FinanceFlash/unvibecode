# Paths and Edge Cases

## Supported paths
- Dispute or chargeback intake from a provider webhook or manual report
- Reason-code classification and evidence-deadline assignment
- Evidence collection and representment submission
- Auto-accept and auto-contest policy for low-value or clear-cut cases
- Liability-shift determination for authenticated transactions
- Escalation to pre-arbitration or arbitration where the network allows it
- Provisional debit, reserve adjustment, and final ledger settlement
- Chargeback-ratio monitoring and merchant risk-program status

## Normal paths
- A valid dispute links to its original payment once and complete evidence wins the case before the deadline
- A low-value dispute is auto-accepted by policy without wasted evidence effort
- An authenticated transaction wins through liability shift

## Denied paths
- A dispute references a payment or order that does not exist or was never captured
- Evidence is submitted after the network deadline
- The dispute amount or currency does not match the original payment
- The actor lacks access to the dispute case or tenant

## Timing, concurrency, and boundaries
- Two dispute webhooks for the same case arrive together
- The evidence deadline falls at a timezone or network cutover boundary
- A case escalates to pre-arbitration after an initial win or loss
- The cardholder withdraws the dispute after representment was submitted
- The disputed order was already fully refunded before the case opened

Cover valid, invalid, duplicate, expired, stale, replayed, repeated, simultaneous, partially completed, unauthorized, and recovery outcomes.
