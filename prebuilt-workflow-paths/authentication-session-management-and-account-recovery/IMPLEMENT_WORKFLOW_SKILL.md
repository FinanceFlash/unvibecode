---
name: implement-multi-step-approval
description: Implement or modify Multi-step Approval and Rejection. Use when adding or changing validation, authorization, state transitions, external effects, retries, recovery, privacy controls, monitoring, or tests.
---

# Implement Multi-step Approval

Confirm:
- Sequential, parallel, or quorum decision policy
- Who can approve each step and whether delegation is permitted
- Whether requesters, owners, or conflicted people may approve
- What edits invalidate earlier decisions
- Whether rejection is final or allows correction and resubmission
- Deadline, reminder, escalation, and substitute-reviewer policy
- Whether an approval may be withdrawn or reversed
- What finalization triggers and whether it must be atomic
- Notification, audit-retention, and evidence-visibility policy
- Duplicate, replay, automation, and bulk-action limits

Follow project conventions and protect:
- Only eligible reviewers may act within their assigned tenant, step, and scope
- Every decision must bind the authoritative submitted request version
- Required order, quorum, conflict, and separation-of-duties policy must hold
- Material edits must not silently retain stale approvals
- One terminal workflow outcome must be authoritative
- Retries and replays must not duplicate decisions or downstream effects
- Deadlines and escalations must use trusted time and current state
- Evidence, comments, and reviewer identity must follow visibility policy

Add all core tests and summarize decisions, files, state changes, recovery, privacy and security controls, and remaining gaps.

