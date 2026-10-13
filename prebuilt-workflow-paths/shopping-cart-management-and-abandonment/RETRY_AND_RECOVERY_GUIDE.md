# Retry and Recovery Guide

## Partial failures
- **Database timeout during add:** The request fails, but the cart state remains consistent. The user can safely retry adding the item.
- **Merge failure during login:** If the login succeeds but the cart merge fails, the guest items may be orphaned. The system should ideally wrap the merge in a transaction or allow manual recovery.

## Idempotency
- Cart additions should ideally be idempotent if the client includes an idempotency key, preventing double-additions on network retries.
- Quantity updates (e.g., `PUT /cart/items/{id} {"quantity": 2}`) are naturally idempotent.
- The cart abandonment reminder job must record successful notifications to prevent spamming the user if the job restarts.

## Reconciliation
- **Stale prices:** The system must reconcile cart prices against the live catalog during the checkout transition to ensure customers are not charged outdated prices.
- **Expired carts:** A background worker must periodically reconcile and clear abandoned carts that have passed the retention policy to free up storage.

## Manual repair
- Customer support may need tools to clear a corrupted cart or manually apply a discount if the merge logic fails during a promotion.
