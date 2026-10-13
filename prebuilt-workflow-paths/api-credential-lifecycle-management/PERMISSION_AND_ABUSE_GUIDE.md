# Permission and Abuse Guide

## Permission boundaries
- Only an authorized credential owner, service operator, administrator, or approved security actor may create, rotate, or revoke a credential
- Credential lifecycle actions must bind the intended owner, application or service, environment, credential, scope, and current lifecycle state
- Requested permissions must remain within the actor's and target application's allowed scope
- Credential assignment must not cross owner, application, service, environment, or tenant boundaries
- Emergency revocation must require the authority defined for compromised-credential response
- Temporary credential overlap during rotation must be policy-bound, time-bounded, and auditable
- Lifecycle state changes must not be performed solely from an untrusted credential identifier or request identifier
- Recovery and reconciliation must preserve the authoritative ownership, scope, and lifecycle state

## Misuse paths
- Unauthorized credential creation — An actor obtains an active credential without sufficient authority
- Excessive credential scope — A credential receives permissions beyond the approved application or business purpose
- Credential misassignment — A credential is associated with another owner, application, service, environment, or tenant
- Stale credential access — An expired or revoked credential continues to authorize protected API access
- Rotation abuse — Repeated or concurrent rotation creates unnecessary active credentials or contradictory lifecycle states
- Compromised credential exposure — A known compromised credential remains active while normal lifecycle processing is pending
- Lifecycle-state manipulation — An actor changes credential state or ownership without the required authorization
- Audit-evidence exposure — Credential secrets, privileged lifecycle data, or sensitive audit information reaches unsafe logs or tools

Protect actor identity, owner and tenant scope, credential identifiers, permission scope, lifecycle state, privileged tools, secrets, and audit records. Deny uncertain identity, ownership, scope, or authority.