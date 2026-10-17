# Verifying workflow guards

A workflow can describe a documented precondition as though the code enforces it. Before relying on a reported guard, distinguish the intended rule, the implemented condition, and the behaviour observed in a test.

## Check the claim against the implementation

1. Save the exact report statement, UnvibeCode version, repository commit, and supporting file or symbol.
2. Find the conditional, early return, exception, or delegated check that enforces the rule. Read its actual predicate; a docstring, comment, or exception message alone does not establish the condition.
3. Exercise a valid case, a clearly invalid case, and a nearby boundary case that distinguishes the claimed rule from the implemented one. Record whether rejection happens at entry or only when a later operation needs the missing state.
4. Report the observed difference at that revision. If a runtime check is unavailable, describe the static evidence and remaining uncertainty instead of claiming a verified outcome.

## Example: application context versus request context

A completed UnvibeCode 0.3.14 review of Flask at commit `d086db856be187255b8ec61ef409357393020f32` exported this rule in `workflow_context.md`, under workflow 19, **request-scoped context management**:

> copy_current_request_context requires an active request context.

At that revision, [copy_current_request_context](https://github.com/pallets/flask/blob/d086db856be187255b8ec61ef409357393020f32/src/flask/ctx.py#L193-L204) reads `_cv_app.get(None)` and rejects only `original is None`. An application context can exist without a request, so the condition does not enforce the full requirement described by its error message.

The nearby [after_this_request](https://github.com/pallets/flask/blob/d086db856be187255b8ec61ef409357393020f32/src/flask/ctx.py#L139-L145) checks `ctx is None or not ctx.has_request`. It provides a useful control: it rejects the application-only case that the other helper accepts.

### Reproduce the distinction

Use a separate working directory and a Python virtual environment. Clone and install the exact revision; an arbitrary released Flask version may behave differently:

```text
git clone https://github.com/pallets/flask.git
git -C flask checkout d086db856be187255b8ec61ef409357393020f32
python -m pip install ./flask
```

Save the following as `check_context_guards.py` beside the `flask` directory, then run `python check_context_guards.py`. It imports the pinned checkout directly, starts no server, and invokes the callback synchronously.

```python
from contextlib import nullcontext
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / "flask" / "src"))

from flask import Flask, after_this_request, copy_current_request_context
from flask import has_request_context

app = Flask(__name__)

for name, context in (
    ("none", nullcontext()),
    ("application only", app.app_context()),
    ("request", app.test_request_context("/")),
):
    with context:
        try:
            callback = copy_current_request_context(has_request_context)
            copied = f"accepted; callback has request={callback()}"
        except RuntimeError:
            copied = "rejected"

        try:
            after_this_request(lambda response: response)
            after = "accepted"
        except RuntimeError:
            after = "rejected"

        print(f"{name}: copy={copied}; after={after}")
```

Observed with Python 3.13.7 on Windows, using the pinned Flask checkout:

```text
none: copy=rejected; after=rejected
application only: copy=accepted; callback has request=False; after=rejected
request: copy=accepted; callback has request=True; after=accepted
```

The distinguishing case is **application only**. The callback runs without a request; an error would occur later if it tried to use request-only data. This check establishes the entry-guard mismatch, not the safety of background execution, thread isolation, or session mutation.

To generate a review for comparison, install `unvibecode==0.3.14`, run `python -m unvibecode review --repository ./flask`, and inspect the workflow rules in the exported context ZIP. Generated wording may vary between runs; the quoted rule above records the observed output, not an assertion that every run will produce it.

## Describe the result precisely

For this example, an evidence-supported description is: "The helper rejects a missing application context, but does not explicitly reject an application-only context without a request. Its error message describes a request-context requirement."

Include the pinned source, exact report claim, reproduction, and observed result when filing a report-accuracy issue. Keep the reported rule separate from any claim that the repository has a confirmed business risk or that accepting the boundary case is intended behaviour.

This example is tracked in [issue #248](https://github.com/FinanceFlash/unvibecode/issues/248). The guide helps readers validate output; it does not change the analyzer or resolve that issue.

Return to [Understanding UnvibeCode Outputs](OUTPUTS.md).
