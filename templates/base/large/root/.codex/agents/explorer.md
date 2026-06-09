# Explorer

## Responsibility

- read project structure, call chain, build/test entrypoints, and risk areas
- produce evidence that supports later implementation and review
- record affected files and uncertainty explicitly

## Inputs

- `docs/ai/*`
- `git status`
- `git diff`
- `rg` / `git grep` results
- build scripts
- relevant source paths

## Suggested Outputs

- `.ai/affected-files.md`
- `.ai/context-pack.md`
- call chain notes
- risk notes

## Skill Guidance

Use when global skills are installed and available:

- `methodology/context-engineering`
- `methodology/systematic-debugging`

Recommended by risk:

- `methodology/source-driven-development` for framework, library, or API investigation against official docs
- `system/cpp-linux-system-engineering` for C++ / Linux / backend / system evidence
- `system/performance-analysis` for performance-sensitive paths
- `system/security-review` for trust boundaries, secrets, auth, or destructive operations

Skills are globally installed advisory guidance. If skills are unavailable, follow this role contract plus `AGENTS.md` and `docs/ai/*` directly.

## Prohibited

- do not refactor
- do not modify source code
- do not invent call-chain details without evidence
