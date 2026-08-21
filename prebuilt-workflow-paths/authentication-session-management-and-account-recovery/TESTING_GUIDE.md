# Testing Guide

Check authoritative records, state transitions, permissions, external effects, recovery, and audit changes—not only HTTP responses or user-interface messages.

## 1. All sequential reviewers approve

**Given:** A valid submitted request has two ordered eligible reviewers

**When:** Each reviewer approves in the required order

**Expect:** The request becomes approved once and the downstream handoff is recorded

**Must not happen:** A later step starts early or finalization runs twice

**Best test levels:** Integration and end-to-end.

## 2. Parallel stage reaches quorum

**Given:** A valid policy requires two of three eligible approvals

**When:** Two reviewers approve

**Expect:** The stage and request advance exactly once

**Must not happen:** A non-vote counts or additional responses duplicate effects

**Best test levels:** Integration.

## 3. Authorized reviewer rejects

**Given:** A pending step permits rejection and requires a reason

**When:** The assigned reviewer rejects

**Expect:** The workflow reaches the written rejection outcome and stops or opens correction

**Must not happen:** Later stages proceed as though approved

**Best test levels:** API and integration.

## 4. Required request evidence is missing

**Given:** A submitted request lacks a required document or field

**When:** Submission or review validation runs

**Expect:** The request is rejected or returned for correction before approval

**Must not happen:** An incomplete request reaches final approval

**Best test levels:** Unit and API.

## 5. Decision input is malformed

**Given:** A decision contains an invalid value, reason, attachment, or excessive payload

**When:** The reviewer submits it

**Expect:** Validation fails safely without changing the step

**Must not happen:** Malformed content reaches storage, rendering, or logs unsafely

**Best test levels:** Unit, API, and security.

## 6. Reviewer is no longer eligible

**Given:** The assigned reviewer lost the required role, seat, employment, or membership

**When:** They attempt a decision

**Expect:** Current eligibility is checked and the action is denied or reassigned

**Must not happen:** Old assignment alone authorizes approval

**Best test levels:** Authorization integration.

## 7. Requester attempts self-approval

**Given:** Policy requires separation of duties

**When:** The requester or conflicted owner attempts to approve

**Expect:** Conflict policy blocks or routes the decision

**Must not happen:** Self-approval bypasses required independent review

**Best test levels:** Security and policy.

## 8. Request changes after approval

**Given:** An earlier step approved version one and material fields are edited

**When:** Review continues on version two

**Expect:** Prior decisions are invalidated or retained only by explicit policy

**Must not happen:** Version two inherits stale approval silently

**Best test levels:** Integration.

## 9. Approve and reject arrive together

**Given:** Two eligible actions target the same pending step concurrently

**When:** Both transactions execute

**Expect:** One authoritative outcome follows policy and the other sees current state

**Must not happen:** The workflow ends both approved and rejected

**Best test levels:** Concurrency integration.

## 10. Decision arrives at deadline

**Given:** A step is tested immediately before, at, and after its deadline

**When:** The reviewer decides

**Expect:** One explicit server-time boundary rule is applied

**Must not happen:** Client time or race conditions extend eligibility unpredictably

**Best test levels:** Unit with controlled time.

## 11. Submission response is lost

**Given:** The request may already be submitted and reviewers assigned

**When:** The client repeats submission

**Expect:** The existing result is returned or one new version is created safely

**Must not happen:** Duplicate workflows and notifications are created

**Best test levels:** API and integration.

## 12. Recorded decision is replayed

**Given:** A reviewer decision already committed

**When:** The same action or event is submitted again

**Expect:** It is rejected or returns a safe idempotent result

**Must not happen:** Votes, finalization, or downstream effects repeat

**Best test levels:** Integration and security.

## 13. Approval actions are automated or flooded

**Given:** One actor repeatedly submits decisions, reminders, or bulk operations

**When:** Abuse limits are reached

**Expect:** Further activity is bounded, auditable, and safely handled

**Must not happen:** Notification amplification or policy bypass occurs

**Best test levels:** Security and load.

## 14. Decision commits but notification fails

**Given:** The authoritative decision is stored but a message cannot be sent

**When:** Recovery runs

**Expect:** The decision remains correct and notification is retried or recorded failed

**Must not happen:** The decision is rolled back incorrectly or repeated

**Best test levels:** Integration.

## 15. Policy or identity dependency times out

**Given:** Reviewer eligibility or approval policy cannot be confirmed

**When:** A decision is attempted

**Expect:** The action fails closed or enters explicit recoverable uncertainty

**Must not happen:** Unverified eligibility becomes approval

**Best test levels:** Dependency contract and integration.

## 16. Final approval response is lost

**Given:** The request may already be approved and downstream handoff created

**When:** The client repeats the last approval

**Expect:** Current state returns one clear outcome

**Must not happen:** Finalization or downstream work runs again

**Best test levels:** Integration and API.

## 17. Cross-tenant reviewer attempts action

**Given:** A valid reviewer identifier belongs to another organization

**When:** They try to view or decide the request

**Expect:** Tenant ownership and assignment checks deny access

**Must not happen:** Identifiers alone cross the tenant boundary

**Best test levels:** Authorization and security.

## 18. Sensitive evidence causes an error

**Given:** The request contains confidential evidence and reviewer comments

**When:** Validation, rendering, logging, or notification fails

**Expect:** Errors remain useful without exposing protected content

**Must not happen:** Evidence, comments, or authorization proof appears in unsafe logs or messages

**Best test levels:** Security and log inspection.

## 19. Late approval follows terminal action

**Given:** The request was rejected, withdrawn, expired, or cancelled

**When:** A delayed approval arrives

**Expect:** Current terminal state blocks the decision

**Must not happen:** The request returns to approved through a stale action

**Best test levels:** Integration.

## 20. Approved request downstream work fails

**Given:** The approval is final but payment, provisioning, publication, or another effect fails

**When:** Reconciliation runs

**Expect:** The failure is visible and repaired without changing decision history or duplicating work

**Must not happen:** The system reports complete while the business outcome is missing

**Best test levels:** Integration and operations.

