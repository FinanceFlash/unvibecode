# API Credential Lifecycle Management

Starts when an authorized person or service requests creation, rotation, or revocation of an API credential. Ends when the requested lifecycle action reaches a verified state: the credential is activated, denied, rotated with the previous credential invalidated, revoked, expired, or remains explicitly incomplete with evidence and recovery work recorded.

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

- credential request, requester authorization, scope validation, and lifecycle state changes
- credential generation, activation, assignment, expiry, rotation, and revocation
- controlled credential overlap during rotation and invalidation of superseded credentials
- credential use verification, audit evidence, dependency failures, partial completion, retry, recovery, and final-state reconciliation

## Excluded

- general user login and session management
- OAuth and OIDC authorization flows
- JWT issuance and validation
- password management and password recovery
- general API rate limiting
- general secrets-management infrastructure
- general authorization architecture outside credential lifecycle decisions

The five `*_SKILL.md` files are self-contained.