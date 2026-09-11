# UnvibeCode Limits and Review Boundaries

This page collects repository-size behavior and review boundaries that are intentionally kept out of the main README so the project overview stays concise.

## Repository-size behavior

Repositories at or below approximately two million estimated source tokens receive the full UnvibeCode review:

- Connected Code Map for LLMs
- Complete Repository Context
- Business Workflow Map
- Business Risk Findings

Repositories above approximately two million estimated source tokens receive:

- Connected Code Map for LLMs
- Complete Repository Context

The deeper Business Workflow and Risk Review is not started above that threshold. This prevents oversized repositories from entering a long hosted review while still producing useful code-graph and LLM-context outputs.

For more detail, see [How UnvibeCode works](HOW_IT_WORKS.md).

## What UnvibeCode does not replace

UnvibeCode supports code understanding, workflow review, and evidence-based engineering investigation. It does not replace:

- Unit, integration, end-to-end, load, or penetration testing
- Manual code review by engineers familiar with the system
- Security, privacy, legal, or regulatory assessment
- Production monitoring and incident investigation
- Validation of business requirements with the responsible product owner

A reported scenario should be validated against the application's intended behavior and runtime environment before being treated as a confirmed production defect.

## Evidence and coverage matter

A review result should be interpreted within the analyzed scope. Partial or skipped stages should not be treated as repository-wide conclusions.

When UnvibeCode publishes a business-risk finding, the intended standard is to connect the finding to the affected workflow and supporting code evidence so it can be independently investigated and validated.
