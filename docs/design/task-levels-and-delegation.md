# Task Levels And Delegation

## Core Principle

The main agent owns user intent, scope, state, delegation, approval, and final judgment.
Subagents own bounded analysis, bounded implementation, independent review, test design, and acceptance evidence.

Across simple, medium, and complex alike, the agent should begin with a requirement clarification pass:

- restate target outcome
- restate expected scope
- restate key constraints
- restate verification intent

If the task is still ambiguous after that pass, and the user did not explicitly say not to ask questions, ask targeted clarification questions before implementation.

## Levels

### Simple

Use simple mode when impact is local, rollback is easy, and verification is quick.

- main agent plans, edits, reviews, and verifies directly
- still begins with the same requirement clarification pass
- no required subagent
- no full `.ai/` planning gate
- if the same simple task fails twice, escalate

### Medium

Use medium mode when the task spans multiple files or one bounded workflow but does not require a full gate chain.

- main agent keeps ownership
- still begins with the same requirement clarification pass
- optional scanner or reviewer subagent
- short plan and run trace are enough
- no mandatory spec / plan / final approval gates
- the built-in `ai-dispatch` helper remains `large`-only because role packets are only generated in the large scaffold
- escalate to complex if scope expands, rollback becomes hard, or validation becomes uncertain

### Complex

Use complex mode when the task changes architecture, shared contracts, high-risk workflows, or broad repository behavior.

- use large mode runtime artifacts
- still begins with the same requirement clarification pass
- require `spec`, `plan`, `diff`, and `final` gates when applicable
- use planner, explorer, implementer, reviewer, and evaluator roles when available
- store evidence in `.ai/run-trace.md`, `.ai/reviews/*`, `.ai/approvals/*`, and `.ai/evaluation.md`
- if a real subagent is dispatched, record its role, scope, required skills, optional skills, objective, and result location in `.ai/run-trace.md`

## Multi-Agent vs State Machine

Multi-agent is an execution strategy.
State-machine documents are a risk-control strategy.

- simple usually uses neither
- medium may use subagents without full state-machine gates, but may need manual coordination instead of the built-in dispatch helper
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
