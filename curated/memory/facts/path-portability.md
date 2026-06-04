---
claim_id: path-portability
claim_type: workflow_rule
status: active
confidence: 0.95
fact_id: path-portability
freshness_class: static
scope: agent-system
lens: world
topic: shared.path.portability
source_agent: hermes
source_paths:
  - manifest.yaml
  - AGENTS.md
  - capabilities/skills/foundation/path-portability/SKILL.md
  - scripts/resolve_shared_root.py
evidence_refs:
  - manifest.yaml#deployment
  - capabilities/skills/foundation/path-portability/SKILL.md
  - scripts/resolve_shared_root.py
  - inbox/hermes/daily/2026-06-02.md
sensitivity: low
secret_checked: true
created_at: 2026-06-02T11:30:00+08:00
updated_at: 2026-06-02T11:30:00+08:00
last_verified_at: 2026-06-02T11:30:00+08:00
review_due_at: 2026-09-02
review_status: approved
review_after: 2026-09-02
supersedes: []
superseded_by: []
---

# Path Portability — 共享中台 v2 的可迁移路径契约

## 一句话结论

shared hub v2 的所有运行时代码（scripts、skills、prefill、agent 接入）必须通过 `scripts/resolve_shared_root.py` 解析宿主根，**禁止硬编码 `/home/vany/...` 这类绝对路径**。跨机器搬运时只需保留 `manifest.yaml: deployment.portable.must_preserve` 列出的子树。

## 触发场景

- 在 vany（`/home/vany/agent/shared`）开发的脚本迁移到 ubuntu（`/home/ubuntu/agent/shared`）时无法直接运行
- 容器内 `OpenClaw` 与宿主路径不一致时无法定位 shared 根
- 不同工作站（开发机、生产机、笔记本）共享同一份中台结构时

## 解析顺序

```text
$SHARED_HUB_ROOT
  ↓
$AGENTS_SHARED_ROOT
  ↓
$XDG_DATA_HOME/openclaw/shared
  ↓
~/.local/share/openclaw/shared
  ↓
<脚本位置>/../..
  ↓
<脚本位置>/..
  ↓
<cwd>/..
  ↓
<cwd>
```

## 反模式（绝对禁止）

| 反模式 | 后果 | 替代 |
|---|---|---|
| `Path("/home/vany/agent/shared")` | 迁移后立即失效 | `resolve_shared_root.py` |
| prefill JSON 写死绝对路径 | agent 启动后无法找到根 | 用 `shared_root_resolution` 字段 |
| AGENTS.md / README.md 引用 `/home/vany/...` | 文档误导 | 改为示例 + `${SHARED_HUB_ROOT}` 占位 |
| `runtime/` 进入 Git 主线 | 仓库臃肿 | `.gitignore` |

## 跨机器搬运最小保留集

必须保留：manifest.yaml / AGENTS.md / README.md / curated/ / capabilities/skills/ / capabilities/manifests/ / compat/daily/ / prefill/

可省略：runtime/、inbox/<agent>/daily/

## 证据

- `manifest.yaml: deployment.resolution_order`
- `manifest.yaml: deployment.portable.must_preserve`
- `capabilities/skills/foundation/path-portability/SKILL.md`
- `scripts/resolve_shared_root.py`（已写 + 单测通过）
- `inbox/hermes/daily/2026-06-02.md`（vany → ubuntu 迁移实操记录）

## 风险与边界

- 容器场景下挂载点变了，路径解析可能落到不正确的根；优先用 `SHARED_HUB_ROOT` 显式指定
- `runtime/` 仍可能因早期 commit 残留被 track，需要 `git rm --cached` 清理
- 旧 fact 中若仍引用 `/home/vany/...`，是兼容历史；新增 fact 必须遵守本约定
