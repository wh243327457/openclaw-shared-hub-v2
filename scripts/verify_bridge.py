#!/usr/bin/env python3
"""Verify the shared memory bridge layout and config references."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from promoter import ManifestError, json_dump, load_manifest, resolve_bridge_paths

DEFAULT_WORKSPACES = ["workspace", "workspace-friend-001", "workspace-friend-002"]
DEFAULT_SHARED_SKILLS_MANIFEST = "capabilities/manifests/shared-skills.yaml"



def first_existing_path(candidates: list[Path], fallback: Path) -> Path:
    for item in candidates:
        try:
            if item.expanduser().exists():
                return item.expanduser()
        except OSError:
            continue
    return fallback.expanduser()


def default_hermes_config() -> Path:
    env_config = os.environ.get("HERMES_CONFIG")
    if env_config:
        return Path(env_config)
    hermes_home = Path(os.environ.get("HERMES_HOME", str(Path.home() / ".hermes"))).expanduser()
    return hermes_home / "config.yaml"


def default_openclaw_config() -> Path:
    env_config = os.environ.get("OPENCLAW_CONFIG")
    if env_config:
        return Path(env_config)
    candidates = []
    for var in ("OPENCLAW_HOME", "OPENCLAW_AGENT_DIR"):
        val = os.environ.get(var)
        if val:
            candidates.append(Path(val) / "openclaw.json")
    # portable-audit: allow container fallback path for OpenClaw running inside its standard container.
    candidates.extend([
        Path.home() / ".openclaw" / "openclaw.json",
        Path("/home/node/.openclaw/openclaw.json"),  # portable-audit: allow standard OpenClaw container fallback
    ])
    return first_existing_path(candidates, candidates[0] if candidates else Path.home() / ".openclaw" / "openclaw.json")


def path_exists_safe(path: Path) -> tuple[bool, str | None]:
    try:
        return path.exists(), None
    except OSError as exc:
        return False, f"{type(exc).__name__}: {exc}"

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


def symlink_check(name: str, path: Path, expected_target: Path, allow_missing_target: bool = False) -> dict[str, Any]:
    exists = path.exists()
    is_link = path.is_symlink()
    actual_target = str(path.resolve()) if is_link and exists else None
    expected_resolved = str(expected_target.resolve()) if expected_target.exists() else str(expected_target)
    if is_link and not exists and allow_missing_target:
        try:
            raw_target = os.readlink(path)
        except OSError:
            raw_target = None
        ok = raw_target == os.path.relpath(expected_target, start=path.parent) or raw_target == str(expected_target)
        actual_target = raw_target
    else:
        ok = is_link and exists and actual_target == expected_resolved
    return {
        "name": name,
        "path": str(path),
        "kind": "symlink",
        "exists": exists,
        "is_symlink": is_link,
        "actual_target": actual_target,
        "expected_target": expected_resolved,
        "ok": ok,
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


def normalize_skill_entry(skill: Any) -> dict[str, Any]:
    if isinstance(skill, str):
        value = skill.strip()
        return {
            "id": value,
            "path": value,
            "legacy_string_entry": True,
        }
    if isinstance(skill, dict):
        return dict(skill)
    return {"id": str(skill).strip(), "path": str(skill).strip(), "invalid_type": type(skill).__name__}


def verify_shared_skills_manifest(shared_root: Path, paths: dict[str, Path]) -> dict[str, Any]:
    manifest_path = shared_root / DEFAULT_SHARED_SKILLS_MANIFEST
    record: dict[str, Any] = {
        "path": str(manifest_path),
        "exists": manifest_path.exists(),
        "loaded": False,
        "records": [],
        "warnings": [],
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

    required_fields = []
    if isinstance(payload, dict):
        schema = payload.get("schema")
        if isinstance(schema, dict) and isinstance(schema.get("required_fields"), list):
            required_fields = [str(item) for item in schema["required_fields"]]
    if not required_fields:
        required_fields = ["id", "path", "version", "status", "agents", "owner", "last_reviewed"]

    entries: list[dict[str, Any]] = []
    overall_ok = True
    metadata_ok = True
    for raw_skill in skills:
        skill = normalize_skill_entry(raw_skill)
        skill_path = str(skill.get("path") or skill.get("id") or "").strip()
        skill_id = str(skill.get("id") or skill_path).strip()
        skill_file = paths["capabilities_skills"] / skill_path / "SKILL.md"
        missing_fields = [field for field in required_fields if field not in skill or skill.get(field) in (None, "", [])]
        agents = skill.get("agents")
        agents_ok = isinstance(agents, list) and all(isinstance(agent, str) and agent.strip() for agent in agents)
        item_ok = bool(skill_path) and skill_file.is_file()
        item_metadata_ok = not missing_fields and agents_ok
        overall_ok = overall_ok and item_ok
        metadata_ok = metadata_ok and item_metadata_ok
        if skill.get("legacy_string_entry"):
            record["warnings"].append(f"legacy string shared skill entry: {skill_path}")
        if not item_metadata_ok:
            record["warnings"].append(f"metadata incomplete for shared skill: {skill_id}")
        entries.append(
            {
                "id": skill_id,
                "skill": skill_path,
                "path": str(skill_file),
                "exists": skill_file.exists(),
                "metadata": {
                    "required_fields": required_fields,
                    "missing_fields": missing_fields,
                    "agents_ok": agents_ok,
                    "ok": item_metadata_ok,
                },
                "ok": item_ok,
            }
        )

    record["count"] = len(entries)
    record["records"] = entries
    record["metadata_ok"] = metadata_ok
    record["ok"] = overall_ok
    return record


def _equivalent_existing_paths(path: Path) -> list[str]:
    """Return literal and resolved string forms for the same existing path."""
    candidates = [str(path)]
    try:
        resolved = str(path.resolve())
        if resolved not in candidates:
            candidates.append(resolved)
    except OSError:
        pass
    return candidates


def verify_hermes_config(config_path: Path, paths: dict[str, Path]) -> dict[str, Any]:
    expected_skills_refs = _equivalent_existing_paths(paths["legacy_skills"])
    expected_prefill_refs = _equivalent_existing_paths(paths["prefill_file"])
    exists, exists_error = path_exists_safe(config_path)
    record: dict[str, Any] = {
        "path": str(config_path),
        "exists": exists,
        "expected_refs": {
            "skills": expected_skills_refs,
            "prefill": expected_prefill_refs,
        },
    }
    if exists_error:
        record["ok"] = False
        record["error"] = exists_error
        return record
    if not exists:
        record["ok"] = False
        record["error"] = "config file not found"
        return record
    try:
        text = read_text(config_path)
    except OSError as exc:
        record["ok"] = False
        record["error"] = f"failed to read config: {exc}"
        return record

    record["has_skills_ref"] = any(ref in text for ref in expected_skills_refs)
    record["has_prefill_ref"] = any(ref in text for ref in expected_prefill_refs)
    record["ok"] = record["has_skills_ref"] and record["has_prefill_ref"]
    return record


def verify_openclaw_config(config_path: Path, paths: dict[str, Path]) -> tuple[dict[str, Any], Path]:
    workspace_base = config_path.parent
    expected_extra_dirs = _equivalent_existing_paths(paths["legacy_skills"]) + _equivalent_existing_paths(paths["capabilities_skills"])
    record: dict[str, Any] = {
        "path": str(config_path),
        "exists": path_exists_safe(config_path)[0],
        "expected_extra_dirs": expected_extra_dirs,
    }
    exists, exists_error = path_exists_safe(config_path)
    record["exists"] = exists
    if exists_error:
        record["ok"] = False
        record["error"] = exists_error
        return record, workspace_base
    if not exists:
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
    # 容器场景下 OpenClaw 只能写容器内路径（如 /home/node/.openclaw/shared/skills），
    # 该路径经 docker mount 映射到宿主 shared 根；比较时需同时接受容器前缀的等价路径。
    container_shared_prefix = "/home/node/.openclaw/shared"
    expected_refs = list(expected_extra_dirs)
    for ref in expected_extra_dirs:
        if ref.startswith("/home/") and "/shared" in ref:
            suffix = ref.split("/shared", 1)[1]  # e.g. /skills 或 /capabilities/skills
            expected_refs.append(container_shared_prefix + suffix)
    record["extra_dirs"] = extra_dirs
    record["expected_extra_dirs"] = expected_extra_dirs
    record["has_expected_extra_dir"] = any(ref in extra_dirs for ref in expected_refs)
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


def collect_structure_checks(shared_root: Path, paths: dict[str, Path], portable_only: bool = False) -> dict[str, Any]:
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
        path_check("shared/inbox/future-agent", paths["inbox"] / "future-agent", "dir"),
        path_check("shared/inbox/future-agent/daily", paths["inbox"] / "future-agent" / "daily", "dir"),
        path_check("shared/runtime", paths["runtime"], "dir"),
        path_check("shared/runtime/openclaw/dreams", runtime_openclaw_dreams, "dir"),
        path_check("shared/runtime/future-agent", paths["runtime"] / "future-agent", "dir"),
        path_check("shared/capabilities", paths["capabilities"], "dir"),
        path_check("shared/capabilities/manifests", paths["capabilities"] / "manifests", "dir"),
        path_check("shared/capabilities/manifests/shared-skills.yaml", shared_root / DEFAULT_SHARED_SKILLS_MANIFEST, "file"),
        path_check("shared/memory", legacy_memory, "dir"),
        path_check("shared/prefill/hermes-shared-memory.json", paths["prefill_file"], "file"),
        path_check("shared/prefill/future-agent-shared-memory.json", paths["prefill_file"].parent / "future-agent-shared-memory.json", "file"),
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
    runtime_names = {"shared/runtime", "shared/runtime/openclaw/dreams", "shared/runtime/future-agent"}
    required_path_records = [item for item in path_records if not (portable_only and item["name"] in runtime_names)]
    required_link_records = [item for item in link_records if not (portable_only and item["name"] == "shared/compat/daily/.dreams")]
    overall_ok = all(item["ok"] for item in required_path_records) and all(item["ok"] for item in required_link_records)
    return {
        "paths": path_records,
        "symlinks": link_records,
        "portable_only": portable_only,
        "ok": overall_ok,
    }


def count_markdown_files(path: Path) -> int:
    if not path.exists() or not path.is_dir():
        return 0
    return len([item for item in path.glob("*.md") if item.is_file() and not item.name.startswith(".")])


def directory_size_bytes(path: Path) -> int:
    total = 0
    if not path.exists():
        return total
    if path.is_file():
        try:
            return path.stat().st_size
        except OSError:
            return total
    for item in path.rglob("*"):
        try:
            if item.is_file() and not item.is_symlink():
                total += item.stat().st_size
        except OSError:
            continue
    return total


def count_text_lines(path: Path) -> int:
    if not path.exists() or not path.is_file():
        return 0
    return len(read_text(path).splitlines())


def list_tracked_files(shared_root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=shared_root,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def count_top_level_entries(shared_root: Path) -> int:
    if not shared_root.exists() or not shared_root.is_dir():
        return 0
    return sum(1 for item in shared_root.iterdir() if not item.name.startswith(".git"))


def collect_slimming_metrics(
    shared_root: Path,
    paths: dict[str, Path],
    tracked_paths: list[str] | None = None,
) -> dict[str, Any]:
    tracked = tracked_paths if tracked_paths is not None else list_tracked_files(shared_root)
    tracked_inbox_dreaming = [path for path in tracked if path.startswith("inbox/") and "/dreaming/" in path]
    tracked_inbox_dot_dreams = [path for path in tracked if path.startswith("inbox/") and "/.dreams/" in path]
    tracked_compat_dreaming = [path for path in tracked if path.startswith("compat/daily/dreaming/")]
    tracked_compat_dot_dreams = [path for path in tracked if path.startswith("compat/daily/.dreams/")]
    runtime_size = directory_size_bytes(paths["runtime"])
    memory_path = paths.get("memory_index") or paths.get("memory_file") or paths["curated_memory"] / "MEMORY.md"
    memory_lines = count_text_lines(memory_path)

    skill_reference_records = []
    skills_root = paths["capabilities_skills"]
    if skills_root.exists() and skills_root.is_dir():
        for skill_dir in sorted([item for item in skills_root.iterdir() if item.is_dir() and not item.name.startswith(".")]):
            references_dir = skill_dir / "references"
            reference_count = 0
            if references_dir.exists() and references_dir.is_dir():
                reference_count = sum(1 for item in references_dir.rglob("*") if item.is_file())
            skill_reference_records.append(
                {
                    "skill": skill_dir.name,
                    "references_dir": str(references_dir),
                    "reference_count": reference_count,
                    "ok": reference_count <= 15,
                }
            )

    warnings: list[str] = []
    if memory_lines > 150:
        warnings.append(f"SLIMMING_MEMORY_TOO_LONG: curated/memory/MEMORY.md has {memory_lines} lines > 150")
    if tracked_inbox_dreaming or tracked_inbox_dot_dreams:
        warnings.append(
            "SLIMMING_TRACKED_INBOX_DREAMING: "
            f"{len(tracked_inbox_dreaming) + len(tracked_inbox_dot_dreams)} tracked files"
        )
    if tracked_compat_dreaming or tracked_compat_dot_dreams:
        warnings.append(
            "SLIMMING_TRACKED_COMPAT_DREAMING: "
            f"{len(tracked_compat_dreaming) + len(tracked_compat_dot_dreams)} tracked files"
        )
    if runtime_size > 100 * 1024 * 1024:
        warnings.append(f"SLIMMING_RUNTIME_TOO_LARGE: runtime has {runtime_size} bytes > 104857600")
    for item in skill_reference_records:
        if not item["ok"]:
            warnings.append(
                f"SLIMMING_SKILL_REFERENCES_TOO_MANY: {item['skill']} has {item['reference_count']} references > 15"
            )

    return {
        "policy": "warning-only; no deletion",
        "thresholds": {
            "memory_lines": 150,
            "runtime_bytes": 100 * 1024 * 1024,
            "skill_reference_files_per_skill": 15,
        },
        "top_level_entries": count_top_level_entries(shared_root),
        "top_level_bytes": directory_size_bytes(shared_root),
        "tracked_inbox_dreaming_count": len(tracked_inbox_dreaming) + len(tracked_inbox_dot_dreams),
        "tracked_compat_dreaming_count": len(tracked_compat_dreaming) + len(tracked_compat_dot_dreams),
        "tracked_samples": {
            "inbox_dreaming": (tracked_inbox_dreaming + tracked_inbox_dot_dreams)[:10],
            "compat_dreaming": (tracked_compat_dreaming + tracked_compat_dot_dreams)[:10],
        },
        "runtime_size_bytes": runtime_size,
        "memory_lines": memory_lines,
        "skill_reference_records": skill_reference_records,
        "warnings": warnings,
        "ok": True,
    }


def parse_frontmatter(text: str) -> dict[str, Any]:
    """Parse a minimal YAML-like frontmatter block from a markdown file."""
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    frontmatter = text[4:end]
    try:
        payload = load_manifest_from_text(frontmatter)
    except ManifestError:
        return {}
    return payload if isinstance(payload, dict) else {}


def load_manifest_from_text(text: str) -> Any:
    """Load a minimal YAML payload from text using promoter's parser."""
    from promoter import parse_simple_yaml

    return parse_simple_yaml(text)


def parse_iso_datetime(value: Any) -> datetime | None:
    """Parse ISO datetime values used by fact metadata."""
    if not isinstance(value, str) or not value.strip():
        return None
    normalized = value.strip()
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"
    try:
        return datetime.fromisoformat(normalized)
    except ValueError:
        return None


def collect_fact_governance_checks(facts_dir: Path, now: datetime | None = None) -> dict[str, Any]:
    """Collect warning-only freshness and conflict checks for curated facts."""
    current_time = now or datetime.now().astimezone()
    records: list[dict[str, Any]] = []
    warnings: list[str] = []
    fact_ids: dict[str, str] = {}
    active_groups: dict[str, list[dict[str, Any]]] = {}
    valid_statuses = {"active", "stale", "superseded", "disputed", "deprecated"}
    valid_freshness = {"static", "slow_changing", "operational", "volatile"}

    if not facts_dir.exists() or not facts_dir.is_dir():
        return {"ok": True, "path": str(facts_dir), "records": [], "warnings": []}

    for fact_path in sorted(facts_dir.glob("*.md")):
        metadata = parse_frontmatter(read_text(fact_path))
        if not metadata:
            warnings.append(f"LEGACY_FACT_METADATA_MISSING: {fact_path.name}")
            records.append({"path": str(fact_path), "metadata_present": False, "ok": True})
            continue

        fact_id = str(metadata.get("fact_id") or fact_path.stem).strip()
        status = str(metadata.get("status") or "").strip()
        freshness_class = str(metadata.get("freshness_class") or "").strip()
        scope = str(metadata.get("scope") or "global").strip() or "global"
        subject = str(metadata.get("subject") or "").strip()
        attribute = str(metadata.get("attribute") or "").strip()
        value_summary = str(metadata.get("value_summary") or "").strip()
        conflict = metadata.get("conflict") if isinstance(metadata.get("conflict"), dict) else {}

        if fact_id in fact_ids:
            warnings.append(f"DUPLICATE_FACT_ID: {fact_id}")
        fact_ids[fact_id] = str(fact_path)
        if status not in valid_statuses:
            warnings.append(f"INVALID_FACT_STATUS: {fact_id}")
        if freshness_class and freshness_class not in valid_freshness:
            warnings.append(f"INVALID_FACT_FRESHNESS_CLASS: {fact_id}")
        if not freshness_class:
            warnings.append(f"FACT_FRESHNESS_CLASS_MISSING: {fact_id}")
        if metadata.get("secret_checked") is not True:
            warnings.append(f"FACT_SECRET_CHECK_MISSING: {fact_id}")

        review_due_at = parse_iso_datetime(metadata.get("review_due_at"))
        if metadata.get("review_due_at") and review_due_at is None:
            warnings.append(f"FACT_REVIEW_DUE_AT_INVALID: {fact_id}")
        if review_due_at and review_due_at.tzinfo is None:
            review_due_at = review_due_at.replace(tzinfo=current_time.tzinfo)
        if review_due_at and review_due_at < current_time:
            warnings.append(f"STALE_FACT_REVIEW_NEEDED: {fact_id}")

        if status == "superseded" and not metadata.get("superseded_by"):
            warnings.append(f"SUPERSEDED_FACT_TARGET_MISSING: {fact_id}")
        if status == "disputed" and conflict.get("status") != "disputed":
            warnings.append(f"DISPUTED_FACT_CONFLICT_STATUS_MISMATCH: {fact_id}")
        if conflict.get("status") == "resolved":
            missing = [field for field in ("resolved_by", "resolved_at", "resolution") if not conflict.get(field)]
            if missing:
                warnings.append(f"RESOLVED_CONFLICT_METADATA_MISSING: {fact_id}")

        if status == "active" and subject and attribute:
            group_key = f"{scope}|{subject}|{attribute}"
            active_groups.setdefault(group_key, []).append({"fact_id": fact_id, "value_summary": value_summary})

        records.append({"path": str(fact_path), "fact_id": fact_id, "metadata_present": True, "ok": True})

    for group_key, items in active_groups.items():
        values = {item.get("value_summary", "") for item in items}
        if len(items) > 1 and len(values) > 1:
            warnings.append(f"POSSIBLE_ACTIVE_FACT_CONFLICT: {group_key}")

    known_ids = set(fact_ids)
    for fact_path in sorted(facts_dir.glob("*.md")):
        metadata = parse_frontmatter(read_text(fact_path))
        fact_id = str(metadata.get("fact_id") or fact_path.stem).strip() if metadata else fact_path.stem
        superseded_by = metadata.get("superseded_by") if metadata else None
        if superseded_by and str(superseded_by) not in known_ids:
            warnings.append(f"SUPERSEDED_BY_TARGET_NOT_FOUND: {fact_id}")
        supersedes = metadata.get("supersedes") if metadata else None
        if isinstance(supersedes, list):
            for target in supersedes:
                if str(target) not in known_ids:
                    warnings.append(f"SUPERSEDES_TARGET_NOT_FOUND: {fact_id}->{target}")

    return {"ok": True, "path": str(facts_dir), "records": records, "warnings": warnings}


def collect_governance_checks(shared_root: Path) -> dict[str, Any]:
    docs = [
        "docs/promote-protocol.md",
        "docs/promote-log-template.md",
        "docs/maintenance.md",
    ]
    records = [path_check(name, shared_root / name, "file") for name in docs]
    return {
        "documents": records,
        "ok": all(item["ok"] for item in records),
    }


def collect_promotion_backlog(paths: dict[str, Path]) -> dict[str, Any]:
    inbox_root = paths["inbox"]
    records = []
    total = 0
    for agent_dir in sorted([item for item in inbox_root.iterdir() if item.is_dir() and not item.name.startswith(".")]) if inbox_root.exists() else []:
        daily_dir = agent_dir / "daily"
        count = count_markdown_files(daily_dir)
        total += count
        records.append({
            "agent": agent_dir.name,
            "daily_dir": str(daily_dir),
            "daily_files": count,
            "ok": daily_dir.is_dir(),
        })
    return {
        "total_daily_files": total,
        "records": records,
        "ok": all(item["ok"] for item in records),
    }


def collect_future_agent_readiness(shared_root: Path, paths: dict[str, Path], portable_only: bool = False) -> dict[str, Any]:
    checks = [
        path_check("inbox/future-agent/README.md", paths["inbox"] / "future-agent" / "README.md", "file"),
        path_check("inbox/future-agent/daily", paths["inbox"] / "future-agent" / "daily", "dir"),
        path_check("runtime/future-agent/README.md", paths["runtime"] / "future-agent" / "README.md", "file"),
        path_check("prefill/future-agent-shared-memory.json", shared_root / "prefill" / "future-agent-shared-memory.json", "file"),
    ]
    required = [item for item in checks if not (portable_only and item["name"] == "runtime/future-agent/README.md")]
    return {
        "checks": checks,
        "portable_only": portable_only,
        "ok": all(item["ok"] for item in required),
    }


def collect_runtime_retention_report(paths: dict[str, Path]) -> dict[str, Any]:
    runtime_root = paths["runtime"]
    records = []
    if runtime_root.exists() and runtime_root.is_dir():
        for agent_dir in sorted([item for item in runtime_root.iterdir() if item.is_dir() and not item.name.startswith(".")]):
            records.append({
                "agent": agent_dir.name,
                "path": str(agent_dir),
                "size_bytes": directory_size_bytes(agent_dir),
            })
    return {
        "policy": "report-only; no deletion",
        "records": records,
        "ok": True,
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
        default=None,
        help="Hermes 配置文件；默认 $HERMES_CONFIG 或 $HERMES_HOME/config.yaml 或 ~/.hermes/config.yaml",
    )
    parser.add_argument(
        "--openclaw-config",
        default=None,
        help="OpenClaw 配置文件；默认 $OPENCLAW_CONFIG / $OPENCLAW_HOME/openclaw.json / ~/.openclaw/openclaw.json",
    )
    parser.add_argument(
        "--portable-only",
        action="store_true",
        help="只验证共享中台自身的可迁移结构，不验证当前机器 Hermes/OpenClaw/workspace 配置",
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
    hermes_config = Path(args.hermes_config).expanduser().resolve() if args.hermes_config else default_hermes_config().expanduser().resolve()
    openclaw_config = Path(args.openclaw_config).expanduser().resolve() if args.openclaw_config else default_openclaw_config().expanduser().resolve()
    os.environ.setdefault("SHARED_HUB_ROOT", str(shared_root))
    workspace_names = args.workspace_names or list(DEFAULT_WORKSPACES)

    manifest, manifest_record = verify_manifest(shared_root)
    paths = resolve_bridge_paths(manifest or {}, shared_root)
    structure = collect_structure_checks(shared_root, paths, portable_only=args.portable_only)
    governance = collect_governance_checks(shared_root)
    promotion_backlog = collect_promotion_backlog(paths)
    future_agent_readiness = collect_future_agent_readiness(shared_root, paths, portable_only=args.portable_only)
    runtime_retention = collect_runtime_retention_report(paths)
    slimming_metrics = collect_slimming_metrics(shared_root, paths)
    fact_governance = collect_fact_governance_checks(paths["facts"])
    shared_skills_record = verify_shared_skills_manifest(shared_root, paths)
    if args.portable_only:
        hermes_record = {"ok": True, "skipped": True, "reason": "portable_only"}
        openclaw_record = {"ok": True, "skipped": True, "reason": "portable_only"}
        workspace_record = {"ok": True, "skipped": True, "reason": "portable_only"}
    else:
        hermes_record = verify_hermes_config(hermes_config, paths)
        openclaw_record, inferred_workspace_base = verify_openclaw_config(openclaw_config, paths)
        workspace_base = Path(args.workspace_base).expanduser().resolve() if args.workspace_base else inferred_workspace_base
        workspace_record = verify_workspaces(workspace_base, workspace_names)

    errors: list[str] = []
    warnings: list[str] = []
    if not manifest_record.get("loaded"):
        errors.append("manifest")
    if not structure["ok"]:
        errors.append("structure")
    if not governance["ok"]:
        errors.append("governance")
    if not promotion_backlog["ok"]:
        errors.append("promotion_backlog")
    if not future_agent_readiness["ok"]:
        errors.append("future_agent_readiness")
    if not runtime_retention["ok"]:
        errors.append("runtime_retention")
    if not slimming_metrics["ok"]:
        errors.append("slimming_metrics")
    warnings.extend(slimming_metrics.get("warnings", []))
    if not fact_governance["ok"]:
        errors.append("fact_governance")
    warnings.extend(fact_governance.get("warnings", []))
    if not shared_skills_record.get("ok"):
        errors.append("shared_skills")
    if not shared_skills_record.get("metadata_ok"):
        warnings.append("shared_skills_metadata")
    warnings.extend(shared_skills_record.get("warnings", []))
    if not hermes_record.get("ok"):
        errors.append("hermes_config")
    if not openclaw_record.get("ok"):
        errors.append("openclaw_config")
    if not workspace_record.get("ok"):
        errors.append("workspaces")

    payload = {
        "ok": not errors,
        "mode": "portable_only" if args.portable_only else "full",
        "shared_root": str(shared_root),
        "manifest": manifest_record,
        "structure": structure,
        "governance": governance,
        "promotion_backlog": promotion_backlog,
        "future_agent_readiness": future_agent_readiness,
        "runtime_retention": runtime_retention,
        "slimming_metrics": slimming_metrics,
        "fact_governance": fact_governance,
        "shared_skills_manifest": shared_skills_record,
        "hermes_config": hermes_record,
        "openclaw_config": openclaw_record,
        "workspaces": workspace_record,
        "warnings": warnings,
        "errors": errors,
    }
    print(json_dump(payload))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
