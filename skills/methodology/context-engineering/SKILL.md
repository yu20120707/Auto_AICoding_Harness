---
name: context-engineering
description: Select the smallest useful repo context for a task, including relevant docs, source paths, diffs, and prior artifacts.
source: adapted
upstream: addyosmani/agent-skills skills/context-engineering
license: see-upstream
adaptation_notes: Condensed to the harness context model and safe for repository-owned global use; no external integrations included.
---

# Context Engineering

## Purpose

Load enough context to be correct without flooding the agent with unrelated files.

## Use When

Starting exploration, resuming a task, preparing a handoff, narrowing an unfamiliar code path, or handing work to a subagent.

## Inputs

`AGENTS.md`, `docs/ai/*`, `.ai/context-pack.md`, `.ai/handoff.md`, `git status`, `git diff`, `rg` results, and relevant source paths.

## Process

Identify the question, list likely files, read entrypoints first, follow call chains, keep evidence paths, and stop when the remaining unknowns are explicit.
Prefer `rg`, current git status, and targeted source reads over broad repository scans.

## Output

A compact context set with file paths, decisions, risks, and open questions.

## Do Not

Do not read the whole repository by default.
Do not ignore current git status.
Do not invent behavior without source evidence.
