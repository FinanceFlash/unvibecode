# Product and Business Guide

## Boundary
Starts when an authenticated or eligibility-checked actor initiates sign-in with, connection to, or account linking for a supported external identity or data provider. Ends when the request is denied, cancelled, linked once with the approved scopes and subject bound to the correct local account, or remains explicitly uncertain with tokens, identity, permissions, and local account state reconciled.

## People and systems
- End user, administrator, or support-approved actor
- Local application, session service, and account service
- OAuth or OIDC authorization server
- External provider API or tenant directory
- Risk, abuse, audit, and notification services
- Support, security, privacy, and operations teams

## Things created or changed
- Link or sign-in request
- State, nonce, PKCE verifier, and redirect context
- Provider authorization code or device code if supported
- Provider subject, tenant, approved scopes, and claims
- Local account, login session, or provider-link record
- Access token, refresh token, expiry, rotation status, and revocation state
- Consent record, audit entry, and user-visible connection status

## Stages
- Link request: created → awaiting provider, callback received, approved, denied, cancelled, failed, or uncertain
- Provider link: absent → pending → linked, relink required, revoked, or blocked
- Local session: anonymous → challenged, authenticated, linked, or rejected
- Token set: absent → active → rotated, expired, revoked, or uncertain

## Product decisions
- Which providers, tenants, account types, and environments are supported
- Whether the flow is login-only, link-only, or allows both for the same provider
- Which scopes are mandatory, optional, incremental, or forbidden
- Whether new local accounts may be created automatically from provider claims
- How email, phone, subject, tenant, and domain are trusted for account matching
- State, nonce, PKCE, redirect, and callback-expiry policy
- How an already-linked external account is handled when another local account tries to claim it
- Session lifetime, step-up authentication, and support override policy
- Token storage, encryption, rotation, revocation polling, and disconnect behavior
- Customer communication, audit retention, abuse monitoring, and manual repair path

## Happy paths
- A signed-in user links one external provider account with the approved scopes
- A returning user signs in through the same provider and is mapped to the correct local account
- A provider rotates refresh tokens and the link remains valid without duplicate records

## Negative paths
- State, nonce, PKCE, redirect, subject, or tenant binding is invalid
- The provider denies consent or returns an explicit error
- The actor lacks permission to create or change the link
- Provider claims collide with another local account or forbidden tenant

## Edge cases
- Two callbacks or link attempts arrive for the same request
- A callback arrives after the user cancelled or the request expired
- The provider succeeds but the local write or response fails
- Scopes change between initial request and callback
- The provider revokes or rotates tokens while local state still shows active

## Acceptance criteria
1. Only an eligible actor may start login or linking for the chosen provider and tenant context
2. State, nonce, PKCE, redirect target, provider, tenant, and local account must bind to one request
3. The approved provider subject must map to exactly one allowed local account outcome
4. Consent, scopes, claims, and account-creation rules must follow explicit policy
5. A provider account already linked elsewhere must not be silently reassigned
6. Duplicate callbacks, code replay, and repeated exchanges must not create extra sessions or links
7. Tokens, claims, and personal data must remain protected in storage, logs, and support tooling
8. Uncertain exchange or callback outcomes must be reconciled before unsafe retry or relink
9. Local connection status must stay consistent with provider revocation, expiry, and rotation state
10. Every account-link change must be auditable and manually repairable

## Business risks
| Risk | Business consequence |
|---|---|
| Account takeover | A user is signed into or linked with another person's local account |
| Cross-tenant connection | An identity from one tenant gains access to another tenant's data or settings |
| Scope overreach | The application stores or uses broader permissions than the user approved |
| Duplicate or broken links | Replays or concurrent callbacks create conflicting provider-link records |
| False active connection | A revoked or expired provider relationship still appears usable |
| Silent identity collision | Email or claim matching joins the wrong local account |
| Token exposure | Access or refresh tokens leak through logs, support tools, or unsafe storage |
| Unrepairable uncertainty | A successful provider exchange is lost locally and cannot be reconciled safely |
