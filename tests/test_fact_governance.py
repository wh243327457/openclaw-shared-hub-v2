#!/usr/bin/env python3
"""Tests for shared v2 fact governance warning checks."""
from __future__ import annotations

import datetime as dt
import importlib.util
import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VERIFY_PATH = ROOT / "scripts" / "verify_bridge.py"
PROMOTER_PATH = ROOT / "scripts" / "promoter.py"

spec = importlib.util.spec_from_file_location("verify_bridge", VERIFY_PATH)
verify_bridge = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.path.insert(0, str(ROOT / "scripts"))
spec.loader.exec_module(verify_bridge)


class FactGovernanceWarningTests(unittest.TestCase):
    """共享 fact 治理 warning-only 检查测试。"""

    maxDiff = None

    def setUp(self) -> None:
        self.tmp = ROOT / "runtime" / "hermes" / "test-fact-governance"
        if self.tmp.exists():
            shutil.rmtree(self.tmp)
        (self.tmp / "curated" / "memory" / "facts").mkdir(parents=True)
        (self.tmp / "curated" / "memory" / "projects").mkdir(parents=True)
        (self.tmp / "runtime").mkdir(parents=True)
        (self.tmp / "compat" / "daily").mkdir(parents=True)
        (self.tmp / "inbox").mkdir(parents=True)
        (self.tmp / "capabilities").mkdir(parents=True)
        (self.tmp / "manifest.yaml").write_text("version: 2\n", encoding="utf-8")
        (self.tmp / "curated" / "memory" / "MEMORY.md").write_text("# Test memory\n", encoding="utf-8")

    def tearDown(self) -> None:
        if self.tmp.exists():
            shutil.rmtree(self.tmp)

    def write_fact(self, name: str, content: str) -> Path:
        path = self.tmp / "curated" / "memory" / "facts" / name
        path.write_text(content, encoding="utf-8")
        return path

    def test_collect_fact_governance_warns_for_stale_and_disputed_facts(self) -> None:
        """过期和 disputed facts 应只产生 warning，不导致 bridge 失败。"""
        self.write_fact(
            "stale.md",
            """---
fact_id: stale-fact
status: active
freshness_class: operational
scope: hermes
subject: config.model
attribute: provider
value_summary: old provider
last_verified_at: 2026-01-01T00:00:00+08:00
review_due_at: 2026-01-02T00:00:00+08:00
secret_checked: true
---
# stale
""",
        )
        self.write_fact(
            "disputed.md",
            """---
fact_id: disputed-fact
status: disputed
freshness_class: operational
scope: hermes
subject: config.model
attribute: provider
value_summary: disputed provider
last_verified_at: 2026-01-01T00:00:00+08:00
review_due_at: 2026-06-01T00:00:00+08:00
secret_checked: true
conflict:
  status: none
---
# disputed
""",
        )

        record = verify_bridge.collect_fact_governance_checks(
            self.tmp / "curated" / "memory" / "facts",
            now=dt.datetime.fromisoformat("2026-05-16T00:00:00+08:00"),
        )

        self.assertTrue(record["ok"])
        self.assertIn("STALE_FACT_REVIEW_NEEDED: stale-fact", record["warnings"])
        self.assertIn("DISPUTED_FACT_CONFLICT_STATUS_MISMATCH: disputed-fact", record["warnings"])

    def test_collect_fact_governance_detects_active_conflict_by_subject_attribute_scope(self) -> None:
        """同 scope/subject/attribute 多个 active 且值不同，应产生冲突 warning。"""
        for name, fact_id, value in [
            ("one.md", "fact-one", "path A"),
            ("two.md", "fact-two", "path B"),
        ]:
            self.write_fact(
                name,
                f"""---
fact_id: {fact_id}
status: active
freshness_class: static
scope: shared-hub
subject: openclaw.inbox
attribute: write_path
value_summary: {value}
last_verified_at: 2026-05-01T00:00:00+08:00
review_due_at: 2026-12-01T00:00:00+08:00
secret_checked: true
---
# {fact_id}
""",
            )

        record = verify_bridge.collect_fact_governance_checks(
            self.tmp / "curated" / "memory" / "facts",
            now=dt.datetime.fromisoformat("2026-05-16T00:00:00+08:00"),
        )

        self.assertTrue(record["ok"])
        self.assertIn("POSSIBLE_ACTIVE_FACT_CONFLICT: shared-hub|openclaw.inbox|write_path", record["warnings"])

    def test_promoter_candidate_scan_includes_governance_suggestions(self) -> None:
        """promoter 候选扫描应输出 freshness/conflict 建议，但不写 curated。"""
        inbox = self.tmp / "inbox" / "hermes" / "daily"
        inbox.mkdir(parents=True)
        (inbox / "2026-05-16.md").write_text(
            "- 已确认 OpenClaw workspace memory 指向 inbox/openclaw/daily，旧记录可能已被替代。\n",
            encoding="utf-8",
        )
        result = subprocess.run(
            [
                sys.executable,
                str(PROMOTER_PATH),
                "--shared-root",
                str(self.tmp),
                "--dry-run",
                "--scan-promote-candidates",
                "--recent-limit",
                "1",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        candidate = payload["promotion_candidates"]["records"][0]["candidates"][0]
        self.assertIn("freshness_suggestion", candidate)
        self.assertIn("possible_conflict", candidate)
        self.assertIn("recommended_state", candidate)


if __name__ == "__main__":
    unittest.main()
