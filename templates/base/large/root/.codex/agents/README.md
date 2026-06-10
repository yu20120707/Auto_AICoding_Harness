# Agents

These files are role templates for optional large-mode subagent workflows.

- They are optional enhancement templates.
- They are not required for small mode.
- They do not execute anything by themselves.
- Any real subagent dispatch should copy the role's skill guidance explicitly into the dispatch request.
- Any real subagent dispatch should be recorded in `.ai/run-trace.md`.
- If the environment does not support subagents, the main Codex agent should follow the same role contracts sequentially.
- Human review gates remain authoritative.

Current role templates:

- `planner.md`
- `explorer.md`
- `implementer.md`
- `reviewer.md`
- `evaluator.md`
