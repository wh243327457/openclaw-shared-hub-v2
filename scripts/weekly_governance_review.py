#!/usr/bin/env python3
"""Generate a report-only weekly shared-governance review draft.

This script is intentionally conservative: it reads promoter/verify outputs and
writes only runtime draft artifacts. It never writes curated memory, deletes raw
files, or marks candidates as accepted automatically.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any


def json_dump(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)


def iso_week_label(day: date) -> str:
    year, week, _ = day.isocalendar()
    return f"{year}-W{week:02d}"


def parse_date(value: str | None) -> date:
    if not value:
        return datetime.now().astimezone().date()
    return date.fromisoformat(value)


def run_json(command: list[str], cwd: Path) -> tuple[dict[str, Any], str | None]:
    proc = subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)
    if proc.returncode != 0:
        return {}, f"command failed ({proc.returncode}): {' '.join(command)}\nstderr={proc.stderr.strip()}"
    try:
        return json.loads(proc.stdout), None
    except json.JSONDecodeError as exc:
        return {}, f"invalid JSON from {' '.join(command)}: {exc}"


def find_daily_summaries(shared_root: Path, end_day: date) -> list[str]:
    start_day = end_day - timedelta(days=6)
    base = shared_root / "runtime" / "hermes" / "governance" / "daily"
    if not base.exists():
        return []
    summaries: list[str] = []
    for path in sorted(base.glob("*.md")):
        try:
            item_day = date.fromisoformat(path.stem[:10])
        except ValueError:
            continue
        if start_day <= item_day <= end_day:
            summaries.append(str(path.relative_to(shared_root)))
    return summaries


def flatten_candidates(promoter: dict[str, Any]) -> list[dict[str, Any]]:
    records = promoter.get("promotion_candidates", {}).get("records", [])
    flattened: list[dict[str, Any]] = []
    for record in records:
        for candidate in record.get("candidates", []):
            evidence = candidate.get("evidence") or ""
            target = candidate.get("suggested_target") or ""
            decision = candidate.get("decision") or "review"
            possible_conflict = bool(candidate.get("possible_conflict"))
            missing_evidence: list[str] = []
            if decision == "candidate" and target:
                if len(evidence) < 40:
                    missing_evidence.append("来源片段过短，需要回读原文")
                if not candidate.get("reason"):
                    missing_evidence.append("缺少自动分类理由")
                if not target:
                    missing_evidence.append("缺少建议目标")
            if candidate.get("evidence_needed"):
                missing_evidence.extend(str(item) for item in candidate.get("evidence_needed") or [])
            score = 0
            if decision == "candidate":
                score += 40
            elif decision == "review":
                score += 10
            elif decision == "blocked":
                score -= 100
            if target.startswith("curated/memory/projects/"):
                score += 12
            elif target.startswith("curated/memory/facts/"):
                score += 10
            if possible_conflict:
                score -= 18
            if "operational" in str(candidate.get("freshness") or ""):
                score += 4
            if "volatile" in str(candidate.get("freshness") or ""):
                score -= 6
            score += min(len(evidence) // 24, 12)
            if len(missing_evidence) >= 2:
                score -= 4
            if decision == "candidate" and not possible_conflict and score >= 45:
                decision_hint = "本周优先处理"
                summary = f"{target or 'candidate'}：值得本周拍板"
                action_line = "先补证据后直接拍板"
            elif decision == "review":
                decision_hint = "继续观察"
                summary = f"{target or 'candidate'}：证据还不够稳"
                action_line = "继续观察，等下周候选池再确认"
            elif decision == "blocked" or possible_conflict:
                decision_hint = "先脱敏/先解决冲突"
                summary = f"{target or 'candidate'}：先解决安全或冲突问题"
                action_line = "先处理脱敏/冲突，再考虑晋升"
            else:
                decision_hint = "待总控复核"
                summary = f"{target or 'candidate'}：需要总控复核"
                action_line = "总控复核后再决定是否晋升"
            flattened.append(
                {
                    "source": record.get("path"),
                    "agent": record.get("agent"),
                    "line": candidate.get("line"),
                    "decision": decision,
                    "recommended_state": candidate.get("recommended_state"),
                    "target": target,
                    "freshness": candidate.get("freshness_suggestion") or "",
                    "reason": candidate.get("reason") or "",
                    "possible_conflict": possible_conflict,
                    "evidence_needed": candidate.get("evidence_needed") or [],
                    "missing_evidence": missing_evidence,
                    "score": score,
                    "handle_this_week": decision == "candidate" and not possible_conflict and score >= 45,
                    "decision_hint": decision_hint,
                    "summary": summary,
                    "action_line": action_line,
                    "evidence": evidence,
                }
            )
    flattened.sort(key=lambda item: (item["score"], len(item.get("evidence", ""))), reverse=True)
    return flattened


def group_review_buckets(candidates: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)
    seen: set[tuple[str, str, str]] = set()
    for item in candidates:
        key = (str(item.get("target")), str(item.get("evidence"))[:120], str(item.get("source")))
        bucket = "deferred"
        if item.get("decision") == "blocked":
            bucket = "rejected_or_redact_first"
        elif item.get("possible_conflict") or item.get("recommended_state") in {"conflict_detected", "supersede_pending"}:
            bucket = "duplicate_or_disputed"
        elif item.get("decision") == "candidate" and item.get("target"):
            # Report-only suggestion. Human/Hermes must still verify evidence before promotion.
            bucket = "accept_review_needed"
        elif item.get("decision") == "review":
            bucket = "deferred"
        if key in seen and bucket == "accept_review_needed":
            bucket = "duplicate_or_disputed"
        seen.add(key)
        buckets[bucket].append(item)
    return dict(buckets)


def first_n(items: list[dict[str, Any]], n: int) -> list[dict[str, Any]]:
    return items[:n]


def health_from_verify(verify: dict[str, Any], candidates: list[dict[str, Any]]) -> tuple[str, list[str]]:
    reasons: list[str] = []
    if not verify.get("ok", False):
        reasons.append("verify_bridge.py 未通过")
        return "红", reasons
    warnings = verify.get("warnings") or []
    slimming_warnings = (verify.get("slimming_metrics") or {}).get("warnings") or []
    blocked = sum(1 for item in candidates if item.get("decision") == "blocked")
    conflicts = sum(1 for item in candidates if item.get("possible_conflict"))
    if warnings:
        reasons.append(f"verify warnings={len(warnings)}")
    if slimming_warnings:
        reasons.append(f"slimming warnings={len(slimming_warnings)}")
    if blocked:
        reasons.append(f"blocked candidates={blocked}")
    if conflicts:
        reasons.append(f"conflict/supersede candidates={conflicts}")
    if warnings or slimming_warnings or blocked or conflicts:
        return "黄", reasons
    return "绿", ["verify ok 且无新增高风险信号"]


def render_candidate_table(items: list[dict[str, Any]], limit: int) -> list[str]:
    lines = ["| 候选 | 一句话结论 | 一句话动作 | 评分 |", "|---|---|---|---:|"]
    if not items:
        lines.append("| （无） | - | - | - |")
        return lines
    for item in first_n(items, limit):
        summary = str(item.get("summary") or item.get("target") or "-").replace("|", "\|")[:90]
        action = str(item.get("action_line") or item.get("decision_hint") or "继续观察").replace("|", "\|")[:90]
        label = f"`{item.get('target') or '-'}` · `{item.get('source')}`:{item.get('line')}"
        lines.append(f"| {label} | {summary} | {action} | {item.get('score', 0)} |")
    return lines


def render_markdown(
    *,
    week: str,
    generated_at: str,
    shared_root: Path,
    promoter: dict[str, Any],
    verify: dict[str, Any],
    daily_summaries: list[str],
    candidates: list[dict[str, Any]],
    buckets: dict[str, list[dict[str, Any]]],
    errors: list[str],
    limit: int,
) -> str:
    health, health_reasons = health_from_verify(verify, candidates)
    decision_required = "是" if candidates or verify.get("warnings") else "否"
    counts_by_decision = Counter(item.get("decision") for item in candidates)
    counts_by_bucket = {key: len(value) for key, value in buckets.items()}
    stats = promoter.get("stats") or {}
    slimming = verify.get("slimming_metrics") or {}
    promotion_backlog = verify.get("promotion_backlog") or {}
    fact_governance = verify.get("fact_governance") or {}
    lines: list[str] = []
    lines.extend(
        [
            f"# Governance Weekly Review Draft · {week}",
            "",
            "> 自动草稿，只写 runtime，不自动晋升 curated。accepted 仅表示“建议进入人工/总控复核队列”，不是已写入长期记忆。",
            "",
            "## 结论",
            f"- 生成时间：`{generated_at}`",
            f"- 共享根目录：`{shared_root}`",
            f"- 健康度：**{health}**（{'; '.join(health_reasons)}）",
            f"- 是否需要人工决策：**{decision_required}**",
            f"- 本周候选总数：{len(candidates)}",
            f"- 建议分组：{json.dumps(counts_by_bucket, ensure_ascii=False, sort_keys=True)}",
            "",
            "## 指标",
            "| 指标 | 当前 | 阈值/说明 | 处理 |",
            "|---|---:|---|---|",
            f"| facts 文件数 | {stats.get('facts_count', '-')} | 趋势观察 | 仅 promoter 状态统计 |",
            f"| projects 文件数 | {stats.get('projects_count', '-')} | 趋势观察 | 仅 promoter 状态统计 |",
            f"| inbox daily 总数 | {promotion_backlog.get('total_daily_files', '-')} | >30 天需周复盘筛选 | 保留 raw，筛选候选 |",
            f"| MEMORY.md 行数 | {slimming.get('memory_lines', '-')} | <=150 | 超阈值则月度压缩 |",
            f"| runtime 大小 bytes | {slimming.get('runtime_size_bytes', '-')} | <=100MB | 超阈值只列清理候选 |",
            f"| fact governance warnings | {len(fact_governance.get('warnings') or [])} | 0 最佳 | warning-only，周复盘处理 |",
            f"| verify warnings | {len(verify.get('warnings') or [])} | 0 最佳 | 需解释，不阻断草稿 |",
            "",
            "## 最近 daily summaries",
        ]
    )
    if daily_summaries:
        lines.extend(f"- `{path}`" for path in daily_summaries)
    else:
        lines.append("- （未发现最近 7 天 governance daily summary；本草稿直接使用 promoter/verify 扫描结果）")
    lines.extend(
        [
            "",
            "## 候选处理总览",
            f"- promoter files_scanned：{(promoter.get('promotion_candidates') or {}).get('files_scanned', '-')}",
            f"- counts_by_decision：{json.dumps(dict(counts_by_decision), ensure_ascii=False, sort_keys=True)}",
            "",
            "### A. 本周优先拍板 Top 10",
        ]
    )
    prioritized = [item for item in candidates if item.get("decision") == "candidate" and not item.get("possible_conflict")]
    lines.extend(render_candidate_table(prioritized, min(limit, 10)))
    lines.extend(["", "### B. accept_review_needed（可进入总控复核，不自动写入）"])
    lines.extend(render_candidate_table(buckets.get("accept_review_needed", []), min(limit, 5)))
    lines.extend(["", "### B. deferred（证据不足/观察项）"])
    lines.extend(render_candidate_table(buckets.get("deferred", []), limit))
    lines.extend(["", "### C. duplicate_or_disputed（疑似重复/冲突/替代）"])
    lines.extend(render_candidate_table(buckets.get("duplicate_or_disputed", []), limit))
    lines.extend(["", "### D. rejected_or_redact_first（拒绝或先脱敏）"])
    lines.extend(render_candidate_table(buckets.get("rejected_or_redact_first", []), limit))
    lines.extend(
        [
            "",
            "## 风险与后续",
            "- 自动化边界：本脚本只生成草稿；不写 `curated/memory/`，不删除 `inbox/` / `runtime/`。",
            "- 晋升前必须逐条补证据：读取来源文件、确认跨 agent 价值、去重、脱敏、确定目标路径。",
            "- 若需要晋升 shared skill，必须同步 `capabilities/manifests/shared-skills.yaml`。",
            "- 若只是单次任务进度、PR/commit、临时日志，默认保留在 inbox/runtime，不进长期记忆。",
            "",
            "## 需要你决策",
        ]
    )
    top_picks = [item for item in candidates if item.get("decision") == "candidate" and not item.get("possible_conflict")][:5]
    if top_picks:
        lines.append("- A 组里优先处理这 5 条：")
        for item in top_picks:
            lines.append(
                f"  - {item.get('summary')}｜动作：{item.get('action_line')}"
            )
    else:
        lines.append("- 暂无明确可晋升候选；建议继续运行 daily 候选池。")
    if buckets.get("duplicate_or_disputed"):
        lines.append("- C 组是否需要本周处理冲突/替代关系，还是下周继续观察？")
    if errors:
        lines.extend(["", "## 生成错误", *[f"- {error}" for error in errors]])
    lines.append("")
    return "\n".join(lines)


def run(shared_root: Path, review_date: date, recent_limit: int, max_candidates_per_file: int, table_limit: int, dry_run: bool) -> tuple[int, dict[str, Any]]:
    generated_at = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    week = iso_week_label(review_date)
    errors: list[str] = []
    promoter, err = run_json(
        [
            sys.executable,
            str(shared_root / "scripts" / "promoter.py"),
            "--shared-root",
            str(shared_root),
            "--dry-run",
            "--scan-promote-candidates",
            "--recent-limit",
            str(recent_limit),
            "--max-candidates-per-file",
            str(max_candidates_per_file),
        ],
        cwd=shared_root,
    )
    if err:
        errors.append(err)
    verify, err = run_json([sys.executable, str(shared_root / "scripts" / "verify_bridge.py")], cwd=shared_root)
    if err:
        errors.append(err)
    daily_summaries = find_daily_summaries(shared_root, review_date)
    candidates = flatten_candidates(promoter)
    buckets = group_review_buckets(candidates)
    markdown = render_markdown(
        week=week,
        generated_at=generated_at,
        shared_root=shared_root,
        promoter=promoter,
        verify=verify,
        daily_summaries=daily_summaries,
        candidates=candidates,
        buckets=buckets,
        errors=errors,
        limit=table_limit,
    )
    output_path = shared_root / "runtime" / "hermes" / "governance" / "weekly" / f"{week}.md"
    json_path = output_path.with_suffix(".json")
    payload = {
        "ok": not errors,
        "dry_run": dry_run,
        "generated_at": generated_at,
        "week": week,
        "review_date": review_date.isoformat(),
        "output_path": str(output_path),
        "json_path": str(json_path),
        "candidate_count": len(candidates),
        "bucket_counts": {key: len(value) for key, value in buckets.items()},
        "verify_ok": verify.get("ok"),
        "verify_warnings": verify.get("warnings", []),
        "errors": errors,
        "policy": "report-only runtime draft; no curated writes",
    }
    if not dry_run:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(markdown, encoding="utf-8")
        json_path.write_text(json_dump({**payload, "buckets": buckets}), encoding="utf-8")
    return (0 if not errors else 1), payload


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--shared-root", default=str(Path(__file__).resolve().parent.parent))
    parser.add_argument("--date", help="review date, defaults to today; ISO YYYY-MM-DD")
    parser.add_argument("--recent-limit", type=int, default=20)
    parser.add_argument("--max-candidates-per-file", type=int, default=10)
    parser.add_argument("--table-limit", type=int, default=12)
    parser.add_argument("--dry-run", action="store_true", help="do not write runtime draft files")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.recent_limit <= 0:
        parser.error("--recent-limit must be > 0")
    if args.max_candidates_per_file <= 0:
        parser.error("--max-candidates-per-file must be > 0")
    if args.table_limit <= 0:
        parser.error("--table-limit must be > 0")
    code, payload = run(
        Path(args.shared_root).expanduser().resolve(),
        parse_date(args.date),
        args.recent_limit,
        args.max_candidates_per_file,
        args.table_limit,
        args.dry_run,
    )
    print(json_dump(payload))
    return code


if __name__ == "__main__":
    sys.exit(main())
