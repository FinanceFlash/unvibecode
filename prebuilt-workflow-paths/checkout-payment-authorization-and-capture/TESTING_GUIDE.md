# Testing Guide

Check authoritative records, financial or inventory changes, permissions, external effects, recovery, and audit—not only responses.

## 1. Valid checkout is captured once

**Given:** An eligible checkout has an authoritative amount, currency, payer, and payment method

**When:** Payment runs

**Expect:** One attempt is captured for the correct amount and the order records the same result

**Must not happen:** The customer is charged twice or for a different amount

**Best test levels:** Integration and end-to-end.

## 2. Authorization is captured before expiry

**Given:** A valid active authorization exists for the same order and amount

**When:** Capture is requested

**Expect:** The authorization becomes captured once and the order-payment state advances

**Must not happen:** A new authorization or duplicate capture is created

**Best test levels:** Provider integration.

## 3. Customer authentication resumes payment

**Given:** The provider requires a valid customer challenge for an existing attempt

**When:** The customer completes it

**Expect:** The same attempt resumes and reaches its allowed outcome

**Must not happen:** A second attempt or wrong customer session is used

**Best test levels:** End-to-end and security.

## 4. Required payment input is missing

**Given:** The checkout lacks order, payer, amount, currency, or required method reference

**When:** Payment is requested

**Expect:** Validation fails before provider action

**Must not happen:** A guessed or zero-value provider request is sent

**Best test levels:** Unit and API.

## 5. Amount or currency is malformed

**Given:** The amount is negative, excessive, imprecise, overflowing, or uses invalid currency units

**When:** Validation and conversion run

**Expect:** The request is rejected safely

**Must not happen:** Rounding or conversion silently changes the charge

**Best test levels:** Unit and property.

## 6. Provider declines payment

**Given:** The provider or fraud service returns a valid decline

**When:** The result is processed

**Expect:** The attempt and order record a decline without capture or fulfilment

**Must not happen:** The decline is reported as success or retried blindly

**Best test levels:** Provider contract and integration.

## 7. Actor cannot pay for order

**Given:** The authenticated actor lacks access to the checkout or tenant

**When:** They submit payment or capture

**Expect:** Ownership and scope checks deny the action

**Must not happen:** An order identifier permits cross-account payment control

**Best test levels:** Authorization and security.

## 8. Minor-unit boundary is calculated

**Given:** A currency with zero, two, or three decimal minor units reaches a rounding boundary

**When:** The provider amount is built

**Expect:** One documented rounding rule matches checkout, provider, ledger, and receipt

**Must not happen:** Different services charge or record different totals

**Best test levels:** Unit and integration.

## 9. Two payments arrive together

**Given:** Two valid requests target the same payable checkout concurrently

**When:** Both execute

**Expect:** Uniqueness and idempotency allow one permitted payment outcome

**Must not happen:** Both attempts capture before order state changes

**Best test levels:** Concurrency integration.

## 10. Authorization expires at boundary

**Given:** Capture is attempted immediately before, at, and after authorization expiry

**When:** Trusted time and provider state are checked

**Expect:** One explicit boundary rule is applied

**Must not happen:** Clock differences extend or shorten validity unpredictably

**Best test levels:** Unit with controlled time.

## 11. Payment response is lost

**Given:** The provider action may have succeeded but the client sees no result

**When:** The client retries

**Expect:** The same attempt and authoritative outcome are returned

**Must not happen:** Retry creates another charge

**Best test levels:** API and integration.

## 12. Idempotency key is replayed with changed payload

**Given:** A used key is submitted with another amount, currency, order, or payer

**When:** Payment runs

**Expect:** The mismatch is rejected without provider action

**Must not happen:** The old key authorizes a different payment

**Best test levels:** Security and integration.

## 13. Payment attempts are flooded

**Given:** One source makes repeated payment or card-verification attempts

**When:** Velocity and abuse limits are reached

**Expect:** Further activity is bounded and legitimate recovery remains possible

**Must not happen:** Card testing, provider cost, or account harm grows unchecked

**Best test levels:** Security and load.

## 14. Authorization succeeds but local write fails

**Given:** The provider authorized while the local attempt remains incomplete

**When:** Recovery runs

**Expect:** Provider status repairs the same attempt or voids it by policy

**Must not happen:** A second authorization is created blindly

**Best test levels:** Integration.

## 15. Provider times out uncertainly

**Given:** The authorization or capture call returns no reliable outcome

**When:** Failure handling runs

**Expect:** The attempt remains uncertain pending lookup, callback, or reconciliation

**Must not happen:** Timeout is treated as decline and immediately retried

**Best test levels:** Provider contract and integration.
**Example test:** Stub the provider so the authorization request receives no reliable outcome. Verify that the payment attempt remains in an uncertain or pending state and that no second authorization is sent until provider status or reconciliation resolves the outcome.

## 16. Capture succeeds but response is lost

**Given:** The provider captured while the caller received failure

**When:** The request repeats or status is queried

**Expect:** The original capture is found and returned once

**Must not happen:** A second capture or contradictory order status is created

**Best test levels:** Integration.

## 17. Cross-tenant order reference is supplied

**Given:** A valid payment actor submits an order or attempt from another tenant

**When:** Payment is requested

**Expect:** Tenant, merchant, payer, and order binding deny the action

**Must not happen:** Identifiers cross the financial boundary

**Best test levels:** Authorization and security.

## 18. Payment error is logged

**Given:** The path contains method tokens, customer data, provider responses, and credentials

**When:** An error occurs

**Expect:** Diagnostics remain useful without sensitive authentication or payment data

**Must not happen:** Tokens, secrets, or prohibited card data enter logs

**Best test levels:** Security and log inspection.

## 19. Late capture follows cancellation

**Given:** The order or authorization was cancelled, voided, expired, or already captured

**When:** A delayed capture command arrives

**Expect:** Current local and provider state block or escalate it

**Must not happen:** A stale command charges a cancelled order

**Best test levels:** Integration.

## 20. Capture succeeds but order update fails

**Given:** Money is captured while order, ledger, fulfilment, or receipt update fails

**When:** Reconciliation runs

**Expect:** All systems converge without another charge

**Must not happen:** The customer pays without order value or financial trace

**Best test levels:** Integration and operations.

