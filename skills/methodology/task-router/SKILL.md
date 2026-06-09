---
name: task-router
description: Use before non-trivial coding tasks to choose simple, medium, or complex execution, decide when to delegate scanner/reviewer subagents, and decide when to upgrade to large-mode state artifacts.
source: project
upstream: Auto_AICoding_Harness task-level design; mutli-agent.txt user design notes; agentsmd/agents.md
license: project-local
adaptation_notes: Expanded into a fuller task-routing workflow for the harness; encodes complexity selection, delegation guidance, and large-mode triggers without adding a second state machine.
---

# Task Router

## Purpose

Choose the lightest workflow that still controls risk.

This skill separates two questions that are often confused:

1. how risky or broad is the task?
2. should subagents be used?

Subagents are optional acceleration.
Task level is about risk and control.

## Use When

Use before non-trivial edits, after repeated failure in a simple task, when touched files expand, or when the user asks whether the task should use simple, medium, or complex mode.

## Inputs

- user request
- repository `AGENTS.md`
- relevant `docs/ai/*`
- current `.ai/state.json` when present
- expected file scope
- risk areas
- available verification commands
- current branch and diff

## Process

### 1. Route by Risk First

Evaluate:

- impact surface
- rollback cost
- coordination cost
- verification depth

File count is only a weak signal.

### 2. Choose the Level

#### Simple

Use when:

- behavior is local
- rollback is easy
- one agent can hold the task cleanly
- verification is quick

Expected behavior:

- no full `.ai/` planning gate
- no mandatory subagent
- direct implementation with targeted check

#### Medium

Use when:

- several files or one bounded workflow are involved
- a short plan is useful
- scope could drift without checkpoints
- a scanner or reviewer subagent could help

Expected behavior:

- concise plan
- optional scanner or reviewer delegation
- no automatic requirement for full large-mode gate chain

#### Complex

Use when:

- architecture changes
- shared contracts or schemas change
- security-sensitive or production-sensitive behavior is touched
- rollback is expensive
- several review checkpoints are needed

Expected behavior:

- large-mode artifacts
- stronger planning and verification
- planner/explorer/implementer/reviewer/evaluator split when useful

### 3. Decide Whether To Upgrade to Large Mode

Upgrade to large mode when the task needs:

- spec / plan / diff / final gate artifacts
- long-lived task state across sessions
- explicit review and approval skeletons
- subagent packet templates

Do not force large mode for every multi-file task.

### 4. Decide Delegation Separately

Recommended delegation pattern:

- simple: none by default
- medium: scanner or reviewer
- complex: planner, explorer, implementer, reviewer, evaluator as needed

Subagent roles should have:

- disjoint purpose
- explicit context
- explicit stop conditions
- no ownership of final approval

### 5. Watch for Escalation Triggers

Escalate simple -> medium when:

- the same task fails twice
- touched scope expands
- verification becomes unclear

Escalate medium -> complex when:

- rollback becomes hard
- shared interfaces appear
- review gates are needed
- subagent packets or long-running artifacts become necessary

### 6. Record the Route

Before implementation, state:

- selected level
- target outcome
- expected scope
- delegation plan
- verification plan
- escalation triggers

This route is the working contract for the task.

## Output

Return:

- selected level
- reason for the level
- whether large mode is needed
- whether subagents are useful
- what each delegated role should own
- what verification must happen before completion

## Do Not

- do not equate multi-agent with complex mode
- do not create full state-machine artifacts for every medium task
- do not bypass review gates once complex mode is active
- do not let subagents own final user intent or final approval
- do not keep a high-risk task in a low-control mode because the diff is short
