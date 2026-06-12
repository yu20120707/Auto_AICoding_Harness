# Reviewed Final Design v1

## Positioning

- Repository name: `Auto_AICoding_harness`
- Primary identity: `Codex-first, multi-agent-compatible AI Coding Harness`
- First shipping profile: `cpp-linux-backend-system`
- Intended user: ourselves

This repository is published for reuse across our own future repositories.
It is not a generic framework and not a target-project runtime.

## Core Decision

The system is split into:

- `core`: workflow contract layer
- `profile`: engineering policy layer
- `templates`: only source of generated target-project files
- `skills`: portable repository-owned skill source
- `global`: user-level instruction templates
- `prompts`: one-time local-agent setup prompts

## Core Owns

- `small / medium / large` mode semantics
- requirement-clarification behavior across all modes
- review-gate rules
- handoff and context-pack contracts
- command contracts
- state contracts
- generated-file safety policy
- downgrade behavior when `subagent` or `skills` are unavailable

`core` must not directly encode `cmake`, `ctest`, `clang-tidy`, or similar profile policy.

## Profile Owns

- `C++ / Linux / backend / system` review focus
- build, test, and check expectations
- engineering overlays for prompts, skills, and generated docs
- profile-specific target-project templates
- profile metadata such as languages, domains, risk triggers, and verification defaults

`profile` must not redefine the workflow state machine or bypass review gates.

## Mode Model

`small`, `medium`, and `large` are different control strengths on one workflow.

All three modes should start with the same requirement clarification pass:

- restate target
- restate scope
- restate constraints
- restate verification intent

If ambiguity remains and the user did not explicitly say not to ask questions, the agent should ask targeted clarification questions before implementation.

`small`:

- current implementation does not create `spec.md`
- `spec.md` currently appears in the `large` overlay only
- does not require `spec` or `plan` approval gates
- current implementation realizes `spec`, `plan`, `diff`, and `final` review / approve / reject
- may skip `context-pack` and `handoff`

`medium`:

- current implementation adds `.ai/implementation-plan.md`, `.ai/run-trace.md`, and `.ai/verification.md`
- keeps the same state shape as `small` and `large`
- does not enforce the `spec -> plan -> diff -> final` chain
- may use bounded reviewer/scanner coordination without the full large scaffold

`large`:

- design target requires `spec`, `plan`, `diff`, and `final`
- current implementation realizes `spec`, `plan`, `diff`, and `final` gate chains with enforced ordering
- current implementation now also syncs a task-scoped evidence chain under `docs/ai/tasks/<task-id>/`
- treats `context-pack` and `handoff` as standard capabilities
- may use `subagent` and `skills`
- must remain executable without them

## Subagent and Skill Position

- `subagent` is a `large`-mode acceleration layer
- `skills` are repository-owned portable guidance installed explicitly by the active local agent
- `.ai/subagent-packets/` is the large-mode prompt/context protocol for bounded role delegation
- neither is a correctness dependency
- absence of either must fall back to the same artifacts and gate semantics

## Runtime and Long-lived Knowledge

In generated target projects:

- `docs/ai/` = long-lived project knowledge
- `.ai/` = task runtime
- `.codex/agents/` = optional project agent config when enabled
- `.github/copilot-instructions.md` = lightweight Copilot trigger instructions
- `CLAUDE.md` = optional Claude-compatible shim to `AGENTS.md`
Global skills live outside target projects or in a supported project skill directory chosen by the active local agent.

In this harness repository:

- live root `.ai/`, `.codex/`, `.agents/` are not product structure
- those contents exist only as template source under `templates/`

## Safety Contract

- default write result: `SKIPPED`
- overwrite result with `--force`: `OVERWRITTEN`
- overwrite requires `--force`
- `--force` must back up each overwritten file into target-project `.ai/backups/<timestamp>/`
- overwrite backup metadata should remain inspectable through a manifest under the same backup root
- no default delete behavior
- no writes to business source code or business directories

## Shipping Baseline

The original stable baseline shipped in this repository was:

- audited design documents
- repository boundary rules
- template-source skeleton
- initial `cpp-linux-backend-system` profile scaffold

The current implementation baseline is `v1.7-optimization-hardening`.
Actual command implementation should conform to the adjacent contract documents, with future-only capabilities marked explicitly as not implemented.
