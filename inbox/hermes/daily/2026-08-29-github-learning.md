# 2026-08-29 GitHub 热门项目学习报告

> 执行者：Hermes（未调用 OpenClaw）  
> 查询时间：2026-08-29T07:39:50+08:00  
> 发现来源：实际抓取 GitHub Trending daily 页面；Stars、Forks、Language、License、更新时间来自 GitHub repository API。  
> 深读固定提交：`tailscale/tailcat@53845983d15e5c86fd7ea8dbe0f2eb6b47c7e643`；`abhigyanpatwari/GitNexus@b059ab3541ea68c2ce292955fc367a5de04b39ea`。

## 今日结论

当系统移除一个中心控制面、或把自然语言代码理解换成静态图索引时，真正决定可靠性的不是“功能更强”，而是能否把最小身份/发现协议、阶段依赖、证据覆盖、降级状态和最终副作用边界变成**可验证的确定性契约**；Tailcat 与 GitNexus 同时说明，协议简化和预计算会减少协调成本，却不会自动消除授权、生命周期、陈旧索引、依赖供应链或许可风险。

### 今日证据与实测摘要

- GitHub Trending daily 实际解析到 `tt-a1i/archify`、`K-Dense-AI/scientific-agent-skills`、`anthropics/claude-plugins-official`、`bilawalsidhu/gods-eye-view`、`abhigyanpatwari/GitNexus`、`JetBrains/go-modern-guidelines`、`calesthio/OpenMontage`、`abi/screenshot-to-code`、`cursor/plugins`、`tailscale/tailcat` 等候选。
- 两仓元数据均以 07:39+08:00 的 API 复查值为准；不采用 README badge 数字。
- Tailcat 本机没有 Go：`go version` 与 `go test ./...` 真实返回 exit 127；因此本报告只把源码、API、issue 与 GitHub check-runs 当证据，不伪称本机 Go 测试通过。固定提交的 GitHub check-runs 为 `build/test/wasm/deploy` 四项 success。
- GitNexus 本机 Node `v22.14.0`，低于项目要求 `^22.18.0 || >=24.11.0`。锁定依赖安装后，`pipeline-runner` + `pipeline-phase-registry` 定向测试 **30 passed / 0 failed**；完整 build（shared、CLI、Web）成功，但有 EBADENGINE、browser externalization 和大 chunk 警告。混跑 `hybrid-search` 时因 `npm ci --ignore-scripts` 未安装 LadybugDB native binary 而 blocked，不能外推全仓测试。
- GitNexus package production audit 实报 **1 moderate**（`protobufjs` GHSA-j3f2-48v5-ccww，经 optional `@huggingface/transformers → onnxruntime-web`）；Web production audit 实报 **1 high**（`nanoid` GHSA-2v37-7h3g-55p8，经 `postcss`）。两仓 Dependabot alerts API 均因权限 403，不能据此声称无其他漏洞；公开 repository advisories 都返回 0，也不等于依赖安全。

## 项目速览

| 项目 | Stars | Forks | Language | License（GitHub API） | API updated / pushed (UTC) | 今日判断 |
|---|---:|---:|---|---|---|---|
| [abhigyanpatwari/GitNexus](https://github.com/abhigyanpatwari/GitNexus) | 46,153 | 5,101 | TypeScript | **NOASSERTION** | 2026-08-28T23:39:51Z / 2026-08-28T20:22:09Z | **深读：显式 phase DAG、语义图与 evidence-aware 查询** |
| [tailscale/tailcat](https://github.com/tailscale/tailcat) | 2,646 | 69 | Go | BSD-3-Clause | 2026-08-28T23:38:03Z / 2026-08-28T19:41:03Z | **深读：无中心控制面的最小发现握手与 userspace data plane** |
| [abi/screenshot-to-code](https://github.com/abi/screenshot-to-code) | 75,532 | 9,217 | Python | MIT | 2026-08-28T23:22:33Z / 2026-08-14T17:20:50Z | 多模态生成候选；今日不执行 provider/UI 路径 |
| [calesthio/OpenMontage](https://github.com/calesthio/OpenMontage) | 53,278 | 6,645 | Python | AGPL-3.0 | 2026-08-28T23:29:54Z / 2026-08-22T18:22:24Z | AGPL 边界高，只观察机制 |
| [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | 36,543 | 3,474 | Python | MIT | 2026-08-28T23:31:33Z / 2026-08-28T21:41:24Z | skill registry 候选；需逐 skill 审 effect/依赖 |
| [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | 35,010 | 3,935 | Python | Apache-2.0 | 2026-08-28T23:28:29Z / 2026-08-28T18:40:54Z | 插件分发候选；不能外推 Hermes loader 兼容 |
| [tt-a1i/archify](https://github.com/tt-a1i/archify) | 27,248 | 1,726 | JavaScript | MIT | 2026-08-28T23:31:31Z / 2026-08-28T18:45:36Z | 8 月 27 日已深读，今日不重复 |
| [bilawalsidhu/gods-eye-view](https://github.com/bilawalsidhu/gods-eye-view) | 11,017 | 2,233 | JavaScript | NOASSERTION | 2026-08-28T23:30:52Z / 2026-08-28T00:46:30Z | 许可未断言，不迁移源码 |
| [cursor/plugins](https://github.com/cursor/plugins) | 5,943 | 478 | TypeScript | **NOASSERTION（API license=null）** | 2026-08-28T23:31:25Z / 2026-08-28T17:12:06Z | 插件目录候选；许可与安装 effect 待核验 |
| [JetBrains/go-modern-guidelines](https://github.com/JetBrains/go-modern-guidelines) | 2,581 | 78 | Go | Apache-2.0 | 2026-08-28T23:18:51Z / 2026-08-19T17:39:58Z | 文档型候选，不满足今日源码深读主线 |

> 注：表中速览值来自实际 API 批量查询；尾随数值可能在用户阅读时继续变化。深读部分再给出固定提交与实时快照，避免把动态 Stars 与源码 revision 混为同一证据。

## 深读项目

### 1. tailscale/tailcat

- **一句话判断**：值得学的不是“另一个 VPN”，而是它如何把成熟 data plane 与中心 control plane 解耦，用一个自包含/可扩展 token 加极小 `Meow/Meowed` 握手恢复点对点身份和连通性。
- **解决的问题**：替代“必须先注册 Tailscale account、由控制平面分发 peer/network map”的旧做法；服务端把 WireGuard 公钥和 DERP region 放进带外共享 token，客户端借 DERP 完成最初发现，之后由 magicsock 尝试直连。
- **URL / API 快照**：https://github.com/tailscale/tailcat ；**Stars 2,646 / Forks 69 / Language Go / License BSD-3-Clause**；`updated_at=2026-08-28T23:38:03Z`，`pushed_at=2026-08-28T19:41:03Z`，open issues API 字段 9（含 PR）。
- **固定提交**：[`53845983d15e5c86fd7ea8dbe0f2eb6b47c7e643`](https://github.com/tailscale/tailcat/commit/53845983d15e5c86fd7ea8dbe0f2eb6b47c7e643)，提交 API 显示 unsigned；仓库当前没有 GitHub Release 条目，不能把 main 当 stable release。
- **来源交叉核验**：README 的 connection flow / stability；关键 Go 源码；open issues [#17](https://github.com/tailscale/tailcat/issues/17)、[#18](https://github.com/tailscale/tailcat/issues/18)；固定提交 check-runs。

#### 架构/实现与数据流

1. `ConnBlob` 是 `tc` 前缀 + URL-safe Base64(CBOR)，最少携带 server WireGuard public key 与 DERP region ID；长 token 可直接嵌 DERP node 元数据，省掉客户端 map fetch。
2. Server 初始化 userspace WireGuard engine、magicsock、gVisor netstack 和 packet filter；它不改系统 route/DNS，也不要求 root。
3. Client 经同一 DERP region 发送 raw DERP `MeowPing(node public, disco public)`；Server 先执行 `AllowedClients` gate，再把 peer 写入 network map，最后回 `Meowed`。
4. 收到 ACK 后才开始拨号；DERP 是 bootstrap/fallback，双方通过 disco endpoint advertisement 与 STUN 尝试 direct UDP。
5. TCP 最终在 userspace netstack 中终止，`OnTCP`/`OnTCPForward` 决定 localhost 转发、exit-node 或 SSH；packet filter 是前置 defense-in-depth，callback 是连接级二次 gate。

#### repo tree 摘要

```text
tailcat/                              # 固定提交共 39 tracked files
├── tailcat.go                        # Server/Client、engine/netstack、DERP map、peer map
├── disco.go                          # Meow/Meowed 最小发现协议
├── wire.go                           # 独立、紧凑、受测试约束的 CBOR wire types
├── pickregion.go / pickregion_js.go  # native netcheck 与 WebAssembly region 策略
├── tailcat_ssh.go                    # no-auth SSH、PTY/pipes、受限 env
├── cmd/tailcat/                      # CLI：serve/ping/socks/ssh/parse/resolve/key
├── web/ / webdemo/                   # Wasm browser demo 与 tests
├── internal/wasmbuild/               # Wasm 构建辅助
├── go.mod / go.sum                   # Go 1.26.5、完整锁定依赖图
└── .github/workflows/                # test 与 web demo deploy
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `tailcat.go` | data-plane 生命周期 | `Server.Start` 组装 engine/netstack/filter；`Client.initLocked` 惰性构建；`onMeow` 做 allowlist 后写 peer map |
| `disco.go` | 最小 bootstrap 协议 | 固定 magic + type + 两个 32-byte public key；长度/type 不合法即拒绝 |
| `wire.go` | token wire contract | 自建单字节 CBOR 字段，避免上游 `tailcfg` 结构变化直接污染 wire format；过滤 STUN-only node |
| `pickregion.go` | relay 选择 | `netcheck` 获取 RegionLatency，选最小延迟；无结果由 `ConnInfo.Expand` 随机 fallback |
| `cmd/tailcat/tailcat.go` | CLI adapter | DNS TXT token、DERP map disk cache、bounded ping、half-close 后等对端 EOF，避免进程提前退出丢包 |
| `tailcat_ssh.go` | 高权 SSH adapter | WireGuard identity 替代 SSH client auth；只接受 `TERM/LANG/LC_*`；但 raw command 交给 login shell `-c` |

#### ⭐ 源码精读

**1) `func (s *Server) Start() error`：组装确定性外壳后才启动 data plane**

```go
func (s *Server) Start() error {
    if s.lb != nil {
        return errors.New("tailcat: Server.Start called twice")
    }
    priv := s.Key
    if priv.IsZero() {
        priv = key.NewNode()
    }
    // Resolve/pick DERP region, construct event bus/netmon/engine/netstack...
    s.lb = lb
    sys.Engine.Get().SetFilter(s.buildFilter())
    return lb.Start()
}
```

逻辑：零值配置补 ephemeral key 和 region；engine/netstack 完成后安装由 `ServedTCPPorts`/`OnTCPForward` 推导的 filter，再启动 backend。风险是 issue #18 已指出中途失败时已分配的资源可能泄漏；当前源码在多个 error return 前没有统一 deferred rollback，`s.lb` 又接近末尾才赋值。

**2) `func (b *locoBackend) onMeow(...) bool`：身份 gate 先于 ACK 与 peer 生效**

```go
func (b *locoBackend) onMeow(src key.NodePublic, discoPub key.DiscoPublic) bool {
    b.mu.Lock()
    defer b.mu.Unlock()
    if b.allowedClients != nil && !b.allowedClients[src] {
        return false
    }
    if _, ok := b.clients[src]; ok {
        return true
    }
    mak.Set(&b.clients, src, &tailcfg.Node{Key: src, DiscoKey: discoPub, ...})
    mc.SetNetworkMap(nm.SelfNode, nm.Peers)
    b.sys.Netstack.Get().UpdateNetstackIPs(nm)
    go b.advertiseEndpoints()
    return true
}
```

逻辑：在 mutex 下先做 allowlist，幂等处理重复 client，再发布新的 network map；caller 只在返回 true 后发 `Meowed`。这让 ACK 兼任“服务端已经配置 peer”的阶段屏障，而不是单纯“收到包”。边界：token 默认仍是 bearer-like reachability secret；不配置 `AllowedClients` 时持 token 者都可进入握手。

**3) `func EncodeMeowPing` / `func ParseMeowPing`：极窄 wire protocol**

```go
func EncodeMeowPing(nodeKey key.NodePublic, discoKey key.DiscoPublic) []byte {
    b := make([]byte, 0, 4+1+key.NodePublicRawLen+key.DiscoPublicRawLen)
    b = append(b, meowMagic[:]...)
    b = append(b, meowTypePing)
    b = nodeKey.AppendTo(b)
    return discoKey.AppendTo(b)
}

func ParseMeowPing(pkt []byte) (nodeKey key.NodePublic, discoKey key.DiscoPublic, ok bool) {
    if len(pkt) < 4+1+key.NodePublicRawLen+key.DiscoPublicRawLen || pkt[4] != meowTypePing {
        return nodeKey, discoKey, false
    }
    // Decode exact raw key slices.
    return nodeKey, discoKey, true
}
```

逻辑：发现协议不传账户、ACL prose 或任意 JSON，只传配置 WireGuard/disco 所需的最小公钥。注意 parser 只要求“至少”固定长度，不检查 trailing bytes；当前扩展/兼容语义待核验，不能假定 extra bytes 一定被拒绝。

**4) `func (ci *ConnInfo) Expand(...) error`：short token 到可用 relay config**

```go
func (ci *ConnInfo) Expand(ctx context.Context, opts ...any) error {
    if len(ci.Region) > 0 || ci.RegionID == 0 { return nil }
    ctx, cancel := context.WithTimeout(ctx, 10*time.Second)
    defer cancel()
    dm, err := fetchDERPMap(ctx, fetchURL, mode, cache)
    if ci.RegionID == -1 {
        regionID, err := PickBestRegion(ctx, dm)
        // Prefer measured best; otherwise bounded random map choice.
    }
    ci.Region = append(ci.Region, dm.Regions[ci.RegionID])
    return err
}
```

逻辑：embedded region 直接可用；region ID 需 fetch/cache；`-1` 表示启动时自动选区。`fetchDERPMap` 有 10 秒 deadline、8 MiB response cap、ETag revalidation、stale-on-error fallback。边界：README 与 TODO 都承认 DERP map 漂移和 public relay 无 SLA。

#### 依赖分析与供应链风险

`go.mod` 要求 **Go 1.26.5**。直接核心依赖包括：

- `tailscale.com v1.101.0-pre...`：magicsock/WireGuard/DERP/engine 主体，且是 pre pseudo-version；上游 API 漂移风险高。
- `gvisor.dev/gvisor ...`：userspace netstack，体积与 native/network behavior 复杂。
- `github.com/fxamacker/cbor/v2 v2.9.0`：token 序列化。
- SSH/PTY 路径：`gliderssh`、`creack/pty`、`x/crypto`、`x/sys`、u-root。
- indirect graph 很大，包含 platform/network/cloud 依赖；“repo 只有 39 files”不等于供应链小。

真实审计边界：本机无 Go，未运行 `govulncheck` 或编译；Dependabot endpoint 403；公开 advisories 0 不能证明无漏洞。固定提交 GitHub test/check success 是上游 CI 证据，不是本机复现。

#### 可复用经验

- 当去掉中心控制面但仍需建立双方可信连接时，应优先设计只包含 immutable identity 与 bootstrap location 的窄 token，再用最小 ACK 表示“peer 已真正配置”，因为 prose/session 状态无法证明 data plane ready；边界是 token 保密性、撤销和 relay 可用性仍需单独解决。
- 当网络服务同时有 packet-level 与 connection-level policy 时，应优先前置窄 filter、后置 callback gate，而不是让单个 handler 承担全部授权；边界是两层规则必须共源或做 drift fixture。
- 当初始化连续分配多个资源时，应优先使用 rollback stack / staged owner / exactly-one terminal receipt，因为对象字段尚未赋值时 `Close()` 看不到半成品；边界是 rollback 自身也必须可重复且保留首因。

#### 可尝试实验（30 分钟内）

在 `runtime/hermes/github-learning-poc/bootstrap-ready-contract/` 做**纯离线** fixture：输入 token identity、allowlist、阶段事件 `received → identity_allowed → peer_configured → acked`，注入每一阶段失败，断言只有 `peer_configured` 后可 ACK、所有失败路径释放资源且返回 typed terminal。禁止启动 Tailcat、DERP、SSH 或真实端口。

#### 风险边界

- **License**：仓库 API 与 `LICENSE` 均为 BSD-3-Clause；但 Tailscale/gVisor/SSH 等依赖仍需逐项 license review。
- **维护活跃度**：固定提交为 8 月 28 日，check-runs success；但仓库无正式 Release/API stability promise，README 明说 Go API/CLI/wire format 都可变，public DERP 无 SLA。
- **安全风险**：`no-auth-ssh` 以 WireGuard identity 代替 SSH auth；默认无 `AllowedClients` 时任何 token 持有者可连接。`--serve=exit-node` 与 shell `-c` 是高权 effect，绝不能由无人值守 Agent 自动启用。
- **已知缺陷**：issue #17 报 PTY `io.Copy`/`Wait` 次序可挂死；#18 报 partial startup resource leak。两 issue 提供上游复现，但本机无 Go，均标**本机待核验**。
- **不适用**：需要集中设备管理、实时撤销、审计、稳定 SLA、多租户 policy 的环境；Tailcat 明确不是完整 control plane 替代品。

#### ⭐ Skill 升格判断

**需二次验证**。可抽象的是 `bootstrap-ready contract + staged rollback`，不是复制 Tailcat 源码、wire format 或 SSH 功能。先与已有 `completion/receipt`、`effect-scope`、`scoped-authority` 候选去重，并完成 failure-injection fixture；今日不新建 shared skill、不写 curated active fact。

#### Hermes/shared hub 落地路径

- POC：`runtime/hermes/github-learning-poc/bootstrap-ready-contract/{schema.json,checker.py,fixtures/}`。
- 若 fixture 证明有增量价值：更新现有 `capabilities/skills/autonomous-learning/self-reflection-engine/` 或 verification 类 shared skill 的 reference，加入 `resource_owner/stage/ready_evidence/terminal/rollback` 字段；不要创建网络专用大 skill。
- Hermes adapter 只读取离线 fixture；任何真实 network/SSH/port effect 必须在 `~/.hermes` 本地能力层显式授权，不能从 shared 自动执行。
- shared hub 只保存 agent-neutral contract；运行日志进 `runtime/hermes/`，候选记录留 inbox，不进入 curated。

### 2. abhigyanpatwari/GitNexus

- **一句话判断**：值得学的是“把 Agent 需要的代码关系在索引期结构化、在查询期携带覆盖边界”，而不是把知识图谱工具直接安装进 Hermes。
- **解决的问题**：替代 Agent 每轮以 grep/文件阅读临时重建 call/import/process context 的旧做法；GitNexus 先将多语言 AST、scope、call、route、DI、process、可选 PDG 归一为图，再由 CLI/MCP 返回预结构化 blast radius 与 provenance。
- **URL / API 快照**：https://github.com/abhigyanpatwari/GitNexus ；**Stars 46,153 / Forks 5,101 / Language TypeScript / GitHub API License NOASSERTION**；`updated_at=2026-08-28T23:39:51Z`，`pushed_at=2026-08-28T20:22:09Z`，open issues API 字段 344（含 PR）。
- **固定提交**：[`b059ab3541ea68c2ce292955fc367a5de04b39ea`](https://github.com/abhigyanpatwari/GitNexus/commit/b059ab3541ea68c2ce292955fc367a5de04b39ea)，GitHub commit API 为 verified signature。
- **Release**：[`v1.6.10`](https://github.com/abhigyanpatwari/GitNexus/releases/tag/v1.6.10)，2026-08-27T22:49:55Z；main 已有 `v1.6.11-rc.1`，不能把 fixed HEAD 与 stable release 混称。
- **License 真相**：API `NOASSERTION`；README badge、root `LICENSE`、`gitnexus/package.json` 均指 **PolyForm-Noncommercial-1.0.0**。这是非商业限制，不是 OSI 开源许可；任何商业/组织落地必须法务核验。
- **来源交叉核验**：README、`ARCHITECTURE.md`、v1.6.10 release、open issues #3073–#3080、关键源码、锁定依赖与本机测试/build/audit。

#### 架构/实现与数据流

1. CLI `analyze` 调 `runFullAnalysis`，再进入 `runPipelineFromRepo`；默认 phase registry 以显式 deps 组成 DAG。
2. `scan → structure → parse → routes/tools/orm → crossFile → scopeResolution → ... → communities/processes` 共同写一个 graph；runner 只把**声明过的依赖结果**传给 phase，阻止隐藏跨阶段读取。
3. parse worker 将多语言 tree-sitter 结果归一为 `ParsedFile`/semantic captures；scope resolver 通过 registry 与语言 hook 输出统一 CALLS/IMPORTS/ACCESSES 等边。
4. graph 持久化到 `.gitnexus/lbug`（LadybugDB）；metadata、WAL、shadow、lock 分层，registry 供 MCP 发现。
5. MCP/CLI/HTTP 共用 local backend；query 使用 BM25 + optional semantic，再以 RRF 合并 rank；impact/context 还返回 ambiguity、truncation、epistemic lower-bound 等信息。
6. 可选 `--pdg` 增加 CFG/reaching-def/taint/CDG；每层有 cap 与 degraded status，避免 partial graph 无声冒充 complete。

#### repo tree 摘要

```text
GitNexus/                                  # 固定提交 5,029 tracked files
├── gitnexus/                              # npm CLI/MCP/HTTP/ingestion/LadybugDB
│   ├── src/core/ingestion/                # phase DAG、language providers、scope/PDG
│   ├── src/core/search/                   # BM25、RRF、CJK segmentation、timing
│   ├── src/core/lbug/                     # schema、CSV、WAL/connection/query adapter
│   ├── src/mcp/                           # tools/resources/policy/local backend
│   ├── src/storage/                       # registry、atomic fs、index lock/hash/cache
│   ├── skills/ / hooks/                   # 发布给各 Agent 的 skill/hook surfaces
│   └── test/                              # unit/integration/fixtures
├── gitnexus-web/                          # Vite + React graph/chat thin client
├── gitnexus-shared/                       # CLI/Web 共享 schema/types
├── gitnexus-*-plugin/integration/          # Claude/Cursor 等 adapter
├── eval/                                  # benchmark/evaluation harness
├── pr-swarm-review/                       # CLI-neutral review personas/spec
├── ARCHITECTURE.md / SECURITY.md           # 机制与部署边界
└── package-lock.json + 子包 lockfiles      # 多 workspace 锁定依赖
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `gitnexus/src/core/ingestion/pipeline.ts` | phase registry 与总编排 | 显式注册、opt-in predicate、streaming 配置缺失时 fail loudly、结果 presence check |
| `.../pipeline-phases/runner.ts` | DAG validator/executor | duplicate/missing/cycle 检查；Kahn sort；只暴露 declared deps；error terminal 保留 cause |
| `.../scope-resolution/contract/scope-resolver.ts` | 多语言插件契约 | shared ingestion 不按语言名分支；语言差异经 provider hooks 注入 |
| `.../search/hybrid-search.ts` | BM25/semantic fusion | RRF_K=60；以 filePath 合并；FTS exception 退 semantic-only |
| `gitnexus/src/mcp/local/local-backend.ts` | tool semantics | 参数 alias 冲突检测、candidate window/truncation、valid relation、epistemic boundary |
| `gitnexus/src/storage/index-lock.ts` | index writer ownership | 单写者锁与并发分析边界 |
| `ARCHITECTURE.md` | 架构契约 | 19/21 phase DAG、semantic model write/read freeze、PDG coverage 和 storage layout |

#### ⭐ 源码精读

**1) `export function buildPhaseList(options?)`：把 phase enablement 也纳入静态契约**

```ts
export function buildPhaseList(options?: PipelineOptions): PipelinePhase[] {
  return new PhaseRegistry<PipelineOptions>()
    .register(scanPhase)
    .register(structurePhase)
    .register(parsePhase)
    .register(crossFilePhase)
    .register(scopeResolutionPhase)
    .register(taintSummariesPhase, { enabledWhen: o => o.pdg === true })
    .register(communitiesPhase, { enabledWhen: o => !o.skipGraphPhases })
    .register(processesPhase, { enabledWhen: o => !o.skipGraphPhases })
    .build(options ?? {});
}
```

逻辑：phase 集合不是任意 plugin 动态加载，而是 typed registry；PDG 与高成本 graph phase 由 predicate 控制。结果读取端用 `results.has(...)` 而非只看 option，避免“phase 已过滤却被强取”造成假成功或 crash。

**2) `export async function runPipeline(...)`：DAG、可见性和 terminal error 一起约束**

```ts
export async function runPipeline(phases, ctx) {
  const sorted = topologicalSort(phases); // duplicate/missing/cycle reject
  const results = new Map();
  for (const phase of sorted) {
    const declaredDeps = new Map();
    for (const depName of phase.deps) {
      const dep = results.get(depName);
      if (dep) declaredDeps.set(depName, dep);
    }
    try {
      const output = await phase.execute(ctx, declaredDeps);
      results.set(phase.name, { phaseName: phase.name, output, durationMs: ... });
    } catch (err) {
      ctx.onProgress({ phase: 'error', percent: 100, ... });
      throw new Error(`Phase '${phase.name}' failed: ...`, { cause: err });
    }
  }
  return results;
}
```

逻辑：Kahn sort 不只给顺序，也拒绝 missing/duplicate/cycle 并给 concrete cycle path；phase 不能偷读未声明上游；progress handler 失败不能覆盖原始 cause。这一模式适合 Hermes orchestrator，但要补 immutable input/artifact/coverage receipt 才能证明业务完成。

**3) `export const mergeWithRRF(...)`：不同 score 空间先转 rank 再融合**

```ts
export const mergeWithRRF = (bm25Results, semanticResults, limit = 10) => {
  const merged = new Map<string, HybridSearchResult>();
  for (let i = 0; i < (bm25Results ?? []).length; i++) {
    const r = bm25Results[i];
    merged.set(r.filePath, { filePath: r.filePath, score: 1 / (60 + i + 1), sources: ['bm25'], ... });
  }
  for (let i = 0; i < (semanticResults ?? []).length; i++) {
    const r = semanticResults[i];
    const existing = merged.get(r.filePath);
    if (existing) existing.score += 1 / (60 + i + 1);
    else merged.set(r.filePath, { filePath: r.filePath, score: 1 / (60 + i + 1), sources: ['semantic'], ... });
  }
  return [...merged.values()].sort((a, b) => b.score - a.score).slice(0, limit);
};
```

逻辑：BM25 与 vector distance 不做伪归一，统一转名次贡献。边界：identity 只用 `filePath`，同文件多个 semantic node 会折叠；tie ordering、source coverage 与 FTS unavailable 状态应随结果投影，不能只返回排名。

**4) `function normalizeToolParams(...)`：alias 是输入兼容，不是模糊猜测**

```ts
function normalizeToolParams(method: string, params: unknown) {
  const input = params && typeof params === 'object' ? params : {};
  for (const { canonical, aliases } of TOOL_STRING_ALIASES[method] ?? []) {
    const supplied = [canonical, ...aliases]
      .filter(k => Object.prototype.hasOwnProperty.call(input, k));
    // Non-string/blank rejects; distinct supplied values reject.
    if (new Set(supplied.map(({ value }) => value.trim())).size > 1) {
      return { error: `Conflicting MCP parameters for ${method}.${canonical}...` };
    }
  }
  return { params: normalized };
}
```

逻辑：兼容旧参数名，但多个入口若值不一致就 fail closed；不会“canonical 空值覆盖 legacy 真值”。这比模型侧自行猜 alias 更适合 shared adapter。边界：schema validation 与 effect authorization 仍需宿主层完成。

#### 依赖分析与供应链风险

`gitnexus/package.json` 核心生产依赖：

- `@ladybugdb/core`：native property graph DB，install script / prebuilt ABI / lock/WAL 是重要供应链与平台边界。
- `tree-sitter` + 多语言 grammars：native/parser surface；另有 vendored Kotlin/Dart/Proto/Swift grammar。
- `@modelcontextprotocol/sdk`：MCP surface；Express/CORS/rate-limit/busboy 是 HTTP/upload surface。
- `@huggingface/transformers` + `onnxruntime-node` 为 optional embedding stack，会引入 native/download 与较大依赖图。
- `graphology`/`mnemonist`/`glob`/`js-yaml`/`pino` 等支撑 graph、scan、config、logging。

本机真实结果：

- `npm ci --ignore-scripts` 安装 package 348 项，提示宿主 Node 22.14 不满足 engine；skip scripts 导致 LadybugDB `lbugjs.node` 缺失，这正证明安装成功不等于 runtime prerequisite 完整。
- 在补建 `gitnexus-shared` 后，pipeline runner/registry 定向 tests：**30 passed / 0 failed**。
- 完整 `npm run build`：shared、CLI TypeScript、Web Vite build 成功；但 Web install 报 7 个全依赖漏洞、生产审计单独为 1 high nanoid，且有大 chunk/browser externalization warnings。
- package production audit：1 moderate `protobufjs`，来源为 optional embedding 路径；Web production audit：1 high `nanoid`，`npm explain` 显示经 `postcss`。两项都有 fixAvailable，但本任务不自动改 lockfile。
- Dependabot alerts API 403；因此不能声称锁文件只存在上述两项，也不能用 repository advisories=0 抵消本机 audit。

#### 可复用经验

- 当多阶段分析会被 Agent 当作事实源时，应优先让 phase 名、依赖、enablement、typed output 与 exactly-one error terminal 成为 host-owned DAG，因为 prompt 顺序和隐式共享 map 会产生隐藏耦合；边界是 DAG success 仍需 artifact/coverage readback。
- 当融合 BM25、向量、热度或其他不可比 score 时，应优先按 source 内 rank 做 RRF 并保留 source/provenance，而不是直接加原始分数；边界是同源重复、identity 粒度、missing source 与 tie 必须显式处理。
- 当索引或 checker 只能覆盖部分语言/文件/关系时，应优先输出 `exact/lower-bound/degraded/blocked` 与 machine-readable causes，因为 0 result 可能是未解析、stale、路径 miss 或真正无依赖；边界是 coverage 声明本身要由固定 revision 和 fixture 验证。
- 当 CLI/MCP 需要兼容旧参数或旧入口时，应优先 canonicalize 后检查冲突，不能静默选择任一 alias；边界是兼容解析不能代替权限与副作用 gate。

#### 可尝试实验（30 分钟内）

在 `runtime/hermes/github-learning-poc/evidence-phase-runner/` 实现 Python 纯 fixture：3 个 phase，显式 deps，输入 hash，output artifact hash，coverage=`complete|partial|blocked`，错误时 exactly-one terminal；加入 undeclared dep、disabled phase、checker missing、progress handler throws 四组测试。不要安装或运行 GitNexus MCP，不修改 Hermes config。

#### 风险边界

- **License**：GitHub API 是 NOASSERTION；仓库文本为 PolyForm Noncommercial 1.0.0。只抽象机制，不复制源码/发布物到 shared skill；商业用途需单独许可。
- **维护活跃度**：8 月 27 日 stable release，8 月 28 日仍高频 commit/PR；活跃不等于稳定。open issue #3080 报 `analyze` 可覆盖 committed skill，#3077 报 stale false positive，#3074 报 path target miss 却返回 0/UNKNOWN，#3075 报不同 target type 风险分不可比。
- **安全风险**：native DB/grammar/install scripts、HTTP/MCP/server/upload、optional embedding/model download 都扩大 authority surface。`SECURITY.md` 明说 Render edge token 是唯一 access control，直接公开 `serve` 的 MCP route 有既存 gap；任何 token holder 可读全部 indexed source。
- **测试局限**：宿主 Node 不受支持；hybrid-search 混跑被缺失 native binary 阻塞；只实测 30 个定向 tests 和 build，未运行 full suite、真实 analyze、LadybugDB、MCP、provider、embedding 或 hosted deploy。
- **语义局限**：静态图存在 language/parser/resolution lower-bound；RRF ranking 不是 authority；issue #3076 还显示有工具并不保证 Agent 在 read-only task 使用它（报告称 0/9）。

#### ⭐ Skill 升格判断

**需二次验证**。`explicit phase DAG + coverage terminal` 与 `source-aware RRF` 有迁移价值，但 shared hub 已有 verification-first、subagent 四状态、self-reflection 和 GitHub learning 能力，直接新建 skill 会重复。先做窄 fixture，再决定更新 orchestrator contract 或现有 skill；GitNexus 源码受非商业许可限制，不复制。

#### Hermes/shared hub 落地路径

- POC：`runtime/hermes/github-learning-poc/evidence-phase-runner/{runner.py,schema.json,fixtures/,test_runner.py}`。
- Hermes 现有对接候选：`scripts/github_learning_orchestrator.py` 的 prepare/research/audit 三阶段，增加 host-owned `deps/input_hash/artifact_hash/coverage/terminal/cause` status，而非从 Markdown 关键词推断完成。
- shared skill 候选：若 fixtures 稳定，通过更新 `capabilities/skills/research/github-hot-project-learning/SKILL.md` 的审计契约实现；manifest 只在正式升格时更新。本日不直接改 active skill。
- 多 Agent projection：canonical receipt 留 `runtime/<agent>/`，raw report 留 `inbox/<agent>/daily/`；只有经治理评分、去重、许可审查的 agent-neutral pattern 才可候选进入 `curated/memory/facts/`。
- 不安装 GitNexus、不运行 `gitnexus setup/analyze`，避免自动写 `.claude/skills`/AGENTS 或 MCP config，尤其 issue #3080 未解决前。

## 经验沉淀

1. 当系统去掉中心协调层时，应优先保留最小 immutable identity、bootstrap location 与“真正 ready 后才 ACK”的阶段屏障，因为省掉控制面不等于省掉身份、授权和 readiness；边界是撤销、密钥泄漏与服务发现漂移仍需独立设计。
2. 当流程有多个阶段或可选阶段时，应优先用 host-owned typed DAG、declared dependencies、coverage 和 exactly-one terminal，而不是让 phase 从全局状态偷读；边界是 phase success 还必须绑定 input/artifact hash 与 readback。
3. 当多种检索/评分源不可比时，应优先用 per-source rank fusion 并保留 provenance/attempted/degraded，而不是把 BM25、distance、Stars 或模型信心直接相加；边界是 identity 粒度和同源重复必须另行治理。
4. 当 checker、parser、native binary 或工具链没有真正运行时，应优先返回 blocked/unsupported 并保存真实错误，因为安装完成、CI 绿色、空 findings 都不能证明本机覆盖完整；边界是上游 CI 只能作为外部证据。
5. 当 CLI/MCP 同时支持新旧参数时，应优先 canonicalize、blank/type validation 与 conflict rejection，因为静默选 alias 会掩盖调用方 drift；边界是参数规范化不提供 effect authorization。
6. 当第三方项目 API license 为 NOASSERTION 或实际许可是 noncommercial 时，应优先只抽象机制并停止源码/发布物迁移，因为 GitHub 元数据、README badge 与依赖许可都不能替代合规审查。
7. 当初始化需要连续创建 engine、monitor、netstack、lock 或输出文件时，应优先 staged ownership + rollback stack + failure injection，因为最终对象字段未赋值时普通 Close 无法回收半成品；边界是 rollback 必须幂等且不能覆盖原始错误。

### 今日总 Skill 升格判断

- `bootstrap-ready contract`：**需二次验证**；与 completion/effect-scope 去重后再决定。
- `evidence phase runner`：**需二次验证**；优先更新现有 GitHub-learning/self-reflection 契约，不新建大 skill。
- `source-aware RRF`：**暂不沉淀为 skill**；先证明 shared memory/research candidate ranking 有真实收益并解决 provenance/duplicate fixtures。
- 今日不修改 `capabilities/skills/`、manifest、config、model/provider、cron、secret，也不写 curated active fact。

## 明日继续

1. 建立 `runtime/hermes/github-learning-poc/evidence-phase-runner/` 最小离线 fixture，先覆盖 undeclared dep、disabled prerequisite、partial coverage、duplicate terminal、progress callback throws。
2. 把 Tailcat issue #17/#18 抽象成资源生命周期 counterexample；若后续环境有受支持 Go，再固定 commit 运行聚焦 tests，未复现前保持“待核验”。
3. 复核 GitNexus issue #3080/#3074 的修复状态与 released tag；在 issue 未关闭前禁止让任何 Agent 在真实项目运行会写 skill/context 的 `analyze`。
4. 对 GitNexus audit 做可达性复核：optional embedding 的 protobuf parser 是否接收不可信 `.proto`、Web 是否实际调用 custom nanoid size=0；在此之前保留 advisory，不夸大成已可利用漏洞。

## 候选反哺

### Candidate Facts

- [ ] topic: control-plane-free bootstrap 仍需 `identity → authorized → peer configured → acked` 明确阶段 | evidence: `tailcat.go:onMeow`、`disco.go`、README connection flow、fixed commit 5384598 | 建议: create candidate / 与 completion-effect 事实去重 | 安全级别: medium
- [ ] topic: phase DAG 必须同时携带 dependency visibility、coverage 与 terminal evidence | evidence: GitNexus `pipeline.ts`、`runner.ts`、本机 30 passed | 建议: update autonomous-learning-system candidate | 安全级别: low
- [ ] topic: API NOASSERTION 与仓库 PolyForm Noncommercial 不可外推为开源可商用 | evidence: GitHub repo API、root LICENSE、package.json | 建议: create license-governance candidate | 安全级别: medium

### Candidate Skills / Workflow

- [ ] 名称: evidence-phase-runner-v0 | 可复用场景: GitHub learning / reflection / future-agent staged workflows | 是否建议 shared: yes-after-fixtures | 原因: 横切能力，但需与 verification-first、subagent 四状态去重
- [ ] 名称: bootstrap-ready-contract | 可复用场景: agent handoff、connector readiness、worker registration | 是否建议 shared: no-today | 原因: 当前只有 Tailcat 单项目证据，先做 failure-injection POC
- [ ] 名称: source-aware-rank-fusion | 可复用场景: 多来源研究候选融合 | 是否建议 shared: no | 原因: 缺真实 corpus、duplicate/source independence 与 privacy fixtures

### Candidate Open Questions

- [ ] 问题: `MeowPing` parser 允许 trailing bytes 是前向兼容设计还是缺少 exact-length validation？ | reason: gap | priority: medium
- [ ] 问题: GitNexus query 在 FTS unavailable 时是否向所有 MCP consumers 明确暴露 degraded source coverage？ | reason: adaptation | priority: high
- [ ] 问题: GitNexus #3080 的 skill overwrite 是否会在下一个 stable release 修复，且能否提供 dry-run/ownership receipt？ | reason: stale | priority: high
- [ ] 问题: GitNexus production audit 的 protobufjs/nanoid advisory 在真实调用路径是否可达？ | reason: gap | priority: medium

### 不应自动落地

- 不运行或安装 Tailcat，不开放端口、不启动 DERP、不启用 no-auth SSH/exit-node。
- 不运行 `gitnexus setup/analyze` 写真实 repo、Hermes MCP config、AGENTS 或 skills。
- 不自动修改配置、模型、provider、cron、secret；不自动修漏洞或改第三方 lockfile。
- 不复制 GitNexus 的 PolyForm Noncommercial 源码到 shared，不把 Tailcat dependency license 视为已审完。
- 不把今日候选直接写入 curated active fact；只把完整原始证据留在 Hermes inbox/runtime，等待二轮治理。
