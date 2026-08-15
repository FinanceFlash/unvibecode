# Authentication, Session Management, and Account Recovery

A reusable workflow specification for authenticating users, establishing and maintaining authenticated sessions, handling session termination, and recovering account access when normal authentication is unavailable.

## Workflow boundary

### Start event

The workflow starts when a user attempts to authenticate, establish an authenticated session, terminate an existing session, or recover access to an account.

### End events

The workflow ends when one of these authoritative outcomes is reached:

- Authentication succeeds and an authenticated session is established.
- Authentication is denied without creating an authenticated session.
- An authenticated session is terminated.
- Account recovery succeeds and the user can authenticate again.
- Account recovery is denied, expired, or safely abandoned.

## Included scope

This workflow covers:

- Login and authentication attempts.
- Credential validation.
- Multi-factor authentication or step-up authentication where applicable.
- Session creation and session lifecycle management.
- Session expiration and explicit logout.
- Authentication failure handling and bounded retry behaviour.
- Password or credential reset requests.
- Recovery-token issuance, validation, expiration, and single use.
- Recovery completion and restoration of account access.
- Authorization boundaries during authentication and recovery.
- Concurrent authentication and recovery attempts.
- Abuse controls such as enumeration, brute force, and token replay.

## Excluded scope

The following workflows are outside this pack:

- Account creation and initial onboarding.
- Payment or subscription access.
- Account-data deletion or right-to-erasure.
- General application authorization after authentication.
- Fraud scoring and investigation beyond authentication-specific controls.
- Transactional notification delivery.
- Business-specific approval workflows.

Use the relevant workflow pack instead of duplicating those lifecycles.

## Primary business outcome

A legitimate user must be able to establish or recover authenticated access while unauthorized users must not gain access to the account or authenticated session.

## People and systems

- User
- Authentication service
- Session or token store
- Identity provider, when applicable
- Multi-factor authentication provider, when applicable
- Account database
- Password or credential-reset service
- Notification service used for recovery messages
- Security or operations team

## Things created or changed

- Authentication attempt
- Authenticated session
- Access or refresh token
- Recovery request
- Recovery token
- Credential
- Session-revocation record
- Authentication security state

## Stages

1. Authentication or recovery request received.
2. Account and request context identified.
3. Credentials or recovery proof validated.
4. Additional authentication challenge completed when required.
5. Session established, terminated, or recovery state updated.
6. Tokens and credentials invalidated or rotated when required.
7. Final authenticated, denied, terminated, recovered, expired, or rejected outcome recorded.

## Core scenarios

See `CORE_20_SCENARIOS.md` for the required 20 scenarios covering normal completion, invalid input, denial, boundaries, concurrency, permissions, abuse, dependency failures, partial completion, retry, and recovery.

## Supporting guides

- `PRODUCT_AND_BUSINESS_GUIDE.md` — product and business requirements.
- `ENGINEERING_GUIDE.md` — implementation and code-tracing guidance.
- `CORE_20_SCENARIOS.md` — compact scenario checklist.
- `TESTING_GUIDE.md` — complete test scenarios.
- `PATHS_AND_EDGE_CASES.md` — unusual and boundary paths.
- `PERMISSION_AND_ABUSE_GUIDE.md` — authorization and abuse controls.
- `RETRY_AND_RECOVERY_GUIDE.md` — retry, expiration, invalidation, and recovery.
- `WRITE_PRODUCT_SPEC_SKILL.md` — product specification LLM task.
- `REVIEW_BUSINESS_RISK_SKILL.md` — business-risk review LLM task.
- `UNDERSTAND_CODE_SKILL.md` — code-understanding LLM task.
- `IMPLEMENT_WORKFLOW_SKILL.md` — implementation LLM task.
- `TEST_WORKFLOW_SKILL.md` — testing LLM task.

## Evidence rule

This pack describes expected workflow controls. It must not be treated as proof that an application implements any control.

When reviewing an implementation, verify actual routes, functions, permissions, session state, token storage, credential changes, invalidation behaviour, external calls, tests, and runtime evidence.

## Adaptation rule

Applications may use passwords, passkeys, social login, enterprise identity providers, magic links, multi-factor authentication, or other authentication mechanisms.

Adapt the scenarios to the actual authentication mechanisms and account-recovery policies used by the application while preserving the workflow boundary and safety requirements.