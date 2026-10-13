---
name: "Review Business Risk for Password Reset and Account Recovery"
description: "Reviews the password reset and account recovery workflow for customer, security, revenue, and operational risks, including account takeover, session persistence after credential change, enumeration exposure, and partial recovery failures."
---

# Review Business Risk — Password Reset and Account Recovery

You are reviewing the password reset and account recovery workflow for business risk.

## Your task

Using the connected code context and any available specification, identify risks that could harm customers, expose accounts to takeover, cause revenue loss, or create an unrecoverable operational state.

## Risk categories to evaluate

**Account takeover risks**
- Is the token single-use? Can a consumed token be replayed?
- Is token entropy sufficient to prevent brute force within the expiry window?
- Are multiple valid tokens possible for the same account at the same time?
- Is session invalidation guaranteed after a credential update?

**Enumeration and privacy risks**
- Does the response differ by content or timing based on whether the email is registered?
- Are plaintext tokens written to logs, URLs, or error messages?
- Does the reset link embed the email address in a way that allows account discovery?

**Availability and abuse risks**
- Can an attacker flood a user's inbox by submitting repeated reset requests?
- Is rate limiting applied per email address and per source IP independently?
- Can reset request flooding prevent a legitimate user from completing a reset?

**Recovery and operational risks**
- If session invalidation fails, is the failure visible and repairable by operations?
- If the credential update succeeds but confirmation notification fails, is the user informed through another channel?
- Can operations revoke all tokens and invalidate all sessions for an account without resetting the credential?

**Forced reset risks**
- If an admin forces a reset, can the user bypass it by using an existing session?
- Is the forced reset flag checked on every authenticated request until the reset is complete?

## For each risk found, state

- What triggers the risk
- What the code currently does or fails to do
- The affected workflow stage
- The potential business impact
- What should change
- How to verify the correction

If no risk meets the evidence threshold, record a no-findings outcome with the scope reviewed and the evidence examined.
