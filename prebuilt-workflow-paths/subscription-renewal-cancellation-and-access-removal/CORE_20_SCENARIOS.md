# Core 20 Scenarios

| # | Scenario | Must not happen |
|---:|---|---|
| 1 | Due subscription renews once | The same period is charged or extended twice |
| 2 | Period-end cancellation releases on time | Access ends early or billing continues into another period |
| 3 | Immediate cancellation follows policy | The action silently behaves as period-end or leaves stale access |
| 4 | Required subscription data is missing | A guessed subscription is charged or terminated |
| 5 | Period or price is malformed | Invalid dates or amounts reach provider and entitlement systems |
| 6 | Subscription is ineligible | A stale job revives or charges an ineligible subscription |
| 7 | Actor cannot manage subscription | A subscription identifier grants financial control |
| 8 | Billing boundary handles calendar rules | Periods overlap, gap, or charge on the wrong date |
| 9 | Renewal and cancellation race | The customer is charged after effective cancellation or gets free access |
| 10 | Payment completes at grace boundary | Races create both active and terminated outcomes |
| 11 | Cancellation response is lost | Another cancellation or access release effect is created |
| 12 | Renewal job is replayed | Payment, invoice, period, or notification repeats |
| 13 | Renewal or cancellation is flooded | Provider cost, messages, or state contention grows unchecked |
| 14 | Payment succeeds but period update fails | The customer is charged again or loses access |
| 15 | Provider times out during renewal | Timeout is treated as final failure or safe success |
| 16 | Renewal commits but response is lost | The period, charge, or entitlement extends again |
| 17 | Cross-tenant subscription is referenced | Identifiers cross the billing boundary |
| 18 | Billing failure is logged | Sensitive billing data reaches logs or alerts |
| 19 | Late payment follows termination | Stale payment silently reactivates or is ignored while money is kept |
| 20 | Entitlement release fails | Billing stops while unauthorized free access continues |

Full details are in [TESTING_GUIDE.md](TESTING_GUIDE.md).

