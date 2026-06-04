#!/usr/bin/env python3
"""Bootstrap machine-local directories and compatibility symlinks for shared hub v2.

This script is safe to run after clone/import on every machine. It creates only
runtime/inbox skeleton directories and relative compatibility symlinks. It does
not overwrite real files or secrets.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from resolve_shared_root import resolve  # noqa: E402


def rel_target(link: Path, target: Path) -> str:
    return os.path.relpath(target, start=link.parent)


def ensure_dir(path: Path, dry_run: bool, actions: list[dict[str, Any]]) -> None:
    if path.is_dir():
        actions.append({"action": "dir_exists", "path": str(path), "ok": True})
        return
    if path.exists() and not path.is_dir():
        actions.append({"action": "dir_conflict", "path": str(path), "ok": False})
        return
    actions.append({"action": "mkdir", "path": str(path), "ok": True, "dry_run": dry_run})
    if not dry_run:
        path.mkdir(parents=True, exist_ok=True)


def ensure_symlink(link: Path, target: Path, dry_run: bool, actions: list[dict[str, Any]], force: bool = False) -> None:
    expected = rel_target(link, target)
    if link.is_symlink():
        current = os.readlink(link)
        if current == expected or link.resolve() == target.resolve():
            actions.append({"action": "symlink_exists", "path": str(link), "target": current, "ok": True})
            return
        if not force:
            actions.append({"action": "symlink_mismatch", "path": str(link), "target": current, "expected": expected, "ok": False})
            return
        actions.append({"action": "replace_symlink", "path": str(link), "old_target": current, "target": expected, "ok": True, "dry_run": dry_run})
        if not dry_run:
            link.unlink()
            link.symlink_to(expected)
        return
    if link.exists():
        actions.append({"action": "path_conflict", "path": str(link), "expected_target": expected, "ok": False})
        return
    actions.append({"action": "symlink", "path": str(link), "target": expected, "ok": True, "dry_run": dry_run})
    if not dry_run:
        link.parent.mkdir(parents=True, exist_ok=True)
        link.symlink_to(expected)


def main() -> int:
    ap = argparse.ArgumentParser(description="Bootstrap shared hub v2 local runtime skeleton and compat symlinks.")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force-symlinks", action="store_true", help="Replace mismatched symlinks; never replaces real files/dirs.")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    root, attempts = resolve()
    actions: list[dict[str, Any]] = []

    dirs = [
        root / "runtime" / "hermes",
        root / "runtime" / "openclaw" / "dreams",
        root / "runtime" / "future-agent",
        root / "inbox" / "hermes" / "daily",
        root / "inbox" / "openclaw" / "daily",
        root / "inbox" / "future-agent" / "daily",
        root / "compat" / "daily",
        root / "memory",
    ]
    for d in dirs:
        ensure_dir(d, args.dry_run, actions)

    readme = root / "runtime" / "future-agent" / "README.md"
    if not readme.exists():
        actions.append({"action": "write_file", "path": str(readme), "ok": True, "dry_run": args.dry_run})
        if not args.dry_run:
            readme.parent.mkdir(parents=True, exist_ok=True)
            readme.write_text("# future-agent runtime\n\nMachine-local runtime artifacts for future-agent. Do not commit generated files.\n", encoding="utf-8")

    ensure_symlink(root / "skills", root / "capabilities" / "skills", args.dry_run, actions, args.force_symlinks)
    ensure_symlink(root / "memory" / "MEMORY.md", root / "curated" / "memory" / "MEMORY.md", args.dry_run, actions, args.force_symlinks)
    ensure_symlink(root / "memory" / "facts", root / "curated" / "memory" / "facts", args.dry_run, actions, args.force_symlinks)
    ensure_symlink(root / "memory" / "projects", root / "curated" / "memory" / "projects", args.dry_run, actions, args.force_symlinks)
    ensure_symlink(root / "memory" / "daily", root / "compat" / "daily", args.dry_run, actions, args.force_symlinks)
    ensure_symlink(root / "compat" / "daily" / ".dreams", root / "runtime" / "openclaw" / "dreams", args.dry_run, actions, args.force_symlinks)

    ok = all(item.get("ok") for item in actions)
    payload = {"ok": ok, "shared_root": str(root), "actions": actions, "attempts": attempts}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"shared_root: {root}")
        for item in actions:
            status = "OK" if item.get("ok") else "FAIL"
            print(f"{status} {item['action']}: {item.get('path')}" + (f" -> {item.get('target')}" if item.get('target') else ""))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
