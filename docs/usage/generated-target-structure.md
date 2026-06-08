# Generated Target Structure

The exact generated files depend on which commands have already been run, but the target repository typically grows toward this shape:

```text
target-repo/
├── AGENTS.md
├── .agents/skills/
│   ├── README.md
│   ├── methodology/
│   │   ├── design-before-code/SKILL.md
│   │   ├── systematic-debugging/SKILL.md
│   │   ├── verification-before-completion/SKILL.md
│   │   └── human-in-loop-development/SKILL.md
│   └── system/
│       ├── cpp-system-dev/SKILL.md
│       ├── linux-debug/SKILL.md
│       ├── network-programming/SKILL.md
│       ├── concurrency-review/SKILL.md
│       ├── performance-analysis/SKILL.md
│       └── cpp-api-abi-review/SKILL.md
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
│   ├── cmake.md
│   ├── build.md
│   └── testing.md
├── scripts/
│   ├── ai_build.sh
│   ├── ai_test.sh
│   └── ai_check.sh
└── .ai/
    ├── .gitkeep
    ├── templates/
    ├── state.json
    ├── spec.md
    ├── scope.md
    ├── implementation-plan.md
    ├── affected-files.md
    ├── run-trace.md
    ├── evaluation.md
    ├── context-pack.md
    ├── handoff.md
    ├── reviews/
    ├── approvals/
    └── backups/
```

## When Files Appear

- `ai-init small` creates the base repository structure: `AGENTS.md`, `docs/ai/`, `scripts/`, `.ai/state.json`, and `.ai/templates/`.
- `ai-upgrade large` adds the richer `.ai/` planning and review scaffold such as `spec.md`, `scope.md`, `implementation-plan.md`, `affected-files.md`, `run-trace.md`, `evaluation.md`, `reviews/`, and `approvals/`.
- `ai-upgrade large` also adds optional `.codex/agents/` role templates.
- `ai-upgrade large` also adds optional `.agents/skills/` local templates.
- `ai-context-pack` creates `.ai/context-pack.md`.
- `ai-handoff` creates `.ai/handoff.md`.
- `ai-review ...` creates files under `.ai/reviews/`.
- `ai-approve ...` and `ai-reject ...` create files under `.ai/approvals/`.
- `--force` operations create files under `.ai/backups/`.

## Commit Guidance

- `docs/ai/` = long-lived project AI knowledge and should usually be committed.
- `.codex/agents/` = optional subagent role templates and can be committed when the project wants explicit large-mode agent guidance.
- `.agents/skills/` = optional project-level skill templates and can be committed when the project wants local enhancement guidance.
- `scripts/` = project validation entrypoints and should usually be committed.
- `.ai/` = runtime and task state; most of it should usually stay ignored except `.ai/templates/` and `.ai/.gitkeep`.
- `.ai/reviews/` and `.ai/approvals/` = runtime review artifacts.
- `.ai/backups/` = runtime backup artifacts.
