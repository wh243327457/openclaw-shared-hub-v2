# GitHub 热门项目每日学习执行计划

**版本**: v1.0
**更新时间**: 2026-05-13
**执行者**: Hermes Agent (主控)

---

## 流程概览

```
┌─────────────────────────────────────────────────────────────┐
│  单一任务闭环（每日执行一次）                                  │
├─────────────────────────────────────────────────────────────┤
│  Step 1: 读取本 plan + 生成今日学习指令                       │
│     ↓                                                        │
│  Step 2: 触发 OpenClaw 执行深度学习                          │
│     ↓                                                        │
│  Step 3: 等待学习完成 + 审计产出                              │
│     ↓                                                        │
│  Step 4: 审计失败 → 反思 → 更新模板                          │
│         审计成功 → 更新知识库 → 推送微信（精华摘要）            │
└─────────────────────────────────────────────────────────────┘
```

---

## 微信推送内容要求（v3，重要）

### 推送定位
**这不是流程字段堆叠，而是一份用户早上能快速吸收的学习复盘。**

目标：用户不打开知识库，也能知道：
1. 今天学习主线是什么
2. OpenClaw 学了哪些项目
3. 哪些项目值得关注，为什么
4. 哪些经验能迁移到当前体系
5. Hermes 如何审计和判断
6. 明天应该继续追什么

### v3 必须包含的章节
1. **🧭 今日一句话结论** - 先给今日学习主线和最值得关注的方向
2. **🔥 今日最值得看的项目** - 用价值导向表格展示 2-3 个重点项目
3. **🎯 计划 vs 实际** - Hermes 原计划、OpenClaw 实际产出、Hermes 主观评价
4. **💡 今天真正学到的东西** - 3 条可迁移经验，必须说明来源和可迁移到哪里
5. **🎉 可沉淀判断** - 分级判断：立即沉淀 / 继续观察 / 暂不沉淀
6. **✅ Hermes 审计结果** - 不只给分数，还要说明来源、深度、迁移价值、风险和不足
7. **🧠 Hermes 主观复盘** - Hermes 自己的判断、联想、批评或表扬
8. **➡️ 明日学习建议** - 基于今日结果给出继续追踪方向和最小动作
9. **📁 知识库** - 详细报告路径

### 推送格式示例
```
📚 GitHub 热门项目学习日报 · v3
📅 YYYY-MM-DD

━━━━━━━━━━━━━━━━━━━━

🧭 今日一句话结论

今天主线是：xxxxxxxx。

我最关注的是 xxx：因为它和我们当前的 xxx 方向高度相关。

━━━━━━━━━━━━━━━━━━━━

🔥 今日最值得看的项目

| 项目 | 为什么值得看 | Hermes 判断 | 可沉淀点 |
|---|---|---|---|
| owner/repo1 | 解决什么关键问题 | 和我们有什么关系 | 可复用模式 |
| owner/repo2 | 解决什么关键问题 | Hermes 主观看法 | 可复用模式 |
| owner/repo3 | 解决什么关键问题 | 是否值得继续追 | 可复用模式 |

━━━━━━━━━━━━━━━━━━━━

🎯 计划 vs 实际

Hermes 原计划：
▸ 目标：深读 2-3 个高价值项目
▸ 重点：AI Agent / DevOps / 工具链
▸ 标准：必须提炼可迁移经验

OpenClaw 实际：
▸ 深读：X 个项目
▸ 产出：X 条经验沉淀
▸ 报告：XX 行

我的评价：✅ 达标 / ⚠️ 勉强 / ❌ 不达标
这里要表达真实情绪：惊喜、认可、失望、批评或加压。

━━━━━━━━━━━━━━━━━━━━

💡 今天真正学到的东西

1. 经验 1
   来自：owner/repo
   可迁移到：我们的 xxx 工作流

2. 经验 2
   来自：owner/repo
   可迁移到：Agent / 共享中台 / 工具链 / DevOps

3. 经验 3
   来自：owner/repo
   可迁移到：xxx

━━━━━━━━━━━━━━━━━━━━

🎉 可沉淀判断

| 模式 | 判断 | 原因 |
|---|---|---|
| 模式 1 | ✅ 立即沉淀 | 与当前体系高度相关 |
| 模式 2 | 🟡 继续观察 | 有价值，但需要二次验证 |
| 模式 3 | ❌ 暂不沉淀 | 暂时不适合当前体系 |

如果有惊喜，要明确说出来；如果 OpenClaw 学浅了，也要直接指出。

━━━━━━━━━━━━━━━━━━━━

✅ Hermes 审计结果

得分：XX/20
结论：通过 / 不通过

审计判断：
▸ 来源完整：✅ / ⚠️ + 简短原因
▸ 技术深度：✅ / ⚠️ + 简短原因
▸ 可迁移价值：✅ / ⚠️ + 简短原因
▸ 风险边界：✅ / ⚠️ + 简短原因
▸ 不足：明天要加压的点

━━━━━━━━━━━━━━━━━━━━

🧠 Hermes 主观复盘

这里必须有 Hermes 自己的判断，不要机械复述 OpenClaw。
说明：
- 今天最有价值的项目是什么
- 它让我想到什么
- 能不能迁移到用户的系统
- OpenClaw 哪些地方认真，哪些地方浅
- 明天我会如何调整学习指令

━━━━━━━━━━━━━━━━━━━━

➡️ 明日学习建议

明天建议继续追：

1. 方向 1
   原因：xxx

2. 方向 2
   原因：xxx

最小动作：一个可执行的小任务。

━━━━━━━━━━━━━━━━━━━━

📁 知识库

/path/to/report.md
```

### v3 核心原则
- 第一屏先给价值，不先报流程。
- 项目表格必须是：`项目 / 为什么值得看 / Hermes 判断 / 可沉淀点`。
- 必须有 Hermes 主观意识：判断、联想、情绪、批评或表扬。
- 情绪表达必须基于审计事实，不能机械套模板。
- 审计结果必须解释“为什么”，不能只给分数。
- 可沉淀判断必须分级：✅ 立即沉淀 / 🟡 继续观察 / ❌ 暂不沉淀。
- 明日建议必须来自今日学习结果，不能是固定话术。

### 禁止事项
- ❌ 不要只说"详见知识库"
- ❌ 不要只列审计优点
- ❌ 不要把 OpenClaw 原文机械压缩
- ❌ 不要缺少 Hermes 主观复盘
- ❌ 不要把项目表格写回“简介/亮点”
- ❌ 不要没有情绪、没有判断
- ❌ 不要生成太长的项目背景介绍
- ❌ 不要把所有项目等权展示；必须突出最值得看的 2-3 个

---

## 常量定义

### 路径常量

```yaml
# 共享根目录
SHARED_ROOT: <shared-root>

# 学习指令（Hermes 生成，OpenClaw 读取）
INSTRUCTION_FILE: ${SHARED_ROOT}/runtime/hermes/github-hot-project-learning/instruction.md

# OpenClaw 学习产出（OpenClaw 写入，Hermes 读取）
OUTPUT_FILE: ${SHARED_ROOT}/inbox/openclaw/daily/YYYY-MM-DD.md

# 项目卡片目录
PROJECTS_DIR: ${SHARED_ROOT}/runtime/openclaw/github-learning/projects/

# 经验沉淀文件
LESSONS_FILE: ${SHARED_ROOT}/runtime/openclaw/github-learning/lessons.md

# 审计反馈存储
AUDIT_FEEDBACK_FILE: ${SHARED_ROOT}/runtime/hermes/github-hot-project-learning/audit-feedback.json

# 学习模板（含审计反馈区）
TEMPLATE_FILE: ${SHARED_ROOT}/capabilities/skills/research/github-hot-project-learning/templates/daily-instruction.md

# 个人知识库
KNOWLEDGE_BASE_DIR: /mnt/d/system/selfSystem/03-学习/技术实践/GitHub 热门项目学习档案/
OVERVIEW_FILE: ${KNOWLEDGE_BASE_DIR}/00-总览索引.md
DAILY_FILE: ${KNOWLEDGE_BASE_DIR}/每日学习/YYYY-MM-DD-GitHub热门项目学习日报.md
AUDIT_FILE: ${KNOWLEDGE_BASE_DIR}/质量审计/YYYY-MM-DD-质量审计.md

# OpenClaw cron job ID
OPENCLAW_LEARNING_JOB_ID: 7aa310ea-b264-40c8-b23a-ed655c565a69
```

### 时间常量

```yaml
OPENCLAW_LEARNING_SCHEDULE: "30 8 * * *"
OPENCLAW_TIMEOUT: 1800  # 30 分钟超时
```

### 评分常量

```yaml
PASS_SCORE: 16  # 审计通过分数（20 分制）
TOTAL_SCORE: 20
```

---

## Step 1: 生成今日学习指令

**执行时机**: 每日 07:30
**执行者**: Hermes Agent
**输入**: 审计反馈历史 + 昨日遗留
**输出**: instruction.md

### 动作

1. 读取 `audit-feedback.json`，提取最近 7 天反馈
2. 分析失败点，提取需要强化的方面
3. 生成今日学习指令：
   - 学习目标（3-5 个）
   - 推荐技术栈
   - 推荐领域
   - 质量标准
   - 强化指令（来自历史失败）
4. 写入 `instruction.md`

### 验证

- [ ] 文件存在且内容完整
- [ ] 包含今日学习目标
- [ ] 包含产出要求
- [ ] 包含审计反馈区

---

## Step 2: 触发 OpenClaw 执行深度学习

**执行时机**: Step 1 完成后
**执行者**: Hermes Agent
**输入**: instruction.md
**输出**: 等待 OpenClaw 学习完成

### 动作

1. 确认 `instruction.md` 已生成
2. 执行命令触发 OpenClaw 学习：
   ```bash
   docker exec openclaw openclaw cron run 7aa310ea-b264-40c8-b23a-ed655c565a69
   ```
3. 等待 OpenClaw 学习完成（轮询检查输出文件）
4. 超时处理：如果 30 分钟未完成，标记失败并继续

### 验证

- [ ] OpenClaw 已触发执行
- [ ] 学习产出文件已生成
- [ ] 文件内容非空

### 失败处理

- 如果 OpenClaw 容器未运行：`docker start openclaw` 并重试
- 如果超时：记录错误，继续审计步骤

---

## Step 3: 审计学习产出

**执行时机**: Step 2 完成后
**执行者**: Hermes Agent
**输入**: OpenClaw 的学习产出
**输出**: 审计报告 + 评分

### 审计维度（20 分制）

| 维度 | 满分 | 检查点 |
|------|------|--------|
| 来源完整 | 2 | 仓库链接、README、release、issue |
| 事实准确 | 2 | 数据来自 GitHub API，标注查询时间 |
| 中心判断 | 2 | 明确说明为什么值得学 |
| 技术深度 | 3 | 讲清实现思路和边界 |
| 可复用动作 | 3 | 有条件-动作规则或 checklist |
| 安全合规 | 2 | license、安全、数据风险 |
| 反宣传能力 | 2 | 局限和不适用场景 |
| 完整性 | 2 | 无截断，格式规范 |
| 可迁移价值 | 2 | 提取可复用模式 |

### 动作

1. 读取 `YYYY-MM-DD.md` 学习产出
2. 按维度评分
3. 记录优点和问题
4. 写入审计结果（JSON 格式）

### 验证

- [ ] 评分已完成
- [ ] 优点和问题已记录
- [ ] 审计结果已保存

---

## Step 4: 处理审计结果

**执行时机**: Step 3 完成后
**执行者**: Hermes Agent
**输入**: 审计评分和问题
**输出**: 模板更新 或 知识库更新 + 微信推送

### 4A: 审计失败（得分 < 16）

**动作**:

1. **反思失败原因**：
   - 分析每个扣分点
   - 总结为什么学习不够深入
   - 识别是否有价值但被遗漏的内容

2. **生成改进指令**：
   - 将反思总结成具体规则
   - 格式：「当 [场景] 时，应 [动作]」

3. **更新模板**：
   - 调用 `audit_feedback_writer.py`
   - 写入审计反馈区
   - 更新强化指令

4. **输出总结**：
   - 今日失败点
   - 已更新的强化指令
   - 明日改进方向

**验证**:
- [ ] 失败原因已分析
- [ ] 模板已更新
- [ ] 强化指令已写入

### 4B: 审计成功（得分 >= 16）

**动作**:

1. **更新个人知识库**：
   ```bash
   # 创建目录
   mkdir -p "${KNOWLEDGE_BASE_DIR}/每日学习"
   mkdir -p "${KNOWLEDGE_BASE_DIR}/质量审计"
   
   # 复制学习日报
   cp "${OUTPUT_FILE}" "${DAILY_FILE}"
   
   # 写入审计报告
   # 写入审计报告
   cat > "${AUDIT_FILE}" << EOF
   # 质量审计 - YYYY-MM-DD
   
   **得分**: XX/20
   **状态**: 通过
   
   ## 优点
   - ...
   
   ## 建议
   - ...
   EOF
   
   # 更新总览索引
   # 追加今日记录到总览
   ```

2. **提取技能沉淀**：
   - 检查是否有可迁移模式
   - 如有，生成 skill 草案
   - 写入 `shared/capabilities/skills/`

3. **生成微信推送摘要**：
   ```
   📚 GitHub 热门项目学习日报 - YYYY-MM-DD
   
   🏆 今日成果
   - 深读 X 个项目
   - 提取 Y 条经验
   - 审计得分: XX/20
   
   📖 学习了什么
   1. owner/repo - 一句话判断
   2. ...
   
   🔍 审计摘要
   - 优点: ...
   - 建议: ...
   
   💡 可沉淀技能
   - skill-name: 简要描述
   
   🔗 详见知识库: ${DAILY_FILE}
   ```

4. **推送微信消息**

5. **更新反馈记录**：
   ```bash
   python3 ${SHARED_ROOT}/scripts/audit_feedback_writer.py \
     --date YYYY-MM-DD \
     --score XX \
     --issues "..." \
     --strengths "..."
   ```

**验证**:
- [ ] 知识库文件已更新
- [ ] 审计报告已生成
- [ ] 微信已推送
- [ ] 反馈已记录

---

## 失败回退

### 微信主动推送限流保护

Hermes Weixin 主动推送限流保护必须在**平台发送层统一收口**，不能挂在某个业务功能下。

已在 Hermes Weixin adapter 的 `send()` 入口实现全局计数：所有通过 `send_message(target='weixin')`、cron 自动投递、以及其它功能触发的微信文本推送都会共用同一个计数器。

已确认源码事实：

- 限流返回：`ret=-2` 或 `errcode=-2`
- 典型错误：`iLink sendmessage rate limited: ret=-2 errcode=None errmsg=rate limited`
- 单条文本默认约 2000 字上限，超长会拆成多个 chunk，拆多条更容易触发频控
- 默认每个 chunk 失败重试 4 次，限流时约 3 秒退避，但不能保证解除限流
- iLink 未暴露明确的“连续 N 条未回复即限流”官方阈值

全局保守规则：

1. 平台层维护连续主动推送计数，检测到用户微信回复后清零。
2. 连续主动推送达到 3 次且用户未回复时，发送层自动在消息末尾追加提示：
   `如果你看到这条，回复任意内容即可刷新微信会话，避免后续主动推送被 iLink 限流。`
3. 连续主动推送达到 4 次仍无回复时，发送层会追加更强提醒；业务层应避免继续推长消息，优先落盘或等用户回复。
4. 关键异常/失败告警可继续推送，但必须短消息，避免拆 chunk。
5. 出现 `ret=-2` / `rate limited` 后记录全局 `last_rate_limited_at`，后续业务不得反复补发同一长内容。

公共状态文件：

```text
/root/.hermes/weixin/weixin-push-guard.json
```

状态字段：

```json
{
  "consecutive_push_without_user_reply": 0,
  "last_push_at": "YYYY-MM-DDTHH:mm:ssZ",
  "last_context_token_mtime": 0,
  "last_rate_limited_at": ""
}
```

用户是否回复的近似判断：观察 `/root/.hermes/weixin/accounts/*.context-tokens.json` 的 mtime 是否在上次推送后变化。该方法不是官方 ACK，但足够判断“用户是否近期和 bot 对话过”。

业务脚本要求：业务脚本只生成/落盘推送内容，不要自己维护局部微信计数器，避免不同功能之间重复计数或漏计。

---

## 失败回退

| 场景 | 处理 |
|------|------|
| OpenClaw 容器未运行 | `docker start openclaw` 并重试 |
| OpenClaw 学习超时 | 记录错误，跳过审计 |
| 学习产出为空 | 标记失败，记录原因 |
| 知识库路径不存在 | 自动创建目录 |
| 微信推送失败 | 记录错误，不阻塞流程 |
| 审计脚本异常 | 记录错误，手动介入 |

---

## 执行检查清单

每次执行前检查：

- [ ] OpenClaw 容器运行中
- [ ] 共享目录可访问
- [ ] 知识库目录可访问
- [ ] 审计反馈文件可读写

执行后检查：

- [ ] instruction.md 已更新
- [ ] 学习产出已生成
- [ ] 审计结果已记录
- [ ] 模板已更新（失败时）
- [ ] 知识库已更新（成功时）
- [ ] 微信已推送（成功时）

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-05-13 | 初始版本 |
