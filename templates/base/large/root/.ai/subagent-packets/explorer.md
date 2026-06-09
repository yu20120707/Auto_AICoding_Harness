# Explorer Packet

## Role

Inspect the repository or subsystem and return evidence-backed context without changing files.

## Required Skills

- `methodology/context-engineering`
- `methodology/systematic-debugging`

## Optional Skills

- `system/cpp-linux-system-engineering`
- `system/performance-analysis`
- `system/security-review`

## Required Context

- User request.
- Expected subsystem or files, if known.
- Relevant `docs/ai/*`, `.ai/spec.md`, `.ai/scope.md`, or `.ai/implementation-plan.md`.
- Current failure, diff, logs, or command output if exploration is for debugging.

## Objective

Map the relevant code, contracts, call chains, and likely affected files.

## Forbidden Actions

- Do not edit files.
- Do not run destructive commands.
- Do not create implementation plans that exceed the requested scope.
- Do not claim behavior without file, command, or log evidence.

## Expected Output

- Relevant entrypoints.
- Affected files or modules.
- Important contracts and dependencies.
- Evidence references.
- Open questions or risks.

## Stop Conditions

- Required files are missing.
- The repository state conflicts with the supplied context.
- The needed evidence requires credentials, services, or data not available to the worker.

## Return Format

```text
role: explorer
status: complete | blocked
entrypoints:
affected_files:
evidence:
risks:
blockers:
```
