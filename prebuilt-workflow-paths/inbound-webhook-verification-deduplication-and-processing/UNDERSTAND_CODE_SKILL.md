---
name: understand-inbound-webhook-code
description: Trace and explain Inbound Webhook Verification, Deduplication, and Processing across an existing codebase. Use when locating endpoints, provider proof, tenant binding, inbox state, effects, retries, recovery, privacy controls, and tests.
---

# Understand Inbound Webhook Code

Trace in this order:

1. Public webhook routes, proxy rewrites, provider adapters, and replay entry points
2. Endpoint, provider account, environment, tenant, event type, schema, and secret resolution
3. Raw-body acquisition, limits, signature comparison, timestamp checks, replay checks, and parsing
4. Delivery identity, payload digest, inbox transaction, uniqueness constraint, acknowledgement, and queue handoff
5. Event routing, ordering, worker lease, business command, external effect, idempotency, and completion state
6. Failure classification, retry, backoff, dead letter or quarantine, reconciliation, redrive, and support permissions
7. Payload storage, redaction, encryption, retention, metrics, alerts, audit, and tests

Explain actors, authoritative identities, states, transaction boundaries, side effects, failures, security and privacy boundaries, operational controls, and gaps. Cite files and symbols for every implementation claim and distinguish verified behavior from provider documentation or inference.
