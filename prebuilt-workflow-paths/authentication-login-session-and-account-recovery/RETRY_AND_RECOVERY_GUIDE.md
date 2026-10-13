# Retry and Recovery Guide

## Recovery rules

1. Retries must not turn one authentication or recovery action into multiple state changes.
2. One-time tokens must remain one-time across retries and concurrent requests.
3. Provider failures must not silently grant access.
4. If credential persistence succeeds but notification fails, preserve the authoritative credential state and record the notification failure for safe retry.
5. If a session is revoked, retries using that session must remain rejected.
6. Refresh-token rotation must detect reuse of an already-consumed token.
7. Expired recovery requests require a new recovery request.
8. Manual repair must use authoritative account/security records rather than rewriting audit history.

## Idempotency

Use an operation identifier or equivalent mechanism for recovery completion where duplicate submissions are possible. The second submission should return the already-determined safe outcome or a clear rejection without repeating the credential change.
