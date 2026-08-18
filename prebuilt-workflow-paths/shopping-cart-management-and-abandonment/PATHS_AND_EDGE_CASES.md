# Paths and Edge Cases

## Supported paths
- Anonymous guest adds items, reviews cart, and updates quantities
- Authenticated user accesses saved cart across multiple devices
- Guest logs in and their guest cart items are merged with their saved cart
- Cart applies dynamic promotion codes and computes discounts
- System identifies abandoned carts and sends reminder emails

## Denied paths
- Adding an item that exceeds available inventory
- Setting a line item quantity below 1 or above the maximum limit
- Applying an expired or invalid promotional code
- Modifying a cart that has already been converted to an order
- Attempting to view or update a cart session owned by another user

## Timing and boundary cases
- The catalog price changes exactly when the user is checking out
- The cart retention policy expires the cart while the user is actively browsing
- The abandonment reminder job runs exactly as the user converts the cart
- Two devices attempt to add or remove items simultaneously

## Unusual paths
- The user clears the cart manually after applying a complex discount code
- The guest cart contains duplicate items with the saved cart during a login merge
- The database connection fails during a quantity update
