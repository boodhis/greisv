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
    deck = ROOT / "study/data/deck.js"
    assert deck.exists(), "нет study/data/deck.js — запусти gen/gen_deck.py"
    text = deck.read_text(encoding="utf-8")
    assert "SRS_WORDS" in text and "SRS_CMDS" in text
    assert "SRS_GUITAR" in text and "SRS_FRETS" in text


def test_pwa_files():
    for name in ("manifest.webmanifest", "sw.js", "icon-192.png", "icon-512.png"):
        assert (ROOT / name).exists(), f"нет {name} — запусти gen/gen_icons.py"


def test_key_pages():
    for rel in ("index.html", "manifest.html", "study/index.html", "study/words.html",
                "study/cheatsheets.html", "electric/index.html", "electric/safety.html",
                "electric/panels.html", "electric/wiring.html", "electric/smart.html",
                "style.css", "study/data/srs.js", "study/data/wordday.js", "study/data/widget.js"):
        assert (ROOT / rel).exists(), f"нет {rel}"


def test_trainer_tags():
    words = (ROOT / "study/words.html").read_text(encoding="utf-8")
    srs = (ROOT / "study/data/srs.js").read_text(encoding="utf-8")
    for needle in ("SRS.pick", "SRS.grade", 'data-cat="words"', "deck.js", "srs.js"):
        assert needle in words, f"в study/words.html нет {needle}"
    assert "srs_state_v1" in srs, "в study/data/srs.js нет ключа srs_state_v1"
    assert "11520" in srs, "в srs.js нет интервала 11520"


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