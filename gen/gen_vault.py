#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Автоген «Сайт» из волта Obsidian: ~/obsid/Сайт/*.md -> ~/greisv/<section>/*.html.

Правила:
  - зеркальная папка волта «Сайт»: подпапка = раздел greisv, имя файла = страница.
  - README.md и файлы с префиксом "_" не публикуются.
  - frontmatter: title, description, priority (для sitemap).
  - после генерации согласуются sitemap.xml и sw.js (ASSETS + бамп CACHE),
    прогоняются тесты и (в --auto/--push) коммит+push в greisv.
  - состояние: gen/.vault_state хранит последний обработанный коммит поддерева «Сайт/».

Использование:
  gen/gen_vault.py --force          перегенерировать всё сразу
  gen/gen_vault.py --auto           только если «Сайт/» изменился с прошлого раза
  gen/gen_vault.py --auto --push    то же + коммит и push в greisv
  gen/gen_vault.py --dry            ничего не писать, только показать план
"""
import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

import markdown

HOME = Path.home()
VAULT = Path(HOME, "obsid", "Сайт")
GREISV = Path(HOME, "greisv")
STATE = Path(HOME, "greisv", "gen", ".vault_state")
SITE = "https://boodhis.github.io/greisv/"

SECTIONS = {
    "getting-started": ("С чего начать", "#3ef06a"),
    "services": ("Сервисы", "#3ef06a"),
    "guides": ("Гайды", "#ffe14d"),
    "homelab": ("Homelab", "#35e6e0"),
    "resources": ("Ресурсы", "#ff55f0"),
    "hobbies": ("Досуг", "#d9f7d0"),
}
# порядок разделов в рамке навигации (fnav)
FNAV = [
    ("index.html", None, "Главная", "#35e6e0"),
    ("manifest.html", None, "Манифест", "#35e6e0"),
    ("getting-started/index.html", "getting-started", "С чего начать", "#3ef06a"),
    ("study/index.html", None, "Обучение", "#ffe14d"),
    ("electric/index.html", None, "Электрика", "#ff55f0"),
    ("homelab/index.html", "homelab", "Homelab", "#35e6e0"),
    ("services/index.html", "services", "Сервисы", "#3ef06a"),
    ("guides/index.html", "guides", "Гайды", "#ffe14d"),
    ("resources/index.html", "resources", "Ресурсы", "#ff55f0"),
    ("hobbies/index.html", "hobbies", "Досуг", "#d9f7d0"),
]

HEAD = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__ — Цифровая Крепость</title>
<meta name="description" content="__DESC__">
<link rel="icon" type="image/svg+xml" href="__REL__favicon.svg">
<link rel="stylesheet" href="__REL__style.css">
<meta name="theme-color" content="#050b06">
<style>
body::after{content:"";position:fixed;inset:0;z-index:9999;pointer-events:none;opacity:.65;background:repeating-linear-gradient(0deg,rgba(0,0,0,.07) 0 1px,transparent 1px 3px)}
h1,h2,.brand{text-shadow:0 0 14px rgba(62,240,106,.22)}
main{max-width:880px}
.content h2{border-bottom:1px solid #1c2b1f;padding-bottom:6px;margin-top:34px}
.content h3{margin-top:22px}
.content table{border-collapse:collapse;width:100%;margin:14px 0;font-size:14px}
.content th,.content td{border:1px solid #1c2b1f;padding:7px 10px;text-align:left;vertical-align:top}
.content th{color:#35e6e0;font-weight:600}
.content code{background:#0a140d;border:1px solid #1c2b1f;border-radius:5px;padding:1px 5px;color:#c9ff87;font-family:ui-monospace,Consolas,monospace;font-size:13px}
.content pre{background:#0a140d;border:1px solid #1c2b1f;border-radius:10px;padding:14px;overflow-x:auto;line-height:1.55}
.content pre code{border:0;background:none;padding:0;color:#d9f7d0}
.content blockquote{border-left:3px solid #3ef06a;margin:14px 0;padding:2px 0 2px 14px;color:#7ba87c}
.content a{color:#35e6e0}
.content ul,.content ol{padding-left:22px;margin:10px 0}
.content img{max-width:100%;border-radius:8px}
.callout{background:#0a140d;border:1px solid #1c2b1f;border-left:4px solid #3ef06a;border-radius:10px;padding:12px 16px;margin:18px 0}
.callout .callout-t{color:#35e6e0;font-weight:600;margin-bottom:6px;text-transform:uppercase;letter-spacing:.06em;font-size:13px}
.callout.callout-warn,.callout.callout-danger{border-left-color:#ffe14d}
.callout.callout-danger{border-left-color:#ff6b6b}
</style>
</head>
<body>
<div class="fnav">
<i class="cor ctl"></i><i class="cor ctr"></i><i class="cor cbl"></i><i class="cor cbr"></i>
<nav class="frow">__FNAV__</nav>
</div>
<div class="layout">
<main>
<h1>__TITLE__</h1>
__MOTTO__
<div class="content">
__BODY__
</div>
<footer>Цифровая Крепость — образовательный сайт. · <a href="https://github.com/boodhis/greisv">Исходный код</a> · Источник статьи: заметка в Obsidian (волт)</footer>
</main>
</div>
<div id="wordday" style="display:none"></div>
<script src="__REL__study/data/wordday.js"></script>
<script src="__REL__study/data/widget.js"></script>
<script>if("serviceWorker" in navigator){navigator.serviceWorker.register("__REL__sw.js");}</script>
<script src="__REL__js/notes.js"></script>
</body>
</html>
"""


def sh(*args, cwd=None):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True)


def git(*args, cwd):
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    return r.stdout.strip()


def last_vault_site_commit():
    r = subprocess.run(["git", "log", "-1", "--format=%H", "--", "Сайт/"],
                       cwd=Path(HOME, "obsid"), capture_output=True, text=True)
    return r.stdout.strip() or "none"


def has_changes():
    cur = last_vault_site_commit()
    if not STATE.exists():
        return True, cur
    return cur != STATE.read_text().strip(), cur


def parse_frontmatter(text):
    fm = {}
    body = text
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, _, v = line.partition(":")
                fm[k.strip().lower()] = v.strip()
        body = text[m.end():]
    return fm, body


def to_html(body):
    # спрятать код (блоки и inline) от замены вики-ссылок
    code_blocks, code_spans = [], []

    def keep_fence(m):
        code_blocks.append(m.group(0))
        return f"\x00CODEBLOCK{len(code_blocks) - 1}\x00"

    def keep_span(m):
        code_spans.append(m.group(0))
        return f"\x00CODESPAN{len(code_spans) - 1}\x00"

    body = re.sub(r"```.*?```", keep_fence, body, flags=re.S)
    body = re.sub(r"`[^`\n]+`", keep_span, body)

    # Obsidian callouts: > [!TYPE] Заголовок
    out = []
    for line in body.splitlines():
        m = re.match(r"^\s*> \[!(\w+)\]\s*(.*)$", line)
        if m:
            ctype = m.group(1).lower()
            ctitle = m.group(2).strip()
            if not ctitle:
                ctitle = {"note": "Заметка", "tip": "Совет", "warn": "Внимание",
                          "warning": "Внимание", "danger": "Опасно"}.get(ctype, ctype.capitalize())
            out.append(f'<div class="callout callout-{ctype}">')
            out.append(f'<div class="callout-t">{ctitle}</div>')
            out.append('<div class="callout-body">')
            continue
        out.append(line)
    body = "\n".join(out)
    # Obsidian wikilinks -> ссылки на страницы сайта
    def wl(m2):
        target, alias = m2.group(1), m2.group(2)
        name = alias if alias else target
        parts = target.split("/")
        basename = parts[-1].split(".")[0]
        return f'<a href="{basename}.html">{name}</a>'
    body = re.sub(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]", wl, body)

    def restore(m):
        i = int(m.group(2))
        return code_blocks[i] if m.group(1) == "BLOCK" else code_spans[i]

    body = re.sub(r"\x00CODE(BLOCK|SPAN)(\d+)\x00", restore, body)
    return markdown.markdown(body, extensions=["tables", "fenced_code", "sane_lists"])


def fnav_html(active_section, relp="", depth=0):
    items = []
    for href, sec, label, color in FNAV:
        cls = " on" if sec == active_section else ""
        items.append(f'<a href="{relp}{href}"{cls} style="--c:{color}"><span class="td"></span>{label}</a>')
    return "\n".join(items)


def rel_depth(path):
    return path.relative_to(GREISV).as_posix()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--auto", action="store_true")
    ap.add_argument("--push", action="store_true")
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args()

    if not args.force and args.auto:
        changed, cur = has_changes()
        if not changed:
            print("[gen_vault] «Сайт/» не менялся, выхожу")
            return 0
        print(f"[gen_vault] «Сайт/» изменился (с {STATE.read_text().strip() if STATE.exists() else '—'} до {cur})")

    if not VAULT.exists():
        print(f"[gen_vault] нет папки волта {VAULT}", file=sys.stderr)
        return 2

    rel_pages = {}
    for md in sorted(VAULT.rglob("*.md")):
        if md.name == "README.md" or md.name.startswith("_"):
            continue
        rel = md.relative_to(VAULT).as_posix()
        section = rel.split("/", 1)[0]
        if section not in SECTIONS:
            print(f"[gen_vault] пропуск: раздел «{section}» не из SECTIONS ({rel})")
            continue
        rel_pages[rel] = md

    if not rel_pages:
        print("[gen_vault] нет заметок для публикации")
        return 0

    dirty = sh("git", "status", "--porcelain", cwd=GREISV).stdout
    if dirty and not args.dry:
        print("[gen_vault] greisv не чистый — стоп (закоммить/засташь):\n" + dirty)
        return 2

    news = []
    for rel, md in rel_pages.items():
        section = rel.split("/", 1)[0]
        page = GREISV / Path(rel).with_suffix(".html")
        fm, body = parse_frontmatter(md.read_text(encoding="utf-8"))
        title = fm.get("title") or (page.stem.replace("-", " ").capitalize())
        desc = fm.get("description", f"Статья «{title}» — из волта Obsidian. Цифровая Крепость.")
        depth = len(page.relative_to(GREISV).parts) - 1
        relp = ("../" * depth)
        html = (HEAD.replace("__TITLE__", title)
                    .replace("__DESC__", desc)
                    .replace("__REL__", relp)
                    .replace("__FNAV__", fnav_html(section, relp))
                    .replace("__MOTTO__", f'<p class="muted">{desc}</p>')
                    .replace("__BODY__", to_html(body)))
        if args.dry:
            print(f"[gen_vault] -> {rel} → {page}")
            continue
        page.parent.mkdir(parents=True, exist_ok=True)
        page.write_text(html, encoding="utf-8")
        news.append(rel)

    if args.dry:
        return 0

    # --- согласование sitemap.xml и sw.js ---
    reconcile_site_meta()

    print(f"[gen_vault] сгенерировано страниц: {len(news)}")
    for r in news:
        print("   ·", r)

    # --- тесты ---
    t = sh("python3", "tests/test_site.py", cwd=GREISV)
    print(t.stdout[-400:])
    if t.returncode != 0:
        print("[gen_vault] тесты не прошли, push не делаю", file=sys.stderr)
        return 2

    if args.push:
        print("[gen_vault] коммит + push greisv")
        sh("git", "add", "-A", cwd=GREISV)
        msg = sh("git", "commit", "-q", "-m",
                 "Волт→сайт: автоген страниц из obsid/Сайт (" + ", ".join(news) + ")",
                 cwd=GREISV)
        if msg.returncode != 0:
            print("[gen_vault] нечего коммитить")
        sh("git", "push", "origin", "main", cwd=GREISV)

    cur = last_vault_site_commit()
    STATE.write_text(cur)
    print("[gen_vault] done, state →", cur)
    return 0


def reconcile_site_meta():
    sw = GREISV / "sw.js"
    stext = sw.read_text(encoding="utf-8")
    old_assets = re.findall(r'  "([^"]+)"', stext.split("var ASSETS = [", 1)[1].split("];", 1)[0])
    html_files = sorted({p.relative_to(GREISV).as_posix()
                         for p in GREISV.rglob("*.html") if ".git" not in p.parts})
    cur_set = set(html_files) | {"index.html"}
    assets = list(dict.fromkeys([a for a in old_assets if a in cur_set or not a.endswith(".html")]))
    for h in sorted(cur_set):
        if h not in assets:
            assets.append(h)
    assets_block = "".join(f'  "{a}",\n' for a in assets)
    new_block = f"var ASSETS = [\n{assets_block}];"
    stext2 = stext.split("var ASSETS = [", 1)[0] + new_block + stext.split("];", 1)[1]
    m = re.search(r'var CACHE = "(\w+)-v(\d+)";', stext2)
    if m:
        stext2 = stext2.replace(m.group(0), f'var CACHE = "{m.group(1)}-v{int(m.group(2)) + 1}";')
    sw.write_text(stext2, encoding="utf-8")

    sm = GREISV / "sitemap.xml"
    stext = sm.read_text(encoding="utf-8")
    locs = dict(re.findall(r"<url><loc>https://boodhis\.github\.io/greisv/([^<]*)</loc><priority>([0-9.]+)</priority></url>", stext))
    locs = {x if x else "index.html": p for x, p in locs.items()}
    out = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for h in sorted(cur_set):
        prio = locs.get(h, "0.5")
        loc = SITE + ("" if h == "index.html" else h)
        out.append(f'  <url><loc>{loc}</loc><priority>{prio}</priority></url>')
    out.append("</urlset>")
    sm.write_text("\n".join(out) + "\n", encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())