---
name: write-checkout-payment-spec
description: Write or review a product specification for Checkout Payment Authorization and Capture. Use when defining actors, states, financial or access rules, policy decisions, edge cases, acceptance criteria, recovery, or business risks.
---

# Write a Checkout Payment Authorization and Capture Specification

Use application-native terms. Decide:
- Immediate capture versus separate authorization and capture
- Authoritative amount, currency, minor-unit, rounding, tax, and discount source
- Who may pay for which checkout or order
- Payment-attempt and provider idempotency policy
- Fraud, velocity, step-up, wallet, and 3-D Secure requirements
- Authorization lifetime, partial capture, incremental capture, and void policy
- Provider success, decline, timeout, and uncertain-outcome meanings
- Whether order commitment precedes, follows, or is atomic with payment
- Ledger, receipt, fulfilment, and customer-notification timing
- Attempt limits, card-testing controls, privacy, monitoring, and manual review

Write scope, actors, objects, states, paths, customer and financial outcomes, permissions, recovery, privacy, misuse, acceptance criteria, and unanswered decisions.

