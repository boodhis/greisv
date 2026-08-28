---
title: Wi-Fi фикс
description: Решение проблем с Wi-Fi в Linux
---

## Wi-Fi в Linux

Проблемы с Wi-Fi — одна из самых частых проблем при установке Linux. Вот как их решить.

### Проверка интерфейса

```bash
# Есть ли Wi-Fi адаптер?
ip link show

# Включён ли Wi-Fi?
rfkill list
```

:::tip[Разбор команды]
- `ip link show` — показать все сетевые интерфейсы
- `rfkill list` — показать состояние блокировок (Wi-Fi, Bluetooth)
:::

### Включение Wi-Fi

```bash
# Разблокировать Wi-Fi
rfkill unblock wifi

# Включить интерфейс
sudo ip link set wlp3s0 up
```

:::tip[Разбор команды]
- `rfkill unblock wifi` — разблокировать Wi-Fi
- `ip link set up` — включить сетевой интерфейс
:::

### Подключение к сети

```bash
# Просмотр доступных сетей
iwlist wlp3s0 scan | grep ESSID

# Подключение через wpa_supplicant
wpa_supplicant -B -i wlp3s0 -c <(wpa_passphrase "SSID" "password")

# Получение IP
dhclient wlp3s0
```

:::tip[Разбор команды]
- `iwlist scan` — сканирование доступных сетей
- `wpa_supplicant` — клиент для WPA/WPA2
- `dhclient` — получение IP по DHCP
:::

### Автоматическое подключение

Для постоянного подключения используй `netplan` или `NetworkManager`.

#### Netplan (рекомендуется для серверов)

```yaml
network:
  version: 2
  wifis:
    wlp3s0:
      dhcp4: true
      access-points:
        "SSID":
          password: "password"
```

Примени:

```bash
sudo netplan apply
```

#### NetworkManager (для десктопов)

```bash
nmcli device wifi connect "SSID" password "password"
```

### Исправление проблем

#### Проблема: "Wi-Fi включён, но не подключается"

```bash
# Перезапустите NetworkManager
sudo systemctl restart NetworkManager

# Или перезагрузите Wi-Fi
sudo ip link set wlp3s0 down
sudo ip link set wlp3s0 up
```

#### Проблема: "Нет драйвера"

```bash
# Проверьте наличие драйвера
lspci | grep -i wireless

# Установите драйвер (для некоторых адаптеров)
sudo apt install firmware-iwlwifi
```

#### Проблема: "Wi-Fi отключается после сна"

```bash
# Отключите энергосбережение
sudo iwconfig wlp3s0 power off

# Или добавьте в автозагрузку
echo "sudo iwconfig wlp3s0 power off" | sudo tee /etc/rc.local
```

### Полезные команды

```bash
# Статус Wi-Fi
iwconfig wlp3s0

# Информация о подключении
iw dev wlp3s0 link

# Сила сигнала
iw dev wlp3s0 station dump
```

### Готово!

Теперь ты можешь:
- ✅ Включить Wi-Fi
- ✅ Подключиться к сети
- ✅ Настроить автоподключение
- ✅ Решить типичные проблемы

---

*Wi-Fi в Linux работает, но иногда требует внимания. Терпение — ключ к успеху.*
