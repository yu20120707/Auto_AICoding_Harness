# Spec

## Objective

Add Phase 1 task-state hardening as an internal large-mode supplement. The implementation should create a small, explicit task-state model that can validate task metadata and state transitions without replacing `.ai/state.json` or the existing review gate chain.

## Current Baseline

- `core/state.py` owns `.ai/state.json`.
- `core/state_machine.py` owns existing gate ordering for `spec`, `plan`, `diff`, and `final`.
- `core/task_chain.py` syncs large evidence into `docs/ai/tasks/<task-id>/`.
- `ai-status` reads current state and reports next actions.
- `small` and `medium` must remain usable without structured task-state supplements.

## Required Behavior

1. Define a structured task-state schema for large-mode task supplements.
2. Validate required task fields, supported modes, supported statuses, and artifact references.
3. Validate legal state transitions for the new supplement.
4. Reject illegal state transitions with clear errors.
5. Keep `.ai/state.json` as the canonical workflow state for existing commands.
6. Allow `ai-status` to report supplement state when the supplement exists.
7. Make the new behavior optional for existing projects that do not yet have `.ai/tasks/TASK-*`.

## Compatibility Constraints

- No new public command is required for Phase 1.
- No generated project should be migrated from `.ai/ + docs/ai/` to another control plane.
- No change may require `small` or `medium` to create `task.json`.
- No change may weaken current large gate ordering.
- No change may hard-code C++ build tools into core task-state semantics.

## State Model Scope

The first version should cover only the states needed to support large-mode implementation flow:

```text
planning
ready
implementing
reviewing
waiting_approval
approved
rejected
needs_fix
finalizing
completed
blocked
```

The design may add narrower names if implementation evidence shows the existing gate statuses map better to another set. Any deviation must be recorded in `.ai/run-trace.md`.

## Success Criteria

- Unit tests cover valid schema, invalid schema, valid transitions, and invalid transitions.
- Integration-style checks cover `ai-status` with and without the task supplement.
- Existing command behavior still matches `docs/design/command-contracts.md`.
- Documentation states that the task supplement is optional and large-mode-first.
