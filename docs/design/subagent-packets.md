# Subagent Task Packets

## Purpose

Subagent task packets are large-mode delegation artifacts.
They describe how the main agent should hand a bounded piece of work to a role-specific agent or to the same agent acting in that role.

They are not an execution framework.
They do not start subagents, install skills, advance gates, or replace `.ai/state.json`.

## Ownership

The main agent owns:

- user intent
- task level
- state transitions
- scope control
- final integration judgment
- final verification claims

The subagent or role worker owns only the bounded packet objective.
If the packet is unsafe, underspecified, or stale, the worker must stop and return the blocker instead of expanding scope.

## Packet Location

Large mode creates reusable packet templates under:

```text
.ai/subagent-packets/
```

These files are target-project runtime guidance.
They can be copied into a prompt, adapted by a local agent, or used manually when the platform supports subagents.

## Packet Fields

Every packet should include:

- `Role`
- `Required Skills`
- `Optional Skills`
- `Required Context`
- `Objective`
- `Forbidden Actions`
- `Expected Output`
- `Stop Conditions`
- `Return Format`

Skills are advisory routing hints.
They help Codex, Claude, Copilot, or another local agent choose the right local guidance, but absence of a skill must not block execution when the needed context is already present.

## Role Map

Recommended packet roles:

- `planner`: turns requirements into scope, sequencing, gates, and verification strategy
- `explorer`: reads code and evidence without editing
- `implementer`: makes scoped code or document changes
- `reviewer`: reviews diff, contracts, regressions, and missing tests
- `evaluator`: verifies results, commands, evidence, and residual risk

The same human-facing task can use no packet, one packet, or several packets.
Simple work should stay with the main agent.
Medium work may use one scanner or reviewer packet.
Large work may use several packets plus the normal gate artifacts.

## Context Passing

The packet must name the context it needs.
Typical context includes:

- user request
- task level and non-goals
- relevant `docs/ai/*`
- relevant `.ai/*` artifacts
- files or modules in scope
- expected verification command
- current git diff or touched files

Do not assume a subagent has implicit memory of the main conversation.
If the context matters, include it or point to the exact file.

## Output Routing

Packet output should be summarized into the existing large-mode artifacts:

- exploration notes into `.ai/affected-files.md` or `.ai/run-trace.md`
- review findings into `.ai/reviews/*`
- verification results into `.ai/evaluation.md`
- handoff-worthy conclusions into `.ai/context-pack.md` or `.ai/handoff.md`

The packet output is evidence.
It is not approval by itself.

## Non-goals

This protocol does not implement:

- automatic subagent execution
- subagent scheduling
- tool-specific adapter logic
- automatic skill installation
- review gate approval
- a second state machine
