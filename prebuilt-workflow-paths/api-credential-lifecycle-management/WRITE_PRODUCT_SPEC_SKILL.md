---
name: write-api-credential-lifecycle-spec
description: Write or review a product specification for API Credential Lifecycle Management. Use when defining credential owners, lifecycle states, permissions, scope, rotation, expiry, revocation, recovery, audit, edge cases, or business risks.
---

# Write an API Credential Lifecycle Specification

Use application-native terms. Decide:
- Who may create, rotate, revoke, or recover a credential and what authorization is required
- Which owners, applications, services, environments, and tenants a credential may be assigned to
- Which permission scopes are allowed and how excessive scope is rejected
- Which credential lifecycle states exist and what transitions are permitted
- When credentials become active and when they expire
- Whether old and replacement credentials may overlap during rotation and when the old credential must be invalidated
- How emergency revocation works for compromised credentials
- How duplicate requests, concurrent operations, lost responses, and partial lifecycle operations are handled
- Which lifecycle actions require audit evidence and what sensitive information must never be exposed
- How dependency failures, inconsistent states, retries, reconciliation, and recovery are handled
- How protected API access responds to active, expired, revoked, or otherwise invalid credentials

Write scope, actors, objects, states, lifecycle paths, user and business outcomes, permissions, recovery, security, misuse, acceptance criteria, and unanswered decisions.