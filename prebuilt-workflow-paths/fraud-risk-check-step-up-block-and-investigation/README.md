# Fraud-risk Scoring, Step-up, Block, and Case Creation

Starts when a protected customer or business action supplies identity, session, device, transaction, and behavioral signals. Ends when the action is allowed, challenged, held, blocked, or routed to an investigation case with enforcement and customer state recorded consistently.

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
- protected-action eligibility, signal collection, feature freshness, rules, model score, and risk policy
- threshold decision, allow, step-up, hold, block, challenge result, and case creation
- manual review and override, decision version, expiry, enforcement, notification, and audit
- privacy, fairness, adversarial probing, rate limits, provider failure, retry, recovery, and monitoring

## Excluded
- generic model inference without fraud policy
- KYC identity-document verification
- AML and sanctions screening
- security-incident response after confirmed compromise

The five `*_SKILL.md` files are self-contained.

