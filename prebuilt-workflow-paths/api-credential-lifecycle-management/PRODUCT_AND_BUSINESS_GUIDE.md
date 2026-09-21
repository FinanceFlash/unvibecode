# Product and Business Guide

## Boundary
Starts when an authorized person or service requests creation, rotation, or revocation of an API credential. Ends when the requested lifecycle action reaches a verified state: the credential is activated, denied, rotated with the previous credential invalidated, revoked, expired, or remains explicitly incomplete with evidence and recovery work recorded.

## People and systems
- Credential owner or authorized service operator
- Platform administrator or security operator
- Credential management service
- Application or service that uses the credential
- Protected API or API gateway
- Audit and security monitoring systems
- Notification or lifecycle-management systems where applicable

## Things created or changed
- API credential and credential identifier
- Credential owner, assigned application or service, and permission scope
- Credential lifecycle state, creation time, expiry time, and rotation history
- Credential activation, rotation, and revocation records
- Audit record for lifecycle actions and their outcomes
- Recovery or reconciliation record for incomplete lifecycle operations
- Expiry or lifecycle notification state where applicable

## Stages
- Request: requested → authorization pending → approved, denied, or cancelled
- Provisioning: generation pending → generated → activation pending → active or failed
- Active credential: active → nearing expiry → expired, rotating, or revoked
- Rotation: requested → replacement provisioning → replacement active → old credential invalidated → completed, or partial/incomplete
- Revocation: requested → authorized → revoked, or failed/incomplete
- Recovery: inconsistent or incomplete → reconciliation pending → verified final state

## Product decisions
- Who may create, rotate, or revoke a credential and what authorization is required
- Which applications, services, environments, and permission scopes a credential may be assigned to
- Whether credentials have mandatory expiry periods and when expiry warnings begin
- Whether old and new credentials may temporarily overlap during rotation
- When the previous credential must become invalid after successful rotation
- Whether emergency revocation has a separate authorization or execution path
- How compromised credentials are identified, contained, and invalidated
- How duplicate requests and retries are identified and handled
- What lifecycle evidence must be recorded for creation, rotation, expiry, and revocation
- How incomplete or inconsistent lifecycle operations are detected and recovered
- What happens when credential-generation or activation dependencies fail
- Which lifecycle states are authoritative when multiple systems disagree

## Happy paths
- An authorized owner creates a credential with an approved scope, assigns it to the intended service, and activates it successfully
- An authorized rotation creates and activates a replacement credential before the previous credential is invalidated according to the defined rotation policy
- An authorized revocation invalidates the credential and records the completed lifecycle action

## Negative paths
- The requester lacks permission to create, rotate, or revoke the credential
- The requested permission scope is outside the requester's allowed policy
- The credential is assigned to an unauthorized application or service
- An expired or revoked credential attempts to access the protected API
- Credential generation or activation fails before the lifecycle operation completes

## Edge cases
- A client retries a creation request after losing the original response
- Two rotation requests target the same credential concurrently
- The replacement credential is generated but activation or state update fails
- Old and new credentials overlap longer than the defined migration window
- A credential is compromised while a normal rotation is already in progress
- Revocation succeeds but the audit record cannot be written
- Different lifecycle components disagree about the credential's current state

## Acceptance criteria
1. Only an authorized actor or service may create, rotate, or revoke a credential
2. Credential ownership, assignment, scope, and lifecycle state must remain consistently bound
3. A credential must not become usable before required authorization and activation checks complete
4. A credential must not receive permissions beyond the approved scope
5. Expired or revoked credentials must not authorize protected API access
6. A completed rotation must leave the previous credential invalidated according to the defined policy
7. Temporary credential overlap must have a defined purpose, boundary, and termination condition
8. Repeated or concurrent lifecycle requests must not create unintended duplicate or contradictory credential states
9. Partial lifecycle operations must remain identifiable and recoverable rather than being reported as completed
10. Lifecycle actions and recovery outcomes must remain traceable through protected audit evidence

## Business risks
| Risk | Business consequence |
|---|---|
| Unauthorized credential access | Weak authorization allows an actor to obtain or control credentials they should not manage |
| Excessive credential scope | A credential grants access beyond the intended application or business purpose |
| Stale credential access | Expired or revoked credentials continue to access protected APIs |
| Failed rotation | A replacement credential is unusable or the previous credential is invalidated prematurely |
| Credential duplication | Retries or concurrent operations create unnecessary active credentials |
| Compromised credential exposure | A known compromised credential remains active longer than necessary |
| Inconsistent lifecycle state | Different systems disagree about whether a credential is active, revoked, or replaced |
| Missing audit evidence | Lifecycle changes cannot be reliably traced during security or operational investigation |
| Recovery failure | An incomplete operation leaves the credential in an unknown or contradictory state |
| Credential misassignment | A credential is associated with the wrong application, service, owner, or environment |