# -*- coding: utf-8 -*-
# авторотация: заменяет старую кнопку «Стереть всё» на кнопку поштучного удаления.
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLD = '<button class="wclear" type="button">Стереть всё</button>'
NEW = '<button id="wall-undo" class="wclear" type="button">↩ убрать надпись</button>'

n = 0
for root, dirs, files in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in ("gen", "tests", "node_modules", ".git")]
    for name in files:
        if not name.endswith(".html"):
            continue
        p = os.path.join(root, name)
        with open(p, "r", encoding="utf-8") as f:
            html = f.read()
        if OLD in html:
            with open(p, "w", encoding="utf-8") as f:
                f.write(html.replace(OLD, NEW))
            n += 1
            print("+", os.path.relpath(p, ROOT))

print("страниц обновлено:", n)