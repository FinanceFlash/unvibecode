---
name: "Implement Password Reset and Account Recovery"
description: "Guides the implementation or modification of the password reset and account recovery workflow while preserving token safety, single-use enforcement, session invalidation, enumeration protection, rate limiting, and audit completeness."
---

# Implement Workflow — Password Reset and Account Recovery

You are implementing or modifying the password reset and account recovery workflow.

## Your task

Using the connected code context and any available specification, implement the change described while preserving all existing safeguards. Require file and symbol evidence for every conclusion about what the current code does.

## Implementation sequence

**1. Reset request handler**
Implement account lookup using constant-time or uniform-delay logic to prevent timing-based enumeration. Apply rate limiting before the account lookup to avoid leaking account existence through rate-limit bypass. Return an identical response regardless of whether the account exists.

**2. Token generation**
Use a cryptographically secure random source with at least 128 bits of entropy. Store only the hash of the token. Assign an expiry timestamp at generation. Revoke any prior unconsumed token for the same account before inserting the new one.

**3. Email dispatch**
Construct the reset link using a path that does not embed the email address. Queue the email after the token is stored. Handle delivery failure without exposing token details in error logs.

**4. Token validation**
Use constant-time comparison when matching the submitted token against the stored hash. Enforce expiry before checking validity. Consume the token in the same transaction as the credential write, not before.

**5. Password policy enforcement**
Validate length, complexity, and history requirements before attempting the credential write. Reject passwords identical to the current credential if policy requires it. Return a specific policy violation message without revealing the current credential.

**6. Credential update**
Write the new password hash in a transaction that includes token consumption. Do not commit the credential update if policy validation has not passed.

**7. Session invalidation**
Invalidate all active sessions, refresh tokens, and access tokens after the credential update is committed. Log any invalidation failure as a recoverable, auditable state. Do not block the credential update on session invalidation failure.

**8. Audit record**
Write an audit record at each stage: request received, token issued, validation attempted, credential updated, session invalidation outcome, and notification dispatched. Do not include the plaintext token, new password, or old password hash in any log entry.

## Safety checks before shipping
- Verify that the response body and processing time are identical for registered and unregistered emails
- Verify that a consumed token cannot be replayed
- Verify that an expired token is rejected
- Verify that session invalidation is called after every successful credential update
- Confirm that all 20 core scenarios have a corresponding test
