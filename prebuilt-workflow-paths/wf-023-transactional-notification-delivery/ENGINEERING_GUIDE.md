# Engineering Guide

## Trace the implementation
1. Business-event producers and notification-request entry points
2. Event eligibility, deduplication, purpose, tenant, recipient, preference, consent, and suppression checks
3. Destination verification, channel selection, quiet-hours, expiry, and provider routing
4. Template lookup, version, locale, variables, escaping, redaction, links, and attachments
5. Message and attempt storage, transactions, uniqueness, and simultaneous-event handling
6. Provider client, credentials, timeouts, accepted result, and provider reference
7. Callback correlation, monotonic status, failure classification, and retry handoff
8. Audit, privacy, retention, monitoring, support tools, and tests

## Rules the code should protect
- Only eligible business events may create transactional notifications
- Recipient, destination, purpose, tenant, and channel must come from authoritative policy
- Rendered content must use an approved version and only allowed recipient-scoped data
- One deduplication key must not create repeated recipient-visible messages
- Provider acceptance must not be mistaken for confirmed delivery
- Status changes and callbacks must be correlated and monotonic
- Uncertain outcomes must not trigger blind duplicate sends
- Provider credentials, secrets, destinations, and personal content must remain protected

## Build or change safely
1. Confirm the product decisions before relying on framework or provider defaults.
2. Follow existing authorization, state, storage, logging, monitoring, and test conventions.
3. Bind every action to the authoritative actor, object, version, state, and scope.
4. Enforce permission, current-state, uniqueness, ordering, and time rules at the write.
5. Make retries and replays safe after partial failure and lost responses.
6. Keep downstream inconsistency visible and repairable.
7. Add the core 20 tests.

