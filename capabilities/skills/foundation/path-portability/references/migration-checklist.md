# 共享中台 v2 跨机器迁移清单

## 1. 前置

- 源机器 A：已有可用的 shared hub v2 实例
- 目标机器 B：具备 Python 3.9+、git、bash
- 网络：能 clone 或 scp 源机器 A 的目录
- 共享身份：知道目标机器的 `whoami`（用于拼 `~/agent/shared` 之类）

## 2. 打包

> 只保留 `manifest.yaml: deployment.portable.must_preserve` 里的内容。

```bash
cd <A 上的 shared-root>
tar czf /tmp/shared-hub.tgz \
  manifest.yaml AGENTS.md README.md \
  curated/ capabilities/ compat/ prefill/
```

> 不打包 `runtime/` 与 `inbox/*/daily/`。这些是机器本地产物，迁过去反而干扰清理。

## 3. 传输

```bash
# 方式 1：scp
scp /tmp/shared-hub.tgz B:/tmp/

# 方式 2：通过 git（如果用 PR/branch 模式）
#   在 A 上 push 一个迁移 branch，B 上 clone 即可
```

## 4. 解压

```bash
# 选一个宿主路径（建议 ~/agent/shared，但任意都行）
mkdir -p ~/agent/shared
cd ~/agent/shared
tar xzf /tmp/shared-hub.tgz
```

## 5. 校验

```bash
cd ~/agent/shared
python3 scripts/resolve_shared_root.py --check
python3 scripts/resolve_shared_root.py --explain
```

预期：

- `--check` 退出码 0
- `--explain` 列出尝试过的候选路径

## 6. 显式声明（可选）

如果 shared 根不在标准探测路径下，建议显式 export：

```bash
echo 'export SHARED_HUB_ROOT=~/agent/shared' >> ~/.bashrc
source ~/.bashrc
```

## 7. 接入 agent

### Hermes

确认 `~/.hermes/config.yaml` 里 `shared_root` 或类似字段指向正确路径（如果项目里有写死 `/home/vany/...`，按 `path-portability` skill 改为动态解析）。

### OpenClaw

同上。容器内使用 `SHARED_HUB_ROOT` 显式指定或通过挂载点让 `script:..` 自动命中。

## 8. 第一次跑 daily / weekly

```bash
cd ~/agent/shared
python3 scripts/promoter.py --dry-run --scan-promote-candidates --recent-limit 10
python3 scripts/verify_bridge.py
```

## 9. 排错

| 现象 | 原因 | 修复 |
|---|---|---|
| `resolve_shared_root.py` 解析到错的目录 | 多个候选都"看起来合法" | 用 `SHARED_HUB_ROOT` 显式指定 |
| `verify_bridge.py` 找不到 hermes 配置 | `~/.hermes/config.yaml` 引用了旧路径 | 按 config-target-routing skill 改 |
| OpenClaw 容器内找不到 shared | 挂载点改了 | 在容器内 `echo $SHARED_HUB_ROOT` 检查 |
| Git 历史里出现 `runtime/` | 早期提交未 ignore | 用 `git rm --cached -r runtime/` 清理 |

## 10. 迁移后必做

- [ ] 在 `curated/memory/projects/<本机名>-onboarding.md` 写一行"已接入 shared hub v2"
- [ ] 更新 `curated/memory/MEMORY.md` 的"当前状态"小节
- [ ] 跑一次 `promoter.py --dry-run` 把状态块刷进 MEMORY.md
- [ ] 把本机 `<shared-root>/runtime/<agent>/` 加入 git 忽略
