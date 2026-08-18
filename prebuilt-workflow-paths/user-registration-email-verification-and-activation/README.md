# User Registration, Email Verification, and Account Activation

Starts when an anonymous visitor submits registration credentials and required profile data. Ends when one verified, activated account exists and is ready for first authenticated use, or the registration is rejected, the verification token expires, or the account is suspended before activation completes.

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
- credential submission, email format and uniqueness validation, password strength, and required profile fields
- account record creation, verification token generation, email delivery, and token validation
- account activation, welcome notification, initial entitlement grant, and audit trail
- duplicate email handling, bot detection, abuse throttling, and expired token cleanup

## Excluded
- authentication and session management after activation
- password reset and account recovery
- OAuth, SSO, and federated identity linking
- profile editing and account settings changes after activation

The five `*_SKILL.md` files are self-contained.
