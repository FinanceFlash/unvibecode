---
name: review-fraud-risk-decision-risk
description: Review customer, security, privacy, compliance, and operational risks in Fraud-risk Scoring, Step-up, Block, and Case Creation. Use when founders, PMs, or engineering managers need prioritized consequences, controls, tests, and release concerns.
---

# Review Fraud-risk Decision and Step-up Risk

Review entry, identity, authorization, policy, state, timing, concurrency, external effects, retry, recovery, privacy, and support paths. Prioritize:
- Fraud allowed — Missing, stale, manipulated, or incorrectly scored signals permit harmful action
- Legitimate customer blocked — Bad thresholds or features create customer loss and support cost
- Step-up bypass — Challenge state or proof is detached from the protected action
- Enforcement divergence — Decision says block or hold but the transaction or account proceeds
- Unauthorized override — An actor releases a block or closes a case outside authority
- Cross-tenant signal contamination — Another customer's behavior changes the decision
- Adversarial probing — Repeated requests reveal thresholds or evade controls
- Sensitive-data exposure — Device, identity, payment, scores, rules, or evidence reach unsafe logs

For each material risk, explain trigger, behavior, business consequence, protection, decision or test, and acceptance condition.

