# Retry and Recovery Guide

## Partial failures
- Payment succeeds but subscription period does not advance
- Subscription advances but invoice or ledger update fails
- Cancellation records but provider schedule remains active
- Termination records but entitlement or sessions remain active
- Entitlement releases but notification or data-policy action fails
- Renewal or cancellation commits but the response is lost

## Recovery rules
- Use subscription id, period, and version as stable renewal and cancellation identities.
- Re-read subscription, payment, invoice, provider, cancellation, and entitlement state before retrying.
- Never repeat a renewal charge solely because the scheduler or client lost a response.
- Keep paid-customer access and terminated-customer release exceptions visible.
- Reconcile billing, provider, subscription, entitlement, session, invoice, and notifications.

