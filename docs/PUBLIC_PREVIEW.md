# UnvibeCode Public Preview

## Current customer experience

During the current public preview:

- No activation key is required.
- No customer OpenAI API key is required.
- The repository path is the only required review input.
- The Python package uploads eligible source files; analysis runs on our hosted service.
- For a local-only graph, fork the graph source in `src/unvibecode_graph/`; no API key or upload is required.
- Hosted business analysis is available subject to service reliability and technical safety protections.

Hosted AI analysis uses our OpenAI API credentials. We will introduce bring-your-own-key support shortly, so you can use your own API credentials.

We do not retain your uploaded source code or analysis results on our server after processing. Results are downloaded to your computer. OpenAI processes the AI requests under its own data policies.

Full workflow and risk analysis supports up to approximately two million estimated source tokens. Larger repositories receive graph and context outputs only, subject to [upload limits](LIMITATIONS.md).

## Service protections

Request-size, concurrency, abuse-prevention, and infrastructure protections may operate without changing the normal two-command customer workflow.

## Request a public-repository review

Maintaining or evaluating a public repository?

Email [divya.singaravelu@iiml.org](mailto:divya.singaravelu@iiml.org) with:

- The public GitHub repository URL
- The workflow or code area you want to understand
- The question you want the analysis to answer
- Permission to publish the resulting maps or findings, if applicable

Only submit repositories that you are authorized to analyze.

## Future changes

Usage controls, account-based access, or paid plans may be introduced after actual demand and operating costs are understood. Material changes should be announced in the package release notes and this document.

Public-preview availability is not a service-level agreement.
