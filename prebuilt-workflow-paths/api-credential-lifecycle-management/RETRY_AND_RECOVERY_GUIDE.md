# Retry and Recovery Guide

## Partial failures
- Credential is generated but activation or assignment does not complete
- Replacement credential is created but old-credential invalidation fails
- Credential rotation completes partially and lifecycle status is not updated
- Credential generation or provisioning dependency fails
- Credential lifecycle change succeeds but the response is lost
- Credential state changes but the audit record cannot be written
- Credential is revoked or rotated in one system while another system retains a conflicting state
- Recovery or reconciliation detects an incomplete or contradictory credential lifecycle state

## Recovery rules
- Use credential, owner, application or service, scope, lifecycle operation, and policy-version identities consistently.
- Re-read authorization, ownership, scope, current credential state, and operation state before retrying.
- Never mark creation, rotation, or revocation complete until all mandatory lifecycle effects have a resolved outcome.
- Keep incomplete, failed, uncertain, and superseded credential states visible.
- Make retries idempotent so a lost response or repeated request does not create duplicate credentials or contradictory states.
- Reconcile credential state, assignments, protected API access, audit evidence, and downstream systems before declaring recovery complete.
- Never expose credential secrets while diagnosing or recovering a failed lifecycle operation.