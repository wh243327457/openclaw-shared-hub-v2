#!/usr/bin/env python3
"""Audit shared hub files for non-portable host path references.

The audit is intentionally stricter for runnable files than for historical
references. Runnable code and prefill must not hardcode machine-specific roots.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from resolve_shared_root import resolve  # noqa: E402

PATTERNS = [
    re.compile(r"/home/vany(?:/|\b)"),  # portable-audit: allow scanner pattern
    re.compile(r"/home/ubuntu(?:/|\b)"),  # portable-audit: allow scanner pattern
    re.compile(r"/root/\.hermes(?:/|\b)"),
    re.compile(r"/home/node/\.openclaw(?:/|\b)"),
    re.compile(r"[A-Za-z]:[\\/]Users[\\/]"),
]

TEXT_SUFFIXES = {".py", ".sh", ".bash", ".md", ".json", ".yaml", ".yml", ".txt", ".toml"}
RUNNABLE_PREFIXES = ("scripts/",)
RUNNABLE_PARTS = ("/scripts/",)
PREFILL_PREFIX = "prefill/"
DOC_PREFIXES = ("README.md", "AGENTS.md", "docs/", "curated/memory/", "capabilities/skills/")
ALLOW_MARKERS = ("portable-audit: allow", "host_examples", "legacy example", "示例", "容器")


def git_files(root: Path) -> list[str]:
    result = subprocess.run(["git", "ls-files"], cwd=root, text=True, capture_output=True, check=False)
    if result.returncode == 0:
        return [line.strip() for line in result.stdout.splitlines() if line.strip()]
    return [str(p.relative_to(root)) for p in root.rglob("*") if p.is_file() and ".git" not in p.parts]


def severity_for(path: str, line: str) -> str:
    if any(marker in line for marker in ALLOW_MARKERS):
        return "info"
    if path.startswith(RUNNABLE_PREFIXES) or any(part in path for part in RUNNABLE_PARTS):
        return "error"
    if path.startswith(PREFILL_PREFIX):
        return "error"
    if path in {"README.md", "AGENTS.md", "manifest.yaml"}:
        return "warning"
    if path.startswith(DOC_PREFIXES):
        return "warning"
    return "info"


def main() -> int:
    ap = argparse.ArgumentParser(description="Audit shared hub path portability.")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--fail-on-warning", action="store_true")
    args = ap.parse_args()

    root, _ = resolve()
    findings: list[dict[str, Any]] = []
    for rel in git_files(root):
        path = root / rel
        if not path.is_file() or path.suffix not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for lineno, line in enumerate(text.splitlines(), start=1):
            for pat in PATTERNS:
                if pat.search(line):
                    findings.append({
                        "path": rel,
                        "line": lineno,
                        "match": pat.pattern,
                        "severity": severity_for(rel, line),
                        "text": line.strip()[:240],
                    })
                    break

    errors = [f for f in findings if f["severity"] == "error"]
    warnings = [f for f in findings if f["severity"] == "warning"]
    payload = {
        "ok": not errors and (not warnings or not args.fail_on_warning),
        "shared_root": str(root),
        "summary": {"errors": len(errors), "warnings": len(warnings), "info": len([f for f in findings if f["severity"] == "info"])},
        "findings": findings,
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"shared_root: {root}")
        print(f"errors={len(errors)} warnings={len(warnings)} info={payload['summary']['info']}")
        for f in findings[:200]:
            print(f"{f['severity'].upper()} {f['path']}:{f['line']}: {f['text']}")
        if len(findings) > 200:
            print(f"... truncated {len(findings)-200} findings")
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
