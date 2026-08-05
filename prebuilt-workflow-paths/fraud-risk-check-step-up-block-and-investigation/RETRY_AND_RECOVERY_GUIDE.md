# Retry and Recovery Guide

## Partial failures
- Decision commits but step-up challenge creation fails
- Block or hold commits but protected service enforcement fails
- Case creates but evidence or assignment fails
- Challenge passes but action resumption fails
- Model returns a score but decision persistence fails
- Override commits but downstream release or notification fails

## Recovery rules
- Keep action, actor, feature snapshot, model, rules, policy, decision, and challenge versions correlated.
- Re-read current action and enforcement state before retrying any effect.
- Never bypass risk control solely because a dependency or response failed.
- Make decision–enforcement and decision–case inconsistency visible.
- Reconcile action, decision, challenge, enforcement, case, notification, and audit.

