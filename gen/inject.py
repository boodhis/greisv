#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Инжектит во все страницы сайта:
  1) old-инъекция (только для разделов с инлайн-стилем): ссылка «Манифест»,
     группы «Обучение»/«Электрика», виджет «Слова дня» + wordday.js/widget.js/sw.js;
  2) рамка-бар навигации (во все страницы, кроме корневого index.html-графа):
     снятие <aside>, тонкая рамка вокруг окна с узлами-точками разделов
     (у текущего раздела подсветка .on); для страниц без style.css —
     inline-CSS рамки;
  3) заметки страницы (во все страницы): кнопка-кружок «📝» + текстовое поле,
     js/notes.js; для страниц без style.css — inline-CSS заметок;
  4) вычистка старого: стена-рисовалка (bgwall, wall-* , js/wall.js, inline wall CSS)
     и подключения js/nav.js.

Запуск из корня проекта:  python3 gen/inject.py
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLD_DIRS = ["getting-started", "homelab", "services", "guides", "articles", "hobbies"]
SKIP_OLD = {"esp32.html"}

MANIFEST_LINK = '<a class="nmain" href="../manifest.html">Манифест</a>'
NEW_GROUPS = ('<div class="ngroup"><div class="ngt">Обучение</div>'
              '<a class="nli" href="../study/index.html">Обучение</a>'
              '<a class="nli" href="../study/words.html">Тренажёр карточек</a>'
              '<a class="nli" href="../study/cheatsheets.html">Шпаргалки</a></div>\n'
              '<div class="ngroup"><div class="ngt">Электрика</div>'
              '<a class="nli" href="../electric/index.html">Раздел</a>'
              '<a class="nli" href="../electric/safety.html">Безопасность</a>'
              '<a class="nli" href="../electric/panels.html">Щиты и автоматы</a>'
              '<a class="nli" href="../electric/wiring.html">Кабели и монтаж</a>'
              '<a class="nli" href="../electric/smart.html">Умный дом</a></div>\n')
WIDGET = ('<div id="wordday"><div class="wd-t">Слово дня</div><div class="wd-w">…</div>'
          '<div class="wd-ph"></div><div class="wd-t2"></div><div class="wd-hint">нажми, чтобы раскрыть перевод</div></div>\n'
          '<script src="../study/data/wordday.js"></script>\n'
          '<script src="../study/data/widget.js"></script>\n'
          '<script>if("serviceWorker" in navigator){navigator.serviceWorker.register("../sw.js");}</script>\n')
HOMELAB = '<div class="ngroup"><div class="ngt">Homelab</div>'

FNAV_LINKS = [
    ("home", "Главная", "{pf}index.html", "#35e6e0"),
    ("manifest", "Манифест", "{pf}manifest.html", "#35e6e0"),
    ("start", "С чего начать", "{pf}getting-started/index.html", "#3ef06a"),
    ("study", "Обучение", "{pf}study/index.html", "#ffe14d"),
    ("elec", "Электрика", "{pf}electric/index.html", "#ff55f0"),
    ("lab", "Homelab", "{pf}homelab/index.html", "#35e6e0"),
    ("srv", "Сервисы", "{pf}services/index.html", "#3ef06a"),
    ("guide", "Гайды", "{pf}guides/index.html", "#ffe14d"),
    ("res", "Мыслево", "{pf}articles/index.html", "#ff55f0"),
    ("hobby", "Досуг", "{pf}hobbies/index.html", "#d9f7d0"),
]
SECTION_KEYS = {
    "getting-started": "start", "study": "study", "electric": "elec",
    "homelab": "lab", "services": "srv", "guides": "guide",
    "articles": "res", "hobbies": "hobby",
}

FRAME_CSS = """/* Рамка-бар в стиле графа: тонкая полоса вокруг окна */
.fnav{position:fixed;top:0;left:0;right:0;z-index:40}
.fnav .frow{display:flex;align-items:center;gap:2px;overflow-x:auto;white-space:nowrap;background:rgba(10,20,13,.92);backdrop-filter:blur(6px);border-bottom:1px solid #1c2b1f;padding:5px 16px;scrollbar-width:none}
.fnav .frow::-webkit-scrollbar{display:none}
.fnav .frow a{display:inline-flex;align-items:center;gap:7px;color:#7ba87c;text-decoration:none;font-size:13px;font-family:ui-monospace,Consolas,monospace;padding:6px 10px;border-radius:999px;flex-shrink:0;cursor:pointer}
.fnav .frow a:hover{color:#fff;background:#1c2b1f}
.fnav .frow a.on{color:#fff;text-shadow:0 0 10px var(--c)}
.fnav .frow a.on .td{box-shadow:0 0 12px var(--c),0 0 3px var(--c)}
.fnav .td{width:8px;height:8px;border-radius:50%;background:var(--c);box-shadow:0 0 6px var(--c);display:inline-block}
.fnav .cor{display:none}
.layout main{padding-top:56px}
@media(max-width:820px){.fnav .frow a{font-size:12px;padding:5px 8px}.layout main{padding-top:50px}}"""

NOTES_CSS = """/* Заметки страницы: одна кнопка, одно текстовое поле */
#nts-btn{position:fixed;right:16px;bottom:16px;z-index:120;width:46px;height:46px;border-radius:50%;border:1px solid #1c2b1f;background:#0a140d;color:#d9f7d0;cursor:pointer;font-size:18px;line-height:1;box-shadow:0 8px 24px rgba(0,0,0,.45)}
#nts-btn:hover{color:#35e6e0;border-color:#35e6e0}
#nts-btn.on{background:linear-gradient(135deg,#35e6e0,#ffe14d);color:#04141f;border-color:transparent}
#nts{position:fixed;right:16px;bottom:74px;z-index:120;width:min(360px,calc(100vw - 32px));background:#0a140d;border:1px solid #1c2b1f;border-radius:12px;box-shadow:0 10px 30px rgba(0,0,0,.5)}
#nts[hidden]{display:none}
.nts-bar{display:flex;align-items:center;justify-content:space-between;padding:8px 12px;border-bottom:1px solid #1c2b1f;font-size:12px;color:#35e6e0;text-transform:uppercase;letter-spacing:.08em}
.nts-x{background:none;border:0;color:#7ba87c;cursor:pointer;font-size:14px;padding:2px 6px}
.nts-x:hover{color:#fff}
.nts-t{width:100%;min-height:140px;max-height:40vh;resize:vertical;background:#050a06;color:#d9f7d0;border:0;padding:12px;font-family:inherit;font-size:14px;line-height:1.6;border-radius:0 0 12px 12px;outline:none}
.nts-t::placeholder{color:#4a6a4c}"""


def strip_wordday(path):
    """Убирает виджет «Слово дня» (html-блок + подключения wordday/widget/srs)."""
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    orig = html
    html = re.sub(r"\s*<div id=\"wordday\">[\s\S]*?</div>\s*</div>", "", html, flags=re.S)
    for name in ("wordday.js", "widget.js", "srs.js"):
        html = re.sub(r"\s*<script[^>]*src=\"[^\"]*" + name + r"\"[^>]*></script>\s*", "\n", html)
    if html != orig:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        return 1
    return 0


def inject_old(path):
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    orig = html
    changed = 0
    if "<aside" in html:
        if "Манифест" not in html:
            anchor = '<a class="nmain" href="../index.html">Главная</a>'
            if anchor in html:
                html = html.replace(anchor, anchor + MANIFEST_LINK, 1)
                changed += 1
        if HOMELAB in html and "study/index.html" not in html:
            html = html.replace(HOMELAB, NEW_GROUPS + HOMELAB, 1)
            changed += 1
    if html != orig:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
    return changed


def inject_notes(path, prefix):
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    orig = html
    changed = 0
    if "js/notes.js" not in html and "</body>" in html:
        html = html.replace("</body>", '<script src="' + prefix + 'js/notes.js"></script>\n</body>', 1)
        changed += 1
    if "style.css" not in html and "js/notes.js" in html and "<style>" not in html:
        pass
    if "style.css" not in html and ".nts-t{" not in html and "</head>" in html:
        html = html.replace("</head>", "<style>\n" + NOTES_CSS + "\n</style>\n</head>", 1)
        changed += 1
    if html != orig:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
    return changed


def _cur_key(parts):
    if parts[0] in SECTION_KEYS:
        return SECTION_KEYS[parts[0]]
    if parts[-1] == "manifest.html":
        return "manifest"
    return ""


def fnav_markup(prefix, cur):
    row = []
    for key, label, href, c in FNAV_LINKS:
        on = ' class="on"' if key == cur else ""
        href = href.format(pf=prefix)
        row.append('<a href="{href}"{on} style="--c:{c}"><span class="td"></span>{label}</a>'.format(
            href=href, on=on, c=c, label=label))
    return ('<div class="fnav">\n'
            '<nav class="frow">' + "\n".join(row) + "</nav>\n"
            "</div>\n")


def inject_frame(path, prefix):
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    cur = _cur_key(os.path.relpath(path, ROOT).split(os.sep))
    markup = fnav_markup(prefix, cur)
    orig = html
    changed = 0
    if 'class="fnav"' in html:
        # рамка уже есть — пересобираем заново (метки/ссылки разделов могли измениться)
        updated = re.sub(r'<div class="fnav">.*?</div>\s*', markup + "\n", html, flags=re.S)
        if updated != html:
            html = updated
            changed += 1
    else:
        new = re.sub(r"\s*<aside[^>]*>.*?</aside>\s*", "\n", html, flags=re.S)
        if new != html:
            html = new
            changed += 1
        m = re.search(r"(<body[^>]*>)", html)
        if m:
            html = html.replace(m.group(1), m.group(1) + "\n" + markup, 1)
            changed += 1
    html = re.sub(r"\s*<style>\s*/\* Рамка-бар в стиле графа[\s\S]*?</style>", "\n", html, flags=re.S)
    if "style.css" not in html and "</head>" in html:
        html = html.replace("</head>", "<style>\n" + FRAME_CSS + "\n</style>\n</head>", 1)
        changed += 1
    if html != orig:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
    return changed


def strip_redundant_back(path):
    """Убирает ручную ссылку «← на главную»: она дублирует чип «Главная» в
    frow-баре (leжат поверх него под фиксированной рамкой)."""
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    orig = html
    if 'class="fnav"' in html:
        html = re.sub(r'\s*<a href="[^"]*index\.html" aria-label="на главную"[^>]*>← на главную</a>\s*', "\n", html)
    if html != orig:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        return 1
    return 0


def strip_old_wall(path):
    """Вычищает рисовалку «стена»: canvas, кнопки, подсказку, js/wall.js,
    инлайн-блок wall-css и подключения js/nav.js."""
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    orig = html
    html = re.sub(r"\s*<canvas id=\"bgwall\"[^>]*></canvas>\s*", "\n", html)
    html = re.sub(r"\s*<button id=\"wall-btn\"[\s\S]*?</button>\s*", "\n", html)
    html = re.sub(r"\s*<div id=\"wall-bar\"[\s\S]*?</div>\s*", "\n", html)
    html = re.sub(r"\s*<div id=\"wall-hint\"[^>]*>.*?</div>\s*", "\n", html)
    html = re.sub(r"\s*<script[^>]*src=\"[^\"]*js/wall\.js\"[^>]*></script>\s*", "\n", html)
    html = re.sub(r"\s*<style>\s*#bgwall\{position:fixed;inset:0;z-index:90[\s\S]*?</style>\s*", "\n", html)
    html = re.sub(r"\s*<script[^>]*src=\"[^\"]*js/nav\.js\"[^>]*></script>\s*", "\n", html)
    if html != orig:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        return 1
    return 0


def all_pages():
    found = []
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in ("gen", "tests", "node_modules")]
        for name in files:
            if name.endswith(".html"):
                found.append(os.path.join(root, name))
    return sorted(found)


def main():
    pages = all_pages()
    n_old = 0
    n_frame = 0
    n_notes = 0
    n_strip = 0
    for path in pages:
        rel = os.path.relpath(path, ROOT)
        parts = rel.split(os.sep)
        name = parts[-1]
        depth = len(parts) - 1
        prefix = "../" * depth
        changed = 0
        c = strip_old_wall(path)
        if c:
            n_strip += 1
        changed += c
        if rel == "index.html":
            pass  # корневой граф самоценен — без рамки
        else:
            c = strip_wordday(path)
            if c:
                n_strip += 1
            changed += c
            c = strip_redundant_back(path)
            if c:
                n_strip += 1
            changed += c
            if parts[0] in OLD_DIRS and name not in SKIP_OLD:
                c = inject_old(path)
                if c:
                    n_old += 1
                changed += c
            c = inject_frame(path, prefix)
            if c:
                n_frame += 1
            changed += c
        c = inject_notes(path, prefix)
        if c:
            n_notes += 1
        changed += c
        print(("+" if changed else "="), rel)
    print(f"Страниц обработано: {len(pages)} | old: {n_old} | рамка: {n_frame} | заметки: {n_notes} | вычищено: {n_strip}")


if __name__ == "__main__":
    main()