# GitHub 热门项目每日学习流水线 - 2026-05-11

---

## A. 抓取口径

| 字段 | 值 |
|------|-----|
| **查询 URL（Trending）** | `https://github.com/trending` |
| **查询 URL（星标搜索）** | `https://api.github.com/search/repositories?q=stars%3A%3E1000+pushed%3A%3E2026-05-09&sort=stars&order=desc` |
| **抓取时间** | 2026-05-11T01:13 UTC |
| **筛选算法** | ① GitHub Trending 页面抓取热榜项目（按今日 star 增量排序）；② GitHub Search API 补充星标 >1000 且近期有 push 的项目；双重口径交叉验证 |
| **口径说明** | Trending 热榜口径未确认（GitHub 未公开算法，可能是 24h 星标增量）；Search API 为 stars 排序、时间窗口 2 天内，符合硬性约束 |

---

## B. 候选表（真实 owner/repo）

| # | owner/repo | source_url | stars | language | license | created_at | pushed_at | why_selected |
|---|---|---|---|---|---|---|---|---|
| 1 | bytedance/UI-TARS-desktop | https://github.com/bytedance/UI-TARS-desktop | 32,131 | TypeScript | Apache-2.0 | 2025-01-19 | 2026-04-29 | 今日热榜 669⭐，字节 multimodal AI Agent 桌面应用栈，双子项目含 Agent TARS CLI + UI-TARS Desktop |
| 2 | anthropics/financial-services | https://github.com/anthropics/financial-services | 18,843 | Python | Apache-2.0 | 2026-02-23 | 2026-05-09 | 今日热榜 1,449⭐，Anthropic 官方金融领域 Agent 参考实现，2 个月内新建但爆发力强 |
| 3 | addyosmani/agent-skills | https://github.com/addyosmani/agent-skills | 38,429 | Shell | MIT | 2026-02-15 | 2026-05-10 | 今日热榜 1,065⭐，Google 工程师产出，为 AI 编码 Agent 提供生产级工程技能集 |
| 4 | CloakHQ/CloakBrowser | https://github.com/CloakHQ/CloakBrowser | 4,735 | Python | MIT | 2026-02-22 | 2026-05-10 | 今日热榜 496⭐，反爬指纹黑科技，Playwright 替代方案，30/30 bot 检测全过 |
| 5 | playcanvas/supersplat | https://github.com/playcanvas/supersplat | 6,819 | TypeScript | MIT | 2023-10-19 | 2026-05-08 | 今日热榜 579⭐，3D Gaussian Splat 编辑器，Web 前沿可视化方向 |
| 6 | decolua/9router | https://github.com/decolua/9router | 7,297 | JavaScript | MIT | 2026-01-05 | 2026-05-10 | 今日热榜 803⭐，聚合 40+ AI provider 的免费 coding 路由方案，自动 fallback |

---

## C. 深读项目：bytedance/UI-TARS-desktop

### README 核心命令

```bash
# npx 启动
npx @agent-tars/cli@latest

# 全局安装（需 Node >= 22）
npm install @agent-tars/cli@latest -g

# 运行（Volcengine provider + 豆包模型）
agent-tars --provider volcengine --model doubao-1-5-thinking-vision-pro-250428 --apiKey your-api-key

# 运行（Anthropic provider）
agent-tars --provider anthropic --model claude-3-7-sonnet-latest --apiKey your-api-key
```

桌面应用安装：
```bash
brew install --cask ui-tars   # macOS via Homebrew
# 或从 https://github.com/bytedance/UI-TARS-desktop/releases/latest 下载
```

### repo tree 摘要（主要目录）

```
bytedance/UI-TARS-desktop/
├── apps/
│   └── ui-tars/              # Electron 桌面应用主体
│       ├── resources/icon.png
│       └── images/           # UI 截图资源
├── packages/
│   └── @agent-tars/          # CLI 核心 npm 包
│       └── cli/              # 命令行入口
├── docs/                     # 文档（quick-start.md, setting.md, sdk.md, deployment.md）
├── .github/ISSUE_TEMPLATE/   # Issue 模板
├── README.md
├── CONTRIBUTING.md
└── package.json (monorepo workspaces)
```

**核心技术栈**：TypeScript + Electron + Node.js >= 22  
**模型支持**：UI-TARS-1.5（HuggingFace 部署）、Doubao-1.5-UI-TARS（VolcEngine Ark）

### 关键源码文件

| 文件 | 作用 |
|------|------|
| `apps/ui-tars/src/` | Electron 主进程，GUI Agent 驱动 |
| `packages/@agent-tars/cli/src/` | CLI 核心逻辑，provider 抽象层 |
| `docs/quick-start.md` | 快速上手文档（含本地/远程 operator 启动方式） |
| `docs/sdk.md` | 跨平台 GUI 自动化 SDK 说明 |
| `README.md` | 入口文档，双子项目概述 |

### 最小运行验证路径

```
1. 安装 Node.js >= 22
2. npm install -g @agent-tars/cli@latest
3. 申请 VolcEngine API Key（https://console.volcengine.com/ark/）
4. agent-tars --provider volcengine --model doubao-1-5-thinking-vision-pro-250428 --apiKey YOUR_KEY
5. 输入自然语言指令（如"帮我打开 VS Code 的自动保存功能"）
```

### 可迁移设计模式

1. **Provider 抽象层**：CLI 支持多模型 provider（Volcengine/Anthropic/OpenAI），新 provider 只需实现 provider interface，适合 OpenClaw 工具链扩展
2. **Event Stream 协议**：用流式事件驱动 Context Engineering，Agent UI 可订阅，B/S 分离，适合 MCP 工具事件上报
3. **MCP 协议集成**：内核 build on MCP，支持 mounting 外部 MCP Servers，标准可插拔
4. **Monorepo 结构**：`apps/` + `packages/` workspaces，适合多端（CLI/Desktop/Web）共享核心逻辑

### 风险边界

- **平台依赖**：桌面应用需 Chrome/Edge/Firefox，macOS 需开启 Accessibility + Screen Recording 权限
- **远程 operator 已停服**：文档明确写"Remote Operator 服务将于 2025-08-20 终止"，需自建或用 Volcano Engine OS Agent
- **多显示器未支持**：UI-TARS-desktop 当前仅支持单显示器环境
- **模型 API 费用**：本地 operator 需要调用云端模型 API，存在成本

---

## D. Skill 升格判断

### 候选 Skill：MCP Provider 动态加载模式

**判断结果**：需要二次验证

**理由**：
- `bytedance/UI-TARS-desktop` 的 Provider 抽象层设计清晰，OpenClaw 已有 MCP 工具生态，理论上可迁移
- 但该设计依赖 `@agent-tars/cli` 的内部 provider interface，需验证其是否稳定、是否开放 extension point
- 当前 skill-creator 流程适合沉淀标准技能，但这种"动态 provider 加载"属于架构模式，需要示例代码验证可操作性

**下一步**：
- 读取 `packages/@agent-tars/cli/src/` 源码，确认 provider interface 定义
- 若 interface 稳定，沉淀为 `skill-mcp-dynamic-provider`

---

### 候选 Skill：Agent Event Stream 订阅模式

**判断结果**：可直接沉淀

**理由**：
- Event Stream 驱动设计独立，不强依赖具体 provider，适合 OpenClaw 的工具上报场景
- 文档清晰，有 Web UI + CLI 双重消费示例，可直接拆解为 skill 设计文档

---

## E. 给 Hermes 的审计清单

### 需要复核的事实

| 事实 | 风险级别 | 说明 |
|------|----------|------|
| `bytedance/UI-TARS-desktop` stars = 32,131 | 中 | trending 页面显示 32,131 今日抓取；API 同时返回 32,131，两处一致；今日增量 669⭐ 来自 trending 页面文本，需复核 trending 算法是否准确 |
| `anthropics/financial-services` description = null | 低 | API 返回 description: null，Trending 页面也未显示描述，属实；但这可能影响 why_selected 判断 |
| Remote Operator 服务终止时间 2025-08-20 | 中 | 文档原文，需确认此日期是否已过（当前 2026-05-11，已过期约 9 个月）；若无后续替代声明，可能存在功能缺失 |
| `addyosmani/agent-skills` language = Shell | 低 | 看起来像文档类 repo 但被标为 Shell，可能是脚本类工具集，需人工确认 |
| `playcanvas/supersplat` 创建于 2023-10-19 | 低 | 属实在线上有活跃开发的成熟项目，但相对其他项目更老，与"今日热门"关联可能偏弱 |

### 可能幻觉点

1. **今日星标增量**：`669 stars today`、`1,449 stars today` 等数据来自 trending 页面渲染文本，未经 API 数值复核，真实增量可能略有偏差
2. **Trending 排序口径**：GitHub 未公开 trending 算法，可能是 24h 星标增量（与 `stars_today` 显示一致），但未 100% 确认
3. **Repo tree 摘要**：递归 tree API 被截断（750KB truncation），主要目录结构来自 README 和少量 API 数据，可能遗漏重要子目录

### 失败或限流情况

- **Tree API truncated**：递归 tree 被 GitHub 截断至 ~750KB，未能获取完整 repo 结构；补充方案：分别对 `apps/`、`packages/` 子目录单独调用 tree API
- **jq 不可用**：容器内无 `jq` 命令，已用 Python 替代解析 JSON，正常
- **API rate limit**：未触发，当前仅 6 次 repo 查询 + 1 次 search + 1 次 trending，均在未认证限制（60次/小时）内

---

_报告生成时间：2026-05-11T01:14 UTC | 抓取工具：web_fetch + exec(curl)_