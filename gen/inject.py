#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Инжектит во все страницы сайта:
  1) рамку-бар навигации (во все страницы, кроме корневого index.html):
     верхняя строка .frow с точками-разделами, у текущего раздела класс .on;
  2) вычистку старого: стену-рисовалку (bgwall, wall-*, js/wall.js, inline
     wall CSS), подключения js/nav.js, виджет «Слова дня», ручную ссылку
     «← на главную» (её дублирует чип «Главная» в frow).

Навигация (6 пунктов, тема «тёплая бумага»):
    Главная · Крепость · Homelab · Электрика · Обучение · Заметки

Запуск из корня проекта:  python3 gen/inject.py
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FNAV_LINKS = [
    ("home", "Главная", "{pf}index.html", "#0a5c52"),
    ("fort", "Крепость", "{pf}getting-started/index.html", "#3d5c2c"),
    ("lab", "Homelab", "{pf}homelab/index.html", "#0a5c52"),
    ("elec", "Электрика", "{pf}electric/index.html", "#7a2f6b"),
    ("study", "Обучение", "{pf}study/index.html", "#7d611b"),
    ("notes", "Заметки", "{pf}articles/index.html", "#6b6659"),
]
SECTION_KEYS = {
    "getting-started": "fort", "study": "study", "electric": "elec",
    "homelab": "lab", "articles": "notes",
}


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


def _cur_key(parts):
    if parts[0] in SECTION_KEYS:
        return SECTION_KEYS[parts[0]]
    if parts[-1] == "manifest.html":
        return "fort"
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
        m = re.search(r"(<body[^>]*>)", html)
        if m:
            html = html.replace(m.group(1), m.group(1) + "\n" + markup, 1)
            changed += 1
    html = re.sub(r"\s*<style>\s*/\* Рамка-бар в стиле графа[\s\S]*?</style>", "\n", html, flags=re.S)
    if html != orig:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
    return changed


def strip_redundant_back(path):
    """Убирает ручную ссылку «← на главную»: она дублирует чип «Главная» в
    frow-баре."""
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
        dirs[:] = [d for d in dirs if d not in ("gen", "tests", "node_modules", ".venv", ".git")]
        for name in files:
            if name.endswith(".html"):
                found.append(os.path.join(root, name))
    return sorted(found)


def main():
    pages = all_pages()
    n_frame = 0
    n_strip = 0
    for path in pages:
        rel = os.path.relpath(path, ROOT)
        parts = rel.split(os.sep)
        depth = len(parts) - 1
        prefix = "../" * depth
        changed = 0
        c = strip_old_wall(path)
        if c:
            n_strip += 1
        changed += c
        if rel == "index.html":
            pass  # корневая витрина — без рамки, у неё своя тема
        else:
            c = strip_wordday(path)
            if c:
                n_strip += 1
            changed += c
            c = strip_redundant_back(path)
            if c:
                n_strip += 1
            changed += c
            c = inject_frame(path, prefix)
            if c:
                n_frame += 1
            changed += c
        print(("+" if changed else "="), rel)
    print(f"Страниц обработано: {len(pages)} | рамка: {n_frame} | вычищено: {n_strip}")


if __name__ == "__main__":
    main()
