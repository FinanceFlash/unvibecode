---
name: implement-checkout-payment
description: Implement or modify Checkout Payment Authorization and Capture. Use when adding or changing validation, authorization, state transitions, financial or access effects, retries, recovery, privacy controls, monitoring, or tests.
---

# Implement Checkout Payment Authorization and Capture

Confirm:
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

Follow project conventions and protect:
- One payable checkout must not produce more than one permitted charge
- Provider amount and currency must equal the authoritative checkout
- Every provider action must bind the intended payer, merchant, order, tenant, and attempt
- Current attempt and authorization state must be enforced at capture
- Uncertain provider outcomes must not trigger blind duplicate payment
- Order, payment, ledger, and fulfilment must converge on one business outcome
- Attempt and fraud controls must remain bounded
- Payment secrets and unnecessary personal data must remain protected

Add all core tests and summarize decisions, files, state changes, recovery, privacy and security controls, and remaining gaps.

