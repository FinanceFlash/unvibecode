# Testing Guide

Check authoritative records, financial or inventory changes, permissions, external effects, recovery, and audit—not only responses.

## 1. Valid dispute opens against a captured payment

**Given:** A dispute notification references an existing captured or settled payment

**When:** The case-intake path runs

**Expect:** One case is created and bound to the payment, order, payer, and tenant

**Must not happen:** A case opens against a payment that was never captured or does not exist

**Best test levels:** Integration and end-to-end.

## 2. Complete evidence is submitted before the deadline

**Given:** A case has a reason code, required evidence types, and an active deadline

**When:** A complete evidence bundle is submitted before the deadline

**Expect:** The case advances to under-review with the submission recorded

**Must not happen:** Incomplete or wrong evidence is recorded as a complete submission

**Best test levels:** Integration.

## 3. Low-value dispute is auto-accepted by policy

**Given:** A case amount falls below the configured cost-to-fight threshold

**When:** Auto-accept policy evaluates the case

**Expect:** The case is accepted automatically and funds are finalized without a contest attempt

**Must not happen:** The case is contested past the cost-to-fight threshold without approval

**Best test levels:** Unit and integration.

## 4. Authenticated transaction wins on liability shift

**Given:** The disputed payment carries valid strong-customer-authentication evidence

**When:** Liability-shift evaluation runs

**Expect:** The case wins on liability shift and the merchant is not debited

**Must not happen:** Liability shift is ignored and the merchant absorbs an avoidable loss

**Best test levels:** Integration.

## 5. Required dispute fields are missing

**Given:** A dispute notification lacks a payment reference, amount, or reason code

**When:** Case intake validates the notification

**Expect:** Case creation is rejected before any ledger or order effect

**Must not happen:** A guessed or unlinked case is created

**Best test levels:** Unit and API.

## 6. Dispute amount or currency mismatches the payment

**Given:** The dispute amount or currency differs from the original captured payment

**When:** The case is linked to the payment

**Expect:** The mismatch is flagged for manual review before any automated resolution

**Must not happen:** The mismatch is silently reconciled instead of flagged

**Best test levels:** Unit and integration.

## 7. Actor without dispute-team access submits evidence

**Given:** An authenticated actor lacks dispute-team access to the case's tenant

**When:** They attempt to submit or modify evidence

**Expect:** Ownership and scope checks deny the action

**Must not happen:** An unauthorized actor modifies or submits case evidence

**Best test levels:** Authorization and security.

## 8. Evidence deadline is reached at a timezone boundary

**Given:** A submission arrives immediately before, at, and after the evidence deadline across a timezone or network cutover

**When:** Trusted time and the authoritative deadline are checked

**Expect:** One explicit boundary rule is applied consistently

**Must not happen:** Clock differences extend or shorten the window unpredictably

**Best test levels:** Unit with controlled time.

## 9. Two dispute webhooks arrive together for one case

**Given:** Two dispute-opened webhooks for the same network case ID arrive concurrently

**When:** Both are processed

**Expect:** Idempotency allows exactly one case and one provisional debit

**Must not happen:** The provisional debit is applied twice

**Best test levels:** Concurrency integration.

## 10. Provider retries the dispute-opened notification

**Given:** The provider resends a dispute-opened notification already processed

**When:** The retry is received

**Expect:** The existing case is returned without creating another one

**Must not happen:** A duplicate case is created for one chargeback

**Best test levels:** Integration.

## 11. Representment response from the network is lost

**Given:** A representment was submitted but no confirmation was received by the caller

**When:** The submission is retried or status is queried

**Expect:** The original representment is found and reused

**Must not happen:** Resubmission creates a second representment instead of resuming the same case

**Best test levels:** API and integration.

## 12. Case is escalated to pre-arbitration after resolution

**Given:** A resolved case receives a network escalation to pre-arbitration or arbitration

**When:** The escalation notification is processed

**Expect:** The case reopens into the escalation stage with prior resolution preserved as history

**Must not happen:** The case is treated as final and closed prematurely

**Best test levels:** Integration.

## 13. Merchant chargeback ratio crosses the risk threshold

**Given:** Confirmed dispute outcomes push the merchant's chargeback ratio above the configured threshold

**When:** Ratio aggregation runs

**Expect:** The merchant risk-program status updates and the configured escalation fires

**Must not happen:** Risk-program escalation is not triggered

**Best test levels:** Integration.

## 14. Cardholder withdraws the dispute after representment

**Given:** A cardholder withdrawal notification arrives for a case with submitted representment

**When:** The withdrawal is processed

**Expect:** The case closes as withdrawn and provisionally debited funds are reinstated

**Must not happen:** The case stays open or funds are not reinstated

**Best test levels:** Integration.

## 15. Provisional debit succeeds but the ledger write fails

**Given:** The provider applies a provisional debit while the local ledger entry fails to persist

**When:** Recovery runs

**Expect:** The authoritative provider state repairs the same ledger entry without a new debit

**Must not happen:** A second debit is applied blindly on retry

**Best test levels:** Integration.

## 16. Dispute references another tenant's payment

**Given:** A dispute notification's payment reference belongs to a different tenant than the case actor

**When:** Case linkage is attempted

**Expect:** Tenant and payment binding deny the linkage

**Must not happen:** Identifiers cross the tenant boundary into another merchant's case

**Best test levels:** Authorization and security.

## 17. Resolution arrives after the order was already refunded

**Given:** The disputed order was fully refunded before the case resolved

**When:** The case resolution is processed

**Expect:** The resolution is reconciled against the existing refund without moving funds again

**Must not happen:** The ledger reverses the same funds twice

**Best test levels:** Integration and operations.

## 18. Evidence bundle contains cardholder PAN or secrets

**Given:** An evidence bundle or case record contains card-number fragments or personal data

**When:** The bundle is stored, logged, or displayed

**Expect:** Sensitive fields are masked or excluded outside authorized access

**Must not happen:** Sensitive data enters logs or unauthorized storage

**Best test levels:** Security and log inspection.

## 19. Final network outcome arrives after internal tracking expired

**Given:** The internal deadline-tracking record for a case has already expired or archived

**When:** The authoritative final network outcome is received

**Expect:** The case record is reopened or updated to match the authoritative outcome

**Must not happen:** Stale internal state contradicts the authoritative network outcome

**Best test levels:** Integration.

## 20. Case resolves but the order or customer record update fails

**Given:** A case resolves won or lost while the order or customer-facing record update fails

**When:** Reconciliation runs

**Expect:** All systems converge on the same outcome without a contradictory or duplicate ledger effect

**Must not happen:** The ledger, order, and customer outcome show contradictory states

**Best test levels:** Integration and operations.
