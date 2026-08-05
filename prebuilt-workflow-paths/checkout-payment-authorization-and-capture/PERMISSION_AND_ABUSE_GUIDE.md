# Permission and Abuse Guide

## Permission boundaries
- One payable checkout must not produce more than one permitted charge
- Provider amount and currency must equal the authoritative checkout
- Every provider action must bind the intended payer, merchant, order, tenant, and attempt
- Current attempt and authorization state must be enforced at capture
- Uncertain provider outcomes must not trigger blind duplicate payment

## Misuse paths
- Duplicate charge — Concurrent requests, retries, or lost responses capture payment more than once
- Wrong amount or currency — The provider charge differs from the authoritative checkout
- Payment–order divergence — Money moves but the order, entitlement, fulfilment, or ledger does not
- False success — A decline, timeout, authorization, or pending state is shown as captured
- Unauthorized payment action — Another account or tenant controls the order or capture
- Stale authorization — Expired, voided, cancelled, or previously captured authorization is reused
- Card-testing or cost abuse — Automated attempts create fraud, provider fees, or customer harm
- Secret or personal-data exposure — Payment data, tokens, provider responses, or credentials reach unsafe logs

Protect actor identity, tenant scope, authoritative business objects, financial data, provider proof, support tools, and audit records. Deny uncertain ownership or permission.

