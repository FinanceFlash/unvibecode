# Retry and Recovery Guide

## Partial failures
- Message commits but provider submission does not start
- Provider accepts but its response is lost
- Provider reference returns but local attempt update fails
- Message submits but audit or operational event creation fails
- Delivery callback arrives but local status update fails
- Initial failure records but retry handoff cannot be created

## Recovery rules
- Use the business-event deduplication key and local message record as the authoritative send intent.
- Correlate every provider attempt and callback to one message and attempt.
- Do not resend solely because provider acknowledgement is uncertain.
- Separate accepted, delivered, failed, suppressed, expired, and uncertain states.
- Hand retryable failure to the retry workflow once and reconcile missing status asynchronously.

