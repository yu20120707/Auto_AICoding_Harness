---
name: karpathy-guidelines
description: Use when writing, reviewing, or refactoring code to keep changes simple, scoped, assumption-aware, and verified.
source: adapted
upstream: forrestchang/andrej-karpathy-skills
license: MIT
adaptation_notes: Condensed for Auto_AICoding_Harness as a local project-level template; no scripts or installer logic included.
---

# Karpathy Guidelines

## Purpose

Reduce common AI coding failure modes: overengineering, broad edits, hidden assumptions, and false completion.

## Use When

Use for any implementation, refactor, debugging pass, review, or code-facing plan.

## Inputs

User request, `AGENTS.md`, current git status, relevant source files, current diff, and verification output.

## Process

Think before coding: surface assumptions, ambiguity, and tradeoffs before editing.
Keep the solution simple: add only what the request and codebase require.
Make surgical changes: touch the smallest responsible file scope and preserve unrelated user changes.
Verify before claiming completion: run or document the check that proves the claim.

## Output

A scoped implementation or review with explicit assumptions, changed files, verification evidence, and residual risk when relevant.

## Do Not

Do not add speculative abstractions.
Do not refactor unrelated code.
Do not hide uncertainty.
Do not claim tests passed without fresh evidence.
