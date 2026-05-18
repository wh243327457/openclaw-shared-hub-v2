# 2026-05-18 候选晋升分流与部分晋升经验

## 场景

自主学习系统从 runtime learning / quality reviews 中扫描出一批高分候选。用户先批准其中一部分进入 curated，随后要求继续处理剩余候选。

## 可复用做法

1. **先区分“晋升”和“分流”**
   - 用户批准的候选：写入 `curated/memory/facts/` 或 `curated/memory/projects/`，同步更新 `curated/memory/MEMORY.md`、项目页、pending queue、state、inbox。
   - 未批准但高分候选：不要默认进 curated，应重新分类为 `awaiting_user_approval`、`runtime_learning_only`、`observation_card`、`archive` 等。

2. **相似候选要合并，不要重复沉淀**
   - 同一主题来自不同日期/管道时，优先合并成观察卡或单一 fact。
   - 示例：`zero` 两条候选分别来自 deep analysis 与 5/18 热点跟踪，但核心结论相同且项目过新，应合并为一个 observation card，而不是建两条长期事实。

3. **pending queue 是用户决策界面，不是全部执行日志**
   - 对用户只暴露需要拍板的候选。
   - 已明确 runtime-only 的候选从“需要你决策”中移除，避免制造决策噪音。

4. **高分不等于立即 curated**
   - 20/20 的内容如果与当前主线较远，仍可保留为 curated candidate 等待确认。
   - 18/20 的工程热点如果证据未到“稳定长期事实”，可留 runtime learning only。

5. **状态更新要成组完成**
   - JSON 队列与 Markdown 视图要一致。
   - `state.json` 只记录运行态摘要，不把原始长内容塞进去。
   - `inbox/hermes/daily/YYYY-MM-DD.md` 记录本轮人类决策和分流结果，作为审计线索。

## 推荐分类字段

```json
{
  "status": "awaiting_user_approval | runtime_learning_only | accepted_promoted_curated | blocked_sensitive_review_needed",
  "classification": "curated_candidate | observation_card | runtime_only | archive",
  "recommendation": "一句人话说明",
  "target_hint": "目标路径或 runtime 观察卡路径",
  "next_action": "ask_user_to_accept_defer_or_reject | merge_with_<card> | keep_runtime_only_or_archive | none_promoted"
}
```

## 用户汇报格式

- 先给当前总数：已晋升 / 待确认 / runtime-only / blocked。
- 再列“需要你拍板”的少数项。
- 不要把 15+ 个 runtime-only 全贴给用户；只说明已分流。

## Pitfall

不要把“用户同意按建议来”扩大解释为“所有高分候选都自动晋升”。只执行用户明确同意的那一组建议；剩余候选需要重新分流或继续等待确认。
