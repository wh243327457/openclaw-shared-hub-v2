# 每日复盘 2026-08-28

> 数据来源：Claude Code 0 条 | Codex 263 条 | Chrome 664 次（公开 197 / 内网 467）
> 复盘生成方式：Claude Code CLI 配置的模型不可用，由 Hermes 基于本地 raw 数据降级生成

---

## 1. 今日概览

今日工作集中在两条主线：一是把 `yishouapp`、`yishouos`、`service-order`、`yishou-go` 四个项目在本地拉起并打通；二是继续排查和完善商品图片向量链路，覆盖命令调度、GD 批处理、PG 写入、队列常驻消费和重试耗尽诊断。

## 2. 主要工作

### 2.1 四项目本地联调闭环

- 在独立目录 `D:\www\yishou-local-stack` 建立 Docker Compose 联调栈，四个原项目以只读方式接入，未改动项目源码。
- 逐步解决了路径误写、Docker/WSL 挂载、Go 模块下载代理、PB 生成文件滞后、OpenAPI 目录缺失、HTTP/gRPC 端口错配、PHP 运行目录不可写、启动脚本重启不幂等等问题。
- 最终确认两个 Go 服务 `/ping` 均返回 `pong`，`service-order -> yishou-go:8091` 与 `yishou-go -> service-order:8090` 双向 TCP 连通。
- 新增本地 Nginx 网关，将入口统一为 `*.yishou.com`：
  - `http://api.yishou.com`
  - `http://os.yishou.com`
  - `http://service-order.yishou.com/ping`
  - `http://yishou-go.yishou.com/ping`
- 当前仍依赖开发环境 MySQL、Redis、Apollo；其中 Redis/Apollo 曾出现瞬时超时，Compose 已配置 `unless-stopped` 自动恢复。

### 2.2 商品图片向量任务与数据链路

- 核验三个新命令为独立 Think 命令，正确调用方式是 `think API-GoodsImageVectorUpdate`、`think API-GoodsImageVectorRetry`、`think API-GoodsImageVectorCompensate`，不需要旧式 `-f` 参数。
- 定位到主队列无数据的关键原因：线上 `autoRunUploadDataByApiNew()` 路径没有调用向量队列入队逻辑；仅打开配置开关不会生效，后续需补齐生产者调用，历史缺口再走补偿任务。
- 将实时更新、失败重试两个消费者调整为：空队列时每秒休眠并继续轮询，只在运行满 `3480` 秒（58 分钟）后退出；已通过 PHP 7.0.28 语法检查和 ThinkPHP 命令注册检查。
- 定位 GD 微批回退原因：不同宽高比图片预处理后形成 `800×1147` 与 `800×1097` 张量，批量堆叠前未 padding。当前会降级逐图推理，不直接导致整批失败，但会降低吞吐；临时可设批量大小为 1，根治应做 padding 或同尺寸分桶。
- 明确吞吐观测日志：`goods_image_vector_micro_batch`、`goods_image_batch_sync_item`、`goods_image_vector_micro_batch_fallback`，并按 `batch_id` 聚合。
- 核验 `status=stored` 表示 PG UPSERT 与写后回查均成功；样例总耗时 `8438ms`，其中 Qwen 占 `7631ms`，是主要瓶颈。
- `HTTP_REQUEST_FAILED` / `retry_exhausted` 表示 PHP 到 GD 的 HTTP 传输连续 3 次未获得响应，常见原因是 60 秒超时、连接重置或网络/DNS 问题；需结合 `goods_image_vector batch curl fail error=` 中的 `curl_error` 精确判断。

## 3. 值得沉淀

1. 多项目本地联调应把编排与运行时配置放在独立目录，源码只读挂载，避免污染脏工作区。
2. 健康验证不能只看容器 `Up`：应同时验证 HTTP 响应、容器内 DNS、双向 TCP，以及重启后的幂等性。
3. 本地模式与远端动态配置要严格区分；错误环境变量可能触发 Apollo 覆盖本地服务地址。
4. GPU 批处理必须统一张量尺寸；没有 padding 的“真实 batch”可能比逐图循环更脆弱。
5. 日志状态应形成明确语义：`stored` 代表落库成功，`processed` 仅代表 dry-run，`retry_exhausted` 代表自动重试已耗尽。

## 4. 明日线索

- 把向量主队列入队调用补到 `autoRunUploadDataByApiNew()`，并验证新商品与历史补偿两条路径。
- 为 GD 批处理实现 padding 或尺寸分桶，复测 fallback 率、吞吐和显存占用。
- 在 HTTP 请求失败日志/告警中保留 cURL 错误码与错误文本，缩短超时类问题定位时间。
- 继续观察本地联调栈对开发 Redis/Apollo 的依赖稳定性；必要时增加显式健康检查与启动等待。
- 收口实时/重试消费者改动，补最小行为测试后按功能提交。

---

## 5. 今日访问概览（Chrome）

| 次数 | 域名 | 用途 |
|---:|---|---|
| 382 | `127.0.0.1:5173` | 本地 Vite 前端调试 |
| 80 | `139.159.254.167:5920` | gocron 定时任务系统 |
| 53 | `gitlab.yishou.pro` | MR、Pipeline 与代码协作 |
| 30 | `get-token.vip` | 账号管理相关操作 |
| 18 | `sub.aikangs.com` | API 密钥/服务管理 |
| 17 | `prd-upload-pub.yishouapp.com` | 业务图片资源 |
| 14 | `yearning.yishou.com` | 数据库查询/审核 |
| 10 | `console.huaweicloud.com` | 云日志与监控 |

公开访问 197 次，内网访问 467 次；活动主要集中在本地前端、定时任务平台、GitLab、数据库管理和云日志排查。

---

*数据来源：Claude Code 0 条 | Codex 263 条 | Chrome 664 次*
