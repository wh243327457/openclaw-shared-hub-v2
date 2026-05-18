#!/bin/bash
# Knowledge Base Git Auto-Sync
# 知识库 git 自动同步脚本
# 用法: kb_git_sync.sh [--push]
#   --push  : 同步后推送到 remote

set -e

KB_DIR="/mnt/d/system/selfSystem"
LOG_DIR="/home/vany/openclaw-data/.openclaw/shared/runtime/hermes"
mkdir -p "$LOG_DIR"

TIMESTAMP=$(date -Iseconds)
LOG_FILE="$LOG_DIR/kb_sync.log"

log() {
    echo "[$TIMESTAMP] $1" >> "$LOG_FILE"
}

cd "$KB_DIR"

# 确保 safe.directory 已配置（WSL dubios ownership 修复）
git config --global --add safe.directory "$KB_DIR" 2>/dev/null || true

# 检查是否有未提交更改
if [ -z "$(git status --porcelain 2>/dev/null)" ]; then
    log "kb sync: no changes, skip"
    echo "OK: no changes to commit"
    exit 0
fi

# 有更改，先 add
git add -A

# 获取变更文件列表（简短）
CHANGED=$(git status --short 2>/dev/null | wc -l)
log "kb sync: $CHANGED file(s) changed, committing..."

# Commit，变更内容作为 message
git commit -m "auto-sync: $TIMESTAMP

Changed files:
$(git status --short 2>/dev/null | head -20)" 2>/dev/null

COMMIT_OK=$?

if [ $COMMIT_OK -eq 0 ]; then
    log "kb sync: commit done"
    echo "OK: committed $CHANGED file(s)"
else
    log "kb sync: commit failed"
    echo "WARN: commit failed (may be empty commit)"
    exit 0
fi

# 如果带了 --push，则推送到 remote
if [ "$1" = "--push" ]; then
    log "kb sync: pushing to origin..."
    PUSH_RESULT=$(git push origin main 2>&1)
    if [ $? -eq 0 ]; then
        log "kb sync: push done"
        echo "OK: pushed to origin"
    else
        log "kb sync: push failed: $PUSH_RESULT"
        echo "WARN: push failed: $PUSH_RESULT"
    fi
else
    echo "OK: changes committed locally (use --push to push)"
fi
