# Testing Guide

Check account identity, tenant binding, consent scope, token safety, session outcomes, recovery, and audit, not only redirect success.

## 1. Eligible user links a provider account once

**Given:** A signed-in eligible user starts linking with an approved provider and scope set

**When:** The flow completes successfully

**Expect:** One provider subject is linked to one local account and the visible connection state becomes active

**Must not happen:** One provider account creates duplicate local links

**Best test levels:** End-to-end and integration.

## 2. Returning user signs in with the linked provider

**Given:** A provider subject is already linked to a local account

**When:** The user signs in through that provider again

**Expect:** The same local account and permitted session are restored

**Must not happen:** The provider subject maps to the wrong local account

**Best test levels:** End-to-end.

## 3. State or PKCE verifier is missing or wrong

**Given:** A callback arrives with altered, missing, or mismatched state, nonce, or PKCE data

**When:** Callback validation runs

**Expect:** The flow is rejected before token exchange or session creation

**Must not happen:** The callback still creates a session or link

**Best test levels:** Security and integration.

## 4. Provider denies consent

**Given:** The user rejects consent or the provider returns an OAuth denial error

**When:** The callback is handled

**Expect:** The request ends in a denied state with no new link or login session

**Must not happen:** Denial is stored as a successful connection

**Best test levels:** Provider contract and end-to-end.

## 5. Callback code is replayed

**Given:** A valid authorization code and callback context have been accepted once, and the same callback payload is submitted again

**When:** Callback handling or token exchange runs for the replayed request

**Expect:** The replay is detected using the request/code state, and the existing outcome is returned or the replay is rejected without a new side effect

**Must not happen:** A second session, provider link, token set, or account-linking side effect is created

**Fixtures:** Persist one valid authorization request, provider subject, local account, and completed callback outcome

**Controlled provider behavior:** Return the same authorization code or replayable callback payload on the second submission

**Best test levels:** Security and integration

**Cleanup:** Remove the authorization request, provider-link state, session, and test provider state

## 6. Redirect target is unapproved

**Given:** A request contains an altered callback target or post-login destination

**When:** Redirect allowlist checks run

**Expect:** The destination is rejected or normalized to a safe target

**Must not happen:** The flow forwards tokens or users to an attacker-controlled destination

**Best test levels:** Security and API.

## 7. Requested scopes exceed policy

**Given:** The client or provider response includes scopes outside the product policy

**When:** Scope validation and consent recording run

**Expect:** The flow blocks, downgrades, or requires explicit approval by policy

**Must not happen:** Broader access is granted without explicit approval

**Best test levels:** Unit and integration.

## 8. Provider subject is already linked elsewhere

**Given:** The external provider account already belongs to another local account

**When:** A second account tries to link it

**Expect:** The new request is denied or routed to an explicit manual recovery path

**Must not happen:** The existing link is silently reassigned

**Best test levels:** Integration and security.

## 9. Email or claim collides with another account

**Given:** Provider claims match an email, alias, or identifier already present on another account

**When:** Local account resolution runs

**Expect:** Trust rules require explicit verified matching or manual resolution

**Must not happen:** A guessed identity joins the wrong user

**Best test levels:** Unit, integration, and security.

## 10. Two link attempts run concurrently

**Given:** The same local account and provider subject have two valid link requests started at nearly the same time

**When:** Both callbacks reach account resolution and provider-link persistence concurrently

**Expect:** Transactional and uniqueness controls converge both requests on one consistent provider-link outcome

**Must not happen:** Both requests create conflicting provider-link records, reassign ownership, or create duplicate sessions

**Fixtures:** Create one local account and provider subject with two independent authorization requests

**Controlled concurrency:** Release both callback handlers at the same synchronization point before persistence

**Best test levels:** Concurrency integration and database integration

**Cleanup:** Remove the authorization requests, provider link, sessions, and test provider state.

## 11. Callback arrives after cancellation or expiry

**Given:** The link request has been cancelled, timed out, or invalidated

**When:** A late callback arrives

**Expect:** The callback is rejected or recorded as stale without new trust

**Must not happen:** A stale request still becomes active

**Best test levels:** Integration with controlled time.

## 12. Token exchange succeeds but local write fails

**Given:** The provider successfully exchanges the authorization code and returns valid tokens, but the local persistence operation fails before the link is durably recorded

**When:** Recovery or retry runs after the partial failure

**Expect:** The application reconciles the provider result with the existing request and local state without repeating an unsafe exchange or creating a duplicate link

**Must not happen:** Retrying creates a second provider link, loses the successful exchange permanently, or creates a session without a valid local link

**Fixtures:** Create a valid authorization request and configure the persistence layer to fail once after successful provider exchange

**Controlled provider behavior:** Return a deterministic successful token exchange without issuing a different provider subject on retry

**Best test levels:** Integration and failure-injection testing

**Cleanup:** Remove the authorization request, provider-link state, tokens, sessions, and injected failure configuration

## 13. Local write succeeds but response is lost

**Given:** The local link or session is created but the user receives no completion response

**When:** The user restarts the same flow

**Expect:** The application returns the existing link or session result safely

**Must not happen:** The user repeats the flow and duplicates the link or session

**Best test levels:** End-to-end and integration.

## 14. Refresh token rotates

**Given:** An active provider connection has a current refresh token and the provider rotates it during a refresh operation

**When:** The application receives a new refresh token and persists the rotated token

**Expect:** The new token becomes authoritative atomically, the previous token is no longer accepted for future refreshes, and the provider link remains active

**Must not happen:** The old token remains authoritative, concurrent refreshes overwrite the newest token incorrectly, or a failed rotation leaves the connection falsely active

**Fixtures:** Create an active provider link with a known current refresh token and persisted rotation state

**Controlled provider behavior:** Return a replacement refresh token and invalidate the previous token

**Best test levels:** Provider contract, integration, and concurrency testing

**Cleanup:** Revoke or delete test tokens and remove the provider link and session state

## 15. Provider revokes access later

**Given:** The user or provider revokes the application's access after successful linking

**When:** Refresh, webhook, or status check detects revocation

**Expect:** Local connection state becomes revoked or relink-required and protected actions stop

**Must not happen:** Local state still shows an active trusted connection

**Best test levels:** Integration and operations.

## 16. Cross-tenant provider identity is supplied

**Given:** A provider identity belongs to another tenant, organization, or configured environment

**When:** The actor attempts login or linking

**Expect:** Tenant and environment binding deny the connection

**Must not happen:** An identity from another tenant crosses the boundary

**Best test levels:** Authorization and security.

## 17. Support or admin relink is attempted without authority

**Given:** Privileged tooling can modify provider links on behalf of users

**When:** An operator without sufficient approval attempts a relink

**Expect:** Elevated checks, audit, and policy controls block or record the action explicitly

**Must not happen:** Privileged tooling bypasses normal ownership checks

**Best test levels:** Security and administrative integration.

## 18. OAuth error details are logged

**Given:** The path contains tokens, claims, provider payloads, redirect data, and client identifiers

**When:** Any validation or exchange step fails

**Expect:** Logs remain diagnosable while redacting secrets and sensitive identity data

**Must not happen:** Tokens, claims, or secrets leak into logs or support traces

**Best test levels:** Security and log inspection.

## 19. Provider callback omits required claim data

**Given:** Required subject, tenant, email-verification, or issuer claims are missing or malformed

**When:** Account resolution and trust checks run

**Expect:** The flow blocks, requests another step, or escalates to manual review

**Must not happen:** The system invents or over-trusts missing identity fields

**Best test levels:** Unit and integration.

## 20. Reconciliation runs after uncertain exchange status

**Given:** The application cannot determine whether a provider code exchange completed because the response was lost or the local operation timed out

**When:** Automated or manual reconciliation examines the authorization request, provider identity, audit trail, and current local state

**Expect:** Reconciliation determines whether the exchange and link already succeeded and converges the request to one authoritative outcome

**Must not happen:** Reconciliation creates a duplicate link, assigns the provider identity to the wrong local account, exchanges the same one-time code unsafely, or overwrites a valid newer state

**Fixtures:** Create an authorization request with an uncertain exchange status and optionally persist evidence of a completed provider exchange

**Controlled provider behavior:** Simulate a successful exchange whose response is lost, followed by a reconciliation lookup

**Best test levels:** Integration and operations testing

**Cleanup:** Remove the authorization request, reconciliation records, provider-link state, audit entries, tokens, and test provider state
