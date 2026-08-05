# Paths and Edge Cases

## Supported paths
- Schema-constrained generation
- Free-text generation with field-level business validation
- Safety-blocked or refused request
- Malformed output with bounded repair
- Truncated or token-limit output
- Streaming or non-streaming provider response
- Cached or idempotent result where allowed
- Provider uncertainty, fallback, reconciliation, and manual review

## Normal paths
- A valid request returns one schema-valid output using only authorized context
- Allowed content passes safety and field-level business validation
- An initially malformed model response is repaired within an explicit bounded policy

## Denied paths
- Required input, context, schema, or model configuration is missing or invalid
- The requester cannot use the referenced context or generation capability
- Prompt or context attempts to override protected system rules
- The output is unsafe, truncated, unparseable, or violates the business schema

## Timing, concurrency, and boundaries
- Two equivalent generation requests execute together
- Input or output reaches token, length, cost, or timeout boundary
- Prompt, model, schema, or policy version changes during retry
- Provider succeeds but the response is lost
- Accepted output persists but downstream consumption fails

Cover valid, invalid, duplicate, stale, replayed, repeated, simultaneous, partially completed, unauthorized, unsafe, and recovery outcomes.

