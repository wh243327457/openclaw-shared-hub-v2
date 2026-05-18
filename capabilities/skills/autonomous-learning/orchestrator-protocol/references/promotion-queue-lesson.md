# 自主学习候选晋升与去重规则（2026-05-18）

本页记录本次 autonomous-learning 编排中的几个可复用收口点，供后续 run 直接参考。

## 晋升分流模式

- 18/20 以上不等于自动晋升；仍需用户确认。
- 用户明确说“可以 / 按建议来 / 我觉得可以晋升”时，可视为对当前建议的确认。
- 候选应分成三类：
  1. **长期 fact**：方法论、机制、稳定工程规则。
  2. **项目 note**：系统架构、项目状态、可持续推进的观察卡。
  3. **runtime / observation card**：项目太新、重复出现、或适合先观察 2–4 周的内容。

## 去重规则

- 同一 repo / 同一主题在相近时间窗口出现多个候选时，优先合并成一个观察卡，而不是重复晋升。
- `zero` 这种“深读 + 热点跟踪”的重复候选，应合并成同一观察卡，避免在 curated 里制造重复知识点。
- 对于“一个是项目深读、一个是增长跟踪”的组合，先判断是否在讲同一机制；若是，先合并，再决定是否晋升。

## 元数据规则

- 长期事实文件建议使用标准 frontmatter：`fact_id`、`status`、`freshness_class`、`scope`、`subject`、`attribute`、`value_summary`、`created_at`、`updated_at`、`last_verified_at`、`review_due_at`、`source_refs`、`confidence`、`authority`、`secret_checked`。
- 对稳定但非实时的长期事实，`freshness_class` 应优先使用 `static`；运行态或频繁变化项才用 `operational`。
- 事实晋升后要同步更新 `curated/memory/MEMORY.md` 的索引，否则后续检索会断链。

## 验证规则

- 晋升后必须做 read-back 或 verify_bridge 级别的验证。
- 允许保留 legacy metadata warning，但应当把 warning 视为后续待清理项，而不是晋升失败。
