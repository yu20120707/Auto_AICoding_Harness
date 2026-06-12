# AGENTS.md

## Project Type

This repository uses `Auto_AICoding_harness` base workflow.

## Required Reading

Read `docs/ai/README.md` first.

For non-trivial tasks, also read the relevant `docs/ai/*` files for the area you are changing.
Read `docs/ai/workflow.md` before driving a multi-step or resumed task.

Always read active `.ai/` task files when they exist.

## Workflow

- Classify non-trivial tasks as simple, medium, or complex before editing.
- `small`, `medium`, and `large` share one workflow model with different control strengths.
- `small` is suitable for direct local work without full planning gates.
- `medium` is suitable for bounded multi-file work that should keep plan, run trace, and verification artifacts current.
- `large` is suitable for complex work that needs `spec`, `plan`, `diff`, and `final` gates.
- If a simple task fails twice or the impact expands, escalate the execution level.
- Apply `karpathy-guidelines` by default for planning, code changes, reviews, and refactors.
- In every mode, run a short requirement clarification pass before implementation: restate the target, scope, constraints, and verification plan.
- Unless the user explicitly says not to ask, do not silently choose between materially different implementations.
- If ambiguity remains after that clarification pass, ask targeted clarification questions when direction, scope, acceptance criteria, or risk boundaries are ambiguous, but avoid performative questioning that would not change the work.

## Harness Command Protocol

- The agent must not claim a mode or gate change unless the corresponding harness command completed successfully.
- Use `ai-status` or `ai-doctor` after meaningful workflow transitions when state evidence matters.
- Read-only commands the agent may run without extra approval: `ai-status`, `ai-state`, `ai-doctor`.
- Context commands the agent may run: `ai-context-pack`, `ai-handoff`.
- Workflow commands the agent may run after explaining intent: `ai-review spec|plan|diff|final`.
- Commands requiring explicit user approval: `ai-upgrade medium|large`, `ai-approve spec|plan|diff|final`, `ai-reject spec|plan|diff|final`.
- The agent must never approve its own work unless the user explicitly says the review passed and asks for the approval command.

## Knowledge Placement

- `AGENTS.md` is the thin project entrypoint.
- `docs/ai/*` stores durable project facts.
- `.ai/*` stores current task runtime, state, plans, verification, reviews, approvals, and handoff artifacts.
- Skills provide reusable methods when available, but they do not override this file.

## Safety

- do not overwrite existing files unless explicitly allowed
- do not treat `.ai/` as long-lived architecture knowledge
- do not bypass review gates or safe-write rules
- do not refactor unrelated code opportunistically
- do not describe a workflow transition as complete if `state.json` still says otherwise
