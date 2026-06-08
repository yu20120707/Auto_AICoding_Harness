# Auto_AICoding_harness

`Auto_AICoding_harness` is a `Codex-only AI Coding Harness` source repository.
It is optimized for our own `C++ / Linux / backend / system engineering` workflow.

This repository is not a target project runtime.
It stores the rules, templates, prompts, scripts, and profile overlays used to inject a stable Codex workflow into other repositories.

## Scope

- `core` concerns: workflow contracts, mode switching, review gates, state semantics, handoff, context packaging, and safe file-write policy.
- `profile` concerns: `cpp-linux-backend-system` engineering policy, checklists, prompts, and target-project overlays.
- `templates/` is the single source of truth for generated target-project files.

## Non-goals

- Do not treat this repository as a live `.ai/` runtime.
- Do not store target-project task state here.
- Do not couple core contracts to `cmake`, `ctest`, or other profile-specific tooling.
- Do not optimize for generic public compatibility over our own workflow stability.

## Design Rules

- `core` owns process contracts, not language or build-system policy.
- `profile` owns engineering policy, not process control.
- `small` and `large` are different control strengths on one workflow, not two different systems.
- `subagent` and `skills` are acceleration layers, never correctness dependencies.
- Target-project long-lived knowledge lives in `docs/ai/`; target-project task runtime lives in `.ai/`.
- Default file policy is `SKIPPED`; overwrite requires `--force` and per-file backup.

## Repository Layout

- [AGENTS.md](/C:/Users/26561/Documents/Auto_AICoding_Harness/AGENTS.md)
- [docs/design/reviewed-final-design-v1.md](/C:/Users/26561/Documents/Auto_AICoding_Harness/docs/design/reviewed-final-design-v1.md)
- [docs/design/current-capabilities.md](/C:/Users/26561/Documents/Auto_AICoding_Harness/docs/design/current-capabilities.md)
- [docs/design/command-contracts.md](/C:/Users/26561/Documents/Auto_AICoding_Harness/docs/design/command-contracts.md)
- [docs/design/state-machine.md](/C:/Users/26561/Documents/Auto_AICoding_Harness/docs/design/state-machine.md)
- [docs/design/repo-boundaries.md](/C:/Users/26561/Documents/Auto_AICoding_Harness/docs/design/repo-boundaries.md)
- [templates/README.md](/C:/Users/26561/Documents/Auto_AICoding_Harness/templates/README.md)
- [profiles/cpp-linux-backend-system/README.md](/C:/Users/26561/Documents/Auto_AICoding_Harness/profiles/cpp-linux-backend-system/README.md)
- [prompts/README.md](/C:/Users/26561/Documents/Auto_AICoding_Harness/prompts/README.md)
- [scripts/README.md](/C:/Users/26561/Documents/Auto_AICoding_Harness/scripts/README.md)
- [README.zh-CN.md](/C:/Users/26561/Documents/Auto_AICoding_Harness/README.zh-CN.md)

## Current Status

This repository currently implements the `v1.3-skill-creator-zh-readme` baseline.
The audited design documents remain the contract source, and future-only capabilities are marked explicitly in `docs/design/`.

## Quick Start

Phase 13 currently supports `ai-init small`, `ai-upgrade large`, `ai-status`, `ai-review diff`, `ai-review spec`, `ai-review plan`, `ai-review final`, `ai-approve spec`, `ai-approve plan`, `ai-approve diff`, `ai-approve final`, `ai-reject spec`, `ai-reject plan`, `ai-reject diff`, `ai-reject final`, `ai-context-pack`, and `ai-handoff`.
`context-pack` and `handoff` do not advance the review state machine.
`ai-review spec` / `ai-review plan` / `ai-review final` generate review material and move state into the corresponding waiting gate only.
The full human gate closure is currently supported for `spec`, `plan`, `diff`, and `final`.
Phase 7 strengthened the `cpp-linux-backend-system` profile and target-project `docs/ai` plus script templates.
Phase 8 aligned the release baseline and usage docs.
Phase 9 added optional subagent role templates for large mode.
Phase 10 adds optional skills templates for large mode.
Phase 11 strengthens the optional skills library and maps subagent roles to recommended local skills.
Phase 12 consolidates skills into a smaller provenance-aware set adapted from selected high-quality upstream skills plus local C++/Linux system guidance.
Phase 13 adds a local `skill-creator` template and a Chinese README.
No new CLI commands were added in Phase 13.
subagent execution and skills installation are intentionally not implemented yet.
automatic third-party skill fetching is intentionally not implemented yet.
`subagent` and `skills` remain enhancement layers, not hard dependencies.
small mode does not depend on subagents.
small mode does not depend on skills.
If subagents are unavailable, the main agent should follow the same role contracts sequentially.
If skills are unavailable, the main agent should rely on `AGENTS.md` and `docs/ai/*` directly.
skills are local project-level enhancement templates, not auto-installed or auto-executed features.
skills declare provenance and adaptation notes; third-party scripts, hooks, marketplace metadata, and installers are not vendored.
Python integration tests are the stable verification path for the current implementation baseline.

## Release Docs

- [docs/release/v0.8-release-checklist.md](/C:/Users/26561/Documents/Auto_AICoding_Harness/docs/release/v0.8-release-checklist.md)
- [docs/usage/walkthrough.md](/C:/Users/26561/Documents/Auto_AICoding_Harness/docs/usage/walkthrough.md)
- [docs/usage/generated-target-structure.md](/C:/Users/26561/Documents/Auto_AICoding_Harness/docs/usage/generated-target-structure.md)

### Windows

Use `py` from the repository root:

```powershell
py bin/ai-status
py bin/ai-init small
py bin/ai-upgrade large
py bin/ai-review diff
py bin/ai-review spec
py bin/ai-review plan
py bin/ai-review final
py bin/ai-approve spec
py bin/ai-approve plan
py bin/ai-approve diff
py bin/ai-approve final
py bin/ai-reject spec
py bin/ai-reject plan
py bin/ai-reject diff
py bin/ai-reject final
py bin/ai-context-pack
py bin/ai-handoff
py bin/ai-init small --force
```

Run Python regression tests without requiring `bash`:

```powershell
py -m compileall bin core
py tests/test_ai_init_small.py
py tests/test_ai_upgrade_large.py
py tests/test_ai_review_diff.py
py tests/test_ai_approve_reject_diff.py
py tests/test_ai_context_handoff.py
py tests/test_current_capabilities.py
py tests/test_ai_review_spec_plan_final.py
py tests/test_ai_approve_reject_all_gates.py
py tests/test_cpp_profile_templates.py
py tests/test_e2e_workflow.py
py tests/test_subagent_templates.py
py tests/test_skill_templates.py
```

### Unix-like

Use `python3` from the repository root:

```bash
python3 bin/ai-status
python3 bin/ai-init small
python3 bin/ai-upgrade large
python3 bin/ai-review diff
python3 bin/ai-review spec
python3 bin/ai-review plan
python3 bin/ai-review final
python3 bin/ai-approve spec
python3 bin/ai-approve plan
python3 bin/ai-approve diff
python3 bin/ai-approve final
python3 bin/ai-reject spec
python3 bin/ai-reject plan
python3 bin/ai-reject diff
python3 bin/ai-reject final
python3 bin/ai-context-pack
python3 bin/ai-handoff
python3 bin/ai-init small --force
```

If the scripts have execute permission, you can also run:

```bash
bin/ai-status
bin/ai-init small
```

Run regression checks with:

```bash
python3 -m compileall bin core
python3 tests/test_ai_init_small.py
python3 tests/test_ai_upgrade_large.py
python3 tests/test_ai_review_diff.py
python3 tests/test_ai_approve_reject_diff.py
python3 tests/test_ai_context_handoff.py
python3 tests/test_current_capabilities.py
python3 tests/test_ai_review_spec_plan_final.py
python3 tests/test_ai_approve_reject_all_gates.py
python3 tests/test_cpp_profile_templates.py
python3 tests/test_e2e_workflow.py
python3 tests/test_subagent_templates.py
python3 tests/test_skill_templates.py
```

### Shell Test

The repository also keeps [tests/test_ai_init_small.sh](/C:/Users/26561/Documents/Auto_AICoding_Harness/tests/test_ai_init_small.sh).
On Windows systems without a working `bash` or `sh`, prefer the Python regression test above.
