# Implementation Plan

## Phase 1 Only

This plan intentionally covers only large-mode task state hardening. Later phases from `docs/design/trellis-inspired-v1.7-hardening.md` remain out of scope.

## Steps

1. Confirm the current state and gate contracts.
   - Read `core/state.py`, `core/state_machine.py`, `core/task_chain.py`, `bin/ai-status`, and `docs/design/command-contracts.md`.
   - Verify the implementation continues to treat `.ai/state.json` as command-level workflow state.

2. Add focused task-state helpers.
   - Add a minimal schema validation surface under `core/state/` or the closest existing local pattern.
   - Add transition validation as a pure, easily tested function.
   - Keep file IO thin and optional.

3. Integrate with status reporting.
   - Update `ai-status` only enough to summarize task supplement status when the supplement exists.
   - Preserve current output for projects without the supplement.

4. Add tests.
   - Cover valid and invalid schema payloads.
   - Cover valid and invalid transitions.
   - Cover status behavior with no supplement present.
   - Cover status behavior with a valid supplement present.

5. Run targeted verification.
   - Compile Python sources.
   - Run new task-state tests.
   - Run status/state/large-upgrade/review-related regression tests.

6. Prepare review artifacts.
   - Update `.ai/run-trace.md`.
   - Record verification in `.ai/verification.md`.
   - Generate or update diff review before approval.

## Stop Conditions

- The implementation starts changing public command names.
- The implementation requires `small` or `medium` task supplements.
- The implementation rewrites existing gate ordering.
- The implementation starts Phase 2 context manifest work.

## Planned Review Gates

- `ai-review spec`
- `ai-approve spec`
- `ai-review plan`
- `ai-approve plan`
- implementation
- `ai-review diff`
- final verification
- `ai-review final`
