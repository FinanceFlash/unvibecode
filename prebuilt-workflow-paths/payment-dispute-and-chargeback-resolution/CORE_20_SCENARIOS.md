# Core 20 Scenarios

| # | Scenario | Must not happen |
|---:|---|---|
| 1 | Valid dispute opens against a captured payment | A case opens against a payment that was never captured or does not exist |
| 2 | Complete evidence is submitted before the deadline | Incomplete or wrong evidence is recorded as a complete submission |
| 3 | Low-value dispute is auto-accepted by policy | The case is contested past the cost-to-fight threshold without approval |
| 4 | Authenticated transaction wins on liability shift | Liability shift is ignored and the merchant absorbs an avoidable loss |
| 5 | Required dispute fields are missing | A guessed or unlinked case is created |
| 6 | Dispute amount or currency mismatches the payment | The mismatch is silently reconciled instead of flagged |
| 7 | Actor without dispute-team access submits evidence | An unauthorized actor modifies or submits case evidence |
| 8 | Evidence deadline is reached at a timezone boundary | Clock differences extend or shorten the window unpredictably |
| 9 | Two dispute webhooks arrive together for one case | The provisional debit is applied twice |
| 10 | Provider retries the dispute-opened notification | A duplicate case is created for one chargeback |
| 11 | Representment response from the network is lost | Resubmission creates a second representment instead of resuming the same case |
| 12 | Case is escalated to pre-arbitration after resolution | The case is treated as final and closed prematurely |
| 13 | Merchant chargeback ratio crosses the risk threshold | Risk-program escalation is not triggered |
| 14 | Cardholder withdraws the dispute after representment | The case stays open or funds are not reinstated |
| 15 | Provisional debit succeeds but the ledger write fails | A second debit is applied blindly on retry |
| 16 | Dispute references another tenant's payment | Identifiers cross the tenant boundary into another merchant's case |
| 17 | Resolution arrives after the order was already refunded | The ledger reverses the same funds twice |
| 18 | Evidence bundle contains cardholder PAN or secrets | Sensitive data enters logs or unauthorized storage |
| 19 | Final network outcome arrives after internal tracking expired | Stale internal state contradicts the authoritative network outcome |
| 20 | Case resolves but the order or customer record update fails | The ledger, order, and customer outcome show contradictory states |

Full details are in [TESTING_GUIDE.md](TESTING_GUIDE.md).
