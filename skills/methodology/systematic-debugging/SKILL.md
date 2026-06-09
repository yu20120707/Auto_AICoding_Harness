---
name: systematic-debugging
description: Diagnose bugs through reproduction, evidence, root cause isolation, minimal fix, and validation.
source: adapted
upstream: obra/superpowers skills/systematic-debugging
license: MIT
adaptation_notes: Expanded for harness-driven debugging, `.ai/*` evidence capture, and repository-safe workflows; no superpowers-specific command wrappers included.
---

# Systematic Debugging

## Purpose

Diagnose bugs through reproduction, evidence, root cause isolation, minimal fix, and validation.

Random fixes waste time, mask the real problem, and often create new bugs.
This skill exists to force root-cause-first debugging.

## Use When

Use for any technical issue:

- test failures
- unexpected behavior
- build failures
- integration issues
- performance regressions
- repeated implementation failures

Use it especially when:

- the fix seems "obvious"
- you are under time pressure
- more than one attempted fix has already failed
- the issue crosses multiple components

## Inputs

- failing command output
- stack traces and logs
- recent git diff or suspect commits
- relevant source files and tests
- environment or config differences
- `.ai/run-trace.md` or `.ai/affected-files.md` when present

## Process

### 1. Follow the Iron Law

```text
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you have not explained why the bug happens, you are not ready to implement a fix.

### 2. Reproduce Reliably

Before changing code:

- can you trigger it consistently?
- what exact steps reproduce it?
- what command, input, or environment causes it?
- does it always fail the same way?

If reproduction is not stable, gather more data instead of guessing.

### 3. Read the Error, Not Your Assumption

Carefully inspect:

- error messages
- stack traces
- failing assertions
- line numbers
- file paths
- exit codes

Do not skip straight to editing because the first line "looks familiar".

### 4. Check What Changed

Investigate recent changes:

- current diff
- recent commits
- config changes
- dependency changes
- environment differences

Many bugs are change-introduced, not system-mysteries.

### 5. Gather Evidence Across Boundaries

When several components are involved, instrument the handoff points:

- caller -> callee
- API -> service
- service -> database
- workflow -> script
- parser -> business logic

At each boundary, log or inspect:

- input shape
- output shape
- environment/config presence
- error propagation

This shows where the system stops behaving as expected.

### 6. Trace Data Flow Backward

When the failure appears deep in the stack:

- find the bad value or bad state
- ask where it came from
- trace back through callers until the origin is clear

Fix at the source, not at the last place that notices the problem.

### 7. Compare Against a Known-Good Pattern

Look for:

- similar working code
- established local pattern
- expected interface contract
- documented behavior

List concrete differences between working and broken cases.
Small differences often matter.

### 8. Form One Hypothesis at a Time

Write a specific statement:

```text
I think X is the root cause because Y.
```

Then test the smallest change or diagnostic that proves or disproves it.

Do not stack several speculative fixes together.

### 9. Implement the Minimal Fix

Once root cause is established:

- create or identify the failing reproduction
- implement one focused fix
- rerun the failing check
- rerun adjacent regression checks

If the attempted fix fails, return to investigation instead of piling on more patches.

### 10. Escalate After Repeated Failed Fixes

If two or three fixes fail:

- stop assuming this is a local defect
- question the architecture, contract, or environment model
- write down what evidence now contradicts the earlier hypothesis

Repeated failed fixes often mean the diagnosis, not the code, was wrong.

## Debugging Output Template

Use a structure like:

```text
symptom:
reproduction:
evidence:
root_cause_hypothesis:
tested_change:
result:
next_step:
```

## Red Flags

- "quick fix for now"
- "just try this and see"
- changing several things before rerunning the failing check
- no consistent reproduction
- no explanation of why the bug occurs
- jumping to refactor before isolating the failure

## Output

Produce:

- a root-cause-based explanation
- the smallest responsible fix or next experiment
- verification evidence
- residual unknowns if any remain

## Do Not

- do not patch symptoms without explaining the cause
- do not mix multiple hypotheses into one edit
- do not trust intuition over fresh evidence
- do not claim a bug is fixed without rerunning the failing scenario
