---
name: implement-agentic-tool-execution-workflow
description: Implement features or fixes for Agentic Tool Execution and Permission Boundary. Use when building tool registration, schema validators, sandboxing isolation, human approvals, or secret redactors.
---

# Implement Agentic Tool Execution Workflow

Follow architecture guidelines during implementation:
- Implement strict JSON schema validation for all tool arguments using validated Pydantic or JSONSchema parsers
- Enforce explicit authorization scope verification before dispatching tool tasks
- Add human approval confirmation workflows for destructive or side-effecting tools
- Isolate tool process execution using container sandboxes or restricted process environments
- Apply regex secret redactors to tool outputs before returning responses to orchestrators or logs
- Implement timeout limits and recursion counters to prevent resource exhaustion
