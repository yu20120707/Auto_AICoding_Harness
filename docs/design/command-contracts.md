# Command Contracts

## Command Set

The current implemented command set in `v1.7-optimization-hardening` is:

- `ai-init`
- `ai-install-skills`
- `ai-upgrade`
- `ai-doctor`
- `ai-status`
- `ai-state`
- `ai-dispatch`
- `ai-review`
- `ai-approve`
- `ai-reject`
- `ai-context-pack`
- `ai-handoff`

No command names are currently reserved here as design-level only.

## Contract Principles

- each command has one primary responsibility
- human-facing summary and machine-facing state are separate concerns
- commands do not silently expand scope into machine-global setup and repo-local initialization at the same time
- profile-specific checks are injected through overlays, not hard-coded into core command semantics
- command permission levels should be representable in code, not only in prose

## Responsibilities

### `ai-install-skills`

- installs a manifest-selected subset of repository-owned skills from `skills/` into the user's global Codex skills directory as a Codex example installer
- defaults to `$CODEX_HOME/skills` or `~/.codex/skills`
- does not run during `git clone`
- does not fetch third-party skills
- does not install global `AGENTS.md`, Claude, Copilot, or generic-agent files
- supports `--dry-run` to show planned Codex skill writes without changing files
- supports `--list` to inspect the selected manifest set without writing files
- supports `--scope` and `--profile` filters for selecting system or profile skills
- existing skills are skipped unless `--force` is passed
- `--force` backs up overwritten skills under `skill-backups/<timestamp>/`
- real installs write an installed-skills manifest outside the target-project runtime

### `ai-init`

- initializes a target repository with base harness content
- currently supports `small` and `medium`
- `medium` adds `.ai/implementation-plan.md`, `.ai/run-trace.md`, and `.ai/verification.md`
- must honor `SKIPPED` and `--force + backup`

### `ai-upgrade`

- upgrades a target repository from a lower control strength to a higher one
- supports `small -> medium`, `small -> large`, and `medium -> large`
- does not support downgrades
- creates large-mode planning, review, approval, optional agent-role, and subagent packet skeletons
- validates the existing state before upgrading
- prints upgrade evidence plus the next recommended action after a successful transition
- must not delete existing target-project files by default

### `ai-doctor`

- diagnoses harness health without changing workflow state
- checks `.ai/state.json`, generated-file presence, and obvious mode mismatches
- supports human-readable and `--json` output
- should be used when `ai-status` suggests something is inconsistent or when a workflow transition is in doubt

### `ai-status`

- presents a human-readable task summary
- reads from `state.json` and related runtime files
- includes next-action guidance derived from the current state
- surfaces whether the loaded state shape is valid
- must not create a second state system

### `ai-state`

- outputs canonical structured state
- is the machine-facing state entrypoint
- should remain thin over `state.json`
- prints `UNINITIALIZED` JSON when no `.ai/state.json` exists

### `ai-dispatch`

- appends a standardized subagent dispatch record to `.ai/run-trace.md`
- only works in initialized `large` mode
- reads `.ai/subagent-packets/<role>.md` to expand `Required Skills` and `Optional Skills`
- records skill assignment, scope, objective, expected output, and result location
- does not start or manage subagents
- does not advance state

### `ai-review`

- generates gate-specific review artifacts
- only covers review generation, not state approval
- current implementation supports `spec`, `plan`, `diff`, and `final`
- in `large` mode, enforces the gate chain `spec -> plan -> diff -> final`
- `spec`, `plan`, and `final` only generate review material and move state into the corresponding waiting gate
- `final` review can summarize `.ai/verification.md` when the target project records command evidence there

### `ai-approve`

- records explicit approval for a gate
- advances state when approval is valid
- current implementation supports `spec`, `plan`, `diff`, and `final`
- `final` approval also requires meaningful verification evidence in `.ai/verification.md`

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

`medium`:

- `spec`, `plan`, `diff`, and `final` review are implemented when the corresponding artifact exists
- uses the same state format as `small` and `large`
- does not enforce the `spec -> plan -> diff -> final` chain
- is intended to keep `.ai/implementation-plan.md`, `.ai/run-trace.md`, and `.ai/verification.md` current during bounded multi-file work

`large`:

- `spec`, `plan`, `diff`, and `final` review are implemented
- `spec`, `plan`, `diff`, and `final` approve / reject are implemented
- `plan` review requires `spec` approval first
- `diff` review requires `plan` approval first
- `final` review requires `diff` approval first
- `final` approval requires meaningful verification evidence

## Out of Scope for Core Command Contracts

- `cmake`
- `ctest`
- `clang-tidy`
- compiler selection
- sanitizer strategy
- performance tooling choice

Those belong to the active profile overlay.

## Command Permission Model

`core/command_policy.py` is the code-level classification for read-only, artifact-generation, workflow-transition, and user-approval commands.
It does not replace user-facing docs, but it gives the repository one place to keep command permission semantics consistent.

## Release Baseline Note

Phase 8 originally added no new commands.
The current baseline extends that surface with `ai-install-skills`, `ai-state`, `ai-context-pack`, `ai-handoff`, `ai-dispatch`, and `ai-doctor` while keeping the same workflow contract model.
