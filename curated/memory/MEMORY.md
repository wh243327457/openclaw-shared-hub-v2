# MEMORY.md

这是 **共享中台 v2** 的跨 agent 长期记忆主索引。

## 根路径

- 推荐宿主统一目录：`~/agent/shared`
- 推荐环境变量：`SHARED_HUB_ROOT=$HOME/agent/shared`
- 共享中台本体不是 `runtime/`；`runtime/` 只是共享根内的机器本地临时产物层
- 容器或自定义目录必须显式设置 `SHARED_HUB_ROOT`

## 作用范围

`curated/memory/` 是 **跨 agent 真相源**，只保留稳定、重要、后续大概率还会复用的信息。

- 事实片段：`curated/memory/facts/`
- 项目状态：`curated/memory/projects/`
- 兼容入口：`shared/memory/MEMORY.md`（symlink 到本文件）

## 目录索引

- **长期记忆主索引**：`curated/memory/MEMORY.md`
- **稳定事实**：`curated/memory/facts/`
- **项目状态目录**：`curated/memory/projects/`
- **当前项目条目**：`curated/memory/projects/shared-hub-v2.md`
- **自主学习系统**：`curated/memory/projects/autonomous-learning-system.md`
- **OpenHuman 机制本地化**：`curated/memory/projects/openhuman-mechanism-localization.md`
- **OpenClaw 网页/公众号采集系统**：`curated/memory/projects/openclaw-web-watch.md`
- **Self-Healing Agent / 全局巡查自我修复**：`curated/memory/projects/self-healing-agent.md`
- **Elephant Agent 机制研究与 shared hub v2 反哺**：`curated/memory/projects/elephant-agent-mechanism-study.md`
- **共享技能清单**：`capabilities/manifests/shared-skills.yaml`
- **路径可迁移契约**：`capabilities/skills/foundation/path-portability/SKILL.md`
- **跨机器迁移清单**：`capabilities/skills/foundation/path-portability/references/migration-checklist.md`
- **路径解析器**：`scripts/resolve_shared_root.py`
- **路径可迁移长期事实**：`curated/memory/facts/path-portability.md`
- **治理总结标准**：`docs/shared-governance-standard.md`
- **治理总结机制**：`docs/governance-summary-mechanism.md`
- **配置目标识别规则**：`capabilities/skills/foundation/config-target-routing/SKILL.md`
- **自主学习多 agent 编排模式**：`curated/memory/facts/autonomous-learning-multi-agent-orchestration-patterns.md`
- **Skill-as-contract / Subagent 四状态协议**：`curated/memory/facts/autonomous-learning-skill-as-contract-pattern.md`
- **Agent 工程 Verification-first 实践**：`curated/memory/facts/agent-engineering-verification-first-practices.md`
- **工具链迁移兼容优先原则**：`curated/memory/facts/toolchain-migration-compat-first.md`
- **ds4 推理优化长期事实**：`curated/memory/facts/autonomous-learning-ds4-inference-patterns.md`
- **旧 OpenClaw daily 兼容视图**：`compat/daily/`（可通过 `memory/daily/` 访问）
- **agent 原始写入**：`inbox/<agent>/daily/`
- **个人认知资产库（人类向）**：`/mnt/d/system/selfSystem/`（Obsidian 知识库，面向人类阅读与图谱；
  学习沉淀、读书笔记、调研文档的人类侧归宿。新模型进入先读其根目录 `AGENTS.md`；
  详见 `curated/memory/facts/personal-kb-selfsystem-layout.md`）
- **运行时产物**：`runtime/<agent>/`

## 写入规则

- 只有经过整理和验证的长期信息才进入 `curated/memory/`
- agent 原始记录默认进入 `inbox/<agent>/daily/`
- `.dreams`、cache、index、临时摘要等运行时产物进入 `runtime/<agent>/`
- 避免在本文件中写入明文 secret

## 当前状态

- `shared-hub-v2` 项目状态已沉淀到 `curated/memory/projects/shared-hub-v2.md`
- `capabilities/manifests/shared-skills.yaml` 已建立，用于声明常驻 shared 的共享技能
- `docs/shared-governance-standard.md` 已建立，作为 shared hub 长期筛选、总结、晋升、压缩、淘汰的强制执行标准
- `docs/governance-summary-mechanism.md` 已建立，作为 shared hub 治理总结机制说明入口
- `foundation/config-target-routing` 已升格为共享 skill，用于约束 Hermes / OpenClaw / future-agent 在配置类任务前先识别目标系统，避免混改配置
- `foundation/path-portability` 已升格为共享 skill，用于约束运行时代码通过 `resolve_shared_root.py` 解析宿主根，统一推荐宿主目录 `~/agent/shared`，禁止硬编码机器专属绝对路径；`manifest.yaml: deployment` 段同步建立解析顺序、跨机器搬运最小保留集与 git 忽略规则
- `curated/memory/facts/` 已包含自主学习、多 agent 编排、agent 工程、配置治理、路径可迁移等稳定事实条目
- 后续新增长期记忆时，请同时更新本索引
- `autonomous-learning-system` 已进入 v0.1 骨架落地阶段，正式架构在 `curated/memory/projects/autonomous-learning-system.md`，runtime 配置与模板在 `runtime/hermes/autonomous-learning/`
- 已按用户确认晋升 3 条自主学习长期模式：多 agent 编排、skill-as-contract/subagent 四状态、verification-first agent 工程实践。
- `openhuman-mechanism-localization` 已进入 planned 阶段：将 OpenHuman 的 Memory Tree / Obsidian Wiki / Auto-fetch sync_state / Trigger triage / Token compression 思路本地化到 Hermes + OpenClaw + shared hub v2 + Obsidian 工作流；不依赖 OpenHuman 后端，不复用 GPL 源码，先做 runtime/实验区 POC。
- `self-healing-agent` 已创建 v0.1 runtime 脚手架：定位为全局巡查、自我纠错、自我修复迭代机制；当前只做手动 baseline 和 runtime 产物，不启用 cron、不自动改配置。
- `autonomous-learning-system` 继续吸纳架构参考：OpenSquilla 的 TurnRunner / provider-neutral / skill loader / memory snapshot / sandbox 分层已作为长期观察卡记入项目说明。
- `autonomous-learning-system` 已开始集成 2026-05-19 晋升建议：兼容旧入口优先、本地工具简单入口、HTML 输出面 POC、多数据源统一抽象进入 backlog。

<!-- SHARED-BRIDGE-STATE:START -->
## 自动生成的共享桥状态块

- 生成时间: `2026-09-05T06:00:04+08:00`
- 共享根目录: `/home/vany/agent/shared`
- runtime 位置提示: `/home/vany/agent/shared/runtime`
- facts 文件数: 27
- projects 文件数: 11
- 最近 daily 文件:
  - `inbox/hermes/daily/2026-09-04.md` (inbox/hermes/daily)
  - `inbox/hermes/daily/2026-09-04-github-learning.md` (inbox/hermes/daily)
  - `inbox/hermes/daily/2026-09-03-tutorial-learning.md` (inbox/hermes/daily)
  - `inbox/hermes/daily/2026-09-03-github-learning.md` (inbox/hermes/daily)
  - `inbox/hermes/daily/2026-09-02.md` (inbox/hermes/daily)
- inbox 各 agent 文件计数:
  - `future-agent`: 0
  - `hermes`: 153
  - `openclaw`: 64
<!-- SHARED-BRIDGE-STATE:END -->

## 历史 promoted 归档

- 旧自动 promoted 明细已迁出：`curated/memory/archives/promoted-legacy-2026-05.md`
- 主索引只保留稳定入口和当前状态；长期事实请沉淀到 `facts/` 或 `projects/`。











