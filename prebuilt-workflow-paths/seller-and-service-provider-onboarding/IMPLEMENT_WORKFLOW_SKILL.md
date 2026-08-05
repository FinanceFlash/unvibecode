---
name: implement-provider-onboarding
description: Implement or modify Seller or Service-provider Onboarding and Eligibility. Use when adding or changing validation, authorization, state transitions, eligibility or financial effects, retries, recovery, privacy controls, monitoring, or tests.
---

# Implement Seller or Service-provider Onboarding

Confirm:
- Eligible provider types, categories, territories, regions, ages, and business forms
- Required identity, ownership, company, licence, insurance, tax, and background evidence
- Automated approval, manual review, dual control, and exception policy
- Applicant and business deduplication policy
- Which data changes invalidate checks or require reapproval
- Payout-account verification and whether it blocks activation
- Category, listing, territory, role, seat, and entitlement scope at activation
- Document expiry, periodic revalidation, suspension, and reactivation rules
- Applicant-visible reasons, appeal, correction, withdrawal, and retention policy
- Application-rate, fraud, impersonation, privacy, audit, monitoring, and support controls

Follow project conventions and protect:
- Only an authorized representative may control the intended application
- Required eligibility and verification checks must pass before active supply access
- Every decision must bind the authoritative application and evidence version
- Reviewers and exceptions must remain within category, region, tenant, and authority scope
- Duplicate identity or business resolution must not merge unrelated providers or permit evasion
- Activation scope must match the approved category, territory, role, and payout readiness
- Expired, withdrawn, rejected, suspended, or superseded state must block stale activation
- Identity, ownership, bank, tax, and review evidence must remain protected

Add all core tests and summarize decisions, files, state changes, recovery, privacy and security controls, and remaining gaps.

