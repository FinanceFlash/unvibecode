---
name: test-oauth-authorization-and-account-linking
description: Design, implement, or review tests for OAuth Authorization and Account Linking. Use when complete normal, invalid, boundary, concurrency, replay, failure, recovery, permission, privacy, and misuse scenarios are needed.
---

# Test OAuth Authorization and Account Linking

Cover:
1. Eligible user links a provider account once
2. Returning user signs in with the linked provider
3. State or PKCE verifier is missing or wrong
4. Provider denies consent
5. Callback code is replayed
6. Redirect target is unapproved
7. Requested scopes exceed policy
8. Provider subject is already linked elsewhere
9. Email or claim collides with another account
10. Two link attempts run concurrently
11. Callback arrives after cancellation or expiry
12. Token exchange succeeds but local write fails
13. Local write succeeds but response is lost
14. Refresh token rotates
15. Provider revokes access later
16. Cross-tenant provider identity is supplied
17. Support or admin relink is attempted without authority
18. OAuth error details are logged
19. Provider callback omits required claim data
20. Reconciliation runs after uncertain exchange status

For each scenario write Given, When, expected response and authoritative state changes, forbidden outcomes, test level, fixtures, controlled time or provider behavior, and cleanup.
