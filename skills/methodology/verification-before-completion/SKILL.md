---
name: verification-before-completion
description: Prevent false completion by requiring build, test, check, or documented not-run evidence before final claims.
source: adapted
upstream: obra/superpowers skills/verification-before-completion
license: see-upstream
adaptation_notes: Adapted to this harness verification/evaluation files and target project scripts; no external commands added.
---

# Verification Before Completion

## Purpose

Prevent false completion.

## Use When

Before claiming task complete, before final review, and after implementation.

## Inputs

`scripts/ai_check.sh`, `.ai/verification.md`, `.ai/evaluation.md`, and test output.

## Process

Run or document build / test / check steps, record evidence, note why anything was not run, and distinguish "tests passed" from "not run".
Use the freshest available command output for final claims.

## Output

Verification evidence with explicit pass, fail, or not run status.

## Do Not

Do not say tests passed if they were not run.
Do not omit failures.
Do not remove evidence.
