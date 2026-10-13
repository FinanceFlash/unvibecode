# Engineering Guide

## Trace the implementation
1. Dispute-webhook, manual-report, evidence-submission, and case-status entry points
2. Actor, account, tenant, and case ownership checks
3. Payment and order lookup used to bind a new case
4. Case model, reason code, deadline, idempotency, and state-machine controls
5. Evidence-bundle storage, representment drafting, and submission paths
6. Provisional debit or credit, reserve adjustment, and ledger posting
7. Liability-shift, auto-accept, and auto-contest policy evaluation
8. Chargeback-ratio aggregation and risk-program status updates
9. Audit, privacy, monitoring, support tools, and tests

## Rules the code should protect
- One chargeback notification must not open more than one case
- A case must bind the intended payer, merchant, order, tenant, and payment
- Provisional debit or credit must apply exactly once per case
- Evidence deadlines must be enforced from the authoritative reason-code table
- Case, ledger, order, and customer records must converge on one outcome
- Liability-shift and auto-accept policy must not bypass required manual review
- Chargeback-ratio status must reflect confirmed outcomes only
- Cardholder data and evidence must remain protected and access-scoped

## Build or change safely
1. Confirm product decisions before relying on framework or provider defaults.
2. Follow existing authorization, financial-state, storage, logging, monitoring, and test conventions.
3. Bind every action to the authoritative actor, case, payment, order, tenant, and state.
4. Enforce permission, current-state, uniqueness, ordering, and deadline rules at the write.
5. Make retries and replays safe after partial failure and lost responses.
6. Keep ledger, order, and risk-program inconsistency visible and repairable.
7. Add the core 20 tests.
