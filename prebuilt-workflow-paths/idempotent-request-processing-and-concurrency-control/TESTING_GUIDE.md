# Testing Guide

Check authoritative records, state-mutating effects, concurrency outcomes, key bindings, lock states, and audit—not only responses.

## 1. New request with valid key is processed once

**Given:** A client submits a state-mutating request with a valid, unused idempotency key

**When:** The request is processed

**Expect:** The effect is applied exactly once, the key is bound to the request fingerprint, and the result is stored

**Must not happen:** The effect is applied more than once or the key is left unbound

**Best test levels:** Integration and end-to-end.

## 2. Duplicate request returns original stored result

**Given:** A completed request exists for the same idempotency key and matching fingerprint

**When:** The same request is submitted again

**Expect:** The stored original result is returned without re-executing the operation

**Must not happen:** The operation re-executes or returns a different result

**Best test levels:** API and integration.

## 3. Retried request after transient failure replays safely

**Given:** The original request failed transiently after key binding but before effect completion

**When:** The client retries with the same key

**Expect:** The system detects the incomplete state, safely completes or replays, and returns a consistent result

**Must not happen:** Retry creates a second effect or loses the original outcome

**Best test levels:** Integration with injected failure.

## 4. Idempotency key is missing or empty

**Given:** A state-mutating request arrives without an idempotency key or with an empty value

**When:** Key validation runs

**Expect:** The request is rejected with a clear error before any effect

**Must not happen:** The request proceeds without idempotency protection

**Best test levels:** Unit and API.

## 5. Key format is invalid or exceeds length limit

**Given:** The idempotency key contains prohibited characters, exceeds the maximum length, or uses an invalid format

**When:** Key validation runs

**Expect:** The request is rejected with a descriptive error

**Must not happen:** A malformed key is silently accepted and stored

**Best test levels:** Unit and property.

## 6. Key is reused with a different payload

**Given:** A completed idempotency key is submitted with a materially different amount, operation, resource, or parameter set

**When:** Payload-mismatch detection runs

**Expect:** The request is rejected without executing the new payload

**Must not happen:** The changed payload executes under the original key

**Best test levels:** Security and integration.

## 7. Key is reused by a different actor or tenant

**Given:** A valid idempotency key created by one actor or tenant is submitted by another

**When:** Key ownership is checked

**Expect:** The request is denied because the key does not belong to the requesting actor or tenant

**Must not happen:** A foreign key controls another actor's operation

**Best test levels:** Authorization and security.

## 8. Two requests with the same key arrive simultaneously

**Given:** Two concurrent requests carry the same idempotency key and identical payloads

**When:** Both attempt to process

**Expect:** Exactly one request executes the effect; the other waits and receives the stored result or is safely rejected

**Must not happen:** Both execute the effect before duplicate detection completes

**Best test levels:** Concurrency integration.

## 9. Lock is acquired for a contested resource

**Given:** Two concurrent requests target the same resource requiring serialized access

**When:** Both attempt to acquire a lock

**Expect:** One acquires the lock and proceeds; the other waits, retries, or receives a conflict response

**Must not happen:** A second requester proceeds without waiting or is silently ignored

**Best test levels:** Concurrency integration.

## 10. Lock holder crashes before releasing

**Given:** A process holding a distributed lock terminates unexpectedly

**When:** Lock expiry or health-check runs

**Expect:** The lock is released after the lease expires, and waiting requests can proceed

**Must not happen:** The lock remains held indefinitely and blocks all subsequent requests

**Best test levels:** Integration with process termination.

## 11. Optimistic concurrency check detects a conflict

**Given:** Two concurrent processes read the same resource version and attempt to write

**When:** The second write is attempted

**Expect:** The conflict is detected, the second write is rejected, and the caller can read the current state and retry

**Must not happen:** The stale write overwrites the concurrent update and loses data

**Best test levels:** Concurrency integration.

## 12. Key-store becomes unavailable during processing

**Given:** The idempotency-key store (database, cache, or coordination service) is unreachable

**When:** A state-mutating request arrives

**Expect:** The system applies a documented degradation policy: reject, queue, or proceed with compensating controls

**Must not happen:** All state-mutating requests fail catastrophically without degradation

**Best test levels:** Chaos and integration.

## 13. Key expires while a legitimate retry is in flight

**Given:** A key's expiry time passes while the original client is preparing a retry

**When:** The retry arrives after expiry

**Expect:** The system applies an explicit expiry policy: reject with a clear error or extend the key window

**Must not happen:** Expiry permits silent re-execution of the completed operation

**Best test levels:** Unit with controlled time and integration.

## 14. Stored response is evicted before client retries

**Given:** Cache pressure or a storage limit causes the original response to be evicted

**When:** The client retries with the same key

**Expect:** The system reconstructs the result from authoritative state or rejects with a clear error requiring a new key

**Must not happen:** Retry creates a second effect because the original proof is lost

**Best test levels:** Integration with storage-pressure simulation.

## 15. Operation succeeds but response storage fails

**Given:** The downstream effect commits, but writing the result to the key store fails

**When:** The client retries

**Expect:** The system detects the completed effect, stores the result, and returns it without re-execution

**Must not happen:** The client retries, finds no stored result, and the effect doubles

**Best test levels:** Integration with injected storage failure.

## 16. Downstream effect partially fails after key is bound

**Given:** The key is bound and some downstream effects succeed while others fail

**When:** Recovery or retry runs

**Expect:** The key reflects the incomplete state, remaining effects complete or compensate, and the key transitions to completed or failed

**Must not happen:** Partial state persists with the key marked as completed

**Best test levels:** Integration.

## 17. Lock lease is renewed by a slow operation

**Given:** A lock-holding process attempts to extend its lease because the operation is taking longer than expected

**When:** Lease renewal is requested

**Expect:** Renewal succeeds within policy limits, or the process releases the lock and stops mutating state

**Must not happen:** Lease renewal extends beyond the maximum permitted hold time

**Best test levels:** Unit with controlled time.

## 18. Concurrent optimistic writes target the same version

**Given:** Multiple writers read the same version and prepare updates simultaneously

**When:** Both conditional writes execute

**Expect:** Exactly one write succeeds; others receive a version conflict and must re-read before retrying

**Must not happen:** Both writes succeed, producing a lost update or inconsistent state

**Best test levels:** Concurrency integration.

## 19. Request fingerprint contains sensitive data

**Given:** The request includes personal data, credentials, payment tokens, or secrets in fingerprinted fields

**When:** The fingerprint is computed and stored

**Expect:** Sensitive fields are excluded, hashed, or redacted before storage, and stored fingerprints comply with retention policy

**Must not happen:** Personal data, credentials, or secrets persist in fingerprint storage

**Best test levels:** Security and log inspection.

## 20. Key garbage collection runs during peak traffic

**Given:** The key store triggers expired-key cleanup while the system is under high request load

**When:** Garbage collection executes

**Expect:** Collection runs incrementally, respects concurrency limits, and does not degrade live request latency beyond acceptable thresholds

**Must not happen:** Collection latency or lock contention degrades live request processing

**Best test levels:** Load and operations.
