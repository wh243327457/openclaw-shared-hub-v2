# 教程学习源扩展计划

- 创建时间：2026-06-09
- 状态：📋 待验证
- 真相源路径：`shared/docs/plans/2026/06/2026-06-09-tutorial-learning-source-expansion.md`

## 目标

在现有 GitHub 学习（每日 07:30）基础上，新增教程学习闭环，每周 2-3 次。

## 教程来源

| 来源 | 优先级 | 原因 |
|------|--------|------|
| GitHub trending repos README/文档 | P0 | 复用已有 OpenClaw 采集 |
| Hacker News / Lobsters 高赞帖 | P1 | 社区筛选质量 |
| YouTube 技术频道 | P2 | 需 transcript 提取 |
| 官方博客/文档更新 | P2 | 可用 blogwatcher 监控 |

## 执行流程

```
OpenClaw 搜索本周高赞教程
  → Hermes 初筛（质量/时效/匹配度）
  → 选 1-2 个深读（Claude Code 复现实验）
  → Hermes 生成最短实践路径
  → 沉淀：inbox → 审计 → curated/runtime
```

## 输出格式

与 GitHub 日报类似，侧重可操作性：
- 教程速览表（来源/难度/耗时/关系）
- 深读：最短实践路径（可复制命令）+ 坑点 + 可沉淀判断

## Cron 安排

| 项目 | GitHub 学习 | 教程学习（新增） |
|------|------------|----------------|
| 频率 | 每天 07:30 | 每周二/四 10:00 |
| Agent | OpenClaw → Hermes 审计 | OpenClaw → Claude Code → Hermes 审计 |
| 输出 | 日报 + 微信推送 | 教程卡 + 微信推送 |
| 深读数 | 2-3 个项目 | 1-2 个教程 |

## 实施步骤

| 步骤 | 状态 | 说明 |
|------|------|------|
| 1. 手动验证流程 | ✅ 已完成 | 2026-06-09，产出首张教程学习卡（Forge + Statewright 深读） |
| 2. 写编排脚本 | ✅ 已完成 | 2026-06-09，`scripts/tutorial_learning_orchestrator.py`，测试通过 |
| 3. 接入 cron | ✅ 已完成 | 2026-06-09，job `765f2f64936e`，每周二/四 10:00，deliver=local,weixin |

## 与现有系统的关系

- 复用 OpenClaw 采集能力
- 复用 Hermes 审计流程
- 复用 shared hub 沉淀机制
- 不影响现有 GitHub 学习 cron
- 符合自主学习系统架构 DAG（§7.3 教程学习 DAG）

## 约束

- 不自动复现高风险实验（需要用户确认）
- 教程来源必须有可访问的原始链接
- 沉淀前必须经过 Hermes 审计
