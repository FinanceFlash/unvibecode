# Paths and Edge Cases

## Supported paths
- Open registration with email and password
- Invited-user registration with pre-approved email
- Registration with CAPTCHA or bot detection challenge
- Email verification via single-use token link
- Verification resend for unverified accounts
- Rejected registration for invalid or duplicate data
- Expired verification, cleanup, and re-registration
- Admin-initiated account suspension before activation

## Normal paths
- A valid registration creates one unverified account and sends one verification email
- The visitor clicks the verification link before expiry and the account activates
- The activated account receives initial entitlements and a welcome notification

## Denied paths
- Required email, password, or profile field is missing or malformed
- Email format is invalid or the domain is blocked
- Password fails strength, length, or breach-list requirements
- Email is already registered to an existing verified account
- CAPTCHA or bot detection challenge fails
- Terms, age, or region eligibility is not met

## Timing, concurrency, and boundaries
- Two registrations with the same email arrive simultaneously
- Verification link is clicked exactly at token expiry
- Visitor requests multiple verification resends in quick succession
- Account is suspended by admin between registration and verification
- Email delivery fails silently and the visitor never receives the link
- Verification link is valid but the account was already activated by a previous click
- Registration response is lost and the visitor resubmits

Cover valid, invalid, duplicate, expired, replayed, repeated, simultaneous, suspended, partially completed, unauthorized, and recovery outcomes.
