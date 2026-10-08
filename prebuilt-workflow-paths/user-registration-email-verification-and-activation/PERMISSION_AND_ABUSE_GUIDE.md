# Permission and Abuse Guide

## Permission boundaries
- One email address must map to at most one active account
- The password must be hashed before storage and must never appear in logs or responses
- Verification tokens must be cryptographically random, time-bounded, and single-use
- Expired or consumed tokens must not activate an account
- The account must not gain full entitlements until email verification completes
- Rate limits must bound registration, resend, and verification attempts

## Misuse paths
- Duplicate account — Concurrent or replayed registration creates multiple accounts for one email
- Fake or bot account — Automated registrations pollute the user base and consume resources
- Unverified account with full access — The account gains privileges before email ownership is confirmed
- Credential exposure — Plaintext passwords or tokens appear in logs, errors, or responses
- Predictable verification token — An attacker guesses or brute-forces the token to activate arbitrary accounts
- Stale unverified account — Abandoned registrations accumulate personal data without cleanup
- Email delivery failure — The visitor cannot complete verification and the account is permanently stuck
- Unauthorized admin suspension — A valid registration is blocked without proper review or notification

Protect submitted credentials, verification tokens, email addresses, personal data, account status, rate-limit state, and audit records. Deny uncertain ownership or permission.
