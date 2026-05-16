# Self-Improvement Workflow Session

**Date**: 2026-05-16
**Context**: 用户要求用自治学习系统自我完善，把该处理的处理、优化的优化、升级的升级、更新

---

## 用户原话

> "可以，你现在就用这套自主学习系统，自我完善，把该处理的处理，优化的优化，升级的升级，更新的更新"

---

## 执行过程

### Phase 1: 审计
读取了以下文件：
- `runtime/hermes/autonomous-learning/state.json`
- `runtime/hermes/autonomous-learning/learning-backlog.json`
- `runtime/hermes/verify-final.json`
- `runtime/hermes/promotion-governance-final.json`

发现了关键问题：
- `verify_bridge.py` 输出 6 条 `LEGACY_FACT_METADATA_MISSING` warnings
- `docs/fact-frontmatter-template.md` 存在但未被使用
- 6 个 fact 文件只有正文，没有 YAML frontmatter

### Phase 2: P0 修复
对 6 个 fact 文件补齐了标准化 frontmatter：
- `fact_id`, `status`, `freshness_class`, `scope`, `subject`, `attribute`
- `value_summary`, `created_at`, `updated_at`, `last_verified_at`, `review_due_at`
- `conflict`, `supersedes`, `superseded_by`, `confidence`, `authority`, `secret_checked`

修复后 `verify_bridge.py` 输出：`fact_warnings: 0`

### Phase 3: 验证链路
```
test_fact_governance.py  → 3/3 tests OK
verify_bridge.py         → ok=true, errors=0, warnings=0
promoter.py --dry-run     → ok=true
promoter.py (apply)       → ok=true, MEMORY.md updated
promoter.py scan          → blocked=1, candidate=10, review=56
```

### Phase 4: 启用两个半自动治理规则
用户批准启用：
1. `fact-time-decay`（事实新鲜度/过期复查）
2. `promotion-conflict-resolution`（多 agent 冲突识别）

模式：`warning-only`，curated autopromotion 保持禁用。

更新了 `state.json` 和 `learning-backlog.json` 中的治理状态。

### Phase 5: 落盘
- 写 `inbox/hermes/daily/2026-05-16.md`
- 更新 `state.json` 的 `self_improvement_sessions` 记录

---

## 关键教训

### P0 问题优先于 P1 优化
在自治系统里，metadata 结构问题是 P0，因为它会导致所有 downstream 工具（verify/promoter/governance scan）产生假阳性 warnings，降低系统可信度。

### fact frontmatter 是可发现的结构性缺陷
虽然 `docs/fact-frontmatter-template.md` 已经存在，但 6 个 fact 文件都没用。这种"文档存在但没应用"的情况很常见，需要定期审计脚本与文档的一致性。

### warning-only 模式的验证标准
warning-only 模式不等于"不做任何事"。验证标准是：
1. 工具能正常跑通（exit 0）
2. 不产生新的 errors 或 warnings
3. 不自动写 curated
4. promotion candidate 能正确输出 governance 字段

### 沟通要先总后分
用户说"这些都是什么？没看懂有什么用"时，说明技术术语没有对上用户的认知模型。正确方式是：
1. 先一句话说清楚"这堆东西是什么"
2. 再按需展开细节
