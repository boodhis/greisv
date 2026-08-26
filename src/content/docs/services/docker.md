---
title: Docker
description: Контейнеризация с Docker
---

## Docker: Контейнеры для сервисов

**Docker** — это платформа для запуска приложений в контейнерах. Контейнер — это изолированная среда с приложением и его зависимостями.

### Зачем нужен Docker?

| Проблема | Решение Docker |
|----------|----------------|
| "У меня всё работает, а у тебя нет" | Контейнер работает одинаково везде |
| "Зависимости конфликтуют" | Каждый сервис в своём контейнере |
| "Сложно удалить" | Один контейнер — один сервис |

### Установка Docker

```bash
# Установка Docker
curl -fsSL https://get.docker.com | sh

# Добавление текущего пользователя в группу docker
sudo usermod -aG docker $USER

# Перелогинься для применения изменений
```

:::tip[Разбор команды]
- `curl -fsSL https://get.docker.com | sh` — скачивает и запускает скрипт установки Docker
- `usermod -aG docker $USER` — добавляет текущего пользователя в группу `docker` (для работы без sudo)
:::

### Базовые команды

#### Проверка установки
```bash
docker --version
docker run hello-world
```

#### Управление контейнерами
```bash
# Список запущенных контейнеров
docker ps

# Список всех контейнеров (включая остановленные)
docker ps -a

# Остановить контейнер
docker stop <имя_контейнера>

# Удалить контейнер
docker rm <имя_контейнера>

# Посмотреть логи
docker logs <имя_контейнера>
```

:::tip[Разбор команды]
- `docker ps` — показывает работающие контейнеры
- `-a` — все контейнеры (включая остановленные)
- `logs` — выводит логи контейнера
:::

### Docker Compose

**Docker Compose** — инструмент для управления несколькими контейнерами через один файл.

Пример `docker-compose.yml`:

```yaml
version: '3.8'

services:
  navidrome:
    image: deluan/navidrome:latest
    container_name: navidrome
    ports:
      - "4533:4533"
    volumes:
      - ./data:/data
      - /mnt/2tb/muz:/music:ro
    restart: unless-stopped
```

Запуск:

```bash
docker compose up -d
```

:::tip[Разбор команды]
- `image` — Docker-образ для скачивания
- `ports` — проброс портов (хост:контейнер)
- `volumes` — монтирование директорий
- `restart: unless-stopped` — автозапуск после перезагрузки
:::

### Полезные команды

```bash
# Скачать образ
docker pull navidrome/navidrome

# Запустить контейнер
docker run -d --name navidrome -p 4533:4533 navidrome/navidrome

# Удалить все остановленные контейнеры
docker container prune

# Удалить неиспользуемые образы
docker image prune -a
```

### Примеры сервисов

Смотри наши инструкции по настройке:
- [Navidrome](/services/navidrome) — музыка
- [Immich](/services/immich) — фото
- [Transmission](/services/transmission) — торренты

---

*Docker делает управление сервисами простым и предсказуемым.*
