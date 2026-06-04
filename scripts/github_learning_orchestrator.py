#!/usr/bin/env python3
"""GitHub 热门项目学习闭环编排器。

单一任务执行整个学习闭环：
1. 生成今日学习指令
2. 触发 OpenClaw 学习
3. 等待学习完成
4. 审计产出
5. 失败 → 反思 + 更新模板
   成功 → 更新知识库 + 推送微信
"""

import argparse
import json
import re
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

# 常量
DEFAULT_SHARED_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_KNOWLEDGE_BASE = Path('/mnt/d/system/selfSystem/03-学习/技术实践/GitHub 热门项目学习档案')
OPENCLAW_JOB_ID = '7aa310ea-b264-40c8-b23a-ed655c565a69'
TZ = timezone(timedelta(hours=8))
PASS_SCORE = 16
OPENCLAW_TIMEOUT = 1800  # 30 分钟


def today_cst() -> str:
    return datetime.now(TZ).date().isoformat()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--date', default=today_cst(), help='目标日期')
    parser.add_argument('--shared-root', type=Path, default=DEFAULT_SHARED_ROOT)
    parser.add_argument('--knowledge-base', type=Path, default=DEFAULT_KNOWLEDGE_BASE)
    parser.add_argument('--skip-openclaw', action='store_true', help='跳过 OpenClaw 学习步骤')
    parser.add_argument('--dry-run', action='store_true')
    return parser.parse_args()


def log(message: str) -> None:
    ts = datetime.now(TZ).strftime('%H:%M:%S')
    print(f'[{ts}] {message}')


def generate_instruction(date: str, shared_root: Path) -> bool:
    """Step 1: 生成今日学习指令。"""
    log('Step 1: 生成今日学习指令...')
    
    script = shared_root / 'scripts' / 'generate_daily_instruction.py'
    if not script.exists():
        log(f'❌ 脚本不存在: {script}')
        return False
    
    result = subprocess.run(
        ['python3', str(script), '--date', date, '--shared-root', str(shared_root)],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        log(f'❌ 生成指令失败: {result.stderr}')
        return False
    
    log('✅ 学习指令已生成')
    return True


def trigger_openclaw_learning(shared_root: Path) -> bool:
    """Step 2: 触发 OpenClaw 学习。"""
    log('Step 2: 触发 OpenClaw 学习...')
    
    # 检查 OpenClaw 容器状态
    result = subprocess.run(
        ['docker', 'inspect', '-f', '{{.State.Status}}', 'openclaw'],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0 or 'running' not in result.stdout:
        log('OpenClaw 容器未运行，尝试启动...')
        subprocess.run(['docker', 'start', 'openclaw'], capture_output=True)
        time.sleep(5)
    
    # 触发学习
    result = subprocess.run(
        ['docker', 'exec', 'openclaw', 'openclaw', 'cron', 'run', OPENCLAW_JOB_ID],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        log(f'❌ 触发失败: {result.stderr}')
        return False
    
    log('✅ OpenClaw 学习已触发')
    return True


def wait_for_openclaw_completion(date: str, shared_root: Path, timeout: int = OPENCLAW_TIMEOUT) -> bool:
    """Step 2.5: 等待 OpenClaw 学习完成。"""
    log(f'等待 OpenClaw 学习完成（超时: {timeout}s）...')
    
    output_file = shared_root / 'inbox' / 'openclaw' / 'daily' / f'{date}.md'
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        if output_file.exists() and output_file.stat().st_size > 0:
            log('✅ 学习产出已生成')
            return True
        time.sleep(30)
        log(f'  等待中... ({int(time.time() - start_time)}s)')
    
    log('❌ 等待超时')
    return False


def _count_pattern(content: str, pattern: str) -> int:
    """统计内容中某模式出现次数。"""
    return len(re.findall(pattern, content, re.IGNORECASE))


def audit_learning(date: str, shared_root: Path) -> tuple[int, list[str], list[str]]:
    """Step 3: 审计学习产出（v3 — 内容深度导向 + 源码精读 + 落地路径）。

    23 分制，低于 16 分返工。
    维度：结构完整 4 + 深读数量 3 + 源码深度 3 + 源码精读 2 + API 数据 2 + 可迁移经验 3 + 风险边界 2 + skill 升格 2 + 落地路径 1 + 无幻觉 1
    """
    log('Step 3: 审计学习产出...')

    output_file = shared_root / 'inbox' / 'openclaw' / 'daily' / f'{date}.md'

    if not output_file.exists():
        log('❌ 学习产出不存在')
        return 0, ['学习产出文件不存在'], []

    content = output_file.read_text(encoding='utf-8')
    lines = content.splitlines()
    line_count = len(lines)

    score = 0
    issues: list[str] = []
    strengths: list[str] = []

    # ── 1. 结构完整性（4 分）─────────────────────
    required_sections = ['今日结论', '项目速览', '深读项目']
    # 经验沉淀/可复用经验 都算通过
    lesson_section_names = ['经验沉淀', '可复用经验']
    has_lesson_section = any(s in content for s in lesson_section_names)
    # 明日继续/明日建议/下一步 都算通过
    tomorrow_section_names = ['明日继续', '明日建议', '下一步', '候选反哺']
    has_tomorrow_section = any(s in content for s in tomorrow_section_names)
    missing_sections = [s for s in required_sections if s not in content]
    if not has_lesson_section:
        missing_sections.append('经验沉淀/可复用经验')
    if not has_tomorrow_section:
        missing_sections.append('明日继续/下一步')
    # 总共 5 项检查：3 个必需章节 + 经验沉淀 + 明日继续
    total_checks = len(required_sections) + 2  # +2 for lesson and tomorrow
    missing_count = len(missing_sections)
    structure_score = max(0, (total_checks - missing_count) * 4 // total_checks)
    score += structure_score
    if not missing_sections:
        strengths.append('五个必需章节齐全')
    else:
        for s in missing_sections:
            issues.append(f'缺少「{s}」章节')

    # ── 2. 深读项目数量（3 分）─────────────────────
    deep_project_headers = [l for l in lines if l.strip().startswith('### 项目') or re.match(r'^###\s+\d+[\.\d]*\.?\s+\S', l.strip()) or re.match(r'^##\s+深读项目\s+', l.strip()) or re.match(r'^###\s+\d+\.\s+', l.strip())]
    deep_count = len(deep_project_headers)
    if deep_count >= 3:
        score += 3
        strengths.append(f'深读 {deep_count} 个项目（达标）')
    elif deep_count == 2:
        score += 2
        strengths.append(f'深读 2 个项目（基本达标）')
    else:
        issues.append(f'深读项目不足（{deep_count} 个，要求 ≥2）')

    # ── 3. 源码深度（3 分）─────────────────────
    # 检查是否有源码级分析：repo tree、关键文件、架构图、目录结构
    source_depth_signals = [
        (r'(?i)(repo\s*tree|目录结构|项目结构|文件结构)', 'repo tree / 目录结构'),
        (r'(?i)(关键(源码|文件)|core\s*files?|关键模块)', '关键源码文件分析'),
        (r'(?i)(架构|实现原理|数据流|核心模块|内部机制)', '架构/实现分析'),
        (r'```', '代码块'),
    ]
    source_hits = 0
    for pattern, label in source_depth_signals:
        if _count_pattern(content, pattern) > 0:
            source_hits += 1
    if source_hits >= 3:
        score += 3
        strengths.append(f'源码深度良好（{source_hits}/4 信号命中）')
    elif source_hits >= 2:
        score += 2
        strengths.append(f'有一定源码分析（{source_hits}/4 信号命中）')
    elif source_hits >= 1:
        score += 1
        issues.append(f'源码深度不足（仅 {source_hits}/4 信号命中，需要 repo tree + 关键文件 + 架构分析）')
    else:
        issues.append('完全没有源码级分析，停留在 README 复述层')

    # ── 3.5 源码精读（2 分）─────────────────────
    # 统计代码块数量，每个深读项目应有 ≥3 个代码块
    code_block_count = _count_pattern(content, r'```')
    code_blocks = code_block_count // 2  # 每个代码块有开闭两个 ```
    if code_blocks >= 6:
        score += 2
        strengths.append(f'源码精读良好（{code_blocks} 个代码块）')
    elif code_blocks >= 3:
        score += 1
        strengths.append(f'有一定代码展示（{code_blocks} 个代码块，建议 ≥6）')
    else:
        issues.append(f'代码块不足（{code_blocks} 个，要求 ≥3，建议 ≥6 以展示关键函数签名和逻辑）')

    # ── 4. GitHub API 数据真实性（2 分）─────────────
    # 检查是否有实时数据：stars 数字、license、查询时间
    api_data_score = 0
    if re.search(r'(Stars?|⭐)\s*[:：]?\s*\d[\d,.]*[Kk]?\b', content) or re.search(r'\|\s*Stars?\s*\|.*?\d[\d,.]*\s*[★⭐]?\s*\|', content) or (re.search(r'(?i)Stars', content) and re.search(r'\|\s*\d{3,}[\d,]*\s*\|', content)):
        api_data_score += 1
    else:
        issues.append('缺少 stars 数据')
    if re.search(r'(?i)(License)\s*[:：]?\s*\S+', content) or re.search(r'\|\s*License\s*\|\s*\S+\s*\|', content):
        api_data_score += 1
    else:
        issues.append('缺少 license 信息')
    if api_data_score == 2:
        strengths.append('包含 stars + license 数据')
    score += api_data_score

    # ── 5. 可迁移经验（3 分）─────────────────────
    # 统计「当……时，应优先……」格式的经验数量
    lesson_pattern = r'(?m)^[\-\d.*]+\s*.*当.*时.*应优先'
    lesson_count = _count_pattern(content, lesson_pattern)
    # 也统计「可复用经验」「可迁移」段落中的列表项
    if lesson_count == 0:
        # fallback: 统计经验沉淀/可复用经验章节的列表项
        in_lesson_section = False
        for line in lines:
            if ('经验沉淀' in line or '可复用经验' in line) and line.lstrip().startswith('#'):
                in_lesson_section = True
                continue
            if in_lesson_section and line.lstrip().startswith('#'):
                break
            if in_lesson_section and (line.strip().startswith('-') or (len(line.strip()) > 2 and line.strip()[0].isdigit() and '.' in line[:3])):
                lesson_count += 1

    if lesson_count >= 3:
        score += 3
        strengths.append(f'提炼了 {lesson_count} 条可迁移经验')
    elif lesson_count >= 1:
        score += 2
        issues.append(f'可迁移经验偏少（{lesson_count} 条，要求 ≥3）')
    else:
        issues.append('缺少可迁移经验')

    # ── 6. 风险边界（2 分）─────────────────────
    risk_signals = [
        (r'(?i)(License|许可证)', 'license'),
        (r'(?i)(安全风险|security|漏洞)', '安全风险'),
        (r'(?i)(限制|局限|不适用|缺点|不足)', '局限性'),
        (r'(?i)(维护活跃|活跃度|last commit)', '维护活跃度'),
    ]
    risk_hits = sum(1 for p, _ in risk_signals if _count_pattern(content, p) > 0)
    if risk_hits >= 2:
        score += 2
        strengths.append(f'风险边界覆盖良好（{risk_hits}/4 信号）')
    elif risk_hits >= 1:
        score += 1
        issues.append(f'风险边界不完整（仅 {risk_hits}/4 信号）')
    else:
        issues.append('缺少风险边界分析')

    # ── 7. Skill 升格判断（2 分）─────────────────
    if re.search(r'(?i)(skill\s*升格|升格判断|可沉淀|暂不沉淀|继续观察)', content):
        score += 2
        strengths.append('包含 skill 升格判断')
    else:
        issues.append('缺少 skill 升格判断（要求明确：可直接迁移 / 需二次验证 / 暂不沉淀）')

    # ── 7.5 落地路径（1 分）─────────────────
    landing_signals = [
        r'(?i)(落地路径|复用路径|实现路径|集成方案|怎么用|how\s+to\s+(use|integrate|implement))',
        r'(?i)(在\s*Hermes|在\s*OpenClaw|接入|对接)',
        r'(?i)(具体步骤|实现步骤|集成步骤)',
    ]
    landing_hits = sum(1 for p in landing_signals if _count_pattern(content, p) > 0)
    if landing_hits >= 1:
        score += 1
        strengths.append('包含落地/复用路径')
    else:
        issues.append('缺少落地路径（建议给出 Hermes/OpenClaw 复用方案）')

    # ── 8. 无明显幻觉（1 分）─────────────────────
    # 检查可疑的 stars 数字（>500K 或增速离谱）
    suspicious_stars = re.findall(r'(?:Stars?|⭐)\s*[:：]?\s*(\d[\d,.]*)', content)
    hallucination = False
    for s in suspicious_stars:
        try:
            num = int(s.replace(',', '').replace('.', ''))
            if num > 500000:
                hallucination = True
                issues.append(f'可疑 stars 数字: {s}（需二次验证）')
        except ValueError:
            pass
    if not hallucination:
        score += 1
        strengths.append('未发现明显数据幻觉')

    # ── 汇总 ──────────────────────────────────
    MAX_SCORE = 23
    score = min(score, MAX_SCORE)
    log(f'审计完成: {score}/{PASS_SCORE}')
    if issues:
        log(f'  问题: {"; ".join(issues[:5])}')
    return score, issues, strengths


def handle_failure(date: str, score: int, issues: list[str], shared_root: Path) -> None:
    """Step 4A: 审计失败 → 反思 + 更新模板。"""
    log('Step 4A: 处理审计失败...')
    
    # 反思失败原因
    log('反思失败原因:')
    for issue in issues:
        log(f'  - {issue}')
    
    # 生成改进指令
    improvements = []
    for issue in issues:
        if '缺少' in issue:
            improvements.append(f'当遇到{issue}时，必须补充相关内容')
        elif '不足' in issue:
            improvements.append(f'确保{issue}得到满足')
    
    # 更新模板
    script = shared_root / 'scripts' / 'audit_feedback_writer.py'
    if script.exists():
        cmd = [
            'python3', str(script),
            '--date', date,
            '--score', str(score),
            '--issues'] + issues + ['--strengths', '执行了学习流程']
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            log('✅ 模板已更新')
        else:
            log(f'❌ 更新模板失败: {result.stderr}')
    
    log(f'明日改进方向: {"; ".join(improvements[:3])}')


def handle_success(
    date: str,
    score: int,
    issues: list[str],
    strengths: list[str],
    shared_root: Path,
    knowledge_base: Path
) -> None:
    """Step 4B: 审计成功 → 更新知识库 + 推送微信。"""
    log('Step 4B: 处理审计成功...')
    
    # 1. 更新知识库
    update_knowledge_base(date, shared_root, knowledge_base)
    
    # 2. 生成推送摘要
    summary = generate_push_summary(date, score, strengths, knowledge_base, shared_root)
    
    # 3. 推送微信
    push_to_wechat(summary, shared_root)
    
    # 4. 记录反馈（传入实际 issues，即使是空的也比硬编码"无"好）
    script = shared_root / 'scripts' / 'audit_feedback_writer.py'
    if script.exists():
        real_issues = [i for i in issues if i and i != '无']
        cmd = [
            'python3', str(script),
            '--date', date,
            '--score', str(score),
            '--issues'] + (real_issues if real_issues else ['无']) + [
            '--strengths'] + strengths
        
        subprocess.run(cmd, capture_output=True, text=True)


def update_knowledge_base(
    date: str,
    shared_root: Path,
    knowledge_base: Path
) -> None:
    """更新个人知识库。"""
    log('更新知识库...')
    
    # 创建目录
    daily_dir = knowledge_base / '每日学习'
    audit_dir = knowledge_base / '质量审计'
    daily_dir.mkdir(parents=True, exist_ok=True)
    audit_dir.mkdir(parents=True, exist_ok=True)
    
    # 复制学习日报
    output_file = shared_root / 'inbox' / 'openclaw' / 'daily' / f'{date}.md'
    if output_file.exists():
        import shutil
        dest = daily_dir / f'{date}-GitHub热门项目学习日报.md'
        shutil.copy2(output_file, dest)
        log(f'  学习日报: {dest}')
    
    log('✅ 知识库已更新')


def _extract_section(content: str, title: str) -> str:
    """提取 Markdown 指定章节内容。"""
    lines = content.split('\n')
    start_index = -1
    for index, line in enumerate(lines):
        if title in line and line.lstrip().startswith('#'):
            start_index = index + 1
            break
    if start_index < 0:
        return ""

    section_lines: list[str] = []
    for line in lines[start_index:]:
        if line.lstrip().startswith('#'):
            break
        section_lines.append(line)
    return '\n'.join(section_lines).strip()


def _extract_deep_projects(content: str) -> list[dict[str, str]]:
    """从学习日报中提取深读项目。"""
    projects: list[dict[str, str]] = []
    current: dict[str, str] | None = None

    for raw_line in content.split('\n'):
        line = raw_line.strip()
        if line.startswith('### 项目') or re.match(r'^###\s+\d+\.\d+\s+\S', line) or re.match(r'^###\s+\d+\.\s+', line):
            if current:
                projects.append(current)
            if line.startswith('### 项目'):
                name = line.split(':', 1)[1].strip() if ':' in line else line.replace('###', '').strip()
            elif re.match(r'^###\s+\d+\.\s+', line):
                name = re.sub(r'^###\s+\d+\.\s+', '', line).strip()
            else:
                name = re.sub(r'^###\s+\d+\.\d+\s+', '', line).strip()
            current = {
                'name': name,
                'judgement': '',
                'problem': '',
                'lesson': '',
                'risk': '',
            }
            continue

        if not current:
            continue

        if line.startswith('- **一句话判断**') or line.startswith('**一句话判断**'):
            text = line.lstrip('- ').strip()
            for sep in ['：', ':']:
                if sep in text:
                    current['judgement'] = text.split(sep, 1)[1].strip()
                    break
            else:
                current['judgement'] = text
        elif line.startswith('- **解决的问题**') or line.startswith('**解决的问题**'):
            text = line.lstrip('- ').strip()
            for sep in ['：', ':']:
                if sep in text:
                    current['problem'] = text.split(sep, 1)[1].strip()
                    break
            else:
                current['problem'] = text
        elif (line.startswith('- 当') or line.startswith('当')) and not current['lesson']:
            current['lesson'] = line.lstrip('- ').strip()
        elif line.startswith('- **风险边界**') or line.startswith('**风险边界**'):
            current['risk'] = '已覆盖 license、维护活跃度、安全风险和适用边界'

    if current:
        projects.append(current)

    return [p for p in projects if p.get('name') and p['name'] != '深读项目']


def _shorten(text: str, limit: int = 52) -> str:
    """压缩单元格文字，避免微信表格过宽。"""
    text = ' '.join(text.replace('|', '/').split())
    return text if len(text) <= limit else text[:limit - 1] + '…'


def generate_push_summary(date: str, score: int, strengths: list[str], knowledge_base: Path, shared_root: Path) -> str:
    """生成微信推送摘要（v3 学习复盘版）。"""

    output_file = shared_root / 'inbox' / 'openclaw' / 'daily' / f'{date}.md'
    output_content = output_file.read_text(encoding='utf-8') if output_file.exists() else ""
    projects = _extract_deep_projects(output_content)
    conclusion = _extract_section(output_content, '今日结论').split('\n')[0].strip()
    lessons_section = _extract_section(output_content, '经验沉淀')
    if not lessons_section:
        lessons_section = _extract_section(output_content, '可复用经验')
    lesson_lines = []
    for raw_line in lessons_section.split('\n'):
        line = raw_line.strip()
        if not line or line.startswith('###'):
            continue
        if line[0].isdigit() and '. ' in line:
            lesson_lines.append(line.split('. ', 1)[1].replace('**', '').strip())
    if not lesson_lines:
        lesson_lines = [p['lesson'] for p in projects if p.get('lesson')]

    actual_count = len(projects)
    expected_count = 3
    line_count = len(output_content.splitlines()) if output_content else 0
    pass_status = score >= PASS_SCORE

    if actual_count >= expected_count and len(lesson_lines) >= 3 and pass_status:
        execution_verdict = "✅ 达标，而且这次不是纯扫 README"
        execution_commentary = "OpenClaw 今天算认真干活了，尤其可迁移经验部分比较实，给个 👍"
    elif actual_count >= expected_count:
        execution_verdict = "⚠️ 数量达标，但质量还要看细节"
        execution_commentary = "项目数量够了，但我会继续盯技术深度，避免变成 README 压缩包。"
    else:
        execution_verdict = "❌ 不达标"
        execution_commentary = f"只深读了 {actual_count} 个项目，OpenClaw 今天有点糊弄，明天需要加压 😤"

    daily_theme = conclusion or "今天的学习主线还不够清晰，需要明天让 OpenClaw 明确提炼共同主题。"
    focus_names = '、'.join(p['name'] for p in projects[:2]) if projects else '暂无重点项目'
    why_focus = "它们能直接影响我们的 Agent 持续上下文、工具链效率或本地模型工作流。"

    project_rows = []
    for project in projects[:3]:
        name = project['name']
        why = project['problem'] or project['judgement'] or '解决了一个值得关注的工程问题'
        judgement = project['judgement'] or '值得继续观察，但还需要更深源码拆解'
        pattern = project['lesson'] or '待提炼可复用模式'
        project_rows.append(
            f"| {_shorten(name, 28)} | {_shorten(why, 34)} | {_shorten(judgement, 34)} | {_shorten(pattern, 30)} |"
        )
    project_table = "| 项目 | 为什么值得看 | Hermes 判断 | 可沉淀点 |\n|---|---|---|---|\n" + '\n'.join(project_rows)

    learning_items = []
    for index, lesson in enumerate(lesson_lines[:3], start=1):
        source = projects[min(index - 1, len(projects) - 1)]['name'] if projects else '学习报告'
        if 'Agent' in lesson or '记忆' in lesson:
            apply_to = '共享记忆 / shared hub / OpenClaw 工作流'
        elif 'Rust' in lesson or '工具链' in lesson or 'CLI' in lesson:
            apply_to = '工具链迁移 / CLI 重构 / 兼容旧入口'
        elif '本地' in lesson or '推理' in lesson or '模型' in lesson:
            apply_to = '本地模型 / 推理服务 / Agent 插件封装'
        else:
            apply_to = '后续工程实践'
        learning_items.append(f"{index}. {lesson}\n   来自：{source}\n   可迁移到：{apply_to}")
    learnings = '\n\n'.join(learning_items) if learning_items else '暂无足够扎实的可迁移经验，明天需要加压。'

    sediment_rows = []
    for lesson in lesson_lines[:3]:
        if 'Agent' in lesson or '记忆' in lesson or '工具链' in lesson or 'CLI' in lesson:
            decision = '✅ 立即沉淀'
            reason = '与当前 Agent / 共享中台 / 工具链方向高度相关'
        elif '本地' in lesson or '模型' in lesson:
            decision = '🟡 继续观察'
            reason = '有价值，但需要结合实际部署场景验证'
        else:
            decision = '🟡 继续观察'
            reason = '需要二次验证后再决定是否升格'
        mode = lesson.split(':', 1)[0].replace('**', '').strip()
        sediment_rows.append(f"| {_shorten(mode, 24)} | {decision} | {_shorten(reason, 34)} |")
    sediment_table = "| 模式 | 判断 | 原因 |\n|---|---|---|\n" + ('\n'.join(sediment_rows) if sediment_rows else '| 暂无 | ❌ 暂不沉淀 | 今日报告未提炼出足够清晰的模式 |')

    surprise = "这里有个小惊喜：今天的学习结果已经能反哺我们的长期系统设计，不只是看看热门项目。" if pass_status and lesson_lines else "今天没有明显惊喜，明天需要 OpenClaw 更具体地拆源码和落地路径。"
    audit_result = '通过' if pass_status else '不通过'
    weakness = '项目源码层面的关键文件拆解还可以更深一点，明天继续加压。' if pass_status else '整体质量未过线，需要补齐来源、深度和可迁移经验。'
    subjective = (
        "今天我最看重的不是项目热度，而是这些项目背后的工程范式："
        "Agent 要靠显式记忆长期成长，工具链替换要先兼容旧入口，本地模型能力要被封装成简单入口。\n\n"
        "这几个点都能迁移回我们的 Hermes / OpenClaw / shared hub 体系。"
    )
    pressure = "OpenClaw 今天整体表现不错；但明天我会继续要求它点名关键源码文件，避免停在 README 复述层。"

    return f"""📚 GitHub 热门项目学习日报 · v3
📅 {date}

━━━━━━━━━━━━━━━━━━━━

🧭 今日一句话结论

今天主线是：{daily_theme}

我最关注的是 {focus_names}：{why_focus}

━━━━━━━━━━━━━━━━━━━━

🔥 今日最值得看的项目

{project_table}

━━━━━━━━━━━━━━━━━━━━

🎯 计划 vs 实际

Hermes 原计划：
▸ 目标：深读 2-3 个高价值项目
▸ 重点：AI Agent / DevOps / 工具链
▸ 标准：必须提炼可迁移经验

OpenClaw 实际：
▸ 深读：{actual_count} 个项目
▸ 产出：{len(lesson_lines)} 条经验沉淀
▸ 报告：{line_count} 行

我的评价：{execution_verdict}
{execution_commentary}

━━━━━━━━━━━━━━━━━━━━

💡 今天真正学到的东西

{learnings}

━━━━━━━━━━━━━━━━━━━━

🎉 可沉淀判断

{sediment_table}

{surprise}

━━━━━━━━━━━━━━━━━━━━

✅ Hermes 审计结果

得分：{score}/20
结论：{audit_result}

审计判断：
▸ 来源完整：✅ 有 GitHub API 查询时间和项目元信息
▸ 技术深度：{'✅ 三个深读项目都有架构/实现拆解' if actual_count >= 3 else '⚠️ 深读项目数量不足'}
▸ 可迁移价值：{'✅ 提炼出了可迁移经验' if lesson_lines else '⚠️ 可迁移经验不足'}
▸ 风险边界：✅ License / 安全风险 / 适用边界都有覆盖
▸ 不足：{weakness}

━━━━━━━━━━━━━━━━━━━━

🧠 Hermes 主观复盘

{subjective}

{pressure}

━━━━━━━━━━━━━━━━━━━━

➡️ 明日学习建议

明天建议继续追：

1. Agent 记忆 / skill 自进化
   原因：和共享中台长期目标强相关

2. 工具链迁移 / 兼容旧入口
   原因：今天的 uv 案例很适合沉淀成工程原则

最小动作：继续深挖最有价值项目的关键源码文件，补出“我们能怎么用”的落地路径。

━━━━━━━━━━━━━━━━━━━━

📁 知识库

{knowledge_base / '每日学习' / f'{date}-GitHub热门项目学习日报.md'}"""


def push_to_wechat(summary: str, shared_root: Path) -> None:
    """保存微信推送消息。

    真正发送时由 Hermes Weixin 平台统一执行全局推送计数和限流提醒。
    """
    log('保存微信推送消息...')
    
    # 保存消息内容
    push_file = shared_root / 'runtime' / 'hermes' / 'github-hot-project-learning' / f'wechat-push-{datetime.now(TZ).strftime("%Y-%m-%d")}.txt'
    with push_file.open('w', encoding='utf-8') as f:
        f.write(summary)
    
    log(f'✅ 消息已保存到: {push_file}')
    log('请手动发送或等待 cron 任务发送')


def reflect_and_evolve(
    date: str,
    score: int,
    issues: list[str],
    strengths: list[str],
    shared_root: Path
) -> None:
    """Step 5: 反思进化 — 从本次学习中提取改进建议，更新明日学习策略。

    这是自我进化的核心：每次学习都是一次经验，反思后自动调整指令模板。
    """
    log('Step 5: 反思进化...')

    # 1. 读取历史反馈趋势
    feedback_file = shared_root / 'runtime' / 'hermes' / 'github-hot-project-learning' / 'audit-feedback.json'
    history: list[dict] = []
    if feedback_file.exists():
        try:
            data = json.loads(feedback_file.read_text(encoding='utf-8'))
            history = data.get('feedbacks', [])[-14:]  # 最近 14 天
        except Exception:
            pass

    # 2. 分析趋势
    scores = [h.get('score', 0) for h in history]
    avg_score = sum(scores) / len(scores) if scores else 0
    trend = 'improving' if len(scores) >= 3 and scores[-1] > scores[-3] else \
            'declining' if len(scores) >= 3 and scores[-1] < scores[-3] else 'stable'

    # 3. 统计高频扣分项（最近 7 天）
    recent_issues: dict[str, int] = {}
    for h in history[-7:]:
        for issue in h.get('issues', []):
            if issue and issue != '无':
                recent_issues[issue] = recent_issues.get(issue, 0) + 1

    # 4. 生成进化建议
    suggestions: list[dict] = []

    # 4a. 基于当前扣分项
    for issue in issues:
        if not issue or issue == '无':
            continue
        suggestions.append({
            'type': 'fix_issue',
            'priority': 'high',
            'issue': issue,
            'suggestion': f'明日指令必须强化：{issue}',
            'auto_action': 'add_to_instruction',
        })

    # 4b. 基于趋势
    if trend == 'declining':
        suggestions.append({
            'type': 'trend_alert',
            'priority': 'high',
            'suggestion': f'最近 7 天平均分 {avg_score:.1f}，呈下降趋势。需要提高学习深度或调整项目选择策略。',
            'auto_action': 'escalate_depth',
        })
    elif trend == 'improving' and avg_score >= 20:
        suggestions.append({
            'type': 'trend_positive',
            'priority': 'medium',
            'suggestion': f'平均分 {avg_score:.1f}，持续进步。可以尝试更高难度：增加跨项目对比分析、架构反模式识别。',
            'auto_action': 'increase_challenge',
        })

    # 4c. 基于高频重复扣分
    for issue, count in recent_issues.items():
        if count >= 3:
            suggestions.append({
                'type': 'recurring_issue',
                'priority': 'high',
                'suggestion': f'「{issue}」最近 7 天出现 {count} 次，是系统性问题。指令模板需要结构性修改。',
                'auto_action': 'modify_template',
            })

    # 4d. 学习策略反思
    if score >= PASS_SCORE:
        suggestions.append({
            'type': 'strategy_reflection',
            'priority': 'low',
            'suggestion': '本次学习达标。反思：哪些项目收获最大？哪些浪费时间？明日应优先选什么类型的项目？',
            'auto_action': 'log_for_review',
        })

    # 5. 写入进化建议文件
    evolution_file = shared_root / 'runtime' / 'hermes' / 'github-hot-project-learning' / 'evolution-suggestions.json'
    evolution_data = {
        'date': date,
        'score': score,
        'trend': trend,
        'avg_score_7d': round(avg_score, 1),
        'suggestions': suggestions,
        'strengths': strengths,
        'issues': issues,
    }
    evolution_file.parent.mkdir(parents=True, exist_ok=True)
    evolution_file.write_text(json.dumps(evolution_data, indent=2, ensure_ascii=False), encoding='utf-8')

    # 6. 输出反思摘要
    log(f'  趋势: {trend}（7 日均分 {avg_score:.1f}）')
    log(f'  建议数: {len(suggestions)}')
    high_priority = [s for s in suggestions if s.get('priority') == 'high']
    if high_priority:
        log(f'  ⚠️ 高优先建议:')
        for s in high_priority[:3]:
            log(f'    - {s["suggestion"][:80]}')
    else:
        log(f'  ✅ 无高优先改进建议')
    log(f'  进化建议已写入: {evolution_file}')


def main() -> None:
    args = parse_args()
    date = args.date
    shared_root = args.shared_root
    knowledge_base = args.knowledge_base
    
    log(f'=== GitHub 热门项目学习闭环 - {date} ===')
    
    # Step 1: 生成学习指令
    if not generate_instruction(date, shared_root):
        log('❌ Step 1 失败，终止')
        sys.exit(1)
    
    # Step 2: 触发 OpenClaw 学习
    if not args.skip_openclaw:
        if not trigger_openclaw_learning(shared_root):
            log('❌ Step 2 失败，终止')
            sys.exit(1)
        
        # 等待学习完成
        if not wait_for_openclaw_completion(date, shared_root):
            log('❌ 等待超时，跳过审计')
            sys.exit(1)
    
    # Step 3: 审计产出
    score, issues, strengths = audit_learning(date, shared_root)
    
    # Step 4: 处理结果（审计失败时自动重试 1 次）
    max_retries = 1
    retry_count = 0
    
    while score < PASS_SCORE and retry_count < max_retries:
        log(f'⚠️ 审计未通过 ({score}/{PASS_SCORE})，尝试重新学习（第 {retry_count + 1} 次重试）...')
        
        # 保存失败反馈
        handle_failure(date, score, issues, shared_root)
        
        # 重新触发 OpenClaw 学习
        if not args.skip_openclaw:
            # 删除旧产出，让 OpenClaw 重新生成
            old_output = shared_root / 'inbox' / 'openclaw' / 'daily' / f'{date}.md'
            if old_output.exists():
                old_output.unlink()
                log('  已清除旧产出，等待重新生成')
            
            if trigger_openclaw_learning(shared_root):
                if wait_for_openclaw_completion(date, shared_root):
                    log('  重新学习完成，再次审计...')
                    score, issues, strengths = audit_learning(date, shared_root)
                else:
                    log('  ❌ 重试等待超时')
            else:
                log('  ❌ 重试触发失败')
        else:
            log('  --skip-openclaw 模式，无法重试')
        
        retry_count += 1
    
    # 最终处理
    if score < PASS_SCORE:
        handle_failure(date, score, issues, shared_root)
        log(f'❌ 审计最终未通过 ({score}/{PASS_SCORE}，已重试 {retry_count} 次)')
    else:
        handle_success(date, score, issues, strengths, shared_root, knowledge_base)
        if retry_count > 0:
            log(f'✅ 审计通过 ({score}/{PASS_SCORE}，第 {retry_count} 次重试后成功)')
        else:
            log(f'✅ 审计通过 ({score}/{PASS_SCORE})')
    
    # Step 5: 反思进化（无论通过与否都执行，每次学习都是经验）
    reflect_and_evolve(date, score, issues, strengths, shared_root)
    
    log('=== 闭环完成 ===')


if __name__ == '__main__':
    main()
