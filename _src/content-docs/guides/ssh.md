---
title: SSH
description: Удалённый доступ к серверу
---

## SSH: Удалённый доступ

**SSH** (Secure Shell) — протокол для безопасного удалённого подключения к серверу.

### Установка SSH-сервера

```bash
sudo apt update && sudo apt install -y openssh-server
```

### Подключение

```bash
ssh username@ip_address

# Пример
ssh iva@192.168.1.100
```

:::tip[Разбор команды]
- `ssh` — команда для подключения
- `username` — имя пользователя на сервере
- `ip_address` — IP-адрес сервера
:::

### Ключи вместо паролей

#### Генерация ключа

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

:::tip[Разбор команды]
- `ed25519` — современный и безопасный алгоритм
- `-C` — комментарий (обычно email)
:::

#### Копирование ключа на сервер

```bash
ssh-copy-id username@ip_address
```

#### Подключение с ключом

```bash
ssh -i ~/.ssh/id_ed25519 username@ip_address
```

### Отключение парольной авторизации

Для безопасности лучше отключить пароли:

```bash
# На сервере
sudo nano /etc/ssh/sshd_config
```

Добавь или измени:

```
PasswordAuthentication no
PubkeyAuthentication yes
```

Перезапусти SSH:

```bash
sudo systemctl restart ssh
```

### Туннелирование (Port Forwarding)

```bash
# Локальный туннель (доступ к порту на сервере через localhost)
ssh -L 8080:localhost:80 username@ip_address

# Удалённый туннель (доступ к порту на клиенте через сервер)
ssh -R 9090:localhost:3000 username@ip_address
```

:::tip[Разбор команды]
- `-L` — локальный порт пробрасывается на сервер
- `-R` — удалённый порт пробрасывается на клиент
:::

### Полезные опции

```bash
# Подключение с указанием порта
ssh -p 2222 username@ip_address

# Сжатие данных
ssh -C username@ip_address

# Фоновый режим
ssh -f -N username@ip_address
```

### Готово!

Теперь ты можешь:
- ✅ Подключаться к серверу удалённо
- ✅ Использовать ключи для авторизации
- ✅ Настроить туннели для безопасного доступа

---

*SSH — основа удалённой работы. Настрой ключи для безопасности.*
