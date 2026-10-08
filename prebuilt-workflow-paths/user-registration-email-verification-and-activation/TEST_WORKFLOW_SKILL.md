---
name: test-user-registration
description: Design, implement, or review tests for User Registration, Email Verification, and Account Activation. Use when complete normal, invalid, boundary, concurrency, replay, failure, recovery, permission, privacy, and misuse scenarios are needed.
---

# Test User Registration, Email Verification, and Account Activation

Cover:
1. Valid registration creates one unverified account
2. Verification email is delivered with a valid token
3. Valid token click activates the account
4. Required registration field is missing
5. Email format or domain is invalid
6. Password fails strength requirements
7. Email already belongs to a verified account
8. CAPTCHA or bot challenge fails
9. Two registrations with the same email arrive together
10. Verification token has expired
11. Verification token is consumed and replayed
12. Registration response is lost
13. Registration endpoint is flooded
14. Email delivery fails
15. Visitor requests excessive verification resends
16. Account is suspended between registration and verification
17. Verification link is opened in a different session or device
18. Registration error is logged
19. Unverified account lingers past expiry
20. Activation succeeds but welcome notification or entitlement fails

For each scenario write Given, When, expected response and authoritative state changes, forbidden outcomes, test level, fixtures, controlled time or dependency behavior, and cleanup.
