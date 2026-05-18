# 微信主动推送限流保护

## 背景

用户反馈：如果长时间不跟 Hermes 微信 bot 对话，主动推送可能被 iLink 限流，导致后续日报或告警无法正常送达。

## 已确认源码事实

Hermes Weixin 适配器通过 iLink `sendmessage` 发送消息。源码中可确认：

- 限流返回：`ret=-2` 或 `errcode=-2`
- 典型错误：`iLink sendmessage rate limited: ret=-2 errcode=None errmsg=rate limited`
- 单条文本默认约 2000 字上限，超长会拆成多个 chunk
- 拆成多个 chunk 会增加发送频率，更容易触发频控
- 默认每个 chunk 失败重试 4 次
- 限流时按约 3 倍 retry delay 退避，但不能保证解除限流
- iLink 未暴露明确的“连续 N 条未回复即限流”官方阈值

相关源码位置：

- `/root/.hermes/hermes-agent/gateway/platforms/weixin.py`
- `RATE_LIMIT_ERRCODE = -2`
- `MAX_MESSAGE_LENGTH = 2000`
- `_send_text_chunk()` 对 `ret=-2` / `errcode=-2` 做 backoff retry

## 保守执行规则

由于没有官方固定阈值，主动推送采用保守策略：

1. 维护连续主动推送计数，检测到用户微信回复后清零。
2. 连续主动推送达到 3 次且用户未回复时，下一条推送末尾追加提示：
   `如果你看到这条，回复任意内容即可刷新微信会话，避免后续 iLink 主动推送被限流。`
3. 连续主动推送达到 4 次仍无回复时，非关键推送只落盘到 runtime，不继续硬推微信。
4. 关键异常/失败告警可继续推送，但必须尽量短，避免拆 chunk。
5. 主动推送优先控制在 2000 字以内；日报 v3 过长时优先压缩项目背景，而不是拆多条。
6. 出现 `ret=-2` / `rate limited` 后停止补发同一内容，写入 `runtime/hermes/.../wechat-push-YYYY-MM-DD.txt`，等待用户回复或下一轮再试。

## 状态文件建议

```text
shared/runtime/hermes/github-hot-project-learning/weixin-push-guard.json
```

建议字段：

```json
{
  "consecutive_push_without_user_reply": 0,
  "last_push_at": "YYYY-MM-DDTHH:mm:ss+08:00",
  "last_context_token_mtime": 0,
  "last_rate_limited_at": null
}
```

## 用户回复检测

近似方法：观察 Weixin context-token 文件 mtime 是否在上次推送后变化。

```text
/root/.hermes/weixin/accounts/*.context-tokens.json
```

该方法不是官方 ACK，但足够判断“用户是否近期和 bot 对话过”。

## 用在 GitHub 学习日报时

- 发送前读取 guard 状态。
- 若连续未回复计数 >= 3：追加回复提示。
- 若连续未回复计数 >= 4：日报只写 runtime 文件，不推送；如果是失败告警则短消息推送。
- 推送成功后增加计数。
- 检测到用户回复后清零。
