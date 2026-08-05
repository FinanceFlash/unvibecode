# Engineering Guide

## Trace the implementation
1. Ticket-create, email/chat import, reply, attachment, assign, transfer, escalate, resolve, close, reopen, merge, and support entry points
2. Requester authentication, account and tenant ownership, agent role, queue, and field-level permission checks
3. Validation, attachment handling, malware checks, deduplication, classification, priority, and routing
4. Ticket, message, internal-note, owner, status, SLA, and version models
5. Concurrency controls for assignment, replies, merges, resolution, and reopening
6. Notification, email threading, provider callbacks, retry, and delivery state
7. Linked refund, credit, access, or operational actions and their idempotency
8. Audit, privacy, redaction, retention, monitoring, support tools, and tests

## Rules the code should protect
- One eligible issue must resolve to one authoritative ticket or explicit rejection
- Ticket access must enforce requester, account, tenant, agent, queue, and field visibility
- Internal notes must never appear as customer-visible messages
- One authoritative owner and status must survive simultaneous actions
- SLA calculations must use trusted time and explicit pause reasons
- Resolution and closure must not claim unfinished linked actions as complete
- Retries and replays must not duplicate tickets, messages, or business actions
- Messages, attachments, personal data, and credentials must remain protected

## Build or change safely
1. Confirm the product decisions before relying on framework or provider defaults.
2. Follow existing authorization, state, storage, logging, monitoring, and test conventions.
3. Bind every action to the authoritative actor, object, version, state, and scope.
4. Enforce permission, current-state, uniqueness, ordering, and time rules at the write.
5. Make retries and replays safe after partial failure and lost responses.
6. Keep downstream inconsistency visible and repairable.
7. Add the core 20 tests.

