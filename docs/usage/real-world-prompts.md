# Real-World Prompt Patterns

This page keeps longer prompt patterns out of the root `README.md` while preserving copy-ready usage examples.

## How To Use These Prompts

Before sending any prompt to an agent, choose the control strength first:

- `small`: local change, low ceremony, quick verification.
- `medium`: multi-file but bounded change, explicit plan / trace / verification.
- `large`: cross-module or high-risk work that needs spec / plan / review / approval / handoff.

Useful prompt ingredients:

- mode: `small / medium / large`
- commands to run first
- preferred skills or review focus
- whether subagent coordination is expected
- where to write artifacts, such as `.ai/implementation-plan.md`, `.ai/run-trace.md`, and `.ai/verification.md`

## Scenario 1: Onboard An Existing C++ / Linux Backend

Recommended mode: start with `small` or `medium`.

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

## Scenario 2: Fix A Local Production Bug

Recommended mode: `small`, upgrade to `medium` if the investigation crosses module boundaries.

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

## Scenario 3: Implement A Cross-Module Change

Recommended mode: `large`.

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

## Scenario 4: Large Mode With Explicit Subagent Coordination

Recommended mode: `large` with explicit multi-agent wording.

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

## Scenario 5: Medium Mode With Lightweight Subagent Help

Recommended mode: `medium`.

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

## Scenario 6: Review A Complex Branch Before Merge

Recommended mode: existing `large`, otherwise at least `medium`.

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

## Scenario 7: Continue Across Sessions

Recommended mode: `medium` or `large`.

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

## Scenario 8: Inject Harness Into A Real Project

Recommended mode: start with `small`.

```text
把当前业务仓库接入 Auto_AICoding_Harness 工作流，但不要破坏已有工程结构。

先检查项目根目录是否已经有 AGENTS.md、docs/ai/ 和 .ai/state.json。
如果还没有，按仓库说明执行 ai-init small。
如果已经存在，就先读取现有 AGENTS.md 和 docs/ai/*，不要覆盖用户已有约束。

然后告诉我：
- 当前项目是否已接入
- 下一步应该保持 small mode，还是建议升级 large mode
- 如果升级，原因是什么
```

## Session Handoff Prompt

Use this when context is getting too large:

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

Use this in the next session:

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
