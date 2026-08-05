# Product and Business Guide

## Boundary
Starts when a validated checkout has an authoritative payable amount. Ends when payment is declined, requires further customer action, is authorized or captured once, or remains explicitly uncertain with the order, ledger, and customer outcome recorded consistently.

## People and systems
- Customer or authorized payer
- Merchant checkout and order service
- Payment orchestration service
- Payment provider, acquirer, or wallet
- Fraud, authentication, or 3-D Secure service
- Ledger, finance, fulfilment, and notification services
- Support, security, and operations teams

## Things created or changed
- Checkout and order
- Authoritative amount, currency, tax, discount, and minor-unit representation
- Payment attempt and idempotency key
- Provider request and provider payment reference
- Customer-authentication challenge
- Authorization, capture, void, and decline
- Order-payment state, ledger entry, receipt, and audit record

## Stages
- Payment attempt: created → requires action, authorized, captured, declined, cancelled, expired, failed, or uncertain
- Authorization: absent → active → captured, voided, expired, or partially captured if supported
- Order: awaiting payment → paid, payment failed, cancelled, or payment uncertain
- Financial record: pending → posted, reversed, or exception

## Product decisions
- Immediate capture versus separate authorization and capture
- Authoritative amount, currency, minor-unit, rounding, tax, and discount source
- Who may pay for which checkout or order
- Payment-attempt and provider idempotency policy
- Fraud, velocity, step-up, wallet, and 3-D Secure requirements
- Authorization lifetime, partial capture, incremental capture, and void policy
- Provider success, decline, timeout, and uncertain-outcome meanings
- Whether order commitment precedes, follows, or is atomic with payment
- Ledger, receipt, fulfilment, and customer-notification timing
- Attempt limits, card-testing controls, privacy, monitoring, and manual review

## Happy paths
- A valid checkout is captured once for the authoritative amount and currency
- A separate authorization is captured once before expiry
- Required customer authentication completes and resumes the same payment attempt

## Negative paths
- Order, payer, amount, currency, or payment data is missing or invalid
- Provider or fraud controls decline the payment
- The actor cannot access or pay for the checkout
- Authorization is expired, voided, already captured, or belongs elsewhere

## Edge cases
- Two checkout submissions or captures arrive together
- Authorization or customer challenge completes exactly at expiry
- Currency rounding and minor-unit rules produce boundary amounts
- Provider succeeds but the response is lost
- Order cancellation overlaps authorization or capture

## Acceptance criteria
1. Only an eligible payable checkout may start payment
2. Amount, currency, payer, merchant, order, and tenant must bind to one payment attempt
3. Provider and local idempotency must prevent duplicate authorization or capture
4. Customer authentication and fraud decisions must bind the same attempt
5. Declined, expired, voided, cancelled, or captured attempts cannot be captured again
6. Order, payment, ledger, fulfilment, and receipt states must not report contradictory outcomes
7. Provider acceptance and final settlement meanings must remain distinct
8. Uncertain outcomes must be reconciled before unsafe retry
9. Payment credentials, tokens, personal data, and provider secrets must remain protected
10. Every financial state change must be auditable and repairable

## Business risks
| Risk | Business consequence |
|---|---|
| Duplicate charge | Concurrent requests, retries, or lost responses capture payment more than once |
| Wrong amount or currency | The provider charge differs from the authoritative checkout |
| Payment–order divergence | Money moves but the order, entitlement, fulfilment, or ledger does not |
| False success | A decline, timeout, authorization, or pending state is shown as captured |
| Unauthorized payment action | Another account or tenant controls the order or capture |
| Stale authorization | Expired, voided, cancelled, or previously captured authorization is reused |
| Card-testing or cost abuse | Automated attempts create fraud, provider fees, or customer harm |
| Secret or personal-data exposure | Payment data, tokens, provider responses, or credentials reach unsafe logs |

