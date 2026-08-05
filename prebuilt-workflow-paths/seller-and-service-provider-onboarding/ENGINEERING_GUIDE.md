# Engineering Guide

## Trace the implementation
1. Application create, edit, submit, withdraw, resubmit, approve, reject, activate, suspend, revalidate, and support entry points
2. Applicant, representative, business, tenant, reviewer, category, region, and permission checks
3. Data validation, applicant and business deduplication, and versioning
4. Document upload, malware handling, ownership binding, expiry, verification-provider request, callback, and result mapping
5. Review task, evidence visibility, dual control, decision reason, exception, and concurrency controls
6. Seller account, membership, role, listing, category, territory, and entitlement provisioning
7. Payout readiness, tax state, notification, audit, and revalidation scheduling
8. Privacy, retention, fraud, monitoring, reconciliation, support tools, and tests

## Rules the code should protect
- Only an authorized representative may control the intended application
- Required eligibility and verification checks must pass before active supply access
- Every decision must bind the authoritative application and evidence version
- Reviewers and exceptions must remain within category, region, tenant, and authority scope
- Duplicate identity or business resolution must not merge unrelated providers or permit evasion
- Activation scope must match the approved category, territory, role, and payout readiness
- Expired, withdrawn, rejected, suspended, or superseded state must block stale activation
- Identity, ownership, bank, tax, and review evidence must remain protected

## Build or change safely
1. Confirm product decisions before relying on framework or provider defaults.
2. Follow existing authorization, state, financial, storage, logging, monitoring, and test conventions.
3. Bind every action to the authoritative actor, object, evidence or amount, version, state, and scope.
4. Enforce permission, current-state, uniqueness, ordering, and time rules at the write.
5. Make retries and replays safe after partial failure and lost responses.
6. Keep eligibility, access, payout, ledger, and provider inconsistency visible and repairable.
7. Add the core 20 tests.

