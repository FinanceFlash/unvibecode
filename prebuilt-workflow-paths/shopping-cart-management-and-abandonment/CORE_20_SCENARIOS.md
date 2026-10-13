# Core 20 Scenarios

| # | Scenario | Must not happen |
|---:|---|---|
| 1 | Customer adds item to new cart | The item is lost or cart creation fails silently |
| 2 | Customer updates item quantity | The quantity becomes negative or exceeds maximum limits |
| 3 | Customer removes item from cart | The item remains in the total calculation |
| 4 | Guest logs in with items | The guest items are discarded or overwrite saved items |
| 5 | Guest merges duplicate item | The quantity exceeds limits or overwrites without policy |
| 6 | Authenticated user syncs devices | One device's stale state overwrites the other |
| 7 | Catalog price changes during session | The customer checks out with the old price |
| 8 | Promotion code is applied | The discount applies to ineligible items |
| 9 | Cart is abandoned | Reminders are sent for a converted cart |
| 10 | Recovery link is clicked | A stranger accesses the authenticated user's cart |
| 11 | Cart expires | Stale carts remain in the database indefinitely |
| 12 | Cart is converted to order | The cart remains active and modifiable |
| 13 | Concurrent additions to cart | Line item quantities are corrupted |
| 14 | Item becomes out of stock | The cart hides the out-of-stock status until payment |
| 15 | Customer clears the entire cart | Line items persist or totals remain non-zero |
| 16 | Guest cart session is hijacked | An attacker modifies another guest's cart |
| 17 | Guest cart is merged twice | Items are duplicated due to replay |
| 18 | Abandonment job fails halfway | Remaining abandoned carts never receive reminders |
| 19 | Recovery link is expired | The customer accesses a deleted or reassigned cart |
| 20 | Database connection times out | The cart shows an inconsistent or partial state |

Full details are in [TESTING_GUIDE.md](TESTING_GUIDE.md).
