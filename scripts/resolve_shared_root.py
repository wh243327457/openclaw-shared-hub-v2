#!/usr/bin/env python3
"""
resolve_shared_root.py — 共享中台 v2 的可迁移宿主根路径解析器。

目的：让 Hermes / OpenClaw / future-agent 在不依赖绝对路径 /home/vany/...
的前提下，找到当前机器上的 shared hub v2 根目录。

解析顺序（与 manifest.yaml 的 deployment.resolution_order 对齐）：

  1. $SHARED_HUB_ROOT                      显式环境变量，最优先
  2. $AGENTS_SHARED_ROOT                   别名环境变量
  3. $XDG_DATA_HOME/openclaw/shared        XDG 标准目录
  4. ~/.local/share/openclaw/shared        兜底 XDG
  5. <this-script>/../../                  相对本脚本位置的探针
  6. <this-script>/../                     兜底：脚本所在目录
  7. <cwd>/                                当前工作目录
  8. <cwd>/../                             上一级

只要探针目录里同时存在 manifest.yaml 与 AGENTS.md，就认为该目录是合法的
shared hub 根。

Usage:
    python3 resolve_shared_root.py                   # 打印解析到的根
    python3 resolve_shared_root.py --check           # 解析并校验必填项
    python3 resolve_shared_root.py --json            # JSON 输出
    python3 resolve_shared_root.py --explain         # 列出每一步尝试与原因
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import List, Optional

REQUIRED_FILES = ("manifest.yaml", "AGENTS.md")
SCRIPT_LOCATION = Path(__file__).resolve().parent  # .../scripts


def _expand(p: str) -> str:
    """Expand ~ and env vars without requiring the env var to exist."""
    return os.path.expanduser(os.path.expandvars(p))


def _candidate(label: str, path: Path) -> dict:
    return {
        "label": label,
        "path": str(path),
        "exists": path.is_dir(),
        "is_valid": path.is_dir() and all((path / f).is_file() for f in REQUIRED_FILES),
    }


def _valid(p: Path) -> bool:
    return p.is_dir() and all((p / f).is_file() for f in REQUIRED_FILES)


def resolve(explain: bool = False) -> tuple[Path, List[dict]]:
    """Return (root, attempts). attempts 始终记录，方便排错。"""
    attempts: List[dict] = []
    home = Path.home()

    # 1. SHARED_HUB_ROOT
    val = os.environ.get("SHARED_HUB_ROOT")
    if val:
        p = Path(_expand(val)).resolve()
        attempts.append(_candidate("env:SHARED_HUB_ROOT", p))
        if _valid(p):
            return p, attempts

    # 2. AGENTS_SHARED_ROOT
    val = os.environ.get("AGENTS_SHARED_ROOT")
    if val:
        p = Path(_expand(val)).resolve()
        attempts.append(_candidate("env:AGENTS_SHARED_ROOT", p))
        if _valid(p):
            return p, attempts

    # 3. XDG_DATA_HOME/openclaw/shared
    xdg = os.environ.get("XDG_DATA_HOME")
    if xdg:
        p = (Path(_expand(xdg)) / "openclaw" / "shared").resolve()
        attempts.append(_candidate("xdg:$XDG_DATA_HOME/openclaw/shared", p))
        if _valid(p):
            return p, attempts

    # 4. ~/.local/share/openclaw/shared
    p = (home / ".local" / "share" / "openclaw" / "shared").resolve()
    attempts.append(_candidate("xdg:~/.local/share/openclaw/shared", p))
    if _valid(p):
        return p, attempts

    # 5. <this-script>/../../  (scripts 在 <root>/scripts)
    p = (SCRIPT_LOCATION.parent.parent).resolve()
    attempts.append(_candidate("script:../../", p))
    if _valid(p):
        return p, attempts

    # 6. <this-script>/..  (scripts 与 manifest 同级)
    p = SCRIPT_LOCATION.parent.resolve()
    attempts.append(_candidate("script:..", p))
    if _valid(p):
        return p, attempts

    # 7-8. cwd 兜底
    cwd = Path.cwd().resolve()
    for label, base in (("cwd:.", cwd), ("cwd:..", cwd.parent)):
        attempts.append(_candidate(label, base))
        if _valid(base):
            return base, attempts

    # 没找到合法根，返回最后一个探针 + attempts
    return attempts[-1]["path"] and Path(attempts[-1]["path"]) or cwd, attempts


def main() -> int:
    ap = argparse.ArgumentParser(description="Resolve the shared hub v2 root directory.")
    ap.add_argument("--check", action="store_true", help="校验根目录含必填文件")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    ap.add_argument("--explain", action="store_true", help="打印每一步解析尝试")
    args = ap.parse_args()

    root, attempts = resolve(explain=args.explain)

    valid = _valid(root)
    payload = {
        "root": str(root),
        "valid": valid,
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
        print(
            f"ERROR: {root} is missing one of {REQUIRED_FILES}",
            file=sys.stderr,
        )
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
