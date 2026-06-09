# Repository Boundaries

## Repository Type

This repository stores harness source artifacts.
It does not store live target-project runtime artifacts.
Phase 8 adds release and usage documentation, not new runtime behavior.

## Source vs Generated

### Source owned by this repository

- `docs/`
- `templates/`
- `skills/`
- `global/`
- `profiles/`
- `prompts/`
- `scripts/`
- `examples/`

### Generated into target projects

- `AGENTS.md`
- `CLAUDE.md`
- `.github/copilot-instructions.md`
- `docs/ai/**`
- `.ai/**`
- `.codex/**` when agent config templates are enabled

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
Global skills are not generated into target projects.
They are installed explicitly from this repository's `skills/` directory into a tool-supported skill root.
`bin/ai-install-skills` is the Codex example installer only.
Other tools should follow `docs/install-targets.md` and `prompts/bootstrap-local-agent.md`.

Expected ignored generated runtime content:

- `.ai/state.json`
- `.ai/run-trace*`
- `.ai/reviews/**`
- `.ai/approvals/**`
- `.ai/subagent-packets/**`
- `.ai/backups/**`
- `.ai/tmp/**`
- `.ai/context-pack.md`
- `.ai/handoff.md`
