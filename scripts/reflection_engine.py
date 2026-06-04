#!/usr/bin/env python3
"""通用自我反思引擎。

供所有自动化系统共用的反思/进化模块：
- GitHub 热门项目学习
- 读书计划
- 日常巡检
- 任何需要"执行→反馈→反思→进化"闭环的系统

用法：
    from reflection_engine import ReflectionEngine

    engine = ReflectionEngine('github-learning', shared_root)
    engine.record_feedback(score=23, max_score=23, issues=[], strengths=['源码精读到位'])
    suggestions = engine.reflect()
    engine.save()
    # suggestions 自动写入 evolution-suggestions.json，供明日指令读取
"""

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

TZ = timezone(timedelta(hours=8))


@dataclass
class FeedbackRecord:
    """一条反馈记录。"""
    date: str
    score: float
    max_score: float
    issues: list[str] = field(default_factory=list)
    strengths: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)  # 领域特有数据

    @property
    def ratio(self) -> float:
        return self.score / self.max_score if self.max_score > 0 else 0


@dataclass
class Suggestion:
    """一条进化建议。"""
    type: str           # fix_issue / trend_alert / trend_positive / recurring / strategy
    priority: str       # high / medium / low
    message: str
    auto_action: str    # add_to_instruction / escalate / increase_challenge / log
    domain: str = ''
    issue: str = ''

    def to_dict(self) -> dict:
        return asdict(self)


class ReflectionEngine:
    """通用自我反思引擎。

    生命周期：
        1. record_feedback() — 每次执行后记录反馈
        2. reflect() — 分析历史，生成进化建议
        3. save() — 持久化反馈历史 + 进化建议
        4. (可选) get_instruction_enhancement() — 生成明日指令强化文本

    文件布局：
        runtime/<agent>/<domain>/feedback-history.json  — 反馈历史
        runtime/<agent>/<domain>/evolution-suggestions.json — 最新建议
    """

    def __init__(
        self,
        domain: str,
        shared_root: Path,
        agent: str = 'hermes',
        history_window: int = 14,      # 分析最近 N 条
        recurring_threshold: int = 3,  # 出现 N 次算"反复"
        declining_window: int = 3,     # 用最近 N 条判断趋势
    ):
        self.domain = domain
        self.agent = agent
        self.shared_root = Path(shared_root)
        self.history_window = history_window
        self.recurring_threshold = recurring_threshold
        self.declining_window = declining_window

        self._runtime_dir = self.shared_root / 'runtime' / agent / domain
        self._runtime_dir.mkdir(parents=True, exist_ok=True)

        self._feedback_file = self._runtime_dir / 'feedback-history.json'
        self._suggestions_file = self._runtime_dir / 'evolution-suggestions.json'

        self._history: list[FeedbackRecord] = self._load_history()
        self._current: Optional[FeedbackRecord] = None
        self._suggestions: list[Suggestion] = []

    def _load_history(self) -> list[FeedbackRecord]:
        """加载反馈历史。"""
        if not self._feedback_file.exists():
            return []
        try:
            data = json.loads(self._feedback_file.read_text(encoding='utf-8'))
            return [FeedbackRecord(**r) for r in data.get('records', [])]
        except Exception:
            return []

    # ── 1. 记录反馈 ──────────────────────────────────────────

    def record_feedback(
        self,
        score: float,
        max_score: float,
        issues: Optional[list[str]] = None,
        strengths: Optional[list[str]] = None,
        metadata: Optional[dict] = None,
    ) -> None:
        """记录本次执行的反馈。"""
        self._current = FeedbackRecord(
            date=datetime.now(TZ).date().isoformat(),
            score=score,
            max_score=max_score,
            issues=issues or [],
            strengths=strengths or [],
            metadata=metadata or {},
        )

    # ── 2. 反思分析 ──────────────────────────────────────────

    def reflect(self) -> list[Suggestion]:
        """分析历史反馈，生成进化建议。

        返回建议列表，同时存入 self._suggestions。
        """
        self._suggestions = []

        if self._current:
            self._analyze_current_issues()
            self._analyze_trend()
            self._analyze_recurring()
            self._analyze_strategy()

        # 即使没有当前反馈，也分析历史趋势
        if not self._current and self._history:
            self._analyze_trend()
            self._analyze_recurring()

        return self._suggestions

    def _analyze_current_issues(self) -> None:
        """基于本次扣分项生成建议。"""
        for issue in self._current.issues:
            if not issue or issue == '无':
                continue
            self._suggestions.append(Suggestion(
                type='fix_issue',
                priority='high',
                message=f'本次问题需强化：{issue}',
                auto_action='add_to_instruction',
                domain=self.domain,
                issue=issue,
            ))

    def _analyze_trend(self) -> None:
        """分析分数趋势。"""
        all_records = self._history.copy()
        if self._current:
            all_records.append(self._current)

        if len(all_records) < self.declining_window:
            return

        recent = all_records[-self.declining_window:]
        scores = [r.ratio for r in recent]
        avg = sum(scores) / len(scores)

        # 看最后一条 vs 前面
        if scores[-1] < scores[0] - 0.05:  # 下降超过 5%
            self._suggestions.append(Suggestion(
                type='trend_alert',
                priority='high',
                message=f'最近 {self.declining_window} 次平均 {avg:.0%}，呈下降趋势。需要检查执行质量或调整策略。',
                auto_action='escalate',
                domain=self.domain,
            ))
        elif scores[-1] > scores[0] + 0.05 and avg >= 0.85:
            self._suggestions.append(Suggestion(
                type='trend_positive',
                priority='medium',
                message=f'平均 {avg:.0%}，持续进步。可以尝试更高难度。',
                auto_action='increase_challenge',
                domain=self.domain,
            ))

    def _analyze_recurring(self) -> None:
        """统计高频重复问题。"""
        issue_counts: dict[str, int] = {}
        recent = self._history[-7:]
        if self._current:
            recent = recent + [self._current]

        for record in recent:
            for issue in record.issues:
                if issue and issue != '无':
                    issue_counts[issue] = issue_counts.get(issue, 0) + 1

        for issue, count in issue_counts.items():
            if count >= self.recurring_threshold:
                self._suggestions.append(Suggestion(
                    type='recurring',
                    priority='high',
                    message=f'「{issue}」最近出现 {count} 次，是系统性问题。需要结构性改进。',
                    auto_action='modify_template',
                    domain=self.domain,
                    issue=issue,
                ))

    def _analyze_strategy(self) -> None:
        """策略级反思。"""
        if not self._current:
            return

        if self._current.ratio >= 0.85:
            self._suggestions.append(Suggestion(
                type='strategy',
                priority='low',
                message='本次达标。反思：哪些投入产出比最高？哪些可以优化或跳过？',
                auto_action='log',
                domain=self.domain,
            ))
        elif self._current.ratio < 0.5:
            self._suggestions.append(Suggestion(
                type='strategy',
                priority='high',
                message=f'得分率仅 {self._current.ratio:.0%}，需要重新评估执行策略。',
                auto_action='escalate',
                domain=self.domain,
            ))

    # ── 3. 持久化 ────────────────────────────────────────────

    def save(self) -> None:
        """保存反馈历史和进化建议。"""
        # 追加当前反馈到历史
        if self._current:
            self._history.append(self._current)
            # 只保留最近 N 条
            self._history = self._history[-self.history_window:]

        # 保存反馈历史
        history_data = {
            'domain': self.domain,
            'updated': datetime.now(TZ).isoformat(),
            'records': [asdict(r) for r in self._history],
        }
        self._feedback_file.write_text(
            json.dumps(history_data, indent=2, ensure_ascii=False),
            encoding='utf-8',
        )

        # 保存进化建议
        suggestions_data = {
            'domain': self.domain,
            'date': datetime.now(TZ).date().isoformat(),
            'generated_at': datetime.now(TZ).isoformat(),
            'suggestions': [s.to_dict() for s in self._suggestions],
            'summary': self._build_summary(),
        }
        self._suggestions_file.write_text(
            json.dumps(suggestions_data, indent=2, ensure_ascii=False),
            encoding='utf-8',
        )

    def _build_summary(self) -> dict:
        """构建摘要统计。"""
        all_records = self._history.copy()
        if self._current:
            all_records.append(self._current)

        if not all_records:
            return {'total_runs': 0}

        scores = [r.ratio for r in all_records]
        return {
            'total_runs': len(all_records),
            'avg_score': round(sum(scores) / len(scores) * 100, 1),
            'latest_score': round(scores[-1] * 100, 1),
            'best_score': round(max(scores) * 100, 1),
            'worst_score': round(min(scores) * 100, 1),
            'high_priority_suggestions': len([s for s in self._suggestions if s.priority == 'high']),
        }

    # ── 4. 指令增强 ──────────────────────────────────────────

    def get_instruction_enhancement(self) -> str:
        """将进化建议转为明日指令的强化文本。

        调用方在生成 cron prompt 时嵌入此文本。
        """
        if not self._suggestions:
            return ''

        high = [s for s in self._suggestions if s.priority == 'high']
        medium = [s for s in self._suggestions if s.priority == 'medium']

        if not high and not medium:
            return ''

        lines = [f'### 🧬 自我进化建议（{self.domain} 反思）']

        if high:
            lines.append('')
            lines.append('**必须改进：**')
            for s in high:
                lines.append(f'- {s.message}')

        if medium:
            lines.append('')
            lines.append('**可以尝试：**')
            for s in medium:
                lines.append(f'- {s.message}')

        return '\n'.join(lines)

    # ── 5. 读取外部建议（供其他系统消费） ─────────────────────

    @staticmethod
    def read_suggestions(shared_root: Path, domain: str, agent: str = 'hermes') -> list[dict]:
        """读取指定领域的最新进化建议。"""
        path = shared_root / 'runtime' / agent / domain / 'evolution-suggestions.json'
        if not path.exists():
            return []
        try:
            data = json.loads(path.read_text(encoding='utf-8'))
            return data.get('suggestions', [])
        except Exception:
            return []

    @staticmethod
    def read_all_suggestions(shared_root: Path, agent: str = 'hermes') -> dict[str, list[dict]]:
        """读取所有领域的进化建议，返回 {domain: suggestions}。"""
        runtime_dir = shared_root / 'runtime' / agent
        if not runtime_dir.exists():
            return {}

        result = {}
        for domain_dir in runtime_dir.iterdir():
            if not domain_dir.is_dir():
                continue
            suggestions_file = domain_dir / 'evolution-suggestions.json'
            if suggestions_file.exists():
                try:
                    data = json.loads(suggestions_file.read_text(encoding='utf-8'))
                    result[domain_dir.name] = data.get('suggestions', [])
                except Exception:
                    pass
        return result

    # ── 6. 跨领域汇总报告 ────────────────────────────────────

    @staticmethod
    def cross_domain_summary(shared_root: Path, agent: str = 'hermes') -> str:
        """生成跨领域的反思汇总报告。"""
        all_suggestions = ReflectionEngine.read_all_suggestions(shared_root, agent)

        if not all_suggestions:
            return '暂无进化建议。'

        lines = ['## 🔄 自我进化汇总']
        lines.append('')

        total_high = 0
        for domain, suggestions in all_suggestions.items():
            high = [s for s in suggestions if s.get('priority') == 'high']
            medium = [s for s in suggestions if s.get('priority') == 'medium']
            total_high += len(high)

            status = '⚠️' if high else '✅'
            lines.append(f'### {status} {domain}')

            if high:
                for s in high:
                    lines.append(f'  - 🔴 {s["message"]}')
            if medium:
                for s in medium:
                    lines.append(f'  - 🟡 {s["message"]}')
            if not high and not medium:
                lines.append('  - 状态良好，无需调整')
            lines.append('')

        if total_high > 0:
            lines.insert(1, f'**⚡ {total_high} 项高优先级建议需要处理**')
        else:
            lines.insert(1, '✅ 所有领域运行正常')

        return '\n'.join(lines)


# ── CLI 入口 ────────────────────────────────────────────────

def main():
    import argparse

    parser = argparse.ArgumentParser(description='通用自我反思引擎')
    parser.add_argument('action', choices=['reflect', 'summary', 'dashboard'],
                        help='reflect: 分析指定领域; summary: 跨领域汇总; dashboard: 完整面板')
    parser.add_argument('--domain', help='领域名 (github-learning / reading-plan / daily-patrol)')
    parser.add_argument('--agent', default='hermes', help='agent 名')
    parser.add_argument('--shared-root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--score', type=float, help='本次得分')
    parser.add_argument('--max-score', type=float, default=100, help='满分')
    parser.add_argument('--issues', nargs='*', default=[], help='问题列表')
    parser.add_argument('--strengths', nargs='*', default=[], help='优势列表')
    args = parser.parse_args()

    if args.action == 'summary':
        print(ReflectionEngine.cross_domain_summary(args.shared_root, args.agent))
        return

    if args.action == 'dashboard':
        all_suggestions = ReflectionEngine.read_all_suggestions(args.shared_root, args.agent)
        print(ReflectionEngine.cross_domain_summary(args.shared_root, args.agent))
        print()
        for domain in all_suggestions:
            engine = ReflectionEngine(domain, args.shared_root, args.agent)
            summary = engine._build_summary()
            print(f'--- {domain} ---')
            print(f'  总运行: {summary.get("total_runs", 0)} | '
                  f'平均: {summary.get("avg_score", 0)}% | '
                  f'最新: {summary.get("latest_score", 0)}%')
        return

    if not args.domain:
        parser.error('--domain is required for reflect action')

    if args.action == 'reflect':
        engine = ReflectionEngine(args.domain, args.shared_root, args.agent)
        if args.score is not None:
            engine.record_feedback(
                score=args.score,
                max_score=args.max_score,
                issues=args.issues,
                strengths=args.strengths,
            )
        suggestions = engine.reflect()
        engine.save()

        print(f'✅ {args.domain} 反思完成')
        print(f'   建议: {len(suggestions)} 条')
        for s in suggestions:
            print(f'   [{s.priority}] {s.message}')

        enhancement = engine.get_instruction_enhancement()
        if enhancement:
            print()
            print('--- 明日指令增强 ---')
            print(enhancement)


if __name__ == '__main__':
    main()
