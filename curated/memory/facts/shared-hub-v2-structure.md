# 共享中台 v2 结构事实

## 核心分层
- curated/memory/ = 跨 agent 真相源
- inbox/<agent>/daily/ = agent 原始写入
- runtime/<agent>/ = 运行时产物
- capabilities/skills/ = 共享 skills
- compat/daily/ = 旧 OpenClaw daily 兼容

## 兼容链路
- shared/skills -> capabilities/skills
- shared/memory/MEMORY.md -> curated/memory/MEMORY.md
- shared/memory/daily -> compat/daily
- compat/daily/.dreams -> runtime/openclaw/dreams

## 治理规则
- 禁止明文 secret 写入 shared
- 新 skill 需判断是否升格为跨 agent 共享
