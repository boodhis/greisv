# Цифровая Крепость

Образовательный сайт о Linux, homelab и самостоятельном администрировании.
Статический сайт на GitHub Pages: **https://boodhis.github.io/greisv/**

Проект собран максимально бесплатно и из открытого кода: только HTML/CSS/JS,
никакого `npm` и сборки. Вся логика — в браузере (localStorage), сайт умеет
работать офлайн (PWA).

## Что внутри

- **🔁 Тренажёр карточек** (`study/words.html`) — интервальное повторение
  (слова, команды терминала, гитара, лады), прогресс в `localStorage`.
- **🗒 Шпаргалки** (`study/cheatsheets.html`) — git, systemd, Docker, сеть.
- **⚡ Электрика** (`electric/`) — безопасность, щиты и автоматы, кабели, умный дом.
- **🏗 Манифест** (`manifest.html`) — принципы: бесплатно, открыто, офлайн.
- **📴 PWA**: `sw.js` (офлайн-кеш), `manifest.webmanifest`, иконки.
- **🎨 «Стена Крепости»** — холст на главной; роспись сохраняется в браузере.
- Виджет **«Слово дня»** — в футере страниц.

## Структура

```
/
├── index.html                 — Главная (hero, карточки, стена-подложка)
├── manifest.html              — Манифест проекта
├── style.css                  — Единая тёмная тема
├── js/wall.js                 — Стена-подложка для надписей (весь экран)
├── sw.js / manifest.webmanifest / icon-192.png / icon-512.png — PWA/офлайн
├── study/                     — «Обучение»: тренажёр, шпаргалки
│   └── data/  deck.js · srs.js · wordday.js · widget.js
├── electric/                  — «Электрика» (генерируется gen/gen_electric.py)
├── getting-started/ homelab/ services/ guides/ resources/ hobbies/
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
python3 gen/gen_deck.py     # words.txt (с панели Heltec) → study/data/deck.js
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

MIT