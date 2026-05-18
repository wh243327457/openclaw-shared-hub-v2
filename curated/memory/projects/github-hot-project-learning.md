# GitHub 热门项目每日学习任务状态

## 项目概览
- 状态：黄 / OpenClaw 生成可用，但 shared inbox 桥接、健康检查和日维护兜底正在加固验收
- 当前阶段：补齐 OpenClaw cron run → shared inbox 的桥接脚本、Hermes runtime 状态面板、daily maintenance 兜底执行；随后运行 verify/secret 扫描/cron 检查
- 更新时间：2026-05-01

## 人话结论
2026-05-01 已确认 OpenClaw cron run 本身成功，但当天 shared inbox 与 Obsidian 日报曾出现缺口；因此项目状态临时从绿降为黄。当前加固方向不是重做学习任务，而是把 OpenClaw 原始输出稳定桥接到 shared/inbox/openclaw/daily，并让 Hermes 侧留下可审计的 status、healthcheck 与日志，避免以后“生成成功但共享层缺档”。

## 已确认完成
- [x] OpenClaw 容器内 gateway 可用。
- [x] OpenClaw agent 默认改用 `minimax/MiniMax-M2.7` 后可生成内容。
- [x] 已创建 GitHub 热门项目每日学习 cron job。
- [x] 已收紧 OpenClaw cron 提示词：必须输出 `source_url`、抓取口径、时间窗口、`owner/repo` 与可核验字段。
- [x] 已手动触发二次 cron run，状态 `ok`，生成内容已包含必填字段。
- [x] 已将审计后日报落盘到 `/mnt/d/system/selfSystem/03-学习/技术实践/GitHub 热门项目学习档案/`。
- [x] 已创建跨 Agent shared skill：`research/github-hot-project-learning`。
- [x] 已创建 Hermes cron job `2a82c752d86a`，每日 09:10 执行审计推送。
- [x] 已补 `scripts/openclaw_github_learning_bridge.py`：从 OpenClaw cron JSONL 提取目标日期成功 run，写入 `shared/inbox/openclaw/daily/YYYY-MM-DD.md`，并更新 `runtime/hermes/github-hot-project-learning/status.json`。
- [x] 已补 `scripts/github_learning_healthcheck.py`：检查 OpenClaw run、shared inbox、runtime status、bridge log、Obsidian 日报/审计/索引并输出 JSON 状态面板。
- [x] 已将 GitHub learning bridge/healthcheck 集成进 `scripts/daily_maintenance.sh`，支持 `RUN_GITHUB_LEARNING`、`GITHUB_LEARNING_DATE`、`DRY_RUN` 开关。

## 当前阻塞 / 风险
- Hermes 已尝试委派 Claude Code 执行实现与审查，但当前环境未能稳定找到/运行 Claude Code CLI；实现已由 Hermes 直接接管。
- 2026-05-01 当天需要继续跑验收：py_compile、bridge dry-run/实际写入、healthcheck、verify_bridge、bash -n、git diff --check、secret 扫描与 cron 检查。
- OpenClaw 自身 delivery 仍有 `Channel is required (no configured channels detected)` 风险，但 Hermes 微信推送链路已覆盖；当前重点是 shared inbox/状态面板连续性。

## 下一步建议
1. 先完成 2026-05-01 本地验收，确认 bridge 能补齐当天 shared inbox。
2. 若验收通过，配置或确认每日 08:35 左右执行 bridge/healthcheck；当前 `daily_maintenance.sh` 已作为兜底入口。
3. 连续观察 1-3 天：OpenClaw 08:30 生成、bridge/healthcheck、Hermes 09:10 审计推送是否全链路稳定。

## 相关文件
- 当前加固计划：`/home/vany/agent/.openclaw/shared/docs/plans/2026/05/2026-05-01-openclaw-continuous-learning-hardening.md`
- 历史计划：`/home/vany/agent/.openclaw/shared/docs/plans/2026/04/2026-04-28-github-hot-project-learning-pipeline.md`
- Bridge：`/home/vany/agent/.openclaw/shared/scripts/openclaw_github_learning_bridge.py`
- Healthcheck：`/home/vany/agent/.openclaw/shared/scripts/github_learning_healthcheck.py`
- Daily maintenance：`/home/vany/agent/.openclaw/shared/scripts/daily_maintenance.sh`
- Skill：`/home/vany/agent/.openclaw/shared/capabilities/skills/research/github-hot-project-learning/SKILL.md`
- 知识库入口：`/mnt/d/system/selfSystem/03-学习/技术实践/GitHub 热门项目学习档案/00-总览索引.md`
