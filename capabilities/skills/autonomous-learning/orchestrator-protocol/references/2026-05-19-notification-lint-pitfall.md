# 2026-05-19 — Notification linter section-header pitfall

## 触发

pending promotion 复核轮中，手写通知文件使用了 `**🔍 审计结果（待确认晋升项）**` 作为 section header。

## 错误

```
{
  "ok": false,
  "errors": ["missing_section:**🔍 审计结果**"]
}
```

## 根因

`generate_readable_notification.py` 的 linter 对 section header 做**精确字符串匹配**，不支持模糊匹配或前缀匹配。模板定义的必须 section 是：

- `**📋 今天/本轮学了什么**`
- `**🤖 执行情况**`
- `**🔍 审计结果**`
- `**📊 结果沉淀**`
- `**💡 对你有用的收获**`
- `**🎯 下一步**`
- `**需要你决策**`
- `**产出文件**`

任何附加文字（括号注释、子标题、emoji 前缀后缀）都会导致匹配失败。

## 修复

把 header 改回模板原文，去掉所有附加文字。

## 正确做法

```markdown
**🔍 审计结果**       ← ✅ 通过
| 候选 | 分数 | ... | 晋升 |
```

```markdown
**🔍 审计结果（待确认晋升项）**   ← ❌ linter 报 missing
```

## 额外发现：review-consolidation run 通知

当 run 类型是 review consolidation（无新学习主题、仅复核 pending queue）时，`generate_readable_notification.py` 自动产出是通用模板，所有字段为 UNKNOWN 或空泛结论，不会包含 pending 决策表。

**必须**：手写通知文件，把待确认候选的决策表填入。linter 只检查格式，不检查内容准确性。
