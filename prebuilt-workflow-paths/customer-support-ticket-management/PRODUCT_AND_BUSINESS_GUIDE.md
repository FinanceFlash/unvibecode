# Product and Business Guide

## Boundary
Starts when a customer issue enters an approved support channel. Ends when the issue is rejected, merged, resolved and closed, or reopened with ownership, SLA, customer communication, and promised business actions kept consistent.

## People and systems
- Customer or authorized requester
- Support agent
- Triage or routing automation
- Supervisor or escalation owner
- Product, billing, or operations specialist
- Notification and external support providers
- Security, privacy, and audit operations

## Things created or changed
- Ticket and external reference
- Requester identity and account or tenant
- Message, internal note, and attachment
- Category, priority, severity, queue, and owner
- SLA clocks, pause reason, escalation, and reminders
- Resolution, closure reason, linked action, and satisfaction outcome
- Notification and audit record

## Stages
- Ticket: received → validated → triaged → assigned → in progress → waiting → resolved → closed or reopened
- Ownership: unassigned → assigned → transferred, returned, or escalated
- SLA: running → paused by policy → resumed → met or breached
- Linked action: absent → requested → completed, denied, or failed

## Product decisions
- Eligible support channels and requester-verification requirements
- Required ticket fields, attachment types, size, retention, and malware policy
- Duplicate and merge policy
- Priority, severity, queue, language, product, and tenant routing
- Assignment, transfer, workload, absence, and escalation rules
- SLA start, pause, resume, breach, and notification rules
- Customer-visible message versus internal-note policy
- Resolution evidence, customer confirmation, auto-close, and reopen window
- Which refunds, credits, access changes, or other actions require separate approval
- Privacy, redaction, deletion, audit, and misuse policy

## Happy paths
- A valid customer issue becomes one acknowledged and correctly routed ticket
- An eligible agent owns, investigates, communicates, and resolves the issue
- A closed issue reopens within policy when the customer provides relevant new information

## Negative paths
- Required requester, account, contact, or issue details are missing or invalid
- Attachments are unsafe, unsupported, or excessive
- An unauthorized person attempts to view or update a ticket
- A duplicate, spam, or out-of-scope request is safely merged or rejected

## Edge cases
- Two agents assign or update the ticket together
- A customer reply arrives exactly as the ticket auto-closes
- A reply arrives after closure or after the reopen window
- Tenant, customer, priority, or owner changes while work is active
- A linked refund or account correction succeeds while the support response is lost

## Acceptance criteria
1. One eligible issue must create or map to one authoritative ticket
2. Only authorized customers and support roles may view or change permitted ticket fields
3. Customer-visible messages and internal notes must never be confused
4. Priority, routing, assignment, SLA, and escalation must follow current policy
5. Simultaneous assignment and status changes must preserve one authoritative owner and state
6. Resolution and closure must have the required evidence and customer outcome
7. Late messages must follow explicit reopen or new-ticket policy
8. Linked refunds, credits, and account actions must not repeat
9. Partial failures must remain visible, retriable, and reconcilable
10. Personal data, attachments, access details, and internal notes must remain protected

## Business risks
| Risk | Business consequence |
|---|---|
| Lost customer issue | A valid request is accepted externally but no actionable ticket exists |
| Unauthorized ticket access | Another customer, tenant, or agent sees or changes protected support data |
| Internal-note exposure | Private investigation content is sent to the customer |
| Incorrect routing or priority | Critical issues wait in the wrong queue or low-risk issues consume emergency capacity |
| False resolution | A ticket closes while the customer problem or promised action remains incomplete |
| SLA failure | Deadlines pause incorrectly or escalation never occurs |
| Duplicate business action | Retries repeat refunds, credits, notifications, or account changes |
| Sensitive-data exposure | Messages, attachments, credentials, or personal data reach unsafe logs or recipients |

