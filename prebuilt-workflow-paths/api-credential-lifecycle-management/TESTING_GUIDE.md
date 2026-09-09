# Testing Guide

Check authoritative ownership, authorization, scope, lifecycle state, downstream API access, concurrency, recovery, and audit—not only responses.

## 1. Authorized credential creation

**Given:** An authorized credential owner requests a new credential with an approved scope and intended application or service

**When:** Credential creation and activation execute

**Expect:** The credential is created with the correct owner, assignment, scope, lifecycle metadata, and activation state

**Must not happen:** An unauthorized or incorrectly scoped credential becomes active

**Best test levels:** Integration and end-to-end.

## 2. Unauthorized credential creation

**Given:** A requester lacks permission to create a credential for the target owner, application, service, or environment

**When:** Credential creation is attempted

**Expect:** Authorization denies the request and no usable credential is created

**Must not happen:** The requester receives an active credential despite failing authorization

**Best test levels:** Authorization and security.

## 3. Invalid scope during creation

**Given:** An authorized requester asks for permissions outside the policy allowed for the credential

**When:** Scope validation runs

**Expect:** The request is rejected or corrected before activation

**Must not happen:** A credential becomes active with permissions beyond the approved scope

**Best test levels:** Unit, policy integration, and security.

## 4. Credential activation

**Given:** A credential has been provisioned but has not completed the required authorization and activation checks

**When:** Activation is attempted

**Expect:** The credential becomes usable only after all required checks succeed

**Must not happen:** A credential becomes usable before required authorization and activation checks complete

**Best test levels:** Integration.

## 5. Duplicate credential creation

**Given:** A client repeats the same creation request because the original response was lost or timed out

**When:** The repeated request reaches the credential-management service

**Expect:** The existing logical operation is recognized and the intended result is returned or reconciled

**Must not happen:** A retry creates multiple active credentials for one logical creation request

**Best test levels:** API and integration.

## 6. First successful credential use

**Given:** An active credential is assigned to an authorized application or service with a defined scope

**When:** The application uses the credential against the protected API

**Expect:** The protected API accepts the request according to the credential's current scope and lifecycle state

**Must not happen:** A credential belonging to another owner, application, service, or scope is accepted

**Best test levels:** Integration and end-to-end.

## 7. Expired credential rejection

**Given:** A credential has reached its configured expiry time

**When:** The credential is used against the protected API

**Expect:** The protected API rejects the credential

**Must not happen:** An expired credential continues to authorize protected API access

**Best test levels:** Unit with controlled time and integration.

## 8. Credential nearing expiry

**Given:** A credential enters its configured pre-expiry window

**When:** Lifecycle evaluation runs

**Expect:** The credential enters the expected warning or renewal state and exposes the expiry condition to the responsible actor or system

**Must not happen:** The credential reaches expiry without the expected lifecycle transition or actionable renewal indication

**Best test levels:** Unit with controlled time and integration.

## 9. Planned credential rotation

**Given:** An authorized actor requests rotation of an active credential

**When:** The replacement credential is provisioned and activated

**Expect:** The replacement becomes usable according to the defined rotation policy without prematurely invalidating the credential required for continuity

**Must not happen:** Rotation leaves the system without a valid authorized credential when continuity is required

**Best test levels:** Integration and end-to-end.

## 10. Controlled temporary overlap during rotation

**Given:** A rotation policy permits the old and replacement credentials to coexist during a defined migration window

**When:** Both credentials are evaluated during that window

**Expect:** The overlap is bounded by the defined purpose, owner, and termination condition

**Must not happen:** Temporary overlap becomes indefinite or creates an uncontrolled number of active credentials

**Best test levels:** Integration and policy testing.

## 11. Old credential invalidation after rotation

**Given:** The replacement credential has been successfully activated and the rotation reaches its completion point

**When:** The old credential is evaluated

**Expect:** The previous credential is invalidated according to the defined rotation policy

**Must not happen:** The old credential remains usable after completed rotation when it should be invalidated

**Best test levels:** Integration and end-to-end.

## 12. Concurrent rotation attempts

**Given:** Two authorized rotation operations target the same credential at approximately the same time

**When:** Both rotation operations execute

**Expect:** The system resolves the concurrent operations deterministically and leaves one consistent authoritative lifecycle state

**Must not happen:** Concurrent operations leave contradictory active credentials or corrupt lifecycle metadata

**Best test levels:** Concurrency integration.

## 13. Credential revocation

**Given:** An authorized actor requests revocation of an active credential

**When:** The revocation operation executes

**Expect:** The credential reaches the revoked state and protected API access is no longer authorized

**Must not happen:** The system reports revocation while the credential remains authorized for protected API access

**Best test levels:** Authorization and integration.

## 14. Use after revocation

**Given:** A credential has already reached the revoked state

**When:** The application attempts to use it against the protected API

**Expect:** The protected API rejects the request

**Must not happen:** A revoked credential continues to provide protected API access

**Best test levels:** Integration and end-to-end.

## 15. Emergency revocation of compromised credential

**Given:** A credential is suspected or confirmed to be compromised

**When:** The emergency revocation path executes

**Expect:** The credential is invalidated through the appropriate emergency path and the resulting action is traceable

**Must not happen:** A known compromised credential remains active because the normal lifecycle process is still pending

**Best test levels:** Security and integration.

## 16. Credential-generation dependency failure

**Given:** A required credential-generation or provisioning dependency fails during creation or rotation

**When:** The lifecycle operation handles the dependency failure

**Expect:** The operation fails safely and the credential remains in a known non-active or recoverable state

**Must not happen:** A dependency failure leaves a partially provisioned credential incorrectly marked active

**Best test levels:** Dependency contract and integration.

## 17. Partial rotation failure

**Given:** A replacement credential is generated but a later rotation step fails

**When:** The system records and evaluates the incomplete rotation

**Expect:** The rotation remains explicitly incomplete and provides a known recovery path

**Must not happen:** A failed rotation is reported as complete when the replacement is unusable or the previous credential was incorrectly invalidated

**Best test levels:** Integration and operations.

## 18. Retry after incomplete lifecycle operation

**Given:** A creation or rotation operation remains incomplete after a failure or lost response

**When:** The same lifecycle operation is retried

**Expect:** The retry reconciles the existing state and safely continues, completes, or restarts the operation according to policy

**Must not happen:** A retry creates duplicate credentials or conflicting lifecycle states

**Best test levels:** API and integration.

## 19. Lifecycle change succeeds but audit recording fails

**Given:** A credential lifecycle action succeeds but its audit event cannot be recorded

**When:** The system handles the missing audit evidence

**Expect:** The system follows its defined audit-failure policy without falsely claiming complete traceability

**Must not happen:** A lifecycle operation silently loses required audit evidence while being presented as fully traceable

**Best test levels:** Integration and security.

## 20. Recovery and final-state reconciliation

**Given:** Credential-management components disagree about a credential's state or an incomplete lifecycle operation is detected

**When:** Recovery and reconciliation run

**Expect:** The system determines the authoritative state, repairs the inconsistent state where permitted, and records the recovery result

**Must not happen:** Recovery leaves contradictory states or marks a credential healthy without verifying its actual state

**Best test levels:** Integration and operations.