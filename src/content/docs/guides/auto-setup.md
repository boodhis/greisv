---
title: Автоматическая настройка
description: Быстрая настройка Ubuntu Server
---

## Автоматическая настройка сервера

После установки Ubuntu Server нужно установить базовые программы. Вот скрипт для быстрой настройки.

### Единая команда

```bash
sudo apt update && sudo apt install -y \
  curl wget git nano htop tmux \
  samba minidlna nginx \
  smartmontools net-tools \
  build-essential software-properties-common
```

:::tip[Разбор команды]
Устанавливает:
- `curl wget` — загрузчики файлов
- `git` — контроль версий
- `nano` — текстовый редактор
- `htop` — диспетчер задач
- `tmux` — менеджер терминалов
- `samba` — сетевые папки
- `minidlna` — медиа-сервер
- `nginx` — веб-сервер
- `smartmontools` — мониторинг дисков
- `net-tools` — сетевые утилиты
:::

### Включение сервисов

```bash
sudo systemctl enable --now smbd minidlna nginx
```

:::tip[Разбор команды]
- `enable` — добавить в автозагрузку
- `--now` — запустить сразу
:::

### Настройка базовых вещей

#### Имя хоста

```bash
sudo hostnamectl set-hostname homelab
```

#### Статический IP

```bash
sudo nano /etc/netplan/00-installer-config.yaml
```

Пример:

```yaml
network:
  version: 2
  ethernets:
    enp0s3:
      dhcp4: false
      addresses:
        - 192.168.1.100/24
      routes:
        - to: default
          via: 192.168.1.1
      nameservers:
        addresses:
          - 8.8.8.8
          - 8.8.4.4
```

Примени:

```bash
sudo netplan apply
```

#### Firewall

```bash
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### Проверка

```bash
# Проверка сервисов
systemctl is-active smbd minidlna nginx

# Проверка портов
sudo ss -tulpn

# Проверка сети
ping -c 4 google.com
```

### Готово!

Теперь у тебя есть:
- ✅ Базовые программы
- ✅ Работающие сервисы
- ✅ Настроенная сеть
- ✅ Включённый файрвол

---

*Эта базовая настройка занимает 5 минут и экономит часы в будущем.*
