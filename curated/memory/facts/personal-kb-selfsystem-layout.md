---
fact_id: personal-kb-selfsystem-layout
status: active
freshness_class: slow_changing
scope: cross-agent
subject: personal-knowledge-base
attribute: directory-layout-and-boundary
value_summary: "个人认知资产库 selfSystem 位于 /mnt/d/system/selfSystem，Obsidian 结构，面向人类阅读；与共享中台通过 AGENTS.md 互指，学习沉淀的人类侧归宿"
created_at: 2026-08-24
updated_at: 2026-08-24
last_verified_at: 2026-08-24
review_due_at: 2026-11-24
source_refs:
  - /mnt/d/system/selfSystem/AGENTS.md
  - /mnt/d/system/selfSystem/99-索引/01-知识库写作与维护规范.md
conflict: null
supersedes: null
superseded_by: null
confidence: high
authority: hermes-kb-integration
secret_checked: true
---

# 个人认知资产库 selfSystem 布局与边界

## 核心内容

- 位置：Windows 盘 `/mnt/d/system/selfSystem`（即 `D:\system\selfSystem`）
- 性质：Obsidian 知识库（含 wiki-link 图谱），**面向人类阅读**，不是 agent 运行记忆
- 新模型进入必读：根目录 `AGENTS.md` → `99-索引/01-知识库写作与维护规范.md` → `99-索引/00-知识库总览.md`
- 一级目录固定为：01-个人成长 / 02-工作 / 03-学习 / 04-日常 / 05-探索复利系统 / 06-知识合成引擎 / 90-工具 / 90-资料库 / 99-索引，不得新建一级目录
- 不确定归属的内容先放 `05-探索复利系统/01-输入与收件箱/`
- 模型接入包在 `05-探索复利系统/05-模型接入包/`，是接手指南的真相源

## 与共享中台的分工

| 维度 | shared hub (`~/agent/shared`) | selfSystem |
|------|------|------|
| 读者 | agent（Hermes/OpenClaw/future） | 人类 + 所有模型的阅读视图 |
| 内容 | 运行记忆、facts/projects、cron 状态、流水线产物 | 学习沉淀、读书笔记、调研文档、认知提炼 |
| 写入 | 按 AGENTS.md 分层规则 | 按其写作规范（frontmatter + wiki-link） |

- 学习类流水线（GitHub 热门项目、读书计划、教程学习）的机器产物在 shared runtime，
  面向人类的最终沉淀（每日学习日报、项目卡片）落在
  `selfSystem/03-学习/技术实践/GitHub 热门项目学习档案/`
- 调研/学习文档默认落盘到 selfSystem 时按 Obsidian 风格组织（frontmatter + 双链）
