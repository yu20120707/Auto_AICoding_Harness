# Subagent Packets

These files are large-mode task packet templates.
Use them when a task benefits from bounded role-specific work by a subagent, another local agent, or the main agent acting in that role.

Packets are not an execution system.
They do not start subagents, install skills, approve gates, or replace `.ai/state.json`.

## How To Use

1. Pick the role packet that matches the needed work.
2. Fill in the required context with exact files, docs, diffs, and constraints.
3. Give the packet to the worker agent or use it yourself as the role contract.
4. Write the returned evidence into `.ai/run-trace.md`, `.ai/reviews/`, `.ai/evaluation.md`, `.ai/context-pack.md`, or `.ai/handoff.md` as appropriate.

## Roles

- `planner.md`: scope, sequencing, gates, and verification strategy.
- `explorer.md`: read-only repository analysis and affected-file mapping.
- `implementer.md`: scoped edits only.
- `reviewer.md`: diff and regression review.
- `evaluator.md`: verification evidence and residual-risk check.

If subagents are unavailable, the main agent should follow these packet contracts sequentially.
