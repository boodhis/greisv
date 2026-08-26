---
title: Immich
description: Фотохранилище — замена Google Photos
---

## Immich: Своё облако для фото

**Immich** — это высокопроизводительная система для хранения фотографий и видео. Альтернатива Google Photos с полным контролем над данными.

### Возможности

- 📸 Автоматическое распознавание лиц
- 🗺️ Карта с геолокацией
- 📱 Мобильное приложение для автозагрузки
- 🔍 Умный поиск
- 🎬 Поддержка видео

### Установка

Следуй официальной документации: https://immich.app/docs/install/docker-compose

Базовый `docker-compose.yml`:

```yaml
version: '3.8'

services:
  immich-server:
    image: ghcr.io/immich-app/immich-server:release
    volumes:
      - /mnt/2tb/immich/upload:/usr/src/app/upload
    environment:
      - DB_PASSWORD=пароль_из_db_password.txt
      - DB_DATABASE_NAME=immich
      - DB_USERNAME=postgres
      - DB_HOSTNAME=immich-postgres
    depends_on:
      - immich-redis
      - immich-postgres
    restart: always

  immich-machine-learning:
    image: ghcr.io/immich-app/immich-machine-learning:release
    volumes:
      - /mnt/2tb/immich/model-cache:/cache
    restart: always

  immich-redis:
    image: docker.io/redis:6.2-alpine
    healthcheck:
      test: redis-cli ping || exit 1
    restart: always

  immich-postgres:
    image: docker.io/tensorchord/pgvecto-rs:pg14-v0.2.0
    environment:
      - POSTGRES_PASSWORD=пароль_из_db_password.txt
      - POSTGRES_DB=immich
      - POSTGRES_USER=postgres
      - POSTGRES_INITDB_ARGS='--data-checksums'
    volumes:
      - /mnt/2tb/immich/pgdata:/var/lib/postgresql/data
    healthcheck:
      test: pg_isready --dbname='immich' --username='postgres' || exit 1
    restart: always
```

### Доступ

Открой в браузере: `http://192.168.1.100:2283`

### Мобильное приложение

1. Скачай **Immich** из App Store / Google Play
2. Введи адрес сервера: `http://192.168.1.100:2283`
3. Введи логин и пароль
4. Включи автозагрузку

### Структура данных

```
/mnt/2tb/immich/
├── upload/         # Загруженные фото
├── pgdata/         # База данных
└── model-cache/    # Кеш моделей ML
```

### Управление

```bash
# Статус
docker ps | grep immich

# Логи
docker logs immich-server -f

# Обновление
cd /home/iva/services/immich
docker compose pull && docker compose up -d
```

### Бекапы

Важно бекапировать:
1. **Базу данных**: `docker exec immich-postgres pg_dump -U postgres immich > backup.sql`
2. **Файлы**: `rsync -av /mnt/2tb/immich/upload /mnt/storage/backups/immich/`

---

*Immich — лучшая замена Google Photos для тех, кто ценит приватность.*
