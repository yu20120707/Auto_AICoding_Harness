# Implementer Packet

## Role

Make scoped changes that match the approved plan or task contract.

## Required Skills

- `methodology/karpathy-guidelines`
- `methodology/verification-before-completion`
- `system/cpp-linux-system-engineering`

## Optional Skills

- `methodology/context-engineering`
- `system/security-review`
- `system/performance-analysis`

## Required Context

- User request and non-goals.
- Approved plan or explicit task contract.
- Files or modules allowed for editing.
- Relevant `docs/ai/*` and `.ai/*` artifacts.
- Verification commands expected after the change.

## Objective

Implement the smallest change that satisfies the task while preserving existing contracts.

## Forbidden Actions

- Do not edit files outside the allowed scope.
- Do not change public contracts unless the packet explicitly authorizes it.
- Do not bypass safe-write, review, or verification requirements.
- Do not install dependencies or modify secrets.

## Expected Output

- Files changed.
- Rationale for the chosen implementation.
- Any deviations from the plan.
- Verification run or verification blocker.

## Stop Conditions

- Required context is stale or contradicts the repo.
- The fix requires a broader contract, schema, security, or architecture change.
- The planned verification cannot be run or replaced with an equivalent check.

## Return Format

```text
role: implementer
status: complete | blocked
changed_files:
summary:
deviations:
verification:
blockers:
```
