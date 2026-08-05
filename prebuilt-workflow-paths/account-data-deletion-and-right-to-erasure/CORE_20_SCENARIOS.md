# Core 20 Scenarios

| # | Scenario | Must not happen |
|---:|---|---|
| 1 | Eligible request completes erasure | Mandatory stores retain data or another account is affected |
| 2 | Lawful hold preserves only required data | The entire account is retained without justification |
| 3 | Anonymization preserves non-personal record | The person can still be reidentified through retained fields |
| 4 | Required request data is missing | Destructive work starts from guessed identity |
| 5 | Scope or identifier is malformed | Malformed scope reaches deletion workers |
| 6 | Identity verification fails | Support pressure or request possession substitutes for proof |
| 7 | Operator cannot approve or execute | A request id grants destructive control |
| 8 | Aliases resolve to one account safely | An alias crosses users or leaves hidden in-scope data |
| 9 | Duplicate requests execute together | Tasks conflict, over-delete, or mark complete early |
| 10 | Hold expires at boundary | Clock differences cause unlawful deletion or retention |
| 11 | Request response is lost | Duplicate destructive workflows begin |
| 12 | Deletion task is replayed | Shared data, evidence, or unrelated records are deleted |
| 13 | Deletion is abused | Operations are exhausted or other accounts are targeted |
| 14 | Restriction commits but jobs fail | The user is locked out while data remains indefinitely |
| 15 | Processor or datastore times out | Uncertainty is counted as deleted |
| 16 | Deletion commits but response is lost | Retries delete broader or unrelated data |
| 17 | Cross-tenant record is discovered | Identifier matching deletes another customer's data |
| 18 | Deletion failure is logged | Personal data or evidence enters unsafe logs |
| 19 | Late data arrives after completion | Deleted personal data silently becomes active again |
| 20 | One mandatory system fails | The customer receives false completion |

Full details are in [TESTING_GUIDE.md](TESTING_GUIDE.md).

