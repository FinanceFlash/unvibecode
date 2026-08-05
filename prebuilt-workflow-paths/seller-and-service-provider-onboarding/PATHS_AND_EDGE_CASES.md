# Paths and Edge Cases

## Supported paths
- Individual seller onboarding
- Business or service-provider onboarding
- Automated checks followed by approval
- Manual or dual-control review
- Information request and resubmission
- Rejection, withdrawal, expiry, suspension, and reactivation
- Payout readiness and seller-account activation
- Provider uncertainty, reconciliation, and manual repair

## Normal paths
- A valid eligible provider passes required checks and receives one correctly scoped active account
- A reviewer requests missing information and the applicant resubmits a new reviewable version
- An ineligible or failed application is rejected with the allowed reason and no supply access

## Denied paths
- Required applicant, business, category, evidence, or payout data is missing or invalid
- The provider, territory, category, licence, or owner is ineligible
- The actor cannot submit or change the application
- Evidence is expired, forged, mismatched, reused, or belongs elsewhere

## Timing, concurrency, and boundaries
- Two reviewers approve and reject together
- Evidence expires exactly during decision or activation
- Applicant changes ownership, bank, category, or territory after verification
- Verification provider succeeds but the response is lost
- Approval overlaps withdrawal, suspension, duplicate resolution, or support action

Cover valid, invalid, duplicate, expired, stale, replayed, repeated, simultaneous, partially completed, unauthorized, and recovery outcomes.

