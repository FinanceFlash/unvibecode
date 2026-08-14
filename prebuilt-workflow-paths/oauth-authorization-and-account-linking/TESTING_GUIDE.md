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

**Given:** A valid authorization code or callback payload is submitted more than once

**When:** Exchange or callback handling runs again

**Expect:** The replay is recognized and no duplicate side effect occurs

**Must not happen:** A second session or duplicate link is created

**Best test levels:** Security and integration.

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

**Given:** The same user or provider subject starts two link flows at nearly the same time

**When:** Both callbacks complete

**Expect:** Uniqueness and idempotency allow one consistent link outcome

**Must not happen:** Both succeed and create conflicting provider-link state

**Best test levels:** Concurrency integration.

## 11. Callback arrives after cancellation or expiry

**Given:** The link request has been cancelled, timed out, or invalidated

**When:** A late callback arrives

**Expect:** The callback is rejected or recorded as stale without new trust

**Must not happen:** A stale request still becomes active

**Best test levels:** Integration with controlled time.

## 12. Token exchange succeeds but local write fails

**Given:** The provider returned tokens successfully but the database update fails

**When:** Recovery or retry runs

**Expect:** The same exchange is reconciled safely without duplicating the link

**Must not happen:** Retrying creates a second link or loses the successful exchange

**Best test levels:** Integration and operations.

## 13. Local write succeeds but response is lost

**Given:** The local link or session is created but the user receives no completion response

**When:** The user restarts the same flow

**Expect:** The application returns the existing link or session result safely

**Must not happen:** The user repeats the flow and duplicates the link or session

**Best test levels:** End-to-end and integration.

## 14. Refresh token rotates

**Given:** The provider issues a new refresh token and invalidates the previous one

**When:** Token update handling runs

**Expect:** The new token replaces the old one atomically and future refresh still works

**Must not happen:** The old token remains active and breaks future recovery

**Best test levels:** Provider contract and integration.

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

**Given:** The application cannot tell whether the provider code exchange completed and whether a link already exists

**When:** Manual or automated reconciliation runs

**Expect:** Repair uses provider subject, request record, audit, and current local state to converge safely

**Must not happen:** Manual repair changes the wrong account or provider link

**Best test levels:** Operations and integration.
