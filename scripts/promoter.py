#!/usr/bin/env python3
"""Maintain the auto-generated shared bridge status block."""
from __future__ import annotations

import argparse
import ast
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

MARKER_START = "<!-- SHARED-BRIDGE-STATE:START -->"
MARKER_END = "<!-- SHARED-BRIDGE-STATE:END -->"


class ManifestError(RuntimeError):
    """Raised when manifest.yaml is missing or invalid."""


def json_dump(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)


def strip_yaml_comment(line: str) -> str:
    in_single = False
    in_double = False
    result: list[str] = []
    for char in line:
        if char == "'" and not in_double:
            in_single = not in_single
        elif char == '"' and not in_single:
            in_double = not in_double
        elif char == "#" and not in_single and not in_double:
            break
        result.append(char)
    return "".join(result).rstrip()


def parse_scalar(raw_value: str) -> Any:
    value = raw_value.strip()
    lowered = value.lower()
    if lowered in {"null", "none", "~"}:
        return None
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if value.startswith(("'", '"')) and value.endswith(("'", '"')) and len(value) >= 2:
        try:
            return ast.literal_eval(value)
        except Exception:
            return value[1:-1]
    if value.startswith("[") or value.startswith("{"):
        try:
            return ast.literal_eval(value)
        except Exception:
            return value
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        return value


def parse_simple_yaml(text: str) -> Any:
    lines: list[tuple[int, int, str]] = []
    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        if "\t" in raw_line:
            raise ManifestError(f"Tabs are not supported in YAML (line {line_number})")
        cleaned = strip_yaml_comment(raw_line)
        if not cleaned.strip():
            continue
        indent = len(cleaned) - len(cleaned.lstrip(" "))
        lines.append((line_number, indent, cleaned.lstrip(" ")))

    if not lines:
        return {}
    if lines[0][1] != 0:
        raise ManifestError("Top-level YAML indentation must start at column 0")

    index = 0

    def parse_node(expected_indent: int) -> Any:
        nonlocal index
        if index >= len(lines):
            return {}
        _, indent, content = lines[index]
        if indent != expected_indent:
            raise ManifestError(
                f"Unexpected indentation at line {lines[index][0]}: expected {expected_indent}, got {indent}"
            )
        if content.startswith("- "):
            return parse_list(expected_indent)
        return parse_dict(expected_indent)

    def parse_dict(expected_indent: int) -> dict[str, Any]:
        nonlocal index
        payload: dict[str, Any] = {}
        while index < len(lines):
            line_number, indent, content = lines[index]
            if indent < expected_indent:
                break
            if indent > expected_indent:
                raise ManifestError(f"Unexpected indentation at line {line_number}")
            if content.startswith("- "):
                break
            if ":" not in content:
                raise ManifestError(f"Expected 'key: value' on line {line_number}")
            key, raw_value = content.split(":", 1)
            key = key.strip()
            raw_value = raw_value.strip()
            index += 1
            if raw_value:
                payload[key] = parse_scalar(raw_value)
                continue
            if index < len(lines) and lines[index][1] > indent:
                payload[key] = parse_node(lines[index][1])
            else:
                payload[key] = {}
        return payload

    def parse_list(expected_indent: int) -> list[Any]:
        nonlocal index
        payload: list[Any] = []
        while index < len(lines):
            line_number, indent, content = lines[index]
            if indent < expected_indent:
                break
            if indent != expected_indent or not content.startswith("- "):
                break
            item_text = content[2:].strip()
            index += 1
            if not item_text:
                if index < len(lines) and lines[index][1] > indent:
                    payload.append(parse_node(lines[index][1]))
                else:
                    payload.append(None)
                continue
            if ":" in item_text:
                key, raw_value = item_text.split(":", 1)
                item: dict[str, Any] = {}
                key = key.strip()
                raw_value = raw_value.strip()
                if raw_value:
                    item[key] = parse_scalar(raw_value)
                else:
                    item[key] = {}
                if index < len(lines) and lines[index][1] > indent:
                    nested = parse_node(lines[index][1])
                    if isinstance(nested, dict):
                        item.update(nested)
                    else:
                        item["_items"] = nested
                payload.append(item)
                continue
            payload.append(parse_scalar(item_text))
        return payload

    return parse_node(0)


def load_manifest(manifest_path: Path) -> Any:
    if not manifest_path.exists():
        raise ManifestError(f"manifest not found: {manifest_path}")
    try:
        return parse_simple_yaml(manifest_path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ManifestError(f"failed to read manifest: {exc}") from exc


def get_nested(payload: Any, dotted_path: str) -> Any:
    current = payload
    for key in dotted_path.split("."):
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return None
    return current


def coerce_path_value(value: Any) -> str | None:
    if isinstance(value, str) and value.strip():
        return value.strip()
    if isinstance(value, dict):
        for key in ("path", "dir", "file", "target", "location"):
            nested = value.get(key)
            if isinstance(nested, str) and nested.strip():
                return nested.strip()
    return None


def resolve_manifest_relpath(manifest: Any, default: str, *candidates: str) -> Path:
    for candidate in candidates:
        value = coerce_path_value(get_nested(manifest, candidate))
        if value:
            return Path(value)
    return Path(default)


def resolve_bridge_paths(manifest: Any, shared_root: Path) -> dict[str, Path]:
    curated_rel = resolve_manifest_relpath(
        manifest,
        "curated",
        "layers.curated.path",
        "paths.curated",
        "curated",
    )
    curated_memory_rel = resolve_manifest_relpath(
        manifest,
        str(curated_rel / "memory"),
        "layers.curated.children.memory.path",
        "paths.curated_memory",
        "paths.curated.memory",
        "curated_memory",
        "curated.memory",
    )
    facts_rel = resolve_manifest_relpath(
        manifest,
        str(curated_memory_rel / "facts"),
        "layers.curated.children.memory.facts",
        "paths.facts",
        "facts",
    )
    projects_rel = resolve_manifest_relpath(
        manifest,
        str(curated_memory_rel / "projects"),
        "layers.curated.children.memory.projects",
        "paths.projects",
        "projects",
    )
    memory_index_rel = resolve_manifest_relpath(
        manifest,
        str(curated_memory_rel / "MEMORY.md"),
        "layers.curated.children.memory.index",
        "files.memory_index",
        "paths.memory_index",
        "memory_index",
    )
    compat_rel = resolve_manifest_relpath(
        manifest,
        "compat",
        "layers.compat.path",
        "paths.compat",
        "compat",
    )
    compat_daily_rel = resolve_manifest_relpath(
        manifest,
        str(compat_rel / "daily"),
        "layers.compat.children.daily",
        "paths.compat_daily",
        "paths.compat.daily",
        "compat_daily",
        "compat.daily",
    )
    inbox_rel = resolve_manifest_relpath(
        manifest,
        "inbox",
        "layers.inbox.path",
        "paths.inbox",
        "inbox",
    )
    runtime_rel = resolve_manifest_relpath(
        manifest,
        "runtime",
        "layers.runtime.path",
        "paths.runtime",
        "runtime",
    )
    capabilities_rel = resolve_manifest_relpath(
        manifest,
        "capabilities",
        "layers.capabilities.path",
        "paths.capabilities",
        "capabilities",
    )
    capabilities_skills_rel = resolve_manifest_relpath(
        manifest,
        str(capabilities_rel / "skills"),
        "layers.capabilities.children.skills",
        "paths.capabilities_skills",
        "capabilities_skills",
    )
    legacy_memory_rel = resolve_manifest_relpath(
        manifest,
        "memory",
        "layers.legacy_memory.path",
        "paths.legacy_memory",
        "legacy_memory",
    )
    legacy_skills_rel = resolve_manifest_relpath(
        manifest,
        "skills",
        "layers.legacy_skills.path",
        "paths.legacy_skills",
        "legacy_skills",
    )
    prefill_file_rel = resolve_manifest_relpath(
        manifest,
        "prefill/hermes-shared-memory.json",
        "layers.prefill.files.hermes",
        "files.prefill_hermes",
        "paths.prefill_file",
        "prefill_file",
    )

    return {
        "curated": shared_root / curated_rel,
        "curated_memory": shared_root / curated_memory_rel,
        "facts": shared_root / facts_rel,
        "projects": shared_root / projects_rel,
        "memory_index": shared_root / memory_index_rel,
        "compat": shared_root / compat_rel,
        "compat_daily": shared_root / compat_daily_rel,
        "inbox": shared_root / inbox_rel,
        "runtime": shared_root / runtime_rel,
        "capabilities": shared_root / capabilities_rel,
        "capabilities_skills": shared_root / capabilities_skills_rel,
        "legacy_memory": shared_root / legacy_memory_rel,
        "legacy_skills": shared_root / legacy_skills_rel,
        "prefill_file": shared_root / prefill_file_rel,
    }


def is_visible(path: Path, relative_to: Path) -> bool:
    try:
        parts = path.relative_to(relative_to).parts
    except ValueError:
        parts = path.parts
    return not any(part.startswith(".") for part in parts)


def iter_visible_files(root: Path) -> list[Path]:
    if not root.exists() or not root.is_dir():
        return []
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file() and is_visible(path, root)
    )


def count_visible_files(root: Path) -> int:
    return len(iter_visible_files(root))


def daily_rank(path: Path) -> tuple[int, str, float, str]:
    stem = path.stem
    date_candidate = stem[:10]
    try:
        parsed = datetime.fromisoformat(date_candidate)
        return (1, parsed.date().isoformat(), path.stat().st_mtime, path.name)
    except ValueError:
        return (0, "", path.stat().st_mtime, path.name)


def collect_recent_daily(shared_root: Path, compat_daily: Path, inbox_root: Path, limit: int) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []

    for file_path in iter_visible_files(compat_daily):
        candidates.append(
            {
                "path": str(file_path.relative_to(shared_root)),
                "source": "compat/daily",
                "mtime": file_path.stat().st_mtime,
                "rank": daily_rank(file_path),
            }
        )

    if inbox_root.exists() and inbox_root.is_dir():
        for agent_dir in sorted(path for path in inbox_root.iterdir() if path.is_dir() and not path.name.startswith(".")):
            daily_dir = agent_dir / "daily"
            for file_path in iter_visible_files(daily_dir):
                candidates.append(
                    {
                        "path": str(file_path.relative_to(shared_root)),
                        "source": f"inbox/{agent_dir.name}/daily",
                        "agent": agent_dir.name,
                        "mtime": file_path.stat().st_mtime,
                        "rank": daily_rank(file_path),
                    }
                )

    candidates.sort(key=lambda item: (item["rank"][0], item["rank"][1], item["mtime"], item["path"]), reverse=True)
    for item in candidates:
        item.pop("rank", None)
        item.pop("mtime", None)
    return candidates[:limit]


def collect_inbox_counts(inbox_root: Path) -> dict[str, int]:
    counts: dict[str, int] = {}
    if not inbox_root.exists() or not inbox_root.is_dir():
        return counts
    for agent_dir in sorted(path for path in inbox_root.iterdir() if path.is_dir() and not path.name.startswith(".")):
        counts[agent_dir.name] = count_visible_files(agent_dir / "daily")
    return counts


def build_status_block(summary: dict[str, Any]) -> str:
    lines = [
        MARKER_START,
        "## 自动生成的共享桥状态块",
        "",
        f"- 生成时间: `{summary['generated_at']}`",
        f"- 共享根目录: `{summary['shared_root']}`",
        f"- runtime 位置提示: `{summary['runtime_hint']}`",
        f"- facts 文件数: {summary['facts_count']}",
        f"- projects 文件数: {summary['projects_count']}",
        "- 最近 daily 文件:",
    ]

    if summary["recent_daily"]:
        for item in summary["recent_daily"]:
            source = item.get("source", "daily")
            lines.append(f"  - `{item['path']}` ({source})")
    else:
        lines.append("  - （未发现 daily 文件）")

    lines.append("- inbox 各 agent 文件计数:")
    if summary["inbox_counts"]:
        for agent, count in summary["inbox_counts"].items():
            lines.append(f"  - `{agent}`: {count}")
    else:
        lines.append("  - （暂无 inbox agent）")

    lines.extend([MARKER_END, ""])
    return "\n".join(lines)


def default_memory_content() -> str:
    return (
        "# MEMORY.md\n\n"
        "长期记忆主索引。\n\n"
        "你可以在标记块外保留人工维护内容。\n"
    )


def merge_memory_content(existing_text: str, block: str) -> str:
    if not existing_text.strip():
        return default_memory_content().rstrip() + "\n\n" + block

    start = existing_text.find(MARKER_START)
    end = existing_text.find(MARKER_END)
    if start != -1 and end != -1 and start < end:
        end += len(MARKER_END)
        before = existing_text[:start].rstrip()
        after = existing_text[end:].lstrip("\n")
        pieces = [before, block.rstrip()]
        if after:
            pieces.append(after)
        return "\n\n".join(piece for piece in pieces if piece) + "\n"

    return existing_text.rstrip() + "\n\n" + block


def ensure_directories(required_dirs: list[Path], dry_run: bool) -> list[dict[str, Any]]:
    actions: list[dict[str, Any]] = []
    for directory in required_dirs:
        exists_before = directory.exists()
        actions.append(
            {
                "path": str(directory),
                "exists_before": exists_before,
                "action": "keep" if exists_before else "create",
            }
        )
        if not exists_before and not dry_run:
            directory.mkdir(parents=True, exist_ok=True)
    return actions


def run(shared_root: Path, dry_run: bool, recent_limit: int) -> tuple[int, dict[str, Any]]:
    manifest_path = shared_root / "manifest.yaml"
    try:
        manifest = load_manifest(manifest_path)
    except ManifestError as exc:
        return 1, {
            "ok": False,
            "dry_run": dry_run,
            "shared_root": str(shared_root),
            "manifest": str(manifest_path),
            "error": str(exc),
        }

    paths = resolve_bridge_paths(manifest, shared_root)
    required_dirs = [
        paths["curated"],
        paths["curated_memory"],
        paths["facts"],
        paths["projects"],
        paths["compat"],
        paths["compat_daily"],
        paths["inbox"],
        paths["runtime"],
        paths["capabilities"],
    ]
    ensured = ensure_directories(required_dirs, dry_run=dry_run)

    memory_path = paths["memory_index"]
    memory_exists_before = memory_path.exists()
    existing_text = ""
    if memory_exists_before:
        existing_text = memory_path.read_text(encoding="utf-8")

    summary = {
        "generated_at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "shared_root": str(shared_root),
        "runtime_hint": str(paths["runtime"]),
        "facts_count": count_visible_files(paths["facts"]),
        "projects_count": count_visible_files(paths["projects"]),
        "recent_daily": collect_recent_daily(shared_root, paths["compat_daily"], paths["inbox"], recent_limit),
        "inbox_counts": collect_inbox_counts(paths["inbox"]),
    }
    block = build_status_block(summary)
    merged_text = merge_memory_content(existing_text, block)
    changed = merged_text != existing_text

    if not dry_run and changed:
        memory_path.parent.mkdir(parents=True, exist_ok=True)
        memory_path.write_text(merged_text, encoding="utf-8")

    result = {
        "ok": True,
        "dry_run": dry_run,
        "shared_root": str(shared_root),
        "manifest": str(manifest_path),
        "manifest_loaded": isinstance(manifest, dict),
        "ensured": ensured,
        "memory_index": {
            "path": str(memory_path),
            "exists_before": memory_exists_before,
            "changed": changed,
            "write_mode": "dry-run" if dry_run else "write",
        },
        "stats": summary,
    }
    return 0, result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--shared-root",
        default=str(Path(__file__).resolve().parent.parent),
        help="shared 根目录，默认取脚本上级目录",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="只输出将要执行的动作，不写入 MEMORY.md",
    )
    parser.add_argument(
        "--recent-limit",
        type=int,
        default=5,
        help="状态块中保留的最近 daily 文件数量，默认 5",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.recent_limit <= 0:
        parser.error("--recent-limit must be > 0")

    exit_code, payload = run(Path(args.shared_root).expanduser().resolve(), args.dry_run, args.recent_limit)
    print(json_dump(payload))
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
