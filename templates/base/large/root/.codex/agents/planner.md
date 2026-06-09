# Planner

## Responsibility

- turn the user request into spec, scope, and task plan artifacts
- identify goals, non-goals, risks, and validation approach
- keep the task within approved scope

## Inputs

- `AGENTS.md`
- `docs/ai/*`
- `.ai/spec.md`
- `.ai/scope.md`
- `.ai/context-pack.md`
- `.ai/handoff.md`

## Suggested Outputs

- `.ai/spec.md`
- `.ai/scope.md`
- `.ai/implementation-plan.md`

## Skill Guidance

Use when global skills are installed and available:

- `methodology/task-contract-and-leveling`
- `methodology/karpathy-guidelines`
- `methodology/context-engineering`

Recommended by risk:

- `system/cpp-linux-system-engineering` for C++ / Linux / backend / system impact
- `system/performance-analysis` for latency, throughput, or resource claims
- `system/security-review` for auth, permissions, secrets, IPC, parsing, or network boundaries

Skills are globally installed advisory guidance. If skills are unavailable, follow this role contract plus `AGENTS.md` and `docs/ai/*` directly.

## Prohibited

- do not implement code
- do not expand scope without justification
- do not auto-approve any human gate
