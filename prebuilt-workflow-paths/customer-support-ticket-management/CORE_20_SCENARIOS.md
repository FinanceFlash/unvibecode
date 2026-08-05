# Core 20 Scenarios

| # | Scenario | Must not happen |
|---:|---|---|
| 1 | Valid issue creates one ticket | The issue disappears or creates multiple tickets |
| 2 | Ticket is acknowledged and assigned | Acknowledgement exposes internal data or assignment crosses scope |
| 3 | Agent resolves and closes correctly | The ticket closes while promised work remains incomplete |
| 4 | Required intake data is missing | A blank or unowned ticket enters operations |
| 5 | Attachment is malformed or unsafe | Unsafe content is rendered, executed, or exposed to agents |
| 6 | Duplicate issue is submitted | Duplicate tickets trigger duplicate work or SLA noise |
| 7 | Unauthorized person accesses ticket | A ticket identifier grants access |
| 8 | Requester identity formats differ | A format variation crosses accounts or creates false duplicates |
| 9 | Two agents update ownership together | The ticket has conflicting owners or loses a message |
| 10 | SLA action occurs at deadline | Races hide a breach or escalate completed work |
| 11 | Ticket-create response is lost | Repeated retries create ticket and message floods |
| 12 | Inbound message is replayed | The message, notification, or linked automation repeats |
| 13 | Support intake is flooded | Queues, provider cost, or agent workload grow without limit |
| 14 | Ticket commits but acknowledgement fails | The ticket is recreated or customer messages multiply |
| 15 | External support provider times out | Uncertainty is treated as safe success or endless retry |
| 16 | Resolution response is lost | Closure, notifications, or credits repeat |
| 17 | Cross-tenant ticket reference is used | Identifiers bypass tenant isolation |
| 18 | Sensitive message or attachment causes error | Secrets, internal notes, or attachments leak |
| 19 | Customer replies after closure | The reply is silently discarded or mutates archived work |
| 20 | Promised linked action fails | The customer is told the issue is complete or the action repeats |

Full details are in [TESTING_GUIDE.md](TESTING_GUIDE.md).

