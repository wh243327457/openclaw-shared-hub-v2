# shared-hub-v2

## 项目概览

- 状态：黄 / 在轨
- 当前阶段：共享 skill 治理与校验闭环已落地，正在做最终同步与后续收口
- 最近整理时间：`2026-04-15T11:00:27+08:00`
- 当前完成度：约 `88%`

## 人话结论

共享中台 v2 的**本地结构、兼容桥和共享 skill 治理都已经落地**，Hermes / OpenClaw 的关键引用也已通过脚本校验。
当前还没完全收口的部分，不是“桥接坏了”，而是**远端 PR / 仓库同步、后续持续沉淀 facts/projects、以及让更多共享技能进入 shared 清单**还没跟上。

## 已确认完成

### 1. canonical 分层已在本地落地
以下目录 / 文件均已存在：

- `manifest.yaml`
- `AGENTS.md`
- `README.md`
- `curated/memory/MEMORY.md`
- `curated/memory/facts/`
- `curated/memory/projects/`
- `inbox/hermes/daily/`
- `inbox/openclaw/daily/`
- `inbox/future-agent/daily/`
- `runtime/hermes/`
- `runtime/openclaw/`
- `runtime/openclaw/dreams/`
- `runtime/future-agent/`
- `capabilities/skills/`
- `capabilities/manifests/`
- `capabilities/versions/`
- `compat/daily/`
- `prefill/hermes-shared-memory.json`

### 2. legacy 兼容链路已正确建立
以下兼容入口已实际指向 v2 规范位置：

- `shared/skills -> shared/capabilities/skills`
- `shared/memory/MEMORY.md -> shared/curated/memory/MEMORY.md`
- `shared/memory/facts -> shared/curated/memory/facts`
- `shared/memory/projects -> shared/curated/memory/projects`
- `shared/memory/daily -> shared/compat/daily`
- `shared/compat/daily/.dreams -> shared/runtime/openclaw/dreams`

### 3. 配置引用已通过校验
脚本 `scripts/verify_bridge.py` 返回 `ok: true`，并确认：

- Hermes 配置仍引用：
  - `shared/skills`
  - `shared/prefill/hermes-shared-memory.json`
- OpenClaw 配置仍引用：
  - `/home/node/.openclaw/shared/skills`
- 旧 workspaces 的 `MEMORY.md` / `memory` / `shared` symlink 仍可解析

### 4. promoter 能识别当前桥状态
`scripts/promoter.py --dry-run` 返回 `ok: true`，说明自动状态块刷新链路可用。

### 5. 共享 skill 升格治理已补齐
已新增 shared 级治理与清单机制：

- `capabilities/manifests/shared-skills.yaml`：记录要求常驻共享层的技能
- `capabilities/skills/autonomous-ai-agents/claude-research-then-hermes-review/`
- `capabilities/skills/foundation/console-style-progress-report/`
- `prefill/hermes-shared-memory.json`：补充“本地 skill vs shared skill”的升格约束
- `AGENTS.md` / `README.md`：补充共享 skill 治理规则

这意味着后续不会再只靠人工记忆判断“这个 skill 要不要进 shared”，而是有明确入口和可验证目标。

## 当前观察到的真实状态

### 已在使用的兼容层
截至本次整理前，`compat/daily/` 下已存在：

- `2026-04-14.md`
- `2026-04-15.md`

这说明旧 daily 兼容链路**仍在实际承接写入**，兼容目标已生效。

### 尚未沉淀充分的部分
截至本次整理前：

- `curated/memory/facts/` 仍为空
- `curated/memory/projects/` 在本文件创建前尚无结构化项目条目
- `inbox/hermes/daily/`、`inbox/openclaw/daily/`、`inbox/future-agent/daily/` 在本次整理前均为空

### 远端同步状态
当前本地 shared 目录不是 git 仓库；已检查 GitHub 上的 `wh243327457/openclaw-shared-memory`：

- 还没有这次 v2 结构对应的 PR
- 远端仓库也还没有 `manifest.yaml`、`AGENTS.md`、`curated/memory/`、`capabilities/skills/` 这套 v2 结构

## 为什么当前完成度是 75%

已完成：

1. 结构分层
2. 兼容映射
3. Hermes / OpenClaw 引用接通
4. 旧 workspace 兼容验证
5. verify / promoter 校验链路可用

未完成：

1. 将“项目现状”系统沉淀进 `curated/memory/projects/`
2. 让新原始记录逐步从 compat 过渡到 `inbox/<agent>/daily/`
3. 把 v2 结构同步到远端仓库并形成 PR
4. 持续补充 `facts/` 与后续项目条目

## 下一步建议

### 近一步

1. Hermes 后续原始记录默认写入 `inbox/hermes/daily/`
2. 新增 `facts/` / `projects/` 条目时同步更新 `MEMORY.md`
3. 用 promoter 刷新自动状态块
4. 再跑一次 `verify_bridge.py` 做收口确认

### 再下一步

1. 确认用于同步 shared 的 git 仓库位置
2. 把本地 v2 结构整理成可审阅的提交
3. 推出 PR 供审阅

## 长期约束

- `curated/` 只放稳定长期信息
- `inbox/` 只放 agent 原始记录和待整理上下文
- `runtime/` 只放运行时产物
- 新 agent 优先接 canonical 层，不直接依赖 legacy 层
- 禁止把明文 secret 写入 shared
