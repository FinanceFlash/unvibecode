# AI Agent Tool Execution and Side-Effect Control

## Workflow boundary

AI agents may invoke tools that read information or change business state. This workflow defines the path from an agent requesting a tool through validation, authorization, execution, result handling, and recovery.

### Starts when

An AI agent produces a request to invoke a registered tool with a specific set of arguments and target resources.

### Ends when

The tool operation has a confirmed successful outcome, a confirmed failure without an unintended side effect, or an explicitly unresolved outcome requiring recovery or reconciliation.

## Included

- Tool selection and registration
- Tool request validation
- Argument validation
- Authorization and policy enforcement
- Resource and tenant boundaries
- Read-only and side-effecting tool execution
- Side-effect protection
- Idempotency and duplicate execution control
- Tool result validation
- Timeout and dependency failure handling
- Retry and recovery behaviour
- Partial and uncertain execution
- Reconciliation and observability

## Excluded

- General LLM content generation
- RAG retrieval and citation workflows
- Human approval workflows
- Scheduled job execution
- General external-system synchronization
- General authentication lifecycle management

These adjacent workflows should use their dedicated workflow packs when applicable.

## People and systems

- User or calling application
- AI agent
- Tool registry
- Validation and policy layer
- Authorization system
- Tool execution environment
- Target application or resource
- Persistence and audit systems

## Things created or changed

- Tool request
- Validated arguments
- Authorization decision
- Execution record
- Tool result
- Target resource state
- Recovery or reconciliation state

## Stages

1. Tool selection
2. Request and argument validation
3. Authorization and policy evaluation
4. Execution preparation
5. Tool execution
6. Result validation
7. Outcome recording
8. Recovery or reconciliation when required

## Files

- `PRODUCT_AND_BUSINESS_GUIDE.md` — product and business workflow definition
- `ENGINEERING_GUIDE.md` — implementation and code-tracing guidance
- `CORE_20_SCENARIOS.md` — essential workflow scenarios
- `TESTING_GUIDE.md` — detailed testing guidance
- `PATHS_AND_EDGE_CASES.md` — supported, denied, boundary, timing, and unusual paths
- `PERMISSION_AND_ABUSE_GUIDE.md` — authorization and abuse considerations
- `RETRY_AND_RECOVERY_GUIDE.md` — retry, idempotency, partial failure, and recovery
- `WRITE_PRODUCT_SPEC_SKILL.md` — product specification LLM skill
- `REVIEW_BUSINESS_RISK_SKILL.md` — business-risk review LLM skill
- `UNDERSTAND_CODE_SKILL.md` — code-understanding LLM skill
- `IMPLEMENT_WORKFLOW_SKILL.md` — implementation LLM skill
- `TEST_WORKFLOW_SKILL.md` — testing LLM skill

## Evidence rule

This workflow pack describes expected workflow controls and analysis guidance. It does not prove that a particular application implements those controls.

Actual routes, permissions, state transitions, side effects, retries, recovery, and tests must be verified from repository or runtime evidence.