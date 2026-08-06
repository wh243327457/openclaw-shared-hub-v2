# 2026-08-06 GitHub 热门项目学习日报

> 执行器：Hermes（本任务未调用 OpenClaw）  
> 研究时间：2026-08-06T07:30–07:38+08:00；项目速览 GitHub API 最终查询时间约 2026-08-05T23:34Z。  
> 发现来源：真实抓取 [`github.com/trending?since=daily`](https://github.com/trending?since=daily)，再逐仓使用 `gh api repos/{owner}/{repo}` 核验元数据。  
> 固定源码快照：`cloudflare/computer@76d9e75c5688713b656bce85540d9e0071cece8b`；`huangruiteng/loopx@924213b86ba7788bdb83ebecab9569ec6cd79b41`。  
> 证据目录：`runtime/hermes/github-hot-project-learning/evidence/2026-08-06/`；clone：`runtime/hermes/github-hot-project-learning/repos/`。  
> 数据边界：Stars、forks、updated/pushed 是查询时动态值；GitHub Repository API 的仓库级 License 不能替代依赖、镜像、模型、数据或发行制品审查。

## 今日结论

今天的主线是：**长驻 Agent 系统应把“工作状态”和“执行环境”都做成可恢复、带边界的控制面，而不是依赖会话记忆、定时器或一次进程退出。** `cloudflare/computer` 用 SQLite 权威 VFS、内容寻址对象、游标水位线和可重放执行事件，把 agent workspace 与执行后端解耦；`LoopX` 用 goal/todo/gate/quota/receipt/scheduler ACK，把长任务拆成有权威边界、验证和记账的 bounded turn。对 Hermes/shared hub 最值得迁移的不是两套产品，而是两个窄模式：**“游标 + 终态 + 有界重放”**和**“验证后写回、写回后记账”**。

## 证据与执行摘要

- `scripts/resolve_shared_root.py` 真实解析共享根后，按要求读取 `manifest.yaml`、`AGENTS.md`、`curated/memory/MEMORY.md`；今日原始研究只写 Hermes inbox/runtime，没有直接写 curated。
- Trending HTML 真实下载到 `runtime/hermes/github-hot-project-learning/trending.html`，大小 **595,979 bytes**；解析到 `cloudflare/computer`、`huangruiteng/loopx`、`TencentCloud/TencentDB-Agent-Memory`、`firecrawl/pdf-inspector`、`esengine/DeepSeek-Reasonix` 等 13 个仓库。
- 项目速览的 10 个仓库元数据已保存到 `runtime/hermes/github-hot-project-learning/evidence/2026-08-06/project-overview-api.json`；两仓 repo/release/issues 原始 JSON 也保存在同一证据目录。
- 两个深读仓库均通过 `git clone --depth 1` 获取并固定 HEAD；源码结论只绑定上述 commit，不外推到未来 `main`、未核验 tag 或发行制品。
- `cloudflare/computer`：读取 README、`docs/README.md`、capnweb wire 文档、四个 package manifest、issues 和关键 TypeScript 源码。先运行 `npm ci --ignore-scripts`；安装 **766 packages**，npm 报 **2 moderate + 6 high** 漏洞，并因当前 Node 22.14.0 低于部分 Babel/rolldown 包要求的 22.18.0 给出 engine warnings。`@cloudflare/dofs` 定向测试 **10 passed**；先构建 `dofs`/`rpc` 后，`@cloudflare/computerd` runner 定向测试 **22 passed**。未运行真实 FUSE、Docker、Cloudflare Durable Object、Dynamic Worker 或网络执行。
- `huangruiteng/loopx`：读取 README、架构、custom runner 集成、latest release、issues、`pyproject.toml` 及 quota/scheduler/turn/file-lock 源码；`python3 -m compileall -q loopx` 通过，两个定向测试文件真实结果 **38 passed in 0.23s**。未安装或连接 Codex/Claude/Cursor/LoopX daemon，未创建 `.loopx` 状态，未执行真实 agent turn。
- `cloudflare/computer` GitHub Releases API 返回空数组；`LoopX` 最新 Release 为 `v0.4.1`，published 2026-08-04T04:06:38Z。空 release 不能解释为“不维护”。
- 未修改 Hermes/OpenClaw 配置、provider、模型、auth、env、cron 或 secret；当前 OpenClaw runtime 不存在，也未调用 OpenClaw。

## 项目速览

下表 Stars/Forks/Language/License/Updated/Pushed 均来自约 2026-08-05T23:34Z 的 GitHub Repository API。`NOASSERTION` 表示 GitHub API 未识别仓库 License，不代表“无 License”；`updated_at` 也可能被 issue/元数据活动推进。

| 项目 | Stars | Forks | Language | License（GitHub API） | Updated / Pushed (UTC) | 今日判断 |
|---|---:|---:|---|---|---|---|
| [donnemartin/system-design-primer](https://github.com/donnemartin/system-design-primer) | 361,493 | 57,648 | Python | **NOASSERTION** | 2026-08-05T23:31:25 / 2026-03-20T01:52:19 | 大型学习资料；Stars 高但 pushed 较旧，且 License 待核验，不复制内容 |
| [obra/superpowers](https://github.com/obra/superpowers) | 267,279 | 23,877 | Shell | MIT | 2026-08-05T23:31:02 / 2026-08-05T22:34:54 | Agent skill 方法论；shared hub 已有相邻治理能力，避免追热重复升格 |
| [vercel/next.js](https://github.com/vercel/next.js) | 141,533 | 31,680 | JavaScript | MIT | 2026-08-05T23:33:43 / 2026-08-05T23:33:36 | 高活跃 Web 平台；今日与长驻 Agent 控制面主线关联较弱 |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | 81,962 | 8,820 | JavaScript | MIT | 2026-08-05T23:26:31 / 2026-08-05T19:09:28 | Skill 候选集合；只审机制与来源，不批量安装第三方 skill |
| [roboflow/supervision](https://github.com/roboflow/supervision) | 48,900 | 4,618 | Python | MIT | 2026-08-05T23:27:11 / 2026-08-05T17:59:46 | CV 工具库；模型/媒体数据边界需单独审查 |
| [esengine/DeepSeek-Reasonix](https://github.com/esengine/DeepSeek-Reasonix) | 31,560 | 2,027 | Go | MIT | 2026-08-05T23:29:11 / 2026-08-05T21:54:41 | 长驻 coding Agent；继续保留为 prefix-cache 性能复现候选 |
| [TencentCloud/TencentDB-Agent-Memory](https://github.com/TencentCloud/TencentDB-Agent-Memory) | 15,018 | 1,366 | TypeScript | **NOASSERTION** | 2026-08-05T23:30:35 / 2026-08-05T08:04:09 | 与 shared memory 相关，但 API License 未识别，禁止复制源码 |
| [firecrawl/pdf-inspector](https://github.com/firecrawl/pdf-inspector) | 11,404 | 758 | Rust | MIT | 2026-08-05T23:32:38 / 2026-08-05T22:41:44 | 昨日已深读；今日只复核热度，不重复研究 |
| [cloudflare/computer](https://github.com/cloudflare/computer) | **2,820** | **128** | TypeScript | **MIT** | 2026-08-05T23:34:29 / 2026-08-05T15:40:06 | **深读：权威 VFS、内容寻址同步、可重放 exec 生命周期** |
| [huangruiteng/loopx](https://github.com/huangruiteng/loopx) | **2,080** | **161** | Python | **MIT** | 2026-08-05T23:31:18 / 2026-08-05T22:31:12 | **深读：goal/todo/quota/receipt/scheduler 控制面** |

说明：Stars 不是成熟度、安全性或生产可用性证明。`cloudflare/computer` README 明确标为 preview；`LoopX` README 明确不是 autonomous production controller。

## 深读项目

### 1. cloudflare/computer

- **URL**：https://github.com/cloudflare/computer
- **Stars / Forks / Language / License（GitHub API）**：**2,820 / 128 / TypeScript / MIT**。
- **updated / pushed**：2026-08-05T23:34:29Z / 2026-08-05T15:40:06Z。
- **固定 commit**：[`76d9e75c5688`](https://github.com/cloudflare/computer/commit/76d9e75c5688713b656bce85540d9e0071cece8b)，author 2026-08-05T12:43:54Z，committer 2026-08-05T15:40:04Z，message `ci: adopt changesets release flow`。
- **Release 状态**：GitHub Releases API 查询返回 `[]`；package manifest 标 `0.1.0-alpha.1`，不能假定存在稳定 GitHub Release。

#### 一句话判断

`cloudflare/computer` 值得学的不是“把 shell 放进 Cloudflare”，而是它把 **SQLite 权威 workspace、内容寻址同步、后端选择、执行事件流、断线重放与资源回收**做成分层协议；这正好展示了长驻 Agent 如何避免把容器目录、WebSocket 或当前进程内存误当成永久真相。

#### 解决的问题：替代了什么旧做法

1. 替代“容器磁盘就是 Agent 工作区真相”：权威状态放 Durable Object SQLite，容器只通过 FUSE/同步投影。
2. 替代“一种执行环境写死在 Agent 代码里”：`workspace.runtime.exec(source, { backend })` 统一入口可路由 container shell、worker shell 或 worker JavaScript。
3. 替代“断线后重新跑命令”：执行事件写入 SQLite，`getExec(id, after)` 可按 sequence 续接。
4. 替代“文件变更直接携带全部 bytes”：`ChangeEntry` 只携 hash/size，缺失对象再按内容寻址传输。
5. 替代“同步成功只看 RPC resolve”：跨端 `appliedPushCursor` 与本地 watermarks 做一致性断言，远端重启后可 reset/re-baseline。
6. 替代“stdout 无限堆内存”：stream backpressure 暂停 child stdout/stderr；event log 另有 per-exec byte cap 与 TTL。

边界：README 明确该项目是 preview、API 不稳定、不可用于生产；DO 与 `computerd` 当前没有 wire version negotiation，文档还承认连接 handshake 未认证。

#### 架构 / 实现与数据流

```text
Agent / Durable Object caller
          │
          ▼
@cloudflare/computer::Workspace
  ├─ fs API ───────────────┐
  └─ runtime.exec(backend) │
          │                ▼
          │        @cloudflare/dofs
          │        SQLite: nodes/chunks/blobs/revs/watermarks
          │                │
          ▼                ▼
@cloudflare/computer-rpc (capnweb / WebSocket)
  ├─ SyncRPC: changes + hash probe + object streams
  └─ ShellRPC: exec/get/kill/dispose + sequenced events
          │
          ▼
computerd inside container
  ├─ FUSE mount / disk shim
  ├─ Runner + SQLite exec log
  └─ real shell process
```

权威文件状态在 `dofs` SQLite；sync driver 先按 cursor 拉变更，批量探测本地/远端是否已有 hash，仅传缺失 blob，应用后推进 fetch cursor。执行面由 `Runner` 产生 `stdout/stderr/heartbeat/exit` event；日志可按 `seq` 重放。container、worker-shell、worker-javascript 的语义不同，但由 backend interface 汇聚到同一 runtime facade。

#### Repo tree 摘要

```text
cloudflare-computer/
├── README.md / LICENSE / CONTRIBUTING.md / AGENTS.md
├── docs/                              # VFS、schema、sync、runtime、wire、lifecycle、performance
├── packages/
│   ├── dofs/                          # SQLite 权威 VFS、rev、blob、sync primitives
│   ├── rpc/                           # capnweb SyncRPC/ShellRPC、client/server、sync driver
│   ├── computerd/                     # 容器 daemon、FUSE/shim、process runner、exec log
│   ├── computer/                      # Workspace facade、backends、tools、git/assets/artifacts
│   └── computer-computerd-linux-x64/  # 预编译 binary 的 image context
├── examples/                          # container、worker shell/JS、think、tutorial、assets/artifacts
├── script/                            # soak、FUSE conformance、bench、exec harness
└── package.json / package-lock.json   # npm workspace 与锁定依赖图
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `packages/dofs/src/sync/fetch.ts` | object presence probe | 256-hash 分批、校验 blob bytes 长度、按输入顺序返回已有对象 |
| `packages/rpc/src/sync-driver.ts` | 双向同步编排 | batch pull、缺失 blob 传输、cursor checkpoint、watermark divergence reset、push invariant |
| `packages/rpc/src/interface.ts` | wire truth | `SyncRPC` / `ShellRPC` / `ExecEvent` / typed error；源码 exit 字段是 `code` |
| `packages/rpc/src/server.ts` | capnweb server bridge | composite server、WebSocket session、HTTP batch、AsyncIterable→ReadableStream |
| `packages/computerd/src/exec/runner.ts` | process lifecycle | cwd deadlock规避、timeout→SIGTERM/SIGKILL、heartbeat、live replay、backpressure |
| `packages/computerd/src/exec/log.ts` | durable event replay | per-id metadata、monotonic seq、byte-cap eviction、exit row、TTL/dispose |
| `packages/computer/src/backend.ts` / `runtime/*` | backend abstraction | 后端能力、连接与 runtime routing |
| `packages/*/package.json` | 依赖真相 | capnweb、just-bash、fuse-native、VFS、Workers 工具链与 peer deps |

#### 源码精读（固定 commit）

**代码块 1：`pullOnce` 用 cursor + appliedPushCursor 守住跨端一致性**  
来源：[`packages/rpc/src/sync-driver.ts#L69-L178`](https://github.com/cloudflare/computer/blob/76d9e75c5688713b656bce85540d9e0071cece8b/packages/rpc/src/sync-driver.ts#L69-L178)

```ts
export async function pullOnce(
  db: Database,
  remote: SyncRPC,
  backend?: string,
): Promise<ApplyResult> {
  return pullOnceImpl(db, remote, backend, false);
}

async function pullOnceImpl(db, remote, backend, retried) {
  const after = readFetchCursor(db, backend);
  const localPushRev = readWatermark(db, "pushRev", backend);
  const fetchResult = await remote.fetchChanges({ after });

  const pushDiverged = fetchResult.appliedPushCursor.rev < localPushRev;
  const fetchDiverged = compareChangeCursors(fetchResult.currentCursor, after) < 0;
  if (!retried && (pushDiverged || fetchDiverged)) {
    if (pushDiverged) writeWatermark(db, "pushRev", 0, backend);
    if (fetchDiverged) writeFetchCursor(db, { rev: 0, path: null }, backend);
    return pullOnceImpl(db, remote, backend, true);
  }
  assertAppliedPushCursor(fetchResult.appliedPushCursor,
                          { rev: localPushRev, path: null });
  // 后续按 256 entries 拉 blob、apply、checkpoint。
}
```

逻辑：游标不是装饰字段，而是可恢复协议的核心。远端比本地记忆更“短”时只 reset 并重试一次；第二次仍不一致则由 assertion 暴露 protocol break，避免无限自愈掩盖丢状态。每批 `applyChanges` 后才推进 `(rev,path)`，crash 可能重放，但由 idempotent apply 吸收。

**代码块 2：`hasObjects` 不把 metadata row 误当完整对象**  
来源：[`packages/dofs/src/sync/fetch.ts#L35-L64`](https://github.com/cloudflare/computer/blob/76d9e75c5688713b656bce85540d9e0071cece8b/packages/dofs/src/sync/fetch.ts#L35-L64)

```ts
const PROBE_BATCH = 256;

export function hasObjects(db: Database, hashes: Uint8Array[]): Uint8Array[] {
  if (hashes.length === 0) return [];
  const present = new Set<string>();
  for (let i = 0; i < hashes.length; i += PROBE_BATCH) {
    const window = hashes.slice(i, i + PROBE_BATCH);
    const placeholders = window.map(() => "?").join(", ");
    const rows = db.all<{ hash: Uint8Array }>(
      `SELECT b.hash FROM vfs_blobs b
       JOIN vfs_blob_bytes bb ON bb.hash = b.hash
       WHERE b.hash IN (${placeholders})
         AND length(bb.bytes) = b.size`,
      ...window,
    );
    for (const row of rows) present.add(toHex(row.hash));
  }
  return hashes.filter((h) => present.has(toHex(h)));
}
```

逻辑：存在性证明同时要求 metadata、payload 和 length 一致，防止“有索引但 bytes 缺失”被当成 cache hit。256 的批量上限降低 SQLite parameter/frame 风险。边界是这里只核对长度，没有重新计算 hash；完整性仍依赖写入路径和后续 invariant。

**代码块 3：`Runner.exec` 避开在自己的 FUSE mount 上同步 `chdir` 的死锁**  
来源：[`packages/computerd/src/exec/runner.ts#L104-L173`](https://github.com/cloudflare/computer/blob/76d9e75c5688713b656bce85540d9e0071cece8b/packages/computerd/src/exec/runner.ts#L104-L173)

```ts
exec(command: string, options: ExecOptions = {}): ExecHandle {
  const id = options.id ?? randomUUID();
  if (this.records.get(id)?.live) {
    throw new ExecError("EEXEC_BUSY", `exec id ${id} is already running`);
  }
  const cwd = options.cwd ?? this.opts.cwd;
  if (cwd !== undefined) {
    try { stat(this.db, cwd); }
    catch (err) { return this.spawnFailed(id, err); }
  }

  const wrapped = cwd !== undefined
    ? `cd ${shellQuote(cwd)} && ${command}`
    : command;
  const child = spawn("/bin/sh", ["-c", wrapped], { env, stdio: [/*...*/] });

  const onData = (name: "stdout" | "stderr") => (chunk: Buffer) => {
    const value = new Uint8Array(chunk);
    const seq = log.append(name, value);
    record.subscriber?.enqueue({ id, seq, name, value });
  };
}
```

逻辑：`uv_spawn` 内同步 `chdir` 到由本进程服务的 FUSE mount 会让 event loop 无法响应 FUSE lookup；实现先直接查 SQLite 验证 cwd，再让已启动的 `/bin/sh` 执行 `cd`。`shellQuote` 只保护 cwd 参数，用户 command 本身就是设计上交给 shell 的代码，因此调用者仍必须把 exec 视为高权 effect。

**代码块 4：event log 有界持久化，live stream 则按 backpressure 暂停 child pipe**  
来源：[`packages/computerd/src/exec/log.ts#L90-L120`](https://github.com/cloudflare/computer/blob/76d9e75c5688713b656bce85540d9e0071cece8b/packages/computerd/src/exec/log.ts#L90-L120) 与 [`runner.ts#L345-L418`](https://github.com/cloudflare/computer/blob/76d9e75c5688713b656bce85540d9e0071cece8b/packages/computerd/src/exec/runner.ts#L345-L418)

```ts
append(name: "stdout" | "stderr", value: Uint8Array): number {
  const meta = this.meta();
  const seq = this.nextSeq++;
  if (meta?.evicted === 1) return seq;
  const newBytes = meta.bytes + value.byteLength;
  if (newBytes > this.opts.maxBytes) {
    this.evict();
    return seq;
  }
  this.db.transactionSync(() => {
    this.db.run(`INSERT INTO computerd_exec_log (...) VALUES (...)`, /*...*/);
    this.db.run(`UPDATE computerd_exec_meta SET bytes = ? WHERE exec_id = ?`,
                newBytes, this.id);
  });
  return seq;
}

// makeLiveStream subscriber:
if ((controller.desiredSize ?? 1) <= 0) {
  record.child.stdout?.pause();
  record.child.stderr?.pause();
}
```

逻辑：replay log 超预算时删除 rows 并标 `evicted`，后续 replay 抛 `ELOG_TRUNCATED`；但 live seq 继续递增。另一方面，consumer queue 满会暂停 child pipes，让内核 pipe 自然施加 backpressure。边界是“有界日志”意味着慢恢复者可能失去历史，必须把 `ELOG_TRUNCATED` 当显式终态而不是空输出。

#### 依赖分析与供应链风险

- root workspace 的主要 dev tooling：Biome、Changesets、TypeScript 6、esbuild、sherif、postject。
- `@cloudflare/computer` direct runtime dependencies：`acorn ^8.17.0`、`capnweb ^0.8.0`、`just-bash ^3.0.1`；optional peer：`@platformatic/vfs`、AI SDK、Zod。
- `@cloudflare/computer-rpc` direct：workspace `@cloudflare/dofs` + `capnweb ^0.8.0`。
- `@cloudflare/computerd` direct：workspace `rpc/dofs`、`@platformatic/vfs ^0.4.0`、`fuse-native ^2.2.6`；Node 要求 `>=22`，真实 FUSE 还依赖 native toolchain、libfuse 与 privilege。
- `npm ci --ignore-scripts` 真实安装 766 packages；忽略 scripts 可避免本机直接构建 native FUSE，但也不能证明正常安装路径可用。
- `npm audit --json` 真实结果：**8 vulnerabilities = 2 moderate + 6 high + 0 critical**。列出的直接或传递面包括 `@cloudflare/vite-plugin`、`@cloudflare/vitest-pool-workers`、`wrangler`、`miniflare`、`sharp`、`undici`、`fast-uri`、`hono`。这是当前 lockfile/npm advisory 的观测，不等于运行时均可达，也不能忽略。
- 安装时大量 Babel/rolldown 相关包要求 Node `^22.18.0 || >=24`，本机为 22.14.0；定向 tests 通过不消除完整 build/toolchain 的 engine 风险。
- prebuilt `computerd` image、GHCR provenance、Cloudflare platform runtime 与 native FUSE 库不是 repo MIT/API License 能覆盖的供应链结论。

#### README / docs / issues / source 交叉核验

- README 所述 DO SQLite→capnweb→computerd/FUSE 路径能在 `packages/dofs`、`rpc`、`computerd` 和 `computer/backends` 目录找到，三后端入口也在 `packages/computer/package.json` exports 中存在。
- README 明确 preview、非生产；docs 又明确 wire 无 version negotiation、handshake 未认证、frame/batch 限制尚未完全落地，这些都支持“只做 POC”的判断。
- open issue [#59](https://github.com/cloudflare/computer/issues/59) 指出 `docs/08_capnweb_interface.md` 把 exit event 写成 `value`，而实际 [`interface.ts#L150-L153`](https://github.com/cloudflare/computer/blob/76d9e75c5688713b656bce85540d9e0071cece8b/packages/rpc/src/interface.ts#L150-L153) 是 `code`；本报告以源码为准。该 issue 还声称 `EUNKNOWN_HASH` 文档与源码不符，后半项未在本报告完整追踪所有 raise path，标为**待核验**。
- issue [#55](https://github.com/cloudflare/computer/issues/55) 报告 trailing symlink write 可能写到 link inode 并丢数据；[#54](https://github.com/cloudflare/computer/issues/54) 报告 relative symlink resolution 错误；这些 issue 尚未由本机 fixture 复现，不能写成已确认缺陷，但足以说明 VFS correctness 仍在快速演进。
- issue [#58](https://github.com/cloudflare/computer/issues/58) 关注 capnweb stub leak tracker under-count；[#52](https://github.com/cloudflare/computer/issues/52) 报告 deployed Container 的 PDF tutorial 路径失败。两者都说明 unit path 之外还需要 soak/deployed evidence。
- GitHub Releases API 空；不能把 package `0.1.0-alpha.1` 与稳定发布混为一谈。

#### 真实测试结果

```text
$ npm test --workspace @cloudflare/dofs -- --run src/sync/fetch.test.ts
Test Files  1 passed (1)
Tests       10 passed (10)

$ npm run build --workspace @cloudflare/dofs
$ npm run build --workspace @cloudflare/computer-rpc
$ npm test --workspace @cloudflare/computerd -- --run src/exec/runner.test.ts
Test Files  1 passed (1)
Tests       22 passed (22)
```

首次直接跑 `computerd` test 因 sibling `@cloudflare/dofs` 的 `dist` 尚不存在而失败；按仓库 AGENTS 指引先构建 sibling packages 后通过。这验证了 fetch/object probe 与 runner fake/SQLite lane，不验证真实 FUSE、privileged Docker、WebSocket soak、DO、worker backend、Cloudflare deployment 或完整 workspace test。

#### 可复用经验

- 当状态需要跨容器重启或断线恢复时，应优先把权威数据与投影视图分离，并用 cursor/watermark 显式比较，因为“连接还在”不代表远端状态还在；边界是 reset 只能自动一次，持续分歧必须 fail loudly。
- 当同步大对象树时，应优先让 change record 只携 immutable content hash，并先批量 probe 再传缺失 payload，因为 inline bytes 会放大网络和内存；边界是 hash/object scope、完整性重算和 GC 仍需独立设计。
- 当命令可产生长输出并支持重连时，应优先使用 monotonic seq + bounded replay + explicit truncation terminal，因为 EOF 或空 replay 不能证明完整；边界是业务完成仍需 expected artifact/validator。
- 当进程 stdout 的消费者变慢时，应优先把 backpressure 传到 child pipe，而不是只在应用层无限缓存；边界是 child 阻塞可能改变 timeout 行为，必须有 kill/retention policy。

#### 30 分钟最小实验

在 `runtime/hermes/github-learning-poc/cursor-terminal-replay/` 做纯 Python、无网络 fixture：

1. `state.json` 保存 `source_rev, applied_cursor, events[{seq,kind,payload_hash}], terminal`。
2. fixtures 覆盖：正常增量、apply 后 checkpoint 前 crash、远端 rev 回退、seq gap、log truncated、重复 event、终态后追加。
3. validator 要求 cursor 只前进、terminal exactly-one、truncated 不能投影为 completed、同 hash 重放 idempotent。
4. 只使用 synthetic bytes；不安装 Cloudflare package，不启动 FUSE/Docker，不连接 DO，不写 curated。

#### 风险边界

- **License**：GitHub API、root LICENSE 和 package manifests 为 MIT；npm dependencies、GHCR image、native libfuse、Cloudflare platform、示例使用的外部服务另审。
- **维护活跃度**：固定 commit 与 API pushed 时间均在查询日前一天，活跃度高；但 repo 历史很短、GitHub Releases 为空、API 标 alpha/preview，变更风险同样高。
- **安全风险**：workspace exec 是任意 shell/code effect；FUSE 需 privilege；wire handshake 当前未认证；frame/hash batch 没有完整强制上限；VFS parser/path/symlink bug 会影响隔离和数据完整性。
- **供应链风险**：npm audit 报 8 个漏洞；native addon 与预编译 binary 扩大制品面；当前 Node engine 低于若干工具依赖要求。
- **一致性局限**：无 wire version negotiation；DO/daemon lockstep rollout；cursor reset 依赖 idempotent apply；hash presence 检查不等同每次重算内容 hash。
- **运行局限**：定向 32 tests 通过，但未跑完整 suite、FUSE、Docker、soak、deployment 或性能 benchmark。
- **不适用场景**：生产多租户高权沙箱、强合规取证、超大 monorepo/大量 sequential I/O、不能容忍 preview API break 的系统。
- **不可自动执行**：不自动启用 privileged container/FUSE，不把 secret 注入未知 command，不自动部署 Worker/DO，不因 README 示例修改 Hermes/OpenClaw 配置。

#### Skill 升格判断

**需二次验证。**

- **可迁移候选**：`cursor-terminal-replay` 契约——scope、source revision、cursor、dense seq、terminal、truncated、artifact hash。
- **需验证**：先用 synthetic crash/replay/divergence fixtures，再对 shared hub 现有 orchestrator 的 runtime 状态做只读 replay shadow；验证前不改生产脚本。
- **暂不沉淀**：Cloudflare DO/FUSE/capnweb 实现、worker backends、shell tools、Cloudflare deployment skill；它们是平台特定且当前仍 preview。
- **今日动作**：只写 runtime project card、lessons 与 candidate；不创建 shared skill，不复制上游源码，不写 curated active fact。

#### Hermes / shared hub 落地路径

1. POC：`runtime/hermes/github-learning-poc/cursor-terminal-replay/{schema.json,fixtures/,validate.py,test_contract.py,README.md}`。
2. Hermes GitHub learning：未来可给 `runtime/hermes/github-hot-project-learning/status.json` sidecar 增加 `attempt_id, evidence_cursor, terminal_kind, artifact_hash`，先 shadow read，不直接改当前 completed 判定。
3. shared hub：raw events/cache 留 `runtime/hermes/`；完整研究留 `inbox/hermes/daily/`；跨 Agent 验证后的最小契约才考虑更新现有 `capabilities/skills/research/github-hot-project-learning/`。
4. OpenClaw runtime 当前不存在；只设计 agent-neutral schema，不创建、不调用 OpenClaw adapter。

---

### 2. huangruiteng/loopx

- **URL**：https://github.com/huangruiteng/loopx
- **Stars / Forks / Language / License（GitHub API）**：**2,080 / 161 / Python / MIT**。
- **updated / pushed**：2026-08-05T23:31:18Z / 2026-08-05T22:31:12Z。
- **固定 commit**：[`924213b86ba7`](https://github.com/huangruiteng/loopx/commit/924213b86ba7788bdb83ebecab9569ec6cd79b41)，author/committer 2026-08-05T20:06:42Z，message `fix(host-mode): preserve existing identity selection (#2803)`。
- **最新 Release**：[`v0.4.1`](https://github.com/huangruiteng/loopx/releases/tag/v0.4.1)，published 2026-08-04T04:06:38Z；固定 `main` 晚于该 release，源码结论不自动外推到 v0.4.1 artifact。

#### 一句话判断

LoopX 值得学的不是“再做一个 Agent runtime”，而是它明确把 runtime 外的 **goal、todo、claim、gate、quota、evidence、scheduler hint、typed turn receipt**收进 durable control plane，并坚持“host 执行一段、validator 独立验真、writeback 后才 spend”；这与 Hermes/shared hub 的 cron 学习闭环高度相关，但仓库规模和协议面也显示出明显复杂度税。

#### 解决的问题：替代了什么旧做法

1. 替代“聊天记录就是长期目标状态”：registry/goal state/run history/status/quota 分层保存 durable control state。
2. 替代“定时器一到就调用模型”：`quota should-run` 先根据 gate、todo、capability、health 和预算做 decision。
3. 替代“Agent 自称完成就记账”：typed turn phases 要求 host execute→typed result→validation→durable writeback→quota spend→scheduler apply→ACK。
4. 替代“多 Agent 靠自然语言抢任务”：todo 有 `claimed_by`、task class、decision scope、continuation；hard lease 是可选、更强的并发层。
5. 替代“用户 gate 阻塞整个项目”：scope-aware gate 可允许独立 safe fallback，但不允许绕过 gate。
6. 替代“scheduler 配置写完即成功”：host observed RRULE、applied target、ACK 与 failure pair 形成显式状态机。
7. 替代“所有状态写都无限等锁”：mutation/monitor/single-flight 各有有限 timeout 与 operator incident record。

边界：README 明确 LoopX 不是 agent runtime 或 autonomous production controller；dangerous permission、publication、production write 和最终 ownership 留给人。代码仓库非常大，今天只验证 quota/scheduler 的窄切面。

#### 架构 / 实现与数据流

```text
Outer runner / Hermes cron / custom host
          │ wake + host/session setup
          ▼
loopx quota should-run
  ├─ registry + goal state + todo/gate
  ├─ capability/health/workspace boundary
  └─ quota + scheduler execution context
          │ typed decision / interaction contract
          ▼
Agent performs one bounded action
          │
          ▼
Independent validation / provider readback
          │
          ▼
Todo/evidence writeback + refresh-state
          │
          ▼
quota spend-slot（仅 validated durable writeback 后）
          │
          ▼
apply scheduler hint → host readback → ACK
```

架构文档把职责分为 Agent、Provider、Capability、Kernel：Agent 负责计划和工具；Provider 负责外部调用/观测；Capability 负责规范化、验证与 transition proposal；Kernel 负责 durable todo/gate/claim/quota/writeback。Dashboard/Kanban 只是 projection，不是状态真相源。CLI 是兼容基线，host adapter 不应复制第二套 scheduler。

#### Repo tree 摘要

```text
loopx/
├── README.md / LICENSE / pyproject.toml / AGENTS.md
├── loopx/
│   ├── control_plane/
│   │   ├── goals/                     # goal frontier、vision、boundary
│   │   ├── todos/                     # todo contract、claim、projection、defer/resume
│   │   ├── quota/                     # decision、slot accounting、turn envelope
│   │   ├── scheduler/                 # cadence、host observation、ACK/failure state
│   │   ├── runtime/                   # run history/event/state projections
│   │   ├── turn_driver/               # typed transaction、host adapter、validator
│   │   └── work_items/                # interaction/gate/attention/task graph/lease
│   ├── capabilities/                  # issue-fix、auto-research、explore、quality 等
│   ├── extensions/                    # Lark/OpenViking/process provider packages
│   ├── presentation/                  # Markdown/HTML/read models
│   └── cli*.py / quota.py / todos.py  # CLI 与 compatibility facades
├── skills/                            # LoopX 自身 host skills
├── docs/                              # architecture、protocols、guides、incidents、courses
├── apps/presentation/dashboard/       # read-first operator UI
├── examples/ / regression/            # contract smokes 与历史故障 fixtures
└── tests/                             # control-plane/capability/extension/turn tests
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `loopx/control_plane/quota/live_decision.py` | live decision composition | host observation 注入、quota payload、scheduler follow-up route binding |
| `loopx/quota.py` | compatibility facade / decision assembly | plan item、paused/health/unknown precedence、slot preview 与 ACK entry |
| `loopx/control_plane/quota/slot_accounting.py` | spend evidence | eligible/safe-bypass/repair/delivery-completion 分类，before/after 强校验 |
| `loopx/control_plane/scheduler/state_transition_rules.py` | scheduler FSM | identity reset、interval advance、failure suppression、host match ACK |
| `loopx/control_plane/turn_driver/transaction.py` | typed turn transaction | phases、result kinds、receipt validation、commit/spend/ACK eligibility |
| `loopx/file_lock.py` | local writer safety | finite POSIX lock timeout、holder metadata、incident JSONL、single-flight |
| `loopx/control_plane/todos/contract.py` | todo schema | task class/status/claim/continuation/decision scope 与规范化规则 |
| `docs/guides/custom-agent-runner-integration.md` | host contract | decide→claim→execute→validate→writeback→account→schedule 的完整顺序 |

#### 源码精读（固定 commit）

**代码块 1：live quota decision 只在 host context 适用时读取 scheduler 观测**  
来源：[`loopx/control_plane/quota/live_decision.py#L58-L106`](https://github.com/huangruiteng/loopx/blob/924213b86ba7788bdb83ebecab9569ec6cd79b41/loopx/control_plane/quota/live_decision.py#L58-L106)

```python
def build_live_quota_should_run_decision(
    status_payload: dict[str, Any], *, goal_id: str,
    agent_id: str | None, available_capabilities: list[str] | None,
    registry_path: Path, runtime_root: Path,
    host_observation_resolver: HostObservationResolver | None = None,
    scheduler_execution_context=None,
) -> dict[str, Any]:
    resolved = resolve_scheduler_execution_context(scheduler_execution_context)
    applicable = (
        resolved.ok and resolved.context is not None
        and resolved.context.codex_app_applicable
    )
    observed_rrule = ""
    if applicable and host_observation_resolver is not None:
        observation = host_observation_resolver(goal_id=goal_id, agent_id=agent_id)
        if observation.get("available") is True:
            observed_rrule = str(observation.get("rrule") or "")

    payload = build_quota_should_run(
        status_payload, goal_id=goal_id, agent_id=agent_id,
        available_capabilities=available_capabilities,
        codex_app_current_rrule=observed_rrule,
        scheduler_execution_context=resolved,
    )
    bind_scheduler_followup_cli_routes(payload,
        registry_path=registry_path, runtime_root=runtime_root)
    return payload
```

逻辑：host observation 是可注入事实源，不在不适用的 runtime profile 下乱读 Codex App；返回的 ACK/failure CLI 参数又绑定本次 registry/runtime root，避免后续命令写到另一个状态目录。边界是路径绑定仍是本地字符串契约，跨机迁移必须由目标 host 重新生成，不应缓存旧 packet。

**代码块 2：scheduler cadence 与 host apply/ACK 分成两个纯状态机**  
来源：[`state_transition_rules.py#L28-L94`](https://github.com/huangruiteng/loopx/blob/924213b86ba7788bdb83ebecab9569ec6cd79b41/loopx/control_plane/scheduler/state_transition_rules.py#L28-L94)

```python
def decide_scheduler_cadence_transition(
    progression_minutes: Sequence[int], *, scheduler_state: Mapping[str, Any],
    reset_token: str, identity_signature: str,
    advance_same_identity: bool, applied_interval_elapsed: bool,
    has_host_update_failures: bool,
) -> SchedulerCadenceDecision:
    if not scheduler_state:
        return SchedulerCadenceDecision(0, "missing", INITIAL, False)

    same_identity = (
        scheduler_state.get("reset_token") == reset_token
        and scheduler_state.get("identity_signature") == identity_signature
    )
    if not same_identity:
        return SchedulerCadenceDecision(0, "reset_required", IDENTITY_RESET, False)

    if has_host_update_failures and not current_cadence_acknowledged:
        next_index, transition = applied_index, RETRY_UNACKNOWLEDGED_FAILURE
    elif not advance_same_identity:
        next_index, transition = 0, HOLD_ACTIVE_INITIAL
    elif applied_interval_elapsed:
        next_index, transition = applied_index + 1, ADVANCE_AFTER_INTERVAL
    else:
        next_index, transition = applied_index, HOLD_UNTIL_INTERVAL
    return SchedulerCadenceDecision(/* clamped index + facts */)
```

逻辑：cadence progression 先绑定 reset token 与 identity signature；identity 改变就回到初始 cadence，失败但未 ACK 则重试当前目标。另一个 `decide_scheduler_host_transition` 才决定 apply、host-match ACK、failure suppression 或 settled。将“策略选择”和“宿主副作用”拆开，便于 pure fixture 覆盖。

**代码块 3：quota spend 强制验证 before/after 与 eligible reason**  
来源：[`loopx/control_plane/quota/slot_accounting.py#L410-L469`](https://github.com/huangruiteng/loopx/blob/924213b86ba7788bdb83ebecab9569ec6cd79b41/loopx/control_plane/quota/slot_accounting.py#L410-L469)

```python
def build_quota_slot_spend_event(preview: dict[str, Any], *,
    self_repair_spend_actions: set[str] | frozenset[str],
    source: str = DEFAULT_SLOT_SPEND_SOURCE,
    generated_at: str | None = None,
) -> dict[str, Any]:
    if not preview.get("ok"):
        raise ValueError("quota slot spend requires an eligible preview")
    slots = max(1, _int_number(preview.get("slots"), default=1))
    before = compact_quota_decision(preview.get("before") or {})
    after = compact_quota_decision(preview.get("after") or {})
    if after["spent_slots"] != before["spent_slots"] + slots:
        raise ValueError("after.spent_slots must equal before.spent_slots + slots")

    eligible_spend = (
        before["should_run"] is True
        and before["state"] == "eligible"
        and before["effective_action"] != "external_evidence_observe"
        and before["workspace_repair_allowed"] is not True
    )
    if not any((eligible_spend, safe_bypass_spend, self_repair_spend,
                capability_repair_spend, delivery_completion_spend)):
        raise ValueError("quota slot spend requires an eligible ... decision")
```

逻辑：spend 不是任意 append；它必须由可解释 decision preview 产生，before/after 精确增加 slots，并区分 normal delivery、safe bypass、self repair、capability repair 或已验证 completion。monitor/external observation 默认不应耗 delivery quota。边界是 receipt 输入若由同一不可信 actor 自行构造，仍需独立 writer/validator 和幂等键。

**代码块 4：typed turn receipt 把验证、写回、记账和 scheduler ACK 排成前缀事务**  
来源：[`loopx/control_plane/turn_driver/transaction.py#L18-L65`](https://github.com/huangruiteng/loopx/blob/924213b86ba7788bdb83ebecab9569ec6cd79b41/loopx/control_plane/turn_driver/transaction.py#L18-L65) 与 [`#L187-L267`](https://github.com/huangruiteng/loopx/blob/924213b86ba7788bdb83ebecab9569ec6cd79b41/loopx/control_plane/turn_driver/transaction.py#L187-L267)

```python
TRANSACTION_PHASES = (
    "host_execute", "typed_result", "validation", "durable_writeback",
    "quota_spend", "scheduler_apply", "scheduler_ack",
)

class LoopXTurnResultKind(str, Enum):
    VALIDATED_PROGRESS = "validated_progress"
    VALIDATED_COMPLETION = "validated_completion"
    USER_ACTION_REQUIRED = "user_action_required"
    WAIT = "wait"
    HOST_FAILURE = "host_failure"
    VALIDATION_FAILED = "validation_failed"
    WRITEBACK_FAILED = "writeback_failed"
    QUOTA_SPEND_FAILED = "quota_spend_failed"

def validate_loopx_turn_receipt(plan, result) -> dict[str, Any]:
    completed = _completed_phases(result.get("completed_phases"), errors)
    # _completed_phases 要求 completed == TRANSACTION_PHASES 的有序前缀
    if kind in MATERIAL_RESULT_KINDS and "validation" not in completed:
        errors.append("material result requires completed validation")
    if kind in NO_SPEND_RESULT_KINDS and "quota_spend" in completed:
        errors.append(f"{kind.value} cannot spend quota")
    return {
        "commit_eligibility": {
            "writeback": ok and kind in MATERIAL_RESULT_KINDS
                         and "validation" in completed,
            "quota_spend": ok and kind in MATERIAL_RESULT_KINDS
                            and "durable_writeback" in completed,
            "scheduler_ack": ok and "scheduler_apply" in completed,
        },
        "errors": errors,
    }
```

逻辑：completed phases 必须是有序前缀，失败 phase 必须正好是下一个 phase；WAIT、user action、host/validation/writeback/spend failure 都不能带 quota spend。这个模式比单个 `success=true` 更能表达“执行成功但验证失败”或“写回成功但记账失败”。边界是它不是数据库事务；跨文件/跨 host effect 仍要靠幂等、readback 和 recovery 协议收敛。

#### 依赖分析与供应链风险

- `pyproject.toml` 声明 Python `>=3.11`，**runtime dependencies = []**，主要逻辑依赖标准库；这降低第三方运行依赖面，但不降低自身协议复杂度。
- test optional dependencies：`jsonschema`、`pytest`、`pytest-cov`、`pytest-xdist`、`ruff`、`mypy`，均为版本范围而非完整 lock；今天使用系统已有环境跑定向 tests，没有新安装它们。
- package scripts 暴露 `loopx`、Lark provider 和 OpenViking semantic preference provider；optional extensions 连接外部系统时仍有独立 secret/network/privacy 风险。
- README 提供 `curl ... | bash` 安装路径；这对用户方便，但在无人值守或高权主机上应先固定 commit/digest、下载审查后执行，不能把浮动 remote shell 当供应链真相。
- 仓库包含 dashboard npm lock、多个 adapters、extensions 和大量脚本；“核心零 runtime deps”不能外推到所有 optional surface。
- 今日未运行 pip/npm audit，也未构建 dashboard；Python core 的漏洞状态与 optional web/provider 供应链均为**待核验**。

#### README / architecture / release / issues / source 交叉核验

- README 的核心 tick `quota should-run → todo claim/update → refresh-state → spend-slot` 与 custom runner guide 的八步流程、quota/todo/turn 源码一致。
- 架构文档明确 CLI 是兼容基线、dashboard/Kanban 是 projection、Kernel 才持有 durable state；源码目录也按 control_plane/presentation/capabilities/extensions 分层，但 `loopx/quota.py` 等大型 compatibility facade 仍存在迁移债务。
- v0.4.1 release 明确强化 durable work selection、Goal continuation、bounded scheduling 与 agent-scoped recall；今天读取的固定 `main` 更新更晚，不能用 release notes证明 HEAD 的全部行为。
- issue [#2760](https://github.com/huangruiteng/loopx/issues/2760) 报告 Codex CLI resume 分支曾遗漏 sandbox 和 project cwd，可能静默降级 read-only；本报告没有复现实验，状态只作为“host resume 必须重带 authority context”的风险证据。
- issue [#2785](https://github.com/huangruiteng/loopx/issues/2785) 关注同一 Codex thread 重复选择 agent identity；固定 commit message `preserve existing identity selection (#2803)` 表明该区域正在修复，但本机没有运行 Codex App，端到端状态仍待核验。
- issue [#2781](https://github.com/huangruiteng/loopx/issues/2781) 关注 quiet monitor 与 scoped user gate 歧义；说明“执行 eligibility”和“是否通知用户”必须分开，不能只看 should_run。

#### 真实测试结果

```text
$ python3 -m compileall -q loopx
# exit 0

$ python3 -m pytest -q \
    tests/control_plane/test_scheduler_state_transition_rules.py \
    tests/control_plane/test_quota_slot_accounting.py
......................................
38 passed in 0.23s
```

准确结论：Python 源码可编译，scheduler transition 与 quota slot accounting 的定向 tests 通过。没有跑完整 2,000+ 文件仓库测试、CLI integration、Codex/Claude host、dashboard、extensions、Lark/OpenViking、real scheduler 或真实 model turn；不能把 38 tests 外推为整个 LoopX 已验证。

#### 可复用经验

- 当 cron/heartbeat 决定是否调用 Agent 时，应优先把 eligibility、user notification、selected todo、quota 和 scheduler hint 分成结构化字段，因为“该运行”与“该通知”不是同一个决策；边界是字段 precedence 必须有 fixtures。
- 当工作完成会触发预算记账时，应优先坚持 `validate → durable writeback → spend`，因为进程 exit 0 或 Agent 声称完成都不是可计费进度；边界是 writer/validator 不能完全共谋。
- 当 scheduler cadence 会动态改变时，应优先记录 target、observed host value、identity/reset token、apply result 与 ACK，因为写配置命令成功不等于宿主实际采用；边界是 host readback 不可用时应 blocked/unknown。
- 当多 Agent 共享 long-running goal 时，应优先让 todo claim/lease 绑定 agent、goal、write scope 和 continuation，而不是设置永久 leader；边界是 soft claim 只做可见路由，真正并发冲突需 hard lock/lease/CAS。

#### 30 分钟最小实验

在 `runtime/hermes/github-learning-poc/validated-spend-envelope/` 做无副作用 fixture：

1. schema：`attempt_id, selected_todo, execution_status, validation, writeback, spend, scheduler_apply, scheduler_ack, terminal`。
2. fixture 覆盖：validation fail、writeback fail、duplicate spend、apply success/ACK missing、user gate + safe fallback、quiet monitor no-spend。
3. validator 要求 phases 是有序前缀；只有 validated + durable writeback 才可 spend；ACK 必须引用 observed applied value。
4. 用当前 GitHub learning status 的复制 fixture 做 shadow，不改 cron/config，不安装 LoopX，不调用模型或外部 provider。

#### 风险边界

- **License**：GitHub API 与 LICENSE 为 MIT；dashboard npm dependencies、extensions、外部 providers、文档素材和用户接入的运行时另审。
- **维护活跃度**：固定 commit 与 pushed 时间都非常新，v0.4.1 也在两天内发布；高活跃同时意味着协议、CLI 与 host integration 仍快速变化。
- **安全风险**：LoopX 自身不授予权限，但 host adapter、shell、scheduler、provider 和 extension 会执行副作用；错误的 gate/identity/cwd/sandbox 传播可能造成越权或错误写回。
- **复杂度风险**：仓库约 2,861 个非 `.git` 文件，包含超大 facade、脚本、docs 和多 optional surface；规则冲突、projection drift、兼容层债务与上下文税不可忽视。
- **状态一致性局限**：file lock 是本机 POSIX advisory lock；跨主机/网络盘/多进程事务仍需更强 backend。typed phases 不是跨系统 ACID transaction。
- **供应链局限**：core 零 runtime deps，但推荐 `curl | bash`、dashboard npm、optional providers 与 host CLI 都扩大安装面；今日未做完整 audit。
- **运行局限**：只验证 compileall + 38 tests；真实 host identity、resume sandbox/cwd、scheduler apply/readback、quota idempotency端到端待核验。
- **不适用场景**：需要生产级自动授权、跨区域强一致调度、无人审核发布/生产写、把 control plane 当 agent reasoning/runtime 替代品的场景。
- **不可自动执行**：不自动安装 LoopX，不运行其 remote install pipe，不注册 agent/goal，不改 Hermes/OpenClaw cron/config，不连接 Lark/OpenViking/Codex，不自动执行 production effect。

#### Skill 升格判断

**需二次验证。**

- **可迁移候选**：`validated-spend-envelope`——decision、bounded action、independent validation、durable writeback、spend、scheduler apply/readback/ACK。
- **需验证**：先对 GitHub learning 和其他 Hermes cron 的 synthetic/historical status 做 shadow audit，证明 duplicate、partial failure、quiet monitor 不会误记 completed/spend。
- **暂不沉淀**：LoopX CLI、完整 goal kernel、Codex/Claude host skills、Lark/OpenViking extensions、dashboard；当前 shared hub 已有 cron manager/reflection/governance，不应引入第二套状态系统。
- **今日动作**：只提出更新现有 orchestrator/verification workflow 的 candidate，不安装产品、不创建新 shared skill、不写 curated active fact。

#### Hermes / shared hub 落地路径

1. POC：`runtime/hermes/github-learning-poc/validated-spend-envelope/{schema.json,fixtures/,validate.py,test_contract.py,README.md}`。
2. Hermes orchestrator：未来可把 `prepare/research/audit/knowledge-copy/status` 映射为 phases；每 phase 保存真实 exit/readback，`overall_status=completed` 只在 report audit 与知识库 copy 均核验后写入。先旁路验证，不直接改今日脚本。
3. shared hub cron：如 POC 通过，再评估在 `scripts/cron_manager.py`/reflection input 中加入 agent-neutral `attempt_id + terminal_kind + validation_receipt`，但不引入 LoopX dependency。
4. shared skill：优先更新已有 GitHub learning/verification/reflection 能力，不复制 LoopX 的 skills；按 manifest 规则补 scope/reference policy 后才可晋升。
5. 分层：raw phase stdout/receipts 留 `runtime/hermes/`；日报留 `inbox/hermes/daily/`；稳定机制经评分、去重、脱敏与审查后才候选进入 curated。
6. OpenClaw runtime 当前不存在；不创建或调用 OpenClaw integration，只保持未来 agent 可读的 schema。

## 经验沉淀

1. **当长驻任务跨进程、容器或会话恢复时，应优先使用 scope-bound cursor/watermark、dense event sequence 与明确 terminal，因为“进程还活着”或“连接重建了”都不能证明状态完整；边界是持续 divergence 必须 fail loudly，不能无限 reset。**
2. **当结果会触发预算、完成态或后续调度时，应优先执行 `独立验证 → durable writeback → 记账 → scheduler apply/readback/ACK`，因为 exit 0、prose 和发送命令都不是最终事实；边界是每一步仍需幂等键和真实 readback。**
3. **当同步对象大且重复率高时，应优先用 scoped immutable content hash + batch presence probe + missing-only transfer，因为 inline payload 和逐对象 round-trip 都会放大成本；边界是 metadata presence 不能替代 payload/length/hash 完整性。**
4. **当 stdout、event 或 evidence 可无限增长时，应优先同时设计 live backpressure、bounded replay、TTL 和 explicit truncation，因为只限制一种缓存仍会在另一层爆炸；边界是 truncated 必须阻止“完整成功”投影。**
5. **当 scheduler 或 host policy 可能变化时，应优先把目标值、observed value、identity/reset token、apply 和 ACK 分开，因为 cached instruction 会把旧宿主状态带进新运行；边界是 ACK 必须绑定实际 readback。**
6. **当多 Agent 共享目标但没有永久 leader 时，应优先使用 todo/claim/lease/decision scope 和 bounded handoff，因为 display name 或聊天上下文无法提供并发权威；边界是 soft claim 不等于跨进程写锁。**
7. **当 README/docs 与源码不一致时，应优先固定 commit 并读取 interface/实现/tests/issues，因为 forward-looking 文档或 release prose 可能滞后；边界是定向源码核验仍不能外推到未运行 deployment。**
8. **当热门项目宣称 core 轻量或零依赖时，应优先分别审 core、dev toolchain、native binary、optional extension 与安装路径，因为 package-level依赖声明不能覆盖完整供应链；边界是 npm/pip audit 也只代表当前 advisory 观测。**

### 跨项目机制抽象

| 机制 | cloudflare/computer | LoopX | 对 Hermes/shared hub 的窄迁移 |
|---|---|---|---|
| 权威状态 | SQLite VFS / rev / blob | registry / goal / todo / run history | curated/inbox/runtime 分层继续保持，status 不反向成为真相 |
| 恢复身份 | backend + cursor + exec id + seq | goal + agent + todo + turn key | attempt id + runner + report path + evidence hash |
| 进度证明 | apply cursor / event replay / exit | validation / writeback / spend receipt | audit score + file hash + knowledge copy readback |
| 失败表达 | divergence、ELOG_TRUNCATED、typed wire error | validation/writeback/spend/host failure | blocked/failed/partial/completed 分离 |
| 资源治理 | batch、backpressure、byte cap、TTL | quota、bounded turn、cadence | 每次 cron 的 evidence/output/time budget |
| 风险边界 | preview、unauth wire、FUSE privilege | human gate、no production authority | 不自动改 config/cron/secret，不自动晋升 curated |

## 明日继续

1. 实现 `runtime/hermes/github-learning-poc/validated-spend-envelope/` 的最小 schema 与 6 个 synthetic fixtures；只做 shadow validator，不改当前 orchestrator。
2. 将昨日 `routing-envelope-v0` 候选与今日 `cursor-terminal-replay`、`validated-spend-envelope` 去重，判断能否合成一个更小的 `attempt-evidence-envelope-v0`。
3. 对 `cloudflare/computer` 补一个只读源码核验：追踪 issue #59 所述 `EUNKNOWN_HASH` 当前实际 raise path，并检查 docs/source/test 三方差异；不启动 FUSE。
4. 若时间允许，对 LoopX 只跑 `tests/test_loopx_turn_transaction.py`，验证 typed phase/receipt，而不是扩大到完整产品安装。

## 候选反哺

### Candidate Facts

- [ ] topic: 长驻任务恢复需要 cursor/seq/terminal，而不是 connection/process 状态 | evidence: `cloudflare/computer@76d9e75 packages/rpc/src/sync-driver.ts`, `packages/computerd/src/exec/{runner,log}.ts`，定向 32 tests 通过 | 建议: create（先 runtime POC，非 active fact） | 安全级别: low
- [ ] topic: 自动任务预算应在独立验证和 durable writeback 后记账 | evidence: `loopx@924213b loopx/control_plane/{quota/slot_accounting.py,turn_driver/transaction.py}`，定向 38 tests 通过 | 建议: dispute/merge with existing verification-first facts，避免重复 | 安全级别: low
- [ ] topic: scheduler apply 需要 host readback + ACK + identity reset token | evidence: `loopx/control_plane/scheduler/state_transition_rules.py` 与 custom runner guide | 建议: create candidate，先对 Hermes cron 做 shadow fixture | 安全级别: medium

### Candidate Skills / Workflow

- [ ] 名称: attempt-evidence-envelope-v0 | 可复用场景: GitHub learning、教程学习、巡检、reflection 等 cron 的 phase/validation/terminal 证据 | 是否建议 shared: yes（验证后更新既有 workflow，优先不新建） | 原因: 跨 Agent 可复用，但需与 source-outcome/completion/verification candidates 去重
- [ ] 名称: cursor-terminal-replay fixture | 可复用场景: runtime 状态断点恢复、重复执行、截断与 divergence 审计 | 是否建议 shared: no（当前仅 Hermes runtime POC） | 原因: 尚未证明真实 shared hub 收益
- [ ] 名称: LoopX product integration | 可复用场景: 完整 goal/todo/quota controller | 是否建议 shared: no | 原因: 与现有 cron manager/reflection/shared hub 重叠，且会引入第二控制面和较大复杂度

### Candidate Open Questions

- [ ] 问题: `cloudflare/computer` 当前 `EUNKNOWN_HASH` 在 source/tests 中是否已真正 raise，还是 docs/issue 的版本判断不一致？ | reason: conflict | priority: medium
- [ ] 问题: 当前 GitHub learning `overall_status=completed` 是否应要求知识库目标文件 hash/readback，而不仅是 audit pass 后 copy 调用？ | reason: gap | priority: high
- [ ] 问题: Hermes cron 是否已有统一 attempt id 与 exactly-one terminal，能否直接复用而不新增 schema？ | reason: adaptation/duplication | priority: high
- [ ] 问题: LoopX 的 validated-spend 模式与现有 `reflection_engine.py`、verification-first fact 的边界如何划分？ | reason: conflict/duplication | priority: medium

### 不应自动落地

- 不自动安装或部署 Cloudflare Computer / LoopX，不运行 `curl | bash`，不启用 privileged FUSE/Docker/Worker/DO。
- 不自动修改 Hermes/OpenClaw 的 config、provider、模型、auth、env、cron 或 secret；当前 OpenClaw runtime 不存在。
- 不把候选直接写入 curated active fact，不因 audit 通过就创建 shared skill；先做 POC、去重、证据评分与治理审查。
- 不复制上游平台特定源码到 shared；只抽象经过本地 fixture 验证的 agent-neutral contract。
- 不把 npm audit 结果解释成所有漏洞均可达，也不把定向 tests 解释成生产安全或完整产品通过。
