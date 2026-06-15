# Auto_AICoding_Harness v1.7 Incremental Hardening Plan

## Positioning

This document defines a `v1.7-compatible hardening` plan for `Auto_AICoding_Harness`.
It is an incremental design on top of the current repository baseline.
It is not a `v2` redesign, not a control-plane replacement, and not a command-surface reset.

The goal is to absorb proven Trellis-style mechanisms:

- repo-native state
- task lifecycle
- scoped context
- context manifest
- implement/check separation
- finish memory
- template hash
- migration
- RCA feedback loop

The goal is not to copy Trellis directory layout, code, templates, prompts, or product surface.

## Non-Goals

This plan explicitly does not do the following:

1. Introduce `.harness/` as the user-project control plane.
2. Replace the existing `docs/ai/ + .ai/` source-of-truth split.
3. Replace `small / medium / large` with `Level 1 / 2 / 3`.
4. Introduce `ai-run`, `ai-task`, `ai-context`, or `ai-finish` as new public primary commands.
5. Present planned capabilities as already implemented.
6. Copy Trellis source code, templates, prompts, or document text.

## Baseline

### Source Of Truth

The existing split remains the baseline:

- `docs/ai/` = long-lived knowledge, specifications, profiles, workflow documents
- `.ai/` = runtime task state, epic artifacts, review gate artifacts, context-pack, handoff

This plan may extend those locations, but may not replace them.

### Existing User Surface

The existing user-facing semantics remain unchanged:

- `small`
- `medium`
- `large`

The existing public command surface also remains unchanged:

- `ai-install-skills`
- `ai-init`
- `ai-upgrade`
- `ai-doctor`
- `ai-status`
- `ai-state`
- `ai-dispatch`
- `ai-review`
- `ai-approve`
- `ai-reject`
- `ai-context-pack`
- `ai-handoff`

New hardening work should enter through:

- `core/*`
- `templates/*`
- `docs/ai/*`
- `.ai/*`

New user-visible commands are out of scope for this plan.

## Capability Matrix

This matrix is required to keep planning separate from current reality.

| Capability | Current Status | v1.7 Hardening Scope | Future Optional |
| --- | --- | --- | --- |
| `docs/ai/` long-lived knowledge | existing / frozen | preserve and refine spec categories | add spec health checks |
| `.ai/` runtime state | existing / frozen | add structured large-mode runtime artifacts | add stronger session isolation |
| `small / medium / large` | existing / frozen | preserve semantics | add automatic complexity hints |
| `ai-review` | existing | add structured review-gate state | add typed review scopes |
| `ai-approve` / `ai-reject` | existing | bind to task/review transitions | add reject-driven RCA hooks |
| `ai-context-pack` | existing | allow manifest-backed context packing | add token-budgeted scoped packing |
| `ai-handoff` | existing | read task summaries and final artifacts | add stronger cross-session restore |
| `task.json` schema | unknown / do not assume | add as a new core capability | add schema migrations |
| `context.jsonl` | planned | add for large mode first | optional medium usage |
| `quick-brief` | planned | not required in this plan | future repo-summary index |
| `ai_snapshot.json` | planned | not required in this plan | future repo snapshot capability |
| `check-rules` | planned | Phase 4 draft support | future matching and auto-load |
| RCA self-healing loop | planned | Phase 4 reject -> RCA -> rule draft | future historical failure linking |
| template hash | planned | Phase 5 | future registry or bundle support |
| migration | planned | Phase 5 dry-run and conflict policy | future versioned migration system |
| multi-platform expansion | not a current focus | do not expand platform count here | separate RFC later |

Required wording rule:

- `quick-brief`, `ai_snapshot.json`, `check-rules`, `ai-run`, and `ai-task` must not be described as existing repository assets unless they actually land in the codebase.

## Hardening Principles

### Compatibility First

No change in this plan may break the current contract formed by:

- `docs/ai/ + .ai/`
- `small / medium / large`
- the current `ai-*` command surface
- `README.md`
- `docs/design/reviewed-final-design-v1.md`

### Large Mode First

Trellis-style governance mechanisms belong primarily in `large`:

- task state
- context manifest
- review gate
- RCA
- check-rule draft
- finish summary
- template hash
- migration

This keeps heavier control where long-running, high-risk work already exists.

### Small Must Stay Light

`small` must not gain these by default:

- `task.json`
- `context.jsonl`
- RCA
- check-rule writing
- full review gate
- spec distillation

The purpose of `small` is still fast, low-friction execution.

### Medium Boundary Is Explicit

`medium` may gain lightweight planning or checking artifacts, but it does not inherit the full `large` gate chain.

This rule is mandatory:

> `medium` may generate lightweight artifacts, but it does not enter the full `ai-review / ai-approve / ai-reject` large-mode gate chain unless the user explicitly upgrades to `large`.

Default `medium` behavior:

| Capability | Medium Default |
| --- | --- |
| `plan.md` | optional |
| `task.json` | optional |
| `context.jsonl` | optional |
| `ai-review` gate | off by default |
| `ai-approve` / `ai-reject` | off by default |
| RCA | off by default |
| `check-rules` writeback | off by default |
| `handoff` | not required by default |
| upgrade to `large` | supported explicitly |

## Workflow

### Small

`small` remains a direct, lightweight path:

```text
user request
  -> ai-init small
  -> minimal context
  -> direct edit or direct instruction
  -> optional basic check
  -> ai-status
```

`small` does not require:

- `.ai/tasks/*`
- `context.jsonl`
- review gate artifacts

Typical fit:

- README fixes
- small docs edits
- narrow config fixes
- small template fixes

### Medium

`medium` adds bounded structure without becoming `large`:

```text
user request
  -> small path plus medium heuristics
  -> optional lightweight plan
  -> scoped docs/ai read
  -> implementation
  -> basic check summary
  -> done or suggest ai-upgrade large
```

Optional artifacts:

- `.ai/tasks/TASK-*/plan.md`
- `.ai/tasks/TASK-*/check.md`
- `.ai/tasks/TASK-*/summary.md`

Not created by default:

- review gate
- `approval.json`
- `rca.md`
- check-rule drafts
- handoff packages

Upgrade from `medium` to `large` when any of these are true:

1. The task touches workflow, state, review, approval, or context-pack core semantics.
2. The task becomes a multi-file structural change.
3. The task needs an explicit human gate.
4. The task needs cross-session handoff.
5. Verification fails more than once.

### Large

`large` is the main hardening target:

```text
user request
  -> ai-upgrade large
  -> .ai/spec.md
  -> .ai/implementation-plan.md
  -> context manifest generation
  -> implementation
  -> ai-review
  -> waiting approval gate
     -> ai-approve -> final / context-pack / handoff
     -> ai-reject -> reject reason -> RCA draft -> optional check-rule draft -> fix / re-review
```

Large-mode runtime additions:

- `.ai/tasks/TASK-*/task.json`
- `.ai/tasks/TASK-*/context.jsonl`
- `.ai/tasks/TASK-*/review.md`
- `.ai/tasks/TASK-*/approval.json`
- `.ai/tasks/TASK-*/rca.md`
- `.ai/tasks/TASK-*/final.md`

Relationship to the existing epic chain:

- `.ai/epic.md` remains the large-mode epic summary source.
- `.ai/spec.md` remains the large-mode requirement source.
- `.ai/implementation-plan.md` remains the large-mode planning source.
- `.ai/verification.md`, `.ai/evaluation.md`, `.ai/context-pack.md`, and `.ai/handoff.md` remain final-review evidence inputs.
- `.ai/tasks/TASK-*` is a structured runtime supplement, not a replacement.

## Directory Design

### Harness Repository

The hardening work should add or extend internals in place:

```text
Auto_AICoding_Harness/
├── bin/
│   ├── ai-init
│   ├── ai-status
│   ├── ai-upgrade
│   ├── ai-review
│   ├── ai-approve
│   ├── ai-reject
│   ├── ai-context-pack
│   └── ai-handoff
├── core/
│   ├── state/
│   │   ├── task_state.py
│   │   ├── schema.py
│   │   └── transition.py
│   ├── context/
│   │   ├── manifest.py
│   │   └── selector.py
│   ├── review/
│   │   ├── gate.py
│   │   └── approval.py
│   ├── rca/
│   │   ├── classifier.py
│   │   └── rule_draft.py
│   ├── template/
│   │   ├── hash.py
│   │   ├── update.py
│   │   └── migration.py
│   └── safe_write/
├── docs/
│   └── design/
│       └── trellis-inspired-v1.7-hardening.md
├── templates/
└── tests/
```

### Generated User Project

The user-project structure is extended incrementally, not replaced:

```text
target-project/
├── docs/
│   └── ai/
│       ├── workflow/
│       ├── specs/
│       ├── profiles/
│       ├── check-rules/        # planned Phase 4
│       └── migrations/         # planned Phase 5
└── .ai/
    ├── state.json
    ├── epic.md
    ├── spec.md
    ├── tech-design.md
    ├── implementation-plan.md
    ├── verification.md
    ├── evaluation.md
    ├── context-pack.md
    ├── handoff.md
    ├── tasks/                  # large-mode structured runtime supplement
    │   └── TASK-*/
    │       ├── task.json
    │       ├── context.jsonl
    │       ├── review.md
    │       ├── approval.json
    │       ├── rca.md
    │       └── final.md
    ├── context/
    │   ├── packs/
    │   └── manifests/
    └── handoff/
```

## Large-Mode Task State Hardening

### Goal

Introduce structured task state for `large` mode only, while keeping the existing epic chain intact.

Required invariant:

- `.ai/epic.md`, `.ai/spec.md`, `.ai/implementation-plan.md`, and the current final-review evidence files continue to carry the large-mode chain.
- `.ai/tasks/TASK-*` is only a structured runtime supplement.

### Suggested `task.json`

```json
{
  "schema_version": 1,
  "id": "TASK-20260614-example",
  "mode": "large",
  "status": "planning",
  "source": {
    "epic": ".ai/epic.md",
    "spec": ".ai/spec.md",
    "plan": ".ai/implementation-plan.md"
  },
  "scope": [],
  "created_at": "",
  "updated_at": "",
  "review": {
    "status": "none",
    "last_review": null
  },
  "approval": {
    "status": "none",
    "approved_by": null,
    "rejected_reason": null
  },
  "artifacts": {
    "context_manifest": "context.jsonl",
    "review": "review.md",
    "rca": "rca.md",
    "final": "final.md"
  }
}
```

### Suggested State Machine

```text
planning
  -> ready
  -> implementing
  -> reviewing
  -> waiting_approval
     -> approved -> finalizing -> completed
     -> rejected -> needs_fix -> implementing
```

Important scope rule:

- `medium` does not enter `waiting_approval` by default.
- `small` does not use this state machine.

## Context Manifest

### Role

`context.jsonl` is a large-mode context index.
It is not a source-code dump.

### Allowed References

- `docs/ai/specs/**`
- `docs/ai/profiles/**`
- `docs/ai/workflow/**`
- `docs/ai/check-rules/**`
- `.ai/spec.md`
- `.ai/implementation-plan.md`
- `.ai/tech-design.md`
- `.ai/risk-and-rollback.md`
- `.ai/context-pack.md`
- `.ai/handoff.md`
- `.ai/tasks/TASK-*/research/**`
- `.ai/context/packs/**`

### Disallowed By Default

- raw source text under `src/**`
- whole-repository dumps
- all historical tasks
- all handoff artifacts
- all journals

### Example

```jsonl
{"path":"docs/ai/specs/review-gate.md","reason":"Defines large-mode review gate policy","phase":"review"}
{"path":"docs/ai/profiles/cpp-linux-backend-system.md","reason":"Current engineering profile","phase":"implement"}
{"path":".ai/spec.md","reason":"Large-mode requirement source","phase":"implement"}
{"path":".ai/implementation-plan.md","reason":"Large-mode implementation plan","phase":"implement"}
```

## Review Gate Hardening

### No New Public Commands

Keep using:

- `ai-review`
- `ai-approve`
- `ai-reject`

### Internal State Additions

After `ai-review`, write:

- `.ai/tasks/TASK-*/review.md`
- `.ai/tasks/TASK-*/approval.json`

Suggested `approval.json`:

```json
{
  "status": "waiting",
  "review_type": "diff",
  "created_at": "",
  "review_summary": "",
  "risk_level": "medium",
  "required_action": "ai-approve or ai-reject"
}
```

Transitions:

- `ai-approve`: `waiting_approval -> approved`
- `ai-reject`: `waiting_approval -> rejected -> needs_fix`

## RCA And Check-Rule Drafts

### Planned, Not Existing

RCA and `check-rules` are planned capabilities in this design.
They are not current repository features unless they are later implemented.

### Reject Flow

```text
ai-reject
  -> write rejected reason
  -> optional RCA
  -> generate rca.md
  -> optional check-rule draft
```

### Rule Activation Policy

Check-rule drafts must not become enforced rules automatically.

Required policy:

> A generated check-rule draft does not enter `docs/ai/check-rules/index.yaml` automatically. It requires explicit approval or human confirmation.

This avoids agent-generated rule pollution.

## Template Hash And Migration

### Hard Constraint

Template hash and migration only strengthen updates for the existing `templates` system.
They may not change public user-project directory semantics.

Mandatory constraint:

> template hash and migration only enhance existing template update protection. They do not introduce `.harness`, do not migrate `docs/ai/ + .ai/` to a new control plane, and do not rename `small / medium / large` or replace the current `ai-*` command surface.

### Goal

Solve the safe-update problem:

- templates changed upstream
- users changed generated files locally
- updates must not overwrite local work silently

### Expected Behavior

| File State | Behavior |
| --- | --- |
| unchanged locally | auto-update allowed |
| user-modified | report conflict, do not overwrite |
| user-deleted | respect deletion by default |
| `--dry-run` | report only |
| `--force` | explicit overwrite only |
| migration | only declared path changes |

## Token Cost Control

### Small

`small` should:

- not load task manifests
- not load check-rules
- not load historical tasks
- only read the minimum required documents

### Medium

`medium` should:

- read scoped `docs/ai/specs` on demand
- allow optional plan/check artifacts
- avoid full review gate by default

### Large

`large` should:

- read `.ai/spec.md`
- read `.ai/implementation-plan.md`
- read `context.jsonl`
- load relevant `docs/ai` rules through the manifest
- read source code on demand

Core rule:

> read indexes and manifests first, then read full content only as needed.

## Roadmap

### Phase 0: Document Correction

Deliverable:

- `docs/design/trellis-inspired-v1.7-hardening.md`

Must include:

- capability matrix
- medium boundary
- template-hash constraint
- compatibility principles
- non-legal-opinion license wording

Acceptance:

- no `.harness` target control plane
- no `Level 1 / 2 / 3` user surface
- no `ai-run` or `ai-task` as new primary commands
- no planned capability presented as current fact

### Phase 1: Large-Mode Task State Hardening

Deliverables:

- `core/state/*`
- `tests/test_task_state.py`
- `.ai/tasks/TASK-*/task.json`

Acceptance:

- `task.json` schema validates
- state transitions validate
- illegal transitions fail
- `ai-status` can read task state
- `small` and `medium` remain unaffected by default

### Phase 2: Large-Mode Context Manifest

Deliverables:

- `core/context/manifest.py`
- `.ai/tasks/TASK-*/context.jsonl`

Acceptance:

- `context.jsonl` can be generated
- it does not include raw source text by default
- `ai-context-pack` can consume the manifest
- `large` can load `docs/ai` rules through the manifest

### Phase 3: Review Gate State

Deliverables:

- `core/review/gate.py`
- `.ai/tasks/TASK-*/review.md`
- `.ai/tasks/TASK-*/approval.json`

Acceptance:

- `ai-review` writes a waiting gate
- `ai-approve` moves state to approved
- `ai-reject` moves state to rejected or needs-fix
- existing `ai-review / ai-approve / ai-reject` remain usable

### Phase 4: RCA And Check-Rule Drafts

Deliverables:

- `core/rca/*`
- `docs/ai/check-rules/`
- `.ai/tasks/TASK-*/rca.md`

Acceptance:

- reject can generate `rca.md`
- a check-rule draft can be generated
- drafts do not become enforced automatically

### Phase 5: Template Hash And Migration Hardening

Deliverables:

- `core/template/*`
- `docs/ai/migrations/*`
- `.template-hashes.json` or `.ai/template-hashes.json`

Acceptance:

- `--dry-run` shows an update plan
- user-modified files are not overwritten
- `--force` is explicit
- migration does not change public directory semantics

## Risks

1. Large-mode hardening may leak into `medium` unless state, review, and migration boundaries are kept explicit.
2. Planned capability wording may drift back into “current capability” wording if the capability matrix is not maintained.
3. Template-update work may become a hidden v2 migration if public directory semantics are not treated as immutable.
4. Agent-generated rule drafts may pollute project policy unless approval is mandatory before rule activation.

## License Note

Trellis uses AGPL-3.0.
This document treats Trellis as a public architecture reference and not as a code-copy source.
It is not recommended to copy Trellis source code, templates, prompts, or document text.
If future work includes commercial distribution, closed-source use, SaaS integration, or direct reuse of Trellis code, legal review should confirm the actual license obligations.
This document is not legal advice.

## Final Summary

This plan is:

- not a Trellis clone
- not a `.harness` v2
- not a command-surface redesign
- not a directory replacement

This plan is:

- a `v1.7-compatible hardening` effort
- on top of the current `.ai + docs/ai + small/medium/large + ai-*` surface
- absorbing Trellis-style task state, context manifest, review gate, RCA, and template hash ideas incrementally

Trellis is a control-plane mechanism reference here, not a replacement template.
