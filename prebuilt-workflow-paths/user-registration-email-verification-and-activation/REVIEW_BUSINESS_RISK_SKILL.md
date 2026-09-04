---
name: review-user-registration-risk
description: Review customer, revenue, permission, privacy, and operational risks in User Registration, Email Verification, and Account Activation. Use when founders, PMs, or engineering managers need prioritized consequences, controls, tests, and release concerns.
---

# Review User Registration, Email Verification, and Account Activation Risk

Review entry, credential handling, authorization, state, timing, concurrency, external effects, retry, recovery, privacy, and support paths. Prioritize:
- Duplicate account — Concurrent or replayed registration creates multiple accounts for one email
- Fake or bot account — Automated registrations pollute the user base and consume resources
- Unverified account with full access — The account gains privileges before email ownership is confirmed
- Credential exposure — Plaintext passwords or tokens appear in logs, errors, or responses
- Predictable verification token — An attacker guesses or brute-forces the token to activate arbitrary accounts
- Stale unverified account — Abandoned registrations accumulate personal data without cleanup
- Email delivery failure — The visitor cannot complete verification and the account is permanently stuck
- Unauthorized admin suspension — A valid registration is blocked without proper review or notification

For each material risk, explain trigger, behavior, business consequence, protection, decision or test, and acceptance condition.
