# Product and Business Guide

## Boundary
Starts when an eligible business event requires a transactional notification. Ends when one recipient-safe message is rejected before sending, accepted by a channel provider, recorded as delivered or failed, or handed to the separate retry-and-fallback workflow.

## People and systems
- Business event producer
- Intended recipient
- Notification orchestration service
- Template and localization service
- Email, SMS, push, or in-app provider
- Preference, consent, identity, and tenant services
- Support, privacy, security, and operations teams

## Things created or changed
- Eligible business event and deduplication key
- Recipient, destination, locale, purpose, and channel eligibility
- Template version, variables, rendered content, and attachments
- Notification message and delivery attempt
- Provider request and provider message reference
- Delivery status, callback, error classification, and audit record

## Stages
- Event: received → eligible or suppressed → message created
- Message: pending → submitted → accepted, delivered, failed, suppressed, or expired
- Provider attempt: not started → uncertain, accepted, rejected, or failed
- Failure handoff: absent → retryable failure recorded or final failure

## Product decisions
- Which events require a transactional notification
- How the authoritative recipient and tenant are resolved
- Transactional-purpose, consent, preference, suppression, and legal rules
- Channel priority, availability, verified-destination, and quiet-hours policy
- Template version, locale, variable, escaping, redaction, and attachment rules
- What personal or confidential data each channel may contain
- Deduplication key and exactly-once business-notification policy
- Provider success, accepted, delivered, bounced, expired, and failed meanings
- Which initial failures hand off to retry and fallback
- Rate, frequency, cost, provider, monitoring, and retention limits

## Happy paths
- A valid business event creates and submits one safe message to the intended recipient
- The correct approved template and locale render with complete allowed variables
- Provider acceptance and later delivery status are correlated to the same message

## Negative paths
- Recipient, destination, template, purpose, or required variable is missing or invalid
- The destination is unverified, suppressed, or ineligible for the purpose
- Template data would expose another customer or disallowed information
- A duplicate or stale event is rejected or mapped to the existing message

## Edge cases
- Two copies of the same business event arrive together
- The send occurs exactly at expiry or a quiet-hours boundary
- Recipient, locale, preference, or destination changes during rendering
- Provider accepts the message but the response is lost
- A delayed provider callback arrives after local failure or retry handoff

## Acceptance criteria
1. Only an eligible event may create a transactional message
2. The authoritative intended recipient, tenant, destination, purpose, and channel must be resolved
3. Template version, locale, variables, escaping, and redaction must be valid before sending
4. One business event must not create duplicate recipient-visible notifications
5. Suppression, preference, consent, verified-destination, and quiet-hours policy must be explicit
6. Provider requests and callbacks must correlate to the correct local message and attempt
7. Accepted, delivered, failed, and uncertain outcomes must not be confused
8. Retryable failure must be handed off once without duplicating the initial message
9. Provider credentials, message secrets, and unnecessary personal data must not be exposed
10. Every message outcome must remain auditable and operationally visible

## Business risks
| Risk | Business consequence |
|---|---|
| Wrong recipient | Account, tenant, destination, or identity resolution sends protected information elsewhere |
| Ineligible channel | Preference, consent, verification, suppression, or purpose rules are bypassed |
| Duplicate notification | Replayed events or lost responses send the same business message repeatedly |
| Missing critical notice | The application records success although no provider attempt or recoverable handoff exists |
| Unsafe rendering | Template variables, markup, links, or attachments expose data or enable injection |
| False delivery state | Provider acceptance is recorded as final delivery or callbacks move status backward |
| Message amplification | One event or attacker triggers unbounded provider traffic and cost |
| Secret or personal-data exposure | Destinations, content, tokens, provider responses, or credentials reach unsafe logs |

