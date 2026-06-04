---
name: self-reflection-engine
description: >
  通用自我反思引擎 — 适用于任何"执行→反馈→反思→进化"闭环。
  支持多领域（GitHub 学习、读书计划、日常巡检、代码审查等），
  每个领域有专属反思模板，跨领域共享进化趋势。
  核心理念：反思不是打分，是识别模式、找到杠杆点、生成可执行的改进动作。
triggers:
  - 执行完成后的 cron job
  - 用户说"反思"/"复盘"/"总结经验"/"哪里可以改进"
  - 连续 N 次同类任务后自动触发深度反思
  - 分数下降或出现新模式时
---

# 自我反思引擎 Skill

## 核心理念

反思不是打分，是**识别模式**：
- 什么反复出错？→ 系统性问题，改流程
- 什么投入产出比高？→ 加大投入
- 什么在浪费时间？→ 砍掉或自动化
- 什么新能力可以解锁？→ 下一步挑战

## 文件与代码

- **引擎代码**: `shared/scripts/reflection_engine.py`
- **运行时数据**: `shared/runtime/hermes/<domain>/feedback-history.json` + `evolution-suggestions.json`
- **CLI**: `python3 scripts/reflection_engine.py {reflect|summary|dashboard}`

## 使用流程

### 1. 执行后记录反思

每个领域的 cron job 完成后，调用反思：

```bash
# GitHub 学习
python3 scripts/reflection_engine.py reflect \
  --domain github-learning \
  --score 23 --max-score 23 \
  --issues "源码精读不够深" "缺少跨项目对比" \
  --strengths "落地路径清晰" "竞品分析到位"

# 读书计划
python3 scripts/reflection_engine.py reflect \
  --domain reading-plan \
  --score 85 --max-score 100 \
  --issues "案例分析浅" "缺少行动清单" \
  --strengths "核心概念提炼准确"

# 日常巡检
python3 scripts/reflection_engine.py reflect \
  --domain daily-patrol \
  --score 90 --max-score 100 \
  --issues "磁盘告警延迟处理" \
  --strengths "服务健康检查正常"

# 代码审查
python3 scripts/reflection_engine.py reflect \
  --domain code-review \
  --score 70 --max-score 100 \
  --issues "遗漏边界条件" "性能未评估" \
  --strengths "安全检查全面"
```

### 2. 查看跨领域汇总

```bash
python3 scripts/reflection_engine.py dashboard
```

输出示例：
```
## 🔄 自我进化汇总
**⚡ 2 项高优先级建议需要处理**

### ✅ github-learning
  - 状态良好，无需调整

### ⚠️ reading-plan
  - 🔴 本次问题需强化：案例分析不够深入
  - 🔴 本次问题需强化：缺少行动清单

### ⚠️ daily-patrol
  - 🔴 磁盘告警延迟处理出现 3 次，是系统性问题
```

### 3. 在 cron prompt 中嵌入进化建议

```python
from reflection_engine import ReflectionEngine

# 读取该领域的进化建议
suggestions = ReflectionEngine.read_suggestions(shared_root, 'github-learning')

# 生成明日指令增强文本
engine = ReflectionEngine('github-learning', shared_root)
enhancement = engine.get_instruction_enhancement()
# 拼接到 cron prompt 中
```

### 4. 深度反思（每周/每月）

当积累了 7+ 天数据后，执行深度反思：

```bash
# 查看趋势
python3 scripts/reflection_engine.py summary
```

深度反思要回答：
1. **趋势**: 分数是上升、稳定还是下降？
2. **反复问题**: 哪些 issue 出现 ≥3 次？这是系统性问题
3. **高杠杆**: 哪些改进带来最大提升？
4. **瓶颈**: 当前最大瓶颈是什么？
5. **下一步**: 什么新挑战可以解锁？

## 领域反思模板

### GitHub 学习反思

反思维度：
- **广度**: 今日项目覆盖了哪些技术领域？是否有盲区？
- **深度**: 源码分析到了哪一层？是否有"只读 README 没看代码"的情况？
- **关联**: 项目之间有什么关联？能否形成技术趋势判断？
- **落地**: 哪些经验可以立即用到我们的系统？
- **效率**: 哪些项目浪费时间？选题逻辑需要调整吗？

### 读书计划反思

反思维度：
- **理解**: 核心概念用自己的话能说清吗？
- **联系**: 和已有知识体系有什么关联？
- **应用**: 书中方法论能在什么场景用？
- **质疑**: 哪些观点不认同？为什么？
- **行动**: 读完这章，明天可以做什么不同的事？

### 日常巡检反思

反思维度：
- **覆盖**: 巡检项是否遗漏了什么？
- **响应**: 从发现问题到处理的延迟是多少？
- **根因**: 是治标还是治本？
- **预防**: 能否从被动响应变为主动预防？
- **自动化**: 哪些巡检项可以自动化处理？

### 代码审查反思

反思维度：
- **安全**: 是否遗漏安全风险？
- **性能**: 是否评估了性能影响？
- **可维护**: 代码是否容易理解和修改？
- **测试**: 测试覆盖是否充分？
- **架构**: 是否符合整体架构原则？

## 进化阶段

反思引擎会自动识别系统所处阶段：

| 阶段 | 特征 | 策略 |
|------|------|------|
| 🔴 **修复期** | 频繁出错，分数波动大 | 聚焦修复高频问题，简化流程 |
| 🟡 **稳定期** | 分数稳定但无突破 | 尝试新挑战，提高标准 |
| 🟢 **成长期** | 分数持续上升 | 加大难度，扩展边界 |
| 🔵 **精进期** | 接近满分，边际收益递减 | 跨领域迁移经验，创新方法 |

## 与其他 Skill 的关系

- **orchestrator-protocol**: 反思引擎是编排协议的反馈环节
- **github-research-pipeline**: GitHub 学习的具体反思模板
- **reading-plan**: 读书计划的具体反思模板
- **delegation-and-automation**: 反思结果可以触发自动化改进

## 注意事项

1. **不要为了打分而反思** — 分数只是信号，重点是识别模式
2. **反思要具体** — "源码读得不够" → "对 pipeline.py 的 11 阶段只读了 3 个"
3. **建议要可执行** — "提高深度" → "明天每个项目必须读 3 个核心文件的源码"
4. **跨领域复用** — GitHub 学习中发现的"选题偏差"模式，可能也适用于读书选书
5. **定期清理** — feedback-history 只保留最近 14 天，避免历史包袱

## Guardian 模式（自动发现 + 补位）

**核心问题**：新增 cron job 忘记加反思，或换模型后不知道有反思系统。

**解决方案**：`guardian` 模式每天自动扫描所有 cron job，发现缺反思的自动补位。

```bash
# 手动扫描
python3 scripts/reflection_engine.py guardian

# 自动扫描（每天 06:00，cron job a7ccf53ed528）
# 无需手动操作，guardian 会：
# 1. 读取所有 cron jobs
# 2. 按关键词判断哪些需要反思
# 3. 自动创建 feedback-history.json + evolution-suggestions.json
# 4. 输出报告，告诉你哪些 job 需要在 prompt 中加反思步骤
```

**匹配规则**：
- 反思关键词：学习/读书/复盘/采集/分析/闭环/编排/巡检/审查 等
- 排除关键词（只看 job name）：日志/同步/推送/提交/健康检查/总结 等
- 新增 job 只要 name 或 prompt 包含反思关键词，guardian 会自动发现

**换模型也不怕**：guardian 的扫描逻辑在脚本里，不依赖模型记忆。新模型只要跑 `python3 scripts/reflection_engine.py guardian` 就能看到完整覆盖情况。
