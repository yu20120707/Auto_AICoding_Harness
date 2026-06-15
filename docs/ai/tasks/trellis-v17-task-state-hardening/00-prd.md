# Epic

## Task

Phase 1 large-mode task state hardening for the Trellis-inspired v1.7-compatible hardening plan.

## Background

The design document `docs/design/trellis-inspired-v1.7-hardening.md` establishes that Trellis-style task governance should be absorbed incrementally, without changing the existing `docs/ai/ + .ai/` split, `small / medium / large` user semantics, or public `ai-*` command surface.

The first implementation slice should add structured task-state support for `large` mode only. It must remain a supplement to the existing `.ai/state.json`, `.ai/spec.md`, `.ai/implementation-plan.md`, review gate, and `docs/ai/tasks/<task-id>/` evidence chain.

## Goal

Implement the minimum durable task-state foundation needed for later context manifests, review gate state, RCA drafts, and template hash work.

## Non-Goals

- Do not introduce `.harness/`.
- Do not rename or replace `small / medium / large`.
- Do not add `ai-run`, `ai-task`, `ai-context`, or `ai-finish` as public commands.
- Do not change `small` or `medium` default behavior.
- Do not implement context manifest, RCA, check-rules, or template migration in this phase.
- Do not copy Trellis code, templates, prompts, or document text.

## Acceptance

- A task-state schema exists for the new large-mode structured supplement.
- Legal and illegal state transitions can be validated.
- The new state support does not create a second replacement state system.
- `ai-status` can read and summarize the task supplement when present.
- Existing large review gates remain compatible.
- Existing tests for init, upgrade, status, review, approval, and task evidence chain remain passing.
