# Repository Boundaries

## Repository Type

This repository stores harness source artifacts.
It does not store live target-project runtime artifacts.
Phase 8 adds release and usage documentation, not new runtime behavior.

## Source vs Generated

### Source owned by this repository

- `docs/`
- `templates/`
- `profiles/`
- `prompts/`
- `scripts/`
- `examples/`

### Generated into target projects

- `AGENTS.md`
- `docs/ai/**`
- `.ai/**`
- `.codex/**` when agent config templates are enabled
- `.agents/**` when project-coupled skills are enabled

## Template Rule

`templates/` is the only template source of truth.

Do not maintain a second copy of generated target-project files in the harness root.

## Root Runtime Rule

Live root directories below are ignored in this repository if created locally:

- `.ai/`
- `.codex/`
- `.agents/`

They are target-project semantics, not harness product structure.

## Overlay Rule

Generation flow is:

1. apply `templates/base`
2. apply active profile overlay
3. write target-project output using safe-write policy

## Safe-write Policy

- existing file without `--force`: `SKIPPED`
- overwrite only with `--force`
- `--force` requires per-file backup
- default behavior never deletes files

## Commit Policy for Generated Projects

Expected long-lived generated project content:

- `AGENTS.md`
- `docs/ai/**`
- `.codex/agents/**` when the project adopts agent config
- `.agents/skills/**` when those skills are project-coupled

Expected ignored generated runtime content:

- `.ai/state.json`
- `.ai/run-trace*`
- `.ai/reviews/**`
- `.ai/approvals/**`
- `.ai/backups/**`
- `.ai/tmp/**`
- `.ai/context-pack.md`
- `.ai/handoff.md`
