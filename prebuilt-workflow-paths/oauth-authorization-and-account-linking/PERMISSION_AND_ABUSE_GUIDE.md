# Permission and Abuse Guide

## Permission boundaries
- Which actors may start login, create links, relink, disconnect, or use support tooling
- Tenant, organization, environment, and provider-policy boundaries for every callback and token
- Which scopes, claims, and account-creation paths are permitted for each actor type
- Protection of tokens, provider subjects, emails, claims, audit entries, and redirect data

## Misuse paths
- Account takeover — A user is signed into or linked with another person's local account
- Cross-tenant connection — An identity from one tenant gains access to another tenant's data or settings
- Scope overreach — The application stores or uses broader permissions than the user approved
- Duplicate or broken links — Replays or concurrent callbacks create conflicting provider-link records
- False active connection — A revoked or expired provider relationship still appears usable
- Silent identity collision — Email or claim matching joins the wrong local account
- Token exposure — Access or refresh tokens leak through logs, support tools, or unsafe storage
- Support-tool bypass — An operator relinks accounts without the right approval path

Protect actor identity, tenant scope, provider subject ownership, tokens, support tools, and audit records. Deny uncertain ownership or permission.
