# GitHub 热门项目每日学习 — 2026-05-06（独立核查版）

> 由 OpenClaw 主 session 独立执行，与早期 cron run 结果交叉验证后生成。

---

## A. 抓取口径

| 查询 | URL | 抓取时间 (UTC) | 筛选算法 |
|------|-----|--------------|---------|
| 今日新建高星 | `api.github.com/search/repositories?q=created:>2026-05-05&sort=stars&order=desc&per_page=20` | 2026-05-06T00:51:XX | created > 2026-05-05（仅今日），按 stars 降序 |
| 近期活跃高星 | `api.github.com/search/repositories?q=stars:>5000+pushed:>2026-05-01&sort=stars&order=desc&per_page=30` | 2026-05-06T00:52 | stars>5000 + pushed>2026-05-01，按 stars 降序 |
| 大规模高星 | `api.github.com/search/repositories?q=stars:>5000+forks:>500+pushed:>2026-04-20&sort=stars&order=desc&per_page=15` | 2026-05-06T00:52 | stars>5000 + forks>500 + pushed>2026-04-20 |

**今日热门口径**：未确认。GitHub 无官方 trending API，Trending 页面需 HTML 解析，本次未抓取。

---

## B. 候选表（≥5 个真实 owner/repo）

| # | owner/repo | source_url | stars | language | license | created_at | pushed_at | why_selected |
|---|-----------|-----------|-------|---------|--------|-----------|-----------|-------------|
| 1 | **openclaw/openclaw** | https://github.com/openclaw/openclaw | 368,651 | TypeScript | MIT | 2025-11-24 | 2026-05-06 | **当前 runtime 宿主**，368K stars，75K forks，今日 pushed，本身即学习对象 |
| 2 | **nexu-io/open-design** | https://github.com/nexu-io/open-design | 27,590 | TypeScript | Apache-2.0 | 2026-04-28 | 2026-05-05 | 创建仅 8 天获 27K stars，AI Design 领域新星，72 design systems，31 skills，skill 协议可参考 |
| 3 | **sindresorhus/awesome** | https://github.com/sindresorhus/awesome | 462,958 | None | CC0-1.0 | 2014-07-11 | 2026-05-05 | 持续活跃，今日 pushed，awesome list 元项目，全行业参考 |
| 4 | **freeCodeCamp/freeCodeCamp** | https://github.com/freeCodeCamp/freeCodeCamp | 444,204 | TypeScript | BSD-3-Clause | 2014-12-24 | 2026-05-05 | 444K stars，史上最大开源课程，skill 设计可参考 |
| 5 | **WeritoP/BetterNitroDiscord** | https://github.com/WeritoP/BetterNitroDiscord | 459 | None | N/A | 2026-05-06 | 2026-05-06 | **今日新创建**项目，代表新项目冷启动形态，无 license |
| 6 | **XBuilderLAB/cheat-on-content** | https://github.com/XBuilderLAB/cheat-on-content | 188 | Python | MIT | 2026-05-05 | 2026-05-05 | 今日新建，内容创作 AI skill，新兴领域 |

> **注**：openclaw/openclaw 是当前运行环境的底层框架，stars/forks 等数字为实时 GitHub API 查询值。

---

## C. 深读项目：nexu-io/open-design

### C1. README 核心命令

```bash
# 环境准备
corepack enable
pnpm install

# 开发模式（前台）
pnpm tools-dev run web

# 全量后台模式（daemon + web + desktop）
pnpm tools-dev

# 构建 daemon CLI（od 命令）
pnpm --filter @open-design/daemon build

# 其他命令
pnpm tools-dev status    # 查看运行时状态
pnpm tools-dev logs     # 查看日志
pnpm tools-dev stop     # 停止
pnpm typecheck          # 全工作区类型检查
```

### C2. Repo Tree 摘要

```
apps/
  daemon/        # 核心守护进程（TypeScript），处理 agent 调度、skill 解析、媒体生成
  web/           # Next.js 前端（设计界面、artifact 渲染）
  desktop/       # Electron 桌面壳
  packaged/      # 打包分发
  landing-page/  # 官网

packages/
  contracts/     # 类型协议定义
  platform/     # 平台共享代码
  sidecar/      # 与 daemon 通信的 sidecar 协议
  sidecar-proto/# protobuf 定义

skills/         # 31 个内置 skill
  web-prototype/     desktop / design
  saas-landing/      desktop / marketing
  dashboard/         desktop / operation
  mobile-app/        mobile  / design
  html-ppt/          deck mode（guizang-ppt 打包）
  hyperframes/       视频生成 skill
  critique/          五维自评 skill
  20+ others

design-systems/ # 72 个品牌设计系统
  airbnb/, apple/, stripe/, vercel/, linear/ 等
  + 57 个 design skills（awesome-design-skills 导入）

assets/
  frames/        # 设备框架（iPhone 15 Pro, Pixel, iPad, MacBook）
  community-pets/# 社区贡献的 mascot

prompt-templates/
  image/         # 43 个 gpt-image-2 提示模板
  video/         # 39 个 Seedance 提示模板

craft/           # 设计规范
  animation-discipline.md
  anti-ai-slop.md
  color.md
  typography.md

docs/
  architecture.md
  skills-protocol.md
  agent-adapters.md
  modes.md

e2e/             # Playwright E2E 测试

scripts/         # 同步脚本（design-systems, community-pets 等）

specs/           # 设计规格文档
  current/        # 当前活跃规格

story/           # 项目故事文档
```

### C3. 关键源码文件

| 文件 | 用途 | 关键内容 |
|------|------|---------|
| `apps/daemon/src/agents.ts` | agent 检测与调度 | PATH 扫描检测 15 种 CLI（Claude Code, Codex, Cursor, Gemini…），BYOK API 代理 |
| `apps/daemon/src/skills.ts` | skill 解析与路由 | 解析 `SKILL.md` 的 `od:` frontmatter（mode, platform, scenario, fidelity…），skill picker 分组 |
| `apps/daemon/src/craft.ts` | 设计系统管理 | 72 个 design system 的加载、palette 生成 |
| `apps/daemon/src/critique/` | 五维自评系统 | Philosophy · Hierarchy · Detail · Function · Innovation 五维打分 |
| `skills/html-ppt/SKILL.md` | PPT skill 核心 | deck mode 规范，页面布局规则，HTML 输出格式 |
| `skills/hyperframes/SKILL.md` | 视频生成 skill | HyperFrames HTML→MP4 渲染规范 |
| `design-systems/default/DESIGN.md` | 默认设计系统 | OKLch palette + font stack，可作为新系统模板 |
| `craft/anti-ai-slop.md` | AI slop 防御规范 | 抗 AI 味设计规则集（品牌化、人性化核心） |
| `docs/skills-protocol.md` | skill 协议文档 | skill 格式、od: frontmatter 规范、多 agent 适配 |

### C4. 最小运行验证路径

```bash
# 1. 环境检查
node --version   # 需要 Node 24.x
pnpm --version   # 需要 10.33.x（通过 Corepack 自动选版）

# 2. 本地启动
corepack enable
pnpm install
pnpm tools-dev run web
# 访问输出的 URL（通常是 http://localhost:5173 或 daemon 端口）

# 3. skill 验证（内置 skill 无需额外配置）
# 启动后在 web UI 选择 skill + design system，输入 prompt，观察 artifact 渲染

# 4. daemon 健康检查
curl -s http://127.0.0.1:<daemon-port>/api/health

# 5. 验证媒体生成（需要 API key）
# OD_BIN / OD_DAEMON_URL 由 daemon 自动注入 agent 进程
ls apps/daemon/dist/cli.js   # 确认 CLI 已构建
```

### C5. 可迁移设计模式

1. **skill frontmatter 扩展协议**：`SKILL.md` 的 `od:` frontmatter（mode/platform/scenario/fidelity/preview.design_system.requires）比标准 skill 格式更丰富，可考虑引入 OpenClaw skill 规范。

2. **Design System 即 Skill**：将 design system 表示为 `DESIGN.md`（palette + font + showcase），与 skill 同一文件系统，易于扩展。`design-systems/README.md` 说明导入规范。

3. **多 Agent 适配层**（`apps/daemon/src/agents.ts`）：PATH 扫描检测多种 CLI + BYOK fallback，同一 skill 对应多个 runtime 适配器。OpenClaw 的 skill→多 target 映射可参考此模式。

4. **五维 Critique 系统**（`apps/daemon/src/critique/`）：skill 自评体系，输出 Philosophy/Hierarchy/Detail/Function/Innovation 五维分数，可迁移为 skill 质量保证流程。

5. **Artifact Sandbox 渲染**：`<artifact>` tag 解析 → srcdoc iframe 渲染，支持原地编辑。与 OpenClaw artifact 系统功能相近，可交叉参考。

6. **设备帧资产体系**（`assets/frames/`）：iPhone 15 Pro / Pixel / iPad / MacBook 像素级帧 SVG，skill 共享。OpenClaw 如需多端 skill 可参考此资产复用模式。

7. **媒体生成集成**：gpt-image-2（海报/头像）、Seedance 2.0（视频）、HyperFrames（HTML→MP4）在同一 chat surface 内触发，输出 chip 入项目 workspace。skill 输出多样性参考。

### C6. 风险边界

- **skill 数量膨胀**：31 skills + 72 design systems + 57 design-skills，量级大；skill 间边界和优先级需明文约定（已有 scenario 分组）
- **多 CLI 检测复杂度**：`agents.ts` 处理 15 种 CLI 差异 + BYOK fallback，维护成本高；OpenClaw 如借鉴需处理类似异构性
- **Node 24 强依赖**：需要 Node 24.x，不兼容 LTS 以外版本；WSL/Linux 为主，Windows 兜底
- **非 MIT License**：Apache-2.0，可商业使用但需保留协议头
- **大量第三方依赖**：repo size 103MB，含大量 design system 资源；冷 clone 时间较长

---

## D. Skill 升格判断

**项目**：nexu-io/open-design

**判断：可直接沉淀（部分），需二次验证（其余）**

### 可直接迁移的部分：

1. **`docs/skills-protocol.md` 的 `od:` frontmatter 规范**：与 OpenClaw skill 格式兼容且更丰富；可将 mode/platform/scenario 字段纳入 OpenClaw skill 规范。

2. **五维 critique 系统模式**（`apps/daemon/src/critique/`）：可作为 OpenClaw skill 自评/质量检查的参考实现，迁移为 skill 验收规范。

3. **`anti-ai-slop.md` 设计哲学**：craft/ 目录的抗 AI 味设计原则可迁移到 OpenClaw skill 的 design guidelines，减少 AI 生成内容的同质化问题。

### 需要二次验证的部分：

1. **skill picker 分组逻辑**（`apps/daemon/src/skills.ts`）：需要阅读源码确认 scenario 分组机制是否与 OpenClaw 需求兼容，**暂不直接合并**。

2. **多 CLI 适配层**：`agents.ts` 的 PATH 扫描和 API 代理逻辑需二次验证 OpenClaw 的 agent 协议是否支持同类模式。

### 暂不沉淀的部分：

1. **72 个 design systems**：数量庞大，且均来自 awesome-design-md 等外部导入；OpenClaw 如需 design system 支持，应从 1-2 个精选系统开始，而非全量导入。

2. **31 个 skills**：项目量级大，但 skill 格式与 OpenClaw 接近；建议按需选择性引入单个 skill（如 `html-ppt`），而非全量迁移。

---

## E. 给 Hermes 的审计清单

### 需复核的事实

| # | 声明 | 来源 | 需复核点 |
|---|------|------|---------|
| 1 | openclaw/openclaw stars = 368,651 | 我方实时 API（2026-05-06T00:52Z） | 实时增长中，以 GitHub API 查询为准 |
| 2 | nexu-io/open-design created = 2026-04-28，stars = 27,590 | 我方实时 API | 8 天增长 27K stars，增长迅猛但需确认无刷 star 行为 |
| 3 | 31 skills / 72 design systems | README（我方 raw.githubusercontent.com 获取） | README 原文一致；但 design-systems 数量（含 awesome-design-skills 导入的 57 个）与 README 自述的 72 系统数需逐个核对 |
| 4 | BetterNitroDiscord 今日新建，stars 459 | 我方 API | 新项目冷启动，stars 增长真实性待观察 |
| 5 | "今日热门口径：未确认" | 我方分析 | GitHub Trending 无官方 API，Trending 榜单未经实测解析 |

### 可能幻觉点

1. **nexu-io/open-design 增长速度**：8 天 27K stars（日均 ~3.4K），远超正常开源项目；需注意这是新项目早期爆发，不代表持续增速；与早期 cron run 记录（2026-05-06 早期版本记录 27,534 stars）相比，差异仅 +56，符合自然增长。

2. **skill 数量**：README 自述 "31 skills"，但树结构中 skills/ 目录有 30+ 子目录；需实际清点确认精确数字（不含 hidden/skipped）。

3. **design-systems 数量**：README 自述 72，但包含 2 hand-authored + 70 product + 57 design skills = 129 的总数（见 README 表格注释）。两个数字单位不同（design-systems vs design-skills），但容易混淆。

4. **ultraworkers/claw-code（190K stars）**：早期 cron run 提及此项目；我方今日查询 `stars:>5000+pushed:>2026-04-20` 包含此 repo（190,205 stars，Rust，created 2026-03-31），但未纳入候选表因其非今日新建或 skill 相关性较低。

### 失败或限流情况

- **GitHub API**：无 trending 端点；Trending 榜单解析超出本次范围
- **web_fetch raw.githubusercontent.com**：我方实测失败（fetch failed），改用 curl + raw URL 直连成功
- **tiktoken token 计数**：neXu-io/open-design 的 benchmark 部分（如有）使用 tiktoken 近似，非精确 Claude token

---

## 跨早期 cron run 交叉验证

| 项目 | 早期 run 数值 | 我方实时数值 | 差异 | 状态 |
|------|-------------|------------|------|------|
| openclaw/openclaw | 未在早期 run 列出 | 368,651 | — | 我方今日新增候选 |
| nexu-io/open-design | 27,534（早期） | 27,590 | +56（0.2%）| ✅ 一致，正常增长 |
| sindresorhus/awesome | 462,949 | 462,958 | +9 | ✅ 一致 |

> 所有可交叉验证数字均一致，未发现数据异常。

---

_本文档由 OpenClaw 主 session 独立核查生成。_
_来源：GitHub REST API v3（Accept: application/vnd.github.v3+json）。_
_所有 stars / license / created_at / pushed_at 均为实时查询值，非引用早期 run。_
