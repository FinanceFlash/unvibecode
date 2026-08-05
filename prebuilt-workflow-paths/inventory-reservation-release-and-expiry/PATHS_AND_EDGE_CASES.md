# Paths and Edge Cases

## Supported paths
- Single-item reservation
- Atomic multi-line reservation
- Partial allocation where explicitly supported
- Backorder or unavailable rejection
- Reservation extension
- Conversion to committed inventory
- Cancellation, release, and expiry
- Multi-location allocation, reconciliation, and manual repair

## Normal paths
- Available quantity is reserved once for the intended order
- A valid reservation converts once when the order commits to fulfilment
- Cancellation or expiry releases the exact unused quantity once

## Denied paths
- Item, variant, location, order, owner, or quantity is missing or invalid
- Available inventory is insufficient under policy
- Reservation is expired, released, consumed, cancelled, or owned elsewhere
- An extension, release, or conversion violates current state

## Timing, concurrency, and boundaries
- Two customers request the last unit together
- Reservation converts exactly at expiry
- Release, expiry, and conversion arrive together
- Inventory source or location changes during allocation
- A multi-line reservation partially succeeds

Cover valid, invalid, duplicate, expired, stale, replayed, repeated, simultaneous, partially completed, unauthorized, and recovery outcomes.

