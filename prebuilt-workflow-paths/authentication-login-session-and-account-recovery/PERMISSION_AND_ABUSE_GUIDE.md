# Permission and Abuse Guide

## Authorization boundaries

- Only the account owner or an explicitly authorized recovery process may change authentication credentials.
- Support tools must not bypass the normal proof requirements without a separately defined, audited policy.
- Session revocation must be limited to sessions the actor is permitted to revoke.

## Abuse cases

- Credential stuffing
- Password guessing
- MFA brute force
- Recovery-token guessing
- Recovery-token replay
- Account enumeration
- Session theft/reuse
- Refresh-token replay
- Login CSRF/session fixation
- Notification abuse

## Controls

- Rate-limit authentication and recovery attempts.
- Use sufficiently random, short-lived one-time tokens.
- Avoid putting secrets in URLs when safer alternatives exist.
- Do not return different account-existence signals unless intentionally required.
- Record security events without raw secrets.
- Require recent authentication or step-up for sensitive security changes.
- Revoke sessions after high-risk credential changes according to policy.
