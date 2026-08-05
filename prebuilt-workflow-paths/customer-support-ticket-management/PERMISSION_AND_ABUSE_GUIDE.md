# Permission and Abuse Guide

## Permission boundaries
- One eligible issue must resolve to one authoritative ticket or explicit rejection
- Ticket access must enforce requester, account, tenant, agent, queue, and field visibility
- Internal notes must never appear as customer-visible messages
- One authoritative owner and status must survive simultaneous actions
- SLA calculations must use trusted time and explicit pause reasons

## Misuse paths
- Lost customer issue — A valid request is accepted externally but no actionable ticket exists
- Unauthorized ticket access — Another customer, tenant, or agent sees or changes protected support data
- Internal-note exposure — Private investigation content is sent to the customer
- Incorrect routing or priority — Critical issues wait in the wrong queue or low-risk issues consume emergency capacity
- False resolution — A ticket closes while the customer problem or promised action remains incomplete
- SLA failure — Deadlines pause incorrectly or escalation never occurs
- Duplicate business action — Retries repeat refunds, credits, notifications, or account changes
- Sensitive-data exposure — Messages, attachments, credentials, or personal data reach unsafe logs or recipients

Protect actor identity, tenant scope, authoritative objects, sensitive content, external proof, support tools, and audit records. Deny uncertain ownership or permission.

