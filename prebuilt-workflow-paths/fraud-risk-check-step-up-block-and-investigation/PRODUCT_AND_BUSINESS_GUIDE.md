# Product and Business Guide

## Boundary
Starts when a protected customer or business action supplies identity, session, device, transaction, and behavioral signals. Ends when the action is allowed, challenged, held, blocked, or routed to an investigation case with enforcement and customer state recorded consistently.

## People and systems
- Customer or protected-action initiator
- Application, payment, account, or transaction service
- Fraud rules and risk-decision service
- Feature, device, identity, and model services
- Step-up authentication service
- Fraud analyst or authorized reviewer
- Case, enforcement, notification, security, and operations teams

## Things created or changed
- Protected action and business object
- Actor, account, tenant, session, device, network, payment, and behavioral signals
- Feature snapshot, source time, freshness, and quality result
- Rule set, model, model version, score, reason, threshold, and policy version
- Decision, expiry, idempotency key, and enforcement instruction
- Challenge, hold, block, override, and release
- Fraud case, evidence, status, notification, and audit record

## Stages
- Action: pending risk decision → allowed, challenged, held, blocked, cancelled, or uncertain
- Challenge: absent → required → pending → passed, failed, expired, or cancelled
- Case: absent → opened → assigned → resolved, escalated, or closed
- Enforcement: pending → applied, failed, reversed, or exception

## Product decisions
- Which actions require real-time, asynchronous, or no fraud decision
- Required signals, freshness, missing-value, quality, and trusted-source policy
- Rule, model, feature, and policy version selection
- Score calibration, threshold, reason code, and action mapping
- Step-up method, attempts, lifetime, bypass, fallback, and recovery
- Fail-open, fail-closed, hold, or manual-review behavior during dependency failure
- Decision lifetime and whether a changed action requires rescoring
- Who may override, release, or close a case and what evidence is required
- Customer communication, explanation, appeal, and support policy
- Privacy, fairness, monitoring, drift, adversarial probing, rate, and retention controls

## Happy paths
- A low-risk valid action is allowed once under the current policy
- A medium-risk action passes the required step-up and resumes safely
- A high-risk action is blocked or held and creates the required investigation case

## Negative paths
- Required action, actor, feature, model, rule, or policy data is missing or invalid
- Signals are stale, contradictory, poisoned, or belong elsewhere
- The actor cannot perform the protected action or reviewer cannot override
- A challenge is wrong, expired, replayed, bypassed, or belongs to another decision

## Edge cases
- Two risk decisions or enforcement actions run for the same business action
- Score lies exactly on an allow, challenge, hold, or block threshold
- Signals, model, rules, or policy change during challenge or retry
- Model succeeds but the service response is lost
- Late challenge or analyst result arrives after action expiry, block, or completion

## Acceptance criteria
1. Only an eligible authorized action may be evaluated and executed
2. Action, actor, account, tenant, signals, feature snapshot, model, rules, policy, and decision must remain bound
3. Threshold boundaries and missing-signal behavior must be explicit and testable
4. Allowed, challenged, held, blocked, and uncertain states must not be confused
5. Challenge proof must bind the same current decision and action
6. Manual override and release must use scoped authority, reason, evidence, and immutable audit
7. Repeated or simultaneous evaluation must not duplicate action, hold, block, or case effects
8. Model or dependency failure must follow explicit fail-open, fail-closed, hold, or review policy
9. Sensitive signals, scores, rules, customer data, provider credentials, and analyst evidence must remain protected
10. Decision quality, drift, false positives, false negatives, enforcement, latency, and case outcomes must remain observable

## Business risks
| Risk | Business consequence |
|---|---|
| Fraud allowed | Missing, stale, manipulated, or incorrectly scored signals permit harmful action |
| Legitimate customer blocked | Bad thresholds or features create customer loss and support cost |
| Step-up bypass | Challenge state or proof is detached from the protected action |
| Enforcement divergence | Decision says block or hold but the transaction or account proceeds |
| Unauthorized override | An actor releases a block or closes a case outside authority |
| Cross-tenant signal contamination | Another customer's behavior changes the decision |
| Adversarial probing | Repeated requests reveal thresholds or evade controls |
| Sensitive-data exposure | Device, identity, payment, scores, rules, or evidence reach unsafe logs |

