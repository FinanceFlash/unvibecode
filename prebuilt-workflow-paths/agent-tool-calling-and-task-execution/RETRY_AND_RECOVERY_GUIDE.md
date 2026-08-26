# Retry and Recovery Guide

- **Transient Failures**: Tools should retry with backoff.
- **Idempotency**: Retried tools must not duplicate side effects.
- **Max Iterations**: Agent must have a hard limit on steps to prevent runaway loops.
- **Escalation**: Failed tasks must transition to human review.
