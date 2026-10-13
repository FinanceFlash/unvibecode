---
name: understand-oauth-authorization-and-account-linking-code
description: Trace and explain OAuth Authorization and Account Linking across an existing codebase. Use when locating entry points, authorization, state, provider calls, account matching, retries, recovery, monitoring, and tests.
---

# Understand OAuth Authorization and Account Linking Code

Trace:
1. Sign-in or link entry points, provider selection, and redirect construction
2. State, nonce, PKCE, callback, issuer, tenant, and account binding
3. Token exchange, claim normalization, account resolution, and unique-link constraints
4. Token storage, refresh, revocation, session creation, and support tooling
5. Retry, reconciliation, relink, and manual-repair logic

Explain actors, ownership, trust rules, states, transitions, effects, failures, retries, security boundaries, monitoring, tests, and areas needing verification. Cite files and symbols.
