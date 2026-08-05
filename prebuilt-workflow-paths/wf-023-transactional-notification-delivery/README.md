# Transactional Email, SMS, Push, or In-app Delivery

Starts when an eligible business event requires a transactional notification. Ends when one recipient-safe message is rejected before sending, accepted by a channel provider, recorded as delivered or failed, or handed to the separate retry-and-fallback workflow.

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
- event eligibility, recipient resolution, preference and purpose checks
- template version, localization, rendering, redaction, and channel selection
- email, SMS, push, and in-app message creation and initial delivery attempt
- provider references, status, callbacks, audit, privacy, idempotency, and failure handoff

## Excluded
- marketing campaign orchestration
- message-content authoring and template administration
- retry schedules and fallback after an initial failure
- general inbound-message processing

The five `*_SKILL.md` files are self-contained.

