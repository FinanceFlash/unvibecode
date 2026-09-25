# Contributing to UnvibeCode

Thank you for helping engineers understand connected code, reconstruct business workflows, and find evidence-backed business risks.

Contributions are welcome from Python developers, static-analysis enthusiasts, product and QA practitioners, and AI engineers. Search the existing issues and pull requests before starting. If the change is substantial, open an issue first so its scope and workflow boundary can be agreed before implementation.

## Contribution workflow

1. Fork the repository and clone your fork.
2. Create one focused branch from the latest `main`:

   ```bash
   git switch -c feature/short-description
   ```

3. Make the smallest complete change that solves the issue.
4. Add or update tests and documentation for changed behaviour.
5. Run the local quality checks and, when relevant, review a representative codebase with UnvibeCode.
6. Push the branch to your fork and open a pull request against `main`.

Keep proprietary repositories, credentials, customer data, generated customer reports, and unsanitized logs out of commits, issues, and pull requests.

## Local quality setup

This public repository currently contains documentation, workflow packs, and their validation tests. Create and activate a Python 3.11-or-newer virtual environment from the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r .github/quality/requirements.txt
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

Run the same checks used in pull requests:

```bash
python -m black --config .github/quality/pyproject.toml --check .github/quality/tests
python -m flake8 --config .github/quality/.flake8 .github/quality/tests
python -m pytest -c .github/quality/pyproject.toml .github/quality/tests
```

The test suite verifies local Markdown links, workflow-pack structure, core scenario counts, workflow boundaries, and LLM skill metadata.

## Validate changes with UnvibeCode

Use UnvibeCode when a contribution changes code-analysis behaviour, CLI behaviour, engineering guidance, or claims about how a workflow appears in code. Review a representative repository or fixture, not a proprietary customer repository:

```bash
python -m pip install --upgrade unvibecode
python -m unvibecode review --repository "/path/to/test-repository"
```

In the pull request, state:

- the UnvibeCode version used;
- the public test repository, fixture, language, and framework;
- which output was reviewed;
- what changed before and after;
- any remaining limitation.

The review is not required for wording-only documentation changes. Do not attach generated results that contain proprietary source or secrets.

## Contributing a pre-built workflow pack

Add the workflow as one clearly named folder under `prebuilt-workflow-paths/`. Copy an existing complete pack as the structural starting point and replace its content; do not leave copied people, systems, things, stages, risks, or examples from the source pack.

Every pack must contain:

- `README.md`
- `PRODUCT_AND_BUSINESS_GUIDE.md`
- `ENGINEERING_GUIDE.md`
- `CORE_20_SCENARIOS.md`
- `TESTING_GUIDE.md`
- `PATHS_AND_EDGE_CASES.md`
- `PERMISSION_AND_ABUSE_GUIDE.md`
- `RETRY_AND_RECOVERY_GUIDE.md`
- `WRITE_PRODUCT_SPEC_SKILL.md`
- `REVIEW_BUSINESS_RISK_SKILL.md`
- `UNDERSTAND_CODE_SKILL.md`
- `IMPLEMENT_WORKFLOW_SKILL.md`
- `TEST_WORKFLOW_SKILL.md`

Use the same terms that appear inside every workflow pack:

| Workflow-pack heading | What it covers |
|---|---|
| `People and systems` | The people, teams, services, providers, and other systems involved |
| `Things created or changed` | The important records, requests, payments, orders, messages, or other items affected |
| `Stages` | The meaningful points that those things move through during the workflow |
| `Must not happen` | The harmful or incorrect result that each scenario must prevent |

### MECE rules for workflow packs

MECE means the pack's scenarios should be mutually exclusive enough to avoid duplicates and collectively broad enough to cover the important business paths within its stated boundary.

1. **Define one business boundary.** State the exact event that starts the workflow and the authoritative outcomes that end it.
2. **Declare included and excluded scope.** Excluded adjacent workflows must be named explicitly. Reference their packs instead of duplicating them.
3. **Own one primary business outcome.** A pack may coordinate related effects, but it must not combine separate lifecycles such as payment, fulfilment, refund, and dispute into one oversized workflow.
4. **Keep scenarios distinct.** Each core scenario needs a different trigger, stage, permission boundary, timing condition, or failure mechanism. Rewording the same failure is not a new scenario.
5. **Cover the whole boundary.** The 20 scenarios together must include normal completion, invalid input, denied action, stage boundaries, concurrency, permission or abuse, dependency failure, partial completion, retry, and recovery where applicable.
6. **Say what must not happen.** Every core scenario must name the harmful or incorrect result to prevent, such as a duplicate charge, stale stage change, cross-tenant access, silent data loss, or contradictory customer outcome.
7. **Use one vocabulary everywhere.** `People and systems`, `Things created or changed`, `Stages`, start and end events, and outcome names must match across all guides, scenarios, and skills.
8. **Separate generic rules from code evidence.** A reusable pack may describe expected controls. It must not claim that a repository implements a control unless file, symbol, path, or runtime evidence supports that claim.
9. **Keep the five LLM skills task-specific.** Product specification, business-risk review, code understanding, implementation, and testing must have distinct instructions and outputs.
10. **Make the pack self-contained.** A reader must understand a scenario without decoding internal IDs or opening several files to learn its trigger and expected result.

Before submitting, compare every proposed scenario with the other 19. Merge duplicates, move out-of-bound scenarios to the correct adjacent workflow, and add any missing category required to cover the declared boundary.

### Workflow-pack pull request checklist

- [ ] The folder name is descriptive and has no numeric prefix.
- [ ] `README.md` gives the start, end, included scope, and excluded scope.
- [ ] The pack does not duplicate the primary outcome of an existing pack.
- [ ] Exactly 20 distinct core scenarios are present.
- [ ] Every core scenario says what `Must not happen`.
- [ ] Testing scenarios cover happy, negative, boundary, concurrency, permission, partial-failure, retry, and recovery paths where applicable.
- [ ] All 13 required files are present and use consistent terminology.
- [ ] All five LLM skill files include valid `name` and `description` frontmatter.
- [ ] The pack is linked from `prebuilt-workflow-paths/README.md`.
- [ ] Local quality checks pass.

## Contributing to the AI Engineering Cheatsheet

The `AI Engineering Cheatsheet/` series is for guidance that engineers can repeatedly apply while designing, building, reviewing, testing, or operating LLM systems in production.

Add a cheatsheet or engineering guide only when it helps a practitioner make a real production decision, prevent a credible failure, or verify that a system is ready to ship. A large collection of facts is not automatically useful guidance.

### What belongs in this series

Useful contributions may cover:

- LLM application and response architecture;
- RAG ingestion, retrieval, authorization, freshness, and evaluation;
- AI-agent tools, permissions, memory, handoffs, limits, and human approval;
- prompt and context management when connected to production behaviour;
- structured output, validation, guardrails, privacy, and security;
- testing, evaluation, red-teaming, observability, incident response, and rollback;
- latency, reliability, model selection, provider resilience, and unit economics;
- AI-assisted software engineering when the guidance applies to real development or production workflows.

The following usually do not belong:

- generic introductions to AI, machine learning, or popular tools;
- prompt collections without a production workflow or verification method;
- copied social-media carousels, interview-question dumps, or lightly rewritten blog posts;
- vendor directories or feature comparisons without a durable engineering decision;
- speculative claims presented without evidence, assumptions, or limitations;
- specialized training, GPU, hardware, or infrastructure material with no repeated relevance to production LLM application teams;
- content created mainly to increase the number of files, questions, principles, or examples.

### No AI slop or low-effort work

LLM assistance is allowed, but the contributor remains responsible for every sentence, claim, example, link, and recommendation.

A submission may be rejected when it contains:

- repetitive or generic advice that could apply to any software project;
- invented benchmarks, unsupported numbers, fake citations, or dead links;
- confident recommendations that ignore context, disadvantages, or failure modes;
- unnecessary length, duplicated sections, decorative diagrams, or terminology without practical value;
- inconsistent vocabulary or content copied from another guide in the series;
- lists produced by an LLM without engineering review, consolidation, and production validation.

Before submitting, remove filler and duplicates. Verify every external link. Challenge each recommendation with at least one realistic failure case or limitation.

### Scope and format rules

1. **Submit one focused guide per pull request.** Do not bundle unrelated cheatsheets merely because they concern AI.
2. **State the audience and production problem.** Explain who should use the guide, when they should use it, and what costly mistake it helps prevent.
3. **Make it actionable.** Use decision rules, review questions, ship checks, failure signals, examples, or acceptance criteria that can change an engineering decision.
4. **Show the downside.** Recommendations must include important limitations, trade-offs, or conditions under which another option is better.
5. **Separate facts from judgment.** Distinguish sourced facts, observed production evidence, reasoned recommendations, and unresolved assumptions.
6. **Prefer durable principles.** Avoid content that becomes obsolete with one model release unless the guide explicitly tracks versions and dates.
7. **Use visuals only when they clarify a real relationship.** Mermaid diagrams and tables should explain flow, ownership, state, comparison, or failure containment—not decorate the file.
8. **Keep the guide self-contained.** Readers should not need hidden prompts or several unrelated documents to understand and apply it.
9. **Link it from the series README.** Add a concise description to `AI Engineering Cheatsheet/README.md`.
10. **Use a descriptive filename.** Follow the naming style of existing guides and avoid unexplained abbreviations.

### Sources, inspiration, and credit

Original synthesis is expected. Do not copy a source's wording, examples, structure, or full checklist and present it as original work.

If another repository, specification, paper, article, framework, or public guide materially informed the contribution:

- link directly to the source in a `References` or `Credits` section;
- name what the source informed;
- verify that its license permits the way material was reused or adapted;
- preserve any attribution or notice required by that license;
- use short quotations only when necessary and clearly identify them as quotations;
- rewrite, extend, and validate the guidance for UnvibeCode's production-engineering audience.

Common knowledge does not need artificial citations, but verifiable technical, security, performance, or compatibility claims should use primary sources where possible. A list of references does not make copied content original.

### Cheatsheet pull request checklist

- [ ] The contribution contains one focused guide or one focused update to an existing guide.
- [ ] The guide addresses a repeated production LLM engineering decision or failure.
- [ ] The intended reader and use point are clear.
- [ ] Every section provides an actionable question, check, decision, control, or example.
- [ ] Important disadvantages, failure modes, and limitations are included.
- [ ] Claims, links, examples, and Mermaid diagrams were manually verified.
- [ ] Duplicates and generic filler were removed.
- [ ] Materially used external sources are credited and license compatibility was checked.
- [ ] No proprietary code, customer data, secrets, private prompts, or confidential incidents are included.
- [ ] `AI Engineering Cheatsheet/README.md` links to the guide.
- [ ] Local Markdown-link and quality checks pass.

## Python and analysis changes

For development checkouts that include analyzer or CLI source:

- preserve deterministic code paths unless the proposal explicitly changes them;
- preserve customer-facing filenames and CLI progress unless the product change is approved;
- add tests for changed behaviour and failure handling;
- keep supported Python versions and large-repository behaviour in mind;
- avoid exposing internal analysis-stage terminology in customer-facing output.

## Pull request expectations

A pull request must explain the problem, the chosen scope, the implemented change, verification performed, and any known limitation. Link the issue it addresses and include screenshots only when a rendered report or documentation layout changed.

By contributing, you agree that your contribution is licensed under the repository's Apache License 2.0.
