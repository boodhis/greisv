#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Инжектит во все страницы сайта:
  1) old-инъекция (только для разделов с инлайн-стилем): ссылка «Манифест»,
     группы «Обучение»/«Электрика», виджет «Слова дня» + wordday.js/widget.js/sw.js;
  2) стена-подложка (во ВСЕ страницы, кроме корневого index.html, где уже есть):
     canvas #bgwall, кнопка «✏️ Стена», палитра, подсказка, подключение js/wall.js.
     Для разделов с инлайн-стилем добавляется и inline-CSS стены.

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
    if "Манифест" not in html:
        anchor = '<a class="nmain" href="../index.html">Главная</a>'
        if anchor in html:
            html = html.replace(anchor, anchor + MANIFEST_LINK, 1)
            changed += 1
    if HOMELAB not in html:
        print("  !! нет группы Homelab в навигации — пропускаю", path)
    elif "study/index.html" not in html:
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


def inject_wall(path, prefix):
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    if 'id="bgwall"' in html:
        return 0
    orig = html
    changed = 0
    if "<body" in html:
        m = re.search(r'(<body[^>]*>)', html)
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


NAV_SCRIPT = '<script src="{prefix}js/nav.js"></script>\n'


def inject_nav(path, prefix):
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    if 'js/nav.js' in html or 'class="ngroup"' not in html:
        return 0
    orig = html
    html = html.replace("</body>", NAV_SCRIPT.format(prefix=prefix) + "</body>", 1)
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
                p = os.path.join(root, name)
                rel = os.path.relpath(p, ROOT)
                if os.sep not in rel:
                    found.append(p)  # корневые html (index, manifest)
                else:
                    found.append(p)
    return sorted(found)


def main():
    pages = all_pages()
    n_old = 0
    n_wall = 0
    n_nav = 0
    for path in pages:
        rel = os.path.relpath(path, ROOT)
        parts = rel.split(os.sep)
        name = parts[-1]
        depth = len(parts) - 1
        prefix = "../" * depth
        changed = 0
        if parts[0] in OLD_DIRS and name not in SKIP_OLD:
            changed += inject_old(path)
            if changed:
                n_old += 1
        if rel != "index.html":
            c = inject_wall(path, prefix)
            if c:
                n_wall += 1
            changed += c
        c = inject_nav(path, prefix)
        if c:
            n_nav += 1
        changed += c
        print(("+" if changed else "="), rel)
    print(f"Страниц обработано: {len(pages)}  | old-инъекций: {n_old}  | стен: {n_wall}  | навигация: {n_nav}")


if __name__ == "__main__":
    main()