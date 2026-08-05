---
name: understand-support-ticket-code
description: Trace and explain Customer Support Ticket Lifecycle across an existing codebase. Use when locating entry points, authorization, state, storage, external effects, retries, recovery, monitoring, and tests.
---

# Understand Support Ticket Lifecycle Code

Trace:
1. Ticket-create, email/chat import, reply, attachment, assign, transfer, escalate, resolve, close, reopen, merge, and support entry points
2. Requester authentication, account and tenant ownership, agent role, queue, and field-level permission checks
3. Validation, attachment handling, malware checks, deduplication, classification, priority, and routing
4. Ticket, message, internal-note, owner, status, SLA, and version models
5. Concurrency controls for assignment, replies, merges, resolution, and reopening
6. Notification, email threading, provider callbacks, retry, and delivery state
7. Linked refund, credit, access, or operational actions and their idempotency
8. Audit, privacy, redaction, retention, monitoring, support tools, and tests

Explain actors, ownership, states, transitions, effects, failures, retries, security boundaries, monitoring, tests, and areas needing verification. Cite files and symbols.

