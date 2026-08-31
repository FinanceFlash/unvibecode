# Testing Guide

## Scenario 1 — Valid email submits reset request and receives token link
**Given** an active account exists with a registered email address  
**When** the user submits a reset request with that email  
**Expect** a reset token is generated, stored as a hash, and a link is delivered to that email within the expected window  
**Must not happen** the reset link is not delivered or the token is not recorded in the token store  
**Suggested test level** integration, end-to-end

---

## Scenario 2 — Unregistered email submits reset request
**Given** no account exists for the submitted email address  
**When** the user submits a reset request  
**Expect** the response body, status code, and response time are identical to a successful request  
**Must not happen** the response reveals whether the email is registered through content or timing  
**Suggested test level** unit, integration, timing analysis

---

## Scenario 3 — Valid token used within expiry window
**Given** a reset token has been issued and has not expired  
**When** the user submits the token and a new compliant password  
**Expect** the credential is updated, the token is marked consumed, and a success response is returned  
**Must not happen** the credential is updated without the token being consumed in the same operation  
**Suggested test level** unit, integration

---

## Scenario 4 — Expired token submitted for reset
**Given** a reset token was issued and its expiry window has passed  
**When** the user submits the expired token  
**Expect** the request is rejected with a clear expiry message and the credential is unchanged  
**Must not happen** the credential is updated using an expired token  
**Suggested test level** unit, integration

---

## Scenario 5 — Already-consumed token is replayed
**Given** a reset token has been used and the credential has been updated  
**When** the same token is submitted again  
**Expect** the request is rejected and the credential remains as updated in the prior step  
**Must not happen** the credential is updated a second time with the same token  
**Suggested test level** unit, integration

---

## Scenario 6 — New reset request arrives while prior token is still valid
**Given** an unconsumed token exists for an account  
**When** a new reset request is submitted for the same account  
**Expect** the prior token is revoked and a new token is issued  
**Must not happen** both tokens remain valid simultaneously  
**Suggested test level** unit, integration

---

## Scenario 7 — User sets a new password meeting all policy rules
**Given** the user holds a valid token  
**When** the user submits a new password that satisfies length, complexity, and history requirements  
**Expect** the credential is updated and the token is consumed  
**Must not happen** the credential update proceeds without verifying all policy rules  
**Suggested test level** unit, integration

---

## Scenario 8 — New password fails complexity or length policy
**Given** the user holds a valid token  
**When** the user submits a new password that does not meet policy requirements  
**Expect** the request is rejected with a policy violation message and the credential is unchanged  
**Must not happen** a non-compliant credential replaces the current one  
**Suggested test level** unit, boundary

---

## Scenario 9 — New password is identical to the current password
**Given** the user holds a valid token and password reuse is prohibited by policy  
**When** the user submits a new password identical to the current credential  
**Expect** the request is rejected with a reuse message and the credential is unchanged  
**Must not happen** the reused credential is silently accepted  
**Suggested test level** unit, integration

---

## Scenario 10 — Credential update succeeds
**Given** the credential has been updated using a valid token  
**When** the credential update is committed  
**Expect** all active sessions, refresh tokens, and access tokens for the account are invalidated  
**Must not happen** any active session remains valid after the credential changes  
**Suggested test level** integration, end-to-end

---

## Scenario 11 — Two concurrent reset requests arrive for the same account
**Given** two reset requests are submitted simultaneously for the same account  
**When** both requests are processed  
**Expect** only one token is valid after processing; the other is revoked or superseded  
**Must not happen** both tokens are valid simultaneously  
**Suggested test level** concurrency, integration

---

## Scenario 12 — Token format is tampered or structurally invalid
**Given** a reset link has been altered or a token with an invalid format is submitted  
**When** the token is validated  
**Expect** the request is rejected at format validation before any store lookup  
**Must not happen** a malformed token reaches the credential store or causes an unhandled error  
**Suggested test level** unit, security

---

## Scenario 13 — Rate limit is exceeded for reset requests
**Given** the rate limit threshold for reset requests has been reached for a given email or IP  
**When** another reset request is submitted  
**Expect** the request is rejected with a rate-limit response and no new token is issued  
**Must not happen** unlimited reset emails are dispatched from a single source  
**Suggested test level** integration, load

---

## Scenario 14 — Reset request arrives for a locked or suspended account
**Given** the account is in a locked or suspended state  
**When** a reset request is submitted for that account  
**Expect** the request is rejected without issuing a token  
**Must not happen** a token is issued and the credential is changed for a restricted account  
**Suggested test level** unit, integration

---

## Scenario 15 — Account is deleted between request submission and token use
**Given** a token was issued for an account that is subsequently deleted  
**When** the token is submitted for credential update  
**Expect** the request is rejected because the account no longer exists  
**Must not happen** the deleted account credential is updated or a new credential record is created  
**Suggested test level** integration

---

## Scenario 16 — Credential update succeeds but session invalidation response is lost
**Given** the credential has been updated and a session invalidation call is retried  
**When** the invalidation is retried after a lost response  
**Expect** the retry is idempotent and does not produce a duplicate credential update  
**Must not happen** the retry causes the credential to be overwritten or sessions to be partially invalidated  
**Suggested test level** unit, recovery

---

## Scenario 17 — Token link is opened after the account email address has changed
**Given** a token was issued to an email address that has since been changed on the account  
**When** the original email link is submitted  
**Expect** the token is rejected or the account owner is re-verified before credential update  
**Must not happen** the token validates against the new email owner's account  
**Suggested test level** integration, security

---

## Scenario 18 — Reset request response time differs between registered and unregistered emails
**Given** the system receives reset requests for registered and unregistered emails  
**When** response times are compared across both cases  
**Expect** response times are statistically indistinguishable  
**Must not happen** a measurable timing difference reveals whether an account exists  
**Suggested test level** timing analysis, security

---

## Scenario 19 — Successful credential update is not followed by a confirmation notification
**Given** the credential has been updated successfully  
**When** the update is committed  
**Expect** a confirmation notification is dispatched to the account email address  
**Must not happen** the user receives no notification that their credential has changed  
**Suggested test level** integration, end-to-end

---

## Scenario 20 — Admin triggers a forced password reset for a user
**Given** an admin marks an account as requiring a forced password reset  
**When** the user attempts to authenticate with their current credential  
**Expect** the user is redirected to the reset flow and cannot access the application until the reset is complete  
**Must not happen** the user authenticates successfully with the old credential before completing the forced reset  
**Suggested test level** integration, end-to-end
