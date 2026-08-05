# Paths and Edge Cases

## Supported paths
- Single-source grounded answer
- Multi-source synthesis
- Hybrid keyword and vector retrieval
- Follow-up question with authorized conversation context
- Clarification request
- Insufficient-evidence abstention
- Conflicting-source qualification or escalation
- Provider failure, cache invalidation, reconciliation, and manual review

## Normal paths
- An authorized question returns an answer supported by precise accessible citations
- Insufficient evidence produces a clear abstention or clarification request
- Conflicting authoritative sources are represented or escalated instead of silently resolved

## Denied paths
- Question, source scope, index, or required context is missing or invalid
- The requester cannot access one or more candidate sources
- Retrieved documents contain instructions that attempt to control the model
- Evidence is insufficient, stale, deleted, conflicting, or cannot support the answer

## Timing, concurrency, and boundaries
- Index or source changes during retrieval and generation
- Permission is revoked after retrieval but before response
- Question reaches token, latency, top-k, or source-size boundary
- Provider succeeds but the response is lost
- Citation target changes, moves, or becomes unavailable

Cover valid, invalid, duplicate, stale, replayed, repeated, simultaneous, partially completed, unauthorized, unsafe, and recovery outcomes.

