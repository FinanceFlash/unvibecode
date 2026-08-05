# Testing Guide

Check authoritative identity, permissions, policy versions, state changes, downstream effects, recovery, and audit—not only responses.

## 1. Eligible request completes erasure

**Given:** A verified data subject has an approved request with known in-scope data

**When:** Deletion executes

**Expect:** Required data is deleted or anonymized and completion evidence is recorded

**Must not happen:** Mandatory stores retain data or another account is affected

**Best test levels:** Integration and end-to-end.

## 2. Lawful hold preserves only required data

**Given:** A valid hold applies to a defined category and purpose

**When:** Scope and deletion run

**Expect:** Only held data remains restricted with basis and expiry

**Must not happen:** The entire account is retained without justification

**Best test levels:** Policy integration.

## 3. Anonymization preserves non-personal record

**Given:** Policy permits irreversible anonymization instead of deletion for a shared or analytical record

**When:** Transformation runs

**Expect:** Personal linkage is irreversibly removed and evidence retained

**Must not happen:** The person can still be reidentified through retained fields

**Best test levels:** Privacy and integration.

## 4. Required request data is missing

**Given:** Requester, account, tenant, contact, authority proof, or scope is absent

**When:** Validation runs

**Expect:** The request remains unverified or requires correction

**Must not happen:** Destructive work starts from guessed identity

**Best test levels:** Unit and API.

## 5. Scope or identifier is malformed

**Given:** Identifiers, aliases, category, date, encoding, or payload size is invalid

**When:** Validation runs

**Expect:** Unsafe input is rejected

**Must not happen:** Malformed scope reaches deletion workers

**Best test levels:** Unit, API, and security.

## 6. Identity verification fails

**Given:** The requester cannot prove control or representative authority

**When:** Approval is attempted

**Expect:** Deletion is denied or paused safely

**Must not happen:** Support pressure or request possession substitutes for proof

**Best test levels:** Security and policy.

## 7. Operator cannot approve or execute

**Given:** The agent lacks privacy, legal, tenant, system, or destructive authority

**When:** They change scope, hold, approve, or run deletion

**Expect:** Authorization denies the action

**Must not happen:** A request id grants destructive control

**Best test levels:** Authorization and security.

## 8. Aliases resolve to one account safely

**Given:** Email, phone, external id, merged identity, or prior username variants exist

**When:** Account discovery runs

**Expect:** Canonical mapping finds only the intended person's records

**Must not happen:** An alias crosses users or leaves hidden in-scope data

**Best test levels:** Integration.

## 9. Duplicate requests execute together

**Given:** Two valid requests or workers target the same account concurrently

**When:** Both run

**Expect:** One coordinated case and idempotent task set produce consistent outcomes

**Must not happen:** Tasks conflict, over-delete, or mark complete early

**Best test levels:** Concurrency integration.

## 10. Hold expires at boundary

**Given:** A retention exception expires immediately before, at, and after task evaluation

**When:** Trusted time is checked

**Expect:** One explicit rule releases or retains the data

**Must not happen:** Clock differences cause unlawful deletion or retention

**Best test levels:** Unit with controlled time.

## 11. Request response is lost

**Given:** The case may already exist but the requester sees failure

**When:** The request is repeated

**Expect:** The same case and status are returned

**Must not happen:** Duplicate destructive workflows begin

**Best test levels:** API and integration.

## 12. Deletion task is replayed

**Given:** A data-item or processor task already completed

**When:** The job repeats

**Expect:** It no-ops or confirms the same outcome

**Must not happen:** Shared data, evidence, or unrelated records are deleted

**Best test levels:** Worker integration.

## 13. Deletion is abused

**Given:** One actor submits repeated requests, aliases, processor calls, or support escalations

**When:** Abuse controls run

**Expect:** Activity is bounded without blocking legitimate rights

**Must not happen:** Operations are exhausted or other accounts are targeted

**Best test levels:** Security and load.

## 14. Restriction commits but jobs fail

**Given:** The account is disabled or marked pending deletion but tasks were not created

**When:** Recovery runs

**Expect:** Tasks are created once or access is restored under explicit denial policy

**Must not happen:** The user is locked out while data remains indefinitely

**Best test levels:** Integration and operations.

## 15. Processor or datastore times out

**Given:** A deletion target returns uncertain status

**When:** Failure handling runs

**Expect:** The task remains unresolved and reconciliation precedes completion

**Must not happen:** Uncertainty is counted as deleted

**Best test levels:** Dependency contract and integration.

## 16. Deletion commits but response is lost

**Given:** A data item or processor may already be deleted

**When:** The worker retries

**Expect:** The same task resolves idempotently

**Must not happen:** Retries delete broader or unrelated data

**Best test levels:** Integration.

## 17. Cross-tenant record is discovered

**Given:** Inventory links an identifier to another tenant or person

**When:** Deletion evaluates it

**Expect:** Ownership and shared-record policy prevent unsafe removal

**Must not happen:** Identifier matching deletes another customer's data

**Best test levels:** Authorization and privacy.

## 18. Deletion failure is logged

**Given:** The path contains identity proof, data inventory, retained records, and processor responses

**When:** An error occurs

**Expect:** Diagnostics avoid sensitive content and reusable identity proof

**Must not happen:** Personal data or evidence enters unsafe logs

**Best test levels:** Security and log inspection.

## 19. Late data arrives after completion

**Given:** A delayed event, sync, restore, or cache repopulation recreates an identifier

**When:** Reappearance controls run

**Expect:** The data is suppressed, re-erased, or reviewed by policy

**Must not happen:** Deleted personal data silently becomes active again

**Best test levels:** Integration.

## 20. One mandatory system fails

**Given:** Most stores delete but a database, file, index, backup policy, or processor remains unresolved

**When:** Completion is evaluated

**Expect:** The request remains partial and repair continues

**Must not happen:** The customer receives false completion

**Best test levels:** Integration and operations.

