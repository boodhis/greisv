---
title: Первые шаги
description: Что делать после установки Ubuntu Server
---

## Первые шаги после установки

Поздравляю! У тебя теперь есть Linux-сервер. Вот что нужно сделать сразу.

### 1. Обновление системы

Первым делом обнови всё до последней версии:

```bash
sudo apt update && sudo apt upgrade -y
```

:::tip[Разбор команды]
Это команда для обновления всех пакетов в системе. `apt update` обновляет список доступных пакетов, а `apt upgrade` устанавливает обновления.
:::

### 2. Настройка имени хоста

Задай понятное имя для своего сервера:

```bash
sudo hostnamectl set-hostname homelab
```

:::tip[Разбор команды]
`hostnamectl` — утилита для управления именем хоста. `set-hostname` устанавливает новое имя.
:::

### 3. Настройка сети

#### Проверка IP-адреса
```bash
ip a
```

#### Статический IP (рекомендуется для сервера)
Отредактируй файл-netplan:

```bash
sudo nano /etc/netplan/00-installer-config.yaml
```

Пример конфигурации:

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

Примени изменения:

```bash
sudo netplan apply
```

:::tip[Разбор команды]
- `nano` — текстовый редактор для терминала
- `netplan apply` — применить сетевые настройки
- `dhcp4: false` — отключить автоматическое получение IP
:::

### 4. Установка SSH-сервера

Если при установке не выбрал OpenSSH:

```bash
sudo apt install -y openssh-server
```

Включи автозапуск:

```bash
sudo systemctl enable ssh
```

:::tip[Разбор команды]
- `systemctl enable` — добавить сервис в автозагрузку
- `ssh` — сервис для удалённого подключения
:::

### 5. Подключение с другой машины

Теперь можно подключаться удалённо:

```bash
ssh iva@192.168.1.100
```

### 6. Установка базовых инструментов

```bash
sudo apt install -y \
  curl wget git nano htop tmux \
  build-essential software-properties-common
```

:::tip[Разбор команды]
- `build-essential` — компиляторы и инструменты сборки
- `software-properties-common` — управление репозиториями
:::

### 7. Настройка файрвола

```bash
sudo ufw allow OpenSSH
sudo ufw enable
```

:::tip[Разбор команды]
- `ufw` — простой файрвол для Ubuntu
- `allow OpenSSH` — разрешить подключения по SSH
- `enable` — включить файрвол
:::

### 8. Проверка статуса

```bash
sudo systemctl status ssh
sudo ufw status
```

### Готово!

Теперь твой сервер:
- ✅ Обновлён
- ✅ Имеет статический IP
- ✅ Доступен по SSH
- ✅ Защищён файрволом

Следующий шаг — настройка [Сети](/homelab/network) или установка [Сервисов](/services/).

---

*Все команды проверены на Ubuntu Server 24.04. Если что-то не работает — проверь подключение к интернету.*
