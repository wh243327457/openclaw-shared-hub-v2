# OpenClaw 配置事实

## 已确认的配置
- Base URL: https://aixj.vip/v1
- API Key: 环境变量 `$OPENCLAW_API_KEY`
- 默认模型: gpt-5.4 + xhigh thinking
- 配置文件: /home/vany/openclaw-data/.openclaw/openclaw.json
- 后台地址: http://localhost:18789

## 稳定约束
- 不将明文 API Key 写入 shared
- 查询配置时需先确认是 Hermes 配置还是 OpenClaw 配置
