# 共享中台 v2 优化落地 Plan

- 计划创建时间: 2026-04-25 02:19:01 +0800
- 共享根目录: `<shared-root>`
- 当前阶段: 第一轮治理优化已完成，进入复核 / 收口
- 总体策略: 不继续大改目录结构；优先补齐“晋升协议、治理校验、future-agent 接入包、shared skills 元数据、维护脚本隔离、状态一致性、runtime 留存策略”。
- 安全边界: 禁止写入明文 secret；所有长期事实必须进入 curated；原始记录进入 inbox；运行时产物进入 runtime。

## 当前进度

| 编号 | 优化项 | 优先级 | 状态 | 验收方式 |
|---|---|---:|---|---|
| 0 | 当前状态审计 | P0 | ✅ 已完成 | `verify_bridge.py` 与 `promoter.py --dry-run` 可运行；Claude Code 只读审计完成 |
| 1 | inbox → curated 晋升协议 | P0 | ✅ 已完成 | 有协议文档、日志模板；promoter dry-run 可输出候选清单；不自动写 curated |
| 2 | verify_bridge.py 治理级校验 | P0 | ✅ 已完成 | 输出 governance / promotion_backlog / future_agent_readiness / runtime_retention / skills_metadata；`verify_bridge.py` ok=true |
| 3 | future-agent 最小接入包 | P1 | ✅ 已完成 | README / prefill / smoke note 模板存在；verify 可见 readiness=true |
| 4 | shared skills manifest 元数据化 | P1 | ✅ 已完成 | 每个 shared skill 有 id/path/version/status/agents/owner/last_reviewed；metadata_ok=true |
| 5 | 维护脚本副作用隔离 | P1 | ✅ 已完成 | daily maintenance 支持 SHARED_ONLY / DRY_RUN / RUN_KB_SYNC；KB sync 可跳过 |
| 6 | 项目状态字段统一 | P1 | ✅ 已完成 | `status-schema.md` 已落地；项目文档已区分基础设施完成度与治理运营成熟度 |
| 7 | runtime retention 策略 | P2 | ✅ 已完成 | 有 retention 文档；verify 报告 runtime size；默认 report-only 不删除 |

## 分步执行计划

### Step 0：审计基线
- 状态: ✅ 已完成
- 已确认:
  - `scripts/verify_bridge.py` exit 0。
  - `scripts/promoter.py --dry-run --recent-limit 10` exit 0。
  - 当前统计: facts=6，projects=1，inbox hermes=6 / openclaw=3 / future-agent=0。
  - shared skills manifest 当前为简单路径列表，共 4 项。
- 结论: 结构健康，但治理层仍偏人工。

### Step 1：补齐 inbox → curated 晋升协议
- 状态: ✅ 已完成
- 完成时间: 2026-04-25
- 实际改动:
  - `docs/promote-protocol.md`
  - `docs/promote-log-template.md`
  - `scripts/promoter.py` 增加 `--scan-promote-candidates` 候选扫描。
- 验证结果:
  - `python3 scripts/promoter.py --dry-run --scan-promote-candidates --recent-limit 10`: pass
  - `python3 scripts/verify_bridge.py`: pass
- 要落地:
  - `docs/promote-protocol.md`
  - `docs/promote-log-template.md`
  - `scripts/promoter.py` 增加 `--scan-promote-candidates` dry-run 候选扫描能力。
- 验收:
  - 扫描 inbox 后输出候选，不写 curated。
  - 每条候选包含 source path、agent、evidence、decision、suggested target。
  - OpenClaw reflection / dreams / 低置信内容默认只能进入 review，不自动晋升。
  - `python3 scripts/promoter.py --dry-run --scan-promote-candidates` exit 0。
  - `python3 scripts/verify_bridge.py` 仍 exit 0。

### Step 2：增强 verify_bridge.py 治理校验
- 状态: ✅ 已完成
- 完成时间: 2026-04-25
- 实际改动:
  - `scripts/verify_bridge.py` 新增 governance / promotion_backlog / future_agent_readiness / runtime_retention 输出。
  - shared skills manifest 元数据校验兼容旧格式并输出 warnings。
- 验证结果:
  - `python3 scripts/verify_bridge.py`: pass，`ok=true`，`warnings=[]`，`errors=[]`。
- 要落地:
  - 增加 governance section，检查协议文档是否存在。
  - 增加 promotion_backlog section，展示 inbox backlog。
  - 增加 future_agent_readiness section。
  - 增加 skills_metadata section，兼容旧 manifest 但给出 warning。
- 验收:
  - 输出新增 section。
  - 当前健康结构仍 ok=true；治理缺口以 warnings 表达。

### Step 3：future-agent 接入包
- 状态: ✅ 已完成
- 完成时间: 2026-04-25
- 实际改动:
  - `inbox/future-agent/README.md`
  - `runtime/future-agent/README.md`
  - `prefill/future-agent-shared-memory.json`
- 验证结果:
  - `python3 scripts/verify_bridge.py`: `future_agent_readiness.ok=true`。
- 要落地:
  - `inbox/future-agent/README.md`
  - `runtime/future-agent/README.md`
  - `prefill/future-agent-shared-memory.json`
- 验收:
  - future-agent 有明确读取顺序、写入边界、smoke test 格式。
  - 不要求立刻生成真实 daily；只提供接入契约。

### Step 4：shared skills 元数据化
- 状态: ✅ 已完成
- 完成时间: 2026-04-25
- 实际改动:
  - `capabilities/manifests/shared-skills.yaml` 升级为 version 2。
  - 4 个 shared skill 均补齐 id/path/version/status/agents/owner/last_reviewed。
- 验证结果:
  - `python3 scripts/verify_bridge.py`: `shared_skills_manifest.metadata_ok=true`。
- 要落地:
  - 更新 `capabilities/manifests/shared-skills.yaml`。
- 验收:
  - 兼容现有 4 个 skill。
  - 后续 verify 能校验路径存在与元数据完整性。

### Step 5：维护脚本副作用隔离
- 状态: ✅ 已完成
- 完成时间: 2026-04-25
- 实际改动:
  - `docs/maintenance.md`
  - `scripts/daily_maintenance.sh` 支持 `SHARED_ONLY=1`、`DRY_RUN=1`、`RUN_KB_SYNC=0`。
- 验证结果:
  - dry-run / shared-only 模式会跳过 KB sync，不触发外部知识库提交。
- 要落地:
  - `docs/maintenance.md`
  - `scripts/daily_maintenance.sh` 支持更清楚的执行模式。
- 验收:
  - shared-hub 自检与外部知识库 git sync 解耦。
  - dry-run 或 shared-only 模式不会触发 KB commit。

### Step 6：状态字段统一
- 状态: ✅ 已完成
- 完成时间: 2026-04-25
- 实际改动:
  - `docs/status-schema.md`
  - `curated/memory/projects/shared-hub-v2.md` 区分基础设施完成度与治理运营成熟度。
- 验证结果:
  - 项目文档不再用单一 100% 掩盖治理运营待办。
- 要落地:
  - `docs/status-schema.md`
  - 更新 `curated/memory/projects/shared-hub-v2.md`。
- 验收:
  - “100%”只代表 v2 基础设施完成，不掩盖治理运营待办。

### Step 7：runtime retention
- 状态: ✅ 已完成
- 完成时间: 2026-04-25
- 实际改动:
  - `docs/runtime-retention.md`
  - `scripts/verify_bridge.py` 输出 `runtime_retention`，按 agent 报告 runtime size。
- 验证结果:
  - `python3 scripts/verify_bridge.py`: `runtime_retention.ok=true`；策略为 report-only，不默认删除。
- 要落地:
  - `docs/runtime-retention.md`
- 验收:
  - 只作用 runtime；不触碰 curated / inbox。
  - 先报告，默认不删除。

## 状态更新规则

每完成一个 step，必须更新本文件：
- 将对应状态从 `⏳ 进行中` 改为 `✅ 已完成`。
- 将下一步从 `⏳ 待开始` 改为 `⏳ 进行中`。
- 在对应 step 下补充完成时间、实际改动文件、验证命令与结果。

## 第一轮验收出口

第一轮已完成 Step 1 - Step 7，并保证：
- `python3 scripts/promoter.py --dry-run --scan-promote-candidates --recent-limit 10` 通过。
- `python3 scripts/verify_bridge.py` 通过。
- 计划文件状态已同步更新。

