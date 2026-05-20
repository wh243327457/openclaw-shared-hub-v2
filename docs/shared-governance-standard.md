# 共享中台治理总结标准

本文件是 shared hub v2 的强制执行标准。所有 Hermes / OpenClaw / future-agent 对共享中台的写入、总结、晋升、压缩、淘汰，都以本标准为准。

一句话标准：**raw 宽进、候选严筛、curated 少而准、runtime 可清、所有晋升可追溯。**

---

## 0. 标准适用范围

适用于：

- `inbox/<agent>/daily/` 原始记录的筛选。
- `runtime/<agent>/` 运行时材料的证据引用和清理候选。
- `curated/memory/facts/` 稳定事实写入。
- `curated/memory/projects/` 项目状态更新。
- `curated/memory/MEMORY.md` 主索引维护。
- `capabilities/skills/` shared skill 升格与 reference 控制。

不适用于：

- 单个 agent 的私有临时 scratchpad。
- 含 secret 的配置文件正文。
- 未经脱敏的原始日志全文。

---

## 1. 标准状态流

```text
RAW_CAPTURED
  -> CANDIDATE_EXTRACTED
  -> SCREENED
  -> DECIDED_ACCEPTED / DECIDED_DEFERRED / DECIDED_REJECTED / DECIDED_DUPLICATE / DECIDED_DISPUTED
  -> CURATED_WRITTEN / LEFT_IN_INBOX / ARCHIVED / SUPERSEDED
  -> VERIFIED
```

| 状态 | 输入 | 动作 | 产物 | 验收 |
|---|---|---|---|---|
| `RAW_CAPTURED` | agent 原始记录、运行日志、调研输出 | 写入 inbox/runtime | raw 文件 | 不含 secret 明文；路径正确 |
| `CANDIDATE_EXTRACTED` | raw 文件 | 提取候选句/事件/规则 | candidate 记录 | 有 source path、agent、日期 |
| `SCREENED` | candidate | 打分、脱敏、去重、证据检查 | score + 风险标记 | 有 decision basis |
| `DECIDED_*` | screened candidate | 总控/人工做决策 | accept/defer/reject/duplicate/disputed | 决策可解释 |
| `CURATED_WRITTEN` | accepted candidate | 写 facts/projects/skills | curated 条目 | frontmatter/索引/证据齐全 |
| `VERIFIED` | curated 改动 | 跑 promoter/verify | 验证输出 | `verify_bridge.py ok=true` |

---

## 2. 五门准入标准

任何内容进入 `curated/` 前必须同时通过五道门：

| Gate | 问题 | 通过标准 | 不通过处理 |
|---|---|---|---|
| G1 长期价值 | 7 天后还有用吗？ | 是稳定规则、路径、协议、项目状态、经验模式 | 留 inbox/runtime，不晋升 |
| G2 跨 agent 价值 | 是否对两个以上 agent 或 shared 本身有价值？ | Hermes/OpenClaw/future-agent 可复用，或治理 shared | 若只对单 agent 有用，留该 agent 本地 skill/memory |
| G3 证据 | 是否可验证？ | 文件、命令、测试、PR、用户确认、稳定复现之一 | `deferred`，等证据 |
| G4 去重/冲突 | 是否已有覆盖或冲突？ | 无重复；或明确 supersedes/superseded_by/conflict | duplicate/disputed，不直接覆盖 |
| G5 安全 | 是否脱敏？ | 无明文 secret/token/password/cookie/private key | 拒绝；脱敏后重评 |

**硬规则：五门任一失败，不得写入 curated active fact。**

---

## 3. 标准决策表

| 内容类型 | 默认目标 | 是否晋升 | 标准动作 |
|---|---|---:|---|
| 用户长期偏好 / 明确纠正 | `curated/memory/facts/` 或本地 memory | 是 | 写稳定 fact；避免命令式措辞 |
| shared 路径、分层、兼容入口 | `curated/memory/facts/` | 是 | 写 operational/static fact |
| 项目阶段、架构决策、验收标准 | `curated/memory/projects/` | 是 | 更新项目页，不塞 MEMORY 主索引 |
| 跨 agent 工作流 | `capabilities/skills/` + manifest | 是 | 写 shared skill；reference 控制 |
| 单次 PR、commit、issue、临时进度 | inbox/session history | 否 | 不进长期记忆；必要时项目页一句话概括 |
| stdout/stderr/log/cache/index | `runtime/<agent>/` | 否 | 只作为证据路径，不复制全文 |
| `.dreams` / reflection | `runtime/openclaw/dreams/` | 默认否 | 仅作为灵感候选；需证据才能晋升 |
| 调研长文 | `runtime/` + Obsidian/项目页摘要 | 压缩后可 | 只晋升结论、决策、证据链接 |
| 过期事实 | facts with `status: superseded` | 否/更新 | 标记 superseded，不删除历史 |
| 有冲突事实 | facts with `status: disputed` | 暂缓 | 写 conflict metadata，等待裁决 |

---

## 4. Promote Score 标准

候选可自动评分，但分数只辅助决策，不允许自动写 curated。

| 维度 | 分值 |
|---|---:|
| 用户明确要求制度化/记住 | +3 |
| 跨 agent 复用 | +3 |
| shared hub 自身治理规则 | +3 |
| 有可验证证据 | +2 |
| 稳定性超过 7 天 | +2 |
| 对已有条目有增量 | +1 |
| 含 secret 风险 | -5 |
| 单次任务进度 | -3 |
| 原始日志/大段输出 | -3 |
| 与现有 active fact 冲突 | -4 |

决策阈值：

- `score >= 7` 且五门全过：`DECIDED_ACCEPTED`。
- `4 <= score < 7`：`DECIDED_DEFERRED`。
- `score < 4`：`DECIDED_REJECTED`。
- 有重复：`DECIDED_DUPLICATE`。
- 有冲突：`DECIDED_DISPUTED`。
- 有 secret 且无法脱敏：强制 `DECIDED_REJECTED`。

---

## 5. 标准输出格式

### 5.1 Candidate 记录

```yaml
candidate_id: YYYYMMDD-agent-short-slug
source_agent: hermes|openclaw|future-agent
source_path: inbox/<agent>/daily/YYYY-MM-DD.md
extracted_at: YYYY-MM-DDTHH:mm:ss+08:00
summary: 一句话候选摘要
evidence:
  - type: file|command|test|pr|user-confirmation
    ref: 可复查路径或命令
score: 0
gates:
  long_term_value: pass|fail
  cross_agent_value: pass|fail
  evidence: pass|fail
  dedupe_conflict: pass|fail
  secret_check: pass|fail
decision: accepted|deferred|rejected|duplicate|disputed
reviewer: hermes|human|openclaw
notes: 决策理由
```

### 5.2 Fact 标准 frontmatter

```yaml
---
fact_id: kebab-case-id
status: active|superseded|disputed
freshness_class: static|operational|volatile
scope: shared-hub|hermes|openclaw|future-agent|multi-agent
subject: domain.object
attribute: property
value_summary: 一句话事实
last_verified_at: YYYY-MM-DDTHH:mm:ss+08:00
review_due_at: YYYY-MM-DDTHH:mm:ss+08:00
secret_checked: true
source:
  - type: file|command|test|pr|user-confirmation
    ref: evidence ref
supersedes: []
superseded_by: []
conflict:
  status: none|open|resolved
---
```

### 5.3 Project 更新标准

项目页只记录：

- 当前状态：绿/黄/红。
- 当前阶段：一句话。
- 最近验证时间。
- 已完成的稳定能力。
- 当前风险/阻塞。
- 下一步建议。
- 证据链接/路径。

项目页不得成为逐日流水账；单次进度只在“影响项目状态”时压缩成一句话。

### 5.4 MEMORY.md 主索引标准

`curated/memory/MEMORY.md` 只允许放：

- 根路径和作用范围。
- 目录/项目/事实/skill 的索引入口。
- 当前状态摘要。
- 自动生成状态块。
- archive 链接。

不允许放：

- promoted 明细全文。
- 日志、score/source 明细。
- 单次任务进度。
- 大段调研摘要。

---

## 6. 质量阈值

| 指标 | 绿 | 黄 | 红 | 动作 |
|---|---:|---:|---:|---|
| `MEMORY.md` 行数 | `<=120` | `121-150` | `>150` | 黄：计划压缩；红：必须压缩 |
| runtime 总量 | `<=50MB` | `50-100MB` | `>100MB` | 红：生成清理候选 |
| tracked dreaming bulk | `0` | `>0` | `>0 且增长` | 必须 `git rm --cached` 方案 |
| 单 skill references | `<=10` | `11-15` | `>15` | 黄：合并计划；红：必须 review |
| stale facts | `0` | `1-5` | `>5` | 每周复盘处理 |
| disputed facts | `0` | `1-3` | `>3` | 需要人工裁决 |
| inbox backlog days | `<=7` | `8-30` | `>30` | 每周复盘筛选；每月只看结构压力 |

---

## 7. 标准节奏

### Daily Summary 标准

每日只做“总结与候选池”，不做长期晋升：

```bash
cd <shared-root>
python3 scripts/promoter.py --dry-run --scan-promote-candidates --recent-limit 10
python3 scripts/verify_bridge.py
```

产物：

- `runtime/hermes/governance/daily/YYYY-MM-DD.md`
- 候选扫描日志、verify JSON、warning 列表

每日总结必须回答：

1. 昨天 Hermes / OpenClaw / future-agent 分别发生了什么？
2. 哪些信息可能有长期价值，但需要周复盘再判断？
3. 是否出现 secret / verify fail / slimming warning / 用户决策项？
4. 是否有内容明显应拒绝进入核心记忆？

禁止：daily 自动写 curated、自动删除 raw、自动修改 active facts。

### Weekly Review 标准：核心记忆晋升触发点

每周复盘是唯一常规内容晋升节点。每周从最近 7 天 daily summaries 和候选扫描中筛选，决定哪些进入核心记忆。

每周必须回答：

1. 哪些候选 accepted？为什么？写到 `facts/`、`projects/` 还是 `capabilities/skills/`？
2. 哪些 deferred？缺什么证据？下周是否继续观察？
3. 哪些 rejected？原因是什么？是否可直接忽略？
4. 哪些 duplicate/disputed？对应哪个既有事实？
5. 本周 shared 是否变胖？膨胀源是什么？
6. 是否需要用户决策？

### Weekly Review 草稿标准

在不写入 curated 的前提下，允许先生成周复盘草稿，供总控拍板：

- 读取 `scripts/promoter.py --dry-run --scan-promote-candidates` 的候选池。
- 读取 `scripts/verify_bridge.py` 的 warning 和 slimming 指标。
- 生成 `runtime/hermes/governance/weekly/YYYY-WW.md` 与同名 JSON 草稿。
- 草稿中必须明确标注：`accepted` 只是“建议进入人工/总控复核队列”，不是已写入长期记忆。
- 草稿可列出 `accept_review_needed / deferred / duplicate_or_disputed / rejected_or_redact_first` 四类建议，但不得直接写 curated。

允许：

- 写入 `curated/memory/facts/`
- 更新 `curated/memory/projects/`
- 更新 `curated/memory/MEMORY.md` 索引入口
- 升格/更新 shared skill
- 标记 facts 为 `superseded` / `disputed`
- 生成 weekly review 草稿到 `runtime/hermes/governance/weekly/`

禁止：

- 无证据自动写 active fact
- 把 daily/raw 全文复制进 curated
- 在未确认路径时删除 raw/runtime
- 把周报草稿当作自动晋升结果

产物：`runtime/hermes/governance/weekly/YYYY-WW.md`。

### Monthly Health Review 标准：结构治理节点

每月只做结构健康复盘，不作为常规内容晋升主入口。它检查 shared 是否因为长期运行而变胖、变乱或失控。

每月必须做：

1. `MEMORY.md` 压缩审查。
2. facts stale/disputed/superseded 总量审查。
3. shared skill references 合并审查。
4. runtime size 清理候选。
5. Git tracked raw/bulk 审查。
6. 更新项目页治理状态。

产物：`runtime/hermes/governance/monthly/YYYY-MM.md`。

---

## 8. 验收命令

任何治理标准改动后必须跑：

```bash
cd <shared-root>
python3 -m unittest tests/test_fact_governance.py
python3 scripts/promoter.py --dry-run
python3 scripts/verify_bridge.py
git diff --check
```

合格标准：

- 单测通过。
- `verify_bridge.py` 返回 `ok=true`。
- 新 warning 必须能解释；不能引入 slimming warning。
- `MEMORY.md` 不超过 150 行。
- 不新增明文 secret。

---

## 9. 标准版本

- version: `2026-05-18.v1`
- owner: `shared-hub governance`
- review cadence: daily summary + weekly core-memory review + monthly health review
- next review due: `2026-06-18`
