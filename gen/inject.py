#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Инжектит во все страницы сайта:
  1) old-инъекция (только для разделов с инлайн-стилем): ссылка «Манифест»,
     группы «Обучение»/«Электрика», виджет «Слова дня» + wordday.js/widget.js/sw.js;
  2) рамка-бар навигации (во все страницы, кроме корневого index.html-графа):
     снятие <aside>, тонкая рамка вокруг окна с узлами-точками разделов
     (у текущего раздела подсветка .on); для страниц без style.css —
     inline-CSS рамки;
  3) стена-подложка (во все страницы, кроме корневого index.html):
     canvas #bgwall, кнопка «✏️ Стена», палитра, подсказка, js/wall.js;
  4) вычистка старых подключений js/nav.js (аккордеон отменён).

Запуск из корня проекта:  python3 gen/inject.py
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLD_DIRS = ["getting-started", "homelab", "services", "guides", "resources", "hobbies"]
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
    ("res", "Ресурсы", "{pf}resources/index.html", "#ff55f0"),
    ("hobby", "Досуг", "{pf}hobbies/index.html", "#d9f7d0"),
]
SECTION_KEYS = {
    "getting-started": "start", "study": "study", "electric": "elec",
    "homelab": "lab", "services": "srv", "guides": "guide",
    "resources": "res", "hobbies": "hobby",
}


def fnav_markup(prefix, cur):
    row = []
    for key, label, href, c in FNAV_LINKS:
        on = ' class="on"' if key == cur else ""
        href = href.format(pf=prefix)
        row.append('<a href="{href}"{on} style="--c:{c}"><span class="td"></span>{label}</a>'.format(
            href=href, on=on, c=c, label=label))
    return ('<div class="fnav">\n'
            '<i class="cor ctl"></i><i class="cor ctr"></i><i class="cor cbl"></i><i class="cor cbr"></i>\n'
            '<nav class="frow">' + "\n".join(row) + "</nav>\n"
            "</div>\n")


FRAME_CSS = """/* Рамка-бар в стиле графа: тонкая полоса вокруг окна */
.fnav{position:fixed;inset:0;z-index:40;pointer-events:none}
.fnav::before{content:"";position:absolute;inset:8px;border:1px solid #1c2b1f;border-radius:10px;box-shadow:inset 0 0 0 1px rgba(5,11,6,.55),0 0 26px rgba(53,230,224,.05)}
.fnav .frow{position:absolute;top:12px;left:16px;right:16px;display:flex;align-items:center;gap:2px;overflow-x:auto;white-space:nowrap;pointer-events:auto;padding:4px 2px;scrollbar-width:none}
.fnav .frow::-webkit-scrollbar{display:none}
.fnav .frow a{display:inline-flex;align-items:center;gap:7px;color:#7ba87c;text-decoration:none;font-size:13px;font-family:ui-monospace,Consolas,monospace;padding:6px 10px;border-radius:999px;flex-shrink:0;cursor:pointer}
.fnav .frow a:hover{color:#fff;background:#1c2b1f}
.fnav .frow a.on{color:#fff;text-shadow:0 0 10px var(--c)}
.fnav .frow a.on .td{box-shadow:0 0 12px var(--c),0 0 3px var(--c)}
.fnav .td{width:8px;height:8px;border-radius:50%;background:var(--c);box-shadow:0 0 6px var(--c);display:inline-block}
.fnav .cor{position:absolute;width:16px;height:16px;opacity:.9;filter:drop-shadow(0 0 6px rgba(53,230,224,.6))}
.fnav .ctl{top:11px;left:11px;border-top:2px solid #35e6e0;border-left:2px solid #35e6e0;border-top-left-radius:6px}
.fnav .ctr{top:11px;right:11px;border-top:2px solid #35e6e0;border-right:2px solid #35e6e0;border-top-right-radius:6px}
.fnav .cbl{bottom:11px;left:11px;border-bottom:2px solid #35e6e0;border-left:2px solid #35e6e0;border-bottom-left-radius:6px}
.fnav .cbr{bottom:11px;right:11px;border-bottom:2px solid #35e6e0;border-right:2px solid #35e6e0;border-bottom-right-radius:6px}
.layout main{padding-top:76px}
@media(max-width:820px){.fnav .frow a{font-size:12px;padding:5px 8px}.layout main{padding-top:70px}}"""

WALL_CANVAS = '<canvas id="bgwall" aria-hidden="true"></canvas>'
WALL_CONTROLS = ('<button id="wall-btn" class="btn ghost" title="Оставить надпись на стене-подложке">✏️ Стена</button>\n'
                 '<div id="wall-bar" hidden>\n'
                 '<button class="wc on" data-c="#35e6e0" style="background:#35e6e0" title="Голубой"></button>\n'
                 '<button class="wc" data-c="#3ef06a" style="background:#3ef06a" title="Зелёный"></button>\n'
                 '<button class="wc" data-c="#ffe14d" style="background:#ffe14d" title="Жёлтый"></button>\n'
                 '<button class="wc" data-c="#ff55f0" style="background:#ff55f0" title="Розовый"></button>\n'
                 '<button class="wc" data-c="#d9f7d0" style="background:#d9f7d0" title="Белый"></button>\n'
                 '<button id="wall-undo" class="wclear" type="button">⌫ Удалить надпись</button>\n'
                 '</div>\n'
                 '<div id="wall-hint" hidden>Рисуй прямо на подложке. Готово — кнопка справа внизу, выход — Esc</div>\n')
WALL_CSS = """#bgwall{position:fixed;inset:0;z-index:90;pointer-events:none;touch-action:none}
body.drawing{cursor:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='16' height='16'><circle cx='8' cy='8' r='3' fill='%2335e6e0' stroke='%23000' stroke-opacity='.5'/></svg>") 8 8,crosshair}
body.drawing #bgwall{pointer-events:auto}
body.drawing main,body.drawing aside{pointer-events:none}
#wall-btn{position:fixed;right:16px;bottom:16px;z-index:120;padding:11px 20px;border-radius:999px;font-weight:600;border:1px solid #1c2b1f;color:#d9f7d0;background:#0a140d;cursor:pointer;font-family:inherit;font-size:14px}
#wall-btn.on{background:linear-gradient(135deg,#35e6e0,#ffe14d);color:#04141f}
#wall-bar{position:fixed;right:12px;top:50%;bottom:auto;transform:translateY(-50%);z-index:120;display:flex;flex-direction:column;gap:8px;align-items:center;background:#0a140d;border:1px solid #1c2b1f;border-radius:12px;padding:10px 7px;box-shadow:0 8px 24px rgba(0,0,0,.45)}
#wall-bar .wc{width:20px;height:20px;border-radius:50%;border:2px solid rgba(255,255,255,.22);cursor:pointer;padding:0}
#wall-bar .wc.on{border-color:#fff;box-shadow:0 0 8px currentColor}
#wall-bar .wclear{writing-mode:vertical-rl;background:none;border:0;color:#7ba87c;cursor:pointer;font-size:11px;padding:2px 4px;letter-spacing:.08em}
#wall-hint{position:fixed;right:16px;bottom:108px;left:auto;transform:none;z-index:115;max-width:min(430px,82vw);background:rgba(5,11,6,.94);border:1px solid #1c2b1f;padding:8px 14px;border-radius:10px;font-size:12px;line-height:1.45;color:#7ba87c;white-space:normal;pointer-events:none;box-shadow:0 6px 18px rgba(0,0,0,.4)}
@media(max-width:820px){#wall-hint{font-size:11px;white-space:normal;width:auto;right:12px;bottom:104px;left:12px;text-align:left}}"""


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
    if 'id="wordday"' not in html and "</body>" in html:
        html = html.replace("</body>", WIDGET + "</body>", 1)
        changed += 1
    if "max-width:860px" in html:
        html = html.replace("max-width:860px", "max-width:1180px")
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


def inject_frame(path, prefix):
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    if 'class="fnav"' in html:
        return 0
    orig = html
    changed = 0
    new = re.sub(r"\s*<aside[^>]*>.*?</aside>\s*", "\n", html, flags=re.S)
    if new != html:
        html = new
        changed += 1
    m = re.search(r"(<body[^>]*>)", html)
    if m:
        cur = _cur_key(os.path.relpath(path, ROOT).split(os.sep))
        html = html.replace(m.group(1), m.group(1) + "\n" + fnav_markup(prefix, cur), 1)
        changed += 1
    if "style.css" not in html and "</head>" in html:
        html = html.replace("</head>", "<style>\n" + FRAME_CSS + "\n</style>\n</head>", 1)
        changed += 1
    if html != orig:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
    return changed


def html_sniff(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def strip_navjs(path):
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    new = re.sub(r"\s*<script[^>]*src=\"[^\"]*js/nav\.js\"[^>]*></script>\s*", "\n", html)
    if new != html:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new)
        return 1
    return 0


def inject_wall(path, prefix):
    if 'id="bgwall"' in html_sniff(path):
        return 0
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    orig = html
    changed = 0
    if "<body" in html:
        m = re.search(r"(<body[^>]*>)", html)
        if m:
            html = html.replace(m.group(1), m.group(1) + "\n" + WALL_CANVAS, 1)
            changed += 1
    if "</body>" in html:
        if "style.css" not in html:
            style = "<style>\n" + WALL_CSS + "\n</style>\n"
        else:
            style = ""
        block = (style + WALL_CONTROLS +
                 '<script src="' + prefix + 'js/wall.js"></script>\n')
        html = html.replace("</body>", block + "</body>", 1)
        changed += 1
    if html != orig:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
    return changed


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
    n_wall = 0
    n_frame = 0
    n_strip = 0
    for path in pages:
        rel = os.path.relpath(path, ROOT)
        parts = rel.split(os.sep)
        name = parts[-1]
        depth = len(parts) - 1
        prefix = "../" * depth
        changed = 0
        c = strip_navjs(path)
        if c:
            n_strip += 1
        changed += c
        if rel == "index.html":
            pass  # корневой граф самоценен — без рамки и стены
        else:
            if parts[0] in OLD_DIRS and name not in SKIP_OLD:
                c = inject_old(path)
                if c:
                    n_old += 1
                changed += c
            c = inject_frame(path, prefix)
            if c:
                n_frame += 1
            changed += c
            c = inject_wall(path, prefix)
            if c:
                n_wall += 1
            changed += c
        print(("+" if changed else "="), rel)
    print(f"Страниц обработано: {len(pages)} | old: {n_old} | рамка: {n_frame} | стена: {n_wall} | strip nav.js: {n_strip}")


if __name__ == "__main__":
    main()