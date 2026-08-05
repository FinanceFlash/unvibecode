# Retry and Recovery Guide

## Partial failures
- Provider returns output but local validation cannot complete
- Output validates but persistence or downstream handoff fails
- Streaming sends partial content before safety or schema failure
- Usage or cost records fail after generation
- Moderation service fails after provider output exists
- Repair succeeds but the original request response is lost

## Recovery rules
- Keep request, prompt, model, schema, policy, and tenant versions bound throughout retry.
- Do not expose raw or partial output as accepted content.
- Revalidate any recovered provider result before persistence or handoff.
- Bound provider retries, repair attempts, token usage, latency, and cost.
- Reconcile accepted output, downstream effect, usage, cost, safety, and audit records.

