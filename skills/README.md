# Skills

These skills are portable repository-owned skills shipped by this repository.
They do not execute anything by themselves.
For Codex, they can be installed explicitly with `bin/ai-install-skills`.
For other tools, use `prompts/bootstrap-local-agent.md` and `docs/install-targets.md`.
They are not installed implicitly by `git clone`.
They are not third-party skills.
They are repository-owned instruction-only skills adapted for our harness.
They are intentionally fuller workflow skills, not one-paragraph summary cards.
The goal is to retain most of the useful operating procedure from strong upstream skills while rewriting or adapting it to this harness.
Some skills may be kept almost verbatim from upstream when the upstream artifact is already the right shape for this repository.
If an environment has not loaded skills yet, the main Codex agent should read AGENTS.md and docs/ai/* directly.
Human review gates remain authoritative.

Do not install unreviewed third-party skills directly into this directory.
Do not put secrets or environment-specific credentials in SKILL.md.
Do not use skills to bypass review gates.

Current skill groups:

- `methodology/`
- `system/`

## Skill Manifest

Every live skill directory contains both:

- `SKILL.md`: the reusable instruction artifact
- `skill.yaml`: manifest metadata for default installs, `--scope`, `--profile`, `--list`, and the installed-skills manifest

`skill.yaml` currently declares:

- `name`
- `scope`
- `version`
- `install_default`
- `platforms`
- `summary`
- `triggers`
- optional `profile`

Methodology skills:

- `methodology/karpathy-guidelines`: keep code changes simple, scoped, assumption-aware, and verified.
- `methodology/task-router`: choose simple, medium, or complex execution and escalation behavior.
- `methodology/repo-onboarding-analysis`: generate durable `docs/ai/*` knowledge for existing repositories before feature work.
- `methodology/task-contract-and-leveling`: classify task risk, execution level, scope, verification, and human gates.
- `methodology/context-engineering`: select the smallest useful repo context for a task.
- `methodology/systematic-debugging`: diagnose by reproduction, evidence, root cause, minimal fix, and validation.
- `methodology/verification-before-completion`: prevent false completion with fresh verification evidence.
- `methodology/code-review-and-quality`: review diffs for correctness, regression risk, tests, and maintainability.
- `methodology/source-driven-development`: ground framework or library decisions in official documentation and source citations.
- `methodology/planning-and-task-breakdown`: decompose larger tasks into ordered, verifiable implementation slices.
- `methodology/test-driven-development`: enforce red-green-refactor before writing behavior-changing production code.
- `methodology/skill-creator`: create or update repository-owned global skills with concise metadata, provenance, and tests.

System skills:

- `system/cpp-linux-system-engineering`: cover C++ / Linux / backend / system engineering checks.
- `system/security-review`: review auth, permissions, secrets, input parsing, IPC, network, filesystem, and subprocess risk.
- `system/performance-analysis`: ground performance work in baseline and measurement evidence.

## Provenance Policy

Every skill declares `source`, `upstream`, `license`, and `adaptation_notes` in frontmatter.
Third-party skill ideas are adapted into repository-owned instruction-only skills.
Do not copy third-party scripts, hooks, install commands, marketplace metadata, or project-specific workflow assumptions into this directory.
When upstream license allows it, keep most of the workflow structure and practical checklists instead of collapsing the skill into a short abstract.
Exception: a small number of skills may intentionally keep upstream-original frontmatter and body when direct reuse is the better artifact.

## Role To Skill Routing

These mappings guide large-mode subagent work after global skill installation.
They do not make skills a substitute for review gates or state-machine evidence.
They do not bypass human gates.

| Role | Use When Available | Recommended By Risk |
| --- | --- | --- |
| `planner` | `karpathy-guidelines`, `task-contract-and-leveling`, `context-engineering`, `planning-and-task-breakdown` | `source-driven-development`, `security-review`, `performance-analysis`, `cpp-linux-system-engineering` |
| `explorer` | `context-engineering`, `systematic-debugging` | `source-driven-development`, `cpp-linux-system-engineering`, `performance-analysis`, `security-review` |
| `implementer` | `karpathy-guidelines`, `cpp-linux-system-engineering`, `verification-before-completion` | `test-driven-development`, `source-driven-development`, `security-review`, `performance-analysis`, `context-engineering` |
| `reviewer` | `code-review-and-quality`, `security-review`, `cpp-linux-system-engineering` | `source-driven-development`, `systematic-debugging`, `performance-analysis`, `verification-before-completion` |
| `evaluator` | `verification-before-completion`, `performance-analysis` | `systematic-debugging`, `context-engineering`, `code-review-and-quality` |

If skills are unavailable or Codex has not been restarted after installation, each role must follow `AGENTS.md`, `docs/ai/*`, and its `.codex/agents/*.md` role contract directly.

Use `methodology/skill-creator` only when creating, consolidating, or reviewing repository `skills/**/SKILL.md` files.
