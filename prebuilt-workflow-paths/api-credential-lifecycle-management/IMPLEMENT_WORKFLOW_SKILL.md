---
name: implement-api-credential-lifecycle
description: Implement or modify API Credential Lifecycle Management. Use when adding or changing credential validation, authorization, scope, lifecycle state, activation, expiry, rotation, revocation, external effects, retries, recovery, audit, security controls, monitoring, or tests.
---

# Implement API Credential Lifecycle

Confirm:
- Who may create, rotate, revoke, or recover a credential and what authorization is required
- Which owners, applications, services, environments, and tenants a credential may be assigned to
- Which permission scopes are allowed and how excessive scope is rejected
- Which credential lifecycle states exist and which transitions are permitted
- When credentials become active and when they expire
- Whether old and replacement credentials may overlap during rotation and when the old credential must be invalidated
- How emergency revocation works for compromised credentials
- How duplicate requests, concurrent operations, lost responses, and partial lifecycle operations are handled
- Which credential-generation, activation, API, audit, and other dependencies are in scope
- What lifecycle evidence must be recorded and what credential secrets or sensitive information must never be exposed

Follow project conventions and protect:
- Only an authorized actor or service may create, rotate, or revoke a credential
- Credential ownership, assignment, environment, scope, and lifecycle state must remain bound to the intended target
- Credentials must not become usable before required authorization and activation checks complete
- Credentials must not receive permissions beyond their approved scope
- Expired and revoked credentials must not authorize protected API access
- Completed rotation must leave the previous credential invalidated according to the defined rotation policy
- Temporary credential overlap must remain bounded and must not become an unintended permanent state
- Retries, replays, concurrent operations, and lost responses must not create duplicate or contradictory credential states
- Partial lifecycle operations must remain identifiable and recoverable rather than being reported as completed
- Credential secrets, privileged lifecycle data, and audit evidence must remain protected

Add or update all relevant core tests and summarize decisions, files, lifecycle state changes, recovery, audit and security controls, and remaining gaps.