# Product and Business Guide

## Boundary
Starts when a person or authorized representative submits a deletion request. Ends when identity and scope are verified and the request is denied, paused by a lawful hold, completed through deletion or approved anonymization, or remains explicitly incomplete with evidence and repair work recorded.

## People and systems
- Data subject or authorized representative
- Privacy request and identity-verification service
- Account, tenant, and data-owner services
- Privacy, legal, compliance, security, and support reviewers
- Application databases, files, logs, indexes, analytics, backups, and derived-data systems
- Third-party processors and deletion providers
- Operations, audit, and incident-response teams

## Things created or changed
- Erasure request, requester, authority proof, account, tenant, and case
- Identity-verification result and contact channel
- Data inventory, system owner, record category, purpose, and location
- Legal hold, retention rule, exception, decision, reason, and expiry
- Deletion or anonymization task, batch, item result, checkpoint, and retry
- Account status, credentials, sessions, entitlements, and identifiers
- Processor instruction, acknowledgement, completion evidence, and audit record

## Stages
- Request: received → identity pending → scoped → under review → approved, denied, held, executing, completed, partial, or cancelled
- Account: active → restricted or pending deletion → deleted, anonymized, retained by exception, or restored after denial
- Data item: discovered → eligible → deleted, anonymized, retained, missing, failed, or awaiting processor
- Processor task: pending → submitted → acknowledged, completed, failed, or uncertain

## Product decisions
- Who may request deletion and what identity or representative proof is required
- How accounts, aliases, tenants, devices, and related identities are resolved
- Which systems, data categories, derived data, and processors are in scope
- Which legal hold, tax, fraud, safety, contract, dispute, or retention exceptions apply
- Delete versus irreversible anonymization for each category
- When account access, sessions, credentials, billing, and entitlements are restricted
- How shared, multi-user, public, transactional, audit, and security records are handled
- Backup, archive, replica, cache, search, analytics, and model-derived data policy
- Completion deadline, extension, notification, appeal, cancellation, and support policy
- Deletion proof, reappearance prevention, retry, monitoring, privacy, and audit policy

## Happy paths
- A verified eligible request deletes or anonymizes all in-scope data and closes with evidence
- A lawful retention exception preserves only required data with restricted purpose and recorded expiry
- Third-party processors acknowledge and complete their required deletion tasks

## Negative paths
- Requester, account, identity proof, authority, or scope is missing or invalid
- Identity verification fails or representative authority is insufficient
- A lawful hold or retention obligation blocks some or all deletion
- The request targets another account, tenant, shared record, or out-of-scope data

## Edge cases
- Two deletion requests or account actions execute together
- Retention or legal hold expires exactly during deletion
- New data, messages, events, or backups appear after inventory snapshot
- A processor deletes data but acknowledgement is lost
- Account deletion overlaps payment, dispute, security investigation, or recovery

## Acceptance criteria
1. Only a verified data subject or authorized representative may control the request
2. Requester, account, tenant, aliases, scope, decision, and request version must remain bound
3. Every in-scope system and processor must have an explicit delete, anonymize, retain, or not-found outcome
4. Retention exceptions must record legal basis, restricted purpose, scope, and expiry
5. Deletion must not remove another person's, tenant's, shared, or legally required data
6. Completed status must not be issued while required tasks remain failed or uncertain
7. Repeated or concurrent work must not recreate, misassign, or inconsistently delete data
8. New and restored data must not silently reappear after completion
9. Identity proof, data inventory, retained records, processor responses, and completion evidence must remain protected
10. Deadline, progress, exceptions, per-system results, repair, and audit must remain observable

## Business risks
| Risk | Business consequence |
|---|---|
| Wrong-person deletion | Weak identity or account resolution destroys another customer's data |
| Incomplete erasure | Hidden stores, processors, indexes, backups, or derived data retain personal information |
| Unlawful deletion | Required tax, fraud, dispute, safety, or legal-hold evidence is removed |
| Excess retention | Exceptions preserve more data or purpose than permitted |
| Data reappearance | Late events, restores, caches, or resynchronization recreate deleted records |
| Account inconsistency | Credentials, sessions, billing, entitlement, and profile state disagree |
| Cross-tenant deletion | Shared identifiers or jobs remove another customer's records |
| Sensitive-data exposure | Identity proof, inventory, retained data, or deletion evidence reaches unsafe logs |

