# Core 20 Scenarios

| # | Scenario | Must not happen |
|---:|---|---|
| 1 | Valid registration creates one unverified account | The registration creates duplicate accounts or skips verification |
| 2 | Verification email is delivered with a valid token | The token is predictable, reused, or delivered to the wrong address |
| 3 | Valid token click activates the account | Activation grants access without confirming email ownership |
| 4 | Required registration field is missing | An incomplete account record enters the system |
| 5 | Email format or domain is invalid | An unreachable or blocked email creates an account |
| 6 | Password fails strength requirements | A weak, breached, or empty password is stored |
| 7 | Email already belongs to a verified account | A second account is created for the same email |
| 8 | CAPTCHA or bot challenge fails | An automated registration bypasses abuse controls |
| 9 | Two registrations with the same email arrive together | Both create accounts before uniqueness is enforced |
| 10 | Verification token has expired | An expired token activates the account |
| 11 | Verification token is consumed and replayed | A used token activates the account again or triggers duplicate effects |
| 12 | Registration response is lost | A retried submission creates a duplicate account |
| 13 | Registration endpoint is flooded | Unlimited attempts exhaust resources or pollute the user base |
| 14 | Email delivery fails | The account is stuck unverified with no resend path or user feedback |
| 15 | Visitor requests excessive verification resends | Resend abuse generates spam or exhausts email quotas |
| 16 | Account is suspended between registration and verification | The visitor activates a suspended account |
| 17 | Verification link is opened in a different session or device | Token validation leaks the account to an unauthorized party |
| 18 | Registration error is logged | Plaintext passwords, tokens, or personal data appear in logs |
| 19 | Unverified account lingers past expiry | Stale personal data accumulates without cleanup or consent |
| 20 | Activation succeeds but welcome notification or entitlement fails | The account is active without initial roles or the user receives no confirmation |

Full details are in [TESTING_GUIDE.md](TESTING_GUIDE.md).
