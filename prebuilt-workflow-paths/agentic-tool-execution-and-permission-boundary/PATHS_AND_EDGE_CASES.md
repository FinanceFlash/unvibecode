# Paths and Edge Cases

## Complex Workflow Paths

1. **Multi-Tool Chaining**: The agent requests `tool_A` followed immediately by `tool_B` using `tool_A` output.
   - *Control*: Each step in the chain re-evaluates session permissions and timeout budgets. Context size is checked prior to passing output downstream.
2. **Asynchronous Long-Running Execution**: A tool triggers a batch job taking longer than synchronous HTTP response windows.
   - *Control*: Tool returns a `task_id` with status `PENDING`. The orchestrator polls or listens for webhook completion rather than holding open socket connections.

## Boundary Edge Cases

- **Non-Serializable Returns**: Tool returns complex Python/Go objects (e.g., raw sockets, circular refs) that fail JSON encoding.
  - *Handling*: Handlers convert outputs to primitive dicts or stringify via fallbacks before passing to the output filter.
- **Interrupted User Sessions**: The user closes the UI tab while an interactive HITL approval prompt is pending.
  - *Handling*: Pending approval tokens automatically expire after a configurable TTL (e.g., 5 minutes), aborting execution cleanly.
- **Concurrent Identical Calls**: Two agent threads request the exact same mutation tool simultaneously.
  - *Handling*: Idempotency keys bound to the request hash prevent double execution.
