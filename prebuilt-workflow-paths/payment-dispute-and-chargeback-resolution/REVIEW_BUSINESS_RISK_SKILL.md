---
name: review-dispute-chargeback-risk
description: Review customer, revenue, permission, privacy, and operational risks in Payment Dispute and Chargeback Resolution. Use when founders, PMs, or engineering managers need prioritized consequences, controls, tests, and release concerns.
---

# Review Payment Dispute and Chargeback Resolution Risk

Review intake, linkage, evidence, deadline, concurrency, escalation, ledger, and privacy paths. Prioritize:
- Duplicate provisional debit — Retried webhooks debit the merchant ledger twice for one dispute
- Missed deadline — Valid evidence submitted late is rejected, turning a winnable case into a loss
- Wrong payment linkage — A dispute attaches to the wrong order or payment and corrupts the ledger and customer record
- False resolution status — A pending or under-review case is reported as won or lost prematurely
- Liability-shift miscalculation — The merchant absorbs a loss despite authentication that should shift liability to the issuer
- Duplicate dispute case — A provider retry or duplicate notification opens two cases for one chargeback
- Chargeback-ratio blind spot — A missed risk-program escalation risks account suspension or termination
- Sensitive data exposure — Card number fragments, personal data, or evidence documents reach unsafe logs or unauthorized viewers

For each material risk, explain trigger, behavior, business consequence, protection, decision or test, and acceptance condition.
