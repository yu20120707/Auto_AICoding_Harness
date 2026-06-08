# AGENTS.md

## Purpose

This repository is the source of truth for `Auto_AICoding_harness`.
It is not a generated target project.

## Default Working Rules

Before making non-trivial changes:

1. read `README.md`
2. read `docs/design/reviewed-final-design-v1.md`
3. read any contract file directly affected by the change

## Repository Boundaries

- `templates/` contains template source only
- `profiles/` contains engineering overlays only
- `docs/design/` contains workflow and repository contracts
- root live `.ai/`, `.codex/`, `.agents/` are not product structure and should stay ignored if created locally

## Editing Rules

- Do not move target-project runtime files into the harness root.
- Do not couple core workflow contracts to `C++`, `Linux`, `CMake`, or other profile policy.
- Do not create duplicate truths for generated files outside `templates/`.
- Prefer small, local edits that preserve contract clarity.

## Verification

For doc and skeleton changes, verify by:

1. checking repository structure
2. checking cross-file consistency of command, state, and boundary terms
3. checking `.gitignore` behavior for root runtime directories
