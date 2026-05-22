---
type: project-state
status: approved_plan_landed
scope: agent-system
source_agent: hermes
created: 2026-05-22
updated: 2026-05-22
sensitivity: low
related:
  - ../../docs/shared-governance-standard.md
  - ../../runtime/hermes/elephant-agent-mechanism-study/iteration-plan.md
---

# Elephant Agent 机制研究与 shared hub v2 反哺

## 稳定判断

Elephant Agent 是一个 Personal-Model-first self-evolving AI agent，其公开资料和源码展示了可借鉴的长期上下文机制：claim-like memory、evidence-backed facts、background reflect、open questions、claim-aware recall、inspectable dashboard。

## 对 shared hub v2 的价值

当前 shared hub v2 已具备 curated / inbox / runtime / capabilities 分层。Elephant Agent 的机制可作为下一步治理增强参考，重点不是引入其 runtime，而是 clean-room 吸收以下模式：

- curated facts 增加 status/confidence/source/evidence_refs。
- raw inbox/runtime 作为 evidence，不直接等同长期真相。
- recall 返回 strong_match / weak_match / no_match，避免过度声称。
- open questions 先落 runtime，用于管理缺口、冲突、过期状态。
- reflect worker 只生成 candidate，不直接写 active curated fact。

## OpenClaw 每日学习/巡检反哺

本次 Elephant Agent 学习方式已被抽象为 OpenClaw 每日学习/巡检的安全增强模式：

1. 深挖对象：项目 / 工具 / 机制 / 故障。
2. 可验证证据：链接、repo、文件、日志、版本、路径。
3. 核心机制：抽象成可迁移模式，而不是罗列功能。
4. 反哺判断：哪些可进入 shared / workflow / skill / runtime POC。
5. 安全边界：哪些不能自动改、不能晋升、不能复用源码。
6. 候选产物：candidate fact / candidate skill / candidate plan / open question。
7. 下一步：低风险 P0、需要用户审核项、验证命令。

安全边界：OpenClaw 只产出候选建议；Hermes 负责二轮审计和是否落库；每日巡检不得自动修复配置或生产问题。

## 当前边界

- 不直接复用 Elephant Agent 源码；仓库 license 不明。
- 不自动写 active curated fact。
- 不迁移旧 facts。
- 不引入 sqlite-vec。
- 不主动推送 open questions。

## 当前产物

- Obsidian 研究入口：`/mnt/d/system/selfSystem/03-学习/技术实践/Elephant Agent 调研档案/00-总览索引.md`
- Obsidian 深度研究：`/mnt/d/system/selfSystem/03-学习/技术实践/Elephant Agent 调研档案/2026-05-22-Elephant-Agent深度研究与机制借鉴.md`
- Obsidian 迭代计划：`/mnt/d/system/selfSystem/03-学习/技术实践/Elephant Agent 调研档案/2026-05-22-Elephant-Agent机制反哺shared体系迭代计划.md`
- Runtime 计划副本：`runtime/hermes/elephant-agent-mechanism-study/iteration-plan.md`
- Runtime 状态：`runtime/hermes/elephant-agent-mechanism-study/state.json`

## 下一步

建议先执行 Phase 0~2：现状基线审计、claim-like schema 草案、evidence-backed promotion 规范。执行前仍需按 shared governance 标准走验证。
