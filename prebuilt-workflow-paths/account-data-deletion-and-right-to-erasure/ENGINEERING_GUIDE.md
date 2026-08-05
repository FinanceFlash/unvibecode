# Engineering Guide

## Trace the implementation
1. Deletion request, verify, scope, approve, deny, hold, cancel, execute, confirm, appeal, and support entry points
2. Requester, representative, account, tenant, alias, contact, identity-proof, and permission checks
3. Data inventory, ownership, category, purpose, system, processor, dependency, and derived-data mapping
4. Retention, legal hold, tax, fraud, safety, dispute, contract, and shared-record decisions
5. Account restriction, session, credential, entitlement, billing, and communication consequences
6. Deletion, anonymization, database, file, cache, index, analytics, log, backup, and processor tasks
7. Task idempotency, batching, checkpoint, retry, acknowledgement, reappearance prevention, and reconciliation
8. Privacy, encryption, evidence, deadline, metrics, audit, support tools, and tests

## Rules the code should protect
- Only a verified data subject or authorized representative may initiate destructive work
- Deletion scope must bind the intended account, tenant, identities, data categories, and request version
- Each data location must have an explicit policy-grounded outcome
- Retention exceptions must be minimal, purpose restricted, time bounded, and auditable
- Deletion must not cross account, tenant, shared-record, or legal boundaries
- Completed status requires all mandatory tasks to be resolved
- Retries, replays, restores, and late writes must not recreate or misdelete data
- Identity proof, inventories, retained data, and deletion evidence must remain protected

## Build or change safely
1. Confirm product and policy decisions before relying on framework, model, or provider defaults.
2. Follow existing authorization, state, privacy, storage, logging, monitoring, and test conventions.
3. Bind every action to the authoritative actor, tenant, object, evidence or data scope, version, state, and policy.
4. Enforce permission, current-state, identity, threshold or retention, uniqueness, and time rules at material effects.
5. Make retries and replays safe after partial failure and lost responses.
6. Keep decision, enforcement, deletion, and downstream inconsistency visible and repairable.
7. Add the core 20 tests.

