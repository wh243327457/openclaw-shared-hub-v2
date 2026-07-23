#!/usr/bin/env python3
"""读书计划编排器。

每日读书闭环：
1. 读取书单队列 → 确定今日读哪本书哪章
2. AI 提炼章节要点（核心论点/案例/可复用行动）
3. 写入读书笔记
4. 生成微信推送摘要
5. 反思：章节质量评分 → 更新进化建议
"""

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

DEFAULT_SHARED_ROOT = Path(__file__).resolve().parents[1]
TZ = timezone(timedelta(hours=8))
QUEUE_FILE = 'runtime/hermes/reading-plan/book-queue.json'
NOTES_DIR = Path('/mnt/d/system/selfSystem/03-学习/读书笔记/')


def today_cst() -> str:
    return datetime.now(TZ).date().isoformat()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--date', default=today_cst())
    parser.add_argument('--shared-root', type=Path, default=DEFAULT_SHARED_ROOT)
    parser.add_argument('--book-id', help='指定读哪本书（跳过队列选择）')
    parser.add_argument('--chapter', type=int, help='指定读第几章')
    parser.add_argument('--complete-chapter', type=int, help='确认章节笔记已落盘后推进队列')
    parser.add_argument('--list', action='store_true', help='列出书单')
    parser.add_argument('--reflect', action='store_true', help='执行反思（阅读完成后调用）')
    parser.add_argument('--score', type=float, help='本次阅读质量评分')
    parser.add_argument('--max-score', type=float, default=100, help='满分')
    parser.add_argument('--issues', nargs='*', default=[], help='本次问题')
    parser.add_argument('--strengths', nargs='*', default=[], help='本次优势')
    return parser.parse_args()


def log(msg: str) -> None:
    ts = datetime.now(TZ).strftime('%H:%M:%S')
    print(f'[{ts}] {msg}')


def load_queue(shared_root: Path) -> dict:
    path = shared_root / QUEUE_FILE
    if not path.exists():
        log(f'❌ 书单队列不存在: {path}')
        sys.exit(1)
    return json.loads(path.read_text(encoding='utf-8'))


def save_queue(queue: dict, shared_root: Path) -> None:
    path = shared_root / QUEUE_FILE
    path.write_text(json.dumps(queue, indent=2, ensure_ascii=False), encoding='utf-8')


def get_current_book(queue: dict) -> dict | None:
    """获取当前正在读的书，如果没有则从队列中选优先级最高的。"""
    if queue.get('current_book'):
        for book in queue['queue']:
            if book['id'] == queue['current_book']:
                return book

    # 选优先级最高的 pending 书
    pending = [b for b in queue['queue'] if b['status'] == 'pending']
    if not pending:
        return None
    pending.sort(key=lambda b: b.get('priority', 99))
    return pending[0]


def complete_chapter(queue: dict, shared_root: Path, book: dict, chapter: int, date: str) -> None:
    """确认笔记存在后推进章节，避免编排阶段提前写坏进度。"""
    title = book.get('title_cn') or book['title']
    filename_title = ''.join(char for char in title if char.isalnum())
    notes = sorted({
        *NOTES_DIR.glob(f'*-{title}-第{chapter}章.md'),
        *NOTES_DIR.glob(f'*-{filename_title}-第{chapter}章.md'),
    })
    if not notes:
        log(f'❌ 第 {chapter} 章笔记不存在，拒绝推进队列')
        sys.exit(1)

    current = book.get('current_chapter', 0)
    if chapter < current:
        log(f'✅ 第 {chapter} 章已完成，当前队列已在第 {current} 章')
        return
    if chapter > current + 1:
        log(f'❌ 章节不连续：当前第 {current} 章，不能直接完成第 {chapter} 章')
        sys.exit(1)

    book['status'] = 'reading'
    book['current_chapter'] = chapter
    queue['current_book'] = book['id']
    if chapter >= book.get('chapters', chapter):
        book['status'] = 'completed'
        book['completed_at'] = date
    save_queue(queue, shared_root)
    log(f'✅ 已确认《{title}》第 {chapter} 章完成: {notes[-1]}')


def generate_chapter_prompt(book: dict, chapter_num: int) -> str:
    """生成章节阅读指令（给 AI 的 prompt）。"""
    title = book.get('title_cn') or book['title']
    author = book['author']
    domain = book['domain']

    return f"""请深度阅读《{title}》（{author}）第 {chapter_num} 章，完成以下任务：

## 任务

1. **提取核心论点**：这一章的核心观点是什么？用一句话概括
2. **关键案例**：列出 2-3 个最有说服力的案例/故事，每个用 2-3 句话描述 + 启示
3. **可复用行动**：提炼 2-3 条「当 [场景] 时，应该 [行动]，因为 [原因]」格式的行动指南
4. **与已有知识关联**：这一章的内容跟以下领域有什么关联？
   - 沟通技巧
   - 谈判技巧
   - 金融/投资思维
   - AI/技术决策
5. **章节评分**（1-5 星）：
   - 实用性：能直接用在工作/生活中吗？
   - 新鲜度：是全新知识还是已知内容？
   - 行动性：读完能立刻行动吗？

## 领域背景
这本书属于「{domain}」领域，重点提炼与实际工作/生活相关的可操作建议。

## 输出格式
请用中文输出，结构清晰，每个部分有明确标题。核心论点用引用格式，可复用行动用「当...时，应该...」格式。"""


def generate_push_summary(book: dict, chapter_num: int, content: str) -> str:
    """生成微信推送摘要。"""
    title = book.get('title_cn') or book['title']
    total = book.get('chapters', '?')
    progress = f'{chapter_num}/{total}' if isinstance(total, int) else f'第 {chapter_num} 章'
    pct = f' ({chapter_num*100//total}%)' if isinstance(total, int) else ''

    return f"""📚 今日读书 · 《{title}》第 {chapter_num} 章

{content}

📊 进度：{progress}{pct}
🏷️ 领域：{book['domain']}"""


def generate_practice_prompt(book: dict, day: int, total_days: int, notes_dir: Path) -> str:
    """生成刻意练习指令。读完一本书后的巩固阶段。"""
    title = book.get('title_cn') or book['title']
    domain = book['domain']

    return f"""## 《{title}》刻意练习 · 第 {day}/{total_days} 天

这本书属于「{domain}」领域。现在进入巩固阶段，通过实际场景练习书中核心概念。

### 今日练习任务

请根据《{title}》的核心内容，设计今天的刻意练习：

1. **场景模拟**：设计 2-3 个真实场景，让我练习书中最重要的概念
   - 场景要具体（有角色、有冲突、有目标）
   - 难度递进：第 1 天基础场景，第 2 天复杂场景，第 3 天综合场景

2. **我的练习**：对每个场景，我会尝试用书中的方法应对，请给出反馈
   - 我哪里做得好？
   - 我哪里可以改进？
   - 书中的标准做法是什么？

3. **今日反思**：
   - 今天练习中最有收获的一点
   - 还不熟练的地方
   - 明天（或下次实战时）要注意什么

4. **实战作业**：给我一个可以在 24 小时内完成的真实任务
   - 比如：今天跟同事沟通时尝试用 XX 方法
   - 明天汇报时用 YY 框架

### 领域特化
- 如果是「思维模型」：练习识别偏见、做预测、用检查清单
- 如果是「沟通技巧」：练习标注情绪、重构问题、非暴力表达
- 如果是「谈判实战」：练习找 BATNA、锚定、利益交换
- 如果是「思维实战」：练习多元模型分析、决策日志

### 输出格式
用中文，结构清晰。场景要生动具体，反馈要直接可操作。"""


def main() -> None:
    args = parse_args()
    shared_root = args.shared_root

    # 加载书单
    queue = load_queue(shared_root)

    if args.list:
        print('📚 读书队列：\n')
        for b in queue['queue']:
            status = '📖' if b['status'] == 'reading' else '⏳' if b['status'] == 'pending' else '✅'
            ch = b.get('current_chapter', 0)
            total = b.get('chapters', '?')
            practice = ' + 刻意练习' if b.get('practice_after') else ''
            print(f'{status} [{b.get("priority", "?")}] {b.get("title_cn") or b["title"]} ({b["author"]}) — {ch}/{total} — {b["domain"]}{practice}')
        return

    # 反思模式
    if args.reflect:
        from reflection_engine import ReflectionEngine
        engine = ReflectionEngine('reading-plan', shared_root)
        if args.score is not None:
            engine.record_feedback(
                score=args.score,
                max_score=args.max_score,
                issues=args.issues or [],
                strengths=args.strengths or [],
            )
        suggestions = engine.reflect()
        engine.save()
        log(f'✅ 读书反思完成，{len(suggestions)} 条建议')
        for s in suggestions:
            log(f'   [{s.priority}] {s.message}')
        enhancement = engine.get_instruction_enhancement()
        if enhancement:
            print('\n--- 明日指令增强 ---')
            print(enhancement)
        return

    # 检查是否在刻意练习阶段
    practice_state = queue.get('practice_state')
    if practice_state and practice_state.get('active'):
        book_id = practice_state['book_id']
        day = practice_state['day']
        total_days = practice_state.get('total_days', 3)

        # 找到对应的书
        book = next((b for b in queue['queue'] if b['id'] == book_id), None)
        if book:
            title = book.get('title_cn') or book['title']

            if day > total_days:
                # 刻意练习完成，进入下一本书
                log(f'✅ 《{title}》刻意练习完成！')
                practice_state['active'] = False
                queue['practice_state'] = practice_state
                save_queue(queue, shared_root)
                # 继续选下一本书
            else:
                log(f'🎯 刻意练习：《{title}》第 {day}/{total_days} 天')
                prompt = generate_practice_prompt(book, day, total_days,
                    shared_root / 'runtime' / 'hermes' / 'reading-plan')
                instruction_file = shared_root / 'runtime' / 'hermes' / 'reading-plan' / 'today-instruction.md'
                instruction_file.parent.mkdir(parents=True, exist_ok=True)
                instruction_file.write_text(prompt, encoding='utf-8')
                practice_state['day'] = day + 1
                queue['practice_state'] = practice_state
                save_queue(queue, shared_root)
                log(f'✅ 刻意练习指令已生成')
                return

    # 获取当前书
    book = get_current_book(queue)
    if not book and not practice_state:
        log('✅ 所有书都读完了！')
        return

    if not book:
        log('✅ 所有书都读完了！')
        return

    if args.complete_chapter is not None:
        complete_chapter(queue, shared_root, book, args.complete_chapter, args.date)
        return

    # 确定章节
    chapter = args.chapter or (book.get('current_chapter', 0) + 1)
    total_chapters = book.get('chapters', 999)

    if chapter > total_chapters:
        title = book.get('title_cn') or book['title']
        log(f'✅ 《{title}》已读完！')
        book['status'] = 'completed'
        book['completed_at'] = args.date
        queue['completed'].append({
            'id': book['id'],
            'title': title,
            'completed_at': args.date,
            'chapters': total_chapters,
        })
        queue['current_book'] = None

        # 检查是否需要进入刻意练习
        if book.get('practice_after'):
            practice_days = queue.get('reading_config', {}).get('practice_days', 3)
            log(f'🎯 进入刻意练习阶段（{practice_days} 天）')
            queue['practice_state'] = {
                'active': True,
                'book_id': book['id'],
                'day': 1,
                'total_days': practice_days,
                'started_at': args.date,
            }

        save_queue(queue, shared_root)
        return

    title = book.get('title_cn') or book['title']
    log(f'📖 今日读书：《{title}》第 {chapter} 章')

    # 生成章节阅读指令
    prompt = generate_chapter_prompt(book, chapter)

    # 写入指令文件
    instruction_file = shared_root / 'runtime' / 'hermes' / 'reading-plan' / 'today-instruction.md'
    instruction_file.parent.mkdir(parents=True, exist_ok=True)
    instruction_file.write_text(prompt, encoding='utf-8')

    log(f'✅ 阅读指令已生成: {instruction_file}')
    log(f'   书: {title}')
    log(f'   章节: 第 {chapter} 章')
    log(f'   领域: {book["domain"]}')
    log(f'   进度: {chapter}/{total_chapters} ({chapter*100//total_chapters}%)')


if __name__ == '__main__':
    main()
