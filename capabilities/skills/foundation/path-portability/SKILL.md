---
name: path-portability
description: 共享中台 v2 的可迁移路径契约。所有 agent 接入、scripts 编写、prefill 写入、跨机器搬运时，必须通过 resolve_shared_root.py 获取宿主根，禁止硬编码绝对路径。
version: "1.0.0"
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [portability, migration, shared-hub, governance, foundation]
    related_skills: [shared-memory-bridge, config-target-routing]
---

# Path Portability — 共享中台 v2 的可迁移路径契约

## 1. 背景与目标

共享中台 v2 的设计目标是让 Hermes / OpenClaw / future-agent 在不同机器、不同宿主路径下都能复用同一份结构。但早期 manifest、prefill、docs 写死了一批机器专属绝对路径，导致跨机器迁移时所有引用都需要人工改写。

本 skill 确立：

1. **共享中台本体推荐统一放在 `~/agent/shared`，运行时根路径必须通过 `scripts/resolve_shared_root.py` 解析**
2. **agent 原始写入、运行时产物按"相对根路径"表达**
3. **跨机器搬运只需保留 manifest 定义的 `must_preserve` 子树**
4. **新增 scripts / skills / prefill / docs 必须通过 portability 检查**

## 2. 何时使用

| 场景 | 是否需要本 skill |
|---|---|
| 写新的 `scripts/*.py` 并需要拼绝对路径 | 必须 |
| 改 manifest / AGENTS.md 引用宿主路径 | 必须 |
| 写新 prefill JSON | 必须 |
| 写新 shared skill 并引用 curated 路径 | 必须 |
| 写新 agent 的接入文档 | 必须 |
| 写新 docs / README | 必须（不能写死 /home/vany/...） |
| 一次性 CLI 命令（不写入文件） | 鼓励，但不强制 |
| 第三方配置文件原样引用 | 标注 + 备注，不强制 |

## 3. 核心契约

### 3.1 解析顺序（与 manifest.yaml 对齐）

```text
$SHARED_HUB_ROOT
  ↓
$AGENTS_SHARED_ROOT
  ↓
$XDG_DATA_HOME/openclaw/shared
  ↓
~/.local/share/openclaw/shared
  ↓
~/agent/shared
  ↓
<脚本位置>/../../              (即 <root>/scripts/..)
  ↓
<脚本位置>/..                  (即脚本所在根目录的子目录)
  ↓
<cwd>/                         (当前工作目录)
  ↓
<cwd>/..
```

只要探测目录同时含 `manifest.yaml` + `AGENTS.md`，就视为合法根。

### 3.2 脚本模板

```python
import sys
from pathlib import Path

# 把 scripts/ 加入 path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from resolve_shared_root import resolve

SHARED_ROOT = resolve()[0]
CURATED = SHARED_ROOT / "curated" / "memory"
INBOX_HERMES = SHARED_ROOT / "inbox" / "hermes" / "daily"
RUNTIME_HERMES = SHARED_ROOT / "runtime" / "hermes"
```

### 3.3 prefill 引用规范

prefill JSON **不再写死宿主绝对路径**，只描述"语义位置"：

```json
{
  "shared_root_resolution": "scripts/resolve_shared_root.py",
  "layer_reads": ["curated/memory", "capabilities/skills"],
  "layer_writes": ["inbox/hermes/daily", "runtime/hermes"]
}
```

agent 启动时把"语义位置"通过 `SHARED_ROOT / <path>` 拼成实际路径。

## 4. 迁移流程（机器 A → 机器 B）

1. 在机器 A 上 `cd <shared-root> && tar czf shared-hub.tgz manifest.yaml AGENTS.md README.md curated/ capabilities/ compat/ prefill/`
2. 拷贝 `shared-hub.tgz` 到机器 B
3. 机器 B 解压到推荐统一目录 `~/agent/shared/`（如需自定义目录，设置 `SHARED_HUB_ROOT`）
4. 设置：`export SHARED_HUB_ROOT=$HOME/agent/shared`
5. 跑 `python3 scripts/resolve_shared_root.py --check` 校验
6. 跑 `python3 scripts/verify_bridge.py`（如果存在）确认 bridge 状态

> **注意**：跨机器搬运不需要保留 `runtime/` 和 `inbox/*/daily/`（见 `manifest.yaml: deployment.portable.may_omit_on_first_run`）。这些是机器本地的运行时产物。

## 5. 跨机器搬运的最小保留集

必须保留（否则共享中台不再成立）：

- `manifest.yaml`
- `AGENTS.md`
- `README.md`
- `curated/`（跨 agent 真相源）
- `capabilities/skills/` + `capabilities/manifests/`（共享能力）
- `compat/daily/`（旧 OpenClaw 兼容视图）
- `prefill/`（预填充）

可省略（首次在新机器上自动重建）：

- `runtime/`（运行时产物）
- `inbox/<agent>/daily/`（agent 原始记录）

默认 `.gitignore` 忽略（避免 runtime 污染主线）：

- `runtime/`
- `inbox/*/daily/dreaming/`
- `compat/daily/dreaming/`
- `inbox/*/daily/.dreams/`

## 6. 验收命令

```bash
cd <shared-root>
python3 scripts/resolve_shared_root.py --check      # 根解析 + 必填校验
python3 scripts/resolve_shared_root.py --explain    # 打印解析路径，便于排错
python3 scripts/resolve_shared_root.py --json       # JSON 输出
```

新加 scripts 时，跑：

```bash
# 模拟不同机器上的解析
cd /tmp && SHARED_HUB_ROOT=<shared-root> python3 <shared-root>/scripts/resolve_shared_root.py --check
```

## 7. 反模式（禁止）

| 反模式 | 后果 | 替代 |
|---|---|---|
| 在 Python 里 `Path("/home/vany/agent/shared")` | 迁移后失效 | `resolve_shared_root.py` |
| prefill JSON 写死绝对路径 | 迁移后失效 | 用 `shared_root_resolution` 字段 |
| AGENTS.md / README.md 引用某台机器的绝对路径 | 文档误导 | 改为 `~/agent/shared` 规范或 `${SHARED_HUB_ROOT}` |
| 把 `runtime/` 提交到 main | 仓库臃肿 | `.gitignore` |
| 在 cron / launchd plist 里写死机器专属绝对路径 | 迁移后定时任务失效 | 用 `${SHARED_HUB_ROOT}` 占位 |

## 8. 已知 pitfalls

- **env 指向不存在目录不会立即报错**：`resolve_shared_root.py` 会自动降级到下一候选；想要严格模式请用 `--check` 显式断言。
- **portable 模式不能让绝对路径"消失"**：manifest 里仍然保留 `host_examples` 这种文档性例子，但运行时代码禁止读它。
- **首次在新机器上 clone 出来的就是根**：`git clone` 后的目录就是合法根，无需额外 `export`。
- **容器里的根是 `/home/node/.openclaw/shared/`**：容器内 `resolve_shared_root` 会落到 `script:..` 解析。如果挂载路径变了，优先用 `SHARED_HUB_ROOT` 显式指定。
- **XDG 路径可能存在但不是合法根**：例如 `~/.local/share/openclaw/shared` 存在但没有 manifest.yaml，解析器会继续往下找。

## 9. 相关文件

- `scripts/resolve_shared_root.py` — 路径解析器
- `manifest.yaml` 中 `deployment` 段 — 解析顺序与 must_preserve 清单
- `references/migration-checklist.md` — 跨机器迁移的逐步操作
- `curated/memory/facts/path-portability.md` — 长期事实条目
