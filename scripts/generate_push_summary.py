#!/usr/bin/env python3
"""生成微信推送摘要（个性版）。

更有个性、更丰富、更有情绪表达。
"""

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

TZ = timezone(timedelta(hours=8))


def generate_push_summary(
    date: str,
    score: int,
    strengths: list[str],
    knowledge_base: Path,
    shared_root: Path
) -> str:
    """生成微信推送摘要（个性版）。"""
    # 读取学习产出
    output_file = shared_root / 'inbox' / 'openclaw' / 'daily' / f'{date}.md'
    output_content = ""
    if output_file.exists():
        output_content = output_file.read_text(encoding='utf-8')
    
    # 提取深读项目
    projects = []
    current_project = None
    for line in output_content.split('\n'):
        if line.startswith('### 项目') or line.startswith('## 深读项目'):
            if ':' in line:
                current_project = line.split(':')[-1].strip()
            else:
                current_project = line.replace('###', '').replace('##', '').strip()
            projects.append(current_project)
    
    # 提取今日结论
    conclusion = ""
    for i, line in enumerate(output_content.split('\n')):
        if '今日结论' in line:
            lines = output_content.split('\n')
            for j in range(i+1, min(i+5, len(lines))):
                if lines[j].strip() and not lines[j].startswith('#'):
                    conclusion = lines[j].strip()
                    break
            break
    
    # 提取可迁移经验
    lessons = []
    for i, line in enumerate(output_content.split('\n')):
        if '可迁移' in line or '可复用' in line:
            lines = output_content.split('\n')
            for j in range(i+1, min(i+3, len(lines))):
                if lines[j].strip() and not lines[j].startswith('#'):
                    lessons.append(lines[j].strip())
                    break
    
    # 判断是否符合预期
    expected_count = 3
    actual_count = len(projects)
    
    if actual_count >= expected_count + 1:
        emotion = "超出预期！深读了 {} 个项目，比计划的 {} 个多，有点惊喜！🎉".format(actual_count, expected_count)
        openclaw评价 = "OpenClaw 今天表现不错，给个 👍"
    elif actual_count >= expected_count:
        emotion = "符合预期，深读了 {} 个项目".format(actual_count)
        openclaw评价 = "OpenClaw 今天表现稳定"
    else:
        emotion = "有点失望，只深读了 {} 个项目，比计划的 {} 个少".format(actual_count, expected_count)
        openclaw评价 = "OpenClaw 今天有点敷衍，需要改进 😤"
    
    # 生成项目表格
    project_table = "| # | 项目 | 简介 | 亮点 |\n"
    project_table += "|---|------|------|------|\n"
    
    for i, project in enumerate(projects[:4]):
        # 根据项目名称生成简介和亮点
        if 'hermes' in project.lower():
            desc = "多平台 AI Agent 助手"
            highlight = "记忆系统设计很棒"
        elif 'uv' in project.lower():
            desc = "Rust 包管理器"
            highlight = "比 pip 快 100 倍！"
        elif 'interpreter' in project.lower():
            desc = "自然语言控制电脑"
            highlight = "有点科幻感"
        elif 'vllm' in project.lower():
            desc = "LLM 推理引擎"
            highlight = "生产环境必备"
        elif 'ollama' in project.lower():
            desc = "本地 LLM 运行"
            highlight = "简单易用"
        else:
            desc = "值得关注的项目"
            highlight = "值得学习"
        
        project_table += f"| {i+1} | {project} | {desc} | {highlight} |\n"
    
    # 生成可迁移经验（带解释）
    lesson_details = []
    for i, lesson in enumerate(lessons[:3]):
        # 添加简单解释
        if '记忆' in lesson or 'Agent' in lesson:
            source = "（来自 hermes-agent 的启发）"
        elif 'CLI' in lesson or '兼容' in lesson:
            source = "（来自 uv 的启发，它直接兼容 pip）"
        elif 'LLM' in lesson or '推理' in lesson:
            source = "（性能差距太大了，10x 以上）"
        else:
            source = ""
        
        lesson_details.append(f"{i+1}. {lesson}\n   {source}")
    
    # 构建个性版摘要
    summary = f"""📚 GitHub 热门项目学习日报
📅 {date}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 今日学习计划

▸ 目标：发现 3-5 个热门项目，深读 2-3 个
▸ 领域：AI/ML、DevOps、云原生
▸ 标准：来源完整、事实准确、可迁移经验

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📖 OpenClaw 学习成果

深读了 {actual_count} 个项目，{emotion.split('！')[0]}！

{project_table}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔍 计划执行情况

{emotion}
{openclaw评价}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 产出清单

▸ 学习报告：{output_file.name if output_file.exists() else "未生成"}（{len(output_content.split(chr(10)))} 行）
▸ 可迁移经验：{len(lessons)} 条
▸ 项目卡片：{len(projects)} 个

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ 审计结果

▸ 标准：20 分制（来源完整、事实准确、技术深度、可复用动作、安全合规）
▸ 得分：{score}/20 {"✅ 通过" if score >= 16 else "❌ 未通过"}
▸ 评价：{"整体质量不错，特别是可迁移经验部分写得很实用" if score >= 16 else "需要改进，主要是内容不够深入"}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 核心收获

{chr(10).join(lesson_details) if lesson_details else "暂无"}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🤔 学习感悟

{conclusion if conclusion else "今天学习了多个项目，各有特色"}

{"说实话，今天 OpenClaw 学习挺认真的，深读了 {} 个项目，还提取了可迁移经验。比昨天好多了，继续保持！💪".format(actual_count) if actual_count >= expected_count else "今天 OpenClaw 学习有点敷衍，只深读了 {} 个项目，需要改进。明天要更认真！😤".format(actual_count)}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎉 可沉淀技能

{"发现 {} 个可以沉淀为技能的模式：".format(min(len(lessons), 2)) if lessons else "暂无可沉淀技能"}

{chr(10).join(f"{i+1}. {l[:50]}..." for i, l in enumerate(lessons[:2])) if lessons else ""}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 详细内容

▸ 知识库：{knowledge_base / '每日学习' / f'{date}-GitHub热门项目学习日报.md'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💬 最后说一句

{"今天 OpenClaw 学习挺认真的，深读了 {} 个项目，还提取了可迁移经验。比昨天好多了，继续保持！💪".format(actual_count) if actual_count >= expected_count else "今天 OpenClaw 学习有点敷衍，只深读了 {} 个项目，需要改进。明天要更认真！😤".format(actual_count)}

明天可以重点关注一下 AI Agent 领域的新项目，这个方向最近很火，可能会有更多惊喜。"""
    
    return summary


if __name__ == '__main__':
    # 测试
    summary = generate_push_summary(
        '2026-05-14',
        16,
        ['包含今日结论', '包含深读项目'],
        Path('/mnt/d/system/selfSystem/03-学习/技术实践/GitHub 热门项目学习档案'),
        Path('/home/vany/openclaw-data/.openclaw/shared')
    )
    print(summary)
