# Paths and Edge Cases

## Supported paths
- Customer self-service cancellation
- Provider or administrator cancellation
- Cancellation before free cut-off
- Cancellation with fee or no refund
- Provider-approval cancellation
- Capacity release and waitlist promotion
- Refund-request handoff
- Provider uncertainty, compensation, reconciliation, and manual review

## Normal paths
- An eligible cancellation changes the booking once and releases exact unused capacity
- A refund-eligible cancellation creates one refund request with the correct basis
- Provider and customer notifications and waitlist handoff reflect the same cancellation

## Denied paths
- Booking, actor, reason, status, or required cancellation data is missing or invalid
- Cancellation is outside the allowed cut-off or the service already started or completed
- The actor cannot cancel the booking
- The booking is already cancelled, rescheduled, refunded, or owned elsewhere

## Timing, concurrency, and boundaries
- Cancellation races with reschedule, check-in, completion, or provider acceptance
- Request arrives exactly at the cancellation cut-off
- Two actors cancel the same booking together
- Provider cancellation succeeds but the local response is lost
- Late provider or payment events arrive after cancellation

Cover valid, invalid, duplicate, expired, stale, replayed, repeated, simultaneous, partially completed, unauthorized, and recovery outcomes.

