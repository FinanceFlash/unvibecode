# Product and Business Guide

## Boundary

Starts when a user attempts to authenticate, establish, maintain, terminate, or recover access to an account. Ends when the user's authentication state is established, denied, expired, terminated, or recovered according to the applicable security policy.

## People and systems

- Account holder
- Authentication service
- Session or token service
- Multi-factor authentication service
- Account recovery service
- Email, SMS, or identity verification provider
- Security and fraud monitoring service
- Audit and support operations

## Things created or changed

- Account authentication state
- Authentication attempt and security event
- Multi-factor authentication challenge
- Authenticated session or access token
- Session revocation state
- Account recovery request
- Recovery token or verification challenge
- Account credential
- Security and audit record

## Stages

- Authentication: unauthenticated → primary authentication → additional verification → authenticated or denied
- Session: created → active → expired or revoked
- Logout: active → termination requested → terminated
- Recovery: requested → verification pending → verified → credential changed or recovery denied
- Recovery token: issued → valid → consumed, expired, or revoked
- Credential change: requested → verified → updated or rejected

## Product decisions

- Which authentication methods are supported
- Password, passkey, social-login, or other authentication requirements
- Whether multi-factor authentication is required and for which accounts or actions
- Authentication retry, lockout, throttling, and abuse-prevention policy
- Session lifetime, inactivity timeout, refresh-token lifetime, and revocation policy
- Whether sessions are invalidated after password or credential changes
- Logout behaviour across devices and concurrent sessions
- Account-recovery methods and required verification strength
- Recovery-token lifetime, single-use rules, and revocation behaviour
- Whether recovery invalidates existing sessions or credentials
- Notification policy for authentication, recovery, and security-sensitive events
- Account-enumeration and error-message policy
- Audit, security-event retention, and support-access policy
- Device, location, risk, and suspicious-login handling

## Happy paths

- A registered user successfully completes all required authentication steps and receives an authenticated session
- A user completes a valid multi-factor challenge and authentication is finalized
- A user completes account recovery using valid verification and successfully establishes the new credential state

## Negative paths

- Invalid credentials are rejected without creating an authenticated session
- An unknown account does not produce unnecessary account-existence information
- An expired, invalid, revoked, or already-consumed recovery token is rejected
- A restricted or locked account cannot bypass its authentication restriction
- An authenticated user cannot use their session to access another account's protected resources without authorization

## Edge cases

- Multiple authentication attempts occur concurrently for the same account
- A session expires while a protected request is being processed
- Logout occurs while another request attempts to use the same session
- A credential change occurs while existing sessions remain active
- Recovery and ordinary authentication occur concurrently for the same account
- A recovery or notification provider fails after part of the recovery process has completed
- A recovery token is submitted simultaneously from multiple requests
- Authentication succeeds immediately before an account becomes restricted
- Multiple devices attempt authentication or recovery for the same account

## Acceptance criteria

1. Only the intended account may receive an authenticated session after successful authentication
2. Invalid or incomplete authentication must not create authenticated access
3. Required authentication factors must be completed before full authentication is granted
4. Authentication retry and account-restriction policies must be enforced consistently
5. Session credentials must have defined expiration and revocation behaviour
6. Logout must prevent the terminated session from continuing to provide authenticated access
7. Recovery must require the verification evidence defined by the recovery policy
8. Recovery tokens must be scoped to the correct account and must not be reusable after consumption
9. Credential changes must apply the defined session and credential invalidation policy
10. Concurrent authentication, logout, expiration, and recovery operations must produce a deterministic security state
11. Authentication and recovery responses must not unnecessarily expose account-existence information
12. Authentication, recovery, and session operations must respect authorization and account boundaries
13. Failed external dependencies must not cause the system to report recovery success when recovery did not complete
14. Security-sensitive events must be recorded according to the audit policy
15. Authentication credentials, recovery tokens, and protected account data must not be exposed through ordinary responses or logs

## Business risks

| Risk | Business consequence |
|---|---|
| Account takeover | An unauthorized person gains access to a user's account |
| Authentication bypass | A user reaches authenticated state without satisfying required security controls |
| Credential guessing | Attackers repeatedly attempt credentials without effective throttling or restriction |
| Session hijacking | A stolen or incorrectly issued session provides unauthorized account access |
| Session persistence after logout | A terminated session continues to provide access |
| Expired-session acceptance | An expired credential continues to authorize protected actions |
| Recovery abuse | An attacker uses a weak recovery path to take control of an account |
| Recovery-token replay | A consumed recovery token is reused to regain access |
| Account enumeration | Authentication or recovery responses reveal whether accounts exist |
| Cross-account access | An authenticated identity accesses another account's protected resources |
| Credential-change race | Concurrent recovery or authentication leaves contradictory security state |
| Recovery dependency failure | The system reports successful recovery when the required operation did not complete |
| Security-event loss | Important authentication or recovery activity cannot be investigated |
| Sensitive-data exposure | Credentials, recovery evidence, tokens, or protected account information are disclosed |