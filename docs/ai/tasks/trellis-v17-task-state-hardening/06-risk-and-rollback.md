# Risk And Rollback

## Primary Risks

- The task supplement becomes a competing state system instead of a large-mode supplement.
- Existing `ai-review`, `ai-approve`, or `ai-reject` gate ordering regresses.
- `ai-status` changes output in a way that breaks existing tests or user expectations.
- `small` or `medium` begins requiring task supplement files.
- Phase 1 expands into context manifest, RCA, check-rules, or template migration work.

## Compatibility Guardrails

- `.ai/state.json` remains canonical for existing command workflow state.
- `.ai/tasks/<task-id>/task.json` remains optional in Phase 1.
- `docs/ai/tasks/<task-id>/` remains the durable evidence chain.
- Public command names remain unchanged.
- Profile-specific build or test policy stays outside core state logic.

## Implementation Risk Result

- The task supplement is implemented as `core/task_state.py`, a focused helper module, not a replacement for `core/state.py` or `.ai/state.json`.
- `bin/ai-status` reads `.ai/tasks/<task-id>/task.json` only for initialized `large` state and only prints supplement lines when the file exists.
- `small` and `medium` initialization behavior remains unchanged; tests confirm they do not create `.ai/tasks` by default.
- The existing `ai-review`, `ai-approve`, and `ai-reject` chain remains unchanged; regression tests passed for spec, plan, diff, and final gates.
- Phase 2+ artifacts were not generated or consumed. `context.jsonl`, review-gate state files, RCA, check-rules, template hash, and migration remain future work.

## Rollback Plan

If Phase 1 implementation introduces regressions:

1. Revert `core/task_state.py`.
2. Revert the `bin/ai-status` import and supplement-summary block.
3. Revert `tests/test_task_state.py` if removing the capability entirely.
4. Remove or ignore `.ai/tasks/<task-id>/task.json` supplements.
5. Keep existing `.ai/state.json` and `docs/ai/tasks/<task-id>/` evidence chain intact.
6. Re-run:
   - `py -m compileall bin core`
   - `py tests/test_ai_state.py`
   - `py tests/test_ai_doctor.py`
   - `py tests/test_ai_upgrade_large.py`
   - `py tests/test_ai_review_spec_plan_final.py`
   - `py tests/test_ai_approve_reject_all_gates.py`
   - `py tests/test_ai_context_handoff.py`

## Residual Risk After Narrow Follow-up

- The consistency mapping is intentionally minimal. It prevents supplement status from contradicting canonical workflow gates, but it does not make the supplement drive gate transitions.
- `ai-status` remains non-failing for invalid supplements; it reports `task_supplement_valid: no` and a human-readable error so existing workflows are not blocked by optional metadata.
- The current workflow remains at `WAITING_HUMAN_DIFF_APPROVAL`; the corrected supplement status is `waiting_approval`.
- Narrow follow-up fix: supplement status is now validated against canonical `.ai/state.json::status`; a supplement cannot claim `completed` while the canonical workflow is still waiting for diff approval.
