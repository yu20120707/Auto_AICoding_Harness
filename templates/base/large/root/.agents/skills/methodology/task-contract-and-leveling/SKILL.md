---
name: task-contract-and-leveling
description: Use when classifying task risk, execution level, scope, verification, human gates, and blockers before implementation.
source: self-authored
upstream: Auto_AICoding_Harness AGENTS.md
license: project-local
adaptation_notes: Encodes the harness Level 1/2/3 contract as a local skill without redefining the state machine.
---

# Task Contract And Leveling

## Purpose

Make task risk explicit before editing.

## Use When

Starting non-trivial work, touching multiple files, changing shared contracts, entering a human gate, or when rollback confidence is unclear.

## Inputs

`AGENTS.md`, user request, current git status, relevant docs, and known verification constraints.

## Process

Classify impact surface, rollback cost, coordination cost, and scope size.
State target outcome, expected file scope, verification, and uncertainties.
Escalate when the work touches shared interfaces, schemas, security-sensitive paths, or hard-to-revert behavior.
Stop at `WAITING_HUMAN_*` states and require explicit approve / reject commands.

## Output

A concise task contract with level, scope, risks, verification plan, and blockers.

## Do Not

Do not classify only by file count.
Do not hide architectural uncertainty.
Do not start broad edits before the task contract is clear.
Do not define a second state machine inside this skill.
