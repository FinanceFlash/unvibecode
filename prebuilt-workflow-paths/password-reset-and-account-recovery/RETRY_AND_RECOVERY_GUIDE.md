# Retry and Recovery Guide

## Partial failures and their recovery states

### Token issued but email not delivered
The token exists in the store but the email was never received. The user may request a new reset, which revokes the prior token and issues a new one. The system must not leave an orphaned, unreachable token that remains valid indefinitely.

### Credential update succeeds but session invalidation fails
The new credential is committed but one or more sessions remain active. The system must record a session invalidation failure in the audit log and retry invalidation asynchronously. Any retry must be idempotent and must not trigger a second credential update. Operations must be able to trigger a manual forced-logout for all sessions on the account.

### Session invalidation succeeds but confirmation notification fails
Sessions are cleared but the user does not receive a confirmation email. The audit log must record the notification failure. The credential update is not rolled back. A retry of the notification is safe because it carries no credential information.

### Credential update fails after token consumption
If the token is marked consumed before the credential write is committed and the write then fails, the account is left with a consumed token and the old credential. The recovery path is to allow the user to request a new reset. The implementation must avoid consuming the token before the credential write is confirmed.

## Idempotency rules
- Submitting a valid unconsumed token a second time before it is consumed must be idempotent if the password submission is identical; the credential must not be updated twice
- Retrying session invalidation after a lost response must produce the same invalidated state without affecting the credential
- Retrying the confirmation notification must not send duplicate emails if the first delivery succeeded

## Retry boundaries
- The token validation and credential update must complete within one synchronous request; retrying this call with the same token after a timeout must be rejected if the token was already consumed
- Session invalidation retries must be bounded; after a configured number of failures the account must be flagged for manual review

## Manual repair
- Operations must be able to revoke all active tokens for an account without changing the credential
- Operations must be able to force-invalidate all sessions for an account independently of the reset flow
- Operations must be able to mark an account as requiring a forced reset without knowing the current credential
