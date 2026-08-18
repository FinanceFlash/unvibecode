# Testing Guide

Check authoritative identity, permissions, policy versions, state changes, downstream effects, recovery, and audit—not only responses.

## 1. Customer adds item to new cart

**Given:** A customer with no existing cart requests to add an item

**When:** The addition executes

**Expect:** A new cart session is created and the item is stored

**Must not happen:** The item is lost or cart creation fails silently

**Best test levels:** Integration and API.

## 2. Customer updates item quantity

**Given:** An existing cart contains a line item

**When:** The customer requests a quantity update

**Expect:** The quantity is successfully updated within allowed bounds

**Must not happen:** The quantity becomes negative or exceeds maximum limits

**Best test levels:** Unit and API.

## 3. Customer removes item from cart

**Given:** A cart contains multiple line items

**When:** The customer removes one item

**Expect:** The item is deleted and the subtotal is updated

**Must not happen:** The item remains in the total calculation

**Best test levels:** Unit and API.

## 4. Guest logs in with items

**Given:** A guest cart has items and the user logs in

**When:** The cart merge executes

**Expect:** The guest items are transferred to the user's saved cart

**Must not happen:** The guest items are discarded or overwrite saved items

**Best test levels:** Integration.

## 5. Guest merges duplicate item

**Given:** The guest cart and saved user cart contain the same item

**When:** The cart merge executes

**Expect:** The item quantities are merged according to policy

**Must not happen:** The quantity exceeds limits or overwrites without policy

**Best test levels:** Integration.

## 6. Authenticated user syncs devices

**Given:** A user modifies their cart on a mobile device

**When:** They view the cart on a desktop browser

**Expect:** The desktop view reflects the updated cart state

**Must not happen:** One device's stale state overwrites the other

**Best test levels:** End-to-end.

## 7. Catalog price changes during session

**Given:** An item in the cart has its catalog price updated

**When:** The customer views the cart or proceeds to checkout

**Expect:** The cart reflects the new price or prompts the customer

**Must not happen:** The customer checks out with the old price

**Best test levels:** Integration.

## 8. Promotion code is applied

**Given:** The cart contains eligible and ineligible items

**When:** A discount code is applied

**Expect:** The discount applies only to the eligible items

**Must not happen:** The discount applies to ineligible items

**Best test levels:** Unit and Integration.

## 9. Cart is abandoned

**Given:** A cart remains unconverted past the abandonment threshold

**When:** The abandonment job runs

**Expect:** A reminder notification is queued for the customer

**Must not happen:** Reminders are sent for a converted cart

**Best test levels:** Integration and operations.

## 10. Recovery link is clicked

**Given:** A customer clicks a cart recovery link from an email

**When:** The session is restored

**Expect:** The customer is safely authenticated or prompted for login

**Must not happen:** A stranger accesses the authenticated user's cart

**Best test levels:** Security and integration.

## 11. Cart expires

**Given:** A cart exceeds the maximum retention policy

**When:** The cleanup job runs

**Expect:** The cart and line items are hard-deleted or archived

**Must not happen:** Stale carts remain in the database indefinitely

**Best test levels:** Integration and operations.

## 12. Cart is converted to order

**Given:** The checkout process completes successfully

**When:** The cart conversion executes

**Expect:** The cart is marked as converted and locked

**Must not happen:** The cart remains active and modifiable

**Best test levels:** Integration.

## 13. Concurrent additions to cart

**Given:** Two requests simultaneously add the same item

**When:** Both requests process

**Expect:** Database constraints ensure the quantity is updated safely

**Must not happen:** Line item quantities are corrupted

**Best test levels:** Concurrency integration.

## 14. Item becomes out of stock

**Given:** An item in the cart loses available inventory

**When:** The customer views the cart

**Expect:** The item is marked unavailable

**Must not happen:** The cart hides the out-of-stock status until payment

**Best test levels:** Integration.

## 15. Customer clears the entire cart

**Given:** A cart contains multiple items

**When:** The customer requests to clear the cart

**Expect:** All line items are removed and total is zero

**Must not happen:** Line items persist or totals remain non-zero

**Best test levels:** API and integration.

## 16. Guest cart session is hijacked

**Given:** An attacker attempts to guess another guest's session ID

**When:** They request the cart details

**Expect:** The request is denied or the session ID is cryptographically secure

**Must not happen:** An attacker modifies another guest's cart

**Best test levels:** Security.

## 17. Guest cart is merged twice

**Given:** A network retry causes the login merge to execute twice

**When:** Both requests process

**Expect:** The merge handles the replay idempotently

**Must not happen:** Items are duplicated due to replay

**Best test levels:** Integration.

## 18. Abandonment job fails halfway

**Given:** The abandonment job crashes during batch processing

**When:** The job restarts

**Expect:** It resumes processing without sending duplicate emails

**Must not happen:** Remaining abandoned carts never receive reminders

**Best test levels:** Integration and operations.

## 19. Recovery link is expired

**Given:** A customer clicks an old, expired cart recovery link

**When:** The request is processed

**Expect:** The system rejects the link safely

**Must not happen:** The customer accesses a deleted or reassigned cart

**Best test levels:** API and integration.

## 20. Database connection times out

**Given:** The database times out while saving cart state

**When:** The request completes

**Expect:** An error is returned and state remains consistent

**Must not happen:** The cart shows an inconsistent or partial state

**Best test levels:** Integration and fault injection.
