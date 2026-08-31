# Testing Guide

## Validation Strategy

Testing tool execution and permission boundaries requires unit, integration, and security tests spanning happy paths, parameter validation, authorization boundaries, sandboxing, and fault tolerance.

## Test Suites and Scenarios

### 1. Happy Path & Schema Validation Tests
- **Valid Tool Call**: Execute a registered tool (e.g., `search_database`) with schema-compliant JSON. Assert HTTP 200/success status and structured JSON response.
- **Invalid Parameters**: Supply missing required fields or incorrect types. Verify 400 Validation Error and zero tool invocation.

### 2. Authorization & Human-in-the-Loop Tests
- **Scope Enforcement**: Invoke a write tool (e.g., `delete_record`) with a read-only session token. Assert HTTP 403 Forbidden.
- **HITL Confirmation**: Trigger a high-risk tool. Verify execution pauses until approval token is posted; verify rejection aborts execution without side effects.

### 3. Sandboxing & Security Boundary Tests
- **Command Injection Prevention**: Pass arguments containing shell characters (`; rm -rf /`, `$(whoami)`). Verify arguments are properly escaped or rejected.
- **Path Traversal Isolation**: Pass file paths like `../../etc/passwd`. Assert access is strictly restricted to sandbox workdir.
- **Secret Redaction**: Mock tool returning `{"api_key": "sk-proj-12345"}`. Assert output filter redacts key to `[REDACTED_SECRET]`.

### 4. Resiliency & Failure Recovery Tests
- **Timeout Termination**: Force a test tool handler to sleep 30s when max timeout is 5s. Assert execution terminates cleanly with timeout error.
- **Circuit Breaking**: Simulate 5 consecutive tool failures. Verify circuit breaker opens and rejects subsequent calls instantly.
