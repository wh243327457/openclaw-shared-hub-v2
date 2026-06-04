#!/usr/bin/env python3
"""生成 GitHub 热门项目每日学习指令。

读取历史审计反馈，分析昨日失败点，生成今日强化指令。
"""

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

# 常量
DEFAULT_SHARED_ROOT = Path(__file__).resolve().parents[1]
PIPELINE = 'github-hot-project-learning'
TZ = timezone(timedelta(hours=8))

# 默认技术栈
DEFAULT_TECH_STACK = [
    'Go', 'Rust', 'Python', 'TypeScript',
    'Kubernetes', 'Docker', 'Terraform',
    'AI/ML', 'LLM', 'WebAssembly'
]

# 默认领域
DEFAULT_DOMAINS = [
    'DevOps', 'AI/ML', '云原生', '安全', '性能优化',
    '分布式系统', '数据库', 'Web 框架', 'CLI 工具'
]


def today_cst() -> str:
    return datetime.now(TZ).date().isoformat()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--date', default=today_cst(), help='目标日期 YYYY-MM-DD')
    parser.add_argument('--shared-root', type=Path, default=DEFAULT_SHARED_ROOT)
    parser.add_argument('--dry-run', action='store_true', help='仅预览，不写文件')
    return parser.parse_args()


def read_audit_feedback(shared_root: Path) -> dict[str, Any]:
    """读取历史审计反馈。"""
    feedback_file = shared_root / 'runtime' / 'hermes' / PIPELINE / 'audit-feedback.json'
    if not feedback_file.exists():
        return {'feedbacks': [], 'failures': []}
    
    try:
        with feedback_file.open('r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f'读取审计反馈失败: {e}', file=sys.stderr)
        return {'feedbacks': [], 'failures': []}


def analyze_failures(feedbacks: list[dict]) -> list[dict]:
    """分析最近 7 天的审计问题（含通过但有扣分项的情况）。"""
    failures = []

    for fb in feedbacks[-7:]:  # 最近 7 天
        score = fb.get('score', 0)
        issues = fb.get('issues', [])
        # 过滤掉"无"和空值
        real_issues = [i for i in issues if i and i != '无']
        if real_issues:
            for issue in real_issues:
                failures.append({
                    'date': fb.get('date'),
                    'issue': issue,
                    'score': score,
                    'passed': score >= 16,
                })

    return failures


def generate_enhanced_instructions(failures: list[dict]) -> str:
    """根据失败点生成强化指令。"""
    if not failures:
        return """- 今日无特殊强化要求，按照标准流程执行学习。
- 重点关注：深读项目的可迁移模式和实践价值。"""

    instructions = []
    instructions.append('### 今日强化重点')

    # 统计失败类型（含通过但有扣分项的情况）
    issue_counts: dict[str, int] = {}
    for f in failures:
        issue = f['issue']
        issue_counts[issue] = issue_counts.get(issue, 0) + 1

    # 按频率排序，最多 5 个强化点
    sorted_issues = sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)

    for issue, count in sorted_issues[:5]:
        severity = '🔴' if count >= 3 else '🟡' if count >= 2 else '⚪'
        instructions.append(f'- {severity} **{issue}**（最近 7 天出现 {count} 次）')

    # 基于高频问题生成具体强化动作
    action_map = {
        '缺少 stars 数据': '每个深读项目必须用 GitHub API 查询 stars/forks/license，写入报告头部',
        '缺少 license 信息': '每个项目必须标注 License 类型（MIT/Apache-2.0/GPL 等），null 时标注"无 license"',
        '缺少 skill 升格判断': '每个深读项目必须有「Skill 升格判断」章节：可直接迁移 / 需二次验证 / 暂不沉淀',
        '源码深度不足': '每个深读项目必须包含：repo tree 摘要、关键源码文件列表、架构/数据流分析',
        '完全没有源码级分析': '禁止只复述 README，必须深入源码结构和实现细节',
        '可迁移经验偏少': '至少提炼 3 条「当……时，应优先……」格式的可迁移经验',
        '风险边界不完整': '每个项目必须覆盖：License、安全风险、维护活跃度、不适用场景',
    }
    actions = []
    for issue, _ in sorted_issues:
        if issue in action_map:
            actions.append(f'- ✅ {action_map[issue]}')
    if actions:
        instructions.append('')
        instructions.append('### 具体强化动作')
        instructions.extend(actions)

    return '\n'.join(instructions)


def generate_tech_stack(goals: str) -> list[str]:
    """根据学习目标生成推荐技术栈。"""
    # 简单实现：返回默认栈
    return DEFAULT_TECH_STACK


def generate_domains(goals: str) -> list[str]:
    """根据学习目标生成推荐领域。"""
    return DEFAULT_DOMAINS


def generate_daily_goals(date: str, failures: list[dict]) -> str:
    """生成今日学习目标。"""
    goals = []
    goals.append(f'## {date} 学习目标')
    goals.append('')
    goals.append('1. **发现**: 找到 3-5 个值得深读的热门项目')
    goals.append('2. **深读**: 完成 2-3 个项目的深度分析')
    goals.append('3. **沉淀**: 提取至少 3 条可复用经验')
    goals.append('4. **实践**: 设计 1 个可尝试的实验')
    
    if failures:
        goals.append('')
        goals.append('### 强化目标')
        for f in failures[:2]:
            goals.append(f'- 重点改进: {f["issue"]}')
    
    return '\n'.join(goals)


def generate_instruction_template(
    date: str,
    goals: str,
    tech_stack: list[str],
    domains: list[str],
    required_projects: str,
    audit_feedback: str,
    historical_failures: str,
    enhanced_instructions: str
) -> str:
    """生成完整的指令模板。"""
    template = f'''# GitHub 热门项目每日学习指令

**生成时间**: {date}
**生成来源**: Hermes 审计反馈系统
**版本**: v2.0

---

## 今日学习目标

{goals}

---

## 学习范围

### 推荐技术栈

{chr(10).join(f'- {t}' for t in tech_stack)}

### 推荐领域

{chr(10).join(f'- {d}' for d in domains)}

---

## 必读项目

{required_projects}

---

## 产出要求

### 1. 学习报告

**文件**: `shared/inbox/openclaw/daily/{date}.md`

必须包含：
- **今日结论**（一句话总结今日学习主线）
- **项目速览**（5-10 个简要列出，含 Stars/Language/License）
- **深读项目**（每个必须包含以下全部内容）：
  - 一句话判断：为什么值得学
  - 解决的问题：替代了什么旧做法
  - **架构/实现**：核心模块、数据流、关键依赖
  - **repo tree 摘要**：目录结构 + 每层用途
  - **关键源码文件**：文件路径 + 用途 + 关键内容摘要
  - **⭐ 源码精读**（新增）：至少 3 个核心函数/方法的签名 + 逻辑摘要，用代码块展示关键实现片段（≥3 个代码块/项目）
  - **依赖分析**（新增）：go.mod/requirements.txt/package.json 核心依赖列表 + 供应链风险评估
  - **可复用经验**：至少 1 条「当……时，应优先……」格式
  - **可尝试实验**：30 分钟内能做的最小 demo
  - **风险边界**：license、维护活跃度、安全风险、不适用场景
  - **⭐ Skill 升格判断**：可直接迁移 / 需二次验证 / 暂不沉淀（必须明确，禁止空话）
  - **⭐ 落地路径**（新增）：如果要在 Hermes/OpenClaw 中复用该项目的某个模式，具体怎么做（列出文件/模块/接口）
- **经验沉淀**（至少 3 条通用经验）
- **明日继续**（下一步最小动作）
- **候选反哺**（candidate facts / skills / open questions）

### 2. 项目卡片

**文件**: `shared/runtime/openclaw/github-learning/projects/owner-repo.md`

必须包含：
- 基本信息（链接、Stars、Forks、License、语言、最近更新）
- 一句话判断
- 核心价值
- 可迁移模式（含落地路径）
- 已知限制

### 3. 经验沉淀

**文件**: `shared/runtime/openclaw/github-learning/lessons.md`

按日期追加，每条经验需具体可操作。

---

## ⚠️ 质量标准（2026-05-30 强化版）

### 硬性要求（不达标直接不合格，16 分返工线）

|| # | 维度 | 分值 | 要求 |
||---|------|------|------|
|| 1 | 结构完整 | 4 | 五个必需章节齐全（今日结论/项目速览/深读/经验沉淀/明日继续） |
|| 2 | 深读数量 | 3 | ≥2 个深读项目 |
|| 3 | **源码深度** | 3 | repo tree + 关键文件 + 架构分析 + 代码块 |
|| 4 | **源码精读** | 2 | 每个深读项目 ≥3 个代码块，展示关键函数签名+逻辑（新增） |
|| 5 | **API 数据** | 2 | stars + license 来自 GitHub API |
|| 6 | 可迁移经验 | 3 | ≥3 条「当……时，应优先……」格式 |
|| 7 | 风险边界 | 2 | license + 安全 + 局限性 + 维护活跃度 |
|| 8 | **Skill 升格** | 2 | 每个项目明确：可直接迁移 / 需二次验证 / 暂不沉淀 |
|| 9 | **落地路径** | 1 | 至少 1 个项目给出 Hermes/OpenClaw 复用路径（新增） |
|| 10 | 无幻觉 | 1 | 无可疑 stars 数字或未验证声明 |

### 禁止事项

- ❌ 只复述 README，不深入源码
- ❌ 没有 stars/license 实时数据
- ❌ 缺少 skill 升格判断
- ❌ 可迁移经验少于 3 条
- ❌ 风险边界只写一句话

---

## 深度学习与安全反哺要求

每日学习不只做项目摘抄，必须采用"深挖 → 机制抽象 → 反哺建议 → 安全边界"的结构。

### A. 深挖对象
- 明确今日深挖对象是项目、工具、机制还是故障案例。
- 每个深读对象至少核验 README/docs/release/issues 中的 2 类来源；关键 repo 元数据必须来自 GitHub API。

### B. 可验证证据
- 给出 GitHub 链接、核心文件/目录、版本/提交或查询时间。
- 不确定的结论必须标注"待核验"，不得编造。

### C. 核心机制
- 不只罗列功能；必须抽象出可迁移模式。
- 优先使用这种句式：`当……时，应优先……，因为……，边界是……`。

### D. 反哺到现有体系
每个深读项目至少判断一次是否可反馈到：
- shared curated memory / facts / projects
- shared skill / workflow
- Hermes 审计流程
- OpenClaw 每日学习 / 每日巡检
- runtime POC / open questions

### E. 安全边界
必须明确哪些内容不能自动执行：
- 不自动改配置、模型、provider、cron、secret。
- 不直接写 curated active fact，只提出 candidate。
- 不复制 license 不明或不兼容项目源码。
- 不从 assistant-authored prose 生成用户事实。
- 巡检类建议只输出风险、证据、影响、建议动作，不自动修复。

### F. 候选反哺
在日报末尾新增"候选反哺"小节，按以下格式输出：

```markdown
## 候选反哺

### Candidate Facts
- [ ] topic: ... | evidence: ... | 建议: create/update/retire/dispute | 安全级别: low/medium/high

### Candidate Skills / Workflow
- [ ] 名称: ... | 可复用场景: ... | 是否建议 shared: yes/no | 原因: ...

### Candidate Open Questions
- [ ] 问题: ... | reason: gap/conflict/stale/adaptation | priority: low/medium/high

### 不应自动落地
- ...
```

### G. 输出约束
- 候选反哺只作为 Hermes 二轮审计输入，不代表已落库。
- 如果触及安全/密钥/配置，必须只写变量名或占位符，不写明文值。
- 受 cron summary 截断限制，核心结论要短；完整证据应尽量写入 shared inbox/runtime 产物。

---

## 审计反馈区（Hermes 自动更新）

> 以下内容由 Hermes 审计后自动写入，请勿手动修改。

### 最近审计反馈

{audit_feedback}

### 历史失败点

{historical_failures}

### 强化指令

{enhanced_instructions}

---

## 使用说明

### OpenClaw 学习流程

1. **读取本指令**: 确认今日学习目标和范围
2. **执行学习**: 按照产出要求完成学习
3. **提交产出**: 确保文件写入正确路径
4. **自检**: 对照质量标准自查

### Hermes 审计流程

1. **读取产出**: 检查 OpenClaw 的学习产出
2. **评分**: 按照质量标准评分（20 分制）
3. **反馈**: 写入审计反馈区
4. **强化**: 更新强化指令

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v2.0 | {date} | 强化审计标准：源码深度、API 数据、skill 升格判断 |
| v1.0 | {date} | 初始版本 |
'''
    return template


def write_instruction(shared_root: Path, content: str, date: str) -> Path:
    """写入指令文件。"""
    output_dir = shared_root / 'runtime' / 'hermes' / PIPELINE
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / 'instruction.md'
    with output_file.open('w', encoding='utf-8') as f:
        f.write(content)
    
    return output_file


def read_evolution_suggestions(shared_root: Path) -> list[dict]:
    """读取昨日学习的进化建议（由通用反思引擎生成）。"""
    try:
        from reflection_engine import ReflectionEngine
        return ReflectionEngine.read_suggestions(shared_root, 'github-learning')
    except ImportError:
        # fallback: 直接读文件
        evolution_file = shared_root / 'runtime' / 'hermes' / 'github-learning' / 'evolution-suggestions.json'
        if not evolution_file.exists():
            return []
        try:
            data = json.loads(evolution_file.read_text(encoding='utf-8'))
            return data.get('suggestions', [])
        except Exception:
            return []


def generate_evolution_instructions(suggestions: list[dict]) -> str:
    """将进化建议转化为明日指令的强化内容。"""
    if not suggestions:
        return ''

    high_priority = [s for s in suggestions if s.get('priority') == 'high']
    medium_priority = [s for s in suggestions if s.get('priority') == 'medium']

    if not high_priority and not medium_priority:
        return ''

    lines = ['### 🧬 自我进化建议（昨日学习反思）']

    if high_priority:
        lines.append('')
        lines.append('**必须改进**：')
        for s in high_priority:
            msg = s.get('message') or s.get('suggestion', '')
            lines.append(f'- 🔴 {msg}')

    if medium_priority:
        lines.append('')
        lines.append('**建议提升**：')
        for s in medium_priority:
            msg = s.get('message') or s.get('suggestion', '')
            lines.append(f'- 🟡 {msg}')

    return '\n'.join(lines)


def main() -> None:
    args = parse_args()
    date = args.date
    shared_root = args.shared_root
    
    print(f'生成 {date} 学习指令...')
    
    # 1. 读取历史审计反馈
    feedback_data = read_audit_feedback(shared_root)
    feedbacks = feedback_data.get('feedbacks', [])
    
    # 2. 分析失败点
    failures = analyze_failures(feedbacks)
    
    # 3. 生成今日目标
    goals = generate_daily_goals(date, failures)
    
    # 4. 生成技术栈和领域
    tech_stack = generate_tech_stack(goals)
    domains = generate_domains(goals)
    
    # 5. 生成强化指令
    enhanced_instructions = generate_enhanced_instructions(failures)
    
    # 5.5 读取昨日进化建议（自我进化闭环）
    evolution_suggestions = read_evolution_suggestions(shared_root)
    evolution_instructions = generate_evolution_instructions(evolution_suggestions)
    if evolution_instructions:
        enhanced_instructions += '\n\n' + evolution_instructions
        print(f'   - 自我进化建议: {len(evolution_suggestions)} 条')
    
    # 6. 构建审计反馈摘要
    audit_feedback = '暂无最近审计反馈' if not feedbacks else f'最近 {len(feedbacks)} 条反馈已记录'
    
    # 7. 构建历史失败点摘要
    historical_failures = '暂无历史失败点' if not failures else '\n'.join([
        f'- {f["date"]}: {f["issue"]} (得分: {f["score"]})'
        for f in failures[:5]
    ])
    
    # 8. 必读项目（默认为空，由 Hermes 或用户指定）
    required_projects = '今日无指定必读项目，由 OpenClaw 自主发现热门项目。'
    
    # 9. 生成指令模板
    instruction = generate_instruction_template(
        date=date,
        goals=goals,
        tech_stack=tech_stack,
        domains=domains,
        required_projects=required_projects,
        audit_feedback=audit_feedback,
        historical_failures=historical_failures,
        enhanced_instructions=enhanced_instructions
    )
    
    # 10. 写入文件
    if args.dry_run:
        print(instruction)
        print('\n[DRY-RUN] 未写入文件')
    else:
        output_file = write_instruction(shared_root, instruction, date)
        print(f'✅ 指令已生成: {output_file}')
        print(f'   - 失败点分析: {len(failures)} 个')
        print(f'   - 强化指令: 已生成')


if __name__ == '__main__':
    main()
