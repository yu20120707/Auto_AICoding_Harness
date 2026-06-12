# Generated Target Structure

The exact generated files depend on which commands have already been run, but the target repository typically grows toward this shape:

```text
target-repo/
├── AGENTS.md
├── CLAUDE.md
├── .github/
│   └── copilot-instructions.md
├── .codex/agents/
│   ├── README.md
│   ├── planner.md
│   ├── explorer.md
│   ├── implementer.md
│   ├── reviewer.md
│   └── evaluator.md
├── docs/ai/
│   ├── README.md
│   ├── cpp-system.md
│   ├── linux-debug.md
│   ├── network.md
│   ├── concurrency.md
│   ├── api-abi.md
│   ├── performance.md
│   ├── observability.md
│   ├── cmake.md
│   ├── build.md
│   ├── testing.md
│   ├── workflow.md
│   ├── verification-matrix.md
│   └── tasks/
│       ├── README.md
│       └── <task-id>/
│           ├── 00-prd.md
│           ├── 01-spec.md
│           ├── 02-tech-design.md
│           ├── 03-implementation-plan.md
│           ├── 04-diff-review.md
│           ├── 05-verification.md
│           ├── 06-risk-and-rollback.md
│           └── 07-handoff.md
├── scripts/
│   ├── ai_build.sh
│   ├── ai_test.sh
│   └── ai_check.sh
└── .ai/
    ├── .gitkeep
    ├── templates/
    ├── subagent-packets/
    │   ├── README.md
    │   ├── planner.md
    │   ├── explorer.md
    │   ├── implementer.md
    │   ├── reviewer.md
    │   └── evaluator.md
    ├── state.json
    ├── epic.md
    ├── spec.md
    ├── tech-design.md
    ├── scope.md
    ├── implementation-plan.md
    ├── affected-files.md
    ├── run-trace.md
    ├── verification.md
    ├── risk-and-rollback.md
    ├── evaluation.md
    ├── context-pack.md
    ├── handoff.md
    ├── reviews/
    ├── approvals/
    └── backups/
```

`ai-init small` also creates `.github/copilot-instructions.md` as a lightweight Copilot trigger that points agents back to `AGENTS.md`, task levels, `docs/ai/*`, and `.ai/*`.

Repository-owned global skills are not generated into the target repository.
They live in this harness repository and can be installed or copied by the active local agent:

```text
Auto_AICoding_Harness/
├── global/
│   └── AGENTS.md.template
├── prompts/
│   └── bootstrap-local-agent.md
└── skills/
    ├── README.md
    ├── methodology/
    │   ├── karpathy-guidelines/SKILL.md
    │   ├── task-router/SKILL.md
    │   ├── repo-onboarding-analysis/SKILL.md
    │   ├── source-driven-development/SKILL.md
    │   ├── planning-and-task-breakdown/SKILL.md
    │   ├── task-contract-and-leveling/SKILL.md
    │   ├── context-engineering/SKILL.md
    │   ├── systematic-debugging/SKILL.md
    │   ├── code-review-and-quality/SKILL.md
    │   ├── test-driven-development/SKILL.md
    │   ├── verification-before-completion/SKILL.md
    │   └── skill-creator/SKILL.md
    └── system/
        ├── cpp-linux-system-engineering/SKILL.md
        ├── security-review/SKILL.md
        └── performance-analysis/SKILL.md
```

## When Files Appear

- `ai-init small` creates the base repository structure: `AGENTS.md`, `docs/ai/`, `scripts/`, `.ai/state.json`, and `.ai/templates/`.
- `ai-init small` also adds `docs/ai/workflow.md` so target projects have a durable execution contract outside runtime state.
- `ai-init medium` creates the same base structure plus `.ai/implementation-plan.md`, `.ai/run-trace.md`, and `.ai/verification.md`.
- `ai-upgrade medium` adds that same bounded medium scaffold when starting from `small`.
- `ai-upgrade large` adds the richer `.ai/` planning and review scaffold such as `epic.md`, `spec.md`, `scope.md`, `implementation-plan.md`, `affected-files.md`, `run-trace.md`, `verification.md`, `evaluation.md`, `reviews/`, and `approvals/`.
- `ai-upgrade large` also creates a task-scoped evidence chain under `docs/ai/tasks/<task-id>/` so large-mode work has a durable PRD/spec/design/plan/review/verification/handoff trail.
- `ai-upgrade large` also leaves command-line evidence and sets up the next-action path for the strict large-mode gate chain.
- `run-trace.md` is also the required place to record any real subagent dispatch with explicit role-to-skill mapping.
- `ai-dispatch` appends that standardized dispatch record into `run-trace.md` when large mode is active.
- `ai-upgrade large` also adds optional `.codex/agents/` role templates.
- `ai-upgrade large` also adds `.ai/subagent-packets/` prompt/context templates for bounded role delegation.
- `ai-install-skills` installs a manifest-selected repository-owned skill subset into the user's Codex skills directory as an example installer.
- `prompts/bootstrap-local-agent.md` tells the active local agent how to install the same sources into its own supported locations.
- `ai-upgrade large` does not generate `.agents/skills/`; target projects use installed or copied skills after local-agent setup.
- `ai-context-pack` creates `.ai/context-pack.md`.
- `ai-handoff` creates `.ai/handoff.md`.
- `ai-review ...` creates files under `.ai/reviews/`.
- `ai-approve ...` and `ai-reject ...` create files under `.ai/approvals/`.
- `ai-doctor` inspects `.ai/state.json`, generated workflow files, and obvious mode mismatches without writing new runtime state.
- `--force` operations create files under `.ai/backups/`.

## Commit Guidance

- `docs/ai/` = long-lived project AI knowledge and should usually be committed.
- `.codex/agents/` = optional subagent role templates and can be committed when the project wants explicit large-mode agent guidance.
- global skills live outside the target project under `$CODEX_HOME/skills` or `~/.codex/skills`.
- `scripts/` = project validation entrypoints and should usually be committed.
- `.ai/` = runtime and task state; most of it should usually stay ignored except `.ai/templates/` and `.ai/.gitkeep`.
- `.ai/subagent-packets/` = runtime role-delegation packet templates; commit only if the target project wants reusable packet guidance.
- `.ai/reviews/` and `.ai/approvals/` = runtime review artifacts.
- `.ai/backups/` = runtime backup artifacts.
