---
name: implement-fraud-risk-decision
description: Implement or modify Fraud-risk Scoring, Step-up, Block, and Case Creation. Use when adding or changing validation, authorization, policy, state transitions, external effects, retries, recovery, privacy controls, monitoring, or tests.
---

# Implement Fraud-risk Decision and Step-up

Confirm:
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

Follow project conventions and protect:
- Every decision must bind the current protected action, actor, account, tenant, and feature snapshot
- Only trusted fresh signals and approved model, rule, and policy versions may decide
- Threshold and missing-data behavior must be deterministic and explicit
- Step-up proof must bind the same unexpired decision and action
- Enforcement and case effects must match the authoritative decision exactly once
- Overrides must use scoped authority, evidence, reason, and audit
- Retries and replays must not duplicate or bypass risk controls
- Signals, scores, rules, personal data, and credentials must remain protected

Add all core tests and summarize decisions, files, state changes, recovery, privacy and security controls, and remaining gaps.

