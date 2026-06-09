---
name: security-review
description: Use when changes touch auth, permissions, secrets, input parsing, IPC, filesystem writes, subprocess execution, network boundaries, or destructive operations.
source: adapted
upstream: addyosmani/agent-skills skills/security-and-hardening; getsentry/skills security-review patterns
license: MIT plus referenced patterns
adaptation_notes: Expanded into a fuller harness-safe review workflow. Uses MIT upstream workflow structure and selective generic risk patterns only; does not copy OWASP-derived checklist text or vendor third-party scripts.
---

# Security Review

## Purpose

Escalate and review security-sensitive changes before they become casual implementation details.

Security review is not a separate late-stage phase.
It is a stricter lens for tasks that touch trust boundaries.

## Use When

Use when touching:

- authentication
- authorization
- permissions
- secrets and tokens
- input parsing
- IPC
- filesystem access
- subprocess execution
- network boundaries
- logging of sensitive data
- destructive commands

## Inputs

- current diff
- `AGENTS.md`
- relevant `docs/ai/*`
- public interfaces
- error paths
- logs
- test output
- trust-boundary assumptions

## Process

### 1. Model the Trust Boundaries

Before reviewing code, ask:

- where does untrusted data enter?
- what privileged action happens here?
- what secret or sensitive state is exposed?

Typical boundaries:

- HTTP input
- CLI args
- config files
- message queues
- filesystem paths
- subprocess invocations
- remote service responses

### 2. Check Auth and Permission Semantics

Review:

- who is allowed to do this?
- where is that check enforced?
- can a caller skip the guard?
- does the code assume identity without proving it?

Permission logic must be explicit, not implied by route structure or UI flow.

### 3. Review Secrets and Sensitive Data Handling

Check:

- are secrets stored in code?
- are tokens logged?
- are environment variables propagated safely?
- are sensitive values echoed into review artifacts or traces?

Any secret leak is at least a required finding.

### 4. Validate Input and Output Boundaries

Review:

- input normalization
- parser failure handling
- path validation
- command argument construction
- output encoding where needed

Treat every external input as hostile until proven otherwise.

### 5. Review Filesystem and Subprocess Risk

For filesystem writes and command execution:

- is the target path validated?
- can user input escape the intended directory?
- is a shell being invoked unnecessarily?
- are destructive operations bounded?

This repository uses safe-write patterns for a reason.
Do not bypass them casually.

### 6. Review Network and IPC Surfaces

Check:

- remote target validation
- protocol assumptions
- timeout behavior
- retry semantics
- logging and error exposure

If external responses are trusted too early, call that out.

### 7. Escalate Task Level If Needed

Security-sensitive work should not stay low-control just because the diff is short.

Escalate when:

- auth logic changes
- secret handling changes
- a new privileged path is created
- filesystem or subprocess semantics broaden

## Output

Produce a security review note with:

- risks
- evidence
- affected files
- required fixes
- residual risk
- level-escalation recommendation when relevant

## Do Not

- do not log secrets
- do not weaken permission checks without explicit approval
- do not execute destructive commands casually
- do not treat security-sensitive changes as low-risk by default
- do not confuse "works" with "safe"
