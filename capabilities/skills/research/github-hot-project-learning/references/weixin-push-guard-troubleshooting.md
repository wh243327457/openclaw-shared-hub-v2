# 微信推送限流保护排查

## Push Guard 文件位置

**正确**：`/root/.hermes/weixin-push-guard.json`
**错误**：`/root/.hermes/weixin/weixin-push-guard.json`（子目录，不存在）

代码位置：`gateway/platforms/weixin.py::_PUSH_GUARD_FILE = "weixin-push-guard.json"`
读取方式：`Path(get_hermes_home()) / WeixinAdapter._PUSH_GUARD_FILE`

## Push Guard 阻塞条件

`_check_push_guard()` 返回 False（阻塞）当以下任一条件满足：

1. `consecutive_push_without_user_reply >= 8`（阈值 `_PUSH_GUARD_BLOCK_THRESHOLD`）
2. `last_rate_limited_at` 在最近 15 分钟内（`_PUSH_GUARD_COOLDOWN_SECONDS`）

**绕过机制**：`_is_in_active_conversation_window()` — 用户最近发过消息时，主动推送也被视为对话的一部分，跳过 guard 检查。

## Push Guard 计数器行为

- 每次成功发送后 `consecutive_push_without_user_reply += 1`（line 1994）
- 收到 iLink `ret=-2 rate limited` 后 `last_rate_limited_at` 被设为当前时间（line 1860）
- 用户发消息时 `bump_guard_for_user_reply()` 重置 `consecutive_push_without_user_reply = 0`（line 1457）

## 排查流程

```bash
# 1. 查看当前 guard 状态
cat /root/.hermes/weixin-push-guard.json

# 2. 如果 consecutive_push >= 8，重置
# 注意：必须在 gateway 能读到的路径写入
python3 -c "
import json
guard = {
    'consecutive_push_without_user_reply': 0,
    'last_push_at': '',
    'last_context_token_mtime': 0.0,
    'last_rate_limited_at': ''
}
with open('/root/.hermes/weixin-push-guard.json', 'w') as f:
    json.dump(guard, f, indent=2)
"

# 3. 如果 last_rate_limited_at 在 15 分钟内，清空
# 同上，把 last_rate_limited_at 设为 ""

# 4. 注意：gateway 从磁盘读取，不需要重启
# 但如果 gateway 进程正在写回旧状态，可能需要协调
```

## 常见陷阱

1. **路径错误**：写到了 `weixin/` 子目录而不是根目录
2. **iLink 上游限频**：即使 guard 通过，iLink API 也可能返回 `ret=-2`，这会被记录到 `last_rate_limited_at`，触发 15 分钟冷却
3. **冷却期内连续尝试**：每次尝试都会被 guard 拦截（不是 iLink 拦截），需要等冷却期结束或手动清空 `last_rate_limited_at`
4. **消息过长**：长消息更容易触发 iLink 限频，建议拆分或精简

## 相关代码

- `_check_push_guard()`: line 1396-1444
- `_load_push_guard()`: line 1260-1274
- `_save_push_guard()`: line 1276-1283
- `bump_guard_for_user_reply()`: line 1446-1465
- 发送成功后计数器递增: line 1989-1995
- rate limited 后记录时间戳: line 1859-1860
