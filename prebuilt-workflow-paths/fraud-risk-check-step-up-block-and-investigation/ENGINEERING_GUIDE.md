# Engineering Guide

## Trace the implementation
1. Protected-action, score, challenge, challenge-result, hold, block, release, override, case, and support entry points
2. Actor, account, tenant, business-action, reviewer, and permission checks
3. Signal collection, source trust, feature mapping, freshness, quality, missing values, and versioning
4. Rule engine, model request, score calibration, thresholds, reason codes, and policy version
5. Decision model, idempotency, lifetime, uniqueness, concurrency, and current-action binding
6. Step-up creation, attempts, proof verification, expiry, replay protection, and resumption
7. Enforcement, transaction or account effect, case creation, notification, override, and reconciliation
8. Privacy, fairness, monitoring, drift, metrics, audit, support tools, and tests

## Rules the code should protect
- Every decision must bind the current protected action, actor, account, tenant, and feature snapshot
- Only trusted fresh signals and approved model, rule, and policy versions may decide
- Threshold and missing-data behavior must be deterministic and explicit
- Step-up proof must bind the same unexpired decision and action
- Enforcement and case effects must match the authoritative decision exactly once
- Overrides must use scoped authority, evidence, reason, and audit
- Retries and replays must not duplicate or bypass risk controls
- Signals, scores, rules, personal data, and credentials must remain protected

## Build or change safely
1. Confirm product and policy decisions before relying on framework, model, or provider defaults.
2. Follow existing authorization, state, privacy, storage, logging, monitoring, and test conventions.
3. Bind every action to the authoritative actor, tenant, object, evidence or data scope, version, state, and policy.
4. Enforce permission, current-state, identity, threshold or retention, uniqueness, and time rules at material effects.
5. Make retries and replays safe after partial failure and lost responses.
6. Keep decision, enforcement, deletion, and downstream inconsistency visible and repairable.
7. Add the core 20 tests.

