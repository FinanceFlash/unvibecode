---
name: understand-user-registration-code
description: Trace and explain User Registration, Email Verification, and Account Activation across an existing codebase. Use when locating entry points, authorization, state, external calls, business effects, retries, recovery, monitoring, and tests.
---

# Understand User Registration, Email Verification, and Account Activation Code

Trace:
1. Registration form submission, API endpoint, invite-link entry, and admin-creation entry points
2. Input validation for email format, normalization, domain policy, and uniqueness checks
3. Password strength validation, hashing, salting, and credential storage
4. Account record creation, identifier generation, status initialization, and transaction controls
5. Verification token generation, expiry assignment, storage, and single-use enforcement
6. Email composition, delivery dispatch, delivery tracking, and failure handling
7. Token validation endpoint, expiry check, consumption, and account activation
8. Initial entitlement grant, role assignment, tenant binding, and welcome notification
9. Rate limiting, CAPTCHA, bot detection, and abuse throttling at registration and verification
10. Audit logging, privacy controls, monitoring, reconciliation, and cleanup of expired registrations

Explain actors, ownership, credentials, states, transitions, effects, failures, retries, security boundaries, monitoring, tests, and areas needing verification. Cite files and symbols.
