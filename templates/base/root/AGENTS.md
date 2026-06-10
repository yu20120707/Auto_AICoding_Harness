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
- `small` and `large` share one workflow model.
- `small` is suitable for direct or medium-complexity work without full planning gates.
- `large` is suitable for complex work that needs `spec`, `plan`, `diff`, and `final` gates.
- If a simple task fails twice or the impact expands, escalate the execution level.

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
