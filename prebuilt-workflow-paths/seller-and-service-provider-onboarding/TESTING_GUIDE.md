# Testing Guide

Check authoritative records, eligibility or financial changes, permissions, external effects, recovery, and audit—not only responses.

## 1. Eligible provider becomes active

**Given:** An authorized applicant submits complete valid data and passes required checks

**When:** Approval and activation run

**Expect:** One correctly scoped seller account becomes active

**Must not happen:** Supply access is duplicated or granted before checks complete

**Best test levels:** Integration and end-to-end.

## 2. Information request is resubmitted

**Given:** A reviewer requests specific missing evidence from a pending application

**When:** The applicant supplies a new version

**Expect:** The new version returns to review with prior history preserved

**Must not happen:** Edits silently alter the already reviewed version

**Best test levels:** Integration.

## 3. Ineligible application is rejected

**Given:** Policy or verified evidence establishes a valid rejection reason

**When:** An eligible reviewer decides

**Expect:** The application closes or enters appeal policy without supply access

**Must not happen:** Seller entitlement is provisioned despite rejection

**Best test levels:** Policy integration.

## 4. Required application data is missing

**Given:** Applicant, representative, business, owner, category, territory, or evidence is absent

**When:** Submission validation runs

**Expect:** The application remains draft or requires correction

**Must not happen:** An incomplete application reaches approval

**Best test levels:** Unit and API.

## 5. Evidence is malformed or unsafe

**Given:** A document is corrupt, excessive, malicious, unreadable, or has invalid metadata

**When:** Upload and verification run

**Expect:** It is rejected or quarantined safely

**Must not happen:** Unsafe content is rendered or treated as verified

**Best test levels:** File-security and integration.

## 6. Provider is ineligible

**Given:** The category, territory, owner, age, business type, licence, or policy status is disallowed

**When:** Eligibility runs

**Expect:** The application is rejected or routed to an explicit exception

**Must not happen:** Ineligible supply is activated

**Best test levels:** Policy integration.

## 7. Actor cannot change application

**Given:** The person lacks representative, owner, reviewer, or tenant permission

**When:** They submit, edit, approve, or activate

**Expect:** Authorization denies the action

**Must not happen:** An application identifier grants control

**Best test levels:** Authorization and security.

## 8. Duplicate identity is detected

**Given:** Applicant, owner, business, tax, bank, or provider identity matches an existing record

**When:** Resolution runs

**Expect:** Explicit match, merge, link, reject, or review policy applies

**Must not happen:** Unrelated providers merge or a suspended seller evades history

**Best test levels:** Integration and security.

## 9. Approve and reject arrive together

**Given:** Two eligible reviewers decide the same version concurrently

**When:** Both actions execute

**Expect:** One authoritative decision follows policy

**Must not happen:** The application becomes both approved and rejected

**Best test levels:** Concurrency integration.

## 10. Evidence expires at decision boundary

**Given:** Required proof is valid immediately before, at, and after expiry

**When:** Decision or activation runs

**Expect:** One trusted-time boundary rule is applied

**Must not happen:** Expired evidence activates supply through race or clock differences

**Best test levels:** Unit with controlled time.

## 11. Submission response is lost

**Given:** The application may already be submitted

**When:** The applicant retries

**Expect:** The same application version and status are returned

**Must not happen:** Duplicate applications and checks are created

**Best test levels:** API and integration.

## 12. Verification callback is replayed

**Given:** A provider result or review decision already committed

**When:** The event repeats

**Expect:** It maps to the existing outcome or is rejected

**Must not happen:** Verification, approval, or activation repeats

**Best test levels:** Integration.

## 13. Applications are flooded or forged

**Given:** One source creates repeated applicants, documents, checks, or support escalations

**When:** Fraud and rate controls run

**Expect:** Activity and provider cost remain bounded

**Must not happen:** Fake supply overwhelms reviewers or bypasses limits

**Best test levels:** Security and load.

## 14. Application commits but verification fails

**Given:** The submitted version exists but a required provider request cannot be created

**When:** Recovery runs

**Expect:** The application remains visibly pending or retriable

**Must not happen:** It is silently approved or permanently stranded

**Best test levels:** Integration.

## 15. Verification provider times out

**Given:** Identity, company, tax, licence, background, or bank check is uncertain

**When:** Failure handling runs

**Expect:** The check remains pending or inconclusive until reconciled

**Must not happen:** Uncertainty becomes verified or triggers blind duplicate checks

**Best test levels:** Provider contract and integration.

## 16. Approval commits but response is lost

**Given:** Decision and provisioning may already have run

**When:** The reviewer or worker repeats

**Expect:** Current state returns one approval and seller account

**Must not happen:** Roles or accounts duplicate

**Best test levels:** Integration.

## 17. Cross-tenant application is referenced

**Given:** A valid reviewer or applicant supplies another tenant's application or business

**When:** They view or modify it

**Expect:** Ownership and reviewer scope deny access

**Must not happen:** Identifiers cross marketplace boundaries

**Best test levels:** Authorization and security.

## 18. Sensitive evidence causes an error

**Given:** The path contains identity, owner, bank, tax, address, and review data

**When:** Logging, rendering, export, or notification fails

**Expect:** Diagnostics avoid reusable proof and unnecessary personal data

**Must not happen:** Documents or sensitive review notes leak

**Best test levels:** Security and log inspection.

## 19. Stale approval follows withdrawal

**Given:** The applicant withdrew or a newer version, suspension, or duplicate decision became authoritative

**When:** A delayed approval arrives

**Expect:** Current state blocks activation

**Must not happen:** Old evidence unexpectedly activates supply

**Best test levels:** Integration.

## 20. Approved account provisioning fails

**Given:** The decision is approved but seller account, role, listing scope, payout readiness, or notification fails

**When:** Repair runs

**Expect:** Missing effects complete once or activation remains restricted visibly

**Must not happen:** Provider appears active without required controls

**Best test levels:** Integration and operations.

