---
name: code-review-and-quality
description: Review a diff for correctness, regression risk, API/ABI impact, tests, edge cases, and maintainability.
source: adapted
upstream: addyosmani/agent-skills skills/code-review-and-quality
license: see-upstream
adaptation_notes: Condensed for harness diff review and human gate flow; style-only review and unrelated PR workflow guidance removed.
---

# Code Review And Quality

## Purpose

Find real defects and missing verification before human approval.

## Use When

Reviewing `git diff`, preparing `ai-review diff`, checking a completed implementation, or reviewing another agent's changes.

## Inputs

`git diff`, `.ai/spec.md`, `.ai/implementation-plan.md`, `.ai/affected-files.md`, `docs/ai/*`, and test output.

## Process

Check behavior against spec, inspect changed call paths, identify API/ABI or data compatibility risk, verify test coverage, and rank findings by severity.
Start with bugs, regressions, missing tests, and contract risks before style.

## Output

A review finding list with file references, severity, evidence, and required fixes.

## Do Not

Do not focus on style before correctness.
Do not approve missing tests without explanation.
Do not replace the human review gate.
