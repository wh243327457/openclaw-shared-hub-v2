# 每日复盘 2026-10-22

> 数据来源：Claude Code 0 条｜Codex 188 条｜Chrome 52 次（公开 17／内部 35）
> 日期核验：全部记录均属于 2026-10-22（JST），无跨日混入
> 生成方式：Claude CLI 配置的 `MiniMax-M3.1-Flash-Preview` 不可用，由 Hermes 基于本地 raw 数据降级生成

---

## 1. 今日概览

今天主要推进三条线：

1. **多模态图搜与存量刷新**：完成 yishouapp 与 ai-inference-service 的请求契约对齐，补齐套装、resize 两类刷数脚本的限量控制和请求日志。
2. **HTTP 后台触发与数据访问修正**：实现两个独立 HTTP 入口，定位并修正后台 CLI 误读主库的问题，同时收敛套装和 resize 的候选 SQL。
3. **Ruflo 与知识库架构研究**：明确 Ruflo 的能力边界，形成“共享交付骨架 + 项目开发约定 + 任务流程 + 工具适配”的扩展方案，支持未来接入 yishou衣者等新项目。

## 2. 主要工作

### 2.1 多模态图搜与存量刷新

**已完成并验证：**

- 对齐 `yishouapp/feat-1019-多模态图搜套装处理优化`、`yishouapp/feat-10191-跑存量套装数据` 与 `ai-inference-service/feat-20261019-完善商品向量入库逻辑`。
- 发现并修正字段不一致：yishouapp 原发送 `suit_yolo_categories`，下游实际接收 `yolo_cat`；两个 yishouapp 分支均已按下游契约调整。
- 明确 `resource_type` 边界：同步接口可接收，异步通知接口未定义该字段，会将其忽略。
- `feat-10191` 已覆盖两类存量处理：套装图片刷新，以及 PG 向量表中 `is_delete='0'` 且 `crop_url` 含 `resize` 的图片刷新。
- 两个脚本增加 `--limit`：按实际提交图片数计数，失败请求也计入上限；不传或传 `0` 表示全量。
- 共用通知客户端在发送前记录完整请求 body，包括 `batch_id`、图片 URL、商品/资源 ID、类目和 `yolo_cat`。
- PHP 7.0.28 语法检查及相关定向测试通过：
  - `feat-10191`：`GoodsSuitImageRefreshTest`、`GoodsCompressedImageRefreshTest`、`GoodsImageSearchDisplayTest`
  - `feat-1019`：`GoodsImageSearchDisplayTest`、`ImageSearchGdCategoryTest`

**未验证与风险：**

- 尚未完成真实 stable HTTP、GPU 推理和 PG 最终落库回查。
- 单测使用模拟依赖，只能证明参数构造和控制逻辑正确，不能证明真实向量已更新。
- “接口已受理”或“请求日志已记录”均不能作为落库成功的证据。

### 2.2 HTTP 后台触发、主从路由与 SQL

在 `feat-10191-跑存量套装数据` 中实现两个独立 POST 接口：

| 场景 | 接口 |
|---|---|
| 套装刷新 | `/api/goods_image_refresh/refresh_suit` |
| resize 刷新 | `/api/goods_image_refresh/refresh_resize` |

**接口行为与验证：**

- 只接收正整数字符串 `limit`，默认 `"1"`。
- 固定启动对应白名单脚本，以独立后台进程执行并快速返回 `task_id`、`pid`、`limit`、`log_file`。
- 仅允许公司 IP 白名单访问，无需额外启动 Redis 消费者。
- 参数校验、访问限制、失败处理、PHP 语法、原有刷新回归测试及 Linux 后台分离验证均通过。

**数据库问题修正：**

- 定位到后台 `think` 进程不会继承 HTTP 进程中的 `DB_DEPLOY` 常量；未开启读写分离时默认连接会落到主库。
- 两个刷数脚本已显式使用 `dbreadonlyscript` 查询 MySQL。
- 套装候选收敛为十五期表中“正常、专场进行中、上架、未售罄”的套装商品图片；resize 候选按 `is_delete='0'`、`crop_url LIKE '%resize%'` 和资源 ID 游标筛选。

**未验证与风险：**

- 目标环境仍需确认 `tp5/.env` 中 `SCRIPT_PHP7` 的真实可执行路径，以及 FPM 用户的 `exec` 权限。
- 需确认 `dbreadonlyos.hostname` 确实指向从库。
- 线上尚未执行 `EXPLAIN`；`LIMIT 10` 只限制返回行数，不能限制 JOIN 扫描量。
- 当天最后记录显示：变更尚未提交、部署或执行真实刷数。

### 2.3 Ruflo 与知识库架构研究

**已确认：**

- Ruflo 是 Codex、Claude Code 等客户端外部的 Agent 编排层，可提供任务协调、持久记忆、工作流和监控。
- 登记 Agent 不等于 Agent 已经执行任务；真实执行仍依赖客户端子代理、执行接口或独立 worker。
- “自学习”主要指记忆、经验评分和路由反馈，不代表底层模型被训练。
- 知识库中的 `mandatory` 应按任务确定性加载，`discovery` 适合语义索引，`excluded` 必须排除。
- Ruflo 可作为统一知识访问入口，但正式知识仍以现有知识库为权威源；检索命中后必须回读原文并核对版本、适用范围和最后核实日期。

**形成的方案：**

```text
Codex / Claude Code / 其他 Agent
            │
        Ruflo MCP
            │
      知识库适配器
   ┌────────┴────────┐
正式知识库        检索索引
   │
既有审查与落库门禁
```

知识库工作流建议拆成四层：

1. **共享交付骨架**：事实来源、Gate、证据、完成标准和中断恢复。
2. **项目开发约定**：仓库、分支、环境、测试、发布和文档规则。
3. **任务流程**：需求开发、缺陷修复、审查、测试或排障。
4. **工具适配能力**：读取需求、准备分支、创建文档/MR、查询环境。

这样可保留 yishouapp 商城现有流程，同时让 yishou衣者等新项目独立配置，避免继承商城专属约定。

**未验证：** Ruflo 尚未安装，知识库适配器、统一 MCP 后端、权限隔离和索引同步均未实施。

## 3. 值得沉淀

1. **契约测试要覆盖接收方解析**：只断言发送端字段不够，应把真实请求交给下游模型反序列化，才能发现字段被静默忽略。
2. **后台进程要显式声明依赖**：HTTP 进程中的常量、连接和环境状态不会自然传给独立 CLI，数据库连接、PHP 路径和日志位置都应显式确定。
3. **小批量不等于低查询成本**：`LIMIT 1/10` 只能限制结果集，仍需通过 `EXPLAIN` 检查 JOIN、索引和游标条件。
4. **“已受理”与“已完成”分层表达**：HTTP 200、后台启动、下游受理、向量生成和 PG 更新是不同阶段，应逐层留证。
5. **知识检索不能替代治理**：必读规范确定性加载、发现类知识才做语义检索，命中后仍回读权威原文。

## 4. 明日线索

1. 在目标环境确认 `SCRIPT_PHP7` 与 FPM `exec` 权限。
2. 两个接口分别以 `limit=1` 串行验证，核对 `task_id`、日志和完整请求 body。
3. 套装、resize 各选一条记录，保存前后快照并回查向量与更新时间。
4. 核对从库配置，并对套装 MySQL SQL、resize PG SQL 执行 `EXPLAIN`。
5. 明确异步接口是否需要消费 `resource_type`；如需要，补下游契约与测试。
6. Ruflo 先做 10～20 篇文档的只读试点，验证检索准确率、过期内容过滤和原文回读。

## 5. 今日访问概览（Chrome）

| 次数 | 域名 | 主要用途 |
|---:|---|---|
| 22 | `github.com` | Ruflo、WeKnora 等开源项目资料 |
| 12 | `yearning.yishou.com` | SQL 查询与审核 |
| 9 | `yb7ao262ru.feishu.cn` | 飞书需求与业务文档 |
| 3 | `gitlab.yishou.com` | GitLab |
| 2 | `zentao.yishou.com:8088` | 禅道任务 |
| 2 | `zentao.yishou.com` | 禅道任务 |
| 1 | `prd-upload-pub.yishouapp.com` | OS 商品库页面 |
| 1 | `arxiv.org` | 论文页面 |

---

*数据来源：Claude Code 0 条｜Codex 188 条｜Chrome 52 次；由 Hermes 基于 2026-10-22 raw 数据降级生成。*
