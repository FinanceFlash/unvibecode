# Shopping Cart Management and Abandonment

Starts when a customer adds an item to a new or existing cart. Ends when the cart is successfully converted to an order, explicitly cleared by the customer, or abandoned and expired according to retention policy.

| Task | File |
|---|---|
| Product and business | [PRODUCT_AND_BUSINESS_GUIDE.md](PRODUCT_AND_BUSINESS_GUIDE.md) |
| Engineering | [ENGINEERING_GUIDE.md](ENGINEERING_GUIDE.md) |
| Testing | [TESTING_GUIDE.md](TESTING_GUIDE.md) |
| Core 20 | [CORE_20_SCENARIOS.md](CORE_20_SCENARIOS.md) |
| Paths and edge cases | [PATHS_AND_EDGE_CASES.md](PATHS_AND_EDGE_CASES.md) |
| Permissions and misuse | [PERMISSION_AND_ABUSE_GUIDE.md](PERMISSION_AND_ABUSE_GUIDE.md) |
| Retry and recovery | [RETRY_AND_RECOVERY_GUIDE.md](RETRY_AND_RECOVERY_GUIDE.md) |

## Included
- cart creation, item addition, removal, and quantity updates
- guest cart persistence, authenticated carts, and cross-device synchronization
- guest-to-user cart merging during login or registration
- price calculation, discounts, tax estimation, and shipping preview
- cart abandonment tracking, reminder notifications, and cart expiration

## Excluded
- checkout payment authorization and capture (see `checkout-payment-authorization-and-capture`)
- inventory reservation and capacity commitment (see `inventory-reservation-release-and-expiry`)
- order placement and confirmation (see `order-placement-and-confirmation`)

The five `*_SKILL.md` files are self-contained.
