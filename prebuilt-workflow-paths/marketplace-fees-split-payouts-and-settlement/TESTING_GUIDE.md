# Testing Guide

Check authoritative financial inputs, value conservation, permissions, external payout effects, recovery, and audit—not only API responses.

## 1. Eligible transaction settles once

**Given:** A completed eligible transaction has an authoritative financial version and verified payee

**When:** Settlement runs

**Expect:** One balanced settlement and permitted payout outcome are recorded

**Must not happen:** The transaction pays twice or without a balanced ledger

**Best test levels:** Integration and end-to-end.

## 2. Multi-party split balances

**Given:** A transaction has several payees, fees, taxes, reserves, and adjustments

**When:** Split calculation runs

**Expect:** Components exactly conserve gross value under the residual policy

**Must not happen:** Value is lost, created, or assigned unpredictably

**Best test levels:** Unit and property.

## 3. Small balance carries forward

**Given:** A valid payee balance is below the payout minimum

**When:** A settlement cycle closes

**Expect:** The balance remains attributable and carries forward under policy

**Must not happen:** The balance disappears or is paid outside policy

**Best test levels:** Integration.

## 4. Required settlement data is missing

**Given:** Transaction, tenant, payee, amount, currency, version, or destination is absent

**When:** Settlement is requested

**Expect:** Validation fails before ledger posting or payout submission

**Must not happen:** A guessed payee or amount is used

**Best test levels:** Unit and API.

## 5. Financial input is invalid

**Given:** A fee, split, rate, tax, reserve, or adjustment is non-finite, out of range, or inconsistent

**When:** Calculation and validation run

**Expect:** The settlement is rejected or held with a visible exception

**Must not happen:** Invalid arithmetic reaches ledger or payout provider

**Best test levels:** Unit and property.

## 6. Transaction is ineligible or held

**Given:** The transaction is incomplete, disputed, refunded, blocked, or inside a reserve window

**When:** A settlement worker evaluates it

**Expect:** No released balance or payout is created outside policy

**Must not happen:** Held customer value is released prematurely

**Best test levels:** Integration.

## 7. Actor cannot trigger settlement

**Given:** An authenticated actor lacks scoped settlement or approval authority

**When:** They submit, release, adjust, or retry a payout

**Expect:** Authorization denies the action and preserves financial state

**Must not happen:** A transaction identifier grants payout control

**Best test levels:** Authorization and security.

## 8. Currency and rounding reach boundary

**Given:** Percentage, fixed-fee, exchange, and minor-unit calculations reach rounding boundaries

**When:** Settlement components are computed

**Expect:** One versioned rounding and residual rule balances every component

**Must not happen:** Services record different totals or recipients

**Best test levels:** Unit and property.

## 9. Two workers settle same transaction

**Given:** Two workers select the same eligible transaction concurrently

**When:** Both calculate, post, and submit

**Expect:** Uniqueness and locking preserve one settlement and payout set

**Must not happen:** Both pay before transaction state changes

**Best test levels:** Concurrency integration.

## 10. Eligibility changes at boundary

**Given:** Reserve release, settlement delay, or compliance hold changes exactly at a time boundary

**When:** Trusted time is evaluated

**Expect:** One explicit inclusive or exclusive rule determines eligibility

**Must not happen:** Clock differences release funds unpredictably

**Best test levels:** Unit with controlled time.

## 11. Settlement response is lost

**Given:** Ledger or payout submission may have committed before the caller loses the response

**When:** The same request retries

**Expect:** Existing settlement and payout identities return the authoritative outcome

**Must not happen:** Ledger or provider payout duplicates

**Best test levels:** API and integration.

## 12. Transaction event is replayed

**Given:** A processed event or idempotency key is delivered again

**When:** Settlement runs

**Expect:** The original versioned outcome is returned or changed input is rejected

**Must not happen:** Fees, balances, or payouts repeat

**Best test levels:** Integration and security.

## 13. Payout or bank change is abused

**Given:** A payout destination changes near settlement or repeated submissions target the provider

**When:** verification, cooling-period, approval, and velocity controls run

**Expect:** Unverified changes are held and repeated actions are bounded

**Must not happen:** Funds are redirected or provider cost grows unchecked

**Best test levels:** Security and integration.

## 14. Ledger posts but provider submission fails

**Given:** Settlement and ledger entries commit before the provider rejects or cannot receive the payout

**When:** Recovery runs

**Expect:** The same payout instruction remains retryable or reverses under policy

**Must not happen:** Value disappears or a new payout duplicates it

**Best test levels:** Integration.

## 15. Payout provider times out

**Given:** Submission returns no reliable provider outcome

**When:** Failure handling runs

**Expect:** The payout stays uncertain pending lookup, callback, or reconciliation

**Must not happen:** Timeout triggers blind duplicate payment

**Best test levels:** Provider contract and integration.

## 16. Provider pays but response is lost

**Given:** The provider paid while the local caller received failure

**When:** Status is queried or the request repeats

**Expect:** The provider reference repairs the same payout record

**Must not happen:** Another payout is submitted

**Best test levels:** Integration.

## 17. Cross-tenant payee is supplied

**Given:** A valid actor submits a seller, payee, destination, or transaction from another tenant

**When:** Settlement or manual adjustment is requested

**Expect:** Tenant and ownership binding deny the action before ledger or provider effects

**Must not happen:** Identifiers redirect funds across marketplace boundaries

**Best test levels:** Authorization and security.

## 18. Settlement error is logged

**Given:** The path contains bank references, tax data, balances, transactions, and provider credentials

**When:** An error occurs

**Expect:** Diagnostics remain useful while sensitive financial and personal data is redacted

**Must not happen:** Sensitive payout data reaches logs or alerts

**Best test levels:** Security and log inspection.

## 19. Late refund or dispute follows settlement

**Given:** A refund, dispute, chargeback, or payout return arrives after payment

**When:** The event is processed

**Expect:** A versioned adjustment, reserve, recovery, or debt path applies without rewriting history

**Must not happen:** The event is ignored or directly corrupts a paid settlement

**Best test levels:** Integration.

## 20. Provider pays but ledger update fails

**Given:** External money moves while payout, balance, statement, or transaction status remains incomplete

**When:** Reconciliation runs

**Expect:** The same provider payment repairs all internal records without resubmission

**Must not happen:** The marketplace loses financial trace or pays twice

**Best test levels:** Integration and operations.

