---
name: "Understand Code for Password Reset and Account Recovery"
description: "Traces the password reset and account recovery workflow through a codebase using file and symbol evidence, identifying the reset request handler, token generation and storage, email dispatch, token validation, credential update, and session invalidation."
---

# Understand Code — Password Reset and Account Recovery

You are tracing the password reset and account recovery workflow through a codebase.

## Your task

Using the connected code context provided, locate and describe each stage of this workflow with file names, function or method names, and line references where available. Do not state that a control exists unless file or symbol evidence supports it.

## Trace sequence

**1. Reset request handler**
Find the route or endpoint that accepts the reset request. Identify how the submitted email is looked up, how account state is checked, and where the rate limit is enforced.

**2. Token generation and storage**
Find where the token is generated. Note the entropy source, token format, hashing approach, storage location, expiry assignment, and whether prior tokens for the same account are revoked.

**3. Email dispatch**
Find where the reset link is constructed and the email is queued or sent. Note whether delivery failure is handled and how the token is embedded in the link.

**4. Token validation handler**
Find the route or endpoint that accepts the token. Identify how the token is looked up, how expiry is checked, how the single-use flag is enforced, and how account binding is verified.

**5. Credential update**
Find where the new password is validated against policy and where the credential hash is written. Note whether the token is consumed in the same transaction as the credential write.

**6. Session invalidation**
Find where active sessions, refresh tokens, and access tokens are invalidated. Note the scope, whether failure is handled, and whether the invalidation is retried.

**7. Audit record**
Find where reset events are logged. Note which stages are recorded and whether plaintext tokens or passwords appear in any log call.

## For each stage, state
- The file path and function or method name
- What the code does at that stage
- Any missing control, unexpected behaviour, or deviation from the expected workflow
- Any stage that could not be located in the provided context
