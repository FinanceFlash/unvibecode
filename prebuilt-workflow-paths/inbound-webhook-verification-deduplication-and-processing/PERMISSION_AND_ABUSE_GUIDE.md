# Permission and Abuse Guide

## Permission boundaries

- A valid signature proves possession of provider credentials; it does not by itself prove the intended tenant, account, environment, event type, or business authority.
- Endpoint configuration must bind provider account, environment, tenant, accepted event types, schema versions, and active secret versions.
- Support and operations access to raw deliveries, retry controls, quarantine, reconciliation, and redrive must be separately authorized and audited.
- A manual replay must repeat current verification and scope checks or use an explicit trusted internal command with equivalent controls.
- Cross-tenant caches, delivery keys, queues, metrics, support views, and exports must retain tenant and provider scope.

## Abuse paths

| Abuse | Protection |
|---|---|
| Forged request | Raw-body signature verification with constant-time comparison |
| Captured request replay | Timestamp tolerance plus durable delivery identity |
| Cross-tenant routing | Authoritative endpoint, provider-account, environment, and tenant binding |
| Duplicate flood | Storage uniqueness, cheap duplicate responses, and bounded rate limits |
| Payload substitution | Immutable raw-body digest conflict detection |
| Oversized or expensive input | Request-size, decompression, parsing, schema, and time limits |
| Poison-event retry loop | Attempt budget, quarantine, alerting, and authorized redrive |
| Privileged replay misuse | Least privilege, reason capture, approval where required, and audit |
| Secret or payload disclosure | Secret manager, encryption, redaction, access control, and retention limits |

## Review questions

- Can an attacker choose the provider, tenant, environment, event type, or secret lookup key?
- Are signatures verified before body parsing changes the evidence?
- Is the deduplication key scoped so unrelated tenants or providers cannot collide?
- Can support users view or replay more payload data than their role requires?
- Do error responses reveal signature, secret, tenant, event, or existence details?
- Are invalid traffic and duplicate traffic cheaper to handle than valid business processing?

Deny uncertain authenticity, scope, ownership, or operator permission. Preserve enough immutable evidence to investigate conflicts without exposing full payloads broadly.
