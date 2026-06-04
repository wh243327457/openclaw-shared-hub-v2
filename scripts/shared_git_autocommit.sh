#!/bin/bash
# Shared Hub 安全自动提交
# 每小时运行一次，自动检测并提交变化
# 由 cron job 020aabffd76f 调用

set -e
cd "$(dirname "$0")/.." || exit 1

# 1. 检测 cron 变化并导出
python3 scripts/bootstrap.py sync 2>&1 | tail -5

# 2. 检查是否有未提交的变化
if [ -z "$(git status --porcelain)" ]; then
    echo "[autocommit] 无变化，跳过"
    exit 0
fi

# 3. 安全检查：不提交 secret
if git diff --cached --diff-filter=A | grep -qiE '(api.key|token|password|secret)'; then
    echo "[autocommit] ⚠️ 检测到可能的 secret，跳过提交"
    git reset HEAD . 2>/dev/null
    exit 1
fi

# 4. 提交
DATE=$(date +%Y-%m-%d_%H:%M)
git add -A
git commit -m "chore: 自动同步 $DATE" --quiet

# 5. 推送（如果远程可达）
git push origin main --quiet 2>/dev/null || echo "[autocommit] push 失败，下次重试"

echo "[autocommit] ✅ 已提交 $DATE"
