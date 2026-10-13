# Permission and Abuse Guide

## Permission boundaries
- One chargeback notification must not open more than one case
- A case must bind the intended payer, merchant, order, tenant, and payment
- Provisional debit or credit must apply exactly once per case
- Evidence deadlines must be enforced from the authoritative reason-code table
- Liability-shift and auto-accept policy must not bypass required manual review

## Misuse paths
- Duplicate provisional debit — Retried webhooks debit the merchant ledger twice for one dispute
- Missed deadline — Valid evidence submitted late is rejected, turning a winnable case into a loss
- Wrong payment linkage — A dispute attaches to the wrong order or payment and corrupts the ledger and customer record
- False resolution status — A pending or under-review case is reported as won or lost prematurely
- Liability-shift miscalculation — The merchant absorbs a loss despite authentication that should shift liability to the issuer
- Duplicate dispute case — A provider retry or duplicate notification opens two cases for one chargeback
- Chargeback-ratio blind spot — A missed risk-program escalation risks account suspension or termination
- Sensitive data exposure — Card number fragments, personal data, or evidence documents reach unsafe logs or unauthorized viewers

Protect actor identity, tenant scope, authoritative business objects, cardholder and evidence data, provider proof, support tools, and audit records. Deny uncertain ownership or permission.
