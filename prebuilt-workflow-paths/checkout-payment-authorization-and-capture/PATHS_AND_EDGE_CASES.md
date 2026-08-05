# Paths and Edge Cases

## Supported paths
- Immediate authorization and capture
- Separate authorization followed by capture
- Customer authentication or 3-D Secure challenge
- Wallet or provider redirect and return
- Decline, cancellation, void, and authorization expiry
- Partial capture where explicitly supported
- Provider timeout, uncertain result, status lookup, and reconciliation
- Order and ledger repair after partial failure

## Normal paths
- A valid checkout is captured once for the authoritative amount and currency
- A separate authorization is captured once before expiry
- Required customer authentication completes and resumes the same payment attempt

## Denied paths
- Order, payer, amount, currency, or payment data is missing or invalid
- Provider or fraud controls decline the payment
- The actor cannot access or pay for the checkout
- Authorization is expired, voided, already captured, or belongs elsewhere

## Timing, concurrency, and boundaries
- Two checkout submissions or captures arrive together
- Authorization or customer challenge completes exactly at expiry
- Currency rounding and minor-unit rules produce boundary amounts
- Provider succeeds but the response is lost
- Order cancellation overlaps authorization or capture

Cover valid, invalid, duplicate, expired, stale, replayed, repeated, simultaneous, partially completed, unauthorized, and recovery outcomes.

