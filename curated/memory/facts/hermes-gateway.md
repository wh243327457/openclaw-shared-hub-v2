---
fact_id: hermes-gateway-health
status: active
freshness_class: operational
scope: hermes
subject: hermes.gateway
attribute: service_health
value_summary: "systemd gateway active，venv 路径保留修复已生效，websockets 已安装"
created_at: 2026-05-16T02:58:05+08:00
updated_at: 2026-05-16T02:58:05+08:00
last_verified_at: 2026-05-16T02:58:05+08:00
review_due_at: 2026-06-16T02:58:05+08:00
source_refs:
  - /root/.hermes/hermes-agent/venv/
  - systemctl status hermes-gateway.service
conflict:
  status: none
  type: null
  conflicting_fact_ids: []
  conflicting_candidate_refs: []
  resolution: null
  resolved_by: null
  resolved_at: null
supersedes: []
superseded_by: null
confidence: high
authority: filesystem
secret_checked: true
---

# Hermes Gateway 事实

## 已修复的问题
1. **systemd ExecStart 路径错误**
   - 根因: `_remap_path_for_user()` 对 venv/bin/python 做 Path.resolve() 展开为底层 uv Python
   - 结果: 丢失 venv site-packages，缺少 yaml/aiohttp/cryptography/websockets 等模块
   - 修复: 保留原始 venv 路径

2. **websockets 依赖缺失**
   - 已安装到 /root/.hermes/hermes-agent/venv/
   - 服务状态: active (running) since 2026-04-16
