# Live shared 目录直接提交检查清单

适用场景：用户明确要求“提交一下本次修改”，且当前目录就是 shared live Git 仓库（例如 `<shared-root>` 本身有 `.git`、remote 和当前分支），不是 runtime staging PR 仓库。

## 推荐顺序

1. 确认仓库与分支
   ```bash
   git status --short
   git rev-parse --show-toplevel
   git branch --show-current
   git remote -v
   git log -1 --oneline
   ```

2. 看差异规模与范围
   ```bash
   git diff --stat
   git status --short
   ```
   重点确认是否包含：
   - 共享 skill / docs / scripts 修改
   - inbox / compat 日志新增
   - 大目录删除（如废弃 seed、demo scaffold）
   - 不应提交的 runtime/cache/secret 文件

3. 提交前最小检查
   ```bash
   git diff --check
   git diff -- . ':(exclude)next/shared-hub-v3/**' | python3 - <<'PY'
   import sys,re
   text=sys.stdin.read()
   patterns=[
       r'(?i)api[_-]?key\s*[:=]',
       r'(?i)secret\s*[:=]',
       r'(?i)token\s*[:=]',
       r'(?i)password\s*[:=]',
       r'sk-[A-Za-z0-9_-]{16,}',
       r'ghp_[A-Za-z0-9_]{20,}',
   ]
   for pat in patterns:
       if re.search(pat,text):
           print('MATCH',pat)
   PY
   ```
   说明：如果某个大目录是整段删除的历史 seed，可以在 secret 扫描中排除，避免旧内容噪声；新增与修改内容仍要扫。

4. 提交
   ```bash
   git add -A
   git commit -m "<中文功能性提交信息>"
   ```

5. 提交后验证
   ```bash
   git status --short --branch
   git log -1 --oneline --decorate
   git rev-list --left-right --count origin/$(git branch --show-current)...HEAD 2>/dev/null || true
   ```
   回复用户时明确：提交号、分支、工作区是否干净、是否已 push。默认不要把“提交”扩展成 push，除非用户明确要求。

## 回复口径

简短先结论：

- 已提交 / 未提交原因
- commit hash + message
- 分支
- 工作区状态
- 是否领先远端、是否已 push

避免把完整 `git status` 原样塞给用户，除非用户要求详细清单。
