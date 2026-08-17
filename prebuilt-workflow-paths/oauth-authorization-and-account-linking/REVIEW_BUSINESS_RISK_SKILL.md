---
name: review-oauth-authorization-and-account-linking-risk
description: Review account-takeover, scope, tenant, privacy, and operational risks in OAuth Authorization and Account Linking. Use when founders, PMs, or engineering managers need prioritized consequences, controls, tests, and release concerns.
---

# Review OAuth Authorization and Account Linking Risk

Review entry, identity proof, account matching, state, timing, concurrency, external effects, retry, recovery, privacy, and support paths. Prioritize:
- Account takeover — A user is signed into or linked with another person's local account
- Cross-tenant connection — An identity from one tenant gains access to another tenant's data or settings
- Scope overreach — The application stores or uses broader permissions than the user approved
- Duplicate or broken links — Replays or concurrent callbacks create conflicting provider-link records
- False active connection — A revoked or expired provider relationship still appears usable
- Silent identity collision — Email or claim matching joins the wrong local account
- Token exposure — Access or refresh tokens leak through logs, support tools, or unsafe storage
- Unrepairable uncertainty — A successful provider exchange is lost locally and cannot be reconciled safely

For each material risk, explain trigger, behavior, business consequence, protection, decision or test, and acceptance condition.
