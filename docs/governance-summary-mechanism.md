# 共享中台治理总结机制

目标：让 shared hub v2 长期可运行、可审计、可压缩，避免 `inbox/`、`runtime/`、`curated/`、shared skills 随时间变成不可读的堆积层。

本机制文档解释治理思路；强制执行口径以 `docs/shared-governance-standard.md` 为准。

核心原则：**raw 可以宽进，curated 必须严出；自动化负责发现和打分，总控负责判断和压缩。**

---

## 1. 分层生命周期

```text
raw 输入层              候选层                    curated 真相层             压缩/淘汰层
inbox/<agent>/daily  -> promotion candidates  -> facts/projects/skills  -> archives / superseded / local-only
runtime/<agent>/     -> runtime evidence      -> curated 摘要/索引        -> TTL 清理候选
compat/daily/        -> legacy evidence       -> 不直接晋升全文           -> git rm --cached / 本地保留
```

| 层 | 允许增长 | 是否进 Git 主线 | 是否作为跨 agent 真相 | 治理动作 |
|---|---:|---:|---:|---|
| `inbox/<agent>/daily/` | 可以增长 | 常规 daily 可有限进入；dreaming/raw bulk 不进 | 否 | 周期扫描、候选提取、去重 |
| `runtime/<agent>/` | 可以增长但有上限 | 否 | 否 | TTL / size warning / 人工确认清理 |
| `compat/` | 不应增长 | 只保留薄入口 | 否 | 兼容入口化，历史 bulk 移出 Git |
| `curated/memory/MEMORY.md` | 不应线性增长 | 是 | 入口索引 | 超 150 行触发压缩 |
| `curated/memory/facts/` | 小规模增长 | 是 | 是 | frontmatter、时效、冲突检查 |
| `curated/memory/projects/` | 小规模增长 | 是 | 是 | 状态块、决策、下一步 |
| `capabilities/skills/` | 慢增长 | 是 | 能力契约 | shared 准入、reference 阈值 |

---

## 2. 候选筛选标准

### 2.1 晋升必要条件

一条信息要进入 `curated/`，至少满足：

1. **跨会话价值**：7 天后仍有复用价值。
2. **跨 agent 价值**：Hermes / OpenClaw / future-agent 至少两个角色可能受益，或它是 shared hub 自身治理规则。
3. **可验证证据**：来自文件、命令输出、PR、配置、用户明确确认、稳定复现行为之一。
4. **去重通过**：现有 facts/projects/skills 没有覆盖；若覆盖，只更新已有条目或标记 superseded。
5. **脱敏通过**：不含 API key、token、cookie、私钥、密码、可直接滥用的凭据。

### 2.2 默认拒绝晋升

以下内容默认不进 curated：

- 单次任务进度：“今天跑了 X”“PR #n 已开”“commit sha”。
- 原始 stdout/stderr、缓存、索引、`.dreams`、reflection 全文。
- 未验证的推断、模型自我评价、打分噪声、source/score 明细。
- 只对单个 agent 当前运行态有意义的临时状态。
- 未来一周内大概率过期的事实。

### 2.3 可压缩晋升

有价值但太长的内容，只能压缩后进入 curated：

- 调研长文 → `projects/<project>.md` 的“结论 / 决策 / 下一步 / 证据链接”。
- 多次运行日志 → 一条 fact 或项目状态中的“已验证行为”。
- 多个相似 skill reference → 合并成 class-level reference。
- agent 产物集合 → 只保留索引、验收结果和可复查路径。

---

## 3. 评分模型：Promote Score

候选扫描可以给每条候选生成建议分，供总控审查；分数不等于自动晋升。

| 维度 | 分值 | 说明 |
|---|---:|---|
| 用户明确要求记住/制度化 | +3 | “以后都这样”“记住”“沉淀成规则” |
| 跨 agent 复用 | +3 | Hermes/OpenClaw/future-agent 都可能用到 |
| 已验证证据 | +2 | 有文件、命令、PR、测试或用户确认 |
| 稳定性 | +2 | 不是临时状态，7 天后仍有效 |
| 去重后补充价值 | +1 | 对已有 fact/project 有增量 |
| 含 secret 风险 | -5 | 直接拒绝或脱敏后重评 |
| 单次任务进度 | -3 | 默认不进 memory，可进 session/history |
| 原始日志/大段输出 | -3 | 只能压缩摘要 |
| 与现有事实冲突 | -4 | 标记 disputed，不直接覆盖 |

建议口径：

- `score >= 7`：建议人工审查后晋升。
- `4 <= score < 7`：保留候选，等待更多证据。
- `score < 4`：默认拒绝或仅留 inbox/runtime。
- 任意 secret 风险：先脱敏，否则拒绝。

---

## 4. 周期性治理节奏

### Daily：轻量扫描，不写 curated

每天只做：

1. `promoter.py --dry-run --scan-promote-candidates` 生成候选。
2. `verify_bridge.py` 输出 `slimming_metrics` 和 fact governance warnings。
3. 记录 backlog：inbox 文件数、runtime 大小、MEMORY 行数、shared skill references 数。
4. 不自动晋升、不自动删除。

### Weekly：总控压缩审查

每周做一次人工/总控审查：

1. 读取最近 7 天候选。
2. 按 score 分组：accept / defer / reject / duplicate / disputed。
3. 对 accepted 候选写入 facts/projects/skills。
4. 对 duplicate 候选更新已有条目或不处理。
5. 对 disputed 候选写 conflict metadata，不覆盖旧事实。
6. 生成一份 `runtime/hermes/governance-reviews/YYYY-WW.md` 审查报告。
7. 跑 verify，确认 warning 可解释。

### Monthly：结构瘦身

每月做一次结构治理：

1. `MEMORY.md` 是否超过 150 行；超过则迁移到 archive 或项目页。
2. 单个 shared skill references 是否超过 15；超过则合并主题 reference。
3. runtime 是否超过 100MB；超过则生成清理候选，人工确认后清理。
4. Git 是否跟踪 raw/bulk；若是，单独 PR `git rm --cached`。
5. facts 是否有 stale/disputed/superseded 未处理项。

---

## 5. Curated 写入模板

### 5.1 Fact frontmatter 最小字段

```yaml
---
fact_id: shared-hub-governance-summary-mechanism
status: active
freshness_class: operational
scope: shared-hub
subject: governance.summary
attribute: lifecycle
value_summary: raw 宽进、curated 严出，候选经评分/证据/去重/脱敏后人工晋升
last_verified_at: 2026-05-18T00:00:00+08:00
review_due_at: 2026-06-18T00:00:00+08:00
secret_checked: true
---
```

### 5.2 Project 状态最小结构

```markdown
## 治理状态

- 最近审查时间：`YYYY-MM-DDTHH:mm:ss+08:00`
- 当前健康度：绿 / 黄 / 红
- raw backlog：...
- curated pressure：...
- 本轮 accepted / deferred / rejected：...
- 下一次 review：...
```

### 5.3 Weekly review 报告结构

```markdown
# Governance Review YYYY-WW

## 结论
- 健康度：绿/黄/红
- 是否需要人工决策：是/否

## 指标
| 指标 | 当前 | 阈值 | 处理 |
|---|---:|---:|---|

## 候选处理
| 候选 | 来源 | score | 决策 | 目标 |
|---|---|---:|---|---|

## 风险与后续
- ...
```

---

## 6. 自动化边界

允许自动化：

- 统计大小、行数、文件数。
- 扫描候选、生成 score 和建议目标。
- 检测 secret 关键词、冲突、stale facts、reference 超阈值。
- 生成 weekly review 草稿。
- 刷新 `MEMORY.md` 自动状态块。

禁止默认自动化：

- 自动把候选写入 curated。
- 自动删除 inbox/runtime。
- 自动覆盖 active facts。
- 自动把 `.dreams` / reflection 当作事实。
- 自动把单次任务状态写入长期记忆。

---

## 7. 验收标准

治理机制达标的信号：

- `curated/memory/MEMORY.md` 长期保持为入口索引，而不是流水账。
- `verify_bridge.py` 可以直接显示膨胀源和 warning。
- 每条新 fact 都有 frontmatter、review_due_at、secret_checked。
- shared skill references 超阈值时有明确 review 动作。
- raw/inbox 可以保留证据，但不会污染 Git 主线和 curated 真相源。
- 每周 review 能回答：哪些该晋升、哪些该拒绝、哪些该压缩、哪些该清理。
