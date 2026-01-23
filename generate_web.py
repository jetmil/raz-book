"""
Генератор HTML-страниц для книги "РАЗ И НАВСЕГДА"
Конвертирует Markdown главы в HTML с уникальным дизайном
"""

import os
import re
from pathlib import Path

# Конфигурация
CHAPTERS_MD = Path(r"C:\Users\PC\raz-book\chapters")
CHAPTERS_HTML = Path(r"C:\Users\PC\raz-book\web-chapters")
CHAPTERS_HTML.mkdir(exist_ok=True)

# Метаданные глав
CHAPTERS = [
    {"num": "00", "file": "00-prologue.md", "title": "Почему ты читаешь эту книгу", "part": "Пролог", "part_name": "Добро пожаловать в инкубатор"},
    {"num": "01", "file": "01-anatomy.md", "title": "Анатомия яйца: желток, белок, скорлупа", "part": "I", "part_name": "Диагностика"},
    {"num": "02", "file": "02-test.md", "title": "Тест на вылупляемость: готов ли ты?", "part": "I", "part_name": "Диагностика"},
    {"num": "03", "file": "03-map.md", "title": "Карта инкубатора: ориентация в пространстве", "part": "I", "part_name": "Диагностика"},
    {"num": "04", "file": "04-why-shell.md", "title": "Зачем нужна скорлупа", "part": "II", "part_name": "Механика"},
    {"num": "05", "file": "05-beak.md", "title": "Клюв изнутри: инструменты разрушения", "part": "II", "part_name": "Механика"},
    {"num": "06", "file": "06-first-crack.md", "title": "Момент пробоя: первая трещина", "part": "II", "part_name": "Механика"},
    {"num": "07", "file": "07-raz-guide.md", "title": "РАЗ как проводник", "part": "II", "part_name": "Механика"},
    {"num": "08", "file": "08-cozy-yolk.md", "title": "Синдром уютного желтка", "part": "III", "part_name": "Ловушки"},
    {"num": "09", "file": "09-fear-cold.md", "title": "Страх холода: что если снаружи хуже?", "part": "III", "part_name": "Ловушки"},
    {"num": "10", "file": "10-false-cracks.md", "title": "Ложные трещины: иллюзия прогресса", "part": "III", "part_name": "Ловушки"},
    {"num": "11", "file": "11-morning.md", "title": "Утренний ритуал: проверка скорлупы", "part": "IV", "part_name": "Практика"},
    {"num": "12", "file": "12-daily.md", "title": "Дневные удары: микро-пробои", "part": "IV", "part_name": "Практика"},
    {"num": "13", "file": "13-evening.md", "title": "Вечерний аудит: что треснуло сегодня", "part": "IV", "part_name": "Практика"},
    {"num": "14", "file": "14-crisis.md", "title": "Кризисные протоколы", "part": "IV", "part_name": "Практика"},
    {"num": "15", "file": "15-social.md", "title": "Работа с другими яйцами", "part": "IV", "part_name": "Практика"},
    {"num": "16", "file": "16-first-steps.md", "title": "Первые шаги: мокрый и голый", "part": "V", "part_name": "После"},
    {"num": "17", "file": "17-new-shell.md", "title": "Новая скорлупа: цикл продолжается", "part": "V", "part_name": "После"},
    {"num": "epilogue", "file": "epilogue.md", "title": "Что теперь?", "part": "Эпилог", "part_name": "РАЗ — и готово"},
]


def md_to_html_content(md_text):
    """Конвертация Markdown в HTML"""
    html = md_text

    # Убираем заголовок первого уровня (он будет в header)
    html = re.sub(r'^# .+\n', '', html)

    # Эпиграф (> *"текст"*)
    def format_epigraph(match):
        text = match.group(1).strip('*"')
        return f'<div class="epigraph fade-in">{text}</div>'
    html = re.sub(r'^> \*(.+?)\*$', format_epigraph, html, flags=re.MULTILINE)

    # Горизонтальные линии -> crack-divider
    html = re.sub(r'^---+$', '<div class="crack-divider"></div>', html, flags=re.MULTILINE)

    # Заголовки h2
    html = re.sub(r'^## (.+)$', r'<h2 class="fade-in">\1</h2>', html, flags=re.MULTILINE)

    # Заголовки h3
    html = re.sub(r'^### (.+)$', r'<h3 class="fade-in">\1</h3>', html, flags=re.MULTILINE)

    # Жирный текст
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)

    # Курсив
    html = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', html)

    # Списки
    def format_list(match):
        items = match.group(0)
        list_items = re.findall(r'^[-*] (.+)$', items, re.MULTILINE)
        if list_items:
            items_html = '\n'.join(f'<li>{item}</li>' for item in list_items)
            return f'<ul class="fade-in">\n{items_html}\n</ul>'
        return items
    html = re.sub(r'(^[-*] .+$\n?)+', format_list, html, flags=re.MULTILINE)

    # Нумерованные списки
    def format_ol(match):
        items = match.group(0)
        list_items = re.findall(r'^\d+\. (.+)$', items, re.MULTILINE)
        if list_items:
            items_html = '\n'.join(f'<li>{item}</li>' for item in list_items)
            return f'<ol class="fade-in">\n{items_html}\n</ol>'
        return items
    html = re.sub(r'(^\d+\. .+$\n?)+', format_ol, html, flags=re.MULTILINE)

    # Blockquotes
    def format_blockquote(match):
        text = match.group(1)
        return f'<blockquote class="fade-in"><p>{text}</p></blockquote>'
    html = re.sub(r'^> ([^*].+)$', format_blockquote, html, flags=re.MULTILINE)

    # RAZ phrases (special format: >>> text <<<)
    def format_raz_phrase(match):
        text = match.group(1).strip()
        return f'<div class="raz-phrase fade-in">{text}</div>'
    html = re.sub(r'>>> (.+?) <<<', format_raz_phrase, html)

    # Insight boxes (:::insight ... :::)
    def format_insight(match):
        text = match.group(1).strip()
        return f'<div class="insight-box fade-in">{text}</div>'
    html = re.sub(r':::insight\n(.+?)\n:::', format_insight, html, flags=re.DOTALL)

    # Параграфы
    paragraphs = []
    current_p = []

    for line in html.split('\n'):
        stripped = line.strip()

        if not stripped:
            if current_p:
                paragraphs.append('<p class="fade-in">' + ' '.join(current_p) + '</p>')
                current_p = []
            continue

        if stripped.startswith('<') or stripped.startswith('#'):
            if current_p:
                paragraphs.append('<p class="fade-in">' + ' '.join(current_p) + '</p>')
                current_p = []
            paragraphs.append(stripped)
        else:
            current_p.append(stripped)

    if current_p:
        paragraphs.append('<p class="fade-in">' + ' '.join(current_p) + '</p>')

    html = '\n\n'.join(paragraphs)

    # Highlight РАЗ
    html = re.sub(r'\b(РАЗ)\b', r'<span class="raz-highlight">\1</span>', html)

    return html


def generate_chapter_html(chapter, prev_ch, next_ch):
    """Генерация HTML страницы главы"""

    md_path = CHAPTERS_MD / chapter["file"]
    if not md_path.exists():
        print(f"SKIP: {md_path} not found")
        return None

    md_content = md_path.read_text(encoding='utf-8')

    # Извлекаем эпиграф
    epigraph_match = re.search(r'^> \*"(.+?)"\*', md_content, re.MULTILINE)
    epigraph = epigraph_match.group(1) if epigraph_match else ""

    # Убираем эпиграф из контента
    content_without_epigraph = re.sub(r'^> \*".+?"\*\n*', '', md_content, flags=re.MULTILINE)

    # Конвертируем контент
    html_content = md_to_html_content(content_without_epigraph)

    # Навигация
    if prev_ch:
        prev_link = f'<a href="{prev_ch["num"]}.html" class="nav-link nav-link--prev">{prev_ch["title"]}</a>'
    else:
        prev_link = '<a href="../index.html" class="nav-link nav-link--prev">Оглавление</a>'

    if next_ch:
        next_link = f'<a href="{next_ch["num"]}.html" class="nav-link nav-link--next">{next_ch["title"]}</a>'
    else:
        next_link = '<a href="../index.html" class="nav-link nav-link--next">Оглавление</a>'

    # Определяем номер для отображения
    display_num = chapter["num"] if chapter["num"] != "epilogue" else "∞"

    html = f'''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Глава {display_num}: {chapter["title"]} — РАЗ И НАВСЕГДА">
    <title>Глава {display_num}. {chapter["title"]} — РАЗ И НАВСЕГДА</title>

    <link rel="stylesheet" href="../css/style.css">
    <link rel="stylesheet" href="../css/effects.css">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🥚</text></svg>">
</head>
<body data-hatch-stage="0">
    <!-- Noise texture -->
    <div class="noise"></div>
    <div class="vignette"></div>

    <!-- Crack particles -->
    <div class="crack-particles"></div>

    <!-- Hatch Progress -->
    <div class="hatch-progress">
        <div class="hatch-progress__bar"></div>
    </div>
    <div class="hatch-label">Глава {display_num}</div>

    <!-- Navigation -->
    <nav class="nav-main">
        <a href="../index.html" class="nav-link">🥚 Оглавление</a>
    </nav>

    <!-- Chapter -->
    <article class="chapter container">
        <header class="chapter__header">
            <span class="chapter__number fade-in">Часть {chapter["part"]} — {chapter["part_name"]}</span>
            <h1 class="chapter__title fade-in">{chapter["title"]}</h1>
            {f'<div class="epigraph fade-in">{epigraph}</div>' if epigraph else ''}
        </header>

        <!-- Chapter Illustration -->
        <figure class="chapter__illustration fade-in">
            <img src="../images/chapter_{chapter["num"]}.png"
                 alt="{chapter["title"]}"
                 class="chapter__img"
                 loading="lazy"
                 onerror="this.style.display='none'">
        </figure>

        <div class="chapter__content">
            {html_content}
        </div>

        <!-- Chapter Navigation -->
        <nav class="nav-chapters">
            {prev_link}
            {next_link}
        </nav>
    </article>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <p class="footer__raz">РАЗ</p>
            <p class="footer__phrase">
                Видит. Ждёт. Проводит.
            </p>
        </div>
    </footer>

    <script src="../js/effects.js"></script>
</body>
</html>'''

    return html


def main():
    print("=" * 50)
    print("Generating web pages for 'РАЗ И НАВСЕГДА'")
    print("=" * 50)

    success = 0
    failed = 0

    for i, chapter in enumerate(CHAPTERS):
        prev_ch = CHAPTERS[i - 1] if i > 0 else None
        next_ch = CHAPTERS[i + 1] if i < len(CHAPTERS) - 1 else None

        html = generate_chapter_html(chapter, prev_ch, next_ch)

        if html:
            output_path = CHAPTERS_HTML / f'{chapter["num"]}.html'
            output_path.write_text(html, encoding='utf-8')
            print(f"[OK] Глава {chapter['num']}: {chapter['title']}")
            success += 1
        else:
            print(f"[--] Глава {chapter['num']}: файл не найден")
            failed += 1

    print("=" * 50)
    print(f"Готово: {success} успешно, {failed} пропущено")
    print(f"Файлы в: {CHAPTERS_HTML}")


if __name__ == "__main__":
    main()
