# Tech Design

## Proposed Modules

- `core/state/task_state.py`: data model helpers for task supplement loading, normalization, and summary.
- `core/state/schema.py`: schema validation for task supplement payloads.
- `core/state/transition.py`: legal transition table and transition validation.
- `bin/ai-status`: optional integration point to display task supplement information when present.
- `tests/test_task_state.py`: focused tests for schema and transitions.

The exact module split may be adjusted if the current `core/` layout makes a smaller change cleaner. The implementation should prefer local patterns over a new framework.

## Data Location

The planned supplement location is:

```text
.ai/tasks/<task-id>/task.json
```

This file is optional in Phase 1. Existing projects without it remain valid.

## Relationship To Existing State

`.ai/state.json` remains the command-level workflow state. The new task supplement must not replace it.

Expected relationship:

- `.ai/state.json::task_id` identifies the active large task.
- `.ai/tasks/<task-id>/task.json` may provide structured task details.
- `docs/ai/tasks/<task-id>/` remains the durable evidence chain.

## Minimal Schema Direction

The initial schema should include:

- `schema_version`
- `id`
- `mode`
- `status`
- `source`
- `scope`
- `artifacts`
- `created_at`
- `updated_at`

Review and approval fields may be included if they remain passive metadata in Phase 1. Active review state changes should stay with existing `ai-review`, `ai-approve`, and `ai-reject` behavior until Phase 3.

## Transition Direction

The transition validator should be a pure function that accepts current status and next status, then returns success or a clear failure. It should be easy to test without filesystem setup.

## Integration Direction

`ai-status` may display:

- active task supplement path
- task supplement status
- validation status
- next suggested action when validation fails

It must continue to work when the supplement file is absent.

## Risks

- Creating a second state system instead of a supplement.
- Letting Phase 1 expand into context manifest or review-gate rewrites.
- Accidentally requiring `small` or `medium` to create task supplements.
- Naming states in a way that conflicts with existing gate statuses.
