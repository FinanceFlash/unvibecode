# Testing Guide

Check authoritative records, credential storage, token state, permissions, external effects, recovery, and audit—not only responses.

## 1. Valid registration creates one unverified account

**Given:** A visitor submits a valid email, password meeting strength requirements, required profile fields, and passes CAPTCHA

**When:** Registration runs

**Expect:** One account record is created with unverified status, a verification token is generated and stored, and a verification email is dispatched

**Must not happen:** The registration creates duplicate accounts or skips verification

**Best test levels:** Integration and end-to-end.

## 2. Verification email is delivered with a valid token

**Given:** A new unverified account exists with a generated verification token

**When:** Email delivery completes

**Expect:** The email contains a verification link with a cryptographically random, time-bounded, single-use token pointing to the correct account

**Must not happen:** The token is predictable, reused, or delivered to the wrong address

**Best test levels:** Integration and contract.

## 3. Valid token click activates the account

**Given:** An unverified account exists and the visitor clicks the verification link before token expiry

**When:** Token validation runs

**Expect:** The token is consumed, the account status transitions to activated, initial entitlements are granted, and a welcome notification is sent

**Must not happen:** Activation grants access without confirming email ownership

**Best test levels:** Integration and end-to-end.

## 4. Required registration field is missing

**Given:** Email, password, or a required profile field is absent or empty

**When:** Registration validation runs

**Expect:** The request fails before account creation

**Must not happen:** An incomplete account record enters the system

**Best test levels:** Unit and API.

## 5. Email format or domain is invalid

**Given:** The submitted email has invalid syntax, an unreachable domain, or a blocked disposable-email provider

**When:** Email validation runs

**Expect:** Registration is rejected with a clear error

**Must not happen:** An unreachable or blocked email creates an account

**Best test levels:** Unit and API.

## 6. Password fails strength requirements

**Given:** The password is too short, lacks required complexity, or appears in a known breach list

**When:** Password validation runs

**Expect:** Registration is rejected before credential storage

**Must not happen:** A weak, breached, or empty password is stored

**Best test levels:** Unit and security.

## 7. Email already belongs to a verified account

**Given:** A verified and activated account already exists for the submitted email

**When:** Registration runs with the same email

**Expect:** The duplicate is rejected or handled under explicit policy without revealing whether the email is registered

**Must not happen:** A second account is created for the same email

**Best test levels:** Integration and security.

## 8. CAPTCHA or bot challenge fails

**Given:** The CAPTCHA response is missing, invalid, or scored below threshold

**When:** Registration runs

**Expect:** The request is rejected before account creation

**Must not happen:** An automated registration bypasses abuse controls

**Best test levels:** Integration and security.

## 9. Two registrations with the same email arrive together

**Given:** Two concurrent requests submit the same email address

**When:** Both execute

**Expect:** Uniqueness enforcement produces at most one account

**Must not happen:** Both create accounts before uniqueness is enforced

**Best test levels:** Concurrency integration.

## 10. Verification token has expired

**Given:** The token lifetime has elapsed since generation

**When:** The visitor clicks the verification link

**Expect:** Activation is denied, the visitor is offered a resend option, and the expired token cannot be reused

**Must not happen:** An expired token activates the account

**Best test levels:** Unit with controlled time.

## 11. Verification token is consumed and replayed

**Given:** The token was already used to activate the account

**When:** The same token link is clicked again

**Expect:** The request returns the current account state without re-triggering activation effects

**Must not happen:** A used token activates the account again or triggers duplicate effects

**Best test levels:** Integration and security.

## 12. Registration response is lost

**Given:** The account and verification token may have been created but the visitor sees no confirmation

**When:** The visitor resubmits the same registration data

**Expect:** The system returns the existing pending account or resends verification without creating a duplicate

**Must not happen:** A retried submission creates a duplicate account

**Best test levels:** API and integration.

## 13. Registration endpoint is flooded

**Given:** One IP, session, or actor generates repeated registration requests

**When:** Velocity and abuse limits are reached

**Expect:** Further attempts are throttled without blocking legitimate recovery or other visitors

**Must not happen:** Unlimited attempts exhaust resources or pollute the user base

**Best test levels:** Security and load.

## 14. Email delivery fails

**Given:** The email provider rejects, bounces, or silently drops the verification email

**When:** Delivery failure is detected

**Expect:** The failure is recorded, the visitor can retry or update their email, and the account does not remain permanently stuck

**Must not happen:** The account is stuck unverified with no resend path or user feedback

**Best test levels:** Integration and contract.

## 15. Visitor requests excessive verification resends

**Given:** The visitor requests verification email resend repeatedly

**When:** Resend rate limits are reached

**Expect:** Further resends are throttled and previous tokens are invalidated per policy

**Must not happen:** Resend abuse generates spam or exhausts email quotas

**Best test levels:** Security and integration.

## 16. Account is suspended between registration and verification

**Given:** An administrator or automated rule suspends the unverified account

**When:** The visitor clicks the verification link

**Expect:** Activation is denied and the suspension reason is respected

**Must not happen:** The visitor activates a suspended account

**Best test levels:** Integration.

## 17. Verification link is opened in a different session or device

**Given:** A valid, unexpired verification token is used from a device or session different from the one that registered

**When:** Token validation runs

**Expect:** The token is validated against the account, not the session, and the correct account activates

**Must not happen:** Token validation leaks the account to an unauthorized party

**Best test levels:** Security and integration.

## 18. Registration error is logged

**Given:** The registration or verification path contains passwords, tokens, email addresses, and personal data

**When:** An error occurs

**Expect:** Diagnostics avoid plaintext credentials, tokens, and unnecessary personal data

**Must not happen:** Plaintext passwords, tokens, or personal data appear in logs

**Best test levels:** Security and log inspection.

## 19. Unverified account lingers past expiry

**Given:** The verification window has closed and the account was never activated

**When:** Cleanup or retention policy runs

**Expect:** The unverified account and associated personal data are removed or anonymized per policy

**Must not happen:** Stale personal data accumulates without cleanup or consent

**Best test levels:** Integration and operations.

## 20. Activation succeeds but welcome notification or entitlement fails

**Given:** The account is activated but the welcome email, initial role, or entitlement grant fails

**When:** Recovery runs

**Expect:** The missing effect is completed once and the account status remains truthful

**Must not happen:** The account is active without initial roles or the user receives no confirmation

**Best test levels:** Integration and operations.
