---
title: journalctl
description: Работа с системными логами через journalctl
---

## journalctl: Системные логи

**journalctl** — утилита для просмотра системных логов в systemd. Помогает найти ошибки и понять что происходит в системе.

### Базовые команды

```bash
# Все логи текущей загрузки
journalctl

# Ошибки текущей загрузки
journalctl -p 3 -xb

# Последние 100 строк
journalctl -n 100
```

:::tip[Разбор команды]
- `-p 3` — приоритет ошибок (3 = error)
- `-xb` — текущая загрузка
- `-n 100` — последние 100 строк
:::

### Фильтрация по времени

```bash
# За последний час
journalctl --since "1 hour ago"

# За последние 10 минут
journalctl --since "10 minutes ago"

# Конкретная дата
journalctl --since "2024-01-01" --until "2024-01-02"
```

:::tip[Разбор команды]
- `--since` — начиная с указанного времени
- `--until` — до указанного времени
:::

### Фильтрация по сервису

```bash
# Логи конкретного сервиса
journalctl -u docker.service

# Логи Docker за последний час
journalctl -u docker.service --since "1 hour ago"

# Логи SSH
journalctl -u ssh.service
```

:::tip[Разбор команды]
`-u` — фильтрация по имени сервиса (unit).
:::

### Просмотр логов в реальном времени

```bash
# Все новые логи
journalctl -f

# Только ошибки
journalctl -f -p 3

# Конкретный сервис
journalctl -u docker.service -f
```

:::tip[Разбор команды]
`-f` — следить за обновлениями в реальном времени (как `tail -f`).
:::

### Полезные комбинации

```bash
# Ошибки Docker за последние 24 часа
journalctl -u docker.service -p 3 --since "24 hours ago"

# Все failed сервисы
journalctl --failed

# Логи ядра
journalctl -k

# Логи конкретного процесса
journalctl _PID=1234
```

### Очистка логов

```bash
# Удалить логи старше 3 дней
sudo journalctl --vacuum-time=3d

# Удалить логи размером больше 500M
sudo journalctl --vacuum-size=500M
```

:::tip[Разбор команды]
- `--vacuum-time` — удалить записи старше указанного времени
- `--vacuum-size` — удалить записи превышающие размер
:::

### Сохранение логов

По умолчанию логи хранятся в `/var/log/journal/`. Для постоянного хранения:

```bash
sudo mkdir -p /var/log/journal
sudo systemd-tmpfiles --create --prefix /var/log/journal
```

### Готово!

Теперь ты можешь:
- ✅ Просматривать логи системы
- ✅ Фильтровать по времени и сервису
- ✅ Искать ошибки
- ✅ Очищать старые логи

---

*journalctl — основной инструмент для диагностики проблем в systemd.*
