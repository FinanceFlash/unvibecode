# 10 — Observability: Make Failure Explain Itself

> If users can feel a failure but operators cannot see it, the system is not observable.

```mermaid
flowchart LR
    A["User or business symptom"] --> B["Logs, metrics, traces"]
    B --> C["Actionable alert"]
    C --> D["Diagnosis"]
    D --> E["Recover + learn"]
```

## Stop and answer

- [ ] Which user-visible and business-visible symptoms mean the feature is unhealthy even when servers are running?
- [ ] Which structured logs, traces, event metadata, and correlation IDs explain one operation end to end?
- [ ] Which latency, traffic, error, saturation, queue, dependency, cost, and outcome metrics matter?
- [ ] Which silent failures—stalled jobs, dropped events, delayed workflows, partial writes, missing notifications, or drift—need detection?
- [ ] What service-level objectives or error budgets define acceptable reliability?
- [ ] Which alerts require action, who receives them, and what decision or runbook follows?
- [ ] Can operators distinguish code failure from dependency failure, bad data, bad configuration, exhausted capacity, and user misuse?
- [ ] Can failed work be inspected, retried, replayed, cancelled, compensated, or quarantined safely?
- [ ] Is telemetry useful without leaking secrets, personal data, or confidential payloads—or creating uncontrolled cost?
- [ ] Can the team inject a realistic failure and diagnose and recover using only its signals and runbooks?

## Warning signs

- Dashboards show server health but no completed business outcomes.
- Alerts describe symptoms without an owner or next action.
- Logs are either too vague to diagnose or so detailed they expose sensitive data.

## Evidence before code

- User, technical, and business signals
- End-to-end correlation plan
- SLOs, dashboards, and actionable alerts
- Safe retry/replay/cancellation controls
- Failure drill and owned runbooks

## Ask an LLM or reviewer

> “Assume this system fails silently at 3 a.m. Show which signals reveal the user impact, where diagnosis loses correlation, which alerts are noisy or missing, and what recovery action operators still lack.”
