#!/bin/bash
# System-level wrapper for the OpenHuman-inspired memory tree localization POC.
# Keeps all generated artifacts under shared/runtime/hermes/memory-tree-localization.
set -euo pipefail

cd /home/vany/agent/.openclaw/shared

RUNTIME_ROOT="runtime/hermes/memory-tree-localization"
LOG_DIR="$RUNTIME_ROOT/system-runs"
mkdir -p "$LOG_DIR"

TIMESTAMP="$(date -Iseconds)"
RUN_ID="$(date -u +%Y-%m-%d-%H%M%S)"
DRY_RUN="${DRY_RUN:-0}"
POC_MODE="${MEMORY_TREE_POC_MODE:-all}"
INPUT_FILE="${MEMORY_TREE_INPUT_FILE:-}"
RUNNER="/home/vany/agent/.openclaw/shared/runtime/hermes/memory-tree-localization/runner.py"
VERIFY="/home/vany/agent/.openclaw/shared/runtime/hermes/memory-tree-localization/verify_setup.py"
LOG_FILE="$LOG_DIR/$RUN_ID.log"

{
  echo "[$TIMESTAMP] memory-tree-localization system run start"
  echo "dry_run=$DRY_RUN poc_mode=$POC_MODE input_file=${INPUT_FILE:-<auto>}"

  python3 "$VERIFY"

  if [ "$DRY_RUN" = "1" ]; then
    python3 "$RUNNER" --poc "$POC_MODE" --dry-run
  elif [ -n "$INPUT_FILE" ]; then
    python3 "$RUNNER" --poc "$POC_MODE" --input-file "$INPUT_FILE" -v
  else
    python3 "$RUNNER" --poc "$POC_MODE" -v
  fi

  echo "[$(date -Iseconds)] memory-tree-localization system run done"
} >> "$LOG_FILE" 2>&1

cat "$LOG_FILE"
