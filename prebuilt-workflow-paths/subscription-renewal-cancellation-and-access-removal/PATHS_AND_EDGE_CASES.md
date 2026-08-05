# Paths and Edge Cases

## Supported paths
- Automatic successful renewal
- Failed renewal entering past due or grace
- Period-end cancellation
- Immediate cancellation where allowed
- Cancellation reversal before effective time
- Reactivation after cancellation or termination
- Payment retry or recovery handoff
- Entitlement release, reconciliation, and manual repair

## Normal paths
- A due eligible subscription renews once and extends its period and access
- A period-end cancellation preserves access until the boundary then releases it once
- An allowed immediate cancellation terminates access and records its business consequences

## Denied paths
- Subscription, plan, period, price, payer, or effective date is missing or invalid
- The subscription is already cancelled, terminated, ineligible, or owned elsewhere
- An unauthorized actor requests cancellation, reversal, or renewal
- A stale renewal or cancellation targets a newer subscription version

## Timing, concurrency, and boundaries
- Renewal and cancellation execute together
- Payment succeeds exactly at the period or grace boundary
- Timezone, leap date, month length, or daylight-saving changes affect dates
- Cancellation response is lost and repeated
- Late payment or provider callback arrives after termination

Cover valid, invalid, duplicate, expired, stale, replayed, repeated, simultaneous, partially completed, unauthorized, and recovery outcomes.

