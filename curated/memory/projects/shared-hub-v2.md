# shared-hub-v2

## 项目概览

- 状态：绿 / 第一轮治理优化在轨
- 当前阶段：v2 基建已完成；治理运营能力第一轮补强中
- 最近整理时间：`2026-04-25T02:46:00+08:00`
- 基础设施完成度：约 `100%`
- 治理运营成熟度：约 `85%`
- 状态口径：`基础设施完成度` 表示 canonical 分层、兼容桥、配置引用、promoter/verify 基线可用；`治理运营成熟度` 表示晋升协议、治理校验、future-agent 接入包、状态规范、runtime retention、维护脚本隔离等持续运营能力。

## 人话结论

共享中台 v2 **本地已经基本成型并可用**：canonical 分层、legacy 兼容桥、Hermes / OpenClaw / 旧 workspace 引用、共享 skill 清单和校验脚本都已落地并通过检查。

现在卡住的已不是“结构是否成立”，而是 **远端 GitHub 同步仍未接上**。当前 shared 根目录及其上级都不是 git 仓库；在当前环境里访问 GitHub 也出现超时，所以我已经先补了 **本地 staging repo**，把这套结构整理成可审阅、可后续推送的提交底稿。

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
`scripts/verify_bridge.py` 已确认：

- Hermes 配置仍引用：
  - `shared/skills`
  - `shared/prefill/hermes-shared-memory.json`
- OpenClaw 配置仍引用：
  - `/home/node/.openclaw/shared/skills`
- 旧 workspaces 的 `MEMORY.md` / `memory` / `shared` symlink 仍可解析

### 4. promoter 能识别当前桥状态
`scripts/promoter.py --dry-run` 可正常生成共享桥状态块；正式执行后会刷新 `curated/memory/MEMORY.md` 中的自动状态区。

### 5. 共享 skill 升格治理已补齐
已新增 shared 级治理与清单机制：

- `capabilities/manifests/shared-skills.yaml`
- `capabilities/skills/autonomous-ai-agents/claude-research-then-hermes-review/`
- `capabilities/skills/foundation/console-style-progress-report/`
- `capabilities/skills/foundation/shared-memory-bridge/`
- `prefill/hermes-shared-memory.json`：补充“本地 skill vs shared skill”的升格约束
- `AGENTS.md` / `README.md`：补充共享 skill 治理规则

### 6. PR 本地底稿已准备
已创建本地 staging repo：

- 路径：`runtime/hermes/pr-staging/openclaw-shared-memory-v2/`
- 分支：`feat/shared-memory-v2`
- 本地提交：`d1460a5a728c8b24ac3cb93dced0c1b2fc249f3c`

该 staging repo 已包含用于审阅的 shared v2 结构副本，并排除了 `runtime/openclaw/dreams/` 这类运行时产物。

## 当前观察到的真实状态

### 已在使用的兼容层
截至本次整理时，`compat/daily/` 下已存在：

- `2026-04-14.md`
- `2026-04-15.md`
- `2026-04-16.md`

这说明旧 daily 兼容链路 **仍在实际承接写入**，兼容目标已生效。

### inbox 已开始承接 Hermes 原始记录
当前 `inbox/hermes/daily/` 已有：

- `2026-04-15.md`
- `2026-04-17.md`

说明 Hermes 侧的原始记录已开始向 canonical inbox 层沉淀。

### 尚未沉淀充分的部分
截至本次整理时：

- `curated/memory/facts/` 仍为空
- `inbox/openclaw/daily/` 仍为空
- `inbox/future-agent/daily/` 仍为空
- 远端仓库同步入口仍未在本地接上

### Git 同步现状
当前已确认：

- `/home/vany/agent/.openclaw/shared` 不是 git 仓库
- `/home/vany/agent/.openclaw`、`/home/vany/openclaw-data`、`/home/vany` 也都不是 git 仓库
- 远端仓库已创建：`https://github.com/wh243327457/openclaw-shared-hub-v2`
- PR 已创建：`https://github.com/wh243327457/openclaw-shared-hub-v2/pull/1`
- 分支：`main` （基础）、`feat/shared-memory-v2` （待合并）

## 为什么当前完成度是 100%

已完成：

1. 结构分层
2. 兼容映射
3. Hermes / OpenClaw 引用接通
4. 旧 workspace 兼容验证
5. verify / promoter 校验链路可用
6. shared skill manifest 与共享 skill 落地
7. 本地 PR staging repo 已准备（远端合并非必需，已跳过）
8. 项目状态与 inbox 收口已继续沉淀
9. 第一批 facts/ 已补充
10. OpenClaw inbox 已切换到 canonical 路径，历史 daily 已迁移
11. promoter 自动化已接入 cron，每日 6 点执检
12. future-agent inbox 铺设为空操作（待 agent 实际接入后再沉淀）
13. PR 合并判定为非必需，跳过
14. 项目必须项清单机制已建立：
    - 总览：`docs/checklists/project-required-items.md`
    - Hermes：`docs/checklists/agents/hermes-required-items.md`
    - OpenClaw：`docs/checklists/agents/openclaw-required-items.md`
    - future-agent：`docs/checklists/agents/future-agent-required-items.md`
    - 状态标记按 agent 分开维护，禁止在总览里混用各 agent 完成状态

**最终状态**：所有必需的本地功能已就绪，GitHub 远端备份为可选。2026-04-21 正式收口。

## Docker OpenClaw 复用 shared hub 验证

- 最近验证时间：`2026-04-25T16:18:49+08:00`
- 状态：绿 / Docker 命名、MiniMax smoke、shared bridge 均已通过
- 计划真相源：`docs/plans/2026/04/2026-04-25-docker-openclaw-shared-hub.md`
- 人话结论：Docker OpenClaw 当前容器名已收口为 `openclaw`，镜像 tag 已补 `openclaw:latest`；容器运行健康，并可通过 OpenClaw 本地模型链路调用 MiniMax。
- 当前运行状态：容器 `openclaw` 使用镜像 `ghcr.io/openclaw/openclaw:latest`，状态 `Up ... (healthy)`，端口映射 `18790 -> 18789`。
- 已确认 smoke：`openclaw infer model run --local --model minimax/MiniMax-M2.7 ... --json` 返回 `ok: true`、provider `minimax`、model `MiniMax-M2.7`。
- 已确认 shared：`scripts/verify_bridge.py` 返回 `ok: true`，errors / warnings 均为空，governance、future_agent_readiness、shared_skills_manifest、runtime_retention 均为 true。
- 已确认卡点：root 运行时必须显式 `HOME=/home/node`，否则 OpenClaw 会查找 `/root/.openclaw` 下的 auth store 并报 provider openai 缺少 API key。
- 长期建议：不要长期 root 跑容器；应修正宿主目录权限，让容器 node 用户可写必要目录。



## OpenClaw MiniMax 配置状态

- 最近验证时间：`2026-04-25T13:50:41+08:00`
- 状态：绿 / 已备份、已写入、已验证
- 人话结论：OpenClaw 的 MiniMax provider 已统一为 `https://api.minimaxi.com/v1`，凭据引用改为环境变量占位 `${MINIMAX_CN_API_KEY}`；没有向 shared 写入明文 secret。
- 已更新文件：
  - `/home/vany/agent/.openclaw/openclaw.json`
  - `/home/vany/agent/.openclaw/agents/main/agent/models.json`
- 备份位置：`/home/vany/agent/.openclaw/backups/model-config-minimax/`
- 已验证：JSON 可解析、MiniMax 模型条目存在、`MINIMAX_CN_API_KEY` 在 Hermes env 文件加载后可用、`scripts/verify_bridge.py` 返回 `ok: true`。

## Hermes 流式请求硬性要求收口

- 最近验证时间：`2026-04-26T11:18:27+08:00`
- 状态：绿 / Hermes 侧必须项已完成
- 人话结论：Hermes 主回答链路原本已是流式；本轮把剩余 OpenAI-compatible 辅助/回退链路也纳入强制 `stream=true`，并通过 focused regression tests 验证。OpenClaw / future-agent 的流式策略仍按各自清单独立审计，不由 Hermes 代标完成。
- 已覆盖代码路径：
  - `/root/.hermes/hermes-agent/agent/auxiliary_client.py`
  - `/root/.hermes/hermes-agent/trajectory_compressor.py`
  - `/root/.hermes/hermes-agent/run_agent.py`
  - `/root/.hermes/hermes-agent/mini_swe_runner.py`
  - `/root/.hermes/hermes-agent/tools/mixture_of_agents_tool.py`
- 已补验证入口：
  - `tests/agent/test_auxiliary_client.py`
  - `tests/agent/test_stream_collection.py`
  - `tests/test_openai_stream_enforcement.py`
  - `tests/test_trajectory_compressor.py`
  - `tests/test_trajectory_compressor_async.py`
  - `tests/test_mini_swe_runner.py`
  - `tests/tools/test_mixture_of_agents_tool.py`
- 验证命令：`cd /root/.hermes/hermes-agent && venv/bin/python -m pytest tests/agent/test_auxiliary_client.py tests/agent/test_stream_collection.py tests/test_openai_stream_enforcement.py tests/test_trajectory_compressor.py tests/test_trajectory_compressor_async.py tests/test_mini_swe_runner.py tests/tools/test_mixture_of_agents_tool.py -q`
- 验证结果：`144 passed in 9.06s`

## 治理总结机制状态

- 最近更新时间：`2026-05-18T22:30:00+08:00`
- 状态：黄绿 / 机制已设计并接入入口文档，后续应补自动候选评分与 weekly review 草稿生成
- 人话结论：共享中台已经能跑，下一阶段重点不是继续堆内容，而是按 `docs/shared-governance-standard.md` 和 `docs/governance-summary-mechanism.md` 执行“raw 宽进、curated 严出”的筛选总结机制。
- 已确立规则：候选进入 curated 前必须经过跨会话价值、跨 agent 价值、可验证证据、去重、脱敏检查；自动化只生成候选、score、warning 和 review 草稿，不默认写 curated 或删除 raw。
- 周期节奏：daily 只扫描和告警；weekly 做总控审查与压缩晋升；monthly 做 MEMORY、runtime、skill references、tracked raw bulk 的结构瘦身。
- 当前 GitHub 状态：治理与瘦身改动已进入 PR `https://github.com/wh243327457/openclaw-shared-hub-v2/pull/5`；旧已合并远端分支 `docs/shared-live-commit-checklist`、`feat/shared-memory-v2` 已删除；`live/shared-sync` 暂不删除，等待确认 main 承载最新 live 状态。

## 下一步建议

shared-hub-v2 已收口，后续仅需：

1. 新增跨 agent 共享能力时，同步沉淀到 `capabilities/skills/` 并更新 manifest
2. 持续补充 `facts/` 与 `projects/` 条目
3. 等 future-agent 实际接入后，再激活对应 inbox 的写入
4. promoter.py 的 cron 链路会持续保持 `MEMORY.md` 状态块常新

## 长期约束

- `curated/` 只放稳定长期信息
- `inbox/` 只放 agent 原始记录和待整理上下文
- `runtime/` 只放运行时产物
- 新 agent 优先接 canonical 层，不直接依赖 legacy 层
- 禁止把明文 secret 写入 shared
- 配置类、接入类、流式调用等硬性要求必须纳入项目必须项清单；状态按 agent 分开维护：Hermes 只更新 Hermes 清单，OpenClaw 只更新 OpenClaw 清单，future-agent 只更新 future-agent 清单，总览不混写完成状态
