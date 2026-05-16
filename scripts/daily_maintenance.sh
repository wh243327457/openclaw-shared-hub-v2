#!/bin/bash
# Daily shared hub maintenance + self-monitoring
set -e

cd /home/vany/openclaw-data/.openclaw/shared
LOG_DIR="runtime/hermes"
mkdir -p "$LOG_DIR"

TIMESTAMP=$(date -Iseconds)
DRY_RUN="${DRY_RUN:-0}"
SHARED_ONLY="${SHARED_ONLY:-0}"
RUN_KB_SYNC="${RUN_KB_SYNC:-1}"
RUN_GITHUB_LEARNING="${RUN_GITHUB_LEARNING:-1}"
GITHUB_LEARNING_DATE="${GITHUB_LEARNING_DATE:-$(TZ=Asia/Shanghai date -d '1 day ago' +%F)}"
GITHUB_LEARNING_LOG_DIR="$LOG_DIR/github-hot-project-learning"
mkdir -p "$GITHUB_LEARNING_LOG_DIR"

if [ "$SHARED_ONLY" = "1" ]; then
  RUN_KB_SYNC=0
fi
if [ "$DRY_RUN" = "1" ]; then
  RUN_KB_SYNC=0
fi

echo "[$TIMESTAMP] === daily maintenance start === dry_run=$DRY_RUN shared_only=$SHARED_ONLY run_kb_sync=$RUN_KB_SYNC run_github_learning=$RUN_GITHUB_LEARNING github_learning_date=$GITHUB_LEARNING_DATE" >> "$LOG_DIR/cron.log"

# 1. Promoter - refresh auto-state block, or dry-run without writing curated memory.
if [ "$DRY_RUN" = "1" ]; then
  python3 scripts/promoter.py --dry-run --scan-promote-candidates >> "$LOG_DIR/promoter-cron.log" 2>&1 || {
      echo "[$TIMESTAMP] promoter dry-run failed" >> "$LOG_DIR/cron.log"
  }
else
  python3 scripts/promoter.py >> "$LOG_DIR/promoter-cron.log" 2>&1 || {
      echo "[$TIMESTAMP] promoter failed" >> "$LOG_DIR/cron.log"
  }
fi

# 2. Promotion governance candidate scan (report-only; never writes curated memory).
python3 scripts/promoter.py --dry-run --scan-promote-candidates --recent-limit 20 --max-candidates-per-file 10 >> "$LOG_DIR/promotion-governance-cron.log" 2>&1 || {
    echo "[$TIMESTAMP] promotion governance scan failed" >> "$LOG_DIR/cron.log"
}

# 3. GitHub hot project learning bridge + healthcheck.
if [ "$RUN_GITHUB_LEARNING" = "1" ]; then
  if [ "$DRY_RUN" = "1" ]; then
    python3 scripts/openclaw_github_learning_bridge.py --date "$GITHUB_LEARNING_DATE" --dry-run >> "$GITHUB_LEARNING_LOG_DIR/bridge-cron.log" 2>&1 || {
        echo "[$TIMESTAMP] github learning bridge dry-run failed" >> "$LOG_DIR/cron.log"
    }
  else
    python3 scripts/openclaw_github_learning_bridge.py --date "$GITHUB_LEARNING_DATE" >> "$GITHUB_LEARNING_LOG_DIR/bridge-cron.log" 2>&1 || {
        echo "[$TIMESTAMP] github learning bridge failed" >> "$LOG_DIR/cron.log"
    }
  fi
  python3 scripts/github_learning_healthcheck.py --date "$GITHUB_LEARNING_DATE" >> "$GITHUB_LEARNING_LOG_DIR/healthcheck-cron.log" 2>&1 || {
      echo "[$TIMESTAMP] github learning healthcheck non-green" >> "$LOG_DIR/cron.log"
  }
else
  echo "[$TIMESTAMP] github learning bridge skipped" >> "$LOG_DIR/cron.log"
fi

# 4. Verify bridge health.
python3 scripts/verify_bridge.py >> "$LOG_DIR/verify-cron.log" 2>&1 || {
    echo "[$TIMESTAMP] verify failed" >> "$LOG_DIR/cron.log"
}

# 5. Disk usage monitoring.
echo "[$TIMESTAMP] disk usage:" >> "$LOG_DIR/cron.log"
df -h /home/vany >> "$LOG_DIR/cron.log" 2>&1 || true

# 6. Shared directory size tracking.
SHARED_SIZE=$(du -sh . 2>/dev/null | cut -f1)
echo "[$TIMESTAMP] shared dir size: $SHARED_SIZE" >> "$LOG_DIR/cron.log"

# 7. Inbox backlog check.
HERMES_COUNT=$(find inbox/hermes/daily -maxdepth 1 -type f -name '*.md' 2>/dev/null | wc -l)
OPENCLAW_COUNT=$(find inbox/openclaw/daily -maxdepth 1 -type f -name '*.md' 2>/dev/null | wc -l)
FUTURE_AGENT_COUNT=$(find inbox/future-agent/daily -maxdepth 1 -type f -name '*.md' 2>/dev/null | wc -l)
echo "[$TIMESTAMP] inbox backlog: hermes=$HERMES_COUNT, openclaw=$OPENCLAW_COUNT, future-agent=$FUTURE_AGENT_COUNT" >> "$LOG_DIR/cron.log"

# 8. Knowledge base git auto-sync (optional; disabled by SHARED_ONLY=1 or DRY_RUN=1).
if [ "$RUN_KB_SYNC" = "1" ]; then
  echo "[$TIMESTAMP] kb sync:" >> "$LOG_DIR/cron.log"
  bash /home/vany/openclaw-data/.openclaw/shared/scripts/kb_git_sync.sh >> "$LOG_DIR/kb_sync.log" 2>&1 || {
      echo "[$TIMESTAMP] kb sync failed" >> "$LOG_DIR/cron.log"
  }
else
  echo "[$TIMESTAMP] kb sync skipped" >> "$LOG_DIR/cron.log"
fi

echo "[$TIMESTAMP] === daily maintenance done ===" >> "$LOG_DIR/cron.log"
