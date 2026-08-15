# UnvibeCode Business Workflow Packs

Reusable workflow specifications, business-risk checks, engineering guidance, test scenarios, and task-specific LLM skills for common software workflows.

These packs help teams answer four practical questions:

- **Product managers and founders:** Which business paths, decisions, failure consequences, and acceptance criteria must be defined?
- **Engineers:** Where should authorization, state transitions, external effects, retries, and recovery be implemented or reviewed?
- **Testers:** Which normal, negative, boundary, concurrency, permission, abuse, and recovery scenarios should be validated?
- **LLM users:** Which focused skill should be used to write a specification, review risk, understand code, implement the workflow, or design tests?

## Add this collection to a repository

Copy the entire `prebuilt-workflow-paths` directory into the root of your repository:

```text
your-repository/
├── prebuilt-workflow-paths/
│   ├── README.md
│   ├── multi-step-approval-and-rejection/
│   ├── customer-support-ticket-management/
│   └── ...
└── your existing project files
```

No installation, generator, schema, or build step is required. Every workflow is a separate flat folder, so teams can retain the full collection or copy only the workflows relevant to their application.

## Choose a workflow

### Approval, support, and customer communication

| Workflow | Use it when your application… |
|---|---|
| [Multi-step Approval and Rejection](multi-step-approval-and-rejection/) | routes a request through one or more approvers and may approve, reject, return, escalate, or expire it |
| [Customer Support Ticket Lifecycle](customer-support-ticket-management/) | creates, assigns, updates, escalates, resolves, reopens, or closes support cases |
| [Transactional Email, SMS, Push, or In-app Delivery](transactional-notification-delivery/) | sends business-critical messages after customer or system events |
| [Failed Notification Retry and Channel Fallback](failed-notification-retry-and-channel-fallback/) | retries failed delivery or switches communication channels without duplicating or misrouting messages |

### Payments, subscriptions, orders, and inventory

| Workflow | Use it when your application… |
|---|---|
| [Checkout Payment Authorization and Capture](checkout-payment-authorization-and-capture/) | authorizes and captures payment while coordinating checkout and order state |
| [Subscription Renewal, Cancellation, and Entitlement Release](subscription-renewal-cancellation-and-access-removal/) | renews subscriptions, handles cancellation, and grants or removes access |
| [Order Placement and Confirmation](order-placement-and-confirmation/) | validates a cart, creates an order, and confirms acceptance to the customer |
| [Inventory Reservation, Release, and Expiry](inventory-reservation-release-and-expiry/) | temporarily reserves scarce inventory and later commits, releases, or expires it |

### Booking and marketplace operations

| Workflow | Use it when your application… |
|---|---|
| [Booking Confirmation and Capacity Commitment](booking-confirmation-and-capacity-reservation/) | converts availability into a confirmed reservation without overselling capacity |
| [Booking Cancellation, Capacity Release, and Refund Request](booking-cancellation-capacity-release-and-refund/) | cancels a booking and coordinates released capacity and any refund request |
| [Seller or Service-provider Onboarding and Eligibility](seller-and-service-provider-onboarding/) | verifies and activates providers before allowing them to sell or deliver services |
| [Commission, Fee, Split Payout, and Seller Settlement](marketplace-fees-split-payouts-and-settlement/) | calculates platform fees and settles funds among sellers or service providers |

### LLM, retrieval, and external systems

| Workflow | Use it when your application… |
|---|---|
| [LLM Content Generation and Structured-output Validation](llm-content-generation-and-output-validation/) | generates content or structured results and must validate them before use |
| [RAG Question Answering with Evidence and Citations](rag-question-answering-with-evidence-and-citations/) | retrieves sources and produces answers that must remain grounded in evidence |
| [External-system Synchronization and Checkpointing](external-system-data-sync-and-checkpointing/) | synchronizes records with an external system while tracking progress and recovery |

### Risk, privacy, and background execution

| Workflow | Use it when your application… | 
|---|---| 
| [Authentication, Session Management, and Account Recovery](authentication-session-management-and-account-recovery/) | authenticates users, manages authenticated sessions, terminates sessions, or recovers account access |
| [Fraud-risk Scoring, Step-up, Block, and Case Creation](fraud-risk-check-step-up-block-and-investigation/) | evaluates protected actions and may allow, challenge, hold, block, or investigate them | 
| [Right-to-erasure and Account-data Deletion](account-data-deletion-and-right-to-erasure/) | verifies and executes deletion or anonymization requests across data stores and processors | 
| [Scheduled Job Execution, Checkpoint, Retry, and Recovery](scheduled-job-execution-retry-and-recovery/) | runs scheduled work with leases, bounded input windows, checkpoints, retries, and repair | 

The navigation categories are only for discovery. Each workflow has its own clear start, end, stages, effects, permissions, and recovery boundary.

## What each workflow contains

Every workflow folder uses the same flat structure:

| File | Best for | Purpose |
|---|---|---|
| `README.md` | Everyone | Workflow boundary, included scope, excluded scope, and file navigation |
| `PRODUCT_AND_BUSINESS_GUIDE.md` | PMs and founders | People and systems, things created or changed, stages, decisions, paths, edge cases, acceptance criteria, and consequences |
| `ENGINEERING_GUIDE.md` | Developers and engineering managers | Code-tracing sequence, implementation safeguards, effects, state, and recovery concerns |
| `CORE_20_SCENARIOS.md` | Everyone | Compact checklist of the 20 essential scenarios and what must not happen |
| `TESTING_GUIDE.md` | QA and developers | All 20 scenarios written with Given, When, Expect, Must not happen, and suggested test levels |
| `PATHS_AND_EDGE_CASES.md` | PMs, QA, and developers | Supported, denied, timing, boundary, concurrency, and unusual paths |
| `PERMISSION_AND_ABUSE_GUIDE.md` | Security, PMs, and engineers | Authorization boundaries, misuse paths, tenant isolation, and protected data |
| `RETRY_AND_RECOVERY_GUIDE.md` | Engineers, QA, and operations | Partial failures, idempotency, retry, reconciliation, and manual repair |
| `WRITE_PRODUCT_SPEC_SKILL.md` | PMs using an LLM | Writes or reviews a workflow-specific product specification |
| `REVIEW_BUSINESS_RISK_SKILL.md` | Founders and PMs using an LLM | Reviews customer, revenue, privacy, compliance, and operational consequences |
| `UNDERSTAND_CODE_SKILL.md` | Developers using an LLM | Traces the workflow through an existing codebase with file and symbol evidence |
| `IMPLEMENT_WORKFLOW_SKILL.md` | Developers using an LLM | Implements or modifies the workflow while preserving its key safeguards |
| `TEST_WORKFLOW_SKILL.md` | Testers and developers using an LLM | Designs or reviews the complete workflow-specific test set |

Every `PRODUCT_AND_BUSINESS_GUIDE.md` uses the exact headings `People and systems`, `Things created or changed`, and `Stages`. Every core scenario uses `Must not happen` for the outcome that the workflow must prevent.

## Recommended reading paths

### Product manager or founder

1. Read the workflow `README.md` to confirm that its boundary matches your product.
2. Use `PRODUCT_AND_BUSINESS_GUIDE.md` to make unresolved policy decisions.
3. Review `PATHS_AND_EDGE_CASES.md` and `CORE_20_SCENARIOS.md` before finalizing requirements.
4. Use `REVIEW_BUSINESS_RISK_SKILL.md` with your specification or repository context.

### Developer or engineering manager

1. Confirm the workflow boundary in `README.md`.
2. Trace the implementation using `ENGINEERING_GUIDE.md` or `UNDERSTAND_CODE_SKILL.md`.
3. Review permissions, externally visible effects, retries, and recovery before changing code.
4. Use `IMPLEMENT_WORKFLOW_SKILL.md` and require code and symbol evidence for conclusions.

### Tester

1. Start with `CORE_20_SCENARIOS.md` as the coverage checklist.
2. Use the complete scenarios in `TESTING_GUIDE.md` to design test cases.
3. Add application-specific values, roles, time limits, provider behaviour, and expected state changes.
4. Use the permission and retry guides for security, concurrency, partial-failure, and operational testing.

## Using the task skills

The five `*_SKILL.md` files in each workflow are portable and self-contained. Select the file matching the task and provide it to the LLM together with the relevant product specification, codebase, or test context.

Do not treat a workflow pack as proof that a control exists in your application. Verify actual routes, permissions, state transitions, data writes, external calls, retries, tests, and production behaviour.

## Contributing a workflow

Read the [repository contribution guide](../.github/CONTRIBUTING.md) before proposing a pack. It defines the required 13-file structure, MECE workflow boundaries, scenario-coverage rules, and pull-request checklist.

## Collection summary

- 18 independently usable business workflow packs
- 234 workflow-specific Markdown files
- 360 compact core scenarios
- 360 complete Given/When/Expect scenario descriptions
- 90 portable task skills

These packs are starting points for application-specific analysis. Product rules, laws, provider contracts, data-retention requirements, and operational limits still need to be adapted to the repository being reviewed.
