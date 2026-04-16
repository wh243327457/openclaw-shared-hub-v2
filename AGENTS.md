# AGENTS.md

**共享中台 v2 的 source of truth。**

所有接入的 agent（Hermes、OpenClaw workspaces、未来新增 agent）都应以这里定义的真实结构与兼容入口为准。

## 根目录

- 宿主：`/home/vany/openclaw-data/.openclaw/shared`
- 容器：`/home/node/.openclaw/shared`

## 核心分层

1. **跨 agent 真相源**：`curated/memory/`
2. **agent 原始写入**：`inbox/<agent>/daily/`
3. **运行时产物**：`runtime/<agent>/`
4. **共享能力**：`capabilities/skills/`
5. **兼容视图**：`memory/`、`skills/`、`compat/`
6. **预填充**：`prefill/`

## 目录结构

```text
shared/
├── manifest.yaml
├── AGENTS.md
├── README.md
├── curated/
│   └── memory/
│       ├── MEMORY.md
│       ├── facts/
│       └── projects/
├── inbox/
│   ├── hermes/daily/
│   ├── openclaw/daily/
│   └── future-agent/daily/
├── runtime/
│   ├── hermes/
│   ├── openclaw/
│   │   └── dreams/
│   └── future-agent/
├── capabilities/
│   ├── skills/
│   ├── manifests/
│   └── versions/
├── compat/
│   └── daily/
│       ├── YYYY-MM-DD.md
│       └── .dreams -> ../../runtime/openclaw/dreams
├── memory/
│   ├── MEMORY.md -> ../curated/memory/MEMORY.md
│   ├── daily -> ../compat/daily
│   ├── facts -> ../curated/memory/facts
│   └── projects -> ../curated/memory/projects
├── skills -> capabilities/skills
└── prefill/
    └── hermes-shared-memory.json
```

## 读写规范

### 1) Curated：长期稳定真相
写入 `curated/memory/` 的内容必须满足：
- 经过验证、较稳定、会被多个 agent 复用
- 事实片段写入 `curated/memory/facts/`
- 项目状态写入 `curated/memory/projects/`
- 索引更新到 `curated/memory/MEMORY.md`

### 2) Inbox：agent 原始写入
默认原始记录、草稿、待整理上下文写入：
- `inbox/hermes/daily/YYYY-MM-DD.md`
- `inbox/openclaw/daily/YYYY-MM-DD.md`
- `inbox/future-agent/daily/YYYY-MM-DD.md`

这些内容**不是**跨 agent 的最终真相源；需要整理后再晋升到 `curated/memory/`。

### 3) Runtime：运行时产物
运行时文件统一放在 `runtime/<agent>/`：
- `.dreams/`
- cache
- indexes
- 中间摘要
- 其他临时产物

**不要**把运行时产物直接落到 `curated/` 或 `compat/` 的真实目录里。

### 4) Legacy compatibility：保留旧入口
为了不破坏现有 Hermes / OpenClaw 接入：
- `shared/skills` 保留为兼容入口，实际指向 `capabilities/skills`
- `shared/memory/MEMORY.md` 指向 `curated/memory/MEMORY.md`
- `shared/memory/facts` 指向 `curated/memory/facts`
- `shared/memory/projects` 指向 `curated/memory/projects`
- `shared/memory/daily` 指向 `compat/daily`
- `shared/memory/daily/.dreams` 通过 `compat/daily/.dreams` 最终落到 `runtime/openclaw/dreams`

### 5) OpenClaw 旧 workspace 的兼容说明
当前旧 OpenClaw workspace 已把：
- `MEMORY.md` 指到 `shared/memory/MEMORY.md`
- `memory` 指到 `shared/memory/daily`
- `shared` 指到共享根目录

因此本次迁移后：
- 旧 `MEMORY.md` 读取仍可用
- 旧 `memory/YYYY-MM-DD.md` 读取仍可用
- 旧 `memory/.dreams/*` 写入仍会进入 runtime，而不会继续留在 curated / compat 的真实目录中

## 共享 skill 升格规则

- 新沉淀的 skill 默认先判断：它是“仅当前 agent 的本地长期能力”，还是“跨 agent 共享能力”
- 只要该 skill 同时满足以下任一条件，就应升格到 `shared/capabilities/skills/`：
  - Hermes / OpenClaw / future-agent 预计都会复用
  - 属于共享中台、跨 agent 协作、共享记忆、调研工作流、进度汇报等横切能力
  - 不共享会导致不同 agent 行为漂移、重复造轮子或长期规则不一致
- 升格到 shared 时，必须同时完成：
  1. 复制完整 skill 目录（`SKILL.md` 与 `templates/`、`references/`、`scripts/`、`assets/`）
  2. 更新 `capabilities/manifests/shared-skills.yaml`
  3. 如涉及长期协作约束，再同步更新 `prefill/` 或 `curated/memory/` 的对应说明
- 如果明确只保留本地，不进入共享层，则需要在结果里说清楚：当前仅为 agent 本地长期能力，不是 shared 长期能力

## 推荐读取顺序

1. `shared/manifest.yaml`
2. `shared/AGENTS.md`
3. `shared/curated/memory/MEMORY.md`
4. 按需读取 `shared/curated/memory/facts/` 与 `shared/curated/memory/projects/`
5. 如需兼容旧 OpenClaw 日志，再读取 `shared/memory/daily/`（兼容视图）
6. 如需查看 agent 原始记录，再读取 `shared/inbox/<agent>/daily/`
7. 只有调试运行时行为时才读取 `shared/runtime/<agent>/`

## Secrets 安全规范

- **默认禁止**把任何明文 secret、API key、token、密码写入 shared
- 如需引用 secret，用变量名占位，如 `$OPENCLAW_API_KEY`
- 各 agent 的 `.env` / credentials 应保留在各自 agentDir 内，不进入 shared
