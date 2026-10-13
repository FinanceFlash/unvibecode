# Paths and Edge Cases

## Valid

- Correct credentials
- Correct MFA
- Valid recovery token
- Normal logout
- Normal token refresh

## Invalid

- Wrong password
- Wrong/expired MFA
- Invalid or malformed token
- Disabled account
- Revoked session

## Duplicate and replayed

- Repeated login submission
- Reused MFA code
- Reused recovery token
- Reused rotated refresh token
- Duplicate password-reset completion

## Stale and expired

- Expired session
- Expired challenge
- Expired recovery request
- Credential changed between request and completion

## Concurrent

- Two successful logins
- Logout racing with request
- Two recovery completions
- Two refresh requests using the same token
- Lockout racing with a valid login

## Recovery outcomes

- Recovery succeeds
- Recovery token expires
- Recovery token is consumed
- Notification provider fails
- Credential update succeeds but notification fails

## Out of order

- Reset completion before recovery request
- MFA verification before challenge creation
- Refresh after session revocation

Every path must preserve the declared authentication boundary and must not create an unintended bypass.
