# Permission and Abuse Guide

## Permission boundaries
- Only eligible reviewers may act within their assigned tenant, step, and scope
- Every decision must bind the authoritative submitted request version
- Required order, quorum, conflict, and separation-of-duties policy must hold
- Material edits must not silently retain stale approvals
- One terminal workflow outcome must be authoritative

## Misuse paths
- Unauthorized approval — An ineligible or out-of-scope person commits a business decision
- Conflict or self-approval — Separation-of-duties rules are bypassed
- Skipped approval — A required stage, order, or quorum is ignored
- Stale-version approval — Reviewers approve data that is no longer authoritative
- Conflicting final state — Concurrent approve, reject, withdraw, or expire actions disagree
- Duplicate downstream action — A replayed final decision repeats payment, provisioning, publication, or other work
- SLA or escalation failure — Important requests remain unattended or go to the wrong substitute
- Evidence exposure — Sensitive request data or reviewer comments reach the wrong audience or logs

Protect actor identity, tenant scope, authoritative objects, sensitive content, external proof, support tools, and audit records. Deny uncertain ownership or permission.

