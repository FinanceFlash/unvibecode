# Product and Business Guide

## Boundary
Starts when a prospective seller or service provider begins an application. Ends when the application is rejected, withdrawn, awaiting information, approved but pending activation, activated with the correct marketplace scope, suspended, or explicitly requires review.

## People and systems
- Applicant, business owner, or authorized representative
- Marketplace onboarding service
- Operations, risk, compliance, or category reviewer
- Identity, business, licence, tax, or background-check provider
- Payout and bank-account provider
- Seller account, listing, entitlement, and notification services
- Support, security, privacy, and audit teams

## Things created or changed
- Provider application and version
- Applicant, beneficial owner, representative, and business entity
- Category, service, territory, location, capacity, and marketplace scope
- Identity, company, tax, licence, insurance, certification, and policy evidence
- Verification result, risk flags, review task, decision, and reason
- Payout account reference and readiness
- Seller account, membership, role, entitlement, status, and audit record

## Stages
- Application: draft → submitted → validating → under review → information required → approved, rejected, withdrawn, expired, or suspended
- Verification: not started → pending → passed, failed, inconclusive, or expired
- Seller account: absent → provisioned inactive → active, restricted, suspended, or closed
- Payout readiness: incomplete → verified, pending, failed, or blocked

## Product decisions
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

## Happy paths
- A valid eligible provider passes required checks and receives one correctly scoped active account
- A reviewer requests missing information and the applicant resubmits a new reviewable version
- An ineligible or failed application is rejected with the allowed reason and no supply access

## Negative paths
- Required applicant, business, category, evidence, or payout data is missing or invalid
- The provider, territory, category, licence, or owner is ineligible
- The actor cannot submit or change the application
- Evidence is expired, forged, mismatched, reused, or belongs elsewhere

## Edge cases
- Two reviewers approve and reject together
- Evidence expires exactly during decision or activation
- Applicant changes ownership, bank, category, or territory after verification
- Verification provider succeeds but the response is lost
- Approval overlaps withdrawal, suspension, duplicate resolution, or support action

## Acceptance criteria
1. Only an authorized representative may create or modify the intended application
2. Applicant, owners, business, tenant, category, territory, evidence, and application version must remain bound
3. Required eligibility and verification policy must pass before activation
4. Material data changes must invalidate or retain checks only by explicit policy
5. One real provider must not receive conflicting duplicate supply accounts
6. Only eligible reviewers may decide within category, region, tenant, and authority scope
7. Approval, activation, role, listing entitlement, payout readiness, and notifications must converge
8. Repeated, simultaneous, or lost-response actions must produce one authoritative outcome
9. Expired, withdrawn, rejected, suspended, or superseded evidence cannot activate supply
10. Identity documents, ownership data, bank references, and review evidence must remain protected

## Business risks
| Risk | Business consequence |
|---|---|
| Fake or ineligible provider | Fraudulent supply reaches customers and damages trust or safety |
| Premature activation | Listing or order access is granted before required checks complete |
| Duplicate seller identity | One provider evades history, limits, suspension, or fee obligations |
| Reviewer or exception bypass | Unauthorized approval defeats marketplace policy |
| Incorrect scope | Provider receives the wrong category, territory, role, or listing entitlement |
| Expired evidence | Licences, insurance, tax, or identity proof remains trusted after validity ends |
| Payout or account mismatch | Revenue routes to an account not bound to the approved provider |
| Sensitive-data exposure | Identity, ownership, bank, tax, or review evidence reaches unsafe audiences or logs |

