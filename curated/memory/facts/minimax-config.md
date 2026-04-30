# MiniMax 配置事实

## 已确认的配置
- Provider: minimax
- Base URL: https://api.minimax.chat/v1
- API Key: 环境变量 `$MINIMAX_API_KEY`
- 配置文件: /home/vany/openclaw-data/.openclaw/openclaw.json
- .env 文件: /home/vany/openclaw-data/.openclaw/.env

## 可用模型
- MiniMax-M2.7: contextWindow 256k, maxTokens 8k
- MiniMax-Text-01: contextWindow 256k, maxTokens 8k

## 稳定约束
- 不将明文 API Key 写入 shared 或 git
- 使用 `${MINIMAX_API_KEY}` 占位符在配置文件中引用
