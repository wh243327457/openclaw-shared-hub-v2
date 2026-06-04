"""
Smoke test for resolve_shared_root.py.

We cannot use unittest easily without a runner; this is a minimal ad-hoc check.
Exit code 0 = all probes resolve to a valid root.
"""
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE / "resolve_shared_root.py"
SHARED_ROOT = HERE.parent  # scripts/..

env_overrides = [
    ("SHARED_HUB_ROOT", str(SHARED_ROOT)),
    ("AGENTS_SHARED_ROOT", str(SHARED_ROOT)),
    ("XDG_DATA_HOME", str(SHARED_ROOT)),  # so $XDG_DATA_HOME/openclaw/shared points to <root>/openclaw/shared — invalid, should fall through
    (None, None),  # no override; rely on script-position probe
]

failures = []
for var, val in env_overrides:
    cmd = [sys.executable, str(SCRIPT), "--check"]
    if var is not None:
        cmd_env = {**os.environ, var: val}
    else:
        cmd_env = os.environ.copy()
    # Remove all relevant vars for clean probe
    for k in ("SHARED_HUB_ROOT", "AGENTS_SHARED_ROOT", "XDG_DATA_HOME"):
        cmd_env.pop(k, None)
    if var is not None:
        cmd_env[var] = val
    result = subprocess.run(cmd, env=cmd_env, capture_output=True, text=True)
    expected = str(SHARED_ROOT)
    if result.returncode != 0 or result.stdout.strip() != expected:
        failures.append((var, val, result.returncode, result.stdout, result.stderr))

if failures:
    print("FAIL:", failures, file=sys.stderr)
    sys.exit(1)

print("OK: resolve_shared_root.py --check resolves to", SHARED_ROOT, "in all 4 env variants")
