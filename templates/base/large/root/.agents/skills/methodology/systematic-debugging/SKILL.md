---
name: systematic-debugging
description: Diagnose bugs through reproduction, evidence, root cause isolation, minimal fix, and validation.
source: adapted
upstream: obra/superpowers skills/systematic-debugging
license: see-upstream
adaptation_notes: Reduced to instruction-only debugging discipline; no Superpowers installer, marketplace, or subworkflow dependencies included.
---

# Systematic Debugging

## Purpose

Debug by reproduction, observation, root cause, minimal fix, and validation.

## Use When

Bug, failing test, crash, timeout, flaky behavior, or unclear runtime fault.

## Inputs

Error logs, test output, reproduction steps, current diff, `docs/ai/linux-debug.md`, and `docs/ai/cpp-system.md`.

## Process

Reproduce the issue, inspect evidence, isolate the root cause, propose a minimal fix, validate the result, and record remaining unknowns.
After repeated failed fix attempts, stop and reassess the model of the problem instead of guessing again.

## Output

A root-cause-backed fix plan or a validated minimal code change.

## Do Not

Do not guess root cause without evidence.
Do not delete failing tests.
Do not hide unknowns.
