# Current Capabilities

## Version Baseline

`v1.0-phase10`

## Supported Commands

- `ai-init small`
- `ai-upgrade large`
- `ai-status`
- `ai-review diff`
- `ai-review spec`
- `ai-review plan`
- `ai-review final`
- `ai-approve spec`
- `ai-approve plan`
- `ai-approve diff`
- `ai-approve final`
- `ai-reject spec`
- `ai-reject plan`
- `ai-reject diff`
- `ai-reject final`
- `ai-context-pack`
- `ai-handoff`

## Phase 10 Scope

- keeps the Phase 8 release baseline and workflow behavior
- keeps optional subagent role templates for large mode
- adds optional local skills templates for large mode
- keeps subagents as enhancement templates, not execution logic
- keeps skills as local project-level enhancement templates, not installation logic
- No new CLI commands

## Supported Workflow

```text
ai-init small
  -> ai-upgrade large
  -> ai-review spec
  -> ai-approve spec / ai-reject spec
  -> ai-review plan
  -> ai-approve plan / ai-reject plan
  -> ai-review diff
  -> ai-approve diff / ai-reject diff
  -> ai-review final
  -> ai-approve final / ai-reject final
  -> ai-context-pack
  -> ai-handoff
```

## State Behavior

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
- `ai-approve final` can move state to `DONE`
- `ai-reject final` can move state to `NEEDS_MORE_TESTS`
- `ai-context-pack` does not advance state
- `ai-handoff` does not advance state

## Explicitly Not Implemented

- subagent execution
- skills installation
- automatic third-party skill fetching
- multi-profile marketplace

## Dependency Policy

No third-party runtime dependencies.

## Test Coverage

- `tests/test_ai_init_small.py`: small-mode init, default skip behavior, `--force` backup, `ai-status`, exit codes
- `tests/test_ai_upgrade_large.py`: small-to-large upgrade, repeated upgrade behavior, `--force` backup, large-mode status
- `tests/test_ai_review_diff.py`: diff review preconditions, git requirements, review artifact generation, state transition to `WAITING_HUMAN_DIFF_APPROVAL`
- `tests/test_ai_review_spec_plan_final.py`: spec/plan/final review artifact generation, waiting-gate transitions, skip and `--force` behavior, and `ai-status` visibility
- `tests/test_ai_approve_reject_diff.py`: diff approve/reject preconditions, state transitions to `DIFF_APPROVED` and `NEEDS_FIX`, skip and `--force` behavior
- `tests/test_ai_approve_reject_all_gates.py`: spec/plan/final/diff approve-reject coverage, gate mismatch failures, missing review failures, skip and `--force` behavior, and final state visibility
- `tests/test_ai_context_handoff.py`: context-pack and handoff generation, no state advancement, review/approval visibility, skip and `--force` behavior
- `tests/test_current_capabilities.py`: command entrypoint manifest, README support surface, explicit capability declarations, and current baseline markers
- `tests/test_cpp_profile_templates.py`: profile overlay docs generation, keyword coverage, and safe placeholder script content
- `tests/test_e2e_workflow.py`: full mainline workflow from `UNINITIALIZED` to `DONE`
- `tests/test_subagent_templates.py`: large-mode subagent role template generation, keyword coverage, and safe-write behavior
- `tests/test_skill_templates.py`: large-mode local skills template generation, keyword coverage, and safe-write behavior
