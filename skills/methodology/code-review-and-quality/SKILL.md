---
name: code-review-and-quality
description: Review a diff for correctness, regression risk, API/ABI impact, tests, edge cases, and maintainability.
source: adapted
upstream: addyosmani/agent-skills skills/code-review-and-quality
license: MIT
adaptation_notes: Expanded into a fuller review workflow for harness use, with emphasis on actionable findings, review artifact generation, and repository verification expectations.
---

# Code Review And Quality

## Purpose

Review a change across multiple axes before it is treated as safe to merge or approve.

The goal is not perfection.
The goal is to catch real defects, regressions, contract drift, and missing verification before they become someone else's incident.

## Use When

Use when:

- reviewing your own diff before completion
- reviewing another agent's or human's change
- preparing `.ai/reviews/*`
- checking whether a fix actually matches the request
- validating a refactor for regression risk

## Inputs

- current diff
- changed files
- task request or spec
- relevant `docs/ai/*`
- related tests
- verification output
- public headers, schemas, or interfaces when applicable

## Process

### 1. Understand the Intended Change

Before judging code, understand:

- what the change claims to do
- what behavior should change
- what behavior must not change
- what files are central versus incidental

If intent is unclear, surface that first.

### 2. Review Tests Before Implementation

Tests often reveal intent better than the implementation does.

Check:

- do tests exist for changed behavior?
- do they test behavior rather than implementation details?
- are failure paths and edge cases covered?
- would these tests catch a regression?

### 3. Review Across the Main Axes

#### Correctness

- does the code actually satisfy the request?
- are edge cases handled?
- are error paths consistent?
- are state transitions valid?
- are assumptions about ordering, nullability, or timing safe?

#### Readability And Simplicity

- are names descriptive?
- is control flow easy to follow?
- did the change introduce cleverness without payoff?
- are abstractions earning their complexity?

#### Architecture And Boundaries

- does the change fit existing patterns?
- does it respect module boundaries?
- does it create coupling or duplication?
- should a shared contract update have happened but did not?

#### Security

- is untrusted input validated?
- are secrets or tokens exposed?
- are permission checks present where required?
- do filesystem, subprocess, or network changes raise risk?

#### Performance And Operations

- did the change add unbounded work, repeated IO, or expensive hot-path logic?
- are retries, timeouts, or batching still sane?
- is observability preserved?

### 4. Check API And ABI Risk Explicitly

For C++ / system work, review:

- public header changes
- serialization changes
- protocol changes
- config or state format changes
- shared library or consumer impact

This is where API/ABI drift must be named explicitly.

### 5. Review Change Size And Scope

Large diffs are not automatically wrong, but they raise review risk.

Ask:

- is this really one logical change?
- did implementation and refactor get bundled together?
- should this have been split for safer review?

### 6. Categorize Findings

A review finding should be actionable and severity-aware.

Use these categories:

- `critical`: blocks merge or approval
- `required`: must be addressed
- `suggestion`: improvement worth considering
- `fyi`: context only

Each review finding should include:

- what is wrong
- why it matters
- where it is
- what kind of fix is likely needed

### 7. Verify the Verification Story

Check not only code, but proof:

- what commands were run?
- did the reported output match the claim?
- are there missing tests?
- was anything left as "not run"?

If verification is weak, that is itself a review issue.

## Review Output Format

Preferred structure:

```text
findings:
- [severity] file: reason

open_questions:
- ...

verification_gaps:
- ...

change_summary:
- ...
```

## Red Flags

- approval with no tests or checks reviewed
- comments about style while missing correctness issues
- vague criticism with no file reference or consequence
- ignoring API/ABI drift in shared C++ code
- treating missing verification as acceptable by default

## Output

Produce a review note with:

- ordered findings
- review finding severity
- file references when available
- open questions or assumptions
- verification gaps
- brief summary only after findings

## Do Not

- do not lead with praise and bury defects
- do not block a change because it differs from personal taste alone
- do not ignore regression risk because tests happen to pass
- do not approve a contract-sensitive change without checking its consumers
