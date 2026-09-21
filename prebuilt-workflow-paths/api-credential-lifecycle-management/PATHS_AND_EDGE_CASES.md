# Paths and Edge Cases

## Supported paths
- Authorized credential creation and activation
- Credential use with approved owner, application, service, and scope
- Planned credential rotation with controlled old/new credential overlap
- Expiry and renewal handling
- Credential revocation and emergency revocation
- Duplicate request handling, idempotency, reconciliation, and recovery
- Dependency failure, partial lifecycle completion, and manual repair

## Normal paths
- An authorized actor creates a credential with an approved scope and assigns it to the intended application or service
- An active credential successfully accesses the protected API within its permitted scope
- An authorized rotation provisions and activates a replacement before invalidating the previous credential according to policy
- An authorized revocation invalidates the credential and records the completed lifecycle action

## Denied paths
- Requester lacks permission to create, rotate, or revoke the credential
- Requested scope exceeds the requester's or application's allowed permissions
- Credential assignment targets an unauthorized application, service, environment, or owner
- Expired or revoked credentials attempt to access the protected API
- Emergency lifecycle action is attempted without the required authority

## Timing, concurrency, and boundaries
- Two credential creation requests for the same logical operation execute together
- Two rotation operations target the same credential concurrently
- A credential reaches expiry exactly during an API request or rotation
- Old and replacement credentials overlap at the rotation boundary
- A credential becomes compromised while a normal rotation is already in progress
- Credential generation succeeds but activation or state update fails
- A lifecycle operation succeeds but its response or audit record is lost
- Different lifecycle components disagree about the credential's current state
- A retry occurs after a partially completed creation, rotation, or revocation
- Recovery runs after a dependency timeout or incomplete lifecycle operation

Cover valid, invalid, duplicate, stale, replayed, repeated, simultaneous, partially completed, unauthorized, expired, revoked, compromised, and recovery outcomes.