# UnvibeCode Limits and Review Boundaries

This page explains hosted-analysis limits and review boundaries. The local graph source can be run separately without an API key or source upload.

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

This threshold measures estimated repository source tokens, not a single model request or context window. The Python package also limits uploads to 50 MiB compressed, 200 MiB of source, 10,000 files and 10 MiB per file. These upload limits apply before hosted analysis.

Hosted AI analysis uses our OpenAI API credentials. We will introduce bring-your-own-key support shortly, so you can use your own API credentials.

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
