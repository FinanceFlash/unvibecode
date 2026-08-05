# Testing Guide

Check authoritative identity, permission, run ownership, input windows, effects, checkpoints, recovery, and audit—not only process exit codes.

## 1. Due job runs once

**Given:** An enabled job has one due schedule occurrence and a valid bounded input window

**When:** Schedulers evaluate and a worker claims the run

**Expect:** One effective owner processes the window and records effects, checkpoint, and completion

**Must not happen:** The occurrence is missed or executed by multiple effective owners

**Best test levels:** Integration and end-to-end.

## 2. No-work run records truthful outcome

**Given:** A valid run window contains no eligible items

**When:** The source is queried and completion is evaluated

**Expect:** The run records no work and applies the documented checkpoint rule

**Must not happen:** No work is confused with failure or a cursor skips unseen data

**Best test levels:** Integration.

## 3. Missed occurrence follows catch-up policy

**Given:** The scheduler was unavailable past one or more due times

**When:** Service resumes within or beyond the misfire grace period

**Expect:** Only the configured catch-up, backfill, or skip behavior occurs with explicit windows

**Must not happen:** Every missed time floods the system or required work disappears silently

**Best test levels:** Controlled-time integration.

## 4. Required job data is missing

**Given:** Schedule, timezone, tenant, handler, run identity, window, checkpoint, or secret reference is absent

**When:** Configuration or run validation executes

**Expect:** The job remains unrunnable and an actionable error is recorded

**Must not happen:** The runner guesses a window, tenant, or credential

**Best test levels:** Unit and configuration.

## 5. Schedule or checkpoint is malformed

**Given:** A cron expression, timezone, cursor, timestamp, page token, or batch setting is invalid

**When:** Parsing and validation run

**Expect:** Unsafe configuration is rejected before work begins

**Must not happen:** Malformed values create an unbounded or incorrect run

**Best test levels:** Unit, property, and configuration.

## 6. Paused job does not run

**Given:** A job is disabled, paused, retired, or excluded by calendar policy

**When:** Its due time or stale queued trigger arrives

**Expect:** The occurrence is skipped or retained exactly as policy defines

**Must not happen:** A stale trigger bypasses current job state

**Best test levels:** Integration.

## 7. Operator cannot trigger or alter job

**Given:** An actor lacks permission for manual run, backfill, cancel, checkpoint edit, or tenant

**When:** The privileged action is attempted

**Expect:** Authorization denies it and records safe audit context

**Must not happen:** Knowledge of a job name grants operational control

**Best test levels:** Authorization and security.

## 8. Timezone and DST are deterministic

**Given:** The schedule crosses normal time, a missing DST hour, and a repeated DST hour

**When:** Due occurrences are generated

**Expect:** The documented timezone and DST policy produces stable unique occurrences

**Must not happen:** A run duplicates or disappears because hosts interpret local time differently

**Best test levels:** Controlled-time integration.

## 9. Two schedulers claim one run

**Given:** Two coordinators attempt to acquire the same due occurrence concurrently

**When:** Both write claims

**Expect:** Only one valid lease or permitted partition owns the work

**Must not happen:** Both workers create duplicate business effects

**Best test levels:** Concurrency integration.

## 10. Item lies on window boundary

**Given:** Records exist immediately before, exactly at, and immediately after start and end boundaries

**When:** The scheduled query and next run execute

**Expect:** Each eligible record is processed once according to documented inclusivity

**Must not happen:** A boundary record is skipped or processed twice

**Best test levels:** Database integration with controlled data.

## 11. Claim response is lost

**Given:** A lease may have been acquired but the scheduler sees a timeout

**When:** The claim attempt repeats

**Expect:** The same owner resumes or authoritative lease state prevents duplicate ownership

**Must not happen:** A lost response creates two effective owners

**Best test levels:** Integration and fault injection.

## 12. Completed run is replayed

**Given:** A due event, manual request, or orchestration message for a completed run repeats

**When:** Replay handling executes

**Expect:** The recorded completion is returned or safe repair is explicitly requested

**Must not happen:** Completed effects and checkpoint advancement repeat

**Best test levels:** Integration.

## 13. Retries threaten shared capacity

**Given:** Many runs or items fail together and become eligible for retry

**When:** Retry control activates

**Expect:** Attempts, concurrency, backoff, jitter, circuit breaking, and budget contain load

**Must not happen:** Retries synchronize and amplify the dependency outage

**Best test levels:** Load and resilience.

## 14. Outputs commit but checkpoint fails

**Given:** One or more business effects are durable but checkpoint persistence fails

**When:** The run retries or is taken over

**Expect:** Receipts and idempotency prevent repeated effects before checkpoint recovery

**Must not happen:** Effects duplicate or the checkpoint advances without evidence

**Best test levels:** Integration and fault injection.

## 15. External dependency times out

**Given:** A provider or datastore gives an uncertain result

**When:** Timeout handling executes

**Expect:** The item stays uncertain until status is reconciled or an idempotent retry resolves it

**Must not happen:** Timeout is assumed to be a clean failure or success

**Best test levels:** Dependency contract and resilience.

## 16. Checkpoint commits but response is lost

**Given:** The checkpoint and completion may be durable while the runner sees failure

**When:** The run or occurrence repeats

**Expect:** Authoritative state returns the existing result without advancing again

**Must not happen:** The next window or effects are duplicated

**Best test levels:** Integration.

## 17. Cross-tenant job data is supplied

**Given:** Run configuration, checkpoint, input, or secret reference belongs to another tenant

**When:** Ownership checks execute

**Expect:** The run is denied before data or effects cross boundaries

**Must not happen:** A global job key mixes tenant state

**Best test levels:** Authorization and privacy.

## 18. Job failure is logged

**Given:** Inputs, outputs, provider payloads, credentials, or personal data are present during failure

**When:** Diagnostics are emitted

**Expect:** Logs contain safe identifiers and approved metadata only

**Must not happen:** Secrets or sensitive records appear in logs, alerts, or run consoles

**Best test levels:** Security and log inspection.

## 19. Lease expires while worker continues

**Given:** A slow worker loses its lease and a replacement obtains current authority

**When:** Both reach an effect or checkpoint commit

**Expect:** Fencing permits only the current owner to commit, while idempotency protects external effects

**Must not happen:** The stale worker overwrites the replacement or advances the cursor

**Best test levels:** Concurrency and fault injection.

## 20. Partial batch is recovered

**Given:** A batch has successful, failed, poison, skipped, and uncertain items

**When:** Run completion and recovery execute

**Expect:** The summary is truthful and unresolved items remain bounded, visible, and repairable

**Must not happen:** The whole batch is marked successful or one bad item blocks all future runs forever

**Best test levels:** Integration and operations.

