# Agent Tool Calling and Task Execution

Defines the lifecycle of an autonomous AI agent receiving a task, planning, executing tools securely, handling errors, and reaching a final outcome.

## Workflow Boundary

- **Starts when**: User or system submits a task to the agent.
- **Ends when**: Task completed successfully, Task failed permanently, or Task escalated for human review.

## Included scope
- Agent planning and reasoning.
- Tool selection and argument formulation.
- Authorization and validation of tool execution.
- Handling tool errors, timeouts, and retries.
- Parsing tool output.
- Final task resolution.

## Excluded scope
- Simple content generation without external side effects (see LLM Content Generation and Structured-output Validation).
- Question answering over static documents (see RAG Question Answering with Evidence and Citations).
- Standard background job scheduling (see Scheduled Job Execution, Checkpoint, Retry, and Recovery).

## Primary Business Outcome
Secure, reliable, and auditable execution of autonomous tasks using authorized tools without exceeding permission boundaries.

## Navigation
- [Product and Business Guide](PRODUCT_AND_BUSINESS_GUIDE.md)
- [Engineering Guide](ENGINEERING_GUIDE.md)
- [Core 20 Scenarios](CORE_20_SCENARIOS.md)
- [Testing Guide](TESTING_GUIDE.md)
- [Paths and Edge Cases](PATHS_AND_EDGE_CASES.md)
- [Permission and Abuse Guide](PERMISSION_AND_ABUSE_GUIDE.md)
- [Retry and Recovery Guide](RETRY_AND_RECOVERY_GUIDE.md)
- [Write Product Spec Skill](WRITE_PRODUCT_SPEC_SKILL.md)
- [Review Business Risk Skill](REVIEW_BUSINESS_RISK_SKILL.md)
- [Understand Code Skill](UNDERSTAND_CODE_SKILL.md)
- [Implement Workflow Skill](IMPLEMENT_WORKFLOW_SKILL.md)
- [Test Workflow Skill](TEST_WORKFLOW_SKILL.md)
