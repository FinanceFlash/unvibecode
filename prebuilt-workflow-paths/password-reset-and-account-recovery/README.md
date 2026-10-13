# Password Reset and Account Recovery

Starts when a user submits a password reset request with a registered email address. Ends when the user authenticates successfully with the new credential, the reset token is consumed, all prior sessions are invalidated, and the account record reflects the updated credential.

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
- reset request submission and email validation
- token generation, delivery, expiry, single-use enforcement, and revocation
- credential update, password policy validation, and audit record
- active session invalidation after credential change
- account enumeration protection and rate limiting
- admin-triggered forced reset path

## Excluded
- user registration and initial password creation
- multi-factor authentication and step-up verification
- account deletion and right-to-erasure
- transactional notification delivery mechanics
- fraud-risk scoring and account lock investigation

The five `*_SKILL.md` files are self-contained.
