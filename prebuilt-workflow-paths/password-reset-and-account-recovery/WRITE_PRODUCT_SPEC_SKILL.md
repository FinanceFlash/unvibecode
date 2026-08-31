---
name: "Write Product Spec for Password Reset and Account Recovery"
description: "Writes or reviews a product specification for the password reset and account recovery workflow, covering token policy, password rules, session invalidation scope, enumeration protection, rate limiting, admin-triggered resets, and acceptance criteria."
---

# Write Product Spec — Password Reset and Account Recovery

You are writing or reviewing a product specification for the password reset and account recovery workflow.

## Your task

Using the context provided, produce or evaluate a specification that covers the following decisions and requirements.

## Required sections

**Scope and trigger**
State the exact event that starts this workflow and the authoritative outcomes that end it. Distinguish this workflow from user registration, account deletion, and multi-factor authentication.

**Token policy**
Specify token expiry window, entropy requirements, storage strategy, single-use enforcement, and the behaviour when a new request arrives before the prior token is consumed.

**Password rules**
Specify minimum length, complexity requirements, history depth, and the policy for submitting a password identical to the current credential.

**Session invalidation scope**
State which sessions, refresh tokens, and access tokens are invalidated after a successful credential update and whether exceptions apply for the current device.

**Account enumeration protection**
Describe how the workflow ensures that response content and timing reveal nothing about whether the submitted email is registered.

**Rate limiting**
Specify the limit thresholds per email address and per source IP, the lockout duration, and the behaviour when the limit is reached.

**Admin-triggered forced reset**
Describe the conditions under which an admin may force a reset, what the user experiences, and which authentication actions are blocked until the reset is complete.

**Notifications**
Specify which messages are sent at request time and after successful credential update, and what happens when delivery fails.

**Acceptance criteria**
List the verifiable conditions that confirm the workflow is correctly implemented, covering token safety, session invalidation, enumeration protection, and audit completeness.

## Evidence to collect

When reviewing an existing specification, verify that each section above is present and unambiguous. Note any missing policy decision, any acceptance criterion that cannot be verified, and any scope overlap with adjacent workflows.
