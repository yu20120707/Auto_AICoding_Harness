# Auto_AICoding_harness

`Auto_AICoding_harness` 是一个面向 Codex 的 AI Coding Harness 源仓库。
它服务于我们自己的 `C++ / Linux / 后端 / 系统工程` 工作流。

这个仓库不是业务项目本身，也不是目标项目运行态。
它保存的是规则、模板、profile、命令入口和测试，用来把一套稳定的 Codex 工作流注入到其他目标项目里。

## 当前基线

当前实现基线是 `v1.3-skill-creator-zh-readme`。

已实现命令：

- `ai-init small`
- `ai-upgrade large`
- `ai-status`
- `ai-review spec / plan / diff / final`
- `ai-approve spec / plan / diff / final`
- `ai-reject spec / plan / diff / final`
- `ai-context-pack`
- `ai-handoff`

仍未实现：

- subagent 执行逻辑
- skills 安装逻辑
- 自动拉取第三方 skills
- 多 profile marketplace

## 生成内容

`ai-init small` 会在目标项目中生成基础结构：

- `AGENTS.md`
- `docs/ai/*`
- `scripts/ai_build.sh`
- `scripts/ai_test.sh`
- `scripts/ai_check.sh`
- `.ai/state.json`
- `.ai/templates/`

`ai-upgrade large` 会补充 large mode 结构：

- `.ai/epic.md`
- `.ai/spec.md`
- `.ai/scope.md`
- `.ai/implementation-plan.md`
- `.ai/affected-files.md`
- `.ai/run-trace.md`
- `.ai/evaluation.md`
- `.ai/reviews/`
- `.ai/approvals/`
- `.codex/agents/`
- `.agents/skills/`

## Skills

当前 large mode 会生成 `10` 个本地 project-level skill 模板。
它们不是自动安装的第三方 skill，也不带执行脚本。

Methodology:

- `karpathy-guidelines`
- `task-contract-and-leveling`
- `context-engineering`
- `systematic-debugging`
- `verification-before-completion`
- `code-review-and-quality`
- `skill-creator`

System:

- `cpp-linux-system-engineering`
- `security-review`
- `performance-analysis`

每个 skill 都要求写明：

- `source`
- `upstream`
- `license`
- `adaptation_notes`

这样可以区分自写、改造和第三方参考来源。

## Windows 用法

```powershell
py bin/ai-status
py bin/ai-init small
py bin/ai-upgrade large
py bin/ai-review diff
py bin/ai-approve diff
py bin/ai-context-pack
py bin/ai-handoff
```

运行回归测试：

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

## 边界原则

- `core` 只管 workflow、state、gate、safe write。
- `profile` 只管 C++ / Linux / backend / system 工程策略。
- `templates/` 是生成目标项目文件的唯一模板源。
- `.ai/` 是目标项目运行态，不是长期知识库。
- `docs/ai/` 是长期 AI 项目知识，通常应该提交到目标项目。
- `subagent` 和 `skills` 是增强层，不是正确性依赖。
- 默认不覆盖已有文件；只有 `--force` 才会先备份再覆盖。
