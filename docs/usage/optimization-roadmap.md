# 后续优化方向

## 目标

这份文档记录 `Auto_AICoding_Harness` 当前仓库的后续优化方向。

它不是新的设计定稿，也不扩大当前命令能力边界。它的作用是把已经暴露出来的结构问题、能力落差和下一步优先级整理成可执行路线，方便后续按中等模式逐步推进。

最初判断基于 `v1.6-subagent-packets`，当前已推进到 `v1.7-optimization-hardening`：

- 已有可运行闭环：`ai-init small`、`ai-upgrade large`、review / approve / reject、context-pack、handoff、skill install。
- 当前仓库更接近“流程骨架 + 模板源 + skill 包”，还不是完整自动化多 agent 产品。
- 后续优化重点应该先放在一致性、安装体验、样例、profile 操作性，而不是继续堆新命令。

## 优化原则

1. 先收口，再扩展。
2. 先把现有能力说清楚，再增加新能力。
3. 先保证生成物、文档、测试一致，再考虑正式 CLI 化。
4. 保持 `core` 不绑定 C++ / Linux / CMake 等 profile 策略。
5. 保持 skills 是增强层，不作为命令运行时硬依赖。
6. 保持 subagent 是 prompt / packet / role contract，不实现自动 runner。

## 当前主要问题

### 1. 目录结构有残留和过时说明

`skills/` 中当前公开维护的 skill 集合已经收敛到 `skills/README.md` 和 `tests/test_skill_templates.py` 覆盖的清单，但目录里仍可能存在没有 `SKILL.md` 的旧粒度目录。

这些目录不会被 `ai-install-skills` 安装，但会干扰维护者理解。

需要处理：

- 清理没有 `SKILL.md` 的旧 skill 目录。
- 或者把历史目录移动到明确的 `archive` 区域。
- 更新测试，确保 skill 源目录只有被正式维护的集合。

`scripts/README.md` 也需要更新。现在真实入口已经在 `bin/`，公共逻辑在 `core/`，该文件仍描述早期计划，会造成误导。

### 2. 多平台适配仍主要依赖文档和 prompt

当前仓库声明支持 Codex-first、multi-agent-compatible。

真实实现中：

- `ai-install-skills` 是 Codex 示例安装器。
- Claude Code、GitHub Copilot / VS Code、Generic agent 主要依赖 `docs/install-targets.md` 和 `prompts/bootstrap-local-agent.md`。
- 没有真正的 surface-aware installer。

这是当前设计允许的边界，但后续需要把“文档适配”和“命令适配”的边界说得更明确。

可选方向：

- 保持 `ai-install-skills` 只服务 Codex，并在 README 中写得更直。
- 新增 dry-run 检查命令，输出当前 agent 可用的建议安装目标，但不自动写全局文件。
- 先定义 installer spec，再决定是否实现 Claude / Copilot 的实际安装。

### 3. review / approve / context-pack / handoff 是 scaffold，不是智能审查引擎

当前命令能生成 review artifact、approval artifact、context-pack 和 handoff。

但这些能力主要负责：

- 收集状态。
- 摘录 diff 或源文档。
- 生成 checklist。
- 推进 `.ai/state.json`。

它们不负责自动判断代码是否正确，也不替代 human gate 或 agent review。

后续文档应持续使用 `scaffold`、`gate artifact`、`prompt/context artifact` 这类表述，避免让使用者误解为完整自动审查系统。

### 4. `examples/` 仍是占位目录

`examples/README.md` 声明这里用于展示 small / large / profile overlay 输出，但当前没有稳定金样例。

后续应该补：

- `examples/small/`：`ai-init small` 的代表性输出快照。
- `examples/large/`：`ai-init small` + `ai-upgrade large` 的代表性输出快照。
- 生成样例的说明：样例不是模板源，不参与目标项目运行。

注意：样例一旦提交，就需要有测试或脚本防止和模板源长期漂移。

### 5. profile 层偏知识包，操作性还不够

当前唯一 profile 是 `cpp-linux-backend-system`。

它主要通过 `docs/ai/*` 提供工程知识和检查重点，方向是对的。但如果要让 profile 更有执行价值，还需要补齐：

- profile 的 build / test / check contract。
- profile 推荐的验证矩阵。
- profile 风险触发条件。
- profile 对 `scripts/ai_build.sh`、`scripts/ai_test.sh`、`scripts/ai_check.sh` 的期望说明。

这不意味着把 CMake / ctest / clang-tidy 写进 `core`。这些仍然应该留在 profile overlay 或目标项目脚本中。

### 6. skills 质量需要持续治理

当前 skills 已经从摘要卡片升级为 fuller workflow skills，并引入部分上游原版 skill。

后续还要继续控制三件事：

- 每个 skill 的来源、许可证、改写边界要清楚。
- 直接保留上游原版的 skill 要有测试允许规则。
- adapted workflow skill 不能退化成短摘要。

不建议无限增加 skill。优先保证系统级 methodology skill 和 C++ / Linux 系统工程 skill 的质量。

## 建议执行路线

## 当前落地状态

`v1.7-optimization-hardening` 已完成 P0 到 P4：

- P0：结构收口，旧 skill 残留由测试约束，`scripts/README.md` 已更新为真实边界说明。
- P1：安装体验收口，`ai-install-skills --dry-run` 已实现，安装边界已明确为 Codex 示例安装器。
- P2：稳定样例，`examples/small/` 和 `examples/large/` 已提交并由测试约束。
- P3：profile 操作性增强，`cpp-linux-backend-system` 已生成 `docs/ai/verification-matrix.md`。
- P4：命令体验硬化，`ai-state` 已作为薄的机器可读状态入口实现。

### P0：结构收口

目标：让仓库结构和公开文档一致。

动作：

- 清理无 `SKILL.md` 的旧 skill 残留目录。
- 更新或删除过时的 `scripts/README.md`。
- 检查 `README.md`、`docs/design/current-capabilities.md`、`docs/usage/generated-target-structure.md` 是否仍与当前命令一致。
- 增加结构一致性测试，避免残留目录再次出现。

验收：

- `skills/` 中只有正式维护的 skill 源，或历史内容被明确归档。
- `scripts/README.md` 不再暗示命令实现位于 `scripts/`。
- `py tests/test_skill_templates.py` 通过。
- `py tests/test_current_capabilities.py` 通过。

### P1：安装体验收口

目标：让用户清楚知道哪些安装是自动的，哪些交给本地 agent 自适应。

动作：

- 强化 `docs/install-targets.md`，明确 Codex / Claude / Copilot 的当前支持级别。
- 给 `ai-install-skills` 增加更清晰的输出说明，表明它是 Codex 示例安装器。
- 评估是否增加 `--dry-run`，只列出将安装的 skill 和目标目录。
- 不自动写用户全局 `AGENTS.md`，保持由本地 agent 或用户确认。

验收：

- README 能让用户在 2 分钟内理解安装路径。
- `ai-install-skills` 默认不误导用户以为已经配置 Claude / Copilot。
- 无第三方依赖。

### P2：提交稳定样例

目标：让用户能直接看见初始化后的目标项目长什么样。

动作：

- 生成并提交 `examples/small/`。
- 生成并提交 `examples/large/`。
- 增加轻量测试，确认样例结构与模板关键文件一致。
- 明确样例不是模板源，模板源仍然只有 `templates/` 和 `profiles/`。

验收：

- 新用户不用运行命令也能理解输出结构。
- 样例不会和模板源长期漂移。
- `.ai/backups/`、临时状态、测试运行产物不进入样例。

### P3：profile 操作性增强

目标：让 `cpp-linux-backend-system` 不只是知识文档，而是能指导实际验证。

动作：

- 补充 profile 级验证矩阵。
- 明确 C++ / Linux / backend / system 场景下的风险触发条件。
- 让 `docs/ai/build.md`、`docs/ai/testing.md`、`docs/ai/cmake.md` 和脚本占位说明更一致。
- 保持目标项目自己决定具体命令，不把工具链硬编码进 `core`。

验收：

- 目标项目生成后，agent 能知道什么时候该跑 build、test、check、sanitizer、benchmark。
- profile 文档不重写 state machine。
- profile 文档不绕过 review gate。

### P4：命令体验硬化

目标：让现有命令更稳定，但不扩大命令集合。

动作：

- 统一错误信息风格。
- 统一退出码说明。
- 检查 `--force`、backup、skip 输出在所有命令中的一致性。
- 考虑实现设计中保留的 `ai-state`，但只有在确实需要机器可读状态入口时才做。

验收：

- 正常路径返回 `0`。
- 参数错误返回 `2`。
- 状态、文件系统、git 前置条件错误返回 `1`。
- 所有写文件路径仍走 safe write 或等价保护。

## 暂不做

这些不是当前优先级：

- 自动 subagent runner。
- 自动拉取第三方 skills。
- 多 profile 市场化能力。
- 正式包管理发布。
- 把 Claude / Copilot 做成完整硬编码安装器。
- 把 CMake / ctest / clang-tidy 写进 `core`。
- 用 skills 替代 review gate 或 `.ai/state.json`。

## 推荐下一步

P0 到 P4 已在 `v1.7-optimization-hardening` 中落地。

后续最适合继续做两类工作：

- 根据真实业务仓库使用反馈，调整 `docs/ai/*` 和 profile 验证矩阵。
- 在不引入自动 runner 的前提下，继续打磨 subagent packet 和 role templates。

仍建议保持任务契约：

- 执行等级：Level 2 或 Level 3。
- 目标：围绕一个真实目标项目验证 harness 是否降低 AI coding 风险。
- 文件范围：目标项目生成文件、profile docs、必要的 harness 文档。
- 验证：完整 Python 回归和一次真实目标项目初始化 / 升级演练。
