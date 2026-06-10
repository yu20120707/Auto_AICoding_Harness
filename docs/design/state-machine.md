# State Machine

## Source of Truth

Target-project workflow state is represented by `.ai/state.json`.

If `.ai/state.json` does not exist, the target repository is `UNINITIALIZED`.

## Minimum State Shape

```json
{
  "schema_version": 1,
  "mode": "small",
  "profile": "cpp-linux-backend-system",
  "status": "INIT",
  "current_gate": null,
  "approved_gates": [],
  "created_by": "Auto_AICoding_Harness",
  "task_id": "20260608-001",
  "task_title": "short human title",
  "updated_at": "2026-06-08T12:00:00+08:00"
}
```

## Required Fields

- `schema_version`
- `mode`
- `profile`
- `status`
- `current_gate`
- `approved_gates`
- `created_by`
- `task_id`
- `task_title`
- `updated_at`

## Implemented States In `v0.8-release-baseline`

- `INIT`
- `WAITING_HUMAN_SPEC_APPROVAL`
- `SPEC_APPROVED`
- `WAITING_HUMAN_PLAN_APPROVAL`
- `PLAN_APPROVED`
- `WAITING_HUMAN_DIFF_APPROVAL`
- `DIFF_APPROVED`
- `NEEDS_FIX`
- `WAITING_HUMAN_FINAL_APPROVAL`
- `DONE`
- `NEEDS_REPLAN`
- `NEEDS_MORE_TESTS`

## Reserved Future States

- `SPEC_DRAFTED`
- `PLAN_DRAFTED`
- `IMPLEMENTING`
- `IMPLEMENTED`
- `AI_REVIEWED`
- `EVALUATING`
- `EVALUATED`
- `BLOCKED`
- `ABORTED`

## Rules

- `small` and `large` currently share the same initialized base state shape
- `ai-review spec` can move state to `WAITING_HUMAN_SPEC_APPROVAL`
- `ai-approve spec` can move state to `SPEC_APPROVED`
- `ai-reject spec` can move state to `NEEDS_REPLAN`
- `ai-review plan` can move state to `WAITING_HUMAN_PLAN_APPROVAL`
- `ai-approve plan` can move state to `PLAN_APPROVED`
- `ai-reject plan` can move state to `NEEDS_REPLAN`
- `ai-review diff` can move state to `WAITING_HUMAN_DIFF_APPROVAL`
- `ai-approve diff` can move state to `DIFF_APPROVED`
- `ai-reject diff` can move state to `NEEDS_FIX`
- `ai-review final` can move state to `WAITING_HUMAN_FINAL_APPROVAL`
- `ai-approve final` can move state to `DONE` only after meaningful `.ai/verification.md` evidence exists
- `ai-reject final` can move state to `NEEDS_MORE_TESTS`
- `ai-dispatch` does not advance state
- `ai-context-pack` does not advance state
- `ai-handoff` does not advance state
- `state.json` is not a review database
- review text, approvals, logs, context packs, and traces stay in separate files
- Phase 8 adds no new state transitions

## Explicit Non-goals

Do not store the following inside `state.json`:

- review bodies
- approval histories
- command logs
- test logs
- subagent transcripts
- diff summaries
