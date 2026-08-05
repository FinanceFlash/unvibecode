---
name: implement-account-data-erasure
description: Implement or modify Right-to-erasure and Account-data Deletion. Use when adding or changing validation, authorization, policy, state transitions, external effects, retries, recovery, privacy controls, monitoring, or tests.
---

# Implement Account-data Erasure

Confirm:
- Who may request deletion and what identity or representative proof is required
- How accounts, aliases, tenants, devices, and related identities are resolved
- Which systems, data categories, derived data, and processors are in scope
- Which legal hold, tax, fraud, safety, contract, dispute, or retention exceptions apply
- Delete versus irreversible anonymization for each category
- When account access, sessions, credentials, billing, and entitlements are restricted
- How shared, multi-user, public, transactional, audit, and security records are handled
- Backup, archive, replica, cache, search, analytics, and model-derived data policy
- Completion deadline, extension, notification, appeal, cancellation, and support policy
- Deletion proof, reappearance prevention, retry, monitoring, privacy, and audit policy

Follow project conventions and protect:
- Only a verified data subject or authorized representative may initiate destructive work
- Deletion scope must bind the intended account, tenant, identities, data categories, and request version
- Each data location must have an explicit policy-grounded outcome
- Retention exceptions must be minimal, purpose restricted, time bounded, and auditable
- Deletion must not cross account, tenant, shared-record, or legal boundaries
- Completed status requires all mandatory tasks to be resolved
- Retries, replays, restores, and late writes must not recreate or misdelete data
- Identity proof, inventories, retained data, and deletion evidence must remain protected

Add all core tests and summarize decisions, files, state changes, recovery, privacy and security controls, and remaining gaps.

