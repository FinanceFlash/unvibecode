---
name: understand-dispute-chargeback-code
description: Trace and explain Payment Dispute and Chargeback Resolution across an existing codebase. Use when locating intake, linkage, evidence, deadline, ledger, escalation, monitoring, and test paths.
---

# Understand Payment Dispute and Chargeback Resolution Code

Trace:
1. Dispute-webhook, manual-report, evidence-submission, and case-status entry points
2. Actor, account, tenant, and case ownership checks
3. Payment and order lookup used to bind a new case
4. Case model, reason code, deadline, idempotency, and state-machine controls
5. Evidence-bundle storage, representment drafting, and submission paths
6. Provisional debit or credit, reserve adjustment, and ledger posting
7. Liability-shift, auto-accept, and auto-contest policy evaluation
8. Chargeback-ratio aggregation and risk-program status updates
9. Audit, privacy, monitoring, support tools, and tests

Explain actors, ownership, states, transitions, financial effects, failures, retries, security boundaries, monitoring, tests, and areas needing verification. Cite files and symbols.
