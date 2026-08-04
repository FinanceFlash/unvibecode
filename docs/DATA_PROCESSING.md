# Data Processing and Privacy

This document explains the product-level data flow. It is not a substitute for contractual privacy or security terms.

## Processing performed locally

The installed Python package performs the following operations on the customer's computer:

- Repository scanning
- File and language detection
- Dependency and symbol mapping
- Connected graph construction
- Code chunk preparation
- Context-package assembly
- HTML and ZIP rendering

## Processing performed through the hosted service

Structured code context required for business workflow and risk analysis is securely sent to the hosted UnvibeCode service.

Customers do not provide an OpenAI API key. Model-provider credentials remain on the hosted service.

## Customer responsibilities

- Review only repositories you are authorized to process.
- Do not include secrets, credentials, private keys, or regulated data that is unnecessary for the review.
- Remove generated files or local configuration containing sensitive values before analysis.
- Follow your organization's source-code and third-party-processing policies.

## Operational metadata

The hosted service may process request metadata needed for reliability, security, abuse prevention, and troubleshooting. Current preview access and usage controls are described in [PUBLIC_PREVIEW.md](PUBLIC_PREVIEW.md).

Before using UnvibeCode for highly sensitive or regulated repositories, obtain any organizational approvals required for hosted code analysis.

