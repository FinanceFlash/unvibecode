# Testing Guide

Check authoritative records, financial or inventory changes, permissions, external effects, recovery, and audit—not only responses.

## 1. Available quantity is reserved once

**Given:** An eligible order requests an available item, variant, location, and quantity

**When:** Reservation runs

**Expect:** One active reservation reduces available and increases reserved by the same amount

**Must not happen:** Stock is held twice or quantities do not balance

**Best test levels:** Integration.

## 2. Reservation converts once

**Given:** An active unexpired reservation belongs to an order ready for fulfilment

**When:** Conversion runs

**Expect:** Reserved decreases and committed increases exactly once

**Must not happen:** The same reservation is consumed twice

**Best test levels:** Integration and end-to-end.

## 3. Cancellation releases quantity

**Given:** An active unused reservation belongs to a cancelled demand

**When:** Release runs

**Expect:** Reserved decreases and available increases by the exact held amount

**Must not happen:** More stock is released than held or the hold remains stranded

**Best test levels:** Integration.

## 4. Required reservation data is missing

**Given:** Item, variant, location, owner, order, quantity, unit, or expiry input is absent

**When:** Validation runs

**Expect:** The request fails before quantity changes

**Must not happen:** A blank or unowned hold enters inventory

**Best test levels:** Unit and API.

## 5. Quantity is invalid

**Given:** Quantity is zero, negative, excessive, fractional for an indivisible unit, or overflowing

**When:** Validation and conversion run

**Expect:** Unsafe quantity is rejected

**Must not happen:** Invalid arithmetic changes inventory

**Best test levels:** Unit and property.

## 6. Inventory is insufficient

**Given:** Available quantity is below demand and oversell or partial policy does not allow it

**When:** Reservation runs

**Expect:** The request is rejected or backordered explicitly

**Must not happen:** Inventory becomes negative or a false hold is confirmed

**Best test levels:** Integration.

## 7. Actor cannot control reservation

**Given:** The actor or service lacks ownership of the tenant, order, seller, or inventory scope

**When:** They reserve, extend, release, or convert

**Expect:** Authorization denies the action

**Must not happen:** A reservation identifier grants inventory control

**Best test levels:** Authorization and security.

## 8. Equivalent item or unit representations differ

**Given:** SKU, variant, location, case, unit, or conversion representation varies

**When:** Canonicalization runs

**Expect:** One authoritative identity and unit rule is applied

**Must not happen:** Formatting or unit conversion bypasses availability limits

**Best test levels:** Unit and integration.

## 9. Two customers request last unit

**Given:** Only one unit remains and two reservations execute concurrently

**When:** Both attempt to commit

**Expect:** One reservation wins unless explicit oversell policy permits otherwise

**Must not happen:** Both receive confirmed exclusive stock

**Best test levels:** Concurrency integration.

## 10. Conversion occurs at expiry

**Given:** Convert and expiry are tested immediately before, at, and after the boundary

**When:** Trusted time and current state are checked

**Expect:** One explicit precedence rule consumes or expires

**Must not happen:** Both consumption and release occur

**Best test levels:** Unit with controlled time.

## 11. Reservation response is lost

**Given:** The hold may already be active but the caller sees failure

**When:** The caller retries

**Expect:** The same reservation and quantity state are returned

**Must not happen:** A second hold is created

**Best test levels:** API and integration.

## 12. Reservation operation is replayed

**Given:** A request, release, expiry, or conversion identity already completed

**When:** The operation repeats

**Expect:** It no-ops or returns the authoritative result

**Must not happen:** Quantities change again

**Best test levels:** Integration.

## 13. Scarce inventory is hoarded

**Given:** One actor creates repeated holds without completing orders

**When:** Limits, expiry, and abuse controls run

**Expect:** Hold count and duration are bounded fairly

**Must not happen:** Real customers lose stock indefinitely

**Best test levels:** Security and load.

## 14. Reservation commits but expiry job fails

**Given:** The hold exists without a scheduled release

**When:** Recovery detects it

**Expect:** One expiry mechanism is restored or an explicit exception is visible

**Must not happen:** Stock remains stranded silently

**Best test levels:** Integration and operations.

## 15. Inventory dependency times out

**Given:** The inventory database, cache, warehouse, or external seller returns uncertain outcome

**When:** Failure handling runs

**Expect:** The reservation remains uncertain and reconciliation precedes retry

**Must not happen:** Timeout causes blind duplicate hold or false availability

**Best test levels:** Dependency contract and integration.

## 16. Conversion commits but response is lost

**Given:** Inventory may already be committed to fulfilment

**When:** The order or worker retries conversion

**Expect:** Current state returns the consumed result

**Must not happen:** Committed quantity is deducted again

**Best test levels:** Integration.

## 17. Cross-tenant reservation is referenced

**Given:** A valid actor supplies another tenant's order or reservation

**When:** They release, extend, or convert it

**Expect:** Owner, tenant, item, and order binding deny the action

**Must not happen:** Identifiers cross inventory boundaries

**Best test levels:** Authorization and security.

## 18. Inventory error is logged

**Given:** The path contains customer, order, seller, location, operational, and adjustment data

**When:** An error occurs

**Expect:** Diagnostics avoid sensitive business data and privileged adjustment details

**Must not happen:** Protected records or control tokens reach logs

**Best test levels:** Security and log inspection.

## 19. Late expiry follows conversion

**Given:** A stale expiry or release job arrives after the reservation was consumed

**When:** The worker processes it

**Expect:** Current state makes the job obsolete

**Must not happen:** Committed inventory returns to available

**Best test levels:** Worker integration.

## 20. Multi-line reservation partially fails

**Given:** Some items reserve before another line fails

**When:** Atomicity or compensation runs

**Expect:** All lines roll back or explicit partial policy and quantities are recorded

**Must not happen:** Invisible partial holds strand stock or confirm unavailable items

**Best test levels:** Integration and operations.

