## Problem and scope

Describe the user problem and the focused scope of this change.

## What changed

Summarize the implementation or content change.

## Verification

List the commands, fixtures, public repositories, and outputs used to verify the change.

- [ ] `python -m black --check tests`
- [ ] `python -m flake8 tests`
- [ ] `python -m pytest`
- [ ] I used UnvibeCode on a representative repository when the change affects code analysis, CLI behaviour, engineering guidance, or code-specific claims.
- [ ] I updated documentation for changed user-facing behaviour.
- [ ] I included no credentials, proprietary source, customer data, generated customer reports, or unsanitized logs.

## Workflow-pack checks

Complete these items only when adding or changing a pre-built workflow pack.

- [ ] The start, end, included scope, and excluded scope are explicit.
- [ ] The pack owns one primary business outcome and does not duplicate an existing pack.
- [ ] The 20 core scenarios are distinct and collectively cover the declared boundary.
- [ ] Every core scenario states what must not happen.
- [ ] All 13 required files use consistent actors, objects, states, and outcome names.

## Remaining limitations

List any known limitation or follow-up issue.
