# Core 20 Scenarios

| # | Scenario | Must not happen |
|---:|---|---|
| 1 | Eligible transaction settles once | The transaction pays twice or without a balanced ledger |
| 2 | Multi-party split balances | Value is lost, created, or assigned unpredictably |
| 3 | Small balance carries forward | The balance disappears or is paid outside policy |
| 4 | Required settlement data is missing | A guessed payee or amount is used |
| 5 | Financial input is invalid | Invalid arithmetic reaches ledger or payout provider |
| 6 | Transaction is ineligible or held | Held customer value is released prematurely |
| 7 | Actor cannot trigger settlement | A transaction identifier grants payout control |
| 8 | Currency and rounding reach boundary | Services record different totals or recipients |
| 9 | Two workers settle same transaction | Both pay before transaction state changes |
| 10 | Eligibility changes at boundary | Clock differences release funds unpredictably |
| 11 | Settlement response is lost | Ledger or provider payout duplicates |
| 12 | Transaction event is replayed | Fees, balances, or payouts repeat |
| 13 | Payout or bank change is abused | Funds are redirected or provider cost grows unchecked |
| 14 | Ledger posts but provider submission fails | Value disappears or a new payout duplicates it |
| 15 | Payout provider times out | Timeout triggers blind duplicate payment |
| 16 | Provider pays but response is lost | Another payout is submitted |
| 17 | Cross-tenant payee is supplied | Identifiers redirect funds across marketplace boundaries |
| 18 | Settlement error is logged | Sensitive payout data reaches logs or alerts |
| 19 | Late refund or dispute follows settlement | The event is ignored or directly corrupts a paid settlement |
| 20 | Provider pays but ledger update fails | The marketplace loses financial trace or pays twice |

Full details are in [TESTING_GUIDE.md](TESTING_GUIDE.md).

