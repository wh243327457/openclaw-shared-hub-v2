# Hermes Gateway 事实

## 已修复的问题
1. **systemd ExecStart 路径错误**
   - 根因: `_remap_path_for_user()` 对 venv/bin/python 做 Path.resolve() 展开为底层 uv Python
   - 结果: 丢失 venv site-packages，缺少 yaml/aiohttp/cryptography/websockets 等模块
   - 修复: 保留原始 venv 路径

2. **websockets 依赖缺失**
   - 已安装到 /root/.hermes/hermes-agent/venv/
   - 服务状态: active (running) since 2026-04-16
