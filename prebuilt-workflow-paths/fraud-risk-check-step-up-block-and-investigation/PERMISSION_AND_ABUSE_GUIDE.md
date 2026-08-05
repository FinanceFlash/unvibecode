# Permission and Abuse Guide

## Permission boundaries
- Every decision must bind the current protected action, actor, account, tenant, and feature snapshot
- Only trusted fresh signals and approved model, rule, and policy versions may decide
- Threshold and missing-data behavior must be deterministic and explicit
- Step-up proof must bind the same unexpired decision and action
- Enforcement and case effects must match the authoritative decision exactly once

## Misuse paths
- Fraud allowed — Missing, stale, manipulated, or incorrectly scored signals permit harmful action
- Legitimate customer blocked — Bad thresholds or features create customer loss and support cost
- Step-up bypass — Challenge state or proof is detached from the protected action
- Enforcement divergence — Decision says block or hold but the transaction or account proceeds
- Unauthorized override — An actor releases a block or closes a case outside authority
- Cross-tenant signal contamination — Another customer's behavior changes the decision
- Adversarial probing — Repeated requests reveal thresholds or evade controls
- Sensitive-data exposure — Device, identity, payment, scores, rules, or evidence reach unsafe logs

Protect actor identity, tenant scope, signals or personal data, policy, credentials, privileged tools, and audit records. Deny uncertain identity, ownership, or authority.

