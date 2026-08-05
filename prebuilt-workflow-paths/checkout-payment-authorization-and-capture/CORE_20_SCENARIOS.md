# Core 20 Scenarios

| # | Scenario | Must not happen |
|---:|---|---|
| 1 | Valid checkout is captured once | The customer is charged twice or for a different amount |
| 2 | Authorization is captured before expiry | A new authorization or duplicate capture is created |
| 3 | Customer authentication resumes payment | A second attempt or wrong customer session is used |
| 4 | Required payment input is missing | A guessed or zero-value provider request is sent |
| 5 | Amount or currency is malformed | Rounding or conversion silently changes the charge |
| 6 | Provider declines payment | The decline is reported as success or retried blindly |
| 7 | Actor cannot pay for order | An order identifier permits cross-account payment control |
| 8 | Minor-unit boundary is calculated | Different services charge or record different totals |
| 9 | Two payments arrive together | Both attempts capture before order state changes |
| 10 | Authorization expires at boundary | Clock differences extend or shorten validity unpredictably |
| 11 | Payment response is lost | Retry creates another charge |
| 12 | Idempotency key is replayed with changed payload | The old key authorizes a different payment |
| 13 | Payment attempts are flooded | Card testing, provider cost, or account harm grows unchecked |
| 14 | Authorization succeeds but local write fails | A second authorization is created blindly |
| 15 | Provider times out uncertainly | Timeout is treated as decline and immediately retried |
| 16 | Capture succeeds but response is lost | A second capture or contradictory order status is created |
| 17 | Cross-tenant order reference is supplied | Identifiers cross the financial boundary |
| 18 | Payment error is logged | Tokens, secrets, or prohibited card data enter logs |
| 19 | Late capture follows cancellation | A stale command charges a cancelled order |
| 20 | Capture succeeds but order update fails | The customer pays without order value or financial trace |

Full details are in [TESTING_GUIDE.md](TESTING_GUIDE.md).

