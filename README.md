# Auto_AICoding_Harness

面向本地 AI Coding Agent 的工程工作流脚手架。

这个仓库不是业务项目，而是一个 Harness 源仓库：它提供命令、模板、skills、全局指令样板和设计文档，用来把稳定的 AI Coding 流程注入到其他目标项目中。

当前优先服务我们自己的 `C++ / Linux / 后端 / 系统工程` 场景。

## 适合什么

- 给 Codex / Claude Code / GitHub Copilot 等本地 agent 提供统一项目入口。
- 在目标项目中生成 `AGENTS.md`、`docs/ai/`、`.ai/`、检查脚本和 review gate 骨架。
- 把常用 AI coding 方法论沉淀成全局 skills。
- 根据任务复杂度在轻量流程和 large mode 流程之间切换。

## 用户使用场景

- 你有自己的本地 agent，但希望它在不同项目里都按同一套工程习惯做事，而不是每次从零约束。
- 你接手一个已有仓库，想先把任务分级、验证方式、handoff 方式和 review gate 统一下来，再让 agent 开始干活。
- 你希望复杂任务不再只靠一段聊天推进，而是有 `spec / plan / review / verification / handoff` 这些可落地的项目内文件。
- 你想让 subagent 协作更可控，至少把角色、skills、scope、expected output 记录清楚，而不是只写一句“你去看一下”。

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
py bin/ai-install-skills --scope system
py bin/ai-install-skills --profile cpp-linux-backend-system
py bin/ai-init small
py bin/ai-init medium
py bin/ai-upgrade medium
py bin/ai-upgrade large
py bin/ai-doctor
py bin/ai-dispatch planner --scope "docs/design/*" --objective "plan bounded hardening" --expected-output "plan + risks" --result-location ".ai/run-trace.md"
py bin/ai-state
```

类 Unix:

```bash
python3 bin/ai-status
python3 bin/ai-install-skills
python3 bin/ai-install-skills --dry-run
python3 bin/ai-install-skills --scope system
python3 bin/ai-install-skills --profile cpp-linux-backend-system
python3 bin/ai-init small
python3 bin/ai-init medium
python3 bin/ai-upgrade medium
python3 bin/ai-upgrade large
python3 bin/ai-doctor
python3 bin/ai-dispatch planner --scope "docs/design/*" --objective "plan bounded hardening" --expected-output "plan + risks" --result-location ".ai/run-trace.md"
python3 bin/ai-state
```

如果脚本有执行权限，也可以直接运行：

```bash
bin/ai-status
bin/ai-init small
bin/ai-init medium
```

## 拉库后先对本地 Agent 说什么

如果你刚把仓库拉下来，最省事的做法不是自己手工翻目录，而是先让本地 agent 做一次“本地化适配”。

可以直接把下面这段话发给它：

```text
你现在把这个仓库当作 AI coding harness 源仓库来接入你自己。

先阅读：
- README.md
- docs/install-targets.md
- prompts/bootstrap-local-agent.md
- global/AGENTS.md.template
- skills/README.md

然后只按你当前真实支持的环境做本地化适配：
- 识别你现在是 Codex、Claude Code、GitHub Copilot / VS Code，还是别的本地 agent
- 只安装你真正能消费的全局指令和 skills
- 不要静默覆盖已有配置；如果目标文件已存在，先给出 diff、dry-run 或备份方案

最后告诉我：
- 你安装了哪些文件
- 跳过了哪些文件
- 还需要我做什么重启、reload 或手工确认
```

如果你已经进入某个业务项目，想把这套流程注入进去，可以再对 agent 说：

```text
把当前项目接入 Auto_AICoding_Harness 工作流。

先检查项目根目录是否已经有 AGENTS.md、docs/ai/ 和 .ai/state.json。
如果还没有，按仓库说明执行 ai-init small。
如果已经存在，就先读取现有 AGENTS.md 和 docs/ai/*，不要覆盖用户已有约束。

然后告诉我：
- 当前项目是否已接入
- 下一步应该保持 small mode，还是建议升级 large mode
- 如果升级，原因是什么
```

## 推荐使用流程

1. 拉取本仓库。
2. 让本地 agent 阅读 `README.md`、`AGENTS.md`、`docs/install-targets.md` 和 `prompts/bootstrap-local-agent.md`。
3. 执行 `ai-install-skills`，把仓库内 skills 安装到当前 agent 支持的位置。
4. 在目标项目根目录执行 `ai-init small` 或 `ai-init medium`。
5. 普通任务保持 small mode；多文件但边界清晰的任务可以直接用 medium。
6. 复杂任务执行 `ai-upgrade large`，启用 spec / plan / review / approval / handoff 骨架。
7. 如果真的要派发 subagent，先运行 `ai-dispatch`，把角色包里的 skill 显式展开并记录进 `.ai/run-trace.md`。
8. 用 `ai-status` 查看当前状态和 next action；怀疑状态不一致时运行 `ai-doctor`。

## 什么时候升级到 Large Mode

保持 `small` 就够的情况：

- 修一个局部 bug。
- 改一个脚本、prompt、配置或少量文档。
- 回滚成本低，当前会话里能很快验证。

建议用 `medium` 的情况：

- 任务跨多个文件，但仍在一个边界清晰的工作流内。
- 你需要显式 plan、run trace、verification，但不需要完整 spec gate。
- 你希望保留 reviewer/tester 协作空间，但不想进入 full large ceremony。

建议升级到 `large` 的情况：

- 任务已经跨模块、跨流程，或者会影响共享接口。
- 你需要先写 `spec` 和 `plan`，不想让 agent 直接边想边改。
- 任务可能跨多个 session，需要 `context-pack`、`handoff`、`verification` 这些运行痕迹。
- 你准备做显式 review gate，或者确实要做带角色边界的 subagent 协作。

一句话判断：

- “直接改，改完很快就能验” -> 多半继续 `small`
- “需要先控范围、留痕、分阶段审” -> 升到 `large`

## 当前能力

当前基线：`v1.7-optimization-hardening`。

已实现命令：

- `ai-install-skills`
- `ai-install-skills --list / --scope / --profile`
- `ai-init small`
- `ai-init medium`
- `ai-upgrade medium`
- `ai-upgrade large`
- `ai-doctor`
- `ai-status`
- `ai-state`
- `ai-dispatch`
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
- `docs/ai/workflow.md`
- `docs/ai/verification-matrix.md`
- `scripts/ai_build.sh`
- `scripts/ai_test.sh`
- `scripts/ai_check.sh`
- `.ai/state.json`
- `.ai/templates/`

`ai-init medium` 在 `small` 基础上额外生成：

- `.ai/implementation-plan.md`
- `.ai/run-trace.md`
- `.ai/verification.md`

`ai-upgrade large` 追加：

- `.ai/epic.md`
- `.ai/spec.md`
- `.ai/tech-design.md`
- `.ai/scope.md`
- `.ai/implementation-plan.md`
- `.ai/affected-files.md`
- `.ai/run-trace.md`
- `.ai/verification.md`
- `.ai/risk-and-rollback.md`
- `.ai/evaluation.md`
- `.ai/reviews/`
- `.ai/approvals/`
- `.ai/subagent-packets/`
- `.codex/agents/`
- `docs/ai/tasks/README.md`
- `docs/ai/tasks/<task-id>/00-prd.md`
- `docs/ai/tasks/<task-id>/01-spec.md`
- `docs/ai/tasks/<task-id>/02-tech-design.md`
- `docs/ai/tasks/<task-id>/03-implementation-plan.md`
- `docs/ai/tasks/<task-id>/04-diff-review.md`
- `docs/ai/tasks/<task-id>/05-verification.md`
- `docs/ai/tasks/<task-id>/06-risk-and-rollback.md`
- `docs/ai/tasks/<task-id>/07-handoff.md`

`.ai/subagent-packets/` 是角色任务包模板，用来把任务目标、上下文、建议 skills、禁止事项和返回格式传给本地 agent 或 subagent。它不是自动执行器。

`ai-dispatch` 是一个薄记录助手：它只会在 large mode 下读取对应角色包里的 `Required Skills` / `Optional Skills`，然后把标准 dispatch 记录追加到 `.ai/run-trace.md`。它不会启动 subagent，也不会推进状态。

`ai-doctor` 用于检查 `.ai/state.json`、medium/large 生成物和明显的 only-talk / mode mismatch 问题。`ai-status` 负责展示当前状态，`ai-doctor` 负责诊断异常。

large mode 现在会把主证据链同步到 `docs/ai/tasks/<task-id>/`。`.ai/` 仍然保留为运行时主工作区，`docs/ai/tasks/<task-id>/` 则提供更稳定、可审计、可交接的任务文档链。

## Skills

仓库级 skills 位于 `skills/`，不会自动生成到目标项目。

当前分类：

- `skills/methodology/`：任务分级、上下文工程、调试、review、验证、skill 创建等方法论。
- `skills/system/`：C++ / Linux / 系统工程、安全 review、性能分析。

安装到 Codex 示例位置：

```powershell
py bin/ai-install-skills --dry-run
py bin/ai-install-skills
py bin/ai-install-skills --scope system
py bin/ai-install-skills --profile cpp-linux-backend-system
py bin/ai-install-skills --list --scope system
py bin/ai-install-skills --force
```

`ai-install-skills` 是 Codex 示例安装器。它基于每个 skill 目录下的 `skill.yaml` 选择默认 subset，并支持 `--scope system`、`--profile cpp-linux-backend-system` 和 `--list`。其他 agent 的安装位置参考 `docs/install-targets.md` 和 `prompts/bootstrap-local-agent.md`。

`cpp-linux-backend-system` 现在同时包含 `profile.yaml` 元数据。`ai-init`、`ai-upgrade` 和 `ai-install-skills --profile ...` 会先校验这个 manifest，再应用对应 overlay 或 skill 过滤。

## 仓库结构

- `bin/`：用户直接执行的命令入口。
- `core/`：safe write、模板展开、state、review、approval、context、skill install 等公共逻辑。
- `templates/`：生成目标项目文件的唯一模板源。
- `system/`：系统层全局行为源，例如 `AGENTS.global.md`。
- `profiles/`：profile overlay，目前主 profile 是 `cpp-linux-backend-system`。
- `profiles/<name>/profile.yaml`：profile 元数据入口，描述语言、领域、risk triggers 和 verification 策略。
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
