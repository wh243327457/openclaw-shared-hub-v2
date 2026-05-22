# GitHub 热门项目每日学习指令

**生成时间**: {{DATE}} | **来源**: Hermes 审计反馈系统 | **版本**: v1.0

---

## 今日学习目标

{{LEARNING_GOALS}}

---

## 学习范围

### 推荐技术栈
{{TECH_STACK}}

### 推荐领域
{{DOMAINS}}

---

## 必读项目

{{REQUIRED_PROJECTS}}

---

## 产出要求

### 1. 学习报告
**文件**: `shared/inbox/openclaw/daily/YYYY-MM-DD.md`

必须包含：
- 今日结论（一句话总结）
- 项目速览（5-10 个简要列出）
- 深读项目（每个含：一句话判断、解决的问题、架构/实现、可复用经验、可尝试实验、风险边界）
- 经验沉淀（通用经验）
- 明日继续（下一步最小动作）

### 2. 项目卡片
**文件**: `shared/runtime/openclaw/github-learning/projects/owner-repo.md`

必须包含：
- 基本信息（链接、Stars、Forks、License、语言、最近更新）
- 一句话判断
- 核心价值
- 可迁移模式（含落地路径）
- 已知限制

### 3. 经验沉淀
**文件**: `shared/runtime/openclaw/github-learning/lessons.md`

按日期追加，每条经验需具体可操作。

---

## 质量标准

### 硬性要求（不达标直接不合格）

1. **来源完整**: 仓库、README/docs/release/issue 链接齐全
2. **事实准确**: 关键事实可追溯，不臆测
3. **数据真实**: stars/forks/license 来自 GitHub API，标注查询时间
4. **深读完整**: 每个深读项目必须包含「可复用经验」和「风险边界」
5. **无截断**: 报告必须完整，不能中途截断

### 软性要求（扣分项）

1. **技术深度**: 讲清实现思路和边界
2. **可迁移性**: 能指出可复用的模式
3. **实践性**: 有可尝试的实验
4. **反宣传**: 能指出局限和不适用场景

---

## 深度学习与安全反哺要求

每日学习不只做项目摘抄，必须采用“深挖 → 机制抽象 → 反哺建议 → 安全边界”的结构。

### A. 深挖对象
- 明确今日深挖对象是项目、工具、机制还是故障案例。
- 每个深读对象至少核验 README/docs/release/issues 中的 2 类来源；关键 repo 元数据必须来自 GitHub API。

### B. 可验证证据
- 给出 GitHub 链接、核心文件/目录、版本/提交或查询时间。
- 不确定的结论必须标注“待核验”，不得编造。

### C. 核心机制
- 不只罗列功能；必须抽象出可迁移模式。
- 优先使用这种句式：`当……时，应优先……，因为……，边界是……`。

### D. 反哺到现有体系
每个深读项目至少判断一次是否可反馈到：
- shared curated memory / facts / projects
- shared skill / workflow
- Hermes 审计流程
- OpenClaw 每日学习 / 每日巡检
- runtime POC / open questions

### E. 安全边界
必须明确哪些内容不能自动执行：
- 不自动改配置、模型、provider、cron、secret。
- 不直接写 curated active fact，只提出 candidate。
- 不复制 license 不明或不兼容项目源码。
- 不从 assistant-authored prose 生成用户事实。
- 巡检类建议只输出风险、证据、影响、建议动作，不自动修复。

### F. 候选反哺
在日报末尾新增“候选反哺”小节，按以下格式输出：

```markdown
## 候选反哺

### Candidate Facts
- [ ] topic: ... | evidence: ... | 建议: create/update/retire/dispute | 安全级别: low/medium/high

### Candidate Skills / Workflow
- [ ] 名称: ... | 可复用场景: ... | 是否建议 shared: yes/no | 原因: ...

### Candidate Open Questions
- [ ] 问题: ... | reason: gap/conflict/stale/adaptation | priority: low/medium/high

### 不应自动落地
- ...
```

### G. 输出约束
- 候选反哺只作为 Hermes 二轮审计输入，不代表已落库。
- 如果触及安全/密钥/配置，必须只写变量名或占位符，不写明文值。
- 受 cron summary 截断限制，核心结论要短；完整证据应尽量写入 shared inbox/runtime 产物。

---

## 审计反馈区（Hermes 自动更新）

> 以下内容由 Hermes 审计后自动写入，请勿手动修改。

### 最近审计反馈

{{AUDIT_FEEDBACK}}

### 历史失败点

{{HISTORICAL_FAILURES}}

### 强化指令

{{ENHANCED_INSTRUCTIONS}}

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | {{DATE}} | 初始版本 |
