---
title: Transmission
description: Настройка торрент-клиента на сервере
---

## Transmission: Торренты на сервере

**Transmission** — лёгкий торрент-клиент с веб-интерфейсом. Идеально подходит для сервера.

### Установка

```bash
sudo apt update && sudo apt install -y transmission-daemon
```

### Настройка

```bash
sudo nano /etc/transmission-daemon/settings.json
```

Основные параметры:

```json
{
  "download-dir": "/mnt/2tb/downloads",
  "incomplete-dir": "/mnt/2tb/downloads/temp",
  "rpc-whitelist": "127.0.0.1,192.168.1.*",
  "rpc-host-whitelist-enabled": false,
  "rpc-authentication-required": true,
  "rpc-username": "iva",
  "rpc-password": "пароль"
}
```

:::tip[Разбор параметров]
- `download-dir` — папка для скачанных файлов
- `rpc-whitelist` — список разрешённых IP для веб-интерфейса
- `rpc-authentication-required` — требовать авторизацию
:::

### Запуск

```bash
sudo systemctl restart transmission-daemon
sudo systemctl enable transmission-daemon
```

### Доступ

Открой в браузере: `http://192.168.1.100:9091`

Введи логин и пароль.

### Управление

```bash
# Статус
sudo systemctl status transmission-daemon

# Перезапуск
sudo systemctl restart transmission-daemon

# Логи
journalctl -u transmission-daemon -f
```

### Добавление торрентов

1. Открой веб-интерфейс
2. Нажми "Добавить"
3. Введи ссылку или загрузи .torrent файл
4. Выбери папку для скачивания

### Автоматическая загрузка

Можно настроить автоматическую загрузку torrent-файлов из папки:

```json
{
  "watch-dir": "/mnt/2tb/torrents",
  "watch-dir-enabled": true
}
```

---

*Transmission — простой и надёжный торрент-клиент для сервера.*
