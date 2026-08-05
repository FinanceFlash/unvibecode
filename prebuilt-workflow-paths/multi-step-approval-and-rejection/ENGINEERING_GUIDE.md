# Engineering Guide

## Trace the implementation
1. Submission, approve, reject, withdraw, edit, delegate, escalate, and administrative entry points
2. Authentication, tenant, role, assignment, conflict, and separation-of-duties checks
3. Request version, approval policy, stage, quorum, and reviewer-resolution logic
4. Decision validation, reason/evidence requirements, deadlines, and current-state checks
5. Transactions, optimistic locking, uniqueness, and simultaneous-decision handling
6. Finalization and downstream command or event creation
7. Notification, reminder, escalation, retry, reconciliation, and support tools
8. Audit trail, evidence visibility, monitoring, and tests

## Rules the code should protect
- Only eligible reviewers may act within their assigned tenant, step, and scope
- Every decision must bind the authoritative submitted request version
- Required order, quorum, conflict, and separation-of-duties policy must hold
- Material edits must not silently retain stale approvals
- One terminal workflow outcome must be authoritative
- Retries and replays must not duplicate decisions or downstream effects
- Deadlines and escalations must use trusted time and current state
- Evidence, comments, and reviewer identity must follow visibility policy

## Build or change safely
1. Confirm the product decisions before relying on framework or provider defaults.
2. Follow existing authorization, state, storage, logging, monitoring, and test conventions.
3. Bind every action to the authoritative actor, object, version, state, and scope.
4. Enforce permission, current-state, uniqueness, ordering, and time rules at the write.
5. Make retries and replays safe after partial failure and lost responses.
6. Keep downstream inconsistency visible and repairable.
7. Add the core 20 tests.

