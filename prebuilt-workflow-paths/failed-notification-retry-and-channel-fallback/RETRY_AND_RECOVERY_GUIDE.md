# Retry and Recovery Guide

## Partial failures
- Failure records but retry scheduling fails
- Retry job schedules but message state update fails
- Worker submits to provider but acknowledgement is lost
- Primary provider accepts while fallback scheduling starts
- Fallback delivers but local final-state update fails
- Final failure commits but alert or support-case creation fails

## Recovery rules
- Re-read authoritative message, delivery, expiry, recipient, tenant, and permission state before every attempt.
- Use one stable message identity and unique attempt identity across jobs, providers, and callbacks.
- Cancel or no-op obsolete jobs when delivery, suppression, expiry, or final failure is already authoritative.
- Do not retry an uncertain provider outcome until reconciliation or explicit policy permits it.
- Make final failure, dead-letter, alert, and manual repair visible without enabling uncontrolled replay.

