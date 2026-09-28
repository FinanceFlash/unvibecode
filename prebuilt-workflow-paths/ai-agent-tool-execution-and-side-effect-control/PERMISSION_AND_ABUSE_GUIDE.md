\# Permission and Abuse Guide



\## Authorization boundary



Tool availability and authorization are separate concerns.



A registered tool may be callable by an agent while individual operations or resources remain restricted.



Before a side-effecting operation, verify:



1\. requesting identity;

2\. agent or execution context;

3\. requested operation;

4\. target resource;

5\. applicable policy;

6\. authorization decision.



\*\*Must not happen:\*\* A valid tool request must not bypass authorization.



\## Least privilege



Tools should receive only the permissions required for their intended purpose.



Prefer narrow capabilities over unrestricted tools.



Examples:



\- read a specific resource rather than every resource;

\- update a specific field rather than arbitrary records;

\- perform one defined business action rather than arbitrary code execution.



\*\*Must not happen:\*\* An agent must not obtain broader authority simply by selecting a more powerful tool.



\## Resource isolation



When resources belong to users, teams, or tenants, authorization must cover the target resource.



Test manipulated identifiers, references, paths, and query parameters.



\*\*Must not happen:\*\* Changing a resource identifier must not grant access to another user's or tenant's data.



\## Tool argument abuse



Treat tool arguments as untrusted input.



Consider:



\- unexpected fields;

\- oversized values;

\- malformed identifiers;

\- path traversal;

\- unsupported operations;

\- conflicting parameters;

\- values designed to bypass policy checks.



\*\*Must not happen:\*\* Arguments must not change the effective authorization boundary.



\## High-impact operations



Identify tools that can:



\- delete data;

\- modify business-critical records;

\- send external communications;

\- change access or entitlement;

\- create financial effects;

\- trigger irreversible actions.



Apply stronger safeguards where the impact requires them.



\*\*Must not happen:\*\* A high-impact operation must not execute solely because an LLM selected it.



\## Cross-user and cross-tenant abuse



Test whether an agent can:



\- read another user's data;

\- modify another user's records;

\- delete another tenant's resources;

\- infer protected information through tool responses.



\*\*Must not happen:\*\* Tool execution must preserve the application's user and tenant isolation guarantees.



\## Sensitive data



Limit sensitive information exposed through:



\- tool arguments;

\- tool results;

\- logs;

\- execution records;

\- error messages.



Avoid recording secrets, credentials, tokens, or unnecessary personal data.



\*\*Must not happen:\*\* Tool execution must not become an unintended data-exfiltration channel.



\## Prompt-driven abuse



An agent may receive instructions that attempt to make it ignore normal constraints.



Authorization and policy enforcement must therefore occur outside the model's own reasoning where possible.



\*\*Must not happen:\*\* A natural-language instruction must not override application-level authorization.



\## Replay and duplicate abuse



Consider repeated submission of the same side-effecting request.



Use appropriate operation identifiers, idempotency controls, or deduplication.



\*\*Must not happen:\*\* Replaying a request must not create unintended repeated business effects.



\## Auditability



For important operations, retain enough non-sensitive evidence to determine:



\- what tool was requested;

\- who or what requested it;

\- which resource was targeted;

\- whether authorization passed;

\- whether execution occurred;

\- what terminal outcome was reached.



\*\*Must not happen:\*\* A security-relevant tool execution must not become impossible to investigate.



\## Abuse test checklist



\- \[ ] Unknown tool rejected

\- \[ ] Unauthorized operation rejected

\- \[ ] Unauthorized resource rejected

\- \[ ] Cross-tenant access rejected

\- \[ ] Malformed identifiers rejected

\- \[ ] High-impact operation protected

\- \[ ] Sensitive output controlled

\- \[ ] Replay handled safely

\- \[ ] Authorization cannot be overridden by prompt text

\- \[ ] Relevant execution evidence is retained



\## Evidence rule



Do not claim that a specific authorization or abuse control exists unless it is supported by application code, configuration, tests, or runtime evidence.

