# Product and Business Guide

## Boundary
Starts when a cardholder, issuer, or network raises a dispute or chargeback against a previously captured or settled payment. Ends when the case is won, lost, accepted, withdrawn, or expires, with the ledger, order, and customer outcome recorded consistently, including any escalation to a final network decision.

## People and systems
- Cardholder or authorized disputant
- Issuing bank or card network
- Acquirer or payment provider
- Merchant dispute or chargeback team
- Payment orchestration and ledger services
- Fraud and risk team
- Customer support and notification services
- Finance and reconciliation team

## Things created or changed
- Dispute or chargeback case
- Reason code and network evidence deadline
- Evidence bundle and representment submission
- Provisional debit or credit and reserve adjustment
- Dispute outcome and liability decision
- Ledger entry, chargeback fee, and settlement record
- Merchant chargeback-ratio and risk-program status
- Customer communication record

## Stages
- Dispute case: opened → evidence-due → submitted → under-review → won, lost, accepted, expired, or withdrawn
- Representment: not started → drafted → submitted → accepted or rejected → pre-arbitration or arbitration where the network allows it
- Funds: captured → provisionally debited → reinstated on win or finalized reversal on loss
- Merchant risk: normal → monitored → excessive-chargeback program

## Product decisions
- Which reason codes are auto-contested, auto-accepted, or routed to manual review
- Evidence requirements per reason code and network
- Deadline source of truth: network, provider, or internal buffer
- Auto-accept threshold below the cost of contesting a case
- Provisional debit timing and merchant reserve policy
- Liability-shift rules for authenticated or tokenized transactions
- Escalation path and approval for pre-arbitration or arbitration
- Chargeback-ratio thresholds and the resulting account actions
- Customer communication policy while a case is active
- How one dispute binds to exactly one payment and order, including split or partial disputes

## Happy paths
- A valid dispute links to its original payment once and complete evidence is submitted before the deadline, winning the case
- A low-value dispute is auto-accepted by policy without wasted evidence effort
- An authenticated transaction wins through liability shift

## Negative paths
- A dispute references a payment or order that does not exist or was never captured
- Evidence is submitted after the network deadline
- The dispute amount or currency does not match the original payment
- The actor lacks access to the dispute case or tenant

## Edge cases
- Two dispute webhooks for the same case arrive together
- The evidence deadline falls at a timezone or network cutover boundary
- A case escalates to pre-arbitration after an initial win or loss
- The cardholder withdraws the dispute after representment was submitted
- The disputed order was already fully refunded before the case opened
- Merchant chargeback ratio crosses the risk threshold mid-case

## Acceptance criteria
1. Only a dispute matching an existing captured or settled payment may open a case
2. Each chargeback notification must resolve to one case bound to actor, tenant, order, and payment
3. Provisional debit or credit must apply exactly once per case even under retried webhooks
4. Evidence submitted after the network deadline must be rejected or flagged, never accepted silently as timely
5. Reason code, deadline, and required evidence type must come from one authoritative table
6. Case outcome must reconcile ledger, order, and customer records without contradiction
7. Auto-accept and auto-contest policy must not bypass manual review above the configured threshold
8. Liability-shift determination must rely on authoritative authentication evidence, not assumption
9. Chargeback-ratio and risk-program status must update from confirmed outcomes only, not opened cases
10. Dispute evidence and cardholder data must remain access-scoped and auditable

## Business risks
| Risk | Business consequence |
|---|---|
| Duplicate provisional debit | Retried webhooks debit the merchant ledger twice for one dispute |
| Missed deadline | Valid evidence submitted late is rejected, turning a winnable case into a loss |
| Wrong payment linkage | A dispute attaches to the wrong order or payment and corrupts the ledger and customer record |
| False resolution status | A pending or under-review case is reported as won or lost prematurely |
| Liability-shift miscalculation | The merchant absorbs a loss despite authentication that should shift liability to the issuer |
| Duplicate dispute case | A provider retry or duplicate notification opens two cases for one chargeback |
| Chargeback-ratio blind spot | A missed risk-program escalation risks account suspension or termination |
| Sensitive data exposure | Card number fragments, personal data, or evidence documents reach unsafe logs or unauthorized viewers |
