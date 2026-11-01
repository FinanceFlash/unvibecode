---
name: review-agentic-tool-execution-risk
description: Review business risks in Agentic Tool Execution and Permission Boundary implementations. Use when identifying unauthorized actions, sandbox escapes, unvalidated arguments, secret leaks, missing HITL approvals, or unhandled tool failures.
---

# Review Agentic Tool Execution Business Risks

Analyze implementation code for tool calling and security boundaries:
- Verify that tool input arguments are strictly validated against JSON schemas before execution
- Check that role-based access control (RBAC) is enforced for every tool invocation session
- Ensure destructive or high-risk tool operations require explicit human confirmation
- Confirm that tool execution occurs within an isolated sandbox environment with resource limits
- Verify that output sanitization filters strip internal secrets or private API tokens before returning data to LLM context
- Check for loop controls that prevent recursive tool invocation storms
- Verify audit log integrity for all side-effecting operations
