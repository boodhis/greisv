#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Инжектит в старые страницы (со своим инлайн-стилем) следующие блоки:
  - ссылку «Манифест» в верхнюю навигацию (рядом с «Главная»);
  - новые группы навигации «Обучение» и «Электрика» перед группой «Homelab»;
  - виджет «Слова дня» и подключение wordday.js / widget.js / sw.js перед </body>.

Запуск из корня проекта:  python3 gen/inject.py
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLD_DIRS = ["getting-started", "homelab", "services", "guides", "resources", "hobbies"]
SKIP = {"esp32.html"}

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


def inject(path):
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

    if html != orig:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
    return changed


def main():
    files = []
    for d in OLD_DIRS:
        dd = os.path.join(ROOT, d)
        if not os.path.isdir(dd):
            continue
        for name in sorted(os.listdir(dd)):
            if name.endswith(".html") and name not in SKIP:
                files.append(os.path.join(dd, name))
    for path in files:
        changed = inject(path)
        print(("+" if changed else "="), os.path.relpath(path, ROOT))
    print("Обработано страниц:", len(files))


if __name__ == "__main__":
    main()