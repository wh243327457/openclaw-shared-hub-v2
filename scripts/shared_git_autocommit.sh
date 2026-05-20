#!/usr/bin/env bash
# Shared hub safe Git auto-commit watchdog.
# @author 云舒
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SHARED_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$SHARED_ROOT"

LOG_DIR="runtime/hermes"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/shared-git-autocommit.log"
TIMESTAMP="$(TZ=Asia/Shanghai date -Iseconds)"
DRY_RUN="${DRY_RUN:-0}"
AUTO_PUSH="${SHARED_GIT_AUTOPUSH:-0}"
BRANCH="$(git branch --show-current 2>/dev/null || true)"

log() {
    printf '[%s] %s\n' "$TIMESTAMP" "$*" >> "$LOG_FILE"
}

fail() {
    log "FAILED: $*"
    printf '共享中台自动提交失败：%s\n' "$*"
    exit 1
}

if [ -z "$BRANCH" ]; then
    fail "当前目录不是有效 Git 分支：$SHARED_ROOT"
fi

if [ -d .git/rebase-merge ] || [ -d .git/rebase-apply ] || [ -f .git/MERGE_HEAD ] || [ -f .git/CHERRY_PICK_HEAD ]; then
    fail "检测到 merge/rebase/cherry-pick 未完成，跳过自动提交"
fi

if [ -n "$(git status --porcelain)" ]; then
    :
else
    log "no changes; branch=$BRANCH"
    exit 0
fi

python3 - <<'PY'
import pathlib
import re
import subprocess
import sys

patterns = [
    r'(?i)api[_-]?key\s*[:=]',
    r'(?i)secret\s*[:=]',
    r'(?i)token\s*[:=]',
    r'(?i)password\s*[:=]',
    r'sk-[A-Za-z0-9_-]{16,}',
    r'ghp_[A-Za-z0-9_]{20,}',
]
compiled = [re.compile(p) for p in patterns]

# Scan tracked modifications in diff text.
diff = subprocess.check_output(
    ['git', 'diff', '--', '.', ':(exclude)runtime/**'],
    text=True,
    errors='ignore',
)
findings = []
for pat, regex in zip(patterns, compiled):
    if regex.search(diff):
        findings.append(('diff', pat))

# Scan untracked text files that Git would include, excluding ignored files.
raw = subprocess.check_output(
    ['git', 'ls-files', '--others', '--exclude-standard', '-z'],
)
for raw_path in raw.split(b'\0'):
    if not raw_path:
        continue
    path = pathlib.Path(raw_path.decode('utf-8', 'ignore'))
    if str(path).startswith('runtime/'):
        continue
    try:
        data = path.read_bytes()
    except OSError:
        continue
    if b'\0' in data[:4096]:
        continue
    text = data.decode('utf-8', 'ignore')
    for pat, regex in zip(patterns, compiled):
        if regex.search(text):
            findings.append((str(path), pat))

if findings:
    print('secret_scan_needs_review')
    for location, pat in findings:
        print(f'MATCH {location}: {pat}')
    sys.exit(2)
print('secret_scan_ok')
PY

if [ "$DRY_RUN" = "1" ]; then
    log "dry-run ok; branch=$BRANCH"
    printf '共享中台自动提交 dry-run 通过；当前有待提交变更，未实际 commit。\n'
    git status --short
    exit 0
fi

git add -A

if ! git diff --cached --check >/tmp/shared-git-autocommit-diffcheck.log 2>&1; then
    git reset --mixed >/dev/null 2>&1 || true
    fail "git diff --cached --check 未通过：$(tr '\n' '; ' </tmp/shared-git-autocommit-diffcheck.log)"
fi

python3 - <<'PY'
import re
import subprocess
import sys
patterns = [
    r'(?i)api[_-]?key\s*[:=]',
    r'(?i)secret\s*[:=]',
    r'(?i)token\s*[:=]',
    r'(?i)password\s*[:=]',
    r'sk-[A-Za-z0-9_-]{16,}',
    r'ghp_[A-Za-z0-9_]{20,}',
]
text = subprocess.check_output(
    ['git', 'diff', '--cached', '--', '.', ':(exclude)runtime/**'],
    text=True,
    errors='ignore',
)
found = [pat for pat in patterns if re.search(pat, text)]
if found:
    print('secret_scan_needs_review')
    for pat in found:
        print('MATCH', pat)
    sys.exit(2)
print('staged_secret_scan_ok')
PY

if git diff --cached --quiet; then
    log "changes ignored or nothing staged; branch=$BRANCH"
    exit 0
fi

SUMMARY="$(git diff --cached --stat | tail -1 | sed 's/^ *//')"
COMMIT_MSG="chore: 自动提交共享中台变更 $(TZ=Asia/Shanghai date '+%Y-%m-%d %H:%M')"
git commit -m "$COMMIT_MSG" >/tmp/shared-git-autocommit-commit.log 2>&1 || fail "git commit 失败：$(tr '\n' '; ' </tmp/shared-git-autocommit-commit.log)"
COMMIT="$(git rev-parse --short HEAD)"

if [ "$AUTO_PUSH" = "1" ]; then
    git push origin HEAD >/tmp/shared-git-autocommit-push.log 2>&1 || fail "git push 失败：$(tr '\n' '; ' </tmp/shared-git-autocommit-push.log)"
    PUSH_STATE="已 push"
else
    PUSH_STATE="未 push（SHARED_GIT_AUTOPUSH=0）"
fi

log "committed $COMMIT on $BRANCH; $SUMMARY; $PUSH_STATE"
printf '共享中台已自动提交：%s %s；分支：%s；%s。\n' "$COMMIT" "$COMMIT_MSG" "$BRANCH" "$PUSH_STATE"
