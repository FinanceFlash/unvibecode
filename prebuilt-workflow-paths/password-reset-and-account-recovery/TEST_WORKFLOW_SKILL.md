---
name: "Test Password Reset and Account Recovery"
description: "Designs or reviews the complete test set for the password reset and account recovery workflow, covering the 20 core scenarios across unit, integration, concurrency, security, timing, and recovery test levels."
---

# Test Workflow — Password Reset and Account Recovery

You are designing or reviewing the test set for the password reset and account recovery workflow.

## Your task

Using the connected code context and the 20 core scenarios, produce or evaluate tests that verify each scenario. Require specific route, function, fixture, and assertion details. Do not describe a test as passing unless the assertion is stated.

## Test coverage required

**Happy path tests**
- Valid reset request for a registered email issues a token and dispatches an email
- Valid token submitted within expiry updates the credential, consumes the token, and invalidates all sessions
- Admin-triggered forced reset prevents authentication until the reset is completed

**Negative and boundary tests**
- Expired token is rejected and credential is unchanged
- Consumed token replay is rejected
- Non-compliant password is rejected and credential is unchanged
- Password identical to current credential is rejected when policy prohibits reuse
- Reset request for a locked or suspended account is rejected without issuing a token

**Concurrency tests**
- Two simultaneous reset requests for the same account produce only one valid token
- Concurrent credential update and session refresh with the old credential: the refresh fails after the update commits

**Security and timing tests**
- Response body and status code are identical for registered and unregistered email addresses
- Response time difference between registered and unregistered addresses is within the acceptable threshold
- Tampered or invalid token format is rejected before any store lookup
- Cross-account token submission is rejected

**Recovery tests**
- Session invalidation retry after a lost response is idempotent and does not update the credential again
- Token issued but email not delivered: new reset request revokes the prior token and issues a new one

**Audit tests**
- Audit record is written for request, token issue, validation attempt, credential update, and session invalidation outcome
- No plaintext token, new password, or old password hash appears in any audit or log entry

## For each test, state
- The scenario number from CORE_20_SCENARIOS.md
- The test level: unit, integration, concurrency, security, timing, or recovery
- The fixture or setup required
- The action performed
- The exact assertion that must pass
- What must not appear in the result
