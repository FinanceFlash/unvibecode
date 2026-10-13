# Engineering Guide

## Trace sequence

1. Locate login, logout, refresh, password-reset, and recovery entry points.
2. Identify the authoritative user/account record.
3. Trace credential verification and MFA/step-up decisions.
4. Trace session/token creation, rotation, persistence, and expiry.
5. Trace logout and server-side revocation where applicable.
6. Trace recovery-token generation, storage, validation, consumption, and expiry.
7. Trace notifications and audit records.
8. Check rate limits, lockouts, replay protection, and concurrent requests.
9. Confirm downstream authorization receives the intended authenticated identity.

## Implementation safeguards

- Never log passwords, OTPs, recovery tokens, or session secrets.
- Store passwords with an appropriate password-hashing scheme, not reversible encryption.
- Prefer hashed/tokenized recovery secrets at rest.
- Bind recovery actions to the intended account and action.
- Make recovery and credential-changing operations idempotent where appropriate.
- Rotate session identifiers/tokens after authentication state changes when required.
- Revoke compromised or superseded sessions.
- Use constant-time comparisons for secret verification where applicable.
- Keep authentication and authorization distinct.

## Evidence to verify

For every conclusion, identify the route/handler, state mutation, token/session operation, external call, and test that supports it.
