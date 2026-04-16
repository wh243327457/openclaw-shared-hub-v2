#!/usr/bin/env python3
"""Verify the shared memory bridge layout and config references."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from promoter import ManifestError, json_dump, load_manifest, resolve_bridge_paths

EXPECTED_OPENCLAW_SKILLS_REF = "/home/node/.openclaw/shared/skills"
DEFAULT_HERMES_CONFIG = "/root/.hermes/config.yaml"
DEFAULT_OPENCLAW_CONFIG = "/home/vany/openclaw-data/.openclaw/openclaw.json"
DEFAULT_WORKSPACES = ["workspace", "workspace-friend-001", "workspace-friend-002"]
DEFAULT_SHARED_SKILLS_MANIFEST = "capabilities/manifests/shared-skills.yaml"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def safe_realpath(path: Path) -> str:
    try:
        return str(path.resolve())
    except FileNotFoundError:
        return str(path)


def path_check(name: str, path: Path, kind: str) -> dict[str, Any]:
    info: dict[str, Any] = {
        "name": name,
        "path": str(path),
        "kind": kind,
    }
    if kind == "dir":
        info["exists"] = path.exists()
        info["ok"] = path.is_dir()
    elif kind == "file":
        info["exists"] = path.exists()
        info["ok"] = path.is_file()
    else:
        raise ValueError(f"Unsupported path check kind: {kind}")
    return info


def symlink_check(name: str, path: Path, expected_target: Path) -> dict[str, Any]:
    exists = path.exists()
    is_link = path.is_symlink()
    actual_target = str(path.resolve()) if is_link and exists else None
    expected_resolved = str(expected_target.resolve()) if expected_target.exists() else str(expected_target)
    return {
        "name": name,
        "path": str(path),
        "kind": "symlink",
        "exists": exists,
        "is_symlink": is_link,
        "actual_target": actual_target,
        "expected_target": expected_resolved,
        "ok": is_link and exists and actual_target == expected_resolved,
    }


def verify_manifest(shared_root: Path) -> tuple[Any | None, dict[str, Any]]:
    manifest_path = shared_root / "manifest.yaml"
    record: dict[str, Any] = {
        "path": str(manifest_path),
        "exists": manifest_path.exists(),
        "loaded": False,
    }
    manifest = None
    if not manifest_path.exists():
        record["error"] = f"manifest not found: {manifest_path}"
        return manifest, record
    try:
        manifest = load_manifest(manifest_path)
        record["loaded"] = True
        record["type"] = type(manifest).__name__
    except ManifestError as exc:
        record["error"] = str(exc)
    return manifest, record


def verify_shared_skills_manifest(shared_root: Path, paths: dict[str, Path]) -> dict[str, Any]:
    manifest_path = shared_root / DEFAULT_SHARED_SKILLS_MANIFEST
    record: dict[str, Any] = {
        "path": str(manifest_path),
        "exists": manifest_path.exists(),
        "loaded": False,
        "records": [],
    }
    if not manifest_path.exists():
        record["ok"] = False
        record["error"] = f"shared skills manifest not found: {manifest_path}"
        return record

    try:
        payload = load_manifest(manifest_path)
        record["loaded"] = True
    except ManifestError as exc:
        record["ok"] = False
        record["error"] = str(exc)
        return record

    skills = payload.get("shared_skills") if isinstance(payload, dict) else None
    if not isinstance(skills, list):
        record["ok"] = False
        record["error"] = "shared_skills must be a YAML list"
        return record

    entries: list[dict[str, Any]] = []
    overall_ok = True
    for skill in skills:
        skill_name = str(skill).strip()
        skill_file = paths["capabilities_skills"] / skill_name / "SKILL.md"
        item_ok = bool(skill_name) and skill_file.is_file()
        overall_ok = overall_ok and item_ok
        entries.append(
            {
                "skill": skill_name,
                "path": str(skill_file),
                "exists": skill_file.exists(),
                "ok": item_ok,
            }
        )

    record["count"] = len(entries)
    record["records"] = entries
    record["ok"] = overall_ok
    return record


def verify_hermes_config(config_path: Path, paths: dict[str, Path]) -> dict[str, Any]:
    expected_skills = str(paths["legacy_skills"])
    expected_prefill = str(paths["prefill_file"])
    record: dict[str, Any] = {
        "path": str(config_path),
        "exists": config_path.exists(),
        "expected_refs": {
            "skills": expected_skills,
            "prefill": expected_prefill,
        },
    }
    if not config_path.exists():
        record["ok"] = False
        record["error"] = "config file not found"
        return record
    try:
        text = read_text(config_path)
    except OSError as exc:
        record["ok"] = False
        record["error"] = f"failed to read config: {exc}"
        return record

    record["has_skills_ref"] = expected_skills in text
    record["has_prefill_ref"] = expected_prefill in text
    record["ok"] = record["has_skills_ref"] and record["has_prefill_ref"]
    return record


def verify_openclaw_config(config_path: Path) -> tuple[dict[str, Any], Path]:
    workspace_base = config_path.parent
    record: dict[str, Any] = {
        "path": str(config_path),
        "exists": config_path.exists(),
        "expected_extra_dir": EXPECTED_OPENCLAW_SKILLS_REF,
    }
    if not config_path.exists():
        record["ok"] = False
        record["error"] = "config file not found"
        return record, workspace_base
    try:
        payload = json.loads(read_text(config_path))
    except (OSError, json.JSONDecodeError) as exc:
        record["ok"] = False
        record["error"] = f"failed to parse config: {exc}"
        return record, workspace_base

    extra_dirs = payload.get("skills", {}).get("load", {}).get("extraDirs", [])
    record["extra_dirs"] = extra_dirs
    record["has_expected_extra_dir"] = EXPECTED_OPENCLAW_SKILLS_REF in extra_dirs
    record["ok"] = record["has_expected_extra_dir"]
    return record, workspace_base


def verify_workspaces(workspace_base: Path, workspace_names: list[str]) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    overall_ok = True
    for name in workspace_names:
        workspace_path = workspace_base / name
        shared_entry = workspace_path / "shared"
        memory_entry = workspace_path / "MEMORY.md"
        memory_dir_entry = workspace_path / "memory"

        record = {
            "name": name,
            "path": str(workspace_path),
            "exists": workspace_path.is_dir(),
            "entries": {
                "shared": {
                    "path": str(shared_entry),
                    "exists": shared_entry.exists(),
                    "is_symlink": shared_entry.is_symlink(),
                    "target": safe_realpath(shared_entry) if shared_entry.exists() or shared_entry.is_symlink() else None,
                },
                "MEMORY.md": {
                    "path": str(memory_entry),
                    "exists": memory_entry.exists(),
                    "is_symlink": memory_entry.is_symlink(),
                    "target": safe_realpath(memory_entry) if memory_entry.exists() or memory_entry.is_symlink() else None,
                },
                "memory": {
                    "path": str(memory_dir_entry),
                    "exists": memory_dir_entry.exists(),
                    "is_symlink": memory_dir_entry.is_symlink(),
                    "target": safe_realpath(memory_dir_entry) if memory_dir_entry.exists() or memory_dir_entry.is_symlink() else None,
                },
            },
        }
        record["ok"] = record["exists"] and all(entry["exists"] for entry in record["entries"].values())
        overall_ok = overall_ok and record["ok"]
        records.append(record)
    return {
        "base": str(workspace_base),
        "names": workspace_names,
        "records": records,
        "ok": overall_ok,
    }


def collect_structure_checks(shared_root: Path, paths: dict[str, Path]) -> dict[str, Any]:
    legacy_memory = paths["legacy_memory"]
    compat_dreams = paths["compat_daily"] / ".dreams"
    runtime_openclaw_dreams = paths["runtime"] / "openclaw" / "dreams"

    path_records = [
        path_check("shared/curated", paths["curated"], "dir"),
        path_check("shared/curated/memory", paths["curated_memory"], "dir"),
        path_check("shared/curated/memory/facts", paths["facts"], "dir"),
        path_check("shared/curated/memory/projects", paths["projects"], "dir"),
        path_check("shared/curated/memory/MEMORY.md", paths["memory_index"], "file"),
        path_check("shared/compat", paths["compat"], "dir"),
        path_check("shared/compat/daily", paths["compat_daily"], "dir"),
        path_check("shared/inbox", paths["inbox"], "dir"),
        path_check("shared/runtime", paths["runtime"], "dir"),
        path_check("shared/runtime/openclaw/dreams", runtime_openclaw_dreams, "dir"),
        path_check("shared/capabilities", paths["capabilities"], "dir"),
        path_check("shared/capabilities/manifests", paths["capabilities"] / "manifests", "dir"),
        path_check("shared/capabilities/manifests/shared-skills.yaml", shared_root / DEFAULT_SHARED_SKILLS_MANIFEST, "file"),
        path_check("shared/memory", legacy_memory, "dir"),
        path_check("shared/prefill/hermes-shared-memory.json", paths["prefill_file"], "file"),
        path_check("shared/README.md", shared_root / "README.md", "file"),
        path_check("shared/AGENTS.md", shared_root / "AGENTS.md", "file"),
    ]
    link_records = [
        symlink_check("shared/skills", paths["legacy_skills"], paths["capabilities_skills"]),
        symlink_check("shared/memory/MEMORY.md", legacy_memory / "MEMORY.md", paths["memory_index"]),
        symlink_check("shared/memory/facts", legacy_memory / "facts", paths["facts"]),
        symlink_check("shared/memory/projects", legacy_memory / "projects", paths["projects"]),
        symlink_check("shared/memory/daily", legacy_memory / "daily", paths["compat_daily"]),
        symlink_check("shared/compat/daily/.dreams", compat_dreams, runtime_openclaw_dreams),
    ]
    overall_ok = all(item["ok"] for item in path_records) and all(item["ok"] for item in link_records)
    return {
        "paths": path_records,
        "symlinks": link_records,
        "ok": overall_ok,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--shared-root",
        default=str(Path(__file__).resolve().parent.parent),
        help="shared 根目录，默认取脚本上级目录",
    )
    parser.add_argument(
        "--hermes-config",
        default=DEFAULT_HERMES_CONFIG,
        help=f"Hermes 配置文件，默认 {DEFAULT_HERMES_CONFIG}",
    )
    parser.add_argument(
        "--openclaw-config",
        default=DEFAULT_OPENCLAW_CONFIG,
        help=f"OpenClaw 配置文件，默认 {DEFAULT_OPENCLAW_CONFIG}",
    )
    parser.add_argument(
        "--workspace-base",
        default=None,
        help="workspace 根目录；默认取 openclaw.json 所在目录",
    )
    parser.add_argument(
        "--workspace-name",
        action="append",
        dest="workspace_names",
        help="追加要验证的 workspace 名称；默认验证固定 3 个",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    shared_root = Path(args.shared_root).expanduser().resolve()
    hermes_config = Path(args.hermes_config).expanduser().resolve()
    openclaw_config = Path(args.openclaw_config).expanduser().resolve()
    workspace_names = args.workspace_names or list(DEFAULT_WORKSPACES)

    manifest, manifest_record = verify_manifest(shared_root)
    paths = resolve_bridge_paths(manifest or {}, shared_root)
    structure = collect_structure_checks(shared_root, paths)
    shared_skills_record = verify_shared_skills_manifest(shared_root, paths)
    hermes_record = verify_hermes_config(hermes_config, paths)
    openclaw_record, inferred_workspace_base = verify_openclaw_config(openclaw_config)
    workspace_base = Path(args.workspace_base).expanduser().resolve() if args.workspace_base else inferred_workspace_base
    workspace_record = verify_workspaces(workspace_base, workspace_names)

    errors: list[str] = []
    if not manifest_record.get("loaded"):
        errors.append("manifest")
    if not structure["ok"]:
        errors.append("structure")
    if not shared_skills_record.get("ok"):
        errors.append("shared_skills")
    if not hermes_record.get("ok"):
        errors.append("hermes_config")
    if not openclaw_record.get("ok"):
        errors.append("openclaw_config")
    if not workspace_record.get("ok"):
        errors.append("workspaces")

    payload = {
        "ok": not errors,
        "shared_root": str(shared_root),
        "manifest": manifest_record,
        "structure": structure,
        "shared_skills_manifest": shared_skills_record,
        "hermes_config": hermes_record,
        "openclaw_config": openclaw_record,
        "workspaces": workspace_record,
        "errors": errors,
    }
    print(json_dump(payload))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
