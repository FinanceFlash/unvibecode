# Payment Dispute and Chargeback Resolution

Starts when a cardholder, issuer, or network raises a dispute or chargeback against a previously captured or settled payment. Ends when the case is won, lost, accepted, withdrawn, or expires, with the ledger, order, and customer outcome recorded consistently, including any escalation to a final network decision.

| Task | File |
|---|---|
| Product and business | [PRODUCT_AND_BUSINESS_GUIDE.md](PRODUCT_AND_BUSINESS_GUIDE.md) |
| Engineering | [ENGINEERING_GUIDE.md](ENGINEERING_GUIDE.md) |
| Testing | [TESTING_GUIDE.md](TESTING_GUIDE.md) |
| Core 20 | [CORE_20_SCENARIOS.md](CORE_20_SCENARIOS.md) |
| Paths and edge cases | [PATHS_AND_EDGE_CASES.md](PATHS_AND_EDGE_CASES.md) |
| Permissions and misuse | [PERMISSION_AND_ABUSE_GUIDE.md](PERMISSION_AND_ABUSE_GUIDE.md) |
| Retry and recovery | [RETRY_AND_RECOVERY_GUIDE.md](RETRY_AND_RECOVERY_GUIDE.md) |

## Included
- dispute or chargeback intake, reason-code classification, and network deadline tracking
- evidence collection, representment, and escalation to pre-arbitration or arbitration
- provisional debit or credit, reserve adjustment, and final ledger settlement
- dispute outcome, liability-shift determination, and customer communication
- chargeback-ratio monitoring and merchant risk-program status

## Excluded
- checkout payment authorization and capture
- customer-initiated cancellation and refund before any dispute is raised
- fraud or risk screening performed at checkout time
- subscription renewal and cancellation

The five `*_SKILL.md` files are self-contained.
