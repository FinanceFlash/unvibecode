---
name: implement-oauth-authorization-and-account-linking
description: Implement or modify OAuth Authorization and Account Linking. Use when adding or changing validation, authorization, state transitions, identity binding, retries, recovery, privacy controls, monitoring, or tests.
---

# Implement OAuth Authorization and Account Linking

Confirm:
- Which providers, tenants, account types, and environments are supported
- Whether the provider is used for login, linking, or both
- Which scopes are mandatory, optional, incremental, or forbidden
- How provider claims are trusted for account matching or first-time account creation
- State, nonce, PKCE, redirect, callback-expiry, and session-binding policy
- How existing links, email collisions, tenant mismatches, and relink requests are handled
- Token storage, encryption, rotation, revocation, disconnect, and audit policy
- Customer communication, support repair, abuse controls, privacy, and monitoring

Follow project conventions and protect:
- State, nonce, PKCE, provider, tenant, redirect, and local account binding
- Safe account resolution, uniqueness, and collision handling
- Explicit link, session, and token states
- Replay-safe callback and reconciliation behavior
- Protection of tokens, claims, personal data, and provider secrets

Add all core tests and summarize decisions, files, state changes, recovery, privacy and security controls, and remaining gaps.
