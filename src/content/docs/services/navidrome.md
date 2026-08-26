---
title: Navidrome
description: Музыкальный сервер для стриминга своей музыки
---

## Navidrome: Свой Spotify

**Navidrome** — это музыкальный сервер для стриминга своей коллекции. Работает как Spotify, но с твоей музыкой.

### Возможности

- 🎵 Стриминг музыки из любой точки мира
- 📱 Веб-интерфейс + мобильные приложения
- 🎨 Красивые обложки альбомов
- 📋 Плейлисты и рекомендации
- 🔍 Умный поиск по тегам

### Установка через Docker

Создай `docker-compose.yml`:

```yaml
version: '3.8'

services:
  navidrome:
    image: deluan/navidrome:latest
    container_name: navidrome
    restart: unless-stopped
    ports:
      - "4533:4533"
    environment:
      ND_SCANSCHEDULE: "@every 1h"
      ND_LOGLEVEL: info
      ND_BASEURL: ""
    volumes:
      - ./data:/data
      - /mnt/2tb/muz:/music:ro
```

Запуск:

```bash
mkdir -p /home/iva/services/navidrome
cd /home/iva/services/navidrome
# Вставь docker-compose.yml выше
docker compose up -d
```

:::tip[Разбор команды]
- `ND_SCANSCHEDULE: "@every 1h"` — сканировать музыку каждый час
- `- /mnt/2tb/muz:/music:ro` — монтировать папку с музыкой (read-only)
:::

### Доступ

Открой в браузере: `http://192.168.1.100:4533`

### Структура музыки

Navidrome ожидает структуру:

```
/mnt/2tb/muz/
├── Исполнитель 1/
│   ├── Альбом 1/
│   │   ├── 01 - Трек.mp3
│   │   └── 02 - Трек.mp3
│   └── Альбом 2/
└── Исполнитель 2/
    └── ...
```

### Теги файлов

Для лучшего отображения нужно заполнить теги:

- **Artist** — имя исполнителя
- **Album** — название альбома
- **Title** — название трека
- **Year** — год выпуска
- **Genre** — жанр

Инструменты для тегов: `Picard`, `Kid3`, `EasyTAG`.

### Настройка

Основные настройки в веб-интерфейсе:

- **Сканирование**: автоматическое обновление каждые 2 часа
- **Обложки**: автоматическая загрузка из iTunes
- **Плейлисты**: создание и импорт

### Мобильные приложения

- **Android**: Symfonium, Ultrasonic
- **iOS**: Amperfy, play:Sub

### Полезные команды

```bash
# Статус
docker ps | grep navidrome

# Логи
docker logs navidrome -f

# Перезапуск
docker restart navidrome

# Обновление
docker compose pull && docker compose up -d
```

---

*Navidrome — отличная замена стриминговым сервисам. Твоя музыка — твои правила.*
