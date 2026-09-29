# Product and Business Guide

## People and systems

- End user
- Authentication service
- Session/token store
- MFA/authenticator provider
- Email/SMS notification provider
- Account recovery service
- Application/API consuming authenticated identity
- Security/support team

## Things created or changed

- Login attempt
- Authentication challenge
- Session/access token
- Refresh token or session record
- Recovery request/token
- Credential state
- Account security state
- Security notification/audit event

## Stages

1. Authentication requested
2. Credentials validated
3. Additional challenge evaluated
4. Session established or denied
5. Session continued/rotated
6. Logout or revocation
7. Recovery requested
8. Recovery verified
9. Credential/authenticator reset
10. Security notification and audit

## Primary business outcome

Only an authorized user receives an authenticated session, and a legitimate owner can recover access without creating an unauthorized path.

## Decisions to define

- Session lifetime and idle timeout
- Refresh-token lifetime and rotation
- MFA requirements and remembered-device duration
- Maximum failed attempts and lock duration
- Recovery-token lifetime and one-time use
- Whether password reset revokes existing sessions
- Whether recovery changes require notifications or a cooldown
- Support-assisted recovery requirements
- Device/session visibility and revocation policy

## Acceptance criteria

- Invalid credentials never create an authenticated session.
- A successful login creates only the intended session state.
- MFA-protected accounts cannot bypass the required challenge through alternate login paths.
- Logout/revocation makes the affected session unusable.
- Recovery tokens are scoped, short-lived, single-use, and cannot be replayed.
- Credential recovery does not expose whether an account exists beyond the chosen policy.
- Password/authenticator changes invalidate credentials or sessions according to the declared policy.
- Security events are auditable without storing secrets or raw recovery tokens.
