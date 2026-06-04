# Pending Promotion Queue 评估标准（2026-06-04 用户校正）

## 核心原则

**不要按分数排序，要按"对系统的实际价值"排序。**

用户原话："不是看评分，应该是看整个的价值，对应项目对我们现在的系统的价值是什么？有它没它会有什么影响，它能带来的作用是什么？"

## 评估维度（按优先级）

### 高价值（直接影响 Hermes 架构）
- 竞品架构分析（如 OpenSquilla vs Hermes）
- 安全范式（如 permissions-before-autonomy）
- 量化数据（如 token 用量 vs 质量方差）

### 中高价值（指导系统决策）
- 可复用架构模式（如 Disk KV Cache、ContentRouter）
- 经过验证的工程实践（如 Anthropic multi-agent delegation）

### 中等价值（技术参考）
- 有趣的技术判断但当前无应用场景
- 新项目分析，走向不明

### 低价值（归档）
- 已半衰的项目分析（>14 天）
- 同项目重复候选（只保留最高分）

## 汇报格式

向用户展示时：
| 候选 | 对系统的价值 | 有/没它的影响 |

而不是：
| 候选 | 分数 | 推荐 |

## 批量处理规则
- 高价值：批准进 `curated/memory/facts/`
- 中低价值：归档为 runtime learning
- 重复候选：合并，只保留最高分
- 更新 MEMORY.md 索引
- queue 的 `awaiting_user_approval` 清零
