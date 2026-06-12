# Workflow

This document captures the durable AI collaboration workflow for the target project.
It complements `AGENTS.md` and the runtime files under `.ai/`.

## Mode Selection

- Use the lightest execution level that still controls risk.
- Stay in `small` for local, easy-to-verify work with low rollback cost.
- Upgrade to `medium` when the task becomes bounded multi-file work and should keep `.ai/implementation-plan.md`, `.ai/run-trace.md`, and `.ai/verification.md` current.
- Upgrade to `large` when the task needs explicit `spec`, `plan`, `diff`, and `final` gates.
- Escalate when touched scope expands, rollback gets harder, or verification depth increases.
- A mode change is only real after `ai-upgrade medium|large` succeeds and `.ai/state.json` reflects it.

## Command Protocol

- `ai-status`, `ai-state`, and `ai-doctor` are safe read-only commands.
- `ai-review spec|plan|diff|final` creates review artifacts and advances the state into the matching waiting gate.
- `ai-approve` and `ai-reject` require explicit human authorization and must match the current waiting gate.
- `ai-doctor` is the health check for state, generated files, and obvious mode mismatches.
- If a command was not executed successfully, do not describe its state transition as complete.

## Runtime Files

- `.ai/state.json`: authoritative workflow mode, status, current gate, and approved gates.
- `.ai/spec.md`: task goal, non-goals, allowed scope, and validation target.
- `.ai/tech-design.md`: technical design, data flow, and interface boundaries for large-mode work.
- `.ai/implementation-plan.md`: concrete execution steps and verification points.
- `.ai/affected-files.md`: expected edit surface before implementation drifts.
- `.ai/run-trace.md`: notable execution evidence and checkpoints during the task.
- `.ai/verification.md`: what was run, what passed, and what remains unverified.
- `.ai/risk-and-rollback.md`: residual risk, rollback path, and required follow-up.
- `.ai/evaluation.md`: final acceptance summary and residual risk.
- `.ai/context-pack.md`: compact resumable state for the next clean session.
- `.ai/handoff.md`: explicit transfer artifact when stopping or switching sessions.
- `docs/ai/tasks/<task-id>/`: durable large-mode evidence chain for PRD, spec, design, plan, review, verification, risk, and handoff.

## Verification Discipline

- Record real commands and outcomes in `.ai/verification.md`.
- Keep `.ai/evaluation.md` for the final acceptance conclusion, not raw command logs.
- Do not claim build, test, benchmark, or review coverage unless the evidence exists.
- If something was not run, write why it was skipped and what follow-up is required.

## Long-Running Work

- When the task becomes multi-step, keep `.ai/implementation-plan.md`, `.ai/run-trace.md`, and `.ai/verification.md` current.
- When a real subagent is dispatched, record the role, scope, required skills, optional skills, objective, and result location in `.ai/run-trace.md`.
- Use `.ai/context-pack.md` before ending a session that may resume soon.
- Use `.ai/handoff.md` when another agent or a later clean-context session needs to continue.
- If context is getting noisy or the scope is drifting, stop expanding the task and write down the next safe step.

## Durable Versus Runtime Knowledge

- Put project facts that outlive the task in `docs/ai/`.
- Put task-specific plans, evidence, and approvals in `.ai/`.
- Do not turn `.ai/` into long-lived architecture documentation.
