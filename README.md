# Цифровая Крепость

Образовательный сайт о Linux, homelab и самостоятельном администрировании.
Статический сайт на GitHub Pages: **https://boodhis.github.io/greisv/**

Проект собран максимально бесплатно и из открытого кода: только HTML/CSS/JS,
никакого `npm` и сборки. Вся логика — в браузере (localStorage), сайт умеет
работать офлайн (PWA).

## Что внутри

- **🗓 Слово дня** (виджет на главной) — мини-тренажёр английских слов с
  интервальным повторением (прогресс в `localStorage`).
- **🗒 Шпаргалки** (`study/cheatsheets.html`) — git, systemd, Docker, сеть.
- **⚡ Электрика** (`electric/`) — безопасность, щиты и автоматы, кабели, умный дом.
- **🏗 Манифест** (`manifest.html`) — принципы: бесплатно, открыто, офлайн.
- **📴 PWA**: `sw.js` (офлайн-кеш), `manifest.webmanifest`, иконки.
- **📝 Заметки страницы** (`js/notes.js`) — кнопка «📝» внизу справа; текст сохраняется в браузере (localStorage, своя заметка на каждую страницу).
- Виджет **«Слово дня»** — в футере страниц.

## Структура

```
/
├── index.html                 — Главная (hero, карточки, граф-навигация)
├── manifest.html              — Манифест проекта
├── style.css                  — Единая тёмная тема
├── js/notes.js                 — 📝 Заметки страницы (текст, localStorage)
├── sw.js / manifest.webmanifest / icon-192.png / icon-512.png — PWA/офлайн
├── study/                     — «Обучение»: слово дня, шпаргалки
│   └── data/  srs.js · wordday.js · widget.js
├── electric/                  — «Электрика» (генерируется gen/gen_electric.py)
├── getting-started/ homelab/ services/ guides/ articles/ hobbies/
│                              — разделы-статьи (исторически первый контент)
├── gen/                       — Генераторы (см. ниже)
└── tests/test_site.py         — Проверки сайта
```

## Быстрый старт

```bash
git clone git@github.com:boodhis/greisv.git
# или push-ключ: git clone git@github.com-greisv:boodhis/greisv.git
cd greisv
# правь нужный .html → git add -A && git commit -m "..." && git push
```

Push в `main` → GitHub Actions автоматически деплоит на GitHub Pages.

## Генераторы (`gen/`)

```bash
python3 gen/gen_electric.py # шаблон навигации + контент → electric/*.html
python3 gen/gen_icons.py    # простые PNG-иконки для PWA (без зависимостей)
python3 gen/inject.py       # инжектит навигацию/виджет/SW в старые страницы
```

Колоды карточек строятся из `gen/words.txt` (формат: `слово | транскрипция | перевод`,
секция команд — после маркера `# --- терминал:`).

## Тесты

```bash
python3 tests/test_site.py   # все ссылки целы, файлы на месте, ядро SRS
```

## Деплой

Автоматически: push → GitHub Actions → GitHub Pages. URL:
`https://boodhis.github.io/greisv/`

## Лицензия

- **Код** — [AGPL-3.0](LICENSE) (форки обязаны открывать изменения)
- **Тексты, статьи, манифест** — CC BY-SA 4.0
- **Данные** (words.txt, колоды) — CC0