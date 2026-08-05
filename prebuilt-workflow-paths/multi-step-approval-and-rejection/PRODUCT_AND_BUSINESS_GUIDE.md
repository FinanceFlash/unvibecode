# Product and Business Guide

## Boundary
Starts when a complete business request is submitted for approval. Ends when the required decision policy produces an approved, rejected, withdrawn, expired, or correction-required outcome and all authorized downstream effects are recorded consistently.

## People and systems
- Requester
- Reviewer or approver
- Delegated or substitute approver
- Process owner or administrator
- Approval and policy service
- Notification and downstream fulfilment services
- Audit, compliance, and support operations

## Things created or changed
- Business request and immutable submitted version
- Approval policy and ordered steps
- Reviewer assignment and delegation
- Decision, reason, evidence, and comment
- Deadline, escalation, and reminder
- Final outcome and downstream command
- Notification and audit record

## Stages
- Request: draft → submitted → under review → approved, rejected, withdrawn, expired, or correction required
- Step: not started → pending → approved, rejected, skipped by policy, cancelled, or expired
- Decision: absent → recorded → superseded only by explicit policy
- Downstream action: not requested → requested → completed or failed

## Product decisions
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

## Happy paths
- All required sequential reviewers approve the submitted version
- A parallel or quorum stage reaches its valid threshold once
- An authorized reviewer rejects with the required reason and the workflow stops correctly

## Negative paths
- Required request evidence or decision data is missing or malformed
- The reviewer is ineligible, conflicted, inactive, or outside scope
- A stale, expired, withdrawn, rejected, or superseded request receives a decision
- Required approval order or quorum is not satisfied

## Edge cases
- Two valid but conflicting decisions arrive together
- The request changes after one or more approvals
- A decision arrives exactly at its deadline
- Delegation, reviewer removal, or role expiry occurs during review
- Final approval overlaps withdrawal, rejection, or administrative cancellation

## Acceptance criteria
1. Only eligible reviewers may decide the assigned step within the correct tenant and scope
2. A decision must bind the exact submitted request version and approval step
3. Required order, quorum, separation-of-duties, and conflict rules must be enforced
4. Changing material request data must follow an explicit approval-invalidation policy
5. One terminal outcome must win under simultaneous or repeated actions
6. Expired, withdrawn, rejected, completed, or superseded work cannot be decided again
7. Final approval must trigger downstream work no more than once
8. Partial failures must be visible, retriable, and reconcilable
9. Requester, reviewer, and audit notifications must follow explicit visibility rules
10. Evidence, comments, identity data, and authorization proof must not be exposed

## Business risks
| Risk | Business consequence |
|---|---|
| Unauthorized approval | An ineligible or out-of-scope person commits a business decision |
| Conflict or self-approval | Separation-of-duties rules are bypassed |
| Skipped approval | A required stage, order, or quorum is ignored |
| Stale-version approval | Reviewers approve data that is no longer authoritative |
| Conflicting final state | Concurrent approve, reject, withdraw, or expire actions disagree |
| Duplicate downstream action | A replayed final decision repeats payment, provisioning, publication, or other work |
| SLA or escalation failure | Important requests remain unattended or go to the wrong substitute |
| Evidence exposure | Sensitive request data or reviewer comments reach the wrong audience or logs |

