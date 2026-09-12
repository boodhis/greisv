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
                 '<button class="wc on" data-c="#4fc3f7" style="background:#4fc3f7" title="Голубой"></button>\n'
                 '<button class="wc" data-c="#3fb950" style="background:#3fb950" title="Зелёный"></button>\n'
                 '<button class="wc" data-c="#e3b341" style="background:#e3b341" title="Жёлтый"></button>\n'
                 '<button class="wc" data-c="#ff7ab6" style="background:#ff7ab6" title="Розовый"></button>\n'
                 '<button class="wc" data-c="#e6edf3" style="background:#e6edf3" title="Белый"></button>\n'
                 '<button id="wall-undo" class="wclear" type="button">↩ убрать надпись</button>\n'
                 '</div>\n'
                 '<div id="wall-hint" hidden>Рисуй прямо на подложке. Готово — кнопка справа внизу, выход — Esc</div>\n')
WALL_CSS = """#bgwall{position:fixed;inset:0;z-index:90;pointer-events:none;touch-action:none}
body.drawing{cursor:crosshair}
body.drawing #bgwall{pointer-events:auto}
body.drawing main,body.drawing aside{pointer-events:none}
#wall-btn{position:fixed;right:16px;bottom:16px;z-index:120;padding:11px 20px;border-radius:999px;font-weight:600;border:1px solid #21262d;color:#e6edf3;background:#161b22;cursor:pointer;font-family:inherit;font-size:14px}
#wall-btn.on{background:linear-gradient(135deg,#4fc3f7,#7c4dff);color:#04141f}
#wall-bar{position:fixed;right:16px;bottom:64px;z-index:120;display:flex;gap:6px;align-items:center;background:#161b22;border:1px solid #21262d;border-radius:999px;padding:6px 10px;box-shadow:0 8px 24px rgba(0,0,0,.45)}
#wall-bar .wc{width:20px;height:20px;border-radius:50%;border:2px solid rgba(255,255,255,.22);cursor:pointer;padding:0}
#wall-bar .wc.on{border-color:#fff;box-shadow:0 0 8px currentColor}
#wall-bar .wclear{background:none;border:0;color:#8b98a8;cursor:pointer;font-size:12px;padding:4px 6px}
#wall-hint{position:fixed;left:50%;bottom:12px;transform:translateX(-50%);z-index:110;background:rgba(13,17,23,.92);border:1px solid #21262d;padding:7px 16px;border-radius:999px;font-size:12px;color:#8b98a8;white-space:nowrap}
@media(max-width:820px){#wall-hint{font-size:11px;white-space:normal;width:88%;text-align:center}}"""


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
        print(("+" if changed else "="), rel)
    print(f"Страниц обработано: {len(pages)}  | old-инъекций: {n_old}  | стен: {n_wall}")


if __name__ == "__main__":
    main()