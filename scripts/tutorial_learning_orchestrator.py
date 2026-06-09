#!/usr/bin/env python3
"""教程学习闭环编排器。

搜索 HN + GitHub 的高质量技术教程，筛选、深读、产出教程学习卡。

流程：
1. 搜索 HN + GitHub trending 教程候选
2. 初筛（质量 + 时效 + 匹配度）
3. 生成教程学习卡（Hermes 直接执行，不依赖 OpenClaw）
4. 审计产出
5. 成功 → 写入知识库 + 推送微信
"""

import argparse
import json
import re
import subprocess
import sys
import urllib.request
import urllib.parse
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

# 常量
DEFAULT_SHARED_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_KNOWLEDGE_BASE = Path('/mnt/d/system/selfSystem/03-学习/技术实践')
TZ = timezone(timedelta(hours=8))
PASS_SCORE = 12
HN_SEARCH_URL = 'https://hn.algolia.com/api/v1/search'
GITHUB_SEARCH_URL = 'https://api.github.com/search/repositories'

# 用户兴趣关键词
INTEREST_KEYWORDS = [
    'AI agent', 'LLM', 'coding agent', 'tool calling', 'guardrails',
    'MCP', 'model context protocol', 'Claude Code', 'self-hosted',
    'DevOps', 'automation', 'state machine', 'fine-tuning', 'RAG',
]

# 排除关键词
EXCLUDE_KEYWORDS = [
    'hiring', 'job', 'salary', 'crypto', 'blockchain', 'NFT',
]


def today_cst() -> str:
    return datetime.now(TZ).date().isoformat()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--date', default=today_cst(), help='目标日期')
    parser.add_argument('--shared-root', type=Path, default=DEFAULT_SHARED_ROOT)
    parser.add_argument('--knowledge-base', type=Path, default=DEFAULT_KNOWLEDGE_BASE)
    parser.add_argument('--min-stars', type=int, default=100, help='GitHub 最低 star 数')
    parser.add_argument('--min-hn-points', type=int, default=30, help='HN 最低 points')
    parser.add_argument('--top-n', type=int, default=5, help='筛选候选数')
    parser.add_argument('--dry-run', action='store_true')
    return parser.parse_args()


def log(message: str) -> None:
    ts = datetime.now(TZ).strftime('%H:%M:%S')
    print(f'[{ts}] {message}')


def fetch_json(url: str, headers: dict | None = None) -> dict | None:
    """安全 fetch JSON。"""
    try:
        req = urllib.request.Request(url, headers=headers or {})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        log(f'  ⚠️ fetch 失败: {url[:80]}... → {e}')
        return None


# ─── Step 1: 搜索候选 ──────────────────────────────

def search_hn_tutorials(min_points: int, limit: int = 20) -> list[dict]:
    """搜索 HN 高赞教程帖。"""
    log('Step 1a: 搜索 HN 教程候选...')
    candidates = []

    queries = [
        'AI agent tutorial',
        'LLM engineering guide',
        'coding agent best practices',
        'self hosted tools',
        'MCP model context protocol',
    ]

    seen_urls: set[str] = set()
    for query in queries:
        params = urllib.parse.urlencode({
            'query': query,
            'tags': 'story',
            'hitsPerPage': 10,
        })
        data = fetch_json(f'{HN_SEARCH_URL}?{params}')
        if not data:
            continue
        for hit in data.get('hits', []):
            url = hit.get('url', '')
            points = hit.get('points', 0)
            title = hit.get('title', '')
            date = hit.get('created_at', '')[:10]

            if not url or url in seen_urls:
                continue
            if points < min_points:
                continue
            if any(kw.lower() in title.lower() for kw in EXCLUDE_KEYWORDS):
                continue

            seen_urls.add(url)
            candidates.append({
                'source': 'HN',
                'title': title,
                'url': url,
                'points': points,
                'comments': hit.get('num_comments', 0),
                'date': date,
            })

    candidates.sort(key=lambda x: x['points'], reverse=True)
    log(f'  找到 {len(candidates)} 个 HN 候选')
    return candidates


def search_github_tutorials(min_stars: int, limit: int = 15) -> list[dict]:
    """搜索 GitHub 教程/学习类 repo。"""
    log('Step 1b: 搜索 GitHub 教程候选...')
    candidates = []

    queries = [
        f'tutorial agent created:>{(datetime.now() - timedelta(days=14)).strftime("%Y-%m-%d")}',
        f'guide LLM engineering stars:>={min_stars}',
        f'awesome agent stars:>={min_stars}',
    ]

    headers = {'Accept': 'application/vnd.github.v3+json'}
    # 尝试用 gh token
    try:
        result = subprocess.run(
            ['gh', 'auth', 'token'], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0 and result.stdout.strip():
            headers['Authorization'] = f'token {result.stdout.strip()}'
    except Exception:
        pass

    seen_repos: set[str] = set()
    for query in queries:
        params = urllib.parse.urlencode({'q': query, 'sort': 'stars', 'order': 'desc', 'per_page': 10})
        data = fetch_json(f'{GITHUB_SEARCH_URL}?{params}', headers)
        if not data:
            continue
        for item in data.get('items', []):
            repo = item['full_name']
            if repo in seen_repos:
                continue
            seen_repos.add(repo)
            candidates.append({
                'source': 'GitHub',
                'title': item.get('description', '')[:80] or repo,
                'url': item['html_url'],
                'stars': item['stargazers_count'],
                'language': item.get('language', ''),
                'date': item.get('created_at', '')[:10],
                'repo': repo,
            })

    candidates.sort(key=lambda x: x.get('stars', 0), reverse=True)
    log(f'  找到 {len(candidates)} 个 GitHub 候选')
    return candidates


# ─── Step 2: 初筛 ──────────────────────────────────

def filter_candidates(hn: list[dict], gh: list[dict], top_n: int) -> list[dict]:
    """合并 + 去重 + 按相关性排序。"""
    log('Step 2: 初筛候选...')

    all_candidates = []

    for c in hn:
        relevance = sum(1 for kw in INTEREST_KEYWORDS if kw.lower() in c['title'].lower())
        c['relevance'] = relevance
        c['score'] = c['points'] * (1 + relevance * 0.5)
        all_candidates.append(c)

    for c in gh:
        text = f"{c['title']} {c.get('repo', '')}"
        relevance = sum(1 for kw in INTEREST_KEYWORDS if kw.lower() in text.lower())
        c['relevance'] = relevance
        c['score'] = c.get('stars', 0) * 0.1 * (1 + relevance * 0.5)
        all_candidates.append(c)

    # 去重（同域名）
    seen_domains: set[str] = set()
    unique: list[dict] = []
    for c in all_candidates:
        domain = urllib.parse.urlparse(c['url']).netloc
        if domain not in seen_domains:
            seen_domains.add(domain)
            unique.append(c)

    unique.sort(key=lambda x: x['score'], reverse=True)
    selected = unique[:top_n]

    log(f'  筛选出 {len(selected)} 个候选:')
    for i, c in enumerate(selected, 1):
        src = c['source']
        title = c['title'][:50]
        metric = c.get('points', c.get('stars', 0))
        log(f'  {i}. [{src}] {title} ({metric})')

    return selected


# ─── Step 3: 生成教程学习卡 ──────────────────────────

def generate_tutorial_card(date: str, candidates: list[dict], kb: Path) -> Path | None:
    """生成 Markdown 教程学习卡。"""
    log('Step 3: 生成教程学习卡...')

    card_lines = [
        f'# 教程学习卡 · {date}',
        '',
        '> 类型：教程学习源自动采集',
        f'> 生成时间: {datetime.now(TZ).strftime("%Y-%m-%d %H:%M")} CST',
        f'> 候选数: {len(candidates)}',
        '',
        '---',
        '',
        '## 教程速览',
        '',
        '| # | 来源 | 主题 | 指标 | URL |',
        '|---|------|------|------|-----|',
    ]

    for i, c in enumerate(candidates, 1):
        src = c['source']
        title = c['title'][:60].replace('|', '\\|')
        metric = f"⭐{c.get('stars', c.get('points', 0))}"
        url = c['url'][:60]
        card_lines.append(f'| {i} | {src} | {title} | {metric} | {url} |')

    card_lines.extend([
        '',
        '---',
        '',
        '## 深读候选',
        '',
        '以下候选需要深读（由 Hermes cron 或手动触发）：',
        '',
    ])

    for i, c in enumerate(candidates[:2], 1):
        card_lines.extend([
            f'### {i}. {c["title"][:60]}',
            '',
            f'- 来源: {c["source"]} ({c["url"]})',
            f'- 指标: {c.get("stars", c.get("points", 0))}',
            f'- 相关度: {c.get("relevance", 0)} 关键词命中',
            '',
        ])

    card_lines.extend([
        '---',
        '',
        '*本卡由 tutorial_learning_orchestrator.py 自动生成*',
    ])

    # 写入文件
    output_dir = kb / '每日学习'
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f'{date}-教程学习卡.md'

    output_file.write_text('\n'.join(card_lines), encoding='utf-8')
    log(f'✅ 教程学习卡已生成: {output_file}')
    return output_file


# ─── Step 4: 审计 ──────────────────────────────────

def audit_card(card_path: Path) -> tuple[int, list[str], list[str]]:
    """审计教程学习卡质量。"""
    log('Step 4: 审计产出...')

    if not card_path.exists():
        return 0, ['教程学习卡不存在'], []

    content = card_path.read_text(encoding='utf-8')
    score = 0
    issues: list[str] = []
    strengths: list[str] = []

    # 1. 结构完整性（3 分）
    required = ['教程速览', '深读候选']
    found = sum(1 for s in required if s in content)
    score += found * 3 // len(required)
    if found == len(required):
        strengths.append('必需章节齐全')
    else:
        issues.append(f'缺少章节: {[s for s in required if s not in content]}')

    # 2. 候选数量（3 分）
    table_rows = re.findall(r'^\|\s*\d+\s*\|', content, re.MULTILINE)
    count = len(table_rows)
    if count >= 5:
        score += 3
        strengths.append(f'{count} 个候选（达标）')
    elif count >= 3:
        score += 2
        strengths.append(f'{count} 个候选（基本达标）')
    else:
        issues.append(f'候选不足（{count} 个，要求 ≥3）')

    # 3. 来源多样性（3 分）
    sources = set(re.findall(r'\|\s*(HN|GitHub)\s*\|', content))
    if len(sources) >= 2:
        score += 3
        strengths.append(f'来源多样: {", ".join(sources)}')
    elif len(sources) >= 1:
        score += 1
        issues.append('来源单一，建议混合 HN + GitHub')

    # 4. URL 有效性（3 分）
    urls = re.findall(r'https?://\S+', content)
    if len(urls) >= 3:
        score += 3
        strengths.append(f'包含 {len(urls)} 个 URL')
    elif len(urls) >= 1:
        score += 2
    else:
        issues.append('缺少 URL')

    score = min(score, PASS_SCORE)
    log(f'审计完成: {score}/{PASS_SCORE}')
    return score, issues, strengths


# ─── Step 5: 写入 inbox ──────────────────────────────

def write_to_inbox(date: str, card_path: Path, shared_root: Path, score: int) -> None:
    """写入 Hermes inbox。"""
    log('Step 5: 写入 inbox...')

    inbox_dir = shared_root / 'inbox' / 'hermes' / 'daily'
    inbox_dir.mkdir(parents=True, exist_ok=True)
    inbox_file = inbox_dir / f'{date}-tutorial-learning.md'

    if card_path.exists():
        content = card_path.read_text(encoding='utf-8')
        inbox_file.write_text(content, encoding='utf-8')
        log(f'✅ 已写入 inbox: {inbox_file}')
    else:
        log('⚠️ 教程学习卡不存在，跳过 inbox 写入')


# ─── 主流程 ────────────────────────────────────────

def main() -> int:
    args = parse_args()
    date = args.date

    log(f'=== 教程学习编排器 · {date} ===')

    # Step 1: 搜索
    hn = search_hn_tutorials(args.min_hn_points)
    gh = search_github_tutorials(args.min_stars)

    if not hn and not gh:
        log('❌ 未找到任何候选')
        return 1

    # Step 2: 筛选
    candidates = filter_candidates(hn, gh, args.top_n)

    if not candidates:
        log('❌ 筛选后无候选')
        return 1

    if args.dry_run:
        log('🔍 Dry run 完成，不生成文件')
        for c in candidates:
            log(f'  [{c["source"]}] {c["title"][:50]} → {c["url"]}')
        return 0

    # Step 3: 生成教程学习卡
    card_path = generate_tutorial_card(date, candidates, args.knowledge_base)
    if not card_path:
        return 1

    # Step 4: 审计
    score, issues, strengths = audit_card(card_path)

    if score < PASS_SCORE:
        log(f'⚠️ 审计未通过 ({score}/{PASS_SCORE})，但仍写入 inbox')
        for issue in issues:
            log(f'  - {issue}')

    # Step 5: 写入 inbox
    write_to_inbox(date, card_path, args.shared_root, score)

    log(f'=== 完成 · 得分 {score}/{PASS_SCORE} ===')
    return 0 if score >= PASS_SCORE else 1


if __name__ == '__main__':
    sys.exit(main())
