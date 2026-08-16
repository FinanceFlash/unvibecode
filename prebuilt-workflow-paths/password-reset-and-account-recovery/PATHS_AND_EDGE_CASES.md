# Paths and Edge Cases

## Supported paths
- Active account submits reset request and receives token link within the configured window
- User opens token link and sets a new password that meets all policy rules
- Credential is updated, token is consumed, and all sessions are invalidated in one operation
- Admin triggers a forced reset and the user must complete it before accessing the application
- User requests a second reset before the first token expires; the prior token is revoked

## Denied paths
- Unregistered email submits a reset request: safe identical response, no token issued
- Expired token submitted: request rejected, credential unchanged
- Consumed token replayed: request rejected, credential unchanged
- Non-compliant password submitted: request rejected, credential unchanged
- Reset request for locked or suspended account: request rejected, no token issued
- Rate limit exceeded: request rejected, no token issued
- Tampered or structurally invalid token: request rejected at format check

## Timing and expiry boundaries
- Token submitted exactly at the expiry timestamp: implementation must define inclusive or exclusive boundary and apply it consistently
- Reset request submitted immediately before and immediately after the rate limit window resets
- Session invalidation called immediately after credential update: invalidation must not race with a concurrent authentication using the old credential

## Concurrency paths
- Two reset requests arrive simultaneously for the same account: only the later token remains valid
- Reset request and a concurrent login with the old credential overlap: the login must fail after the credential update is committed
- Session invalidation and a concurrent token refresh overlap: the refresh must fail if invalidation is committed first

## Unusual paths
- User completes reset but does not sign in with the new credential before the session invalidation window closes
- Account email address changes between reset request and token use
- Email provider returns a delivery failure after the token has been issued
- User opens the reset link from a forwarded or shared email
- Multiple reset emails are forwarded to a shared inbox and a non-account-holder uses one
