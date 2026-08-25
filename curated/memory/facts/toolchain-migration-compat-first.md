---
fact_id: toolchain-migration-compat-first
status: active
freshness_class: static
scope: shared-hub
subject: toolchain_migration
attribute: compatibility_strategy
value_summary: "Toolchain migrations should keep legacy entrypoints thin and working while moving new writes to canonical paths."
created_at: 2026-05-19T12:30:00+08:00
updated_at: 2026-08-25T12:30:00+08:00
last_verified_at: 2026-08-25T12:30:00+08:00
review_due_at: 2027-02-21
source_refs:
  - /mnt/d/system/selfSystem/03-学习/技术实践/GitHub 热门项目学习档案/每日学习/2026-05-14-GitHub热门项目学习日报.md
  - /mnt/d/system/selfSystem/03-学习/技术实践/GitHub 热门项目学习档案/每日学习/2026-05-19-GitHub热门项目学习日报.md
  - /home/vany/agent/shared/manifest.yaml
  - /home/vany/agent/shared/AGENTS.md
conflict:
  status: none
  type: null
  conflicting_fact_ids: []
  conflicting_candidate_refs: []
  resolution: null
  resolved_by: null
  resolved_at: null
supersedes: []
superseded_by: null
confidence: high
authority: hermes-controller
secret_checked: true
---

# 工具链迁移：兼容旧入口优先

## 事实摘要

当一个新工具链要替换或整合多个旧工具时，优先保留旧入口/旧心智模型，再逐步引导到 canonical 新入口。这个模式适用于 shared hub、Hermes/OpenClaw 配置迁移、CLI 工具替换、skills 目录升格与知识库路径改造。

## 来源与证据

- GitHub 热门项目学习档案 `2026-05-14-GitHub热门项目学习日报.md` 对 `astral-sh/uv` 的观察：`uv pip` 通过兼容 pip 入口降低迁移成本。
- GitHub 热门项目学习档案 `2026-05-19-GitHub热门项目学习日报.md` 的主观复盘：工具链替换要先兼容旧入口。
- shared hub v2 已采用同构做法：
  - `shared/skills -> capabilities/skills`
  - `shared/memory/MEMORY.md -> curated/memory/MEMORY.md`
  - `shared/memory/daily -> compat/daily`

## 可迁移规则

1. **先兼容，再 canonical**：旧入口继续可读/可写一段时间；新写入逐步切到 canonical。
2. **入口薄、真相厚**：兼容层只做 symlink/adapter，不承载新的真相源。
3. **验证旧入口**：每次迁移都要显式测试旧路径仍能解析。
4. **写入分流**：新数据写 canonical；历史/旧 workspace 通过 compat 读取。
5. **人类心智不突变**：命令、路径、输出格式尽量先保留熟悉外观。

## 适用场景

- Hermes / OpenClaw / future-agent 共享 skills 升格。
- shared hub 分层、路径迁移、legacy workspace 兼容。
- Python 工具链从 pip/venv/requirements 迁到 uv。
- 将 Markdown 输出扩展到 HTML、多 surface，但仍保留 Markdown 原始稿。

## 边界

- 兼容层不是长期数据仓库；不得把 runtime/cache/raw bulk 写入 compat 或 curated。
- 旧入口保留不等于允许无限期双写；应有迁移目标和验证脚本。
- 涉及 secret 的配置迁移只引用环境变量名，不写明文密钥。

## 相关文件

- `shared/manifest.yaml`
- `shared/AGENTS.md`
- `shared/curated/memory/facts/shared-hub-v2-structure.md`
- `shared/docs/plans/2026/05/2026-05-19-learning-promotion-integration.md`
