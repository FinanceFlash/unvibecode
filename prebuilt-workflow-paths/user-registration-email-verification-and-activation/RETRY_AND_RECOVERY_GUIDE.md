# Retry and Recovery Guide

## Partial failures
- Account record is created but verification token generation fails
- Verification token is generated but email delivery fails
- Email is delivered but the delivery confirmation is lost
- Verification token is consumed but account activation write fails
- Account activates but initial entitlement or role grant fails
- Account activates but welcome notification fails
- Registration succeeds but the response to the visitor is lost

## Recovery rules
- Use the submitted email address as the stable registration identity for duplicate detection.
- Re-read account status, token state, and delivery records before retrying.
- Never create a second account solely because the registration response was lost.
- Invalidate previous verification tokens before generating replacements on resend.
- Keep the original registration timestamp and submitted data separate from later profile changes.
- Reconcile account status, verification state, entitlement grants, and notification delivery.
