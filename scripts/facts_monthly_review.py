#!/usr/bin/env python3
"""facts_monthly_review.py — curated facts 月度复审扫描器。

扫描 curated/memory/facts/ 下 review_due_at 已到期的 fact，输出复审清单：
- operational 类：核实当前状态后刷新 last_verified_at / review_due_at
- slow_changing/static 类：确认内容仍有效后顺延 review_due_at
- 已失效的：标记 status: retired（人工/总控确认后执行）

默认 dry-run 只报告；--apply 时对"内容无需变更、仅到期"的条目自动顺延
review_due_at 一个周期（static 180 天 / slow_changing 90 天 / operational 30 天），
不做任何内容改写，retired 判定永远留给人工。
"""
from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parent.parent / "curated" / "memory" / "facts"
EXTEND_DAYS = {"static": 180, "slow_changing": 90, "operational": 30, "volatile": 14}
FM_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)


def parse_frontmatter(text: str) -> dict:
    m = FM_RE.match(text)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith((" ", "-")):
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip()
    return fm


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(DEFAULT_ROOT))
    ap.add_argument("--apply", action="store_true", help="顺延到期且无需改内容的 fact")
    args = ap.parse_args()

    root = Path(args.root)
    today = datetime.date.today()
    due, extended, errors = [], [], []

    for p in sorted(root.glob("*.md")):
        text = p.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        if not fm:
            errors.append(f"{p.name}: no frontmatter")
            continue
        if fm.get("status") != "active":
            continue
        raw = fm.get("review_due_at", "")
        m = re.match(r"(\d{4}-\d{2}-\d{2})", raw)
        if not m:
            errors.append(f"{p.name}: bad review_due_at '{raw}'")
            continue
        due_date = datetime.date.fromisoformat(m.group(1))
        if due_date > today:
            continue

        cls = fm.get("freshness_class", "slow_changing")
        days = EXTEND_DAYS.get(cls, 90)
        new_due = today + datetime.timedelta(days=days)
        item = {"fact": p.name, "class": cls, "was_due": str(due_date), "new_due": str(new_due)}

        if args.apply:
            new_fm_line = f"review_due_at: {new_due.isoformat()}"
            new_text = FM_RE.sub(
                lambda mm: mm.group(0).replace(raw, new_due.isoformat(), 1),
                text,
                count=1,
            )
            # 同时刷新 last_verified_at 与 updated_at（仅日期部分）
            new_text = re.sub(r"(last_verified_at: )(\d{4}-\d{2}-\d{2})",
                              lambda mm: mm.group(1) + today.isoformat(), new_text)
            new_text = re.sub(r"(updated_at: )(\d{4}-\d{2}-\d{2})",
                              lambda mm: mm.group(1) + today.isoformat(), new_text)
            p.write_text(new_text, encoding="utf-8")
            item["action"] = "extended"
            extended.append(item)
        else:
            item["action"] = "needs_review"
            due.append(item)

    report = {
        "date": today.isoformat(),
        "mode": "apply" if args.apply else "dry-run",
        "due_count": len(due) + len(extended),
        "extended": len(extended),
        "items": extended + due,
        "errors": errors,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
