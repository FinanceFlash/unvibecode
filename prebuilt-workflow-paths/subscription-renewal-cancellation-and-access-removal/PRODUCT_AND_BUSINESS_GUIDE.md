# Product and Business Guide

## Boundary
Starts at an automatic renewal boundary or an authorized cancellation request. Ends when the subscription is renewed, enters an explicit past-due or grace state, is scheduled to cancel, terminates, or is restored with billing and product access reconciled.

## People and systems
- Subscriber or authorized account administrator
- Subscription and billing scheduler
- Payment orchestration and provider
- Plan, pricing, tax, and invoice services
- Entitlement, access, and session services
- Notification and customer-support teams
- Finance, security, and operations teams

## Things created or changed
- Subscription and plan
- Billing period, renewal date, cancellation date, and trusted clock
- Renewal attempt, invoice, payment, and provider reference
- Cancellation request, reason, effective date, and reversal
- Past-due and grace-period state
- Entitlement, seat, feature access, session, and data-retention outcome
- Notification and audit record

## Stages
- Subscription: active → renewal due → renewing → active, past due, grace, cancellation scheduled, cancelled, or terminated
- Cancellation: absent → requested → scheduled or immediate → effective, reversed, or denied
- Entitlement: active → grace or restricted → released, retained, or restored
- Renewal attempt: due → processing → paid, failed, uncertain, or exhausted

## Product decisions
- Automatic-renewal eligibility and required advance notice
- Authoritative billing timezone, date, period start, and period end
- Immediate versus period-end cancellation
- Grace length, product access, payment retry, and dunning handoff
- Which cancellation or renewal actions require owner or administrator permission
- Price, tax, currency, invoice, and payment-method source at renewal
- Entitlement, seat, API key, data, export, and session behavior at termination
- Cancellation reversal and reactivation rules
- Provider cancellation and local subscription status precedence
- Rate, abuse, audit, notification, retention, and support policy

## Happy paths
- A due eligible subscription renews once and extends its period and access
- A period-end cancellation preserves access until the boundary then releases it once
- An allowed immediate cancellation terminates access and records its business consequences

## Negative paths
- Subscription, plan, period, price, payer, or effective date is missing or invalid
- The subscription is already cancelled, terminated, ineligible, or owned elsewhere
- An unauthorized actor requests cancellation, reversal, or renewal
- A stale renewal or cancellation targets a newer subscription version

## Edge cases
- Renewal and cancellation execute together
- Payment succeeds exactly at the period or grace boundary
- Timezone, leap date, month length, or daylight-saving changes affect dates
- Cancellation response is lost and repeated
- Late payment or provider callback arrives after termination

## Acceptance criteria
1. Only an eligible current subscription may renew or cancel
2. Actor, account, tenant, plan, period, price, currency, and payment must bind to the subscription
3. One billing period must not renew or charge more than once
4. Cancellation effective time and access consequences must be explicit
5. Renewal, cancellation, grace, termination, and reactivation must use trusted current state
6. Payment, invoice, subscription, entitlement, session, and provider states must converge
7. Expired or terminated access must not remain available accidentally
8. Paid active customers must not lose access through partial failure
9. Repeated or simultaneous actions must not duplicate charges or release effects
10. Billing data, payment references, cancellation reasons, and personal data must remain protected

## Business risks
| Risk | Business consequence |
|---|---|
| Duplicate renewal charge | Scheduler replay or concurrency bills one period more than once |
| Premature access loss | Cancellation or partial failure removes paid entitlement too early |
| Free continued access | Termination fails to release entitlement, seats, keys, or sessions |
| Billing–access divergence | Payment, invoice, subscription, and entitlement disagree |
| Unauthorized cancellation | Another user or tenant terminates a paid subscription |
| Missed renewal | A valid due subscription is skipped or silently stranded |
| Hidden or ineffective cancellation | The customer believes renewal stopped but billing continues |
| Sensitive-data exposure | Billing, payment, cancellation, or account data reaches unsafe logs |

