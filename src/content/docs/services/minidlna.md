---
title: MiniDLNA
description: Настройка медиа-сервера для ТВ и других устройств
---

## MiniDLNA: Медиа-сервер

**MiniDLNA** — простой медиа-сервер, совместимый с DLNA/UPnP. Позволяет смотреть видео, слушать музыку и смотреть фото на ТВ и других устройствах.

### Установка

```bash
sudo apt update && sudo apt install -y minidlna
```

### Настройка

```bash
sudo nano /etc/minidlna.conf
```

Основные параметры:

```ini
# Имя сервера (видно на ТВ)
friendly_name=HomeLab Media

# Папки с медиа
media_dir=V,/mnt/2tb/фильмы
media_dir=A,/mnt/2tb/muz
media_dir=P,/mnt/storage/фото

# Автоматическое обновление
inotify=yes

# Порт (по умолчанию 8200)
port=8200
```

:::tip[Разбор параметров]
- `friendly_name` — имя сервера в списке источников ТВ
- `media_dir=V` — видео, `A` — аудио, `P` — фото
- `inotify=yes` — автоматически обновлять базу при изменении файлов
:::

### Права доступа

Если файлы находятся в домашней директории:

```bash
sudo setfacl -m u:minidlna:x /home/iva
sudo setfacl -R -m u:minidlna:rx /home/iva/доступные_папки
```

:::tip[Разбор команды]
`setfacl` — управление списками контроля доступа (ACL). Даёт minidlna права на чтение файлов.
:::

### Запуск

```bash
sudo systemctl restart minidlna
sudo systemctl enable minidlna
```

### Проверка

1. Включи ТВ в той же сети
2. Найди источник "HomeLab Media" (или как назвал)
3. Должны появиться папки с медиа

### Пересканирование базы

Если база не обновляется:

```bash
# Удали старую базу
sudo rm /var/cache/minidlna/*

# Перезапусти сервис
sudo systemctl restart minidlna
```

### Полезные команды

```bash
# Статус сервиса
sudo systemctl status minidlna

# Просмотр логов
journalctl -u minidlna -f

# Принудительное сканирование
sudo minidlnad -R
```

---

*MiniDLNA — простой и надёжный медиа-сервер для домашнего использования.*
