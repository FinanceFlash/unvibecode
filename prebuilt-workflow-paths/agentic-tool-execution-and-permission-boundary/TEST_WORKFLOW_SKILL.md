---
name: test-agentic-tool-execution-workflow
description: Test features, edge cases, and security boundaries for Agentic Tool Execution and Permission Boundary. Use when writing unit, integration, or security tests for tool invocation and sandboxing.
---

# Test Agentic Tool Execution Workflow

Design comprehensive test suites:
- Test valid tool execution returns expected schema-compliant JSON payloads
- Test invalid argument payloads trigger immediate HTTP 400 validation failures
- Test unauthorized session tokens receive HTTP 403 Forbidden responses
- Test human approval rejection halts tool execution without side effects
- Test timeout enforcement terminates long-running tool processes cleanly
- Test output redactors filter API secrets and raw connection strings from results
