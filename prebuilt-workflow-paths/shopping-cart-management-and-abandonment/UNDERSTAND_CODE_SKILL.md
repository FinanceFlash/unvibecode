---
name: understand-shopping-cart-code
description: Trace Shopping Cart Management and Abandonment through an existing codebase.
---

# Understand Shopping Cart Code

Identify and map:
- Guest cart session generation and validation
- Authenticated cart retrieval and device synchronization
- Item addition, removal, and quantity update logic
- Login event handlers that trigger guest-to-user cart merging
- Pricing, tax, and discount calculation engines
- Scheduled jobs for cart abandonment notifications and retention cleanup
- Database constraints and locking mechanisms protecting cart state

Trace the flow from `HTTP POST /cart/items` to state modification and ensure you understand the boundary between the active cart and the converted order state.
