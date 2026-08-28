# Цифровая Крепость

Образовательный сайт о Linux и homelab-самостоятельности.

Простой статичный HTML-сайт на GitHub Pages: `https://boodhis.github.io/greisv/`

## Структура

```
/
├── index.html          — Главная
├── getting-started/    — С чего начать (Linux)
├── homelab/            — Концепция, железо, сеть, сервер
├── services/           — Сервисы (Docker, Samba, Navidrome, ...)
├── guides/             — Гайды и инструкции
├── resources/          — Полезные ссылки
├── hobbies/            — Хобби (досуг, гитара)
├── favicon.svg         — Иконка сайта
└── _src/               — Исходники (генерируются по желанию)
    ├── convert.py      — Конвертер Markdown → HTML
    └── content-docs/   — Исходники контента в Markdown
```

Никакой сборки, никакого `npm`. Это просто HTML-файлы — их можно открыть сразу в браузере или закоммитить в git.

## Как править сайт через VS Code (Remote-SSH)

Сайт живёт на сервере `iva@192.168.0.244` в `~/greisv/`. Проще всего править его удалённо через VS Code:

1. Открой VS Code.
2. `Ctrl+Shift+P` → **Remote-SSH: Connect to Host…** → выбери/введи `iva@192.168.0.244` (вход по SSH-ключу).
3. `File → Open Folder…` → укажи `~/greisv`.
4. В проводнике слева открывай нужный `.html` (например `services/docker.html`) и правь текст.
5. `Ctrl+S` — сохрани. Изменения сразу локальные в этом файле.
6. Коммит: `Ctrl+Shift+G` (панель Git) → подпиши сообщение → жми **✓ Commit**, затем **↻ Sync/Push** (или в терминале: `git add . && git commit -m "..." && git push`).
7. GitHub Actions автоматически задеплоит сайт на GitHub Pages. Через ~1 мин проверь на `https://boodhis.github.io/greisv/`.

Полезные плагины: **Live Server** (правый клик по `index.html` → «Open with Live Server» для локального предпросмотра), **HTML CSS Support**.

## Проще: как добавить/изменить страницу

- **Поправить текст** — открой нужный `.html`, найди текст, отредактируй.
- **Добавить пункт в навигацию** — открой любой `.html`, найди блок `<aside>…</aside>`, скопируй строку `<a class="nli" href="...">…</a>` и добавь новую.
- **Добавить страницу** — скопируй существующий `.html`, переименуй, отредактируй содержимое `<main>…</main>`, добавь ссылку на неё в навигацию всех страниц.

## Регенерация из Markdown-исходников (опционально)

Если хочется вести контент в Markdown, а не в HTML:

1. Отредактируй файл в `_src/content-docs/` (например `_src/content-docs/services/docker.md`).
2. Сгенерируй сайт:

```bash
cd ~/greisv
python3 _src/convert.py
```

Это пересоберёт все `.html` из `.md`-исходников.

## Деплой

Автоматический: push в `main` → GitHub Actions (публикует файлы из корня) → GitHub Pages.

URL: `https://boodhis.github.io/greisv/`
```

## Лицензия

MIT
