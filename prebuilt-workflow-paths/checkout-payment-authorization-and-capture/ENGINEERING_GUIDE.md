# Engineering Guide

## Trace the implementation
1. Checkout, pay, authenticate, authorize, capture, void, cancel, and status entry points
2. Actor, account, tenant, order ownership, payable-state, and merchant checks
3. Amount, currency, tax, discount, rounding, and minor-unit calculation source
4. Payment-attempt model, idempotency, uniqueness, state machine, and concurrency controls
5. Fraud, velocity, step-up, wallet, and customer-authentication paths
6. Provider request, credential handling, timeout, decline, reference, and status mapping
7. Order, ledger, fulfilment, receipt, notification, and reconciliation effects
8. Audit, privacy, monitoring, support tools, and tests

## Rules the code should protect
- One payable checkout must not produce more than one permitted charge
- Provider amount and currency must equal the authoritative checkout
- Every provider action must bind the intended payer, merchant, order, tenant, and attempt
- Current attempt and authorization state must be enforced at capture
- Uncertain provider outcomes must not trigger blind duplicate payment
- Order, payment, ledger, and fulfilment must converge on one business outcome
- Attempt and fraud controls must remain bounded
- Payment secrets and unnecessary personal data must remain protected

## Build or change safely
1. Confirm product decisions before relying on framework or provider defaults.
2. Follow existing authorization, financial-state, storage, logging, monitoring, and test conventions.
3. Bind every action to the authoritative actor, object, amount or quantity, version, state, and scope.
4. Enforce permission, current-state, uniqueness, ordering, and time rules at the write.
5. Make retries and replays safe after partial failure and lost responses.
6. Keep money, access, order, and inventory inconsistency visible and repairable.
7. Add the core 20 tests.

