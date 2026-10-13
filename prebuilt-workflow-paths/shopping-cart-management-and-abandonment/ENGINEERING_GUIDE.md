# Engineering Guide

## Tracing the boundary
- **Start:** HTTP POST `/cart/items` or `/guest/cart` to add an item.
- **End:** HTTP POST `/checkout/convert` to convert the cart to an order, or scheduled job reaping expired carts.

## State and sequence
1. **Creation:** A unique session ID is generated for guest carts or linked to the user ID for authenticated carts.
2. **Modification:** Line items are upserted. Quantities are validated against limits.
3. **Calculation:** Subtotal, discounts, and estimated taxes are recalculated synchronously or asynchronously.
4. **Merge:** On POST `/auth/login`, the guest session ID is read, and its line items are merged into the user's primary cart.
5. **Abandonment:** A scheduled job identifies carts inactive for X hours that have not been converted, and queues reminder notifications.

## Engineering safeguards
- **Idempotency:** Item additions and quantity updates must handle retries safely without duplicating items.
- **Concurrency:** Optimistic locking or database constraints must prevent race conditions during cart updates.
- **Session Security:** Guest cart IDs must be cryptographically secure and unguessable to prevent cart hijacking.
- **Data Integrity:** Prices should not be stored statically in the cart; they must be re-fetched or validated against the catalog before checkout.

## Edge cases in code
- The guest cart contains an item that the user already has in their saved cart; the merge logic must resolve the quantity (e.g., sum them or take the max).
- An item is deleted from the catalog while it is still in a user's cart.
- The cart abandonment worker crashes halfway through sending reminders.
