# Engineering Guide

## Architecture and Components

The tool execution system acts as a secure proxy layer between non-deterministic LLM output and internal infrastructure.

```text
+----------------+      +-------------------+      +-------------------+      +------------------+
| LLM Controller | ---> | Tool Registry     | ---> | Authorization &   | ---> | Execution        |
| (Function Call)|      | (Schema Validator)|      | HITL Consent Gate |      | Sandbox / Worker |
+----------------+      +-------------------+      +-------------------+      +------------------+
                                                                                       |
                                                                                       v
                                                                              +------------------+
                                                                              | Output Filter &  |
                                                                              | Audit Log Engine |
                                                                              +------------------+
```

## Key Technical Controls

1. **Schema Enforcement**: Input arguments must strictly adhere to Pydantic/JSON schemas. Unknown parameters or type coercions must fail closed.
2. **Permission Boundary**: Tool definitions declare required scopes (e.g., `read:files`, `write:database`). Execution fails if the session context lacks matching claims.
3. **Resource Caps**: Executions are limited by strict timeouts (e.g., 10 seconds), max memory (e.g., 256MB), and bounded output tokens.
4. **Credential Decoupling**: Tools receive scoped, short-lived tokens or worker secrets injected at execution time, never raw long-lived user credentials.
5. **Output Filtering**: Result text passes through regex redactors to prevent secret leak (JWTs, AWS keys, private IPs) back to LLM context.
