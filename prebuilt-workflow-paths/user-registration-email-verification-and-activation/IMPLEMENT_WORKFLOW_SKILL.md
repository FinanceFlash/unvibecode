---
name: implement-user-registration
description: Implement or modify User Registration, Email Verification, and Account Activation. Use when adding or changing validation, credential storage, token generation, email delivery, activation, entitlements, retries, recovery, privacy controls, monitoring, or tests.
---

# Implement User Registration, Email Verification, and Account Activation

Confirm:
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

Follow project conventions and protect:
- One email address must create at most one active account
- The password must be hashed before storage and must never appear in logs or responses
- Verification tokens must be cryptographically random, time-bounded, and single-use
- Expired or consumed tokens must not activate an account
- The account must not gain full entitlements until email verification completes
- Concurrent registrations with the same email must not create duplicate accounts
- Rate limits must bound registration, resend, and verification attempts
- Personal data must follow retention and privacy policy from the moment of collection

Add all core tests and summarize decisions, files, state changes, recovery, privacy and security controls, and remaining gaps.
