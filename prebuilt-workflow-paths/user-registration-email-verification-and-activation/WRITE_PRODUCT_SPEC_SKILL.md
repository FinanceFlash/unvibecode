---
name: write-user-registration-spec
description: Write or review a product specification for User Registration, Email Verification, and Account Activation. Use when defining actors, states, credential rules, verification policy, edge cases, acceptance criteria, recovery, or business risks.
---

# Write a User Registration, Email Verification, and Account Activation Specification

Use application-native terms. Decide:
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

Write scope, actors, objects, states, paths, customer and business outcomes, permissions, recovery, privacy, misuse, acceptance criteria, and unanswered decisions.
