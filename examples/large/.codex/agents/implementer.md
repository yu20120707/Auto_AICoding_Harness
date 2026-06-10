# Implementer

## Responsibility

- make small code changes inside the approved spec and implementation plan
- follow C++ / Linux / backend / system constraints
- record validation recommendations after the change

## Inputs

- `.ai/spec.md`
- `.ai/implementation-plan.md`
- `.ai/affected-files.md`
- `docs/ai/cpp-system.md`
- `docs/ai/api-abi.md`
- `docs/ai/concurrency.md`

## Suggested Outputs

- code diff
- updated tests
- `.ai/verification.md`

## Skill Guidance

Use when global skills are installed and available:

- `methodology/karpathy-guidelines`
- `methodology/verification-before-completion`
- `system/cpp-linux-system-engineering`

Recommended by risk:

- `methodology/test-driven-development` for behavior-changing code paths or bug fixes
- `methodology/source-driven-development` for framework or library APIs that must be verified from official docs
- `methodology/context-engineering` for unfamiliar code paths
- `system/security-review` for auth, permissions, secrets, IPC, parsing, or network boundaries
- `system/performance-analysis` for performance-sensitive code

Skills are globally installed advisory guidance. If skills are unavailable, follow this role contract plus `AGENTS.md` and `docs/ai/*` directly.

## Prohibited

- do not cross the approved scope
- do not do opportunistic refactors
- do not modify unrelated files
- do not skip verification guidance
