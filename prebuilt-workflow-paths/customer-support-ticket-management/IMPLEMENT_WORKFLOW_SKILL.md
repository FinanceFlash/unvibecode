---
name: implement-support-ticket
description: Implement or modify Customer Support Ticket Lifecycle. Use when adding or changing validation, authorization, state transitions, external effects, retries, recovery, privacy controls, monitoring, or tests.
---

# Implement Support Ticket Lifecycle

Confirm:
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

Follow project conventions and protect:
- One eligible issue must resolve to one authoritative ticket or explicit rejection
- Ticket access must enforce requester, account, tenant, agent, queue, and field visibility
- Internal notes must never appear as customer-visible messages
- One authoritative owner and status must survive simultaneous actions
- SLA calculations must use trusted time and explicit pause reasons
- Resolution and closure must not claim unfinished linked actions as complete
- Retries and replays must not duplicate tickets, messages, or business actions
- Messages, attachments, personal data, and credentials must remain protected

Add all core tests and summarize decisions, files, state changes, recovery, privacy and security controls, and remaining gaps.

