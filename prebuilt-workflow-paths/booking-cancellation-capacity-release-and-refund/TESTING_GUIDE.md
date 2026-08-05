# Testing Guide

Check authoritative records, capacity or financial changes, permissions, external effects, recovery, and audit—not only responses.

## 1. Eligible cancellation releases capacity

**Given:** An authorized actor cancels a confirmed unused booking within policy

**When:** Cancellation runs

**Expect:** The booking becomes cancelled and exact capacity is released once

**Must not happen:** The booking stays active or too much capacity is released

**Best test levels:** Integration and end-to-end.

## 2. Refund request is created once

**Given:** The authoritative cancellation is refund eligible with a payment reference

**When:** Refund handoff runs

**Expect:** One request records the correct amount basis and reason

**Must not happen:** Refund requests duplicate or use another payment

**Best test levels:** Integration.

## 3. Waitlist and notifications follow cancellation

**Given:** A cancelled slot can serve a waitlist and policy requires messages

**When:** Downstream handoff runs

**Expect:** The same cancellation drives one waitlist and communication outcome

**Must not happen:** Promotion occurs without capacity or messages contradict booking state

**Best test levels:** Integration.

## 4. Required cancellation data is missing

**Given:** Booking, actor, reason, version, or required reference is absent

**When:** Validation runs

**Expect:** The request fails before booking or capacity changes

**Must not happen:** An unowned cancellation enters operations

**Best test levels:** Unit and API.

## 5. Cancellation input is malformed

**Given:** Reason, date, timezone, identifier, version, or payload size is invalid

**When:** Validation runs

**Expect:** Unsafe input is rejected

**Must not happen:** Malformed data reaches refund, provider, waitlist, or logs

**Best test levels:** Unit, API, and security.

## 6. Booking is outside policy

**Given:** The cut-off passed or booking is completed, checked in, no-show, cancelled, or superseded

**When:** Cancellation runs

**Expect:** Current policy denies or routes an explicit exception

**Must not happen:** A stale request releases completed capacity

**Best test levels:** Integration.

## 7. Actor cannot cancel booking

**Given:** The user lacks ownership or administrator permission for the booking or tenant

**When:** They cancel

**Expect:** Authorization denies the action

**Must not happen:** A booking identifier grants destructive control

**Best test levels:** Authorization and security.

## 8. Cancellation policy crosses timezone

**Given:** Booking and requester timezones differ or daylight-saving changes the local cut-off

**When:** Eligibility is calculated

**Expect:** One canonical instant and documented local-time rule apply

**Must not happen:** The customer is charged or denied by inconsistent clocks

**Best test levels:** Unit with controlled timezone.

## 9. Cancel races with check-in or reschedule

**Given:** Cancellation, check-in, completion, or reschedule targets the same booking concurrently

**When:** Actions execute

**Expect:** One explicit transition precedence determines state and effects

**Must not happen:** Capacity is both consumed and released

**Best test levels:** Concurrency integration.

## 10. Request arrives at cut-off

**Given:** Cancellation is submitted immediately before, at, and after the policy boundary

**When:** Trusted server time is checked

**Expect:** One explicit fee and eligibility boundary applies

**Must not happen:** Latency or client time changes the outcome unpredictably

**Best test levels:** Unit with controlled time.

## 11. Cancellation response is lost

**Given:** Cancellation may already be effective but the client sees failure

**When:** The client retries

**Expect:** The same cancellation and effects are returned

**Must not happen:** Capacity, refund, or notification repeats

**Best test levels:** API and integration.

## 12. Cancellation operation is replayed

**Given:** The same request or event already completed

**When:** It is submitted again

**Expect:** It no-ops or returns the authoritative result

**Must not happen:** Booking and financial effects run again

**Best test levels:** Integration.

## 13. Cancellation is abused

**Given:** One actor repeatedly cancels scarce bookings or triggers costly downstream work

**When:** Limits and abuse controls run

**Expect:** Activity is bounded and suspicious patterns are visible

**Must not happen:** Capacity gaming, refund abuse, or message cost grows unchecked

**Best test levels:** Security and load.

## 14. Cancellation commits but release fails

**Given:** The booking is cancelled while capacity remains committed

**When:** Recovery runs

**Expect:** Exact capacity is released once or an exception blocks reuse visibly

**Must not happen:** Inventory is stranded silently

**Best test levels:** Integration and operations.

## 15. Provider cancellation times out

**Given:** The external provider returns uncertain cancellation status

**When:** Failure handling runs

**Expect:** The local outcome follows explicit policy and reconciliation precedes duplicate calls

**Must not happen:** Uncertainty becomes false success or repeated provider cancellation

**Best test levels:** Provider contract and integration.

## 16. Cancellation commits but response is lost

**Given:** Booking, capacity, refund, and provider effects may already exist

**When:** The operation repeats

**Expect:** Current state returns one cancellation outcome

**Must not happen:** Downstream effects duplicate

**Best test levels:** Integration.

## 17. Cross-tenant booking is referenced

**Given:** A valid actor supplies a booking or payment from another tenant

**When:** Cancellation runs

**Expect:** Ownership and tenant binding deny the action

**Must not happen:** Identifiers cross customer or provider boundaries

**Best test levels:** Authorization and security.

## 18. Cancellation error is logged

**Given:** The path contains customer, schedule, reason, payment, and provider data

**When:** An error occurs

**Expect:** Diagnostics avoid secrets and unnecessary personal data

**Must not happen:** Protected cancellation details enter unsafe logs

**Best test levels:** Security and log inspection.

## 19. Late provider completion follows cancellation

**Given:** A delayed check-in, completion, or provider-confirmed event arrives after cancellation

**When:** Reconciliation runs

**Expect:** Written precedence protects capacity, service, payment, and customer outcome

**Must not happen:** The booking becomes both cancelled and completed without review

**Best test levels:** Integration.

## 20. Refund handoff fails

**Given:** Cancellation and capacity release succeed but refund request, waitlist, or notification fails

**When:** Repair runs

**Expect:** Missing effects complete once without reverting cancellation

**Must not happen:** Customer money or communication remains silently wrong

**Best test levels:** Integration and operations.

