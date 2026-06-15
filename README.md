<p align="center">
  <strong>Auto_AICoding_Harness</strong>
</p>

<p align="center">
  <strong>面向本地 AI Coding Agent 的工程工作流脚手架。</strong><br/>
  <sub>把 requirement clarification、small / medium / large 分级、review gate、verification、handoff 和 agent-facing instructions 固化进目标仓库，让本地 Codex / Claude Code / Copilot 等 agent 按稳定工程流程工作。</sub>
</p>

<p align="center">
  <a href="#quick-start">Quick Start</a> •
  <a href="#why-this-harness">Why</a> •
  <a href="#workflow-modes">Modes</a> •
  <a href="#commands">Commands</a> •
  <a href="docs/usage/real-world-prompts.md">Prompt Patterns</a> •
  <a href="docs/usage/generated-target-structure.md">Generated Structure</a> •
  <a href="docs/design/reviewed-final-design-v1.md">Design</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/baseline-v1.7--optimization--hardening-2563eb?style=flat-square" alt="baseline" />
  <img src="https://img.shields.io/badge/modes-small%20%7C%20medium%20%7C%20large-16a34a?style=flat-square" alt="modes" />
  <img src="https://img.shields.io/badge/profile-cpp--linux--backend--system-0f766e?style=flat-square" alt="profile" />
  <img src="https://img.shields.io/badge/commands-ai--init%20%7C%20ai--review%20%7C%20ai--handoff-eab308?style=flat-square" alt="commands" />
</p>

## What It Is

`Auto_AICoding_Harness` is a source repository for AI coding workflow assets. It is not a business project, not a target-project runtime, and not an automatic execution engine.

It provides:

- command entrypoints under `bin/`
- workflow logic under `core/`
- generated target-project templates under `templates/`
- engineering overlays under `profiles/`
- portable skills under `skills/`
- design and usage docs under `docs/`

Current focus: our own `C++ / Linux / backend / system engineering` workflow, while keeping core workflow contracts profile-neutral.

## Why This Harness

| Capability | What It Changes |
| --- | --- |
| **Requirement clarification by default** | Every mode starts by restating target, scope, constraints, and verification intent before implementation. |
| **Small / medium / large control levels** | One workflow scales from quick local edits to gated multi-stage work without renaming the user-facing model. |
| **Repo-native workflow artifacts** | Generated projects get `AGENTS.md`, `docs/ai/`, `.ai/state.json`, scripts, and optional large-mode evidence chains. |
| **Review gate discipline** | Large mode enforces `spec -> plan -> diff -> final` review / approve / reject ordering. |
| **Context and handoff support** | Medium and large work can maintain `implementation-plan`, `run-trace`, `verification`, `context-pack`, and `handoff` artifacts. |
| **Portable agent guidance** | Skills and instruction templates help Codex / Claude Code / Copilot-style agents share consistent behavior. |

## Quick Start

Windows:

```powershell
py bin/ai-status
py bin/ai-install-skills --dry-run
py bin/ai-install-skills
py bin/ai-init small
```

Unix-like:

```bash
python3 bin/ai-status
python3 bin/ai-install-skills --dry-run
python3 bin/ai-install-skills
python3 bin/ai-init small
```

Typical next steps:

1. Run `ai-status` in the target repository.
2. If uninitialized, run `ai-init small` or `ai-init medium`.
3. For complex work, run `ai-upgrade large`.
4. In large mode, follow `ai-review spec`, `ai-approve spec`, `ai-review plan`, `ai-approve plan`, then implement and review the diff.

More detail:

- [Generated target structure](docs/usage/generated-target-structure.md)
- [Walkthrough](docs/usage/walkthrough.md)
- [Real-world prompt patterns](docs/usage/real-world-prompts.md)

## Workflow Modes

| Mode | Use When | Adds |
| --- | --- | --- |
| `small` | A local bug fix, config change, prompt tweak, or small docs edit. | Base agent instructions, `docs/ai/`, scripts, `.ai/state.json`. |
| `medium` | A bounded multi-file task needs an explicit plan, trace, and verification record. | `.ai/implementation-plan.md`, `.ai/run-trace.md`, `.ai/verification.md`. |
| `large` | The task affects workflow, shared interfaces, state, review, approval, context, or cross-session handoff. | Spec / plan / diff / final gates, reviews, approvals, subagent packets, task evidence chain. |

Rule of thumb:

- “直接改，改完很快能验” -> usually `small`
- “需要先控范围、留痕、分阶段审” -> use `large`

## Commands

| Command | Responsibility |
| --- | --- |
| `ai-init small|medium` | Initialize a target repository with base or medium harness files. |
| `ai-upgrade medium|large` | Upgrade control strength without downgrades or default deletes. |
| `ai-status` | Show human-readable workflow status and next action. |
| `ai-state` | Print canonical machine-facing `.ai/state.json`. |
| `ai-doctor` | Diagnose state, generated-file presence, and obvious mode mismatches. |
| `ai-review spec|plan|diff|final` | Generate review artifacts and move to the corresponding waiting gate. |
| `ai-approve spec|plan|diff|final` | Record approval and advance the workflow when valid. |
| `ai-reject spec|plan|diff|final` | Record rejection and move to retry / fix / more-tests state. |
| `ai-context-pack` | Package resumable context without advancing workflow state. |
| `ai-handoff` | Write next-session handoff without advancing workflow state. |
| `ai-dispatch` | Record large-mode role dispatch packets; does not start subagents. |
| `ai-install-skills` | Install repository-owned Codex example skills explicitly. |

Contract details: [Command Contracts](docs/design/command-contracts.md)

## How It Works

```text
small
  -> clarify requirement
  -> make scoped change
  -> optional diff/final review

medium
  -> clarify requirement
  -> maintain implementation-plan / run-trace / verification
  -> make bounded multi-file change
  -> review when useful

large
  -> ai-upgrade large
  -> ai-review spec -> ai-approve spec
  -> ai-review plan -> ai-approve plan
  -> implement
  -> ai-review diff -> ai-approve or ai-reject diff
  -> verification
  -> ai-review final -> ai-approve final
  -> context-pack / handoff when needed
```

Important boundaries:

- `docs/ai/` is long-lived project knowledge.
- `.ai/` is task runtime state and artifacts.
- `.ai/state.json` remains the canonical command-level workflow state.
- `docs/ai/tasks/<task-id>/` is the durable large-mode evidence chain.
- `.ai/subagent-packets/` records role packets; it is not an automatic subagent runner.

## Generated Target Structure

`ai-init small` generates the base harness surface:

- `AGENTS.md`
- `CLAUDE.md`
- `.github/copilot-instructions.md`
- `docs/ai/`
- `scripts/ai_build.sh`, `scripts/ai_test.sh`, `scripts/ai_check.sh`
- `.ai/state.json`
- `.ai/templates/`

`ai-init medium` adds planning and verification runtime files.

`ai-upgrade large` adds large-mode spec, plan, review, approval, handoff, subagent packet, and task evidence-chain files.

See the full list in [Generated Target Structure](docs/usage/generated-target-structure.md).

## Repository Map

| Path | Purpose |
| --- | --- |
| `bin/` | User-facing command entrypoints. |
| `core/` | Workflow contracts, state, review, approval, context, safe write, skill install logic. |
| `templates/` | The only source of generated target-project files. |
| `profiles/` | Engineering overlays; current main profile is `cpp-linux-backend-system`. |
| `skills/` | Repository-owned portable skill source. |
| `global/` | Global instruction templates. |
| `prompts/` | One-time local-agent setup prompts. |
| `docs/design/` | Workflow and repository contracts. |
| `docs/usage/` | Generated structure, walkthroughs, prompt patterns, and roadmap material. |
| `examples/` | Small / large snapshots and before/after examples. |
| `tests/` | Python integration tests and retained shell test. |

## Verification

Common Windows regression set:

```powershell
py -m compileall bin core
py tests/test_ai_init_small.py
py tests/test_ai_init_medium.py
py tests/test_ai_state.py
py tests/test_ai_upgrade_medium.py
py tests/test_ai_upgrade_large.py
py tests/test_ai_dispatch.py
py tests/test_ai_doctor.py
py tests/test_current_capabilities.py
py tests/test_safe_write.py
py tests/test_state_machine.py
py tests/test_subagent_templates.py
py tests/test_skill_templates.py
py tests/test_examples.py
```

Additional review / approval regressions:

```powershell
py tests/test_ai_review_diff.py
py tests/test_ai_review_spec_plan_final.py
py tests/test_ai_approve_reject_diff.py
py tests/test_ai_approve_reject_all_gates.py
py tests/test_ai_context_handoff.py
py tests/test_cpp_profile_templates.py
py tests/test_e2e_workflow.py
```

## Resources

| Need | Link |
| --- | --- |
| Install into a target repo | [Install Targets](docs/install-targets.md) |
| See generated files | [Generated Target Structure](docs/usage/generated-target-structure.md) |
| Follow a usage walkthrough | [Walkthrough](docs/usage/walkthrough.md) |
| Copy real-world prompts | [Prompt Patterns](docs/usage/real-world-prompts.md) |
| Understand the design | [Reviewed Final Design](docs/design/reviewed-final-design-v1.md) |
| Check command rules | [Command Contracts](docs/design/command-contracts.md) |
| Inspect current capabilities | [Current Capabilities](docs/design/current-capabilities.md) |
| Review optimization roadmap | [Optimization Roadmap](docs/usage/optimization-roadmap.md) |
| Browse skills | [Skills README](skills/README.md) |

## FAQ

<details>
<summary><strong>Is this a business project template?</strong></summary>

No. This repository is the source of truth for harness commands, templates, skills, and documentation. It should not contain target-project runtime files except as template source under `templates/` or local ignored `.ai/` work state.

</details>

<details>
<summary><strong>Does large mode automatically run subagents?</strong></summary>

No. Large mode creates stronger workflow artifacts and optional role packets. `ai-dispatch` records role dispatch context, but it does not start or manage subagents.

</details>

<details>
<summary><strong>Do small and medium use the full review gate chain?</strong></summary>

No. The command surface supports review commands, but `medium` does not enforce the large `spec -> plan -> diff -> final` chain by default, and `small` stays lightweight.

</details>

<details>
<summary><strong>Does core hard-code CMake, ctest, or clang-tidy?</strong></summary>

No. Core owns workflow semantics. Profile-specific build and check expectations belong in `profiles/`, currently focused on `cpp-linux-backend-system`.

</details>

<details>
<summary><strong>Does the harness overwrite existing files?</strong></summary>

Default writes are `SKIPPED`. Overwrite requires `--force`, and overwritten files are backed up under `.ai/backups/<timestamp>/`.

</details>

## Non-Goals

- Do not automatically take over business source code.
- Do not write secrets, API keys, or system dependencies.
- Do not fetch third-party skills automatically.
- Do not introduce `.harness/` or replace `docs/ai/ + .ai/`.
- Do not rename `small / medium / large` or replace the current `ai-*` command surface.
