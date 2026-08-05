# Retry and Recovery Guide

## Partial failures
- Account access is restricted but deletion jobs are not created
- Primary database deletes but cache, index, file, analytics, or replica fails
- Local deletion completes but processor instruction fails
- Processor completes but acknowledgement is lost
- Deletion tasks complete but request status or customer confirmation fails
- Backup restore or late event reintroduces data

## Recovery rules
- Use request, account, tenant, data-item, task, processor, and policy-version identities consistently.
- Re-read identity, scope, holds, current data, and task state before retrying.
- Never mark complete until every mandatory location has a resolved outcome.
- Make retained exceptions and failed or uncertain tasks visible.
- Reconcile account, systems, processors, backups, reappearance controls, evidence, and communication.

