# Product and Business Guide

## Boundary
Starts when an anonymous visitor submits registration credentials and required profile data. Ends when one verified, activated account exists and is ready for first authenticated use, or the registration is rejected, the verification token expires, or the account is suspended before activation completes.

## People and systems
- Anonymous visitor or invited user
- Registration, identity, and account services
- Email delivery and verification services
- CAPTCHA, bot detection, and abuse prevention services
- Password hashing and credential storage services
- Entitlement, role, and tenant provisioning services
- Product, security, compliance, and support teams

## Things created or changed
- Registration request and submitted credentials
- Email address, normalized form, and uniqueness record
- Password hash, salt, and credential record
- Account record, account identifier, and status
- Verification token, token expiry, and delivery record
- Email delivery attempt and delivery status
- Activation timestamp, welcome notification, and audit trail
- Initial entitlement, role assignment, and tenant binding

## Stages
- Registration: absent → submitting → pending verification, rejected, or rate-limited
- Verification token: absent → generated → delivered, expired, consumed, or invalidated
- Email: unverified → verification sent → verified or expired
- Account: absent → created (unverified) → activated, suspended, or expired

## Product decisions
- Which fields are required at registration versus deferred to post-activation profile completion
- Email format, domain, and disposable-email policy
- Password length, complexity, breach-list, and reuse rules
- Whether username or display name must be unique
- Verification token format, lifetime, single-use or multi-use policy
- Maximum verification attempts and resend limits
- Whether the account may perform limited actions before email verification
- CAPTCHA, proof-of-work, or invisible bot detection at registration
- Invited-user versus open registration policy
- Age, region, terms acceptance, and consent requirements
- Welcome notification content and delivery timing
- Initial role, entitlement, trial, and tenant assignment
- Duplicate email handling: silent rejection, merge prompt, or explicit error
- Account cleanup policy for unverified registrations past expiry

## Happy paths
- A valid registration creates one unverified account and sends one verification email
- The visitor clicks the verification link before expiry and the account activates
- The activated account receives initial entitlements and a welcome notification

## Negative paths
- Required fields are missing, empty, or malformed
- Email format is invalid or the domain is blocked
- Password fails strength, length, or breach-list checks
- Email is already registered to an existing verified account
- CAPTCHA or bot detection challenge fails
- Terms, age, or region eligibility is not met

## Edge cases
- Two registrations with the same email arrive simultaneously
- Verification link is clicked after token expiry
- Visitor requests multiple verification resends in quick succession
- Account is suspended by admin between registration and verification
- Email delivery fails silently and the visitor never receives the link
- Verification link is valid but the account was already activated by a previous click

## Acceptance criteria
1. Only valid, complete registration data may create an account record
2. One email address must map to at most one active account
3. Duplicate concurrent registrations with the same email must not create multiple accounts
4. The password must never be stored or logged in plaintext
5. Verification tokens must be cryptographically unpredictable and time-bounded
6. Expired or consumed tokens must not activate an account
7. Rate limits must bound registration attempts, verification resends, and token validation per IP, email, and session
8. The account must not gain full entitlements until email verification completes
9. Personal data collected at registration must follow privacy and retention policy
10. Partial failures must remain visible, auditable, and repairable

## Business risks
| Risk | Business consequence |
|---|---|
| Duplicate account | Concurrent or replayed registration creates multiple accounts for one email |
| Fake or bot account | Automated registrations pollute the user base and consume resources |
| Unverified account with full access | The account gains privileges before email ownership is confirmed |
| Credential exposure | Plaintext passwords or tokens appear in logs, errors, or responses |
| Predictable verification token | An attacker guesses or brute-forces the token to activate arbitrary accounts |
| Stale unverified account | Abandoned registrations accumulate personal data without cleanup |
| Email delivery failure | The visitor cannot complete verification and the account is permanently stuck |
| Unauthorized admin suspension | A valid registration is blocked without proper review or notification |
