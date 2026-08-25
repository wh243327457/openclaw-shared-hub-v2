---
fact_id: ai-code-six-failure-modes
status: active
freshness_class: slow_changing
scope: cross-agent
subject: ai-code-quality
attribute: failure-pattern-catalog
value_summary: "AI 生成代码的 6 大系统性失败模式：catch-all 吞错误、硬编码成功返回、幻觉 API、过度抽象、注释污染、copy-from-similar"
created_at: 2026-06-09
updated_at: 2026-08-25
last_verified_at: 2026-08-25
review_due_at: 2026-11-23
source_refs:
  - https://github.com/amElnagdy/guard-skills
  - daily-report: 2026-06-09-GitHub热门项目学习日报.md
conflict: null
supersedes: null
superseded_by: null
confidence: medium
authority: hermes-autonomous-learning
secret_checked: true
---

# AI 代码 6 大系统性失败模式

## 核心内容

AI 编码 Agent 有系统性失败模式，不是随机出错，而是有规律可循：

1. **Catch-all 吞错误**：用 `except Exception` 或 `catch (e)` 捕获所有异常后静默吞掉，导致故障难以定位
2. **硬编码成功返回**：函数无论实际结果都返回成功状态，掩盖真实错误
3. **幻觉 API**：调用不存在的函数/方法/库，代码看起来合理但运行即报错
4. **过度抽象**：为只有一个用例的场景创建接口/工厂/策略模式，增加无意义的间接层
5. **注释污染**：大量冗余注释重复代码已表达的内容，降低信噪比
6. **Copy-from-similar**：从相似代码复制粘贴而不理解差异，引入微妙 bug

## 审查应用

在代码审查流程中，应将这 6 条作为专项检查项：
- 对 AI 生成的代码优先扫描这 6 种模式
- 比通用 clean code 规则更有针对性
- 可整合到 Hermes 的 requesting-code-review skill

## 边界

- 来源于 guard-skills 项目的研究，confidence: medium
- 需要随模型能力变化更新（新模型可能减少某些模式）
- 仅覆盖代码生成场景，不覆盖测试/文档/配置生成

## 来源

- guard-skills (⭐467, MIT) — 编码 Agent 质量门禁
- 2026-06-09 GitHub 热门项目学习日报深读
