# How UnvibeCode Works

UnvibeCode combines local repository analysis with hosted business workflow and risk review.

## 1. Local repository mapping

The package reads supported source files and builds a resolved graph containing files, symbols, imports, calls, and connected code relationships.

## 2. Connected context preparation

Source code is divided into ordered chunks. The graph is used to prepare focused and connected contexts without repeatedly copying the same source into every package.

## 3. Business workflow reconstruction

Relevant structured context is reviewed to connect entry points, decisions, state transitions, external effects, and business outcomes into understandable workflows.

## 4. Critical risk review

Completed workflows are reviewed for failures that can materially affect customers, money, permissions, data integrity, operations, or other business outcomes. Findings must pass evidence checks before appearing in the customer report.

## 5. Customer report generation

UnvibeCode renders the interactive code map, repository-context ZIP, workflow map, and risk findings as customer-ready files.

## Repository-size branches

### Repositories at or below approximately two million source tokens

UnvibeCode prepares the Connected Code Map and complete Business Workflow and Risk Review.

### Repositories above approximately two million source tokens

UnvibeCode prepares:

- Connected Code Map for LLMs
- Complete Repository Context

The deeper Business Workflow and Risk Review is not started for repositories above the supported threshold.

This prevents an oversized repository from entering a long hosted review while still giving the customer useful graph and LLM-context deliverables.

