# Authentication, Login, Session, and Account Recovery

A reusable workflow pack for systems that authenticate users, create and maintain sessions, and recover access when credentials or authenticators are unavailable.

## Boundary

**Start:** a user attempts to establish, continue, or recover authenticated access.

**End:** access is granted, denied, revoked, or recovery completes with a new trusted authentication state.

**Included:** credential verification, MFA/step-up checks, session creation and rotation, logout/revocation, password reset, recovery-token handling, account lock/rate limits, and security notifications.

**Excluded:** identity/KYC verification, payment authorization, full account deletion, SSO provider implementation, and application-specific authorization after authentication.

## Files

- `PRODUCT_AND_BUSINESS_GUIDE.md` — product rules and outcomes
- `ENGINEERING_GUIDE.md` — implementation and tracing guidance
- `CORE_20_SCENARIOS.md` — essential scenario checklist
- `TESTING_GUIDE.md` — detailed test cases
- `PATHS_AND_EDGE_CASES.md` — normal and edge paths
- `PERMISSION_AND_ABUSE_GUIDE.md` — security and misuse controls
- `RETRY_AND_RECOVERY_GUIDE.md` — retry, revocation, and recovery
- `WRITE_PRODUCT_SPEC_SKILL.md`
- `REVIEW_BUSINESS_RISK_SKILL.md`
- `UNDERSTAND_CODE_SKILL.md`
- `IMPLEMENT_WORKFLOW_SKILL.md`
- `TEST_WORKFLOW_SKILL.md`
