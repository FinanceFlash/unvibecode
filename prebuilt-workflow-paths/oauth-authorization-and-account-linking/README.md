# OAuth Authorization and Account Linking

Starts when an authenticated or eligibility-checked actor initiates sign-in with, connection to, or account linking for a supported external identity or data provider. Ends when the request is denied, cancelled, linked once with the approved scopes and subject bound to the correct local account, or remains explicitly uncertain with tokens, identity, permissions, and local account state reconciled.

| Task | File |
|---|---|
| Product and business | [PRODUCT_AND_BUSINESS_GUIDE.md](PRODUCT_AND_BUSINESS_GUIDE.md) |
| Engineering | [ENGINEERING_GUIDE.md](ENGINEERING_GUIDE.md) |
| Testing | [TESTING_GUIDE.md](TESTING_GUIDE.md) |
| Core 20 | [CORE_20_SCENARIOS.md](CORE_20_SCENARIOS.md) |
| Paths and edge cases | [PATHS_AND_EDGE_CASES.md](PATHS_AND_EDGE_CASES.md) |
| Permissions and misuse | [PERMISSION_AND_ABUSE_GUIDE.md](PERMISSION_AND_ABUSE_GUIDE.md) |
| Retry and recovery | [RETRY_AND_RECOVERY_GUIDE.md](RETRY_AND_RECOVERY_GUIDE.md) |

## Included
- provider selection, supported flow choice, state, nonce, PKCE, redirect, and callback binding
- actor eligibility, tenant and environment binding, scope approval, subject mapping, and local account selection
- sign-in, first-time account creation, existing-account linking, token exchange, refresh-token rotation, and audit
- duplicate callback defense, replay prevention, permission changes, revocation awareness, privacy, retry, recovery, and misuse

## Excluded
- local username-password authentication that does not involve an external provider
- post-link data synchronization, import, or background webhook ingestion
- ongoing resource authorization that uses an already-linked identity
- disconnect, full account deletion, and enterprise-provisioning lifecycle

The five `*_SKILL.md` files are self-contained.
