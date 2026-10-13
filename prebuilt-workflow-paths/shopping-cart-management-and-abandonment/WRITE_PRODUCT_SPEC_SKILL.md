---
name: write-shopping-cart-product-spec
description: Write a product specification for Shopping Cart Management and Abandonment.
---

# Write Shopping Cart Product Spec

Define:
- How long an active cart remains valid before expiration
- Whether inventory is checked when adding to cart or only at checkout
- How guest carts are merged into existing user carts upon login (e.g., sum quantities, keep highest, or keep most recent)
- How price changes in the catalog affect items already in the cart
- When and how abandoned carts trigger recovery notifications
- Whether promotional codes remain locked to the cart if the session expires
- How cross-device cart synchronization is handled for authenticated users

Ensure the specification prevents:
- Cart hijacking
- Lost cart data
- Stale pricing
- Duplicate items
- Spam reminders
- Inventory lockup

Summarize the people and systems, things created or changed, stages, happy paths, negative paths, and edge cases.
