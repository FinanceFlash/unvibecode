# Engineering Guide

## Trace the implementation
1. Reset request submission endpoint, email lookup, account state check, and rate-limit enforcement
2. Token generation, entropy source, hashing strategy, storage, and expiry assignment
3. Prior token revocation when a new request is accepted for the same account
4. Email dispatch: queuing, link construction, token embedding, and delivery handoff
5. Token validation endpoint: lookup, hash comparison, expiry check, and single-use flag
6. Password policy enforcement: length, complexity, history, and same-as-current check
7. Credential update: atomic write, password hash replacement, and update timestamp
8. Session invalidation: scope selection, store update, refresh and access token revocation
9. Audit record creation at each stage: request, token issue, validation, credential update, and session invalidation
10. Account enumeration protection: constant-time lookup and uniform response regardless of email existence

## Rules the code should protect
- A reset response must not differ by content or timing based on whether the email exists
- Tokens must be stored as hashes; plaintext tokens must not persist after issue
- A token must transition to consumed in the same transaction as the credential update
- A new reset request must revoke any prior unconsumed token for the same account
- Credential updates must not proceed without passing all password policy checks
- Session invalidation must cover all active sessions, not only the current one
- Partial failure in session invalidation must leave a visible, auditable, and repairable state
- Rate limiting must apply per email address and per source IP independently

## Build or change safely
1. Confirm token expiry window, revocation policy, and session scope with product before implementation
2. Use a cryptographically secure random source for token generation and time-safe comparison for validation
3. Wrap the token consumption and credential update in one atomic write or implement compensating recovery
4. Apply constant-time string comparison to prevent timing-based account enumeration
5. Test rate limiting at the boundary: the first blocked request and the first allowed request after reset
6. Verify session invalidation covers refresh tokens, access tokens, and any persistent device tokens
7. Confirm audit records are written even when the credential update fails
8. Add the core 20 tests before shipping any change to this workflow
