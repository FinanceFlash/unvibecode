---
name: understand-multi-step-approval-code
description: Trace and explain Multi-step Approval and Rejection across an existing codebase. Use when locating entry points, authorization, state, storage, external effects, retries, recovery, monitoring, and tests.
---

# Understand Multi-step Approval Code

Trace:
1. Submission, approve, reject, withdraw, edit, delegate, escalate, and administrative entry points
2. Authentication, tenant, role, assignment, conflict, and separation-of-duties checks
3. Request version, approval policy, stage, quorum, and reviewer-resolution logic
4. Decision validation, reason/evidence requirements, deadlines, and current-state checks
5. Transactions, optimistic locking, uniqueness, and simultaneous-decision handling
6. Finalization and downstream command or event creation
7. Notification, reminder, escalation, retry, reconciliation, and support tools
8. Audit trail, evidence visibility, monitoring, and tests

Explain actors, ownership, states, transitions, effects, failures, retries, security boundaries, monitoring, tests, and areas needing verification. Cite files and symbols.

