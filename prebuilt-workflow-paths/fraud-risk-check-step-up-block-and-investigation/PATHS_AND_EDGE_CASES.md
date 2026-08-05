# Paths and Edge Cases

## Supported paths
- Low-risk allow
- Medium-risk step-up then allow
- Step-up failure or expiry
- High-risk hold or block
- Case creation and analyst review
- Authorized override or release
- Model, feature, or authentication dependency failure
- Reevaluation, reconciliation, appeal, and manual repair

## Normal paths
- A low-risk valid action is allowed once under the current policy
- A medium-risk action passes the required step-up and resumes safely
- A high-risk action is blocked or held and creates the required investigation case

## Denied paths
- Required action, actor, feature, model, rule, or policy data is missing or invalid
- Signals are stale, contradictory, poisoned, or belong elsewhere
- The actor cannot perform the protected action or reviewer cannot override
- A challenge is wrong, expired, replayed, bypassed, or belongs to another decision

## Timing, concurrency, and boundaries
- Two risk decisions or enforcement actions run for the same business action
- Score lies exactly on an allow, challenge, hold, or block threshold
- Signals, model, rules, or policy change during challenge or retry
- Model succeeds but the service response is lost
- Late challenge or analyst result arrives after action expiry, block, or completion

Cover valid, invalid, duplicate, stale, replayed, repeated, simultaneous, partially completed, unauthorized, expired, and recovery outcomes.

