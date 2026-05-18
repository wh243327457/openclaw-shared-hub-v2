#!/usr/bin/env python3
"""
Minimal MCP server providing read_file, write_file, list_files tools.
Zero external dependencies — stdlib only.

Usage:
    python3 scripts/shared_mcp_server.py
"""
import json
import sys
import os
from pathlib import Path
from typing import Any

SHARED_ROOT = Path(os.environ.get("SHARED_ROOT", str(Path(__file__).resolve().parents[1])))
INBOX_DIR = SHARED_ROOT / "inbox" / "openclaw" / "daily"


def read_file(path: str, offset: int = 1, limit: int = 500) -> dict:
    """Read a text file with optional pagination. Returns dict with content/total_lines."""
    p = Path(path)
    if not p.exists():
        return {"ok": False, "error": f"File not found: {path}"}
    try:
        lines = p.read_text(encoding="utf-8").splitlines()
        total = len(lines)
        start = max(0, offset - 1)
        end = start + limit
        content = "\n".join(lines[start:end])
        return {"ok": True, "content": content, "total_lines": total, "offset": offset, "limit": limit}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def write_file(path: str, content: str) -> dict:
    """Write content to a file. Creates parent dirs if needed."""
    p = Path(path)
    try:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        size = p.stat().st_size
        return {"ok": True, "path": str(p), "bytes": size}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def list_files(path: str, pattern: str = "*") -> dict:
    """List files in a directory matching a glob pattern."""
    p = Path(path)
    if not p.exists() or not p.is_dir():
        return {"ok": False, "error": f"Directory not found: {path}"}
    try:
        files = [str(f.relative_to(p)) for f in p.glob(pattern) if f.is_file()]
        return {"ok": True, "path": str(p), "files": sorted(files), "count": len(files)}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def file_exists(path: str) -> dict:
    """Check if a file exists and return its size."""
    p = Path(path)
    exists = p.exists() and p.is_file()
    return {"ok": exists, "path": str(p), "size": p.stat().st_size if exists else 0}


TOOL_HANDLERS = {
    "read_file": read_file,
    "write_file": write_file,
    "list_files": list_files,
    "file_exists": file_exists,
}


def main() -> None:
    """Read JSON-RPC requests from stdin, write responses to stdout."""
    buf = ""
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            buf += line
            # Try to parse complete JSON object
            try:
                req = json.loads(buf)
                buf = ""
            except json.JSONDecodeError:
                # Not enough data yet, keep buffering
                continue

            method = req.get("method", "")
            req_id = req.get("id")
            params = req.get("params", {})

            # Handle MCP protocol messages
            if method == "initialize":
                result = {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "shared-fs", "version": "1.0.0"},
                }
                resp = {"jsonrpc": "2.0", "id": req_id, "result": result}
                print(json.dumps(resp), flush=True)
                continue

            if method == "notifications/initialized":
                # Client ready, no response needed
                continue

            if method == "tools/list":
                tools = [
                    {
                        "name": "read_file",
                        "description": "Read a text file with optional pagination (offset/limit). Returns dict with content, total_lines.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "path": {"type": "string"},
                                "offset": {"type": "integer", "default": 1},
                                "limit": {"type": "integer", "default": 500},
                            },
                            "required": ["path"],
                        },
                    },
                    {
                        "name": "write_file",
                        "description": "Write content to a file. Creates parent directories if needed. Returns dict with ok/path/bytes.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "path": {"type": "string"},
                                "content": {"type": "string"},
                            },
                            "required": ["path", "content"],
                        },
                    },
                    {
                        "name": "list_files",
                        "description": "List files in a directory matching a glob pattern.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "path": {"type": "string"},
                                "pattern": {"type": "string", "default": "*"},
                            },
                            "required": ["path"],
                        },
                    },
                    {
                        "name": "file_exists",
                        "description": "Check if a file exists and return its size.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "path": {"type": "string"},
                            },
                            "required": ["path"],
                        },
                    },
                ]
                resp = {"jsonrpc": "2.0", "id": req_id, "result": {"tools": tools}}
                print(json.dumps(resp), flush=True)
                continue

            if method == "tools/call":
                tool_name = params.get("name", "")
                arguments = params.get("arguments", {}) or {}

                if tool_name in TOOL_HANDLERS:
                    try:
                        result = TOOL_HANDLERS[tool_name](**arguments)
                        content = [
                            {
                                "type": "text",
                                "text": json.dumps(result, ensure_ascii=False),
                            }
                        ]
                        resp = {
                            "jsonrpc": "2.0",
                            "id": req_id,
                            "result": {
                                "content": content,
                                "isError": result.get("ok") is False,
                            },
                        }
                    except Exception as e:
                        resp = {
                            "jsonrpc": "2.0",
                            "id": req_id,
                            "result": {
                                "content": [{"type": "text", "text": json.dumps({"ok": False, "error": str(e)})}],
                                "isError": True,
                            },
                        }
                else:
                    resp = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"},
                    }
                print(json.dumps(resp), flush=True)
                continue

            # Unknown method
            resp = {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Method not found: {method}"},
            }
            print(json.dumps(resp), flush=True)

        except Exception as e:
            try:
                err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32603, "message": str(e)}}
                print(json.dumps(err), flush=True)
            except Exception:
                pass


if __name__ == "__main__":
    main()
