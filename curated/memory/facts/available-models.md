# 当前环境可用模型事实

## 已配置模型
1. **gpt-5.4** (Aixj.vip / custom)
   - 当前主力模型
   - 思考模式: xhigh thinking
   - Base URL: https://aixj.vip/v1

2. **kimi-for-coding** (Kimi For Coding)
   - 代码/长上下文场景
   - 通过 Kimi 提供商切换

3. **MiniMax-M2.7** (MiniMax / minimaxi.com)
   - 新增模型
   - Base URL: https://api.minimax.chat/v1
   - contextWindow: 256k, maxTokens: 8k
   - 适用于中文场景和中长文本处理

## 模型切换策略
- 代码/编程任务: 优先 kimi-for-coding
- 一般任务/调研: 优先 gpt-5.4
- 中文内容/长上下文: 可尝试 MiniMax-M2.7
- 接口限制时: 自动切换到可用模型

## 稳定约束
- 不在 shared 中存储明文 key
- 配置文件使用环境变量占位符
