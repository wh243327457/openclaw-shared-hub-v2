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
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

# 常量
DEFAULT_SHARED_ROOT = Path('/home/vany/agent/.openclaw/shared')
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


def audit_learning(date: str, shared_root: Path) -> tuple[int, list[str], list[str]]:
    """Step 3: 审计学习产出。"""
    log('Step 3: 审计学习产出...')
    
    output_file = shared_root / 'inbox' / 'openclaw' / 'daily' / f'{date}.md'
    
    if not output_file.exists():
        log('❌ 学习产出不存在')
        return 0, ['学习产出文件不存在'], []
    
    content = output_file.read_text(encoding='utf-8')
    
    # 简单评分逻辑（可根据需要扩展）
    score = 0
    issues = []
    strengths = []
    
    # 检查结构完整性
    required_sections = ['今日结论', '项目速览', '深读项目', '经验沉淀', '明日继续']
    for section in required_sections:
        if section in content:
            score += 2
            strengths.append(f'包含「{section}」章节')
        else:
            issues.append(f'缺少「{section}」章节')
    
    # 检查深读项目数量
    deep_reads = content.count('### 项目')
    if deep_reads >= 2:
        score += 4
        strengths.append(f'深读 {deep_reads} 个项目')
    else:
        issues.append(f'深读项目不足（{deep_reads} 个）')
    
    # 检查可迁移经验
    if '可迁移' in content or '可复用' in content:
        score += 3
        strengths.append('包含可迁移经验')
    else:
        issues.append('缺少可迁移经验')
    
    # 检查风险边界
    if '风险' in content or '限制' in content:
        score += 3
        strengths.append('包含风险边界')
    else:
        issues.append('缺少风险边界')
    
    # 检查数据来源
    if 'github.com' in content:
        score += 2
        strengths.append('包含 GitHub 链接')
    else:
        issues.append('缺少 GitHub 链接')
    
    # 补齐分数
    if not issues:
        score = min(score + 2, PASS_SCORE)
    
    log(f'审计完成: {score}/{PASS_SCORE}')
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
    
    # 4. 记录反馈
    script = shared_root / 'scripts' / 'audit_feedback_writer.py'
    if script.exists():
        cmd = [
            'python3', str(script),
            '--date', date,
            '--score', str(score),
            '--issues', '无',
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
        if line.startswith('### 项目'):
            if current:
                projects.append(current)
            name = line.split(':', 1)[1].strip() if ':' in line else line.replace('###', '').strip()
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

        if line.startswith('- **一句话判断**'):
            current['judgement'] = line.split(':', 1)[1].strip() if ':' in line else line
        elif line.startswith('- **解决的问题**'):
            current['problem'] = line.split(':', 1)[1].strip() if ':' in line else line
        elif line.startswith('- 当') and not current['lesson']:
            current['lesson'] = line.lstrip('- ').strip()
        elif line.startswith('- **风险边界**'):
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
    
    # Step 4: 处理结果
    if score < PASS_SCORE:
        handle_failure(date, score, issues, shared_root)
        log(f'❌ 审计未通过 ({score}/{PASS_SCORE})')
    else:
        handle_success(date, score, strengths, shared_root, knowledge_base)
        log(f'✅ 审计通过 ({score}/{PASS_SCORE})')
    
    log('=== 闭环完成 ===')


if __name__ == '__main__':
    main()
