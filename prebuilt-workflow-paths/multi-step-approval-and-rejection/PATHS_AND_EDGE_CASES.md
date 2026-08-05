# Paths and Edge Cases

## Supported paths
- Sequential approval
- Parallel approval
- Quorum or threshold approval
- Delegated or substitute approval
- Rejection with final closure
- Correction and resubmission
- Withdrawal, expiry, escalation, and administrative cancellation
- Downstream handoff, retry, reconciliation, and manual repair

## Normal paths
- All required sequential reviewers approve the submitted version
- A parallel or quorum stage reaches its valid threshold once
- An authorized reviewer rejects with the required reason and the workflow stops correctly

## Denied paths
- Required request evidence or decision data is missing or malformed
- The reviewer is ineligible, conflicted, inactive, or outside scope
- A stale, expired, withdrawn, rejected, or superseded request receives a decision
- Required approval order or quorum is not satisfied

## Timing, concurrency, and boundaries
- Two valid but conflicting decisions arrive together
- The request changes after one or more approvals
- A decision arrives exactly at its deadline
- Delegation, reviewer removal, or role expiry occurs during review
- Final approval overlaps withdrawal, rejection, or administrative cancellation

Cover valid, invalid, duplicate, expired, stale, replayed, repeated, simultaneous, partially completed, unauthorized, and recovery outcomes.

