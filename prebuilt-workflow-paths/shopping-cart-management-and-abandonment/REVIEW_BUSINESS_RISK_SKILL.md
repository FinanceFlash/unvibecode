---
name: review-shopping-cart-business-risk
description: Review Shopping Cart Management and Abandonment for business risks.
---

# Review Shopping Cart Business Risk

Check the implementation or specification for these business risks:
- Cart hijacking
- Lost cart data
- Stale pricing
- Duplicate items
- Spam reminders
- Inventory lockup

Ensure these acceptance criteria are met:
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

Report findings with specific evidence.
