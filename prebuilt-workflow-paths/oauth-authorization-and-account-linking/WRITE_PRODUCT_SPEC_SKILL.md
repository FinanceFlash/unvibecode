---
name: write-oauth-authorization-and-account-linking-spec
description: Write or review a product specification for OAuth Authorization and Account Linking. Use when defining actors, states, trust rules, scope policy, account-matching rules, token handling, recovery, or business risks.
---

# Write an OAuth Authorization and Account Linking Specification

Use application-native terms. Decide:
- Which providers, tenants, account types, and environments are supported
- Whether the provider is used for login, linking, or both
- Which scopes are mandatory, optional, incremental, or forbidden
- How provider claims are trusted for account matching or first-time account creation
- State, nonce, PKCE, redirect, callback-expiry, and session-binding policy
- How existing links, email collisions, tenant mismatches, and relink requests are handled
- Token storage, encryption, rotation, revocation, disconnect, and audit policy
- Customer communication, support repair, abuse controls, privacy, and monitoring

Write scope, actors, objects, states, paths, permissions, trust rules, consent, recovery, privacy, misuse, acceptance criteria, and unanswered decisions.
