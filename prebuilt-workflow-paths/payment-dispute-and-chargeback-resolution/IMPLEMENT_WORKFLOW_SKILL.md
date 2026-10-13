---
name: implement-dispute-chargeback
description: Implement or modify Payment Dispute and Chargeback Resolution. Use when adding or changing intake, linkage, evidence, deadline, ledger effects, escalation, liability-shift policy, recovery, or tests.
---

# Implement Payment Dispute and Chargeback Resolution

Confirm:
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

Follow project conventions and protect:
- One chargeback notification must not open more than one case
- A case must bind the intended payer, merchant, order, tenant, and payment
- Provisional debit or credit must apply exactly once per case
- Evidence deadlines must be enforced from the authoritative reason-code table
- Case, ledger, order, and customer records must converge on one outcome
- Liability-shift and auto-accept policy must not bypass required manual review
- Chargeback-ratio status must reflect confirmed outcomes only
- Cardholder data and evidence must remain protected and access-scoped

Add all core tests and summarize decisions, files, state changes, recovery, privacy and security controls, and remaining gaps.
