# Auto_AICoding_Harness

面向本地 AI Coding Agent 的工程工作流脚手架。

它不是业务项目，也不是自动执行器；它是一个 Harness 源仓库，负责提供命令、模板、skills、全局指令样板和设计文档，用来把稳定的 AI Coding 流程注入到其他目标项目中。

当前优先服务我们自己的 `C++ / Linux / 后端 / 系统工程` 场景。

## 一句话理解

- 这是“给 agent 用的工程工作流源仓库”，不是业务代码仓库。
- `templates/` 和 `profiles/` 负责生成目标项目骨架。
- `small / medium / large` 是同一条工作流的不同控制强度。
- `large mode` 强化 plan / review / verification / handoff，但不等于自动 subagent execution。
- 所有模式都先做一次 requirement clarification pass；如果仍有歧义，再提 targeted questions。

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

## 真实开发场景与建议 Prompt

下面这些场景更贴近真实研发环境，不是抽象 demo。每条都给一个建议模式和可以直接复制给本地 agent 的 prompt。

为了让 prompt 真正落地，建议尽量写清这 5 件事：

- 指定模式：`small / medium / large`
- 指定必须运行的脚本或命令
- 指定优先使用的 skill
- 指定是否真的要开启 subagent / 多 agent
- 指定输出物写到哪里，例如 `.ai/implementation-plan.md`、`.ai/run-trace.md`、`.ai/verification.md`

### 场景 1：刚接手一个已有 C++ / Linux 后端仓库

典型环境：

- 代码库已经在线上跑。
- 使用 `CMake`、`ctest`、shell 脚本或自定义部署脚本。
- 你还不知道入口、模块边界、关键风险点。

建议模式：

- 先 `small` 或 `medium`
- 不要一上来就 `large`

建议 prompt：

```text
先不要改代码。把当前仓库当作一个你刚接手的 C++ / Linux 后端项目。

先运行：
- ai-status
- 如果仓库还没接入 harness，再判断是否需要 ai-init small 或 ai-init medium

优先使用这些 skill：
- repo-onboarding-analysis
- context-engineering
- task-router
- task-contract-and-leveling

先做 repo onboarding：
- 阅读 README、AGENTS.md、docs、构建脚本和主入口
- 识别主要模块、构建方式、测试方式、风险目录
- 告诉我哪些目录是业务核心，哪些是工具层
- 判断当前项目更适合先接入 ai-init small 还是 ai-init medium，并说明原因

输出要求：
- 一份简洁的架构地图
- 建议的接入模式
- 第一批不该乱动的高风险文件
```

### 场景 2：修一个真实线上 bug，但范围还比较局部

典型环境：

- 有报错日志、core 信息、告警截图或复现步骤。
- 问题大概率在单模块或单条调用链。
- 你想先修复并快速验证，不想把流程搞得太重。

建议模式：

- `small`
- 如果排查中变成多文件联动，再升级 `medium`

建议 prompt：

```text
现在按 small mode 处理这个 bug。

先运行：
- ai-status
- 如果仓库还没接入 harness，就执行 ai-init small

优先使用这些 skill：
- systematic-debugging
- karpathy-guidelines
- verification-before-completion

目标：
- 先复现或定位问题
- 只在必要文件里做最小修改
- 改完后给出明确验证步骤

要求：
- 先告诉我你认为最可能的调用链
- 不要先做大重构
- 如果排查过程中发现影响范围已经跨多个模块，暂停并说明为什么应升级到 medium
```

### 场景 3：要做一个跨模块需求，涉及接口、状态流或数据结构

典型环境：

- 改动可能跨 `api / service / storage / worker / script`。
- 可能影响共享结构、协议、任务流转或多种验证路径。
- 这种任务最容易“边改边漂”。

建议模式：

- 直接 `large`

建议 prompt：

```text
现在进入 large mode，处理这个跨模块需求。

必须先运行：
- ai-status
- 如果当前不是 large，就执行 ai-upgrade large
- 然后按顺序准备 ai-review spec 和 ai-review plan 需要的材料

优先使用这些 skill：
- task-router
- planning-and-task-breakdown
- context-engineering
- verification-before-completion
- 如果涉及 C++ / Linux 后端，再加 cpp-linux-system-engineering

先不要直接改代码，先完成：
- scope 梳理
- spec
- tech design
- implementation plan

要求：
- 明确列出会受影响的模块和文件范围
- 明确哪些接口或状态流可能被破坏
- 给出分阶段验证方案
- 在我没有看到 plan 之前，不要直接进入大面积实现
```

### 场景 4：你明确想要多 agent / subagent 编排

典型环境：

- 任务很大，但写入范围可以拆开。
- 你希望主 agent 统筹，子 agent 分别做扫描、方案、实现、CR 或验证。
- 你不想再出现“虽然说了 large mode，但没有真的开 subagent”的歧义。

建议模式：

- `large`
- prompt 里显式写 `多agent编排 / subagent / delegation / 主 agent 统筹`

建议 prompt：

```text
现在进入 large mode，并进行多agent编排。

必须先运行：
- ai-status
- 如果当前不是 large，就执行 ai-upgrade large
- 在真实分派前运行 ai-dispatch，至少先记录 planner 角色

优先使用这些 skill：
- planner: task-router, task-contract-and-leveling, planning-and-task-breakdown
- explorer: context-engineering, systematic-debugging
- implementer: karpathy-guidelines, verification-before-completion
- reviewer: code-review-and-quality
- evaluator: verification-before-completion, performance-analysis

要求：
- 主 agent 只负责统筹全局、划分 write scope、汇总结果
- 如需 subagent，请按 planner / explorer / implementer / reviewer / evaluator 这类角色拆分
- 每个 subagent 只能处理自己负责的边界，不要重复改同一批文件
- 在开始实现前，先告诉我这次是否真的会使用 subagent；如果不用，也要解释原因

目标输出：
- 总体计划
- 子任务划分
- 验证与汇总方式
```

### 场景 4B：你只想在 medium 里做轻量多 subagent 协作

典型环境：

- 任务是多文件但边界还算清晰。
- 你想让 scanner / reviewer 参与，但不想上 full large gate chain。
- 你接受手工协调，不要求 large 的 `ai-dispatch` 辅助。

建议模式：

- `medium`
- 可做 bounded subagent coordination
- 当前 harness 的内建 `ai-dispatch` 仍然是 `large`-only

建议 prompt：

```text
现在按 medium mode 处理这个任务，并开启轻量多 subagent 协作。

必须先运行：
- ai-status
- 如果仓库还没进入 medium，就执行 ai-init medium 或 ai-upgrade medium

优先使用这些 skill：
- task-router
- planning-and-task-breakdown
- context-engineering
- code-review-and-quality
- verification-before-completion

要求：
- 主 agent 先给出 implementation-plan
- 如果平台支持 subagent，可以让 scanner / reviewer 分别并行做探索和 CR
- 由于当前 harness 的 ai-dispatch 是 large-only，所以 medium 下的 subagent 协作要手工记录到 .ai/run-trace.md
- 不要伪造 large 的 spec gate

输出：
- .ai/implementation-plan.md
- .ai/run-trace.md
- .ai/verification.md
```

### 场景 5：准备合并一个复杂分支，想先做高质量 CR 和回归检查

典型环境：

- 功能已经有人写完，或者你自己已经改完。
- 你现在最关心的是回归风险、遗漏测试、边界条件和状态机问题。
- 这类任务更像 review / hardening，而不是从零实现。

建议模式：

- 已经是 `large` 就继续 `large`
- 否则至少 `medium`

建议 prompt：

```text
先不要继续开发，把当前改动当作待合并分支做一次严格 review。

先运行：
- ai-status
- 如果当前任务还没有 verification 记录，提醒我补 .ai/verification.md

优先使用这些 skill：
- code-review-and-quality
- verification-before-completion
- security-review
- 如果是 C++ / Linux 服务，再加 cpp-linux-system-engineering

要求：
- 先看 diff 和受影响文件
- 重点找行为回归、状态流错误、漏测、边界条件和不一致的文档/脚本
- 按严重程度输出 findings
- 如果你认为当前验证不够，明确告诉我还缺哪些测试或手工检查

不要把输出写成泛泛总结，优先给我真正会出问题的点
```

### 场景 6：任务跨多天推进，需要可交接、可恢复上下文

典型环境：

- 今天只能做一部分，明天或下周继续。
- 可能换人继续，也可能是你自己下次再接着做。
- 最怕“下次回来只剩聊天记录，没有结构化上下文”。

建议模式：

- `medium` 或 `large`
- 需要显式维护 `run-trace / verification / handoff`

建议 prompt：

```text
这个任务会跨多个 session 推进。

先运行：
- ai-status
- 如果是 medium，就保持 implementation-plan / run-trace / verification 最新
- 如果是 large，在阶段结束前运行 ai-context-pack 和 ai-handoff

优先使用这些 skill：
- context-engineering
- planning-and-task-breakdown
- verification-before-completion

要求：
- 在执行过程中持续维护 implementation-plan、run-trace、verification
- 每做完一个阶段，都补充当前状态、未完成项、风险和下一步
- 在本轮结束前生成可交接的 handoff

目标：
- 让我下次回来时，不需要重新读完整聊天记录也能继续
```

### 场景 7：把这套 harness 真正注入一个已有业务仓库

典型环境：

- 业务仓库已经有自己的 `README`、脚本、目录约束。
- 你希望引入 `AGENTS.md`、`docs/ai/`、`.ai/`，但不想破坏已有结构。
- 这是最典型的真实接入场景。

建议模式：

- 先 `small`
- 如果发现要补 plan / verification / 多阶段 review，再升级 `medium` 或 `large`

建议 prompt：

```text
把当前业务仓库接入 Auto_AICoding_Harness，但不要破坏已有工程结构。

必须先运行：
- ai-status
- 如果当前仓库还没接入，再判断 ai-init small 还是 ai-init medium

优先使用这些 skill：
- repo-onboarding-analysis
- context-engineering
- task-router

先做：
- 检查是否已有 AGENTS.md、CLAUDE.md、docs/ai/、.ai/state.json
- 识别现有 README、脚本、测试和目录约束
- 判断应该 ai-init small 还是 ai-init medium

要求：
- 不要覆盖用户已有文件
- 如果需要 --force，先解释为什么
- 告诉我接入后会新增什么、不会动什么、潜在冲突点是什么
```

## 多会话接力示例

这个仓库当前没有“自动在 80% 上下文时强制切会话”的能力，但可以把它作为明确的操作启发式。

推荐规则：

- 当你感觉当前会话已经接近上下文上限，或者重要背景已经很多、继续往下会丢细节时，就把它视为“接近 80%”
- 在这个点上，不要硬撑到最后；优先做一次 `context-pack + handoff`

一个实际可复制的接力流程：

1. 当前会话中推进任务，持续更新 `.ai/implementation-plan.md`、`.ai/run-trace.md`、`.ai/verification.md`。
2. 当你判断上下文已经接近 80%，先运行：
   - `ai-context-pack`
   - `ai-handoff`
3. 检查 `.ai/context-pack.md` 和 `.ai/handoff.md` 是否已经包含：
   - 当前 mode / status
   - 已完成阶段
   - 未完成项
   - 验证结果
   - 下一步建议
4. 开一个新会话，把新 prompt 明确写成“先读 handoff，再继续”，而不是重新从头分析。

建议 prompt：

```text
当前会话的上下文已经接近上限。先不要继续扩写。

请先运行：
- ai-context-pack
- ai-handoff

然后基于 .ai/context-pack.md 和 .ai/handoff.md，总结：
- 当前任务已经完成到哪一步
- 哪些结论已经确认
- 哪些风险和未完成项必须继承到下一会话

接着为下一会话生成一个最小 continuation prompt。
```

新会话建议 prompt：

```text
这是一个接力会话。不要重新从零分析。

先阅读：
- .ai/context-pack.md
- .ai/handoff.md
- .ai/implementation-plan.md
- .ai/verification.md

然后告诉我：
- 你理解的当前状态
- 下一步最应该做什么
- 是否需要继续保持当前 mode，还是升级 / 降级

如果是 large mode，继续沿用已有 spec / plan / review / verification 链，不要重建一套平行文档。
```

## 实际使用效果示例

下面是这个仓库自己一次真实 large-mode 改动的效果，不是虚构案例。

任务背景：

- 目标：把 `Auto_AICoding_Harness` 从早期优化状态继续收口，补齐 `medium` 支持、large 任务证据链、profile manifest、examples、README 和一致性测试。
- 范围：`bin/`、`core/`、`schemas/`、`templates/`、`examples/`、`docs/`、`tests/` 多处联动。
- 风险：如果没有 large mode，很容易出现“文档改了、模板没改、测试没补、样例不同步”的漂移。

这次 large mode 的实际成效：

- 明确把任务拆成多阶段：`medium` 能力落地、large task chain、profile metadata、examples 收口、README 优化。
- 在 large 模式下把证据链同步到 `docs/ai/tasks/<task-id>/`，让任务不只停留在运行时文件里。
- 通过 `run-trace / verification / handoff` 让长任务可以跨多个阶段推进，而不是只靠聊天历史。
- 最终回归达到 `141` 个测试通过，说明这套流程对“多文件、多文档、多测试联动优化”是有效的。

如果把这个案例翻成一个实战 prompt，可以这样写：

```text
现在进入 large mode，目标是做一次跨命令、跨模板、跨文档、跨测试的整体优化。

必须先运行：
- ai-status
- 如果当前不是 large，就执行 ai-upgrade large

优先使用这些 skill：
- task-router
- planning-and-task-breakdown
- context-engineering
- verification-before-completion
- code-review-and-quality

要求：
- 先做分阶段计划，不要直接散改
- 每完成一块，都同步文档、样例和测试
- 在需要跨会话时运行 ai-context-pack 和 ai-handoff
- 最后必须给出真实回归结果，而不是只说“理论上可行”
```

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
py bin/ai-install-skills --dry-run
py bin/ai-install-skills
py bin/ai-init small
py bin/ai-init medium
py bin/ai-upgrade medium
py bin/ai-upgrade large
py bin/ai-doctor
py bin/ai-state
```

类 Unix:

```bash
python3 bin/ai-status
python3 bin/ai-install-skills --dry-run
python3 bin/ai-install-skills
python3 bin/ai-init small
python3 bin/ai-init medium
python3 bin/ai-upgrade medium
python3 bin/ai-upgrade large
python3 bin/ai-doctor
python3 bin/ai-state
```

如果脚本有执行权限，也可以直接运行：

```bash
bin/ai-status
bin/ai-init small
bin/ai-init medium
```

## 推荐使用流程

1. 拉取本仓库。
2. 让本地 agent 阅读 `README.md`、`AGENTS.md`、`docs/install-targets.md` 和 `prompts/bootstrap-local-agent.md`。
3. 先做一次 requirement clarification pass：明确目标、范围、约束和验证方式；如果仍有歧义，再提 targeted questions，除非用户明确说不要问。
4. 执行 `ai-install-skills`，把仓库内 skills 安装到当前 agent 支持的位置。
5. 在目标项目根目录执行 `ai-init small` 或 `ai-init medium`。
6. 普通任务保持 small mode；多文件但边界清晰的任务可以直接用 medium。
7. 复杂任务执行 `ai-upgrade large`，启用 spec / plan / review / approval / handoff 骨架。
8. 如果真的要派发 subagent，先运行 `ai-dispatch`，把角色包里的 skill 显式展开并记录进 `.ai/run-trace.md`。
9. 用 `ai-status` 查看当前状态和 next action；怀疑状态不一致时运行 `ai-doctor`。

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

这部分应和 [docs/install-targets.md](/C:/Users/26561/Documents/Auto_AICoding_Harness/docs/install-targets.md) 与 [prompts/bootstrap-local-agent.md](/C:/Users/26561/Documents/Auto_AICoding_Harness/prompts/bootstrap-local-agent.md) 保持同步。

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

补充规则：

- `large mode = 强流程`
- `large mode + 多 agent / subagent / delegation / 并行编排 / 主 agent 统筹 = 强流程 + 多 agent 编排`

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
- `examples/`：small / large 快照与注入前后对照样例。

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
