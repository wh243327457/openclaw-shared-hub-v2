#!/usr/bin/env python3
"""
resolve_shared_root.py — 共享中台 v2 的可迁移根路径解析器。

Canonical location policy:
  - 推荐统一宿主目录：~/agent/shared
  - 共享中台本身不是 runtime；runtime/ 只是共享根下的临时产物层。
  - 如果默认目录不存在，可 clone / 解包到任意路径；resolver 仍可通过脚本相对位置找到根。

Valid root = directory contains both manifest.yaml and AGENTS.md.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import List

REQUIRED_FILES = ("manifest.yaml", "AGENTS.md")
SCRIPT_LOCATION = Path(__file__).resolve().parent


def _expand(p: str) -> str:
    return os.path.expanduser(os.path.expandvars(p))


def _candidate(label: str, path: Path, source: str = "probe") -> dict:
    exists = path.is_dir()
    return {
        "label": label,
        "source": source,
        "path": str(path),
        "exists": exists,
        "is_valid": exists and all((path / f).is_file() for f in REQUIRED_FILES),
    }


def _valid(p: Path) -> bool:
    return p.is_dir() and all((p / f).is_file() for f in REQUIRED_FILES)


def _append_env_candidate(attempts: List[dict], var_name: str) -> Path | None:
    val = os.environ.get(var_name)
    if not val:
        return None
    p = Path(_expand(val)).resolve()
    attempts.append(_candidate(f"env:{var_name}", p, source="env"))
    return p


def resolve(strict_env: bool = False) -> tuple[Path, List[dict]]:
    """Return (root, attempts). attempts 始终记录，方便排错。"""
    attempts: List[dict] = []
    cwd = Path.cwd().resolve()

    # 1. SHARED_HUB_ROOT
    p = _append_env_candidate(attempts, "SHARED_HUB_ROOT")
    if p is not None:
        if _valid(p):
            return p, attempts
        if strict_env:
            return p, attempts

    # 2. AGENTS_SHARED_ROOT
    p = _append_env_candidate(attempts, "AGENTS_SHARED_ROOT")
    if p is not None:
        if _valid(p):
            return p, attempts
        if strict_env:
            return p, attempts

    # 3. XDG_DATA_HOME/openclaw/shared
    xdg = os.environ.get("XDG_DATA_HOME")
    if xdg:
        p = (Path(_expand(xdg)) / "openclaw" / "shared").resolve()
        attempts.append(_candidate("xdg:$XDG_DATA_HOME/openclaw/shared", p, source="xdg"))
        if _valid(p):
            return p, attempts

    # 4. ~/.local/share/openclaw/shared
    p = (Path.home() / ".local" / "share" / "openclaw" / "shared").resolve()
    attempts.append(_candidate("xdg:~/.local/share/openclaw/shared", p, source="xdg"))
    if _valid(p):
        return p, attempts

    # 5. ~/agent/shared (project canonical host location)
    p = (Path.home() / "agent" / "shared").resolve()
    attempts.append(_candidate("home:~/agent/shared", p, source="canonical"))
    if _valid(p):
        return p, attempts

    # 6. <this-script>/../../
    p = SCRIPT_LOCATION.parent.parent.resolve()
    attempts.append(_candidate("script:../..", p, source="script"))
    if _valid(p):
        return p, attempts

    # 7. <this-script>/..
    p = SCRIPT_LOCATION.parent.resolve()
    attempts.append(_candidate("script:..", p, source="script"))
    if _valid(p):
        return p, attempts

    # 8-9. cwd fallbacks
    for label, base in (("cwd:.", cwd), ("cwd:..", cwd.parent)):
        attempts.append(_candidate(label, base, source="cwd"))
        if _valid(base):
            return base, attempts

    return Path(attempts[-1]["path"]) if attempts else cwd, attempts


def main() -> int:
    ap = argparse.ArgumentParser(description="Resolve the shared hub v2 root directory.")
    ap.add_argument("--check", action="store_true", help="校验根目录含必填文件")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    ap.add_argument("--explain", action="store_true", help="打印每一步解析尝试")
    ap.add_argument("--strict-env", action="store_true", help="env 变量存在但无效时不降级")
    args = ap.parse_args()

    root, attempts = resolve(strict_env=args.strict_env)
    valid = _valid(root)
    payload = {
        "root": str(root),
        "valid": valid,
        "required_files": list(REQUIRED_FILES),
        "attempts": attempts if (args.explain or args.json) else None,
    }

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(root)
        if args.explain:
            for a in attempts:
                mark = "OK " if a["is_valid"] else ("-- " if a["exists"] else "x  ")
                print(f"  {mark} {a['label']:<42} {a['path']}")

    if args.check and not valid:
        bad_env = next((a for a in attempts if a.get("source") == "env" and not a["is_valid"]), None)
        if args.strict_env and bad_env:
            print(f"ERROR: {bad_env['label']} points to an invalid shared root: {bad_env['path']}", file=sys.stderr)
        else:
            print(f"ERROR: {root} is missing one of {REQUIRED_FILES}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
