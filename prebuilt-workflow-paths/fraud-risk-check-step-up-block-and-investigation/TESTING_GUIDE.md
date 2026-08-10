# Testing Guide

Check the protected action, authoritative decision, enforcement, challenge, case, privacy, and recovery—not only the returned score.

## 1. Low-risk action is allowed

**Given:** An eligible action has fresh trusted signals and the current policy returns low risk

**When:** Risk evaluation completes

**Expect:** The same action is allowed once with its decision version recorded

**Must not happen:** Another action or stale score is allowed

**Best test levels:** Integration and end-to-end.

## 2. Step-up passes and resumes action

**Given:** A current decision requires a challenge bound to one action and actor

**When:** Valid proof is submitted before expiry

**Expect:** The same action resumes under the documented rescoring policy

**Must not happen:** Proof authorizes another action or bypasses rescoring policy

**Best test levels:** End-to-end and security.

## 3. High-risk action is blocked and cased

**Given:** Current signals cross the block or investigation threshold

**When:** Enforcement runs

**Expect:** The action is blocked and one correlated case is created

**Must not happen:** The action proceeds or cases duplicate

**Best test levels:** Integration.

## 4. Required risk data is missing

**Given:** A required identity, device, transaction, or behavioural signal is absent

**When:** Evaluation starts

**Expect:** The explicit missing-data policy rejects, holds, challenges, or reviews the action

**Must not happen:** Missing data silently becomes low risk

**Best test levels:** Unit and API.

## 5. Signal or feature is malformed

**Given:** A feature is out of range, incorrectly typed, non-finite, or structurally invalid

**When:** Feature validation runs

**Expect:** The input is rejected or handled by an explicit safe policy

**Must not happen:** Bad values distort score or crash evaluation

**Best test levels:** Unit and property.

## 6. Signals or model are stale

**Given:** A signal snapshot, model, rules, or policy exceeds its approved lifetime

**When:** A current action is evaluated

**Expect:** Fresh data is obtained or the documented unavailable policy applies

**Must not happen:** Stale risk state authorizes current action

**Best test levels:** Integration with controlled time.

## 7. Reviewer cannot override

**Given:** An authenticated actor lacks the scoped reviewer permission

**When:** They attempt to release a hold, override a decision, or close a case

**Expect:** Authorization denies the action and records the attempt safely

**Must not happen:** A case identifier grants privileged control

**Best test levels:** Authorization and security.

## 8. Identity and device formats differ

**Given:** Equivalent identifiers arrive in supported case, encoding, or formatting variants

**When:** Signals are normalized and joined

**Expect:** Approved canonicalization preserves the correct account and device boundary

**Must not happen:** Formatting fragments risk history or crosses accounts

**Best test levels:** Unit and property.

## 9. Duplicate decisions run together

**Given:** Two workers evaluate the same protected action concurrently

**When:** Both attempt to persist and enforce a decision

**Expect:** One authoritative compatible decision and effect set remains

**Must not happen:** One allows while another blocks or cases duplicate

**Best test levels:** Concurrency integration.

## 10. Score reaches threshold boundary

**Given:** Scores lie immediately below, exactly on, and immediately above each threshold

**When:** Policy mapping runs

**Expect:** One documented inclusive or exclusive rule determines each outcome

**Must not happen:** Floating-point or service differences change outcomes

**Best test levels:** Unit and property.

## 11. Decision response is lost

**Given:** A decision and effect may have committed but the caller receives no response

**When:** The same request retries

**Expect:** The original authoritative decision is returned without repeating effects

**Must not happen:** Controls or business action duplicate

**Best test levels:** API and integration.

## 12. Risk event is replayed

**Given:** An already processed event or idempotency key is submitted again

**When:** Evaluation or enforcement runs

**Expect:** Replay protection returns the original outcome or rejects changed input

**Must not happen:** Replay bypasses a block or repeats the transaction

**Best test levels:** Security and integration.

## 13. Fraud endpoint is probed or flooded

**Given:** A source repeatedly varies signals to learn thresholds or exhaust capacity

**When:** Velocity and abuse controls are reached

**Expect:** Requests are bounded without exposing sensitive rules or harming legitimate recovery

**Must not happen:** Thresholds are learned or service capacity is exhausted

**Best test levels:** Security and load.

## 14. Decision commits but challenge fails

**Given:** The challenge decision is stored but challenge creation or delivery fails

**When:** Recovery runs

**Expect:** The action stays non-executable until the same challenge is repaired or safely replaced

**Must not happen:** The action proceeds without proof

**Best test levels:** Integration.

## 15. Model or feature service times out

**Given:** A required dependency returns no reliable outcome

**When:** Failure handling runs

**Expect:** The configured fail-closed, hold, challenge, or review policy is applied visibly

**Must not happen:** Timeout silently becomes allow

**Best test levels:** Contract and integration.

## 16. Block commits but response is lost

**Given:** Enforcement and case creation may have succeeded before communication failed

**When:** The request repeats or status is queried

**Expect:** The existing block and case are found and returned

**Must not happen:** Duplicate cases or contradictory allow occurs

**Best test levels:** Integration.

## 17. Cross-tenant signals are supplied

**Given:** A valid actor submits signal, action, or case identifiers from another tenant

**When:** Risk evaluation or review is requested

**Expect:** Tenant and object binding deny the request before data or effects cross boundaries

**Must not happen:** Another customer's behaviour affects decision

**Best test levels:** Authorization and security.

## 18. Fraud failure is logged

**Given:** The path contains personal signals, scores, rules, evidence, and provider credentials

**When:** An error occurs

**Expect:** Logs remain useful while redacting protected inputs and decision internals

**Must not happen:** Personal data or threshold logic leaks

**Best test levels:** Security and log inspection.

## 19. Late challenge follows terminal decision

**Given:** A challenge result arrives after expiry, cancellation, block, or completed action

**When:** The result is processed

**Expect:** Current state rejects or records the stale result without reviving the action

**Must not happen:** Stale proof revives an action

**Best test levels:** Integration with controlled time.

## 20. Decision and enforcement disagree

**Given:** A hold or block is authoritative but a downstream protected service did not apply it

**When:** Reconciliation runs

**Expect:** The mismatch is visible, contained, and repaired under policy

**Must not happen:** System reports protection while fraud proceeds

**Best test levels:** Integration and operations.

