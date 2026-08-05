# Paths and Edge Cases

## Supported paths
- Email delivery
- SMS delivery
- Mobile or web push delivery
- In-app notification creation
- Localized template and channel selection
- Suppression, quiet-hours, expiry, and ineligible-recipient denial
- Provider acceptance, callback, bounce, and failure recording
- Retry handoff, reconciliation, and manual operational review

## Normal paths
- A valid business event creates and submits one safe message to the intended recipient
- The correct approved template and locale render with complete allowed variables
- Provider acceptance and later delivery status are correlated to the same message

## Denied paths
- Recipient, destination, template, purpose, or required variable is missing or invalid
- The destination is unverified, suppressed, or ineligible for the purpose
- Template data would expose another customer or disallowed information
- A duplicate or stale event is rejected or mapped to the existing message

## Timing, concurrency, and boundaries
- Two copies of the same business event arrive together
- The send occurs exactly at expiry or a quiet-hours boundary
- Recipient, locale, preference, or destination changes during rendering
- Provider accepts the message but the response is lost
- A delayed provider callback arrives after local failure or retry handoff

Cover valid, invalid, duplicate, expired, stale, replayed, repeated, simultaneous, partially completed, unauthorized, and recovery outcomes.

