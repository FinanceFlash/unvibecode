# Retry and Recovery Guide

## Partial failures
- Application commits but acknowledgement or review task fails
- Verification completes externally but local result does not update
- Approval commits but seller-account provisioning fails
- Seller account provisions but category or listing entitlement fails
- Activation succeeds but payout readiness or notification remains inconsistent
- Decision commits but the response is lost

## Recovery rules
- Use applicant, business, application, version, evidence, and provider-check identities consistently.
- Re-read application, verification, review, seller account, scope, and payout readiness before retrying.
- Never duplicate provider accounts or verification requests solely because a response was lost.
- Keep approved-but-not-activated and active-but-incomplete outcomes visible.
- Reconcile application, verification, decision, seller account, entitlement, payout, and communication.

