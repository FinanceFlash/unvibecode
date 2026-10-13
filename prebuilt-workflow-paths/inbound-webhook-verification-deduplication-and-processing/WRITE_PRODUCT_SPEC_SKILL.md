---
name: write-inbound-webhook-spec
description: Write or review a product specification for Inbound Webhook Verification, Deduplication, and Processing. Use when defining provider trust, endpoint scope, delivery identity, acknowledgement, processing, retry, recovery, privacy, and operational policy.
---

# Write an Inbound Webhook Specification

Use application and provider terms. Decide:

- start event, authoritative end outcomes, included scope, and excluded adjacent workflows
- provider account, environment, endpoint, tenant, accepted events, schema versions, and configuration ownership
- raw-body and header requirements, signature algorithm, timestamp tolerance, replay policy, and secret rotation
- delivery and event identity, deduplication scope, payload digest conflict behavior, and ordering policy
- acknowledgement meaning, durable inbox, queue handoff, processing stages, timeouts, leases, and concurrency
- domain-effect idempotency, unknown outcomes, partial failure, retries, backoff, quarantine, reconciliation, and redrive
- size, rate, retention, privacy, logging, audit, metrics, alerts, operator permissions, and support procedures

Produce a specification with `People and systems`, `Things created or changed`, `Stages`, normal and denied paths, product decisions, acceptance criteria, business consequences, and unresolved questions. Keep provider contract facts separate from application policy assumptions.
