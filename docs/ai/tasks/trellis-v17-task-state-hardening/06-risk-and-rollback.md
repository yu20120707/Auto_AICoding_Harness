# Risk And Rollback

## Primary Risks

- The task supplement becomes a competing state system instead of a large-mode supplement.
- Existing `ai-review`, `ai-approve`, or `ai-reject` gate ordering regresses.
- `ai-status` changes output in a way that breaks existing tests or user expectations.
- `small` or `medium` begins requiring task supplement files.
- Phase 1 expands into context manifest, RCA, check-rules, or template migration work.
- Local tool runtime directories such as `.codegraph/` or `.reasonix/` are accidentally committed.

## Compatibility Guardrails

- `.ai/state.json` remains canonical for existing command workflow state.
- `.ai/tasks/<task-id>/task.json` remains optional in Phase 1.
- `docs/ai/tasks/<task-id>/` remains the durable evidence chain.
- Public command names remain unchanged.
- Profile-specific build or test policy stays outside core state logic.
- Root local runtime directories are ignored and should not become product structure.

## Follow-up Risk Result

- Phase 2-5 code paths are being removed from the current intended diff after subagent review found scope expansion.
- `.codegraph/` and `.reasonix/` artifacts are deleted from versioned content and ignored going forward.
- `core/safe_write.py` now rejects parent path segments before allowlist checks, closing the in-repo allowlist bypass.
- Existing command files have been restored to pre-expansion behavior, preserving the current public command surface.

## Rollback Plan

If this follow-up introduces regressions:

1. Revert the `core/safe_write.py` and `tests/test_safe_write.py` changes.
2. Re-evaluate whether the `.gitignore` additions should stay; they are expected to stay because `.codegraph/` and `.reasonix/` are local runtime directories.
3. Restore any accidentally removed Phase 1 files only if verification proves they are required.
4. Do not restore Phase 2-5 modules unless a separate Phase 2-5 gate explicitly approves them.
5. Re-run the follow-up verification batch listed in `.ai/verification.md`.

## Residual Risk

- The branch history still contains the earlier broad commit; this follow-up corrects the working tree and should be reviewed as a cleanup/fix commit.
- Some local `.codegraph` database files may remain on disk if another process holds them open, but they are ignored and not tracked.
