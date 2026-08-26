---
title: Samba
description: Настройка сетевых папок для Windows/Linux/Mac
---

## Samba: Сетевые папки

**Samba** — это реализация протокола SMB/CIFS для Linux. Позволяет делиться файлами между компьютерами в сети.

### Установка

```bash
sudo apt update && sudo apt install -y samba
```

:::tip[Разбор команды]
Устанавливает Samba и все необходимые зависимости.
:::

### Базовая настройка

#### Создание общей папки

```bash
sudo mkdir -p /srv/samba/share
sudo chmod 777 /srv/samba/share
```

#### Настройка конфига

```bash
sudo nano /etc/samba/smb.conf
```

Добавь в конец файла:

```ini
[Share]
   comment = HomeLab Share
   path = /srv/samba/share
   browseable = yes
   read only = no
   guest ok = no
   create mask = 0775
   directory mask = 0775
```

#### Создание пользователя Samba

```bash
# Добавь существующего Linux-пользователя
sudo smbpasswd -a iva

# Или создай нового
sudo adduser sammy
sudo smbpasswd -a sammy
```

#### Перезапуск сервиса

```bash
sudo systemctl restart smbd
sudo systemctl enable smbd
```

:::tip[Разбор команды]
- `smbpasswd -a` — добавить пользователя в Samba
- `systemctl restart` — перезапустить сервис
- `systemctl enable` — добавить в автозагрузку
:::

### Подключение

#### Windows
1. Открой Проводник
2. Введи `\\192.168.1.100\Share`
3. Введи логин и пароль

#### Linux/Mac
```bash
#临时
smbclient //192.168.1.100/Share -U iva

# Постоянное монтирование
sudo mount -t cifs //192.168.1.100/Share /mnt/share -o username=iva
```

:::tip[Разбор команды]
- `smbclient` — клиент для подключения к Samba-шарам
- `mount -t cifs` — монтирование сетевой папки
:::

### Удаление мусора от macOS

Если к папке подключается Mac, он создаёт служебные файлы. Чтобы их скрыть:

```ini
[Share]
   veto files = /._*/.DS_Store/.Trashes/.Spotlight-V100/
   delete veto files = yes
```

### Проверка конфига

```bash
testparm
```

### Готово!

Теперь у тебя есть сетевая папка, доступная с любых компьютеров в сети.

---

*Все команды проверены на Ubuntu Server 24.04.*
