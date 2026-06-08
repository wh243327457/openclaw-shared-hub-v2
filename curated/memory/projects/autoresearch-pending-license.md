# autoresearch: Agent 自主训练实验框架

**学习日期**: 2026-06-08
**来源**: karpathy/autoresearch (85k stars)
**状态**: pending - License 需验证

## 核心价值
- 单文件可改 (train.py) + 5 分钟超时 + crash 合法
- Agent-as-researcher 实验范式的最小模板

## 待验证问题
- README 声明 MIT，但 API 返回 License: NONE
- 需要检查仓库根目录的 LICENSE 文件

## 可迁移模式（待确认 License 后）
1. **单文件边界**: 限制 Agent 只能修改一个文件，降低复杂度
2. **时间预算**: 5 分钟超时机制，防止无限循环
3. **合法 crash**: 允许实验失败，降低 Agent 心理压力
