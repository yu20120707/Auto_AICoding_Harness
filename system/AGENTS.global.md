# System Global AGENTS

## Purpose

This is the system-layer global behavior contract for `Auto_AICoding_Harness`.
It is repository-owned and intentionally portable across local AI coding tools.

## Priority

Follow instructions in this order:

1. Platform and system safety rules
2. The user's current explicit request
3. The current repository `AGENTS.md`
4. The current repository `docs/ai/*`
5. This system global contract
6. Skills and reusable prompts

When safety rules conflict, follow the stricter rule.

## Default Behavior

- Read the current repository `AGENTS.md` before changing code.
- Read `docs/ai/README.md` and the relevant `docs/ai/*` files when repository facts matter.
- Keep repository-specific facts out of this global file.
- Classify non-trivial work as simple, medium, or complex before editing.
- Apply `karpathy-guidelines` by default for planning, implementation, review, and refactor work.
- In every mode, run a short requirement clarification pass before implementation: restate the target, scope, constraints, and verification plan.
- Unless the user explicitly says not to ask, do not silently choose between materially different implementations.
- If ambiguity remains after that clarification pass, ask targeted clarification questions only when they can change scope, implementation, or verification.
- Keep edits narrow, reversible, and verified.
- Do not overwrite user work or use destructive git commands unless explicitly requested.
- If a simple task fails twice or the impact expands, escalate to medium or complex mode.

## Command Protocol

- A mode or gate change is real only after the matching harness command succeeds and `.ai/state.json` reflects it.
- `ai-status`, `ai-state`, and `ai-doctor` are read-only status commands.
- `ai-context-pack` and `ai-handoff` are artifact-generation commands.
- `ai-review` enters a review gate and should be explained before it runs.
- `ai-upgrade`, `ai-approve`, `ai-reject`, and `ai-install-skills` require explicit user approval.
- The agent must never approve its own work unless the user explicitly says the review passed and asks for the approval command.

## Mode Defaults

- Simple: main agent executes directly and verifies locally.
- Medium: main agent may delegate scanner or reviewer roles, but does not require the full large-mode gate chain.
- Complex: use project runtime state, planning artifacts, review gates, and bounded subagents when available.
