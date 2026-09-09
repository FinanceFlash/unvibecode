# Engineering Guide

## Trace the implementation
1. Credential creation, rotation, revocation, expiry, activation, and recovery entry points
2. Requester, owner, service identity, permission, scope, environment, and assignment checks
3. Credential generation, metadata, lifecycle state, expiry, replacement, and invalidation logic
4. Application or service credential loading and protected API authentication checks
5. Rotation coordination, old/new credential overlap, activation, and superseded-credential invalidation
6. Revocation, emergency compromise handling, expiry enforcement, and downstream authorization checks
7. Idempotency keys, uniqueness constraints, concurrency controls, checkpoints, retry, reconciliation, and recovery
8. Audit events, security monitoring, lifecycle notifications, metrics, administrative tools, and tests

## Rules the code should protect
- Only an authorized actor or service may create, rotate, or revoke a credential
- Credential ownership, assignment, environment, scope, and lifecycle state must remain bound to the intended target
- A credential must not become usable before required authorization and activation checks complete
- Credentials must not receive permissions beyond their approved scope
- Expired and revoked credentials must not authorize protected API access
- Completed rotation must leave the previous credential invalidated according to the defined rotation policy
- Temporary credential overlap must be bounded and must not become an unintended permanent state
- Retries and concurrent lifecycle operations must not create duplicate or contradictory credential states
- Partial lifecycle operations must remain identifiable and recoverable rather than being reported as completed
- Lifecycle actions and recovery outcomes must remain traceable through protected audit evidence

## Build or change safely
1. Confirm credential policy, authorization, scope, expiry, rotation, and revocation decisions before relying on framework or provider defaults.
2. Follow the repository's existing authorization, state-management, secret-handling, logging, monitoring, and testing conventions.
3. Bind every lifecycle action to the authoritative actor, credential, owner, application or service, scope, environment, version, and current state.
4. Enforce authorization, scope, uniqueness, lifecycle-state, expiry, concurrency, and revocation rules at the point where they have material effect.
5. Never expose credential secrets through logs, audit records, generated reports, error messages, or test fixtures.
6. Make creation, rotation, revocation, and recovery retries safe after partial failure or lost responses.
7. Keep lifecycle decisions, state transitions, downstream authorization effects, and inconsistencies visible and repairable.
8. Add or update tests covering the core 20 scenarios.