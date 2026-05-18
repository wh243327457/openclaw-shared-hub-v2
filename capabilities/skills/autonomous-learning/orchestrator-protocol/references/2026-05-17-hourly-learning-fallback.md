# 2026-05-17 Hourly Autonomous Learning Fallback Lesson

## Context

A scheduled hourly autonomous-learning run required:
- one GitHub growth / engineering hotspot item;
- at least one non-GitHub learning item;
- double Hermes review;
- runtime output + inbox summary;
- final WeChat-friendly report using sections, tables, file list, and a separate decision block.

The loaded `orchestrator-protocol` skill was relevant, but one configured report-style skill was missing: `foundation/console-style-progress-report`.

## What happened

- GitHub delegate_task for Trending/deep-read timed out after 600s with 10 API calls completed.
- Hermes saved failure evidence and produced a fallback output for `colbymchenry/codegraph` using GitHub Trending HTML, GitHub REST API, and raw GitHub files.
- The fallback output was explicitly labeled `completed_with_fallback_executor` and bounded as README/API/design-doc level, not source-level full audit.
- The non-GitHub item completed through delegate_task and focused on local code knowledge graphs, token-efficient coding context, and agent memory.
- Hermes wrote Spec Review and Quality Review files for both items.
- Final report started with the missing-skill warning and included a standalone “需要你决策” table for POC/promotion decisions.

## Durable workflow lesson

For high-frequency autonomous-learning cron jobs:

1. Do not treat delegate_task timeout as a reason to produce an empty or vague report.
2. Save failure evidence under `runtime/hermes/autonomous-learning/failure-evidence/`.
3. Generate a clearly labeled fallback only if enough evidence can be fetched independently.
4. Use conservative phrasing:
   - “降级产出”
   - “未源码级深读”
   - “README/API 级深读”
   - “不自动晋升 curated”
5. Still perform Spec Review and Quality Review on the fallback, but score the boundary honestly.
6. If quality is 15–17/20, keep it in runtime learning and ask the user whether to run a POC or allow promotion after more evidence.
7. If an invoked/configured skill was missing, start the user-facing report with a brief warning before the main content.

## Useful output shape

```text
⚠️ Skill(s) not found and skipped: <skill-name>

📚 自主学习系统 — 本轮学习报告

时间 / 模型

📋 计划
🤖 执行 table
🔍 审计 table
📊 结果
💡 收获
🎯 下一步
需要你决策 table
产出文件清单
```

## Anti-patterns

- Do not hide fallback status only in runtime files.
- Do not let the executor claim review passed.
- Do not promote curated automatically just because the topic is high-value.
- Do not send a separate message manually from cron; final response is delivered by the scheduler.
