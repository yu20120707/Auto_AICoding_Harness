# Systematic Debugging

## Purpose

Debug by reproduction, observation, root cause, minimal fix, and validation.

## Use When

Bug, failing test, crash, timeout, flaky behavior, or unclear runtime fault.

## Inputs

Error logs, test output, git diff, `docs/ai/linux-debug.md`, and `docs/ai/cpp-system.md`.

## Process

Reproduce the issue, inspect evidence, isolate the root cause, propose a minimal fix, and validate the result.

## Output

A root-cause-backed fix plan or a validated minimal code change.

## Do Not

Do not guess root cause without evidence.
Do not delete failing tests.
Do not hide unknowns.
