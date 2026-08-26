---
title: Git команды
description: Основные команды Git
---

## Git: Система контроля версий

**Git** — система контроля версий. Позволяет отслеживать изменения в коде и откатывать ошибки.

### Установка

```bash
sudo apt install -y git
```

### Базовые команды

#### Настройка

```bash
# Имя и email
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# Текущие настройки
git config --list
```

#### Создание репозитория

```bash
# Инициализация нового репозитория
git init

# Клонирование существующего
git clone https://github.com/user/repo.git
```

#### Работа с файлами

```bash
# Статус
git status

# Добавление файлов
git add file.txt        # один файл
git add .               # все файлы

# Коммит
git commit -m "Описание изменений"

# Просмотр истории
git log
git log --oneline       # компактный вид
```

:::tip[Разбор команды]
- `git add` — добавить файлы в индекс (подготовить к коммиту)
- `git commit` — сохранить изменения
- `-m` — сообщение коммита
:::

#### Ветки

```bash
# Список веток
git branch

# Создание ветки
git branch feature

# Переключение на ветку
git checkout feature
git switch feature     # современный способ

# Слияние веток
git checkout main
git merge feature
```

:::tip[Разбор команды]
- `git branch` — управление ветками
- `git checkout/switch` — переключение между ветками
- `git merge` — слияние изменений из другой ветки
:::

#### Удалённые репозитории

```bash
# Просмотр удалённых
git remote -v

# Отправка изменений
git push origin main

# Получение изменений
git pull origin main
```

:::tip[Разбор команды]
- `git remote` — управление удалёнными репозиториями
- `git push` — отправить изменения на сервер
- `git pull` — получить изменения с сервера
:::

### Полезные команды

```bash
# Отмена изменений
git checkout -- file.txt     # отменить изменения в файле
git reset HEAD file.txt      # убрать из индекса

# История изменений файла
git log --follow file.txt

# Разница между коммитами
git diff
git diff commit1 commit2

# Статистика
git shortlog -sn
```

### .gitignore

Создай файл `.gitignore` для игнорирования ненужных файлов:

```
# Системные файлы
.DS_Store
Thumbs.db

# Зависимости
node_modules/
vendor/

# Собранные файлы
dist/
build/
```

### Готово!

Теперь ты можешь:
- ✅ Инициализировать репозитории
- ✅ Делать коммиты
- ✅ Работать с ветками
- ✅ Отправлять и получать изменения

---

*Git — незаменимый инструмент для любых проектов.*
