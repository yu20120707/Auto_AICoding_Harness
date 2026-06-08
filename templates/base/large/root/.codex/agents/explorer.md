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

## Prohibited

- do not refactor
- do not modify source code
- do not invent call-chain details without evidence
