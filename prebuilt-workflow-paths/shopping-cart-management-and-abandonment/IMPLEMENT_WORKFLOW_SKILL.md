---
name: implement-shopping-cart-management
description: Implement or modify Shopping Cart Management and Abandonment. Use when adding or changing cart logic, quantity rules, pricing, merge policies, abandonment, or checkout transitions.
---

# Implement Shopping Cart Management

Confirm:
- How long an active cart remains valid before expiration
- Whether inventory is checked when adding to cart or only at checkout
- How guest carts are merged into existing user carts upon login (e.g., sum quantities, keep highest, or keep most recent)
- How price changes in the catalog affect items already in the cart
- When and how abandoned carts trigger recovery notifications
- Whether promotional codes remain locked to the cart if the session expires
- How cross-device cart synchronization is handled for authenticated users

Follow project conventions and protect:
- Line items and quantities must accurately reflect customer additions and removals
- Prices, taxes, and totals must dynamically reflect the current catalog and applied promotions
- Guest carts must securely merge with authenticated carts upon login without losing items
- Merging duplicate line items must follow the defined quantity-resolution policy
- Cart sessions must expire and release data according to the retention policy
- Abandonment reminders must only trigger for valid, unconverted carts
- Unauthenticated users must not be able to access or modify another user's cart
- Concurrent updates must not corrupt cart state or line item quantities
- Cart operations must not permanently lock inventory
- Converted carts must not be modified or trigger abandonment reminders

Add all core tests and summarize decisions, files, state changes, recovery, privacy and security controls, and remaining gaps.
