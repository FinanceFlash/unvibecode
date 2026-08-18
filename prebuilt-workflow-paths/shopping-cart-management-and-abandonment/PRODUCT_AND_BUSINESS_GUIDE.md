# Product and Business Guide

## Boundary
Starts when a customer adds an item to a new or existing cart. Ends when the cart is successfully converted to an order, explicitly cleared by the customer, or abandoned and expired according to retention policy.

## People and systems
- Anonymous guest customer or authenticated user
- Cart and session management service
- Product catalog and pricing service
- Inventory availability service (read-only for cart)
- Promotion, discount, and tax engine
- Notification service (for abandonment reminders)

## Things created or changed
- Shopping cart session, identifier, and owner
- Cart line items, quantities, and added timestamps
- Applied promotional codes and calculated discounts
- Cart total, subtotal, and estimated tax/shipping
- Abandonment status and reminder schedule

## Stages
- Cart: created → active → abandoned (pending recovery) → expired, cleared, or converted
- Line item: added → updated → removed or purchased
- Guest session: anonymous → merging → authenticated

## Product decisions
- How long an active cart remains valid before expiration
- Whether inventory is checked when adding to cart or only at checkout
- How guest carts are merged into existing user carts upon login (e.g., sum quantities, keep highest, or keep most recent)
- How price changes in the catalog affect items already in the cart
- When and how abandoned carts trigger recovery notifications
- Whether promotional codes remain locked to the cart if the session expires
- How cross-device cart synchronization is handled for authenticated users

## Happy paths
- Customer adds items, logs in, guest cart merges cleanly, and proceeds to checkout
- Authenticated user adds items across multiple devices and sees a synchronized cart
- Customer abandons cart, receives a recovery email, clicks the link, and completes the purchase

## Negative paths
- Added item exceeds available inventory or maximum quantity limits
- Item in the cart becomes unavailable before checkout
- Invalid or expired promotional code is applied
- Customer clears the cart manually

## Edge cases
- Guest cart contains the same item as the authenticated user's saved cart during login merge
- Price or tax rate changes while the cart is active
- Two concurrent requests attempt to modify the same line item
- Cart recovery link is clicked after the cart has expired

## Acceptance criteria
1. Line items and quantities must accurately reflect customer additions and removals
2. Prices, taxes, and totals must dynamically reflect the current catalog and applied promotions
3. Guest carts must securely merge with authenticated carts upon login without losing items
4. Merging duplicate line items must follow the defined quantity-resolution policy
5. Cart sessions must expire and release data according to the retention policy
6. Abandonment reminders must only trigger for valid, unconverted carts
7. Unauthenticated users must not be able to access or modify another user's cart
8. Concurrent updates must not corrupt cart state or line item quantities
9. Cart operations must not permanently lock inventory
10. Converted carts must not be modified or trigger abandonment reminders

## Business risks
| Risk | Business consequence |
|---|---|
| Cart hijacking | Insecure session IDs allow attackers to view or modify another customer's cart |
| Lost cart data | Failed merges or cross-device sync issues frustrate users and lose sales |
| Stale pricing | Customers checkout with outdated, cheaper prices causing revenue loss |
| Duplicate items | Concurrent updates or poor merge logic result in double-charging or over-ordering |
| Spam reminders | Converted or cleared carts still receive abandonment emails, damaging brand trust |
| Inventory lockup | Cart additions incorrectly reserve inventory, preventing real sales |
