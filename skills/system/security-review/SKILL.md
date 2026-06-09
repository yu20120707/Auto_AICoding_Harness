---
name: security-review
description: Use when changes touch auth, permissions, secrets, input parsing, IPC, filesystem writes, subprocess execution, network boundaries, or destructive operations.
source: adapted
upstream: getsentry/skills security-review patterns
license: see-upstream
adaptation_notes: Adapted as a conservative review checklist only; no third-party scripts, marketplace commands, or Sentry-specific workflow included.
---

# Security Review

## Purpose

Escalate and review security-sensitive changes before they become casual implementation details.

## Use When

Use when touching authentication, authorization, permissions, credentials, tokens, IPC, network input, parsers, filesystem access, subprocess execution, logging of sensitive data, or destructive commands.

## Inputs

Current diff, `AGENTS.md`, relevant `docs/ai/*`, public interfaces, error paths, logs, test output, and any trust-boundary assumptions.

## Process

Identify trust boundaries and privileged operations.
Check input validation, output encoding, error handling, and permission checks.
Check secret handling, logging, environment variables, and credential propagation.
Check filesystem, subprocess, shell, and network side effects.
Classify whether the task needs stronger review or Level 2 / Level 3 handling.
Record concrete mitigations and verification evidence.

## Output

A security review note with risks, evidence, affected files, required fixes, and residual risk.

## Do Not

Do not log secrets.
Do not weaken permission checks without explicit approval.
Do not execute destructive commands casually.
Do not treat security-sensitive changes as low-risk work.
