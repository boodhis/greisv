#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Проверки сайта «Цифровая Крепость»: целостность ссылок, наличие колод,
генераторов и PWA-файлов. Запуск: python3 -m pytest tests/ -q  (или python3 tests/test_site.py)
"""
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROOT = Path(sys.path[0])

try:
    import pytest
    HAS_PYTEST = True
except ImportError:
    HAS_PYTEST = False


def all_html_files():
    return [p for p in ROOT.rglob("*.html")
            if "gen" not in p.parts and "tests" not in p.parts and "node_modules" not in p.parts]


def collect_links(path):
    html = path.read_text(encoding="utf-8")
    return re.findall(r'href="([^"#]+)"', html)


def resolve(path, href):
    target = (path.parent / href).resolve()
    return target


def check(path):
    errors = []
    for href in collect_links(path):
        if href.startswith(("http:", "https:", "mailto:", "//")):
            continue
        t = resolve(path, href)
        if not t.exists():
            errors.append(f"  битая ссылка {href} -> {t}")
    return errors


def test_all_links_resolve():
    errors = []
    for p in all_html_files():
        errors += [(str(p), e) for e in check(p)]
    assert not errors, "\n" + "\n".join(f"{p}: {e}" for p, e in errors)


def test_gen_deck_output():
    wd = ROOT / "study/data/wordday.js"
    assert wd.exists(), "нет study/data/wordday.js"
    text = wd.read_text(encoding="utf-8")
    assert "window.SRS_DAY" in text
    cards = text.count('",')
    assert cards >= 20, "в wordday.js подозрительно мало карточек"
    assert text.count('[') >= 20 and text.count(']') >= 20, "wordday.js битый (скобки)"


def test_pwa_files():
    for name in ("manifest.webmanifest", "sw.js", "icon-192.png", "icon-512.png"):
        assert (ROOT / name).exists(), f"нет {name} — запусти gen/gen_icons.py"


def test_key_pages():
    for rel in ("index.html", "manifest.html", "study/index.html",
                "study/cheatsheets.html", "electric/index.html", "electric/safety.html",
                "electric/panels.html", "electric/wiring.html", "electric/smart.html",
                "style.css", "study/data/srs.js", "study/data/wordday.js", "study/data/widget.js"):
        assert (ROOT / rel).exists(), f"нет {rel}"


def _sw_assets():
    sw = (ROOT / "sw.js").read_text(encoding="utf-8")
    m = re.search(r'var ASSETS = \[(.*?)\];', sw, re.S)
    assert m, "в sw.js нет массива ASSETS"
    return set(re.findall(r'"([^"]+)"', m.group(1)))


def test_sw_precache_covers_all_pages():
    assets = _sw_assets()
    missing = []
    for p in all_html_files():
        rel = p.relative_to(ROOT).as_posix()
        if rel not in assets and "./" + rel not in assets:
            missing.append(rel)
    assert not missing, "не в precache sw.js: " + ", ".join(missing)


def test_sitemap_covers_all_pages():
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    locs = set(re.findall(r'<loc>https://boodhis\.github\.io/greisv/([^<]*)</loc>', sitemap))
    locs = {x if x else "index.html" for x in locs}
    missing = [p.relative_to(ROOT).as_posix() for p in all_html_files()
               if p.relative_to(ROOT).as_posix() not in locs]
    assert not missing, "не в sitemap.xml: " + ", ".join(missing)


def test_trainer_tags():
    """Тренажёр слов живёт в study/data (srs.js, widget.js); на главной его нет."""
    wid = (ROOT / "study/data/widget.js").read_text(encoding="utf-8")
    srs = (ROOT / "study/data/srs.js").read_text(encoding="utf-8")
    idx = (ROOT / "index.html").read_text(encoding="utf-8")
    assert 'id="wordday"' not in idx, "на главной больше нет виджета «Слово дня»"
    for needle in ('SRS_DAY', 'SRS.grade', 'wd-forgot', 'wd-ok'):
        assert needle in wid, f"в study/data/widget.js нет {needle}"
    assert "srs_state_v1" in srs, "в study/data/srs.js нет ключа srs_state_v1"
    assert "11520" in srs, "в srs.js нет интервала 11520"


def test_no_empty_wordday():
    """Виджет требует #wordday с .wd-w; скрытый пустой блок ломает widget.js.
       Страницы без слова дня вообще не должны его содержать."""
    for p in all_html_files():
        html = p.read_text(encoding="utf-8")
        if 'id="wordday"' not in html:
            continue
        assert 'wd-w' in html, f"{p}: #wordday без структуры (.wd-w) сломает widget.js"
        assert 'study/data/widget.js' in html, f"{p}: #wordday есть, но widget.js не подключён"


def test_html_structure():
    """Каждая страница — валидный каркас: doctype, lang, title, viewport, desc, favicon."""
    for p in all_html_files():
        html = p.read_text(encoding="utf-8")
        assert re.search(r"<!doctype html>", html, re.I), f"{p}: нет doctype"
        assert "lang=\"ru\"" in html, f"{p}: нет lang=ru"
        m = re.search(r"<title>(.*?)</title>", html, re.S)
        assert m and m.group(1).strip(), f"{p}: пустой/нет title"
        assert "Цифровая Крепость" in m.group(1), f"{p}: title без бренда"
        assert "name=\"viewport\"" in html and "width=device-width" in html, f"{p}: нет viewport"
        assert "name=\"description\"" in html, f"{p}: нет meta description"
        assert "rel=\"icon\"" in html, f"{p}: нет favicon"


VOID_TAGS = {"area","base","br","col","embed","hr","img","input","link","meta","param","source","track","wbr"}


def _strip_code_html(html):
    html = re.sub(r"<script\b.*?</script>", "", html, flags=re.S | re.I)
    html = re.sub(r"<style\b.*?</style>", "", html, flags=re.S | re.I)
    return html


def test_tags_balanced():
    from collections import Counter
    for p in all_html_files():
        html = _strip_code_html(p.read_text(encoding="utf-8"))
        opens = Counter(re.findall(r"<([a-zA-Z][a-zA-Z0-9]*)\b", html))
        closes = Counter(re.findall(r"</([a-zA-Z][a-zA-Z0-9]*)\s*>", html))
        for tag, n in opens.items():
            if tag.lower() in VOID_TAGS:
                continue
            got = closes.get(tag, 0)
            assert got == n, f"{p}: <{tag}> открыт {n}, закрыт {got}"
        for tag, n in closes.items():
            if tag.lower() in VOID_TAGS:
                continue
            assert opens.get(tag, 0) == n, f"{p}: лишний </{tag}>"


def test_unique_ids():
    for p in all_html_files():
        html = p.read_text(encoding="utf-8")
        ids = re.findall(r"id=\"([^\"]+)\"", html)
        dups = sorted({i for i in ids if ids.count(i) > 1})
        assert not dups, f"{p}: дубли id: {dups}"


def test_no_redundant_back():
    """Не должно быть ручной «← на главную» (дублирует чип «Главная» в frow)
    и дублей inline-стиля рамки (инжектор не должен наслаивать второй <style>)."""
    for p in all_html_files():
        html = p.read_text(encoding="utf-8")
        if 'class="fnav"' in html:
            assert 'aria-label="на главную"' not in html, f"{p}: лишняя ссылка «← на главную»"
            assert '>← на главную<' not in html, f"{p}: лишняя ссылка «← на главную»"
            n = html.count(".fnav{")
            assert n <= 1, f"{p}: {n} inline-блоков .fnav{{ — инжектор задвоил стиль"


def _run():
    import traceback
    failed = 0
    for fn in list(globals()):
        if fn.startswith("test_") and callable(globals()[fn]):
            try:
                globals()[fn]()
                print("PASS", fn)
            except AssertionError as e:
                failed += 1
                print("FAIL", fn, "\n", e)
            except Exception as e:
                failed += 1
                traceback.print_exc()
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    _run()