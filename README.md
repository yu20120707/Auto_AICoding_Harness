# Auto_AICoding_Harness

面向本地 AI Coding Agent 的工程工作流脚手架。

这个仓库不是业务项目，而是一个 Harness 源仓库：它提供命令、模板、skills、全局指令样板和设计文档，用来把稳定的 AI Coding 流程注入到其他目标项目中。

当前优先服务我们自己的 `C++ / Linux / 后端 / 系统工程` 场景。

## 适合什么

- 给 Codex / Claude Code / GitHub Copilot 等本地 agent 提供统一项目入口。
- 在目标项目中生成 `AGENTS.md`、`docs/ai/`、`.ai/`、检查脚本和 review gate 骨架。
- 把常用 AI coding 方法论沉淀成全局 skills。
- 根据任务复杂度在轻量流程和 large mode 流程之间切换。

## 不做什么

- 不自动接管业务源码。
- 不在 `git clone` 时写入用户全局配置。
- 不自动拉取第三方 skills。
- 不实现自动 subagent runner。
- 不把 CMake、ctest、clang-tidy 等 profile 策略硬编码进 core。

## 快速开始

Windows:

```powershell
py bin/ai-status
py bin/ai-install-skills
py bin/ai-install-skills --dry-run
py bin/ai-init small
py bin/ai-upgrade large
py bin/ai-state
```

类 Unix:

```bash
python3 bin/ai-status
python3 bin/ai-install-skills
python3 bin/ai-install-skills --dry-run
python3 bin/ai-init small
python3 bin/ai-upgrade large
python3 bin/ai-state
```

如果脚本有执行权限，也可以直接运行：

```bash
bin/ai-status
bin/ai-init small
```

## 推荐使用流程

1. 拉取本仓库。
2. 让本地 agent 阅读 `README.md`、`AGENTS.md`、`docs/install-targets.md` 和 `prompts/bootstrap-local-agent.md`。
3. 执行 `ai-install-skills`，把仓库内 skills 安装到当前 agent 支持的位置。
4. 在目标项目根目录执行 `ai-init small`。
5. 普通任务保持 small mode。
6. 复杂任务执行 `ai-upgrade large`，启用 spec / plan / review / approval / handoff 骨架。
7. 用 `ai-status` 查看当前状态。

## 当前能力

当前基线：`v1.7-optimization-hardening`。

已实现命令：

- `ai-install-skills`
- `ai-init small`
- `ai-upgrade large`
- `ai-status`
- `ai-state`
- `ai-review spec / plan / diff / final`
- `ai-approve spec / plan / diff / final`
- `ai-reject spec / plan / diff / final`
- `ai-context-pack`
- `ai-handoff`

仍未实现：

- subagent execution
- automatic third-party skill fetching
- multi-profile marketplace
- formal packaging / release CLI

## 生成到目标项目的内容

`ai-init small` 生成：

- `AGENTS.md`
- `CLAUDE.md`
- `.github/copilot-instructions.md`
- `docs/ai/`
- `docs/ai/verification-matrix.md`
- `scripts/ai_build.sh`
- `scripts/ai_test.sh`
- `scripts/ai_check.sh`
- `.ai/state.json`
- `.ai/templates/`

`ai-upgrade large` 追加：

- `.ai/epic.md`
- `.ai/spec.md`
- `.ai/scope.md`
- `.ai/implementation-plan.md`
- `.ai/affected-files.md`
- `.ai/run-trace.md`
- `.ai/evaluation.md`
- `.ai/reviews/`
- `.ai/approvals/`
- `.ai/subagent-packets/`
- `.codex/agents/`

`.ai/subagent-packets/` 是角色任务包模板，用来把任务目标、上下文、建议 skills、禁止事项和返回格式传给本地 agent 或 subagent。它不是自动执行器。

## Skills

仓库级 skills 位于 `skills/`，不会自动生成到目标项目。

当前分类：

- `skills/methodology/`：任务分级、上下文工程、调试、review、验证、skill 创建等方法论。
- `skills/system/`：C++ / Linux / 系统工程、安全 review、性能分析。

安装到 Codex 示例位置：

```powershell
py bin/ai-install-skills --dry-run
py bin/ai-install-skills
py bin/ai-install-skills --force
```

`ai-install-skills` 是 Codex 示例安装器。其他 agent 的安装位置参考 `docs/install-targets.md` 和 `prompts/bootstrap-local-agent.md`。

## 仓库结构

- `bin/`：用户直接执行的命令入口。
- `core/`：safe write、模板展开、state、review、approval、context、skill install 等公共逻辑。
- `templates/`：生成目标项目文件的唯一模板源。
- `profiles/`：profile overlay，目前主 profile 是 `cpp-linux-backend-system`。
- `skills/`：仓库维护的可移植 skill 源。
- `global/`：全局指令模板，例如 `AGENTS.md.template`。
- `prompts/`：一次性 bootstrap 或 handoff prompt。
- `docs/design/`：命令契约、状态机、repo 边界和 workflow 设计。
- `docs/usage/`：生成结构和使用 walkthrough。
- `tests/`：Python 集成测试和保留的 shell 测试。

## 验证

Windows:

```powershell
py -m compileall bin core
py tests/test_ai_init_small.py
py tests/test_ai_state.py
py tests/test_ai_upgrade_large.py
py tests/test_current_capabilities.py
py tests/test_subagent_templates.py
py tests/test_skill_templates.py
py tests/test_examples.py
```

完整回归还包括：

```powershell
py tests/test_ai_review_diff.py
py tests/test_ai_review_spec_plan_final.py
py tests/test_ai_approve_reject_diff.py
py tests/test_ai_approve_reject_all_gates.py
py tests/test_ai_context_handoff.py
py tests/test_cpp_profile_templates.py
py tests/test_e2e_workflow.py
```

无 bash 的 Windows 环境优先运行 Python 测试。Shell 测试仍保留在 `tests/test_ai_init_small.sh`。

## 关键文档

- `AGENTS.md`
- `docs/design/current-capabilities.md`
- `docs/design/reviewed-final-design-v1.md`
- `docs/design/command-contracts.md`
- `docs/design/state-machine.md`
- `docs/design/repo-boundaries.md`
- `docs/design/subagent-packets.md`
- `docs/install-targets.md`
- `docs/usage/generated-target-structure.md`
- `docs/usage/optimization-roadmap.md`
- `skills/README.md`

## 安全边界

- 默认不覆盖已有文件。
- 只有 `--force` 才会覆盖，并且先备份到 `.ai/backups/<timestamp>/`。
- 不创建业务源码目录，例如 `src/`、`include/`、`tests/`。
- 不写入 API key、token、secret。
- 不安装系统依赖。
