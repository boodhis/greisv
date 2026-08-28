#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Конвертер MDX/Markdown -> простой статичный HTML-сайт «Цифровая Крепость».
Читает src/content/docs/**, генерирует плоские .html файлы с общим шаблоном.
"""
import os, re, html

BASE = os.path.dirname(os.path.abspath(__file__))
# В репо: BASE = <repo>/_src, SRC = <repo>/_src/content-docs, OUT = <repo>/
SRC = os.path.join(BASE, "content-docs")
OUT = os.path.abspath(os.path.join(BASE, ".."))

def parse_frontmatter(text):
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            fm = text[3:end].strip()
            body = text[end+4:].lstrip("\n")
            meta = {}
            for line in fm.splitlines():
                m = re.match(r'^([A-Za-z_]+):\s*(.*)$', line)
                if m:
                    meta[m.group(1)] = m.group(2).strip().strip('"').strip("'")
            return meta, body
    return {}, text

# ---------- inline ----------
def inline(text):
    # escape html, but keep markdown spans
    # code spans first
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    # inline code `...`
    def code_span(m):
        return '<code>%s</code>' % m.group(1)
    text = re.sub(r'`([^`]+)`', code_span, text)

    # links [text](url)  (before bold to avoid matching **)
    def link(m):
        label = m.group(1); url = m.group(2).strip()
        if url.startswith("#") or url.startswith("http") or url.startswith("mailto"):
            href = url
        else:
            # internal: crop trailing /index or .md -> .html
            had_slash = url.endswith("/")
            href = re.sub(r'/$', '', url)
            href = re.sub(r'\.mdx?$', '', href)
            if not href:
                href = "index.html"
            elif had_slash:
                href = href + "/index.html"
            else:
                href = href + ".html"
        return '<a href="%s">%s</a>' % (href, inline(label))
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', link, text)

    # images ![alt](src) -> keep as img
    # bold **x**
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    # italic *x*
    text = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'<em>\1</em>', text)
    return text

# ---------- tables ----------
def table(block):
    lines = [l for l in block.strip().splitlines() if l.strip()]
    if len(lines) < 2:
        return inline(block)
    header = [c.strip() for c in lines[0].strip().strip('|').split('|')]
    rows = []
    for l in lines[2:]:
        cells = [c.strip() for c in l.strip().strip('|').split('|')]
        rows.append(cells)
    h = "".join("<th>%s</th>" % inline(c) for c in header)
    body = ""
    for r in rows:
        body += "<tr>" + "".join("<td>%s</td>" % inline(c) for c in r) + "</tr>"
    return '<table><thead><tr>%s</tr></thead><tbody>%s</tbody></table>' % (h, body)

# ---------- lists ----------
def list_block(block):
    lines = block.strip().splitlines()
    in_ul = in_ol = False
    out = []
    def close():
        nonlocal in_ul, in_ol
        if in_ul: out.append("</ul>")
        if in_ol: out.append("</ol>")
        in_ul = in_ol = False
    for l in lines:
        m_ul = re.match(r'^[-*]\s+(.*)$', l)
        m_ol = re.match(r'^\d+\.\s+(.*)$', l)
        if m_ul:
            if not in_ul: close(); out.append("<ul>"); in_ul = True
            out.append("<li>%s</li>" % inline(m_ul.group(1)))
        elif m_ol:
            if not in_ol: close(); out.append("<ol>"); in_ol = True
            out.append("<li>%s</li>" % inline(m_ol.group(1)))
        else:
            close()
            out.append(inline(l))
    close()
    return "".join(out)

# ---------- block-level ----------
def blocks(body):
    out = []
    i = 0
    lines = body.split("\n")
    n = len(lines)
    while i < n:
        l = lines[i]
        # callout :::tip[Title]
        cm = re.match(r'^:::(tip|note|warning|info)\s*\[?([^\]]*)\]?\s*$', l.strip())
        if re.match(r'^:::', l.strip()) and not l.strip().startswith("::::"):
            mflag = cm
            callout_type = mflag.group(1) if mflag else "note"
            callout_title = mflag.group(2).strip() if mflag else ""
            i += 1
            acc = []
            while i < n and not lines[i].strip().startswith(":::"):
                acc.append(lines[i]); i += 1
            if i < n: i += 1  # skip :::
            inner = blocks("\n".join(acc).strip())
            t = ('<h4 class="callout-t">%s</h4>' % inline(callout_title)) if callout_title else ""
            out.append('<div class="callout callout-%s">%s<div class="callout-body">%s</div></div>' % (callout_type, t, inner))
            continue
        # fenced code
        if l.strip().startswith("```"):
            i += 1
            acc = []
            while i < n and not lines[i].strip().startswith("```"):
                acc.append(lines[i]); i += 1
            i += 1
            code = "\n".join(acc)
            out.append("<pre><code>%s</code></pre>" % html.escape(code))
            continue
        # hr
        if re.match(r'^---+\s*$', l.strip()) and not l.strip().startswith("----"):
            out.append("<hr/>"); i += 1; continue
        # heading
        hm = re.match(r'^(#{3,6})\s+(.*)$', l)
        if hm:
            lvl = min(6, len(hm.group(1)))
            out.append("<h%d>%s</h%d>" % (lvl, inline(hm.group(2)), lvl))
            i += 1; continue
        hm2 = re.match(r'^(#{1,2})\s+(.*)$', l)
        if hm2:
            lvl = len(hm2.group(1))
            out.append("<h%d>%s</h%d>" % (lvl, inline(hm2.group(2)), lvl))
            i += 1; continue
        # blank
        if not l.strip():
            i += 1; continue
        # gather a paragraph/block until blank
        acc = []
        while i < n and lines[i].strip() != "":
            acc.append(lines[i]); i += 1
        # detect table
        if len(acc) >= 2 and acc[1].strip().startswith("|") and '-' in acc[1]:
            out.append(table("\n".join(acc)))
            continue
        # detect list run
        if re.match(r'^[-*]\s+', acc[0]) or re.match(r'^\d+\.\s+', acc[0]):
            out.append(list_block("\n".join(acc)))
            continue
        # plain paragraph(s)
        para = " ".join(x.strip() for x in acc if x.strip())
        out.append("<p>%s</p>" % inline(para))
    return "\n".join(out)

# ---------- navigation ----------
NAV = [
    ("Главная", "index.html"),
    ("С чего начать", None, [
        ("Обзор", "getting-started/index.html"),
        ("Установка Ubuntu", "getting-started/install-ubuntu.html"),
        ("Первые шаги", "getting-started/first-steps.html"),
        ("Загрузочная флешка", "getting-started/bootable-usb.html"),
    ]),
    ("Homelab", None, [
        ("Концепция", "homelab/index.html"),
        ("Железо", "homelab/hardware.html"),
        ("Сеть", "homelab/network.html"),
        ("Справочник сервера", "homelab/server-reference.html"),
    ]),
    ("Сервисы", None, [
        ("Обзор", "services/index.html"),
        ("Docker", "services/docker.html"),
        ("Samba", "services/samba.html"),
        ("MiniDLNA", "services/minidlna.html"),
        ("Transmission", "services/transmission.html"),
        ("Navidrome", "services/navidrome.html"),
        ("Immich", "services/immich.html"),
        ("SOPDS", "services/sopds.html"),
        ("MQTT / ESPHome", "services/mqtt.html"),
    ]),
    ("Гайды", None, [
        ("Обзор", "guides/index.html"),
        ("Диски и SMART", "guides/disk-health.html"),
        ("Диагностика", "guides/diagnostics.html"),
        ("Бекапы", "guides/backup.html"),
        ("SSH", "guides/ssh.html"),
        ("Терминал", "guides/terminal.html"),
        ("Wi-Fi фикс", "guides/wifi-fix.html"),
        ("Автосборка", "guides/auto-setup.html"),
        ("journalctl", "guides/journalctl.html"),
        ("Авто-выключение", "guides/auto-shutdown.html"),
    ]),
    ("Ресурсы", None, [
        ("Ссылки", "resources/links.html"),
        ("Git команды", "resources/git-commands.html"),
        ("INXI", "resources/inxi.html"),
        ("OpenCode на Windows", "resources/opencode-windows.html"),
    ]),
    ("Хобби", None, [
        ("Досуг", "hobbies/index.html"),
        ("Гитара", "hobbies/guitar.html"),
    ]),
]

def nav_html(current, prefix):
    def href(p):
        return prefix + p
    parts = []
    for group in NAV:
        label = group[0]
        sub = group[2] if len(group) > 2 and group[2] else None
        if sub:
            subs = "".join(
                '<a class="nli%s" href="%s">%s</a>' % (" on" if s[1] == current else "", href(s[1]), s[0])
                for s in sub)
            parts.append('<div class="ngroup"><div class="ngt">%s</div>%s</div>' % (label, subs))
        else:
            cls = " on" if group[1] == current else ""
            parts.append('<a class="nmain%s" href="%s">%s</a>' % (cls, href(group[1]), label))
    return "\n".join(parts)

HEAD = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Цифровая Крепость</title>
<meta name="description" content="{desc}">
<link rel="icon" type="image/svg+xml" href="{fav}">
<style>
:root{{--bg:#0d1117;--panel:#161b22;--line:#21262d;--text:#e6edf3;--dim:#8b98a8;--accent:#4fc3f7;--code:#1f6feb;--green:#3fb950;--tip:#1f6feb;--note:#8957e5}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--text);font-family:system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;line-height:1.65;font-size:16px}}
.layout{{display:flex;min-height:100vh}}
aside{{width:270px;flex-shrink:0;background:var(--panel);border-right:1px solid var(--line);padding:16px 12px;position:sticky;top:0;height:100vh;overflow-y:auto}}
.brand{{font-size:17px;font-weight:700;color:var(--accent);padding:6px 10px 14px;border-bottom:1px solid var(--line);margin-bottom:12px}}
.ngroup{{margin-bottom:10px}}
.ngt{{font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:var(--dim);padding:6px 10px 4px}}
a.nli{{display:block;padding:6px 12px;color:var(--text);text-decoration:none;border-radius:6px;font-size:14px}}
a.nli:hover{{background:#21262d;color:#fff}}
a.nli.on{{background:var(--accent);color:#04141f;font-weight:600}}
a.nmain{{display:block;padding:7px 10px;color:var(--accent);text-decoration:none;font-weight:600;border-radius:6px;font-size:14px}}
a.nmain:hover{{background:#21262d}}
main{{flex:1;padding:40px 48px;max-width:860px}}
h1{{font-size:30px;margin-bottom:6px;color:var(--accent)}}
.desc{{color:var(--dim);margin-bottom:26px;font-size:16px}}
h2{{font-size:23px;margin:30px 0 12px;color:var(--accent);border-bottom:1px solid var(--line);padding-bottom:6px}}
h3{{font-size:19px;margin:24px 0 10px}}
h4{{font-size:16px;margin:18px 0 8px}}
p{{margin:0 0 14px}}
ul,ol{{margin:0 0 16px 22px}}
li{{margin:3px 0}}
a{{color:var(--accent)}}
a:hover{{text-decoration:none}}
code{{background:#21262d;padding:2px 6px;border-radius:4px;font-family:ui-monospace,Consolas,monospace;font-size:.88em;color:var(--green)}}
pre{{background:#0b0e14;border:1px solid var(--line);border-radius:8px;padding:14px;overflow-x:auto;margin:0 0 16px}}
pre code{{background:transparent;padding:0;color:var(--green)}}
table{{width:100%;border-collapse:collapse;margin:0 0 18px;font-size:14px}}
th,td{{border:1px solid var(--line);padding:8px 10px;text-align:left}}
th{{background:var(--panel);color:var(--accent);font-weight:600}}
tr:nth-child(even) td{{background:#14181f}}
hr{{border:none;border-top:1px solid var(--line);margin:24px 0}}
em{{color:var(--dim)}}
.callout{{border-left:4px solid var(--tip);background:rgba(31,111,239,.08);border-radius:6px;padding:12px 14px;margin:0 0 16px}}
.callout-note{{border-color:var(--note);background:rgba(137,87,229,.08)}}
.callout-warning{{border-color:#e3b341;background:rgba(227,179,65,.08)}}
.callout-t{{color:var(--accent);font-size:13px;text-transform:uppercase;letter-spacing:.04em}}
.callout-body p:last-child{{margin-bottom:0}}
footer{{margin-top:44px;padding-top:16px;border-top:1px solid var(--line);color:var(--dim);font-size:13px}}
@media(max-width:820px){{.layout{{flex-direction:column}}aside{{width:100%;height:auto;position:static}}main{{padding:24px 18px}}}}
</style>
</head>
<body>
<div class="layout">
<aside><div class="brand">🛡️ Цифровая Крепость</div>
{nav}
</aside>
<main>
"""

def page_html(title, desc, body_html, current, prefix):
    # заменить абсолютные "/..." на относительные с префиксом глубины
    body_html = re.sub(r'href="/', 'href="' + prefix, body_html)
    nav = nav_html(current, prefix)
    return HEAD.format(title=html.escape(title), desc=html.escape(desc),
                       nav=nav, fav=prefix+"favicon.svg") + body_html + """
<footer>Цифровая Крепость — образовательный сайт о Linux и homelab. Все примеры проверены на реальном сервере.</footer>
</main>
</div>
</body>
</html>"""

def main():
    os.makedirs(OUT, exist_ok=True)
    pages = []
    for root, dirs, files in os.walk(SRC):
        for f in files:
            if f.endswith(".md") or f.endswith(".mdx"):
                full = os.path.join(root, f)
                rel = os.path.relpath(full, SRC)  # e.g. getting-started/index.mdx
                rel_noext = os.path.splitext(rel)[0]
                with open(full, encoding="utf-8") as fh:
                    text = fh.read()
                meta, body = parse_frontmatter(text)
                title = meta.get("title", rel_noext.replace("/", " / "))
                desc = meta.get("description", "")
                body_html = blocks(body)
                if rel_noext == "index":
                    out_name = "index.html"
                else:
                    out_name = rel_noext + ".html"
                outf = os.path.join(OUT, out_name)
                os.makedirs(os.path.dirname(outf), exist_ok=True)
                depth = rel_noext.count("/")
                prefix = "../" * depth
                with open(outf, "w", encoding="utf-8") as fh:
                    fh.write(page_html(title, desc, body_html, out_name.replace("\\", "/"), prefix))
                pages.append(out_name.replace("\\", "/"))
                print("generated:", out_name)
    # resources overview (нет index.mdx)
    top = os.path.join(OUT, "resources/index.html")
    if not os.path.exists(top):
        with open(top, "w", encoding="utf-8") as fh:
            fh.write(page_html("Ресурсы", "Полезные ссылки и материалы",
                '<h1>Ресурсы</h1><p class="desc">Полезный набор материалов для изучения Linux и homelab.</p>'
                '<ul><li><a href="links.html">Полезные ссылки</a></li>'
                '<li><a href="git-commands.html">Git команды</a></li>'
                '<li><a href="inxi.html">INXI</a></li>'
                '<li><a href="opencode-windows.html">OpenCode на Windows</a></li></ul>',
                "resources/index.html", "../"))
    print("TOTAL:", len(pages))

if __name__ == "__main__":
    main()
