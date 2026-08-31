# Permission and Abuse Guide

## Authorization boundaries
- Only the account holder who receives the reset email link may complete the credential update
- A reset token is bound to one account and must not validate against any other account
- Admin-triggered forced resets require an authenticated admin role with an explicit permission to initiate resets for other accounts
- The reset endpoint must not accept authentication credentials as a substitute for a valid token

## Misuse paths

### Account enumeration
An attacker submits reset requests for guessed email addresses and observes response content or timing to determine which accounts exist. The response body, status code, and processing time must be identical for registered and unregistered addresses.

### Token guessing
An attacker generates tokens matching the reset format and submits them. Tokens must have sufficient entropy (minimum 128 bits from a cryptographically secure source) to make brute force infeasible within the expiry window.

### Link interception and replay
An attacker intercepts a reset link from email logs, forwarded messages, or browser history and attempts to use it after the legitimate user has already completed the reset. The single-use flag and session invalidation prevent reuse.

### Reset flooding
An attacker submits continuous reset requests for a target account to fill the user's inbox, block legitimate resets, or exhaust email delivery quotas. Rate limiting per email address and per source IP must bound the number of tokens issued and emails sent.

### Cross-account token submission
An attacker obtains a token issued for their own account and submits it with another account's identifier. The token must be validated against the account it was issued for and rejected for any other account.

### Forced reset bypass
An attacker with access to a session from before a forced reset was triggered attempts to continue using the session. The forced reset flag must be checked on every authenticated request until the reset is completed.

## Tenant isolation
- In multi-tenant systems, a reset token issued for an account in one tenant must not validate for an account in another tenant
- Tenant context must be included in the token binding and verified during validation

## Protected data
- Reset tokens must be stored as hashes; the plaintext token must not be logged, persisted, or exposed in any response
- The account email address must not appear in reset link URLs in a way that allows enumeration
- Audit records must not include the plaintext token, the new password, or the old password hash
