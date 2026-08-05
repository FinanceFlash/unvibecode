# Testing Guide

Check authoritative records, capacity or financial changes, permissions, external effects, recovery, and audit—not only responses.

## 1. Active hold confirms one booking

**Given:** An eligible customer has a valid hold for the intended resource, slot, and capacity

**When:** Confirmation runs

**Expect:** One booking is committed and the hold converts once

**Must not happen:** The hold creates duplicate bookings or capacity deductions

**Best test levels:** Integration and end-to-end.

## 2. Direct booking commits available capacity

**Given:** Policy permits direct booking and sufficient capacity is authoritative

**When:** The request commits

**Expect:** One booking and one capacity movement are recorded

**Must not happen:** Capacity is oversold or reserved without a booking

**Best test levels:** Integration.

## 3. Provider calendar binds same booking

**Given:** A confirmed booking requires an external provider reservation

**When:** Provider acceptance is processed

**Expect:** The external reference attaches to the same booking and slot

**Must not happen:** Another booking or slot receives the reference

**Best test levels:** Provider integration.

## 4. Required booking data is missing

**Given:** Customer, provider, resource, slot, timezone, party size, terms, hold, or payment reference is absent

**When:** Validation runs

**Expect:** The request fails before booking or capacity changes

**Must not happen:** An incomplete booking enters operations

**Best test levels:** Unit and API.

## 5. Slot or party data is malformed

**Given:** Time, timezone, duration, quantity, identifier, encoding, or payload size is invalid

**When:** Validation runs

**Expect:** Unsafe input is rejected

**Must not happen:** Invalid values reach capacity, payment, calendar, or logs

**Best test levels:** Unit, API, and security.

## 6. Hold or capacity is no longer valid

**Given:** The hold expired, was released, belongs elsewhere, or capacity changed

**When:** Confirmation runs

**Expect:** Current state rejects or explicitly revalidates the request

**Must not happen:** Stale capacity is silently committed

**Best test levels:** Integration.

## 7. Actor cannot create booking

**Given:** The user lacks access to the customer, tenant, provider, resource, or attendee

**When:** They confirm

**Expect:** Ownership and permission checks deny the action

**Must not happen:** A hold or resource identifier grants cross-account control

**Best test levels:** Authorization and security.

## 8. Timezone crosses calendar boundary

**Given:** The requested slot crosses midnight, daylight-saving, or provider/customer timezone conversion

**When:** Slot resolution runs

**Expect:** One canonical instant and local display policy are used

**Must not happen:** The provider and customer reserve different times

**Best test levels:** Unit with controlled timezone.

## 9. Two customers request last capacity

**Given:** Two confirmations compete for one remaining unit

**When:** Both execute

**Expect:** One wins unless explicit overbooking policy allows otherwise

**Must not happen:** Both receive exclusive confirmed capacity

**Best test levels:** Concurrency integration.

## 10. Hold converts at expiry boundary

**Given:** Confirmation runs immediately before, at, and after hold expiry

**When:** Trusted time and current state are checked

**Expect:** One explicit boundary rule confirms or rejects

**Must not happen:** Both expiry and conversion change capacity

**Best test levels:** Unit with controlled time.

## 11. Confirmation response is lost

**Given:** The booking may have committed but the customer sees no result

**When:** The client retries

**Expect:** The same booking and confirmation state are returned

**Must not happen:** A second booking is created

**Best test levels:** API and integration.

## 12. Idempotency key is replayed with changed slot

**Given:** A used key is submitted with another customer, resource, slot, or party size

**When:** Confirmation runs

**Expect:** The mismatch is rejected

**Must not happen:** The old key mutates or creates a different booking

**Best test levels:** Security and integration.

## 13. Booking attempts are flooded

**Given:** One actor creates repeated holds or confirmations for scarce capacity

**When:** Rate and abuse limits are reached

**Expect:** Activity is bounded without blocking legitimate recovery

**Must not happen:** Capacity hoarding or provider cost grows unchecked

**Best test levels:** Security and load.

## 14. Booking commits but capacity update fails

**Given:** The booking exists while capacity remains uncommitted

**When:** Recovery runs

**Expect:** The booking stays pending or is compensated visibly

**Must not happen:** The customer is confirmed without capacity

**Best test levels:** Integration.

## 15. External provider times out

**Given:** The provider calendar or reservation API returns uncertain status

**When:** Failure handling runs

**Expect:** The booking remains explicit and reconciliation precedes duplicate submission

**Must not happen:** Timeout becomes false rejection or duplicate provider booking

**Best test levels:** Provider contract and integration.

## 16. Booking commits but response is lost

**Given:** Booking, capacity, payment, and provider effects may already exist

**When:** The operation repeats

**Expect:** Current state returns one booking outcome

**Must not happen:** Confirmation and downstream effects repeat

**Best test levels:** Integration.

## 17. Cross-tenant resource is referenced

**Given:** A valid actor supplies a resource, hold, or provider from another tenant

**When:** Confirmation runs

**Expect:** Tenant and ownership binding deny the request

**Must not happen:** Identifiers cross booking boundaries

**Best test levels:** Authorization and security.

## 18. Booking failure is logged

**Given:** The path contains customer, attendee, schedule, contact, payment, and provider data

**When:** An error occurs

**Expect:** Diagnostics avoid secrets and unnecessary personal data

**Must not happen:** Protected booking details enter unsafe logs

**Best test levels:** Security and log inspection.

## 19. Late provider rejection follows confirmation

**Given:** The provider later rejects or invalidates a locally confirmed slot

**When:** Reconciliation runs

**Expect:** Customer, capacity, payment, and support outcomes follow explicit exception policy

**Must not happen:** The system stays falsely confirmed or silently loses the booking

**Best test levels:** Integration.

## 20. Confirmation or reminder fails

**Given:** The booking is valid but calendar sync, reminder, receipt, or customer message fails

**When:** Repair runs

**Expect:** The missing effect completes once and booking truth remains clear

**Must not happen:** The booking duplicates or the customer is misled

**Best test levels:** Integration and operations.

