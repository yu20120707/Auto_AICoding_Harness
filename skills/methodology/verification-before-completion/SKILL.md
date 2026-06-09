---
name: verification-before-completion
description: Prevent false completion by requiring build, test, check, or documented not-run evidence before final claims.
source: adapted
upstream: obra/superpowers skills/verification-before-completion
license: MIT
adaptation_notes: Expanded for harness command outputs, `.ai/evaluation.md`, and review artifacts; keeps the same evidence-first rule while aligning to repository workflows.
---

# Verification Before Completion

## Purpose

Prevent false completion.

This skill exists to stop one specific failure mode:

- claiming success from confidence instead of evidence

## Use When

Use:

- before saying a task is done
- before saying a fix works
- before creating a commit or PR
- before writing final review or evaluation output
- after implementation and before status claims

## Inputs

- build, test, and check commands
- current diff
- command output
- `.ai/evaluation.md`
- `.ai/run-trace.md`
- `.ai/reviews/*`
- task acceptance criteria

## Process

### 1. Follow the Iron Law

```text
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you have not run the relevant command in this turn or captured equivalent fresh evidence, you cannot honestly claim success.

### 2. Identify the Proof for Each Claim

Before you say anything positive, ask:

- what command proves this?
- what output proves this?
- what failure count or exit code matters?
- what remains unverified?

Examples:

| Claim | Required proof |
| --- | --- |
| tests pass | fresh test command output |
| build succeeds | fresh build command output |
| bug fixed | original failing scenario now passes |
| regression covered | new or existing test fails before and passes after |
| review complete | findings and verification gaps recorded |

### 3. Run the Full Check

Do not substitute partial checks for full ones without saying so.

Bad:

- lint passed, therefore build is fine
- one targeted test passed, therefore all regressions are impossible

Good:

- targeted test passed, full suite not run
- build passed, manual runtime check not run

### 4. Read the Output Carefully

Verification is not just command execution.
Read:

- exit code
- failure count
- skipped tests
- warnings that materially affect confidence
- partial-success messages

### 5. Distinguish Pass, Fail, And Not Run

Only three honest states exist:

- pass
- fail
- not run

"Should pass", "probably fixed", and "looks good" are not statuses.

### 6. Verify the Original Symptom

For bug fixes:

- reproduce the failing scenario
- apply the fix
- rerun the failing scenario
- rerun nearby regression checks

For stronger confidence, verify the red-green story when practical:

- failing check before fix
- passing check after fix

### 7. Validate Delegated Work Independently

If another agent reports success:

- inspect the diff
- verify the actual files
- rerun the relevant checks

Agent success reports are not verification evidence.

### 8. Record What Remains Unverified

If something meaningful was not run, say:

- what was not run
- why it was not run
- how that affects confidence
- what follow-up action is needed

## Verification Output Pattern

Use a structure like:

```text
verified:
- command / check / result

not_run:
- item / reason / follow-up

final_claim:
- what is safe to claim
```

## Red Flags

- "done" before tests
- "fixed" before rerunning the failing scenario
- trusting stale output from earlier turns
- using partial verification without labeling it
- expressing satisfaction before evidence

## Output

Produce verification evidence with:

- pass, fail, or not run status
- the command or artifact used
- any meaningful residual risk

Use the phrases `tests passed` or `not run` only when they reflect actual evidence.

## Do Not

- do not say tests passed if they were not run
- do not omit failures
- do not convert "not run" into implied success
- do not trust assumptions over fresh output
