# Testing Guide

Check authoritative records, financial or inventory changes, permissions, external effects, recovery, and audit—not only responses.

## 1. Valid checkout creates one order

**Given:** An eligible checkout has authoritative customer, item, total, address, terms, payment, and inventory state

**When:** Order placement runs

**Expect:** One immutable order is committed and confirmed according to policy

**Must not happen:** The checkout creates duplicate orders or different accepted values

**Best test levels:** Integration and end-to-end.

## 2. Order preserves accepted snapshot

**Given:** A ready checkout contains item, seller, quantity, price, discount, tax, shipping, currency, and address

**When:** The order commits

**Expect:** The order stores the exact reproducible accepted snapshot

**Must not happen:** Later catalog or profile data silently rewrites it

**Best test levels:** Integration.

## 3. Downstream references bind same order

**Given:** Payment, reservation, fulfilment, and confirmation prerequisites succeed

**When:** The order finalizes

**Expect:** All references point to the one committed order and customer

**Must not happen:** An effect attaches to another order or tenant

**Best test levels:** Integration.

## 4. Required checkout data is missing

**Given:** Customer or guest, item, quantity, price, currency, address, terms, or required reference is absent

**When:** Placement validation runs

**Expect:** The request fails before order commit

**Must not happen:** An incomplete order enters operations

**Best test levels:** Unit and API.

## 5. Checkout value is malformed

**Given:** Quantity, amount, address, currency, encoding, identifier, or payload size is invalid

**When:** Validation runs

**Expect:** Unsafe input is rejected

**Must not happen:** Malformed values reach payment, inventory, fulfilment, or logs

**Best test levels:** Unit, API, and security.

## 6. Quote or hold is stale

**Given:** The price, promotion, inventory hold, terms, or checkout version expired or changed

**When:** Order placement runs

**Expect:** The checkout is rejected or explicitly revalidated under policy

**Must not happen:** Stale values are silently committed

**Best test levels:** Integration.

## 7. Actor cannot place order

**Given:** The user lacks access to the checkout, account, tenant, seller, region, or product

**When:** They submit placement

**Expect:** Ownership and eligibility checks deny it

**Must not happen:** A checkout identifier grants purchase control

**Best test levels:** Authorization and security.

## 8. Totals reach rounding boundary

**Given:** Line, discount, tax, shipping, and minor-unit calculations reach a boundary

**When:** The order total is verified

**Expect:** One documented rule matches checkout, order, payment, ledger, and receipt

**Must not happen:** Services record different totals

**Best test levels:** Unit and property.

## 9. Two submissions arrive together

**Given:** Two requests target the same ready checkout and key concurrently

**When:** Both execute

**Expect:** Uniqueness produces one order and one set of effects

**Must not happen:** Both commit before checkout conversion is visible

**Best test levels:** Concurrency integration.

## 10. Hold expires during commit

**Given:** Placement occurs immediately before, at, and after quote or reservation expiry

**When:** Trusted time and current state are checked

**Expect:** One explicit boundary rule confirms or rejects

**Must not happen:** Races create an order without valid prerequisites

**Best test levels:** Unit with controlled time.

## 11. Placement response is lost

**Given:** The order may have committed but the client sees no result

**When:** The client retries

**Expect:** The same order and confirmation state are returned

**Must not happen:** A duplicate order is created

**Best test levels:** API and integration.

## 12. Key is replayed with changed checkout

**Given:** A used idempotency key is submitted with different items, total, address, or customer

**When:** Placement runs

**Expect:** The mismatch is rejected

**Must not happen:** The old key mutates or creates a different order

**Best test levels:** Security and integration.

## 13. Order creation is flooded

**Given:** One actor generates repeated placements or expensive validations

**When:** Velocity and abuse limits are reached

**Expect:** Activity is bounded without breaking legitimate recovery

**Must not happen:** Order, payment, inventory, or provider load grows unchecked

**Best test levels:** Security and load.

## 14. Order commits but payment handoff fails

**Given:** The order exists but required payment reference or command is absent

**When:** Recovery runs

**Expect:** The order remains visibly pending or is compensated under policy

**Must not happen:** The order confirms without payment or charges twice

**Best test levels:** Integration.

## 15. Dependency times out

**Given:** Payment, inventory, pricing, tax, address, or fraud service returns uncertain status

**When:** Placement handles the result

**Expect:** The order remains denied, pending, or uncertain by explicit policy

**Must not happen:** Uncertainty becomes false confirmation

**Best test levels:** Dependency contract and integration.

## 16. Order commits but response is lost

**Given:** The transaction and effects may already exist

**When:** The request repeats

**Expect:** Current state returns the single order outcome

**Must not happen:** Order number, payment, reservation, or confirmation repeats

**Best test levels:** Integration.

## 17. Cross-tenant checkout is referenced

**Given:** A valid actor submits another tenant's checkout, customer, or destination

**When:** Placement runs

**Expect:** Ownership and tenant binding deny the request

**Must not happen:** Identifiers cross account or tenant boundaries

**Best test levels:** Authorization and security.

## 18. Order failure is logged

**Given:** The path contains address, contact, items, prices, tokens, and internal decisions

**When:** An error occurs

**Expect:** Diagnostics avoid secrets and unnecessary personal data

**Must not happen:** Full customer or payment information enters unsafe logs

**Best test levels:** Security and log inspection.

## 19. Late prerequisite follows rejection

**Given:** A payment or inventory result arrives after checkout expiry, order rejection, or cancellation

**When:** Reconciliation runs

**Expect:** Written policy links, reverses, releases, or escalates safely

**Must not happen:** A stale result creates an unexpected confirmed order

**Best test levels:** Integration.

## 20. Confirmation or fulfilment fails

**Given:** The order is committed but confirmation, receipt, ledger, or fulfilment handoff fails

**When:** Repair runs

**Expect:** The missing effect is completed once and customer state stays truthful

**Must not happen:** The customer is told nothing or downstream work duplicates

**Best test levels:** Integration and operations.

