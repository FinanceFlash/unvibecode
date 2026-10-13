# Engineering Guide

## Trace the implementation
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

## Rules the code should protect
- One email address must create at most one active account
- The password must be hashed before storage and must never appear in logs or responses
- Verification tokens must be cryptographically random, time-bounded, and single-use
- Expired or consumed tokens must not activate an account
- The account must not gain full entitlements until email verification completes
- Concurrent registrations with the same email must not create duplicate accounts
- Rate limits must bound registration, resend, and verification attempts
- Personal data must follow retention and privacy policy from the moment of collection

## Build or change safely
1. Confirm product decisions on required fields, password policy, token lifetime, and verification limits before relying on defaults.
2. Follow existing credential storage, hashing, logging, monitoring, and test conventions.
3. Bind every registration action to the authoritative email, account, token, and scope.
4. Enforce uniqueness, current-state, ordering, and time rules at the write.
5. Make retries and replays safe after partial failure and lost responses.
6. Keep credential, token, and personal-data inconsistency visible and repairable.
7. Add the core 20 tests.
