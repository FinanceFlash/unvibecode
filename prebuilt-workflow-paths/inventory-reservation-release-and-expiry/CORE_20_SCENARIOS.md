# Core 20 Scenarios

| # | Scenario | Must not happen |
|---:|---|---|
| 1 | Available quantity is reserved once | Stock is held twice or quantities do not balance |
| 2 | Reservation converts once | The same reservation is consumed twice |
| 3 | Cancellation releases quantity | More stock is released than held or the hold remains stranded |
| 4 | Required reservation data is missing | A blank or unowned hold enters inventory |
| 5 | Quantity is invalid | Invalid arithmetic changes inventory |
| 6 | Inventory is insufficient | Inventory becomes negative or a false hold is confirmed |
| 7 | Actor cannot control reservation | A reservation identifier grants inventory control |
| 8 | Equivalent item or unit representations differ | Formatting or unit conversion bypasses availability limits |
| 9 | Two customers request last unit | Both receive confirmed exclusive stock |
| 10 | Conversion occurs at expiry | Both consumption and release occur |
| 11 | Reservation response is lost | A second hold is created |
| 12 | Reservation operation is replayed | Quantities change again |
| 13 | Scarce inventory is hoarded | Real customers lose stock indefinitely |
| 14 | Reservation commits but expiry job fails | Stock remains stranded silently |
| 15 | Inventory dependency times out | Timeout causes blind duplicate hold or false availability |
| 16 | Conversion commits but response is lost | Committed quantity is deducted again |
| 17 | Cross-tenant reservation is referenced | Identifiers cross inventory boundaries |
| 18 | Inventory error is logged | Protected records or control tokens reach logs |
| 19 | Late expiry follows conversion | Committed inventory returns to available |
| 20 | Multi-line reservation partially fails | Invisible partial holds strand stock or confirm unavailable items |

Full details are in [TESTING_GUIDE.md](TESTING_GUIDE.md).

