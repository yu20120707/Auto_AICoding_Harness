---
name: task-router
description: Use before non-trivial coding tasks to choose simple, medium, or complex execution, decide when to delegate scanner/reviewer subagents, and decide when to upgrade to large-mode state artifacts.
source: project
upstream: Auto_AICoding_Harness task-level design; mutli-agent.txt user design notes; agentsmd/agents.md
license: project-local
adaptation_notes: Encodes the harness task-level routing model without adding a second state machine or platform-specific automation.
---

# Task Router

## Purpose

Choose the lightest workflow that still controls risk.
Separate task complexity from whether subagents are available.

## Use When

Use before non-trivial edits, after repeated failure in a simple task, when touched files expand, or when a user asks whether a task should use simple, medium, or complex mode.

## Inputs

User request, repository `AGENTS.md`, relevant `docs/ai/*`, current `.ai/state.json` when present, expected file scope, risk areas, and available verification commands.

## Process

1. Classify impact, rollback cost, coordination cost, and verification depth.
2. Choose simple when the change is local, easy to revert, and quick to verify.
3. Choose medium when the task spans multiple files or one bounded workflow but does not need full spec/plan/final gates.
4. Choose complex when the task changes architecture, shared contracts, state semantics, security-sensitive paths, or broad behavior.
5. Escalate simple to medium if the same task fails twice or the touched scope expands.
6. Escalate medium to complex if rollback becomes hard, review gates are needed, or validation confidence drops.
7. Decide subagent use separately:
   - simple: none by default
   - medium: scanner or reviewer
   - complex: planner, explorer, implementer, reviewer, evaluator as needed

## Output

State:

- selected level
- target outcome
- expected file scope
- delegation plan
- verification plan
- escalation triggers

## Do Not

Do not equate multi-agent with complex mode.
Do not create full state-machine artifacts for every medium task.
Do not bypass review gates once complex mode is active.
Do not let subagents own final user intent or final approval.
