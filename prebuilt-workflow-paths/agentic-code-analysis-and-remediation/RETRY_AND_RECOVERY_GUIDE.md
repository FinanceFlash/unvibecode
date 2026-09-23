# Retry and Recovery Guide

## Partial failures

* File index commits but AST extraction fails on a subset of files.
* Reflection loop reaches a conclusion but quota accounting update fails.
* Remediation proposal validates but VCS push fails.
* PR creation succeeds but audit log write fails.
* Provider returns a valid response but the orchestrator connection drops.
* Cancellation signal is received but the current LLM request has already been sent.

## Recovery rules

* Re-read current session state, quota, and sandbox integrity before retrying any effect.
* Bypassing iteration caps or sandbox restrictions because a dependency failed must not happen.
* Make things created or changed visible and repairable, including session, quota, proposal, and VCS state inconsistencies.
* Reconcile ingestion, analysis, remediation, VCS, notification, and audit state across all stages.
* Treat uncertain provider responses as failed, not successful.
