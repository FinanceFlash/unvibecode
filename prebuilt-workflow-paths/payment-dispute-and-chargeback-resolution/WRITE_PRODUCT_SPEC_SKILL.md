---
name: write-dispute-chargeback-spec
description: Write or review a product specification for Payment Dispute and Chargeback Resolution. Use when defining actors, states, deadline or evidence rules, policy decisions, edge cases, acceptance criteria, recovery, or business risks.
---

# Write a Payment Dispute and Chargeback Resolution Specification

Use application-native terms. Decide:
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

Write scope, actors, objects, states, paths, customer and financial outcomes, permissions, recovery, privacy, misuse, acceptance criteria, and unanswered decisions.
