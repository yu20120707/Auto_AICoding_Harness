# Decision Records

## DR-001: The harness remains repository-owned, not a generated runtime

Status: accepted

Reason:

- template source, workflow rules, and portable skills need one canonical maintenance repo
- target projects should receive managed outputs, not the harness source tree itself

## DR-002: `.ai/state.json` is the workflow source of truth

Status: accepted

Reason:

- natural-language claims about mode or gate changes are not reliable enough
- review, approval, and escalation must be script-backed and diagnosable

## DR-003: Keep `small`, `medium`, and `large` as control strengths on one workflow

Status: accepted

Reason:

- `small` is needed for local low-risk work
- `medium` covers bounded multi-file tasks without full large-mode ceremony
- `large` keeps the strict review chain for higher-risk work

## DR-004: Keep `.ai/` as runtime while adding `docs/ai/tasks/<task-id>/` for durable large evidence

Status: accepted

Reason:

- `.ai/` already powers commands and existing tests
- a task-scoped durable chain is more reviewable and better for handoff
- syncing both avoids a breaking redesign

## DR-005: Profiles are metadata-backed overlays

Status: accepted

Reason:

- profile selection should be validated by code, not only by README prose
- a profile needs explicit languages, domains, risk triggers, and verification defaults
- core workflow behavior must stay separate from profile policy

## DR-006: Skills are selectively installed, not blindly copied

Status: accepted

Reason:

- repository-owned skills should stay portable and deduplicated
- target projects should receive project facts and workflow guidance, not the full skill source tree

## DR-007: `ai-dispatch` stays large-only for now

Status: accepted

Reason:

- packet-based dispatch depends on the large scaffold
- `medium` may still use subagents, but coordination can stay manual until a lighter dispatch contract is designed

## DR-008: No third-party runtime dependencies in core

Status: accepted

Reason:

- commands should stay runnable in constrained local environments
- manifest loading, safe writes, and workflow control should not depend on optional packages
