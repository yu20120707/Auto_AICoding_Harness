# Architecture

## Purpose

`Auto_AICoding_Harness` is a repository-owned workflow harness for local AI coding agents.
It is not a business project runtime and it is not an automatic agent runner.

Its job is to make long-running engineering work stateful, reviewable, resumable, and verifiable.

## Layers

### Core

`core/` owns workflow semantics and safety boundaries:

- state shape and transitions
- review / approve / reject gate contracts
- context-pack and handoff rendering
- safe managed writes into target projects
- command permission classification
- task-scoped large-mode evidence-chain sync
- profile manifest loading and validation

Core must stay independent from profile-specific build tools, compilers, and domain rules.

### Templates

`templates/` is the source of truth for generated target-project files.

Current stages:

- `templates/base/root/`: shared small-mode baseline
- `templates/base/medium/root/`: bounded multi-file execution scaffold
- `templates/base/large/root/`: full large-mode planning, review, and delegation scaffold

The harness writes only managed target-project paths such as:

- `AGENTS.md`
- `docs/ai/**`
- `.ai/**`
- `.codex/agents/**`
- `scripts/ai_*.sh`

### Profiles

`profiles/` overlays engineering-domain guidance onto the base workflow.

Current first-class profile:

- `cpp-linux-backend-system`

Each profile now has a `profile.yaml` metadata entrypoint plus template overlays and guidance docs.
Profiles may add domain language, risk triggers, and verification defaults, but they must not replace the core state machine.

### Skills

`skills/` stores portable repository-owned skills.

They are installed selectively into the local agent environment and are not blindly copied into target projects.

### System and Global Guidance

- `system/AGENTS.global.md`: cross-project behavioral rules
- `global/AGENTS.md.template`: user-level bootstrap guidance
- `prompts/`: one-time setup and handoff prompts

## Target Project Model

The generated target-project model separates durable knowledge from runtime state:

- `docs/ai/`: durable project guidance
- `docs/ai/tasks/<task-id>/`: durable large-mode task evidence chain
- `.ai/`: runtime workspace, state, reviews, approvals, context, and handoff artifacts

Large mode now keeps both:

- runtime working artifacts under `.ai/`
- synchronized task evidence under `docs/ai/tasks/<task-id>/`

This preserves backward compatibility while improving auditability and handoff quality.

## Main Command Flow

### Initialization

1. `ai-init small|medium`
2. write base managed files
3. validate selected profile metadata
4. create `.ai/state.json`

### Escalation

1. `ai-upgrade medium|large`
2. validate current state
3. materialize staged templates
4. rewrite `.ai/state.json`
5. in `large`, sync `docs/ai/tasks/<task-id>/`

### Review Chain

In `large` mode:

1. `ai-review spec`
2. `ai-approve spec`
3. `ai-review plan`
4. `ai-approve plan`
5. `ai-review diff`
6. `ai-approve diff`
7. `ai-review final`
8. `ai-approve final`

### Long-Running Work

- `ai-context-pack` writes resumable state
- `ai-handoff` writes continuation context
- `ai-doctor` diagnoses state, mode, scaffold, and task-chain mismatches

## Non-goals

- automatic subagent execution
- third-party dependency installation
- business-source-code generation
- formal multi-profile marketplace
- replacing human approval with agent self-approval
