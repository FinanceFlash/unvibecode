# Retry and Recovery Guide

## Partial failures
- Provider code exchange succeeds but the application crashes before persisting the link
- Local link persists but the redirect response or session cookie is lost
- Token refresh rotates credentials while another worker still uses the old token
- Revocation or relink state changes arrive out of order

## Recovery rules
- Use request, provider, issuer, subject, tenant, local account, and token identities consistently.
- Retry callback handling only with replay-safe request records and uniqueness constraints.
- Record explicit uncertain states instead of guessing whether login or linking completed.
- Reconcile provider subject, scope, token status, local link row, session, and audit to one outcome.
- Keep a manual repair path that can verify the correct local account before changing any link assignment.
