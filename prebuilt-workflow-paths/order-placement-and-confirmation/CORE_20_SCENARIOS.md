# Core 20 Scenarios

| # | Scenario | Must not happen |
|---:|---|---|
| 1 | Valid checkout creates one order | The checkout creates duplicate orders or different accepted values |
| 2 | Order preserves accepted snapshot | Later catalog or profile data silently rewrites it |
| 3 | Downstream references bind same order | An effect attaches to another order or tenant |
| 4 | Required checkout data is missing | An incomplete order enters operations |
| 5 | Checkout value is malformed | Malformed values reach payment, inventory, fulfilment, or logs |
| 6 | Quote or hold is stale | Stale values are silently committed |
| 7 | Actor cannot place order | A checkout identifier grants purchase control |
| 8 | Totals reach rounding boundary | Services record different totals |
| 9 | Two submissions arrive together | Both commit before checkout conversion is visible |
| 10 | Hold expires during commit | Races create an order without valid prerequisites |
| 11 | Placement response is lost | A duplicate order is created |
| 12 | Key is replayed with changed checkout | The old key mutates or creates a different order |
| 13 | Order creation is flooded | Order, payment, inventory, or provider load grows unchecked |
| 14 | Order commits but payment handoff fails | The order confirms without payment or charges twice |
| 15 | Dependency times out | Uncertainty becomes false confirmation |
| 16 | Order commits but response is lost | Order number, payment, reservation, or confirmation repeats |
| 17 | Cross-tenant checkout is referenced | Identifiers cross account or tenant boundaries |
| 18 | Order failure is logged | Full customer or payment information enters unsafe logs |
| 19 | Late prerequisite follows rejection | A stale result creates an unexpected confirmed order |
| 20 | Confirmation or fulfilment fails | The customer is told nothing or downstream work duplicates |

Full details are in [TESTING_GUIDE.md](TESTING_GUIDE.md).

