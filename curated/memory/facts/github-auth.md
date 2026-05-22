---
fact_id: github-auth-status
claim_id: github-auth-status
claim_type: agent_system
status: active
freshness_class: operational
scope: hermes
lens: identity
subject: github.auth
attribute: cli_auth_status
value_summary: "gh CLI 认证完成，账号 wh243327457，scopes 包含 repo/read:org/gist"
topic: github.auth.cli_status
source_agent: hermes
source_paths:
  - /root/.gitconfig
  - /root/.config/gh/hosts.yml
evidence_refs:
  - /root/.gitconfig
  - /root/.config/gh/hosts.yml
sensitivity: low
created_at: 2026-05-16T02:58:05+08:00
updated_at: 2026-05-16T02:58:05+08:00
last_verified_at: 2026-05-16T02:58:05+08:00
review_due_at: 2026-06-16T02:58:05+08:00
source_refs:
  - /root/.gitconfig
  - /root/.config/gh/hosts.yml
review_status: approved
conflict:
  status: none
  type: null
  conflicting_fact_ids: []
  conflicting_candidate_refs: []
  resolution: null
  resolved_by: null
  resolved_at: null
supersedes: []
superseded_by: null
confidence: high
authority: filesystem
secret_checked: true
---

# GitHub 认证事实

## 当前状态
- 账号: wh243327457
- 方式: HTTPS (gh CLI 认证)
- Scopes: repo, read:org, gist
- 已执行 `gh auth setup-git`

## 稳定约束
- WSL/root 仍无 Git 全局配置与 SSH 密钥
- Windows 用户 /mnt/c/Users/Administrator 下有 Git 配置与 SSH 密钥
- .gitconfig 把 github.com 的 ssh URL 重写到 https
