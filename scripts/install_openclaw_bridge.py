#!/usr/bin/env python3
"""Install the local OpenClaw bridge for shared hub v2.

Default mode is dry-run: print the config/workspace changes that would be made.
Use --apply to write the local OpenClaw config and optional workspace symlinks.
This script never writes secrets and never replaces real files/directories.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from resolve_shared_root import resolve  # noqa: E402

DEFAULT_WORKSPACES = ["workspace", "workspace-friend-001", "workspace-friend-002"]


def first_existing_path(candidates: list[Path], fallback: Path) -> Path:
    for item in candidates:
        try:
            expanded = item.expanduser().resolve()
            if expanded.exists():
                return expanded
        except OSError:
            continue
    return fallback.expanduser().resolve()


def default_config_path() -> Path:
    env_config = os.environ.get("OPENCLAW_CONFIG")
    if env_config:
        return Path(os.path.expanduser(os.path.expandvars(env_config))).resolve()
    candidates: list[Path] = []
    for var in ("OPENCLAW_HOME", "OPENCLAW_AGENT_DIR"):
        val = os.environ.get(var)
        if val:
            candidates.append(Path(os.path.expanduser(os.path.expandvars(val))) / "openclaw.json")
    candidates.extend([
        Path.home() / ".openclaw" / "openclaw.json",
        Path("/home/node/.openclaw/openclaw.json"),  # portable-audit: allow standard OpenClaw container fallback
    ])
    return first_existing_path(candidates, candidates[0] if candidates else Path.home() / ".openclaw" / "openclaw.json")


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {}


def dump_json_atomic(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=f"{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def ensure_nested_dict(data: dict[str, Any], keys: list[str]) -> dict[str, Any]:
    current = data
    for key in keys:
        value = current.get(key)
        if not isinstance(value, dict):
            value = {}
            current[key] = value
        current = value
    return current


def add_unique(values: Any, item: str) -> tuple[list[str], bool]:
    if isinstance(values, list):
        result = [str(v) for v in values]
    elif values is None:
        result = []
    else:
        result = [str(values)]
    if item not in result:
        result.append(item)
        return result, True
    return result, False


def rel_target(link: Path, target: Path) -> str:
    return os.path.relpath(target, start=link.parent)


def symlink_action(link: Path, target: Path, apply: bool, force: bool) -> dict[str, Any]:
    expected = rel_target(link, target)
    if link.is_symlink():
        current = os.readlink(link)
        if current == expected or link.resolve() == target.resolve():
            return {"action": "symlink_exists", "path": str(link), "target": current, "ok": True}
        if not force:
            return {"action": "symlink_mismatch", "path": str(link), "target": current, "expected": expected, "ok": False}
        if apply:
            link.unlink()
            link.symlink_to(expected)
        return {"action": "replace_symlink", "path": str(link), "old_target": current, "target": expected, "ok": True, "dry_run": not apply}
    if link.exists():
        return {"action": "path_conflict", "path": str(link), "expected_target": expected, "ok": False}
    if apply:
        link.parent.mkdir(parents=True, exist_ok=True)
        link.symlink_to(expected)
    return {"action": "symlink", "path": str(link), "target": expected, "ok": True, "dry_run": not apply}


def planned_paths(shared_root: Path) -> dict[str, str]:
    return {
        "shared_root": str(shared_root),
        "legacy_skills": str(shared_root / "skills"),
        "capabilities_skills": str(shared_root / "capabilities" / "skills"),
        "legacy_memory": str(shared_root / "memory"),
        "memory_index": str(shared_root / "memory" / "MEMORY.md"),
    }


def apply_config(config_path: Path, shared_root: Path) -> list[dict[str, Any]]:
    data = load_json(config_path)
    paths = planned_paths(shared_root)
    changes: list[dict[str, Any]] = []

    extra = ensure_nested_dict(data, ["skills", "load"])
    extra_dirs, changed = add_unique(extra.get("extraDirs"), paths["legacy_skills"])
    extra["extraDirs"] = extra_dirs
    if changed:
        changes.append({"field": "skills.load.extraDirs", "value": paths["legacy_skills"]})

    shared = ensure_nested_dict(data, ["sharedHub"])
    for key, value in {
        "root": paths["shared_root"],
        "skills": paths["legacy_skills"],
        "memory": paths["legacy_memory"],
        "memoryIndex": paths["memory_index"],
    }.items():
        if shared.get(key) != value:
            shared[key] = value
            changes.append({"field": f"sharedHub.{key}", "value": value})

    backup = None
    if config_path.exists():
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup = config_path.with_name(f"{config_path.name}.bak.{stamp}")
        shutil.copy2(config_path, backup)
    dump_json_atomic(config_path, data)
    if backup:
        changes.append({"field": "backup", "value": str(backup)})
    return changes


def workspace_actions(workspace_base: Path, workspace_names: list[str], shared_root: Path, apply: bool, force: bool) -> list[dict[str, Any]]:
    actions: list[dict[str, Any]] = []
    for name in workspace_names:
        workspace = workspace_base / name
        actions.append({"action": "workspace", "path": str(workspace), "exists": workspace.is_dir(), "ok": workspace.is_dir()})
        if not workspace.is_dir():
            continue
        actions.append(symlink_action(workspace / "shared", shared_root, apply, force))
        actions.append(symlink_action(workspace / "MEMORY.md", shared_root / "memory" / "MEMORY.md", apply, force))
        actions.append(symlink_action(workspace / "memory", shared_root / "memory", apply, force))
    return actions


def main() -> int:
    parser = argparse.ArgumentParser(description="Install OpenClaw local config/workspace bridge for shared hub v2.")
    parser.add_argument("--apply", action="store_true", help="Actually write config and symlinks. Default is dry-run.")
    parser.add_argument("--config", default=None, help="OpenClaw config path. Defaults to $OPENCLAW_CONFIG / $OPENCLAW_HOME / ~/.openclaw/openclaw.json.")
    parser.add_argument("--shared-root", default=None, help="Shared hub root. Defaults to resolver output.")
    parser.add_argument("--workspace-base", default=None, help="Directory containing OpenClaw workspaces. Defaults to config parent.")
    parser.add_argument("--workspace-name", action="append", dest="workspace_names", help="Workspace name to bridge; repeatable.")
    parser.add_argument("--skip-workspaces", action="store_true", help="Only update config; do not plan/create workspace symlinks.")
    parser.add_argument("--force-symlinks", action="store_true", help="Replace mismatched symlinks; never replaces real files/dirs.")
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    args = parser.parse_args()

    shared_root = Path(args.shared_root).expanduser().resolve() if args.shared_root else resolve()[0]
    config_path = Path(args.config).expanduser().resolve() if args.config else default_config_path()
    workspace_base = Path(args.workspace_base).expanduser().resolve() if args.workspace_base else config_path.parent
    workspace_names = args.workspace_names or DEFAULT_WORKSPACES
    paths = planned_paths(shared_root)
    plan: dict[str, Any] = {
        "agent": "openclaw",
        "mode": "apply" if args.apply else "dry-run",
        "config_path": str(config_path),
        "config_exists": config_path.exists(),
        "workspace_base": str(workspace_base),
        "paths": paths,
        "config_changes": [
            {"field": "skills.load.extraDirs", "value": paths["legacy_skills"]},
            {"field": "sharedHub.root", "value": paths["shared_root"]},
            {"field": "sharedHub.skills", "value": paths["legacy_skills"]},
            {"field": "sharedHub.memory", "value": paths["legacy_memory"]},
            {"field": "sharedHub.memoryIndex", "value": paths["memory_index"]},
        ],
        "workspace_actions": [],
        "notes": [
            "Default is dry-run; pass --apply to write openclaw.json and workspace symlinks.",
            "No secrets are read or written.",
            "Restart OpenClaw after applying local config changes.",
        ],
        "ok": True,
    }

    if not args.skip_workspaces:
        plan["workspace_actions"] = workspace_actions(workspace_base, workspace_names, shared_root, args.apply, args.force_symlinks)
    if args.apply:
        try:
            plan["applied_config_changes"] = apply_config(config_path, shared_root)
        except Exception as exc:
            plan["ok"] = False
            plan["error"] = f"{type(exc).__name__}: {exc}"
    if plan["workspace_actions"] and not all(item.get("ok") for item in plan["workspace_actions"]):
        plan["ok"] = False

    if args.json:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
    else:
        print(f"mode: {plan['mode']}")
        print(f"config: {config_path}")
        print(f"shared_root: {shared_root}")
        for change in plan["config_changes"]:
            print(f"would set {change['field']}: {change['value']}")
        for action in plan["workspace_actions"]:
            status = "OK" if action.get("ok") else "FAIL"
            print(f"{status} {action.get('action')}: {action.get('path')}" + (f" -> {action.get('target')}" if action.get("target") else ""))
        if args.apply:
            print("applied" if plan["ok"] else f"failed: {plan.get('error', 'workspace conflict')}")
    return 0 if plan["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
