# Current Capabilities

## Version Baseline

`v1.7-optimization-hardening`

## Supported Commands

- `ai-install-skills`
- `ai-init small`
- `ai-init medium`
- `ai-upgrade medium`
- `ai-upgrade large`
- `ai-doctor`
- `ai-status`
- `ai-state`
- `ai-dispatch`
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

## Phase 16 Scope

- keeps the Phase 8 release baseline and workflow behavior
- keeps optional subagent role templates for large mode
- keeps the consolidated provenance-aware skill set
- keeps skills in repository-level `skills/` as portable skill sources
- keeps `ai-install-skills` as a Codex example installer into `$CODEX_HOME/skills` or `~/.codex/skills`
- supports `ai-install-skills --dry-run` for install inspection without writes
- supports `ai-install-skills --list` for manifest inspection without writes
- supports `ai-install-skills --scope` and `--profile` for subset selection
- supports `--force` install refresh with backup under `skill-backups/<timestamp>/`
- records installed skill metadata in an installed-skills manifest outside target projects
- keeps `skill-creator` for maintaining `skills/**/SKILL.md`
- keeps a single Chinese `README.md`
- adds `global/AGENTS.md.template` for user-level behavior guidance
- adds `system/AGENTS.global.md` as the system-layer global behavior source
- adds `prompts/bootstrap-local-agent.md` for local-agent self-install guidance
- adds `docs/install-targets.md`
- adds `docs/design/platform-adapters.md`
- adds `docs/design/task-levels-and-delegation.md`
- adds `docs/design/subagent-packets.md`
- adds `repo-onboarding-analysis` and `task-router` skills
- adapts selected upstream skill ideas from karpathy-guidelines, obra/superpowers, addyosmani/agent-skills, and getsentry/skills
- keeps local C++ / Linux / backend / system guidance in one profile-oriented skill
- maps large-mode subagent roles to recommended global skills
- adds large-mode `.ai/subagent-packets/` templates for role-specific context passing
- adds large-mode `.ai/verification.md` as a dedicated verification evidence ledger
- adds generated `docs/ai/workflow.md` as a durable execution contract for target projects
- adds `ai-dispatch` as a thin helper that expands role-to-skill mapping into `.ai/run-trace.md`
- uses `.ai/run-trace.md` as the canonical dispatch log when large-mode subagents are actually used
- requires explicit role-to-skill mapping in that dispatch log when real subagents are used
- keeps subagents as enhancement templates, not execution logic
- keeps subagent task packets as prompt/context artifacts, not an automatic runner
- small mode does not depend on subagents
- small mode does not depend on skills at command runtime
- If subagents are unavailable, the main agent should follow the same role contracts sequentially
- If skills are not installed, the main agent should rely on `AGENTS.md` and `docs/ai/*` directly
- does not automatically install skills or global instructions during `git clone`
- does not fetch third-party skills during installation
- supports `ai-state` as a thin machine-readable state output
- supports `ai-doctor` as a consistency check for state and generated medium/large-mode files
- makes `ai-status` show next-action guidance
- supports `medium` as a bounded execution level between `small` and `large`
- lets `ai-init medium` create a lightweight plan / trace / verification scaffold without entering the full large gate chain
- makes `ai-upgrade large` print transition evidence and the next recommended step
- syncs large-mode evidence into `docs/ai/tasks/<task-id>/` so the task chain is durable outside runtime-only files
- enforces the `spec -> plan -> diff -> final` review chain in `large` mode
- adds `core/command_policy.py` as the code-level command permission contract
- adds `core/profile.py`, `profiles/<name>/profile.yaml`, and `schemas/profile.schema.json` so profile selection is validated instead of remaining prose-only

## Phase 17 Scope

- closes the P0-P4 optimization roadmap
- removes stale local skill directory ambiguity through tests
- documents `scripts/` as non-command implementation space
- adds `ai-install-skills --dry-run`
- adds `ai-state`
- adds committed small and large examples
- adds the C++ / Linux profile verification matrix
- keeps subagent execution, third-party skill fetching, and multi-profile marketplace out of scope

## Supported Workflow

```text
ai-install-skills
  -> installs a manifest-selected subset into Codex as an example installer
  -> can run with --dry-run or --list before writing files

ai-init small
  -> ai-upgrade medium
  -> ai-upgrade large
  -> ai-status / ai-doctor

ai-init medium
  -> ai-status / ai-doctor
  -> ai-review diff
  -> ai-approve diff / ai-reject diff
  -> ai-context-pack
  -> ai-handoff

ai-init small|medium
  -> ai-upgrade large
  -> ai-status / ai-doctor
  -> ai-dispatch <role> --scope ... --objective ... --expected-output ... --result-location ...
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
- `ai-approve final` can move state to `DONE` after review material exists and `.ai/verification.md` contains recorded command evidence
- `ai-reject final` can move state to `NEEDS_MORE_TESTS`
- `ai-review plan` in `large` mode requires `spec` approval first
- `ai-review diff` in `large` mode requires `plan` approval first
- `ai-review final` in `large` mode requires `diff` approval first
- `medium` keeps the same state shape but does not enforce the large-mode gate ordering
- `ai-dispatch` appends to `.ai/run-trace.md` and does not advance state
- `ai-context-pack` does not advance state
- `ai-handoff` does not advance state
- `ai-state` reads state and does not advance state
- `ai-doctor` reads state and generated files and does not advance state

## Explicitly Not Implemented

- subagent execution
- automatic third-party skill fetching
- multi-profile marketplace
- heavy platform adapter framework

## Dependency Policy

No third-party runtime dependencies.

## Test Coverage

- `tests/test_ai_init_small.py`: small-mode init, default skip behavior, `--force` backup, `ai-status`, exit codes
- `tests/test_ai_init_medium.py`: medium-mode init, state shape, medium scaffold, and status guidance
- `tests/test_ai_state.py`: machine-readable initialized and uninitialized state output plus argument errors
- `tests/test_ai_upgrade_medium.py`: small-to-medium and medium-to-large upgrade paths plus repeated-upgrade behavior
- `tests/test_ai_upgrade_large.py`: small-to-large upgrade, repeated upgrade behavior, `--force` backup, large-mode status
- `tests/test_e2e_workflow.py`: full mainline workflow from `UNINITIALIZED` to `DONE`, including large task-chain artifacts
- `tests/test_ai_review_medium.py`: medium-mode `plan` and `final` review behavior without a large-mode `spec` prerequisite
- `tests/test_ai_review_diff.py`: diff review preconditions, git requirements, review artifact generation, state transition to `WAITING_HUMAN_DIFF_APPROVAL`
- `tests/test_ai_review_spec_plan_final.py`: spec/plan/final review artifact generation, waiting-gate transitions, skip and `--force` behavior, and `ai-status` visibility
- `tests/test_examples.py`: committed example structure including workflow guidance and large-mode verification scaffold
- `tests/test_ai_approve_reject_diff.py`: diff approve/reject preconditions, state transitions to `DIFF_APPROVED` and `NEEDS_FIX`, skip and `--force` behavior
- `tests/test_ai_approve_reject_all_gates.py`: spec/plan/final/diff approve-reject coverage, gate mismatch failures, missing review failures, skip and `--force` behavior, and final state visibility
- `tests/test_ai_context_handoff.py`: context-pack and handoff generation, no state advancement, review/approval visibility, skip and `--force` behavior
- `tests/test_ai_dispatch.py`: large-mode dispatch logging, packet skill expansion, and mode/precondition failures
- `tests/test_ai_doctor.py`: doctor diagnostics for missing state, medium acceptance, incomplete large scaffolds, mode mismatch, and JSON output
- `tests/test_current_capabilities.py`: command entrypoint manifest, README support surface, explicit capability declarations, and current baseline markers
- `tests/test_safe_write.py`: path safety, overwrite manifest, and symlink-escape hardening
- `tests/test_state_machine.py`: state validation, waiting-gate enforcement, medium permissiveness, and large-mode gate ordering
- `tests/test_cpp_profile_templates.py`: profile overlay docs generation, keyword coverage, and safe placeholder script content
- `tests/test_examples.py`: committed small and large example structure without runtime noise
- `tests/test_subagent_templates.py`: large-mode subagent role template generation, keyword coverage, and safe-write behavior
- `tests/test_skill_templates.py`: portable skill source validation, install behavior, backup behavior, provenance coverage, onboarding/routing skills, subagent routing guidance, and keyword coverage
