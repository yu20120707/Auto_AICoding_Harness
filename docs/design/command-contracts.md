# Command Contracts

## Command Set

The current implemented command set in `v0.8-release-baseline` is:

- `ai-init`
- `ai-upgrade`
- `ai-status`
- `ai-review`
- `ai-approve`
- `ai-reject`
- `ai-context-pack`
- `ai-handoff`

The following command names remain design-level only and are not implemented yet:

- `ai-state`

## Contract Principles

- each command has one primary responsibility
- human-facing summary and machine-facing state are separate concerns
- commands do not silently expand scope into machine-global setup and repo-local initialization at the same time
- profile-specific checks are injected through overlays, not hard-coded into core command semantics

## Responsibilities

### `ai-init`

- initializes a target repository with base harness content
- currently supports only `small`
- must honor `SKIPPED` and `--force + backup`

### `ai-upgrade`

- upgrades a target repository from a lower control strength to a higher one
- default first upgrade path is `small -> large`
- must not delete existing target-project files by default

### `ai-status`

- presents a human-readable task summary
- reads from `state.json` and related runtime files
- must not create a second state system

### `ai-state`

- outputs canonical structured state
- is the machine-facing state entrypoint
- should remain thin over `state.json`

### `ai-review`

- generates gate-specific review artifacts
- only covers review generation, not state approval
- current implementation supports `spec`, `plan`, `diff`, and `final`
- `spec`, `plan`, and `final` only generate review material and move state into the corresponding waiting gate

### `ai-approve`

- records explicit approval for a gate
- advances state when approval is valid
- current implementation supports `spec`, `plan`, `diff`, and `final`

### `ai-reject`

- records explicit rejection for a gate
- moves state into the relevant retry or blocked path
- current implementation supports `spec`, `plan`, `diff`, and `final`

### `ai-context-pack`

- packages context for long-running or resumed work
- does not advance state
- is available in both `small` and `large` projects after initialization

### `ai-handoff`

- writes a clean transfer artifact for next-session continuation
- does not advance state
- is available in both `small` and `large` projects after initialization

## Gate Policy

`small`:

- `spec` and `plan` review commands exist, but require their source artifacts to be present
- `diff` review is implemented
- `final` review is implemented
- `spec`, `plan`, `diff`, and `final` all have approve / reject support

`large`:

- `spec`, `plan`, `diff`, and `final` review are implemented
- `spec`, `plan`, `diff`, and `final` approve / reject are implemented

## Out of Scope for Core Command Contracts

- `cmake`
- `ctest`
- `clang-tidy`
- compiler selection
- sanitizer strategy
- performance tooling choice

Those belong to the active profile overlay.

## Release Baseline Note

Phase 8 adds no new commands.
It is a release-baseline alignment pass over documentation, usage guidance, and end-to-end verification.
