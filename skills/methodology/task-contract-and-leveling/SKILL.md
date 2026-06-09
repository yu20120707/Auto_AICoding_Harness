---
name: task-contract-and-leveling
description: Use when classifying task risk, execution level, scope, verification, human gates, and blockers before implementation.
source: project
upstream: Auto_AICoding_Harness AGENTS.md task model; addyosmani/agent-skills planning-and-task-breakdown
license: project-local
adaptation_notes: Expanded into a fuller harness-native leveling workflow; preserves repository task-contract semantics instead of generic planning advice.
---

# Task Contract And Leveling

## Purpose

Turn a request into an explicit execution contract before implementation.

The contract prevents three recurring failures:

- solving the wrong problem
- using too little process for a risky task
- reporting completion without matching the agreed scope

## Use When

Use before any non-trivial implementation, refactor, or review-driven fix.

Use it especially when:

- impact surface is unclear
- more than one subsystem may be touched
- rollback could be annoying or risky
- review or approval gates may be needed
- the user asked for a direct execution level judgment

## Inputs

- user request
- repository `AGENTS.md`
- current branch and git status
- likely touched files or modules
- known risk areas
- available verification commands
- current `.ai/state.json` when present

## Process

### 1. Write the Task Contract

Before coding, state:

1. proposed execution level
2. target outcome
3. expected file or module scope
4. planned verification
5. known uncertainties or blockers

This is not ceremony.
It is the minimum information needed to keep work bounded and reviewable.

### 2. Classify by Risk, Not by Vibes

Use these signals in order:

1. impact surface
2. rollback cost
3. coordination cost
4. scope size

Impact surface asks what can break if the change is wrong:

- one local behavior
- one bounded workflow
- shared interface, shared data, or cross-system behavior

Rollback cost asks how hard it is to undo:

- easy in the same session
- possible but cleanup-heavy
- risky, slow, or externally visible

Coordination cost asks who else must stay aligned:

- single owner
- one bounded collaboration path
- multiple teams or streams

### 3. Choose the Level

#### Level 1

Use Level 1 when most of these are true:

- impact is local
- rollback is easy
- coordination is not needed
- file scope is narrow
- verification is quick and targeted

Typical examples:

- narrow bug fix
- prompt tweak
- single script adjustment
- local config update

#### Level 2

Use Level 2 when any of these are true:

- the task spans one meaningful workflow
- several implementation steps are needed
- scope could drift without a short plan
- rollback is possible but not trivial
- a review checkpoint would reduce risk

Typical examples:

- bounded feature work across several files
- staged bug fix with tests and validation
- local refactor with real regression risk

#### Level 3

Use Level 3 when any of these are true:

- shared APIs, schemas, or contracts are touched
- rollback is expensive
- security or production data paths are involved
- multiple contributors or substreams need coordination
- validation must go beyond a quick local check

Typical examples:

- architecture changes
- risky refactors
- migrations
- cross-service or contract-sensitive features

### 4. Apply Override Rules

At least Level 2 if the task touches:

- auth
- billing
- permissions
- security-sensitive flows
- production data paths
- migrations

Force Level 3 if it changes:

- public APIs
- shared schemas
- cross-service contracts
- shared libraries with multiple consumers

### 5. Define Verification Before Coding

For the chosen level, define what actually proves success:

- targeted unit tests
- integration checks
- script-based validation
- manual critical-path check
- documented "not run" with blocker and next action

If verification confidence does not match the chosen level, escalate the level or narrow the task.

### 6. Monitor for Escalation

Escalate during execution if:

- more modules are touched than expected
- rollback becomes harder than expected
- production safety or data correctness risk appears
- required testing becomes deeper than planned
- another contributor or subagent becomes necessary

Do not downgrade just because one coding step feels simple.

## Output

Return a task contract with:

- selected level
- outcome
- expected scope
- verification plan
- blockers or assumptions
- escalation triggers when relevant

## Do Not

- do not classify only by file count
- do not keep a risky task at Level 1 because the diff is short
- do not skip verification planning
- do not hide blockers that affect safety or correctness
- do not downgrade a task without a real reduction in risk or coordination
