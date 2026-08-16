# Product and Business Guide

## Boundary
Starts when a user submits a password reset request with a registered email address. Ends when the user authenticates successfully with the new credential, the reset token is consumed, all prior sessions are invalidated, and the account record reflects the updated credential.

## People and systems
- User or account holder requesting the reset
- Authentication and identity service
- Token store and session store
- Email and notification service
- Account and user profile service
- Operations, support, and security teams

## Things created or changed
- Password reset request and submission timestamp
- Reset token, token hash, expiry time, and single-use flag
- Reset email containing the token link and expiry notice
- New credential and password hash replacing the previous one
- Active sessions, refresh tokens, and access tokens invalidated after credential change
- Audit record of reset request, token issue, credential update, and session invalidation

## Stages
- Reset request: absent → submitted → validated, rejected, or rate-limited
- Token: absent → issued → delivered, consumed, expired, or revoked
- Email: absent → queued → delivered or failed
- Credential: current → pending update → updated or unchanged
- Sessions: active → invalidating → fully invalidated or partially active

## Product decisions
- Which email addresses and account states may initiate a reset
- Token format, length, entropy, and storage strategy (hash vs plaintext)
- Token expiry window and whether a new request revokes the prior token
- Safe response policy when the submitted email is not registered
- Password complexity, minimum length, history, and reuse rules
- Whether the new password may match the current password
- Session invalidation scope: all devices, all except current, or configurable
- Rate limiting strategy: per email, per IP, per account, and lockout behaviour
- Notification to the user after a successful credential change
- Admin-triggered forced reset and its interaction with the standard flow
- Audit retention and privacy rules for reset events

## Happy paths
- A registered user submits their email, receives a valid reset link, sets a new password that meets policy, and signs in with the new credential
- All active sessions are invalidated after the credential is updated
- The consumed token cannot be reused

## Negative paths
- The submitted email is not associated with any account
- The token has expired before it is used
- The token has already been consumed
- The new password does not meet complexity or reuse policy
- The account is locked, suspended, or pending deletion at the time of the request or use
- The rate limit for reset requests has been exceeded

## Edge cases
- Two concurrent reset requests arrive for the same account
- The user uses a previously issued token after a newer one has been requested
- The reset email is delivered but the link is opened after the token has expired
- The credential update succeeds but the session invalidation response is lost
- The account is deleted between request submission and token use
- A reset request arrives for an account whose email address has changed since the link was generated
- The user sets the same password as the current one when policy should prevent it

## Acceptance criteria
1. A reset request for an unregistered email must return a safe, identical response to a valid one
2. Tokens must be single-use: a consumed token must not update the credential a second time
3. Tokens must expire: an expired token must not update the credential
4. A new token request must revoke any prior unconsumed token for the same account
5. The new credential must meet all password policy rules before the update is committed
6. All active sessions must be invalidated after a successful credential update
7. The credential update and session invalidation must be atomic or leave a recoverable, auditable state on partial failure
8. Reset requests must be rate-limited to prevent enumeration and abuse
9. The reset audit record must capture request time, token issue, credential update, and session invalidation outcome
10. No information about account existence must be revealed through response timing or content differences

## Business risks
| Risk | Business consequence |
|---|---|
| Account enumeration via reset response | Attacker discovers which email addresses are registered |
| Token not single-use | Attacker who intercepts a used link can change the credential again |
| No token expiry | Indefinitely valid links expose accounts to delayed takeover |
| Sessions not invalidated after reset | Attacker who holds an active session retains access after the user resets |
| Credential update without policy check | Weak or previously breached password replaces the current one |
| New token does not revoke previous token | Multiple valid reset links exist simultaneously, increasing exposure window |
| Timing difference reveals account existence | Statistical analysis of response times exposes registered accounts |
| No rate limiting on reset requests | Attacker floods the system with reset emails, causing denial of service |
| Partial session invalidation not surfaced | User believes they are secure while attacker retains one active session |
| Audit record missing | Security investigation cannot reconstruct the reset sequence |
