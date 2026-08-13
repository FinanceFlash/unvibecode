# AI Engineering Cheatsheet

Practical, pre-build guides for engineers working with teammates, reviewers, and LLMs on Production environment.

Use each series before implementation to surface unclear requirements, missing business paths, architectural risks, failure scenarios, and operational gaps.

## Available guides and series

### [Smart Questions Before You Build](./smart_questions_before_you_build/)

Eleven focused guides covering:

- Requirements
- Backend
- Frontend
- Data
- Events
- Business workflows
- System design
- DevOps
- Security
- Testing
- Observability

Each guide includes a compact visual, ten critical questions, warning signs, evidence to collect, and a prompt for challenging the design with an LLM or reviewer.

### [AI Coding Design and Architecture Principles](./AI_CODING_DESIGN_AND_ARCHITECTURE_PRINCIPLES.md)

Eight practical principles for building coding agents, repository analyzers, developer tools, plugins, and multi-agent workflows. Covers composability, maintainability, context, contracts, deterministic controls, bounded agency, evidence, evaluation, and observability.

### [Production Anti-Patterns for LLMs, RAG, and AI Agents](./AI_PRODUCTION_ANTI_PATTERNS_LLM_RAG_AGENTS.md)

Twenty-six production failure patterns with symptoms, failure mechanisms, safer replacements, and ship checks. Includes a production launch gate for model behaviour, retrieval, agent actions, and operations.

### [40 AI and LLM Production Trade-Offs](./40_AI_LLM_PRODUCTION_TRADE_OFFS.md)

Forty recurring production decisions across model behaviour, RAG, agents, reliability, safety, evaluation, and operations. Each comparison includes the advantages, disadvantages, and a practical decision rule.

## How to use the cheatsheet

1. Open the guide or series relevant to your change.
2. Answer the questions before writing implementation code.
3. Mark a question as not applicable only with a reason.
4. Challenge assumptions with an LLM and the relevant human reviewers.
5. Record important decisions, risks, and evidence beside the implementation plan or pull request.

The goal is not to add process. The goal is to discover expensive mistakes while they are still cheap to fix.
