#!/usr/bin/env python3
"""
共享中台系统自检框架。
提供统一的自检入口，支持多种检查类型。
每个 agent 的巡检任务都可以调用这个脚本。

用法：
  python3 system_self_check.py --checks all          # 运行所有检查
  python3 system_self_check.py --checks cron          # 只检查 cron 配置
  python3 system_self_check.py --checks services      # 只检查服务状态
  python3 system_self_check.py --checks memory        # 只检查共享记忆完整性
"""

import json
import os
import sys
import argparse
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path

# 共享中台根目录
SHARED_ROOT = Path("/home/vany/agent/shared")
HERMES_ROOT = Path(os.path.expanduser("~/.hermes"))
TZ = timezone(timedelta(hours=8))


def load_cron_jobs():
    """加载 Hermes cron jobs 配置"""
    jobs_path = HERMES_ROOT / "cron" / "jobs.json"
    if not jobs_path.exists():
        return []
    with open(jobs_path, "r") as f:
        data = json.load(f)
        if isinstance(data, dict) and "jobs" in data:
            return data["jobs"]
        return data


def normalize_schedule(schedule):
    """把 Hermes cron 的字符串或结构化 schedule 统一为可检查文本。"""
    if isinstance(schedule, dict):
        return str(schedule.get("expr") or schedule.get("at") or schedule.get("every") or "")
    return str(schedule or "")


def delivery_error_matches_current_target(deliver, error):
    """判断投递错误是否属于当前目标，忽略改目标后遗留的历史错误。"""
    if not error:
        return False
    if not deliver or deliver in {"local", "origin", "all"}:
        return True
    current_targets = [target.strip() for target in deliver.split(",") if ":" in target]
    return not current_targets or any(target in str(error) for target in current_targets)


def check_cron_config():
    """检查 cron job 配置完整性"""
    jobs = load_cron_jobs()
    now = datetime.now(TZ)
    findings = []

    for job in jobs:
        job_id = job.get("id", job.get("job_id", "?"))
        name = job.get("name", "未命名")
        enabled = job.get("enabled", False)
        schedule = normalize_schedule(job.get("schedule", ""))
        deliver = job.get("deliver", "")
        last_run_at = job.get("last_run_at")
        last_status = job.get("last_status")
        last_delivery_error = job.get("last_delivery_error")
        prompt = job.get("prompt", job.get("prompt_preview", ""))

        if not enabled:
            continue

        # 检查 1: 从未执行
        if last_run_at is None and not schedule.startswith("20"):
            findings.append({
                "level": "⚠️",
                "type": "从未执行",
                "job_id": job_id,
                "name": name,
                "detail": f"schedule={schedule}",
            })

        # 检查 2: 名称明确要求推送时，scheduler 不能只保存到 local。
        # 具体渠道可以是飞书、微信或其他 gateway 平台，不再写死 weixin。
        name_lower = name.lower()
        needs_external_delivery = any(
            kw in name_lower
            for kw in ["推送", "通知", "push"]
        )
        if needs_external_delivery and (not deliver or deliver == "local"):
            findings.append({
                "level": "🔴",
                "type": "缺少外部投递",
                "job_id": job_id,
                "name": name,
                "detail": f"当前 deliver={deliver}",
            })

        # last_status=ok 只代表 agent 执行成功，不代表消息成功送达。
        if delivery_error_matches_current_target(deliver, last_delivery_error):
            findings.append({
                "level": "🔴",
                "type": "上次投递失败",
                "job_id": job_id,
                "name": name,
                "detail": str(last_delivery_error)[:160],
            })

        # 检查 3: 连续失败
        if last_status and last_status not in ("ok", "success"):
            findings.append({
                "level": "🔴",
                "type": "上次执行失败",
                "job_id": job_id,
                "name": name,
                "detail": f"last_status={last_status}",
            })

        # 检查 4: 超 48h 未执行（排除每周/每月任务）
        if last_run_at and "*/" not in schedule:
            try:
                last_dt = datetime.fromisoformat(last_run_at)
                if last_dt.tzinfo is None:
                    last_dt = last_dt.replace(tzinfo=TZ)
                hours_since = (now - last_dt).total_seconds() / 3600
                # 排除每周任务（schedule 格式如 "0 8 * * 1"）
                parts = schedule.split()
                is_periodic = len(parts) == 5 and parts[4] != "*"
                if hours_since > 48 and not is_periodic:
                    findings.append({
                        "level": "⚠️",
                        "type": "超48h未执行",
                        "job_id": job_id,
                        "name": name,
                        "detail": f"上次执行 {last_run_at}",
                    })
            except Exception:
                pass

    return {"check": "cron_config", "findings": findings}


def check_services():
    """检查关键服务状态"""
    findings = []
    
    # 检查 Hermes gateway
    try:
        result = subprocess.run(
            ["pgrep", "-f", "hermes.*gateway"],
            capture_output=True, timeout=5
        )
        if result.returncode != 0:
            findings.append({
                "level": "🔴",
                "type": "服务未运行",
                "name": "Hermes Gateway",
                "detail": "进程未找到",
            })
    except Exception as e:
        findings.append({
            "level": "⚠️",
            "type": "检查失败",
            "name": "Hermes Gateway",
            "detail": str(e),
        })

    # 容器是可选依赖；只有显式配置为必需时才检查。
    expected = [
        name.strip()
        for name in os.getenv("SYSTEM_SELF_CHECK_REQUIRED_CONTAINERS", "").split(",")
        if name.strip()
    ]
    if expected:
        try:
            result = subprocess.run(
                ["docker", "ps", "--format", "{{.Names}}"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode != 0:
                raise RuntimeError(result.stderr.strip() or "docker ps failed")
            containers = result.stdout.strip().splitlines()
            for name in expected:
                if name not in containers:
                    findings.append({
                        "level": "⚠️",
                        "type": "容器未运行",
                        "name": name,
                        "detail": f"未在 docker ps 中找到",
                    })
        except Exception as e:
            findings.append({
                "level": "⚠️",
                "type": "检查失败",
                "name": "Docker 容器",
                "detail": str(e),
            })

    return {"check": "services", "findings": findings}


def check_shared_memory():
    """检查共享记忆完整性"""
    findings = []
    
    # 检查关键文件是否存在
    critical_files = [
        SHARED_ROOT / "manifest.yaml",
        SHARED_ROOT / "AGENTS.md",
        SHARED_ROOT / "curated" / "memory" / "MEMORY.md",
    ]
    
    for fpath in critical_files:
        if not fpath.exists():
            findings.append({
                "level": "🔴",
                "type": "关键文件缺失",
                "name": str(fpath.relative_to(SHARED_ROOT)),
                "detail": "文件不存在",
            })
    
    # 检查 inbox 目录结构
    inbox_agents = ["hermes", "openclaw"]
    for agent in inbox_agents:
        inbox_dir = SHARED_ROOT / "inbox" / agent / "daily"
        if not inbox_dir.exists():
            findings.append({
                "level": "⚠️",
                "type": "目录缺失",
                "name": f"inbox/{agent}/daily/",
                "detail": "目录不存在",
            })

    return {"check": "shared_memory", "findings": findings}


def format_report(results):
    """格式化检查报告"""
    now = datetime.now(TZ).strftime("%Y-%m-%d %H:%M")
    
    total_findings = sum(len(r["findings"]) for r in results)
    
    if total_findings == 0:
        return f"**✅ 系统自检 — {now}**\n\n所有检查通过，无异常。"
    
    lines = [f"**🔍 系统自检报告 — {now}**\n"]
    lines.append(f"共发现 **{total_findings}** 项异常：\n")
    
    for result in results:
        if not result["findings"]:
            continue
        
        check_name = result["check"]
        lines.append(f"### {check_name}")
        lines.append("| 级别 | 类型 | 名称 | 详情 |")
        lines.append("|------|------|------|------|")
        for f in result["findings"]:
            lines.append(f"| {f['level']} | {f['type']} | {f.get('name', '-')} | {f['detail']} |")
        lines.append("")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="共享中台系统自检")
    parser.add_argument(
        "--checks",
        default="all",
        help="要运行的检查项，逗号分隔：all,cron,services,memory"
    )
    args = parser.parse_args()
    
    checks = [c.strip() for c in args.checks.split(",")]
    run_all = "all" in checks
    
    results = []
    
    if run_all or "cron" in checks:
        results.append(check_cron_config())
    
    if run_all or "services" in checks:
        results.append(check_services())
    
    if run_all or "memory" in checks:
        results.append(check_shared_memory())
    
    report = format_report(results)
    print(report)
    
    # 返回码：有异常返回 1，无异常返回 0
    total = sum(len(r["findings"]) for r in results)
    return 1 if total > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
