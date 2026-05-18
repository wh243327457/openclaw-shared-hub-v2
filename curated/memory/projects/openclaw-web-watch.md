# OpenClaw 网页/公众号采集系统

## 项目概览
- 状态：PLANNED
- 定位：OpenClaw 专属的独立网页/公众号采集系统
- 目标：自动浏览高价值网站、扫描公开公众号文章、做初筛摘要，并把可审计结果交给 Hermes 决定是否晋升
- 归属：shared 中台 v2 / cross-agent capability
- 更新时间：2026-05-17
- 真相源路径：`shared/curated/memory/projects/openclaw-web-watch.md`
- runtime 工作区：`shared/runtime/openclaw/web-watch/`

## 一句话结论
这是一个 **OpenClaw 负责采集、Hermes 负责审计、shared 负责沉淀** 的独立闭环；它适合做网站巡检、文章初筛、趋势扫描和公开公众号内容摘要，但不承担最终知识裁决。

## 设计目标
1. 自动发现高价值网页和公开文章。
2. 对内容做结构化提取：标题、链接、时间、正文、来源、标签、质量评分。
3. 对公众号文章采用“能抓则抓、抓不到就记录失败原因”的保守策略。
4. 由 Hermes 做真伪、完整性和长期价值审计。
5. 通过 curated/inbox/runtime 三层分流，避免把噪音写成长期真相。

## 核心职责边界

| 组件 | 职责 | 不负责 |
|---|---|---|
| OpenClaw | 浏览网页、抓取正文、初筛、生成候选摘要 | 最终晋升判断 |
| Hermes | 审计质量、判断长期价值、决定是否写入 curated | 大量网页手工巡检 |
| shared | 承载 inbox / runtime / curated / skills | 执行抓取逻辑 |

## 能力范围

### 可以做
- 扫网站首页、专题页、RSS、博客、资讯页
- 检索关键词并筛选结果
- 读取公开可访问的公众号文章
- 抽取正文并生成摘要
- 对候选内容打分、分类、去重
- 记录失败页面与原因

### 适合的来源
- 技术博客
- AI / 工程 / 产品 / 研究类网站
- 行业资讯页
- GitHub 相关外部文章
- 公开可访问的公众号文章链接

### 边界
- 需要登录、强反爬、只能微信内查看的页面不保证稳定
- 抓不到时必须记录失败原因，不允许编造正文
- 最终知识裁决不由 OpenClaw 自己完成

## 总体流程

```text
定时触发 / 手动触发
  -> Hermes 生成当天采集目标
  -> OpenClaw 浏览与抓取
  -> 结构化提取与初筛
  -> 写入 shared/inbox/openclaw/daily/YYYY-MM-DD.md
  -> Hermes 审核
  -> 通过则晋升 curated/memory
  -> 必要时补充 runtime 反馈与模板修正
```

## 状态机

```text
IDLE
  -> PLAN_TARGETS
  -> FETCH_PAGES
  -> EXTRACT_CONTENT
  -> SCORE_AND_FILTER
  -> WRITE_RAW_REPORT
  -> HERMES_REVIEW
  -> PROMOTE_OR_REJECT
  -> FEEDBACK_TEMPLATES
  -> IDLE
```

### 状态说明

| 状态 | 输入 | 动作 | 产物 | 验收 |
|---|---|---|---|---|
| PLAN_TARGETS | 白名单、关键词、频率 | 生成今日目标列表 | target plan | 目标明确且可执行 |
| FETCH_PAGES | 目标列表 | 打开页面、收集原文 | raw page data | 有来源链接与时间 |
| EXTRACT_CONTENT | 原文 | 提取标题、正文、时间 | structured items | 字段完整 |
| SCORE_AND_FILTER | structured items | 评分、去重、过滤 | candidate list | 可解释 |
| WRITE_RAW_REPORT | candidate list | 写入 inbox | raw report | 路径正确，格式稳定 |
| HERMES_REVIEW | raw report | 审计质量与价值 | review result | PASS/REJECT 清晰 |
| PROMOTE_OR_REJECT | review result | 决定晋升或退回 | curated update or backlog | 无越级晋升 |
| FEEDBACK_TEMPLATES | failure reasons | 记录失败模式 | template feedback | 可用于下次优化 |

## 目录结构

```text
shared/
├── inbox/openclaw/daily/
│   └── YYYY-MM-DD.md
├── runtime/openclaw/web-watch/
│   ├── state.json
│   ├── plan.md
│   ├── instruction.md
│   ├── report-template.md
│   └── failures/
└── curated/memory/projects/
    └── openclaw-web-watch.md
```

## 报告产物规范

OpenClaw 每次输出都应包含：
1. 今日结论
2. 候选来源表
3. 高价值文章列表
4. 无法抓取 / 失败列表
5. 值得继续跟踪的主题
6. 建议 Hermes 审核项
7. 原始链接清单

## 公众号文章策略

| 情况 | 处理方式 |
|---|---|
| 公开 URL 可直接访问 | OpenClaw 直接抓取并摘要 |
| 需要登录或风控较强 | 记录失败原因，等待人工补充或替换来源 |
| 只有标题/截图/转发文本 | 作为半结构输入，做辅助整理，不伪造正文 |

## 第一版实施范围

### Phase 1：跑通采集
- 维护 10 个以内白名单来源
- 定时访问并提取标题/正文/时间/链接
- 写入 inbox 原始报告

### Phase 2：加筛选
- 用主题相关性、时效性、可复用性打分
- 只保留高价值候选

### Phase 3：接 Hermes 审核
- Hermes 只审价值、真实性、完整性
- 通过后再进 curated

## 共享能力升格判断

此系统后续**很适合**升格为 shared capability，因为它会被 Hermes、OpenClaw 和 future-agent 复用。

升格前提：
- 闭环先跑通
- 报告格式稳定
- 失败模式可审计
- 公众号抓取边界清楚

## 当前结论
这版是 **可落地的最小完整方案**：
- 目标明确
- 职责边界清楚
- 状态机完整
- 目录已经对齐 shared v2
- 公众号内容采用保守抓取策略
- 最终判断权留给 Hermes
