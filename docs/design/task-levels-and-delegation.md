# Task Levels And Delegation

## Core Principle

The main agent owns user intent, scope, state, delegation, approval, and final judgment.
Subagents own bounded analysis, bounded implementation, independent review, test design, and acceptance evidence.

## Levels

### Simple

Use simple mode when impact is local, rollback is easy, and verification is quick.

- main agent plans, edits, reviews, and verifies directly
- no required subagent
- no full `.ai/` planning gate
- if the same simple task fails twice, escalate

### Medium

Use medium mode when the task spans multiple files or one bounded workflow but does not require a full gate chain.

- main agent keeps ownership
- optional scanner or reviewer subagent
- short plan and run trace are enough
- no mandatory spec / plan / final approval gates
- escalate to complex if scope expands, rollback becomes hard, or validation becomes uncertain

### Complex

Use complex mode when the task changes architecture, shared contracts, high-risk workflows, or broad repository behavior.

- use large mode runtime artifacts
- require `spec`, `plan`, `diff`, and `final` gates when applicable
- use planner, explorer, implementer, reviewer, and evaluator roles when available
- store evidence in `.ai/run-trace.md`, `.ai/reviews/*`, `.ai/approvals/*`, and `.ai/evaluation.md`

## Multi-Agent vs State Machine

Multi-agent is an execution strategy.
State-machine documents are a risk-control strategy.

- simple usually uses neither
- medium may use subagents without full state-machine gates
- complex usually uses both

## Escalation Triggers

- the same simple task fails twice
- touched files or modules exceed the original scope
- the task affects public APIs, schemas, auth, permissions, data correctness, build systems, or deployment
- verification cannot be completed confidently
- a reviewer finds blocking design or regression risk

## Artifact Routing

- global behavior: global `AGENTS.md`
- project behavior: repository `AGENTS.md`
- project facts: `docs/ai/*`
- task runtime: `.ai/*`
- reusable method: `skills/*`
- one-time setup: `prompts/*`
