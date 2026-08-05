# Testing Guide

Check authoritative records, financial or inventory changes, permissions, external effects, recovery, and audit—not only responses.

## 1. Due subscription renews once

**Given:** An active eligible subscription reaches its renewal boundary with valid price and payment details

**When:** Renewal runs

**Expect:** One payment succeeds, the period advances once, and access remains active

**Must not happen:** The same period is charged or extended twice

**Best test levels:** Integration and end-to-end.

## 2. Period-end cancellation releases on time

**Given:** An authorized subscriber schedules cancellation at period end

**When:** The effective boundary arrives

**Expect:** The subscription terminates and entitlement releases once after paid access ends

**Must not happen:** Access ends early or billing continues into another period

**Best test levels:** Integration.

## 3. Immediate cancellation follows policy

**Given:** An authorized actor requests an allowed immediate cancellation

**When:** Cancellation runs

**Expect:** Subscription, access, provider schedule, and notification follow the written immediate policy

**Must not happen:** The action silently behaves as period-end or leaves stale access

**Best test levels:** API and integration.

## 4. Required subscription data is missing

**Given:** The action lacks subscription, account, plan, period, price, payer, or effective date

**When:** Validation runs

**Expect:** The request fails before billing or access changes

**Must not happen:** A guessed subscription is charged or terminated

**Best test levels:** Unit and API.

## 5. Period or price is malformed

**Given:** The date, timezone, amount, currency, period length, or version is invalid

**When:** Renewal or cancellation is evaluated

**Expect:** Unsafe input is rejected

**Must not happen:** Invalid dates or amounts reach provider and entitlement systems

**Best test levels:** Unit and property.

## 6. Subscription is ineligible

**Given:** The subscription is cancelled, terminated, paused, not due, or lacks a permitted renewal path

**When:** A renewal job executes

**Expect:** Current state prevents payment

**Must not happen:** A stale job revives or charges an ineligible subscription

**Best test levels:** Worker integration.

## 7. Actor cannot manage subscription

**Given:** The user lacks account-owner, billing-admin, or tenant permission

**When:** They cancel, reverse, reactivate, or manually renew

**Expect:** Authorization denies the action

**Must not happen:** A subscription identifier grants financial control

**Best test levels:** Authorization and security.

## 8. Billing boundary handles calendar rules

**Given:** Renewal spans timezone, month-end, leap date, or daylight-saving changes

**When:** The next period is calculated

**Expect:** One documented billing-calendar rule produces a valid non-overlapping period

**Must not happen:** Periods overlap, gap, or charge on the wrong date

**Best test levels:** Unit with controlled time.

## 9. Renewal and cancellation race

**Given:** A due renewal and authorized cancellation target the same subscription concurrently

**When:** Both execute

**Expect:** One explicit precedence rule determines payment, period, and access

**Must not happen:** The customer is charged after effective cancellation or gets free access

**Best test levels:** Concurrency integration.

## 10. Payment completes at grace boundary

**Given:** Payment succeeds before, at, and after grace expiry

**When:** Trusted time and current state are evaluated

**Expect:** One explicit restore or termination rule applies

**Must not happen:** Races create both active and terminated outcomes

**Best test levels:** Unit with controlled time.

## 11. Cancellation response is lost

**Given:** Cancellation may already be scheduled or effective

**When:** The client repeats the request

**Expect:** The authoritative existing cancellation is returned safely

**Must not happen:** Another cancellation or access release effect is created

**Best test levels:** API and integration.

## 12. Renewal job is replayed

**Given:** The same subscription period already renewed or is processing

**When:** The scheduler delivers the job again

**Expect:** It no-ops or returns the existing period result

**Must not happen:** Payment, invoice, period, or notification repeats

**Best test levels:** Worker integration.

## 13. Renewal or cancellation is flooded

**Given:** One actor or scheduler generates repeated expensive actions

**When:** Rate and abuse limits are reached

**Expect:** Activity is bounded and legitimate recovery remains possible

**Must not happen:** Provider cost, messages, or state contention grows unchecked

**Best test levels:** Security and load.

## 14. Payment succeeds but period update fails

**Given:** The provider captured renewal but local subscription remains due

**When:** Recovery runs

**Expect:** The original payment advances the same period without another charge

**Must not happen:** The customer is charged again or loses access

**Best test levels:** Integration.

## 15. Provider times out during renewal

**Given:** The payment or provider-cancellation call has uncertain outcome

**When:** Failure handling runs

**Expect:** State remains explicit and reconciliation precedes unsafe retry or termination

**Must not happen:** Timeout is treated as final failure or safe success

**Best test levels:** Provider contract and integration.

## 16. Renewal commits but response is lost

**Given:** Payment, invoice, period, and access may already be updated

**When:** The scheduler or client repeats

**Expect:** Current state returns the one renewal result

**Must not happen:** The period, charge, or entitlement extends again

**Best test levels:** Integration.

## 17. Cross-tenant subscription is referenced

**Given:** A valid actor supplies a subscription owned by another tenant

**When:** They renew, cancel, or reactivate it

**Expect:** Ownership and tenant checks deny the action

**Must not happen:** Identifiers cross the billing boundary

**Best test levels:** Authorization and security.

## 18. Billing failure is logged

**Given:** The path contains account, payment, invoice, cancellation, and provider details

**When:** An error occurs

**Expect:** Diagnostics avoid credentials and unnecessary personal or financial data

**Must not happen:** Sensitive billing data reaches logs or alerts

**Best test levels:** Security and log inspection.

## 19. Late payment follows termination

**Given:** A delayed success or callback arrives after cancellation or grace termination

**When:** Reconciliation runs

**Expect:** Written policy restores, refunds, or escalates without duplicate access or charge

**Must not happen:** Stale payment silently reactivates or is ignored while money is kept

**Best test levels:** Integration.

## 20. Entitlement release fails

**Given:** The subscription terminates but features, seats, keys, sessions, or provider schedule do not update

**When:** Repair runs

**Expect:** All access and billing surfaces converge visibly

**Must not happen:** Billing stops while unauthorized free access continues

**Best test levels:** Integration and operations.

