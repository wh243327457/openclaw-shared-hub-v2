#!/usr/bin/env python3
"""Install the local Hermes bridge for shared hub v2.

Default mode is dry-run: print the exact config changes that would be made.
Use --apply to write the local Hermes config. This script never writes secrets.
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


def default_config_path() -> Path:
    env_config = os.environ.get("HERMES_CONFIG")
    if env_config:
        return Path(os.path.expanduser(os.path.expandvars(env_config))).resolve()
    hermes_home = Path(os.path.expanduser(os.path.expandvars(os.environ.get("HERMES_HOME", str(Path.home() / ".hermes"))))).resolve()
    return hermes_home / "config.yaml"


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        import yaml  # type: ignore
    except ImportError as exc:  # pragma: no cover - environment dependent
        raise RuntimeError("PyYAML is required for --apply. Run in the Hermes venv or install pyyaml.") from exc
    if not path.exists():
        return {}
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {}


def dump_yaml_atomic(path: Path, data: dict[str, Any]) -> None:
    import yaml  # type: ignore

    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=f"{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            yaml.safe_dump(data, handle, sort_keys=False, allow_unicode=True, default_flow_style=False, width=120)
        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def ensure_list_value(container: dict[str, Any], key: str, value: str) -> bool:
    current = container.get(key)
    if current is None:
        container[key] = [value]
        return True
    if isinstance(current, str):
        if current == value:
            container[key] = [current]
            return True
        container[key] = [current, value]
        return True
    if isinstance(current, list):
        if value not in current:
            current.append(value)
            return True
        return False
    container[key] = [value]
    return True


def planned_paths(shared_root: Path) -> dict[str, str]:
    return {
        "shared_root": str(shared_root),
        "skills_dir": str(shared_root / "skills"),
        "prefill_file": str(shared_root / "prefill" / "hermes-shared-memory.json"),
    }


def apply_config(config_path: Path, shared_root: Path) -> list[dict[str, Any]]:
    data = load_yaml(config_path)
    paths = planned_paths(shared_root)
    changes: list[dict[str, Any]] = []

    skills = data.setdefault("skills", {})
    if not isinstance(skills, dict):
        data["skills"] = skills = {}
    if ensure_list_value(skills, "extra_dirs", paths["skills_dir"]):
        changes.append({"field": "skills.extra_dirs", "value": paths["skills_dir"]})

    # Hermes versions differ on where prefill/imported system context is wired.
    # Keep both keys as harmless explicit pointers; consumers can read either.
    shared_hub = data.setdefault("shared_hub", {})
    if not isinstance(shared_hub, dict):
        data["shared_hub"] = shared_hub = {}
    for key, value in {
        "root": paths["shared_root"],
        "prefill": paths["prefill_file"],
        "skills": paths["skills_dir"],
    }.items():
        if shared_hub.get(key) != value:
            shared_hub[key] = value
            changes.append({"field": f"shared_hub.{key}", "value": value})

    backup = None
    if config_path.exists():
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup = config_path.with_name(f"{config_path.name}.bak.{stamp}")
        shutil.copy2(config_path, backup)
    dump_yaml_atomic(config_path, data)
    if backup:
        changes.append({"field": "backup", "value": str(backup)})
    return changes


def main() -> int:
    parser = argparse.ArgumentParser(description="Install Hermes local config bridge for shared hub v2.")
    parser.add_argument("--apply", action="store_true", help="Actually write Hermes config. Default is dry-run.")
    parser.add_argument("--config", default=None, help="Hermes config path. Defaults to $HERMES_CONFIG, $HERMES_HOME/config.yaml, or ~/.hermes/config.yaml.")
    parser.add_argument("--shared-root", default=None, help="Shared hub root. Defaults to resolver output.")
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    args = parser.parse_args()

    shared_root = Path(args.shared_root).expanduser().resolve() if args.shared_root else resolve()[0]
    config_path = Path(args.config).expanduser().resolve() if args.config else default_config_path()
    paths = planned_paths(shared_root)
    plan = {
        "agent": "hermes",
        "mode": "apply" if args.apply else "dry-run",
        "config_path": str(config_path),
        "config_exists": config_path.exists(),
        "paths": paths,
        "changes": [
            {"field": "skills.extra_dirs", "value": paths["skills_dir"]},
            {"field": "shared_hub.root", "value": paths["shared_root"]},
            {"field": "shared_hub.prefill", "value": paths["prefill_file"]},
            {"field": "shared_hub.skills", "value": paths["skills_dir"]},
        ],
        "notes": [
            "Default is dry-run; pass --apply to write config.yaml.",
            "No secrets are read or written.",
            "Restart Hermes or /reset after applying local config changes.",
        ],
        "ok": True,
    }

    if args.apply:
        try:
            plan["applied_changes"] = apply_config(config_path, shared_root)
        except Exception as exc:
            plan["ok"] = False
            plan["error"] = f"{type(exc).__name__}: {exc}"

    if args.json:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
    else:
        print(f"mode: {plan['mode']}")
        print(f"config: {config_path}")
        print(f"shared_root: {shared_root}")
        for change in plan["changes"]:
            print(f"would set {change['field']}: {change['value']}")
        if args.apply:
            print("applied" if plan["ok"] else f"failed: {plan.get('error')}")
    return 0 if plan["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
