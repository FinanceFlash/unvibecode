# Go parsing and connected graphs

UnvibeCode maps Go repositories at two levels: packages and files. This page explains what the Go parser extracts, how the connected graph resolves those records, and which cases are reported as unresolved instead of guessed.

## What is parsed

Go files are parsed with tree-sitter. The parser extracts:

- packages and their import paths
- files, functions, and methods
- receiver types for methods
- call and selector expressions inside function bodies
- `go.mod` module path, so internal imports can be distinguished from external ones

Only the standard library and third-party modules stay external. Any import that points inside the scanned module is resolved to a package in the repository.

## How edges are created

Two kinds of edges exist, and they are created by different rules.

**Package edges** come from imports. An import statement can only ever produce a package-level link. It cannot produce a file-to-file link on its own.

**File edges** come from resolved calls. A file edge is added only when all of the following are true:

1. The call target matches exactly one definition in the repository.
2. The qualifier used at the call site is the package or receiver that owns that definition.
3. The qualifier is not shadowed by a local variable, parameter, or import alias in the calling scope.
4. The symbol name is unambiguous across the resolved module.

Because the Go resolver never fills a file slot from an import, a file connection cannot be invented by construction. A missing resolution shows up as an unresolved usage, not as a guessed edge.

Same-package calls are covered, including unexported functions such as `legacyArgs()`, and receiver methods are resolved when the receiver type is known, such as `p.initTerminal()`.

## What stays unresolved

Some calls cannot be resolved statically. These are listed with file, line, receiver, and a reason, and they are not converted into edges:

- interface dispatch
- embedded types
- struct fields that hold function values
- type aliases that hide the concrete type
- calls into standard library or third-party packages

The unresolved list is the honest boundary of the graph. A large repository will have a large unresolved count for these reasons, and that is expected.

## Parse gaps

A small number of files can report a partial parse when the grammar does not cover a construct. Entities from those files are still emitted and the file is flagged, so a partial parse is visible rather than silent.

## Reference run

These results come from the same command on pinned public commits:

| Repository | Commit | Files | Final symbol edges | Package edges | Parse errors |
|---|---|---:|---:|---:|---:|
| chi | `9f8adb1` | 89 | 1,050 | 58 | 0 |
| cobra | `adbc881` | 36 | 1,362 | 12 | 0 |
| bubbletea | `f9df43c` | 116 | 1,253 | 68 | 0 |

Across these runs there are no self-links and no dangling links. Every import of the scanned module resolves, and every reported file edge points at a symbol that exists in the generated report.

## Views and token budget

The connected graph is offered in three views. Narrow is the source file on its own. Optimal and Wider pull in the callee files for the selected links, and Wider has a 75,000 token budget. When the budget is tight, the selection is trimmed rather than allowed to exceed the limit; check the token usage shown for the selection before treating a view as complete.

## Reading the graph responsibly

Package edges answer "which packages depend on which". File edges answer "which code calls which". Treat a resolved file edge as static evidence of a call site, and treat the unresolved list as the set of calls that need a human or runtime check.
