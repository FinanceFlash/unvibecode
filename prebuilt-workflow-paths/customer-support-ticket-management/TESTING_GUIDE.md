# Testing Guide

Check authoritative records, state transitions, permissions, external effects, recovery, and audit changes—not only HTTP responses or user-interface messages.

## 1. Valid issue creates one ticket

**Given:** An authorized customer submits complete issue details through a supported channel

**When:** The request is accepted

**Expect:** One ticket is created with the correct requester, tenant, category, and initial SLA

**Must not happen:** The issue disappears or creates multiple tickets

**Best test levels:** API and integration.

## 2. Ticket is acknowledged and assigned

**Given:** A valid new ticket satisfies routing policy

**When:** Triage and assignment run

**Expect:** The customer receives a safe reference and one eligible owner or queue is recorded

**Must not happen:** Acknowledgement exposes internal data or assignment crosses scope

**Best test levels:** Integration and end-to-end.

## 3. Agent resolves and closes correctly

**Given:** An eligible agent has completed investigation and required linked actions

**When:** They record resolution and close under policy

**Expect:** The customer-visible outcome, status, SLA, and audit trail are consistent

**Must not happen:** The ticket closes while promised work remains incomplete

**Best test levels:** Integration.

## 4. Required intake data is missing

**Given:** The request lacks permitted contact, account, subject, or issue details

**When:** Intake validation runs

**Expect:** A useful validation outcome is returned without creating an unusable ticket

**Must not happen:** A blank or unowned ticket enters operations

**Best test levels:** Unit and API.

## 5. Attachment is malformed or unsafe

**Given:** The request contains an excessive, unsupported, corrupt, or malicious file

**When:** Upload and scanning run

**Expect:** The attachment is rejected or quarantined safely

**Must not happen:** Unsafe content is rendered, executed, or exposed to agents

**Best test levels:** File-security and integration.

## 6. Duplicate issue is submitted

**Given:** The same external message or equivalent active issue already exists

**When:** Intake runs again

**Expect:** The request maps, merges, or creates a new ticket only according to explicit policy

**Must not happen:** Duplicate tickets trigger duplicate work or SLA noise

**Best test levels:** Integration.

## 7. Unauthorized person accesses ticket

**Given:** A person lacks requester, tenant, agent, queue, or field permission

**When:** They read, reply, assign, or close

**Expect:** Authorization denies the operation without revealing protected details

**Must not happen:** A ticket identifier grants access

**Best test levels:** Authorization and security.

## 8. Requester identity formats differ

**Given:** Email casing, aliases, external references, or account identifiers vary across channels

**When:** Identity and deduplication checks run

**Expect:** Canonical rules attach the message to the intended customer and ticket

**Must not happen:** A format variation crosses accounts or creates false duplicates

**Best test levels:** Unit and integration.

## 9. Two agents update ownership together

**Given:** Two eligible agents assign, transfer, or resolve the same ticket concurrently

**When:** Both actions execute

**Expect:** One authoritative owner and permitted status transition wins

**Must not happen:** The ticket has conflicting owners or loses a message

**Best test levels:** Concurrency integration.

## 10. SLA action occurs at deadline

**Given:** A reply, resolution, pause, or escalation occurs before, at, and after the SLA boundary

**When:** The system evaluates time

**Expect:** One explicit server-time and pause policy is applied

**Must not happen:** Races hide a breach or escalate completed work

**Best test levels:** Unit with controlled time.

## 11. Ticket-create response is lost

**Given:** The ticket may already exist but the customer received no response

**When:** The client or channel retries

**Expect:** The existing ticket is returned or one ticket is safely created

**Must not happen:** Repeated retries create ticket and message floods

**Best test levels:** API and integration.

## 12. Inbound message is replayed

**Given:** An email, webhook, or chat message identifier already committed

**When:** The same message arrives again

**Expect:** It is deduplicated or returns a safe existing result

**Must not happen:** The message, notification, or linked automation repeats

**Best test levels:** Integration.

## 13. Support intake is flooded

**Given:** One source sends repeated tickets, replies, attachments, or expensive operations

**When:** Abuse limits are reached

**Expect:** Traffic is bounded without losing legitimate recovery paths

**Must not happen:** Queues, provider cost, or agent workload grow without limit

**Best test levels:** Security and load.

## 14. Ticket commits but acknowledgement fails

**Given:** The authoritative ticket exists but customer delivery fails

**When:** Retry or channel fallback runs

**Expect:** One ticket remains and delivery status is visible

**Must not happen:** The ticket is recreated or customer messages multiply

**Best test levels:** Integration.

## 15. External support provider times out

**Given:** Email, chat, CRM, attachment, or identity service returns an uncertain result

**When:** Recovery runs

**Expect:** The outcome is correlated, bounded, and reconciled

**Must not happen:** Uncertainty is treated as safe success or endless retry

**Best test levels:** Provider contract and integration.

## 16. Resolution response is lost

**Given:** The ticket and linked actions may already be resolved

**When:** The agent repeats resolution

**Expect:** Current state returns one clear outcome

**Must not happen:** Closure, notifications, or credits repeat

**Best test levels:** Integration and API.

## 17. Cross-tenant ticket reference is used

**Given:** A valid customer or agent supplies a ticket identifier from another tenant

**When:** They attempt to read or update it

**Expect:** Ownership and tenant checks deny access

**Must not happen:** Identifiers bypass tenant isolation

**Best test levels:** Authorization and security.

## 18. Sensitive message or attachment causes error

**Given:** The ticket contains personal data, access information, or confidential files

**When:** Logging, rendering, export, or notification fails

**Expect:** Errors and audit records avoid unnecessary protected content

**Must not happen:** Secrets, internal notes, or attachments leak

**Best test levels:** Security and log inspection.

## 19. Customer replies after closure

**Given:** A reply arrives at, within, or after the allowed reopen window

**When:** The inbound message is processed

**Expect:** The ticket reopens or a new linked ticket is created by explicit policy

**Must not happen:** The reply is silently discarded or mutates archived work

**Best test levels:** Integration.

## 20. Promised linked action fails

**Given:** The ticket resolution requires a refund, credit, access restoration, or operational correction

**When:** That downstream action fails

**Expect:** The ticket exposes incomplete work and supports safe repair

**Must not happen:** The customer is told the issue is complete or the action repeats

**Best test levels:** Integration and operations.

