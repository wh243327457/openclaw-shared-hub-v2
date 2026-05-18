# Docker OpenClaw 复用共享中台流程验证计划

日期：2026-04-25
状态：已完成
负责人：Hermes 总控

## 目标

在 Docker 中启动一个 OpenClaw 实例，复用宿主共享中台：

- 宿主 shared：`/home/vany/agent/.openclaw/shared`
- 容器 shared：`/home/node/.openclaw/shared`

验证完整流程中的：

1. 启动卡点
2. shared 读取卡点
3. OpenClaw 写入卡点
4. skills / memory 兼容入口卡点
5. 可优化点
6. 可自动化点

## 安全边界

- 禁止把明文 secret 写入 shared。
- 默认不让容器整体 RW 写入 shared。
- curated/memory、capabilities、manifest、AGENTS 默认只读。
- OpenClaw 可写目录仅限：
  - `shared/inbox/openclaw/daily`
  - `shared/runtime/openclaw`
  - `shared/compat/daily`（仅兼容旧 daily 写入）

## 当前已确认事实

- OpenClaw 镜像存在：`ghcr.io/openclaw/openclaw:latest`
- 镜像默认用户：`node`，uid/gid 为 `1000:1000`
- 镜像默认命令：`node openclaw.mjs gateway --allow-unconfigured`
- 工作目录：`/app`
- 镜像健康检查访问：`http://127.0.0.1:18789/healthz`
- 首次 root 启动时若不显式设置 `HOME`，OpenClaw 会把 auth store 定位到 `/root/.openclaw/agents/main/agent/auth-profiles.json`，导致模型诊断报 `No API key found for provider openai`。
- 使用 `--user 0:0 -e HOME=/home/node` 后，OpenClaw 配置根路径回到 `/home/node/.openclaw`，gateway 可正常健康检查。
- 宿主端口 `18789/18790/18791` 审计时均空闲；当前验证容器占用 `18790 -> 18789`。
- 当前运行中的验证容器：`openclaw-shared-smoke-homefix`。
- shared 中台结构 `verify_bridge.py` 通过，`ok: true`。
- `openclaw.json` 已包含容器侧 shared skills 入口：`/home/node/.openclaw/shared/skills`。

## 阶段状态

| 阶段 | 状态 | 说明 |
|---|---|---|
| 1. 只读审计 | ✅ 已完成 | 镜像、shared 结构、verify_bridge、端口状态已确认 |
| 2. 启动计划落盘 | ✅ 已完成 | 本文件即计划真相源 |
| 3. 只读 smoke test | ✅ 已完成 | 容器内可读 manifest、AGENTS、MEMORY、skills 与兼容入口 |
| 4. 写入权限验证 | ✅ 已完成 | 以 `--user 0:0` 验证 inbox/runtime/compat 可写，curated 保持只读 |
| 5. 安全启动 gateway | ✅ 已完成 | `openclaw-shared-smoke` 已启动，`/healthz` 返回 live |
| 6. shared 流程验证 | ✅ 已完成 | OpenClaw 配置包含 `/home/node/.openclaw/shared/skills`，verify_bridge 通过 |
| 7. 卡点与自动化沉淀 | ✅ 已完成 | 已记录权限、HOME 漂移、RW 风险、compat 分流等卡点，并沉淀优化/自动化建议 |

## 推荐启动策略

### 原则

共享根只读，OpenClaw 需要写的目录单独 RW 覆盖挂载。

### docker run 模板

```bash
docker run --rm \
  --name openclaw-shared-smoke \
  --user 0:0 \
  -e HOME=/home/node \
  -p 18790:18789 \
  -v /home/vany/openclaw-data/.openclaw:/home/node/.openclaw:rw \
  -v /home/vany/agent/.openclaw/shared:/home/node/.openclaw/shared:ro \
  -v /home/vany/agent/.openclaw/shared/inbox/openclaw/daily:/home/node/.openclaw/shared/inbox/openclaw/daily:rw \
  -v /home/vany/agent/.openclaw/shared/runtime/openclaw:/home/node/.openclaw/shared/runtime/openclaw:rw \
  -v /home/vany/agent/.openclaw/shared/compat/daily:/home/node/.openclaw/shared/compat/daily:rw \
  ghcr.io/openclaw/openclaw:latest
```

注意：上面同时挂载整个 `.openclaw` 是为了复用现有 OpenClaw 配置和 runtime。shared 再用更具体的 bind mount 覆盖为只读/局部可写，降低误写 curated 的风险。

## 预计卡点

### 卡点 1：权限

容器默认 uid/gid 是 `1000:1000`，而宿主 OpenClaw 数据目录大量文件可能是 root/vany 所有。

影响：
- 容器能读 shared，但可能不能写 `inbox/openclaw/daily` 或 `runtime/openclaw`。
- gateway 启动时也可能因为 `.openclaw` 目录不可写失败。

候选优化：
- 仅对 OpenClaw 可写目录设置 uid/gid 1000 可写。
- 或通过 `--user` 与宿主目录 owner 对齐。
- 不建议长期 root 运行容器。

### 卡点 2：shared 根 RW 风险

如果直接 `-v shared:/home/node/.openclaw/shared:rw`：
- curated/memory 可能被 OpenClaw 误写。
- runtime/cache 可能落错目录。
- shared skills 可能漂移且未更新 manifest。

优化：
- shared 根 `ro`，必要子目录单独 `rw`。

### 卡点 3：旧兼容入口与 canonical 写入分流

OpenClaw 旧路径可能写 `shared/memory/daily`，canonical 路径应写 `shared/inbox/openclaw/daily`。

优化：
- 保留 compat/daily RW 作为过渡。
- 后续让 OpenClaw 默认写 canonical inbox。

### 卡点 4：root 运行时 HOME 漂移

为了绕过宿主目录权限，短期用 `--user 0:0` 启动容器时，容器进程默认 `HOME=/root`。

影响：
- OpenClaw 会把配置和 auth store 定位到 `/root/.openclaw`。
- 即使 `/home/node/.openclaw/openclaw.json` 已挂载，模型诊断仍可能报 `No API key found for provider openai`，并查找 `/root/.openclaw/agents/main/agent/auth-profiles.json`。

优化：
- 短期验证命令必须同时加 `--user 0:0 -e HOME=/home/node`。
- 长期不建议 root 运行；应修正宿主可写目录权限，让容器用 `node` 用户运行。

## 验证命令

### 1. 只读 smoke test

```bash
docker run --rm --entrypoint sh \
  -v /home/vany/agent/.openclaw/shared:/home/node/.openclaw/shared:ro \
  ghcr.io/openclaw/openclaw:latest \
  -lc 'set -eu; id; test -r /home/node/.openclaw/shared/manifest.yaml; test -r /home/node/.openclaw/shared/AGENTS.md; test -r /home/node/.openclaw/shared/memory/MEMORY.md; test -d /home/node/.openclaw/shared/memory/daily; test -d /home/node/.openclaw/shared/skills; echo OK'
```

### 2. 写入权限 smoke test

```bash
docker run --rm --entrypoint sh \
  -v /home/vany/agent/.openclaw/shared:/home/node/.openclaw/shared:ro \
  -v /home/vany/agent/.openclaw/shared/inbox/openclaw/daily:/home/node/.openclaw/shared/inbox/openclaw/daily:rw \
  -v /home/vany/agent/.openclaw/shared/runtime/openclaw:/home/node/.openclaw/shared/runtime/openclaw:rw \
  -v /home/vany/agent/.openclaw/shared/compat/daily:/home/node/.openclaw/shared/compat/daily:rw \
  ghcr.io/openclaw/openclaw:latest \
  -lc 'set -eu; for p in /home/node/.openclaw/shared/inbox/openclaw/daily /home/node/.openclaw/shared/runtime/openclaw /home/node/.openclaw/shared/compat/daily; do if [ -w "$p" ]; then echo "WRITABLE $p"; else echo "NOT_WRITABLE $p"; fi; done'
```

### 3. gateway 健康检查

```bash
curl -fsS http://127.0.0.1:18789/healthz
```

## 自动化候选

1. `scripts/openclaw-docker-preflight.sh`
   - 检查 Docker、镜像、端口、shared 结构、symlink、权限。

2. `deploy/openclaw-shared/docker-compose.yml`
   - 固化最小权限挂载策略。

3. `scripts/openclaw-shared-smoke.sh`
   - 一键执行容器内只读/写入/gateway health smoke test。

4. `scripts/verify_bridge.py` 增强
   - 增加 Docker OpenClaw 权限检查项。
   - 增加容器路径 `/home/node/.openclaw/shared` smoke test。

## 收口记录

更新时间：`2026-04-25T13:08:56+08:00`

### 已验证

- 只读 smoke test 已通过：容器内可读 `manifest.yaml`、`AGENTS.md`、`curated/memory/MEMORY.md`、legacy `memory/MEMORY.md`、`shared/skills` 与 `capabilities/skills`。
- 写入权限 smoke test 已通过：OpenClaw 可写目录限定为 `inbox/openclaw/daily`、`runtime/openclaw`、`compat/daily`。
- curated 保护已验证：`curated/memory` 在容器内保持只读，未扩大为 shared 根 RW。
- gateway 已验证：使用 `--user 0:0 -e HOME=/home/node` 后，`http://127.0.0.1:18790/healthz` 返回 200。
- 配置入口已验证：`openclaw.json` 的 `skills.load.extraDirs` 包含 `/home/node/.openclaw/shared/skills`，模型 primary 为 `self/gpt-5.4`。

### 实际卡点

1. 权限卡点：容器默认 `node` 用户 uid/gid 为 `1000:1000`，宿主 `.openclaw` 目录权限不完全匹配；短期验证使用 root 跑容器。
2. HOME 漂移卡点：root 运行时若不加 `-e HOME=/home/node`，OpenClaw 会寻找 `/root/.openclaw/.../auth-profiles.json`，触发 `No API key found for provider openai`。
3. shared 根 RW 风险：不能把整个 `shared` 以 RW 暴露给容器，否则 `curated/memory`、`capabilities/skills`、`manifest.yaml` 都有误写风险。
4. compat 分流卡点：旧 OpenClaw daily 入口仍可能走 `shared/memory/daily`，短期保留 `compat/daily` RW，长期应推动 canonical `inbox/openclaw/daily`。

### 优化点

- 长期方案不建议 root 容器；应把需要写的目录 owner/ACL 修成容器 `node` 用户可写。
- 固化 `HOME=/home/node`，避免 OpenClaw 配置根和 auth store 漂到 `/root/.openclaw`。
- shared 根保持只读，仅对白名单子目录单独 RW 覆盖挂载。
- gateway 端口建议使用非默认验证端口（如宿主 `18790`）避免影响已有服务。

### 自动化点

1. 新增 `scripts/openclaw-docker-preflight.sh`：检查 Docker、镜像、端口、shared 结构、symlink、权限、HOME 策略。
2. 新增 `scripts/openclaw-shared-smoke.sh`：一键完成只读、写入、gateway health、curated RO 验证。
3. 新增 `deploy/openclaw-shared/docker-compose.yml`：固化最小权限挂载策略。
4. 增强 `scripts/verify_bridge.py`：加入 Docker/OpenClaw 容器侧路径和权限检查。

### 当前容器状态

- 验证容器：`openclaw-shared-smoke-homefix`
- 宿主端口：`18790 -> 18789`
- 用途：短生命周期 smoke test；如不再继续调试，可停止。
