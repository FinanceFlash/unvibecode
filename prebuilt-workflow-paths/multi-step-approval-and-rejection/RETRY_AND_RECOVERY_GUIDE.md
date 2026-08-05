# Retry and Recovery Guide

## Partial failures
- Submission commits but acknowledgement or reviewer notification fails
- Decision commits but the response is lost
- Final approval commits but downstream command creation fails
- Downstream command exists but fulfilment fails
- Reminder or escalation fires after a decision
- Reviewer eligibility changes between assignment and decision

## Recovery rules
- Re-read the authoritative request version, step, reviewer eligibility, and terminal state before retrying.
- Use idempotent decision and finalization operations tied to request version and step.
- Do not repeat downstream work, reminders, or notifications unintentionally.
- Distinguish safe retry, uncertain outcome, final denial, and manual review.
- Reconcile approval outcome with every downstream system and preserve an immutable decision trail.

