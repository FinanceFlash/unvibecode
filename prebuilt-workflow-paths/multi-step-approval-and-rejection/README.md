# Multi-step Approval and Rejection

Starts when a complete business request is submitted for approval. Ends when the required decision policy produces an approved, rejected, withdrawn, expired, or correction-required outcome and all authorized downstream effects are recorded consistently.

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
- sequential, parallel, and quorum approval
- reviewer eligibility, delegation, conflict, and tenant scope
- request versions, evidence, decisions, comments, deadlines, and escalation
- finalization, notification, downstream handoff, audit, retry, recovery, and misuse

## Excluded
- creating the underlying business request
- executing domain-specific work after approval
- general support-ticket handling
- authentication and role administration

The five `*_SKILL.md` files are self-contained.

