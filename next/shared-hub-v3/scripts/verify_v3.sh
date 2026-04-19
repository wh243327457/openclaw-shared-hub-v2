#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

printf '[shared-v3-verify] root=%s
' "$ROOT_DIR"
if python3 "$ROOT_DIR/tools/shared_v3_verify.py"; then
    printf '[shared-v3-verify] wrapper=PASS
'
else
    printf '[shared-v3-verify] wrapper=FAIL
' >&2
    exit 1
fi
