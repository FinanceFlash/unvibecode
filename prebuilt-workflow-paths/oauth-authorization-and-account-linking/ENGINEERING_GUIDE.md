# Engineering Guide

## Trace the implementation
1. Sign-in or link entry points, supported provider selection, and request validation
2. Actor eligibility, tenant binding, local session state, and step-up requirements
3. State, nonce, PKCE verifier, redirect URI, callback target, and expiry generation
4. Provider authorization request construction, requested scopes, and consent flags
5. Callback handler validation for provider, state, nonce, code, tenant, and local account context
6. Code exchange, token parsing, claim retrieval, provider-subject normalization, and replay defense
7. Local account resolution, create-versus-link decision, uniqueness constraints, and collision handling
8. Token storage, encryption, rotation, revocation checks, audit, session creation, and user-visible status updates
9. Retry, reconciliation, relink, disconnect prerequisite checks, and manual repair paths

## Rules the code should protect
- State, nonce, PKCE, provider, tenant, redirect, and local account are bound to one request record
- Redirect URIs and post-login targets come from an allowlist, not raw user input
- Provider subject, tenant, and trustable claims resolve to one local account outcome
- Unique constraints and idempotent callback handling prevent duplicate sessions or provider-link rows
- Scope changes, missing claims, provider errors, and denial responses are explicit states, not generic success
- Tokens are encrypted or reference-stored, redacted in logs, and rotated or revoked by policy
- Recovery distinguishes user cancellation, provider denial, exchange failure, and uncertain exchange success

## Build or change safely
1. Confirm provider, scope, account-matching, and trust decisions before relying on framework defaults.
2. Follow existing authorization, session, token-storage, logging, monitoring, and test conventions.
3. Bind every action to the authoritative actor, provider, tenant, request, state, and local account scope.
4. Enforce permission, current-state, uniqueness, ordering, and expiry rules at the write.
5. Make retries, callback replays, and lost responses safe after partial failure.
6. Keep identity, token, and session inconsistency visible and repairable.
7. Add the core 20 tests.
