# Usage Walkthrough

This is an executable operator guide for the current self-use harness baseline.

## Windows

```powershell
py bin/ai-status
py bin/ai-state
py bin/ai-init small
py bin/ai-init medium
py bin/ai-upgrade medium
py bin/ai-upgrade large
py bin/ai-doctor
py bin/ai-dispatch planner --scope "docs/design/*" --objective "plan bounded hardening" --expected-output "plan + risks" --result-location ".ai/run-trace.md"
py bin/ai-review spec
py bin/ai-approve spec
py bin/ai-review plan
py bin/ai-approve plan
```

After making real code changes and creating a git diff:

```powershell
py bin/ai-review diff
py bin/ai-approve diff
py bin/ai-context-pack
py bin/ai-handoff
py bin/ai-review final
py bin/ai-approve final
py bin/ai-status
```

## Unix-like

```bash
python3 bin/ai-status
python3 bin/ai-state
python3 bin/ai-init small
python3 bin/ai-init medium
python3 bin/ai-upgrade medium
python3 bin/ai-upgrade large
python3 bin/ai-doctor
python3 bin/ai-dispatch planner --scope "docs/design/*" --objective "plan bounded hardening" --expected-output "plan + risks" --result-location ".ai/run-trace.md"
python3 bin/ai-review spec
python3 bin/ai-approve spec
python3 bin/ai-review plan
python3 bin/ai-approve plan
```

After making real code changes and creating a git diff:

```bash
python3 bin/ai-review diff
python3 bin/ai-approve diff
python3 bin/ai-context-pack
python3 bin/ai-handoff
python3 bin/ai-review final
python3 bin/ai-approve final
python3 bin/ai-status
```

## Main Flow

1. Run `ai-status` before initialization to confirm the repository is `UNINITIALIZED`.
2. Run `ai-init small` for local low-risk work, or `ai-init medium` when the task is already multi-file but still bounded.
3. Run `ai-upgrade medium` when a `small` task grows into bounded multi-file work that needs plan / trace / verification artifacts.
4. Run `ai-upgrade large` when the task needs the full gate chain and richer `.ai/` scaffold.
5. Run `ai-status` or `ai-doctor` to confirm the mode transition was actually recorded in `.ai/state.json`.
6. In `medium`, keep `.ai/implementation-plan.md`, `.ai/run-trace.md`, and `.ai/verification.md` current while you work.
7. If real subagents will be used in `large`, run `ai-dispatch` first so `.ai/run-trace.md` records the role, explicit skills, scope, and expected output.
8. In `large`, fill or refine `.ai/spec.md`, then run `ai-review spec` and `ai-approve spec` or `ai-reject spec`.
9. In `large`, fill or refine `.ai/tech-design.md`, `.ai/implementation-plan.md`, and `.ai/risk-and-rollback.md`; the harness will also sync the corresponding `docs/ai/tasks/<task-id>/` files.
10. In `large`, run `ai-review plan` and `ai-approve plan` or `ai-reject plan`.
11. Make the actual code changes in the target repository.
12. Ensure the repository is a git repo and that a real working-tree diff exists.
13. Run `ai-review diff`, then `ai-approve diff` or `ai-reject diff`.
14. Record actual commands and outcomes in `.ai/verification.md`.
15. Run `ai-context-pack` to produce a compact resumable context summary.
16. Run `ai-handoff` to produce a continuation artifact for the next session.
17. When the task needs a formal close-out gate, run `ai-review final`, then `ai-approve final` or `ai-reject final`.
18. Run `ai-status` again to confirm the final state, task chain, and next action.
19. Run `ai-state` when another tool needs machine-readable JSON state.

## Important Notes

- `ai-review diff` requires a git repository and a real diff in the working tree.
- `ai-review spec` requires `.ai/spec.md`.
- `ai-review plan` requires `.ai/implementation-plan.md`.
- `ai-review final` requires at least one of `.ai/verification.md`, `.ai/evaluation.md`, `.ai/context-pack.md`, or `.ai/handoff.md`.
- `ai-approve final` requires `.ai/verification.md` to contain at least one real recorded command.
- `medium` does not require the full `spec -> plan -> diff -> final` gate chain.
- `ai-review plan` in `large` mode requires `spec` approval first.
- `ai-review diff` in `large` mode requires `plan` approval first.
- `ai-review final` in `large` mode requires `diff` approval first.
- `ai-dispatch` only works in large mode and only appends a standardized dispatch record to `.ai/run-trace.md`.
- `ai-approve` and `ai-reject` only work when the repository is already in the matching waiting-gate state.
- `ai-context-pack` and `ai-handoff` only generate transfer material. They do not advance state.
- `--force` always backs up the previous file under `.ai/backups/<timestamp>/` before overwrite.

## small Versus medium Versus large

- `small` is the lightest initialization mode and gives the base harness structure.
- `medium` adds a bounded plan / trace / verification scaffold without enabling the strict large-mode gate chain.
- `large` adds richer `.ai/` planning and review artifacts such as `spec.md`, `implementation-plan.md`, `reviews/`, and `approvals/`.
- `large` also maintains a task-scoped evidence chain under `docs/ai/tasks/<task-id>/`.
- `ai-dispatch` is intentionally large-only because it depends on `.ai/run-trace.md` and `.ai/subagent-packets/`.
- The rest of the command surface stays aligned across all three modes, but the richer `large` scaffold is what makes the full review chain practical.
