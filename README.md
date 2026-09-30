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
- Виджет **«Слово дня»** — в футере страниц.

## Структура

```
/
├── index.html                 — Главная (hero, карточки, граф-навигация)
├── manifest.html              — Манифест проекта
├── style.css                  — Единая тема «тёплая бумага» (e-ink)

├── sw.js / manifest.webmanifest / icon-192.png / icon-512.png — PWA/офлайн
├── getting-started/           — «Крепость»: ubuntu, первые шаги, флешка
├── homelab/                   — «Homelab»: железо, сеть, сервисы, гайды
├── electric/                  — «Электрика»: безопасность, щиты, монтаж,
│                                инструменты, нормативы
├── study/                     — «Обучение»: курсы, шпаргалки, разборы
│   └── data/  srs.js · wordday.js · widget.js
├── articles/                  — «Заметки»: эссе, книги, досуг
├── gen/                       — Скрипты (см. ниже)
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

## Скрипты (`gen/`)

```bash
python3 gen/inject.py    # пересобирает рамку-бар навигации на всех страницах
python3 gen/gen_icons.py # простые PNG-иконки для PWA (без зависимостей)
```

`gen/gen_electric.py` удалён: он перезаписывал `electric/*.html` старой
боковой навигацией. Электрика правится руками.

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