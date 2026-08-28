---
title: MQTT / ESPHome
description: Настройка MQTT для умного дома и ESPHome
---

## MQTT и ESPHome

**MQTT** — это лёгкий протокол для обмена сообщениями между устройствами. Используется в умном доме для связи датчиков и устройств.

### Mosquitto (MQTT-брокер)

#### Установка

```bash
sudo apt update && sudo apt install -y mosquitto mosquitto-clients
```

#### Настройка

```bash
sudo nano /etc/mosquitto/conf.d/mosquitto.conf
```

```
listener 1883 0.0.0.0
allow_anonymous false
password_file /etc/mosquitto/passwd
```

#### Создание пользователя

```bash
sudo mosquitto_passwd -c /etc/mosquitto/passwd username
```

#### Запуск

```bash
sudo systemctl restart mosquitto
sudo systemctl enable mosquitto
```

:::tip[Разбор команды]
- `mosquitto_passwd -c` — создать файл паролей с первым пользователем
- `-b` — добавить пользователя в существующий файл
:::

### Проверка

Подключение:

```bash
# Подписка на топик
mosquitto_sub -h 127.0.0.1 -u username -P password -t "test/topic"

# Отправка сообщения (в другом терминале)
mosquitto_pub -h 127.0.0.1 -u username -P password -t "test/topic" -m "Hello!"
```

### ESPHome

**ESPHome** — система для управления ESP-устройствами (датчиками, выключателями и т.д.).

#### Установка

```bash
# Создай виртуальное окружение
python3 -m venv /home/iva/esphome/venv
source /home/iva/esphome/venv/bin/activate

# Установи ESPHome
pip install esphome
```

#### Конфигурация устройства

Пример `device.yaml`:

```yaml
esphome:
  name: server-panel
  platform: ESP32
  board: heltec_wifi_lora_32_V3

wifi:
  ssid: "YourWiFi"
  password: "YourPassword"

mqtt:
  broker: 192.168.1.100
  username: "mqtt_user"
  password: "mqtt_password"

sensor:
  - platform: dht
    pin: GPIO4
    temperature:
      name: "Temperature"
    humidity:
      name: "Humidity"
```

#### Прошивка

```bash
# Компиляция
esphome compile device.yaml

# Заливка по USB
esphome upload --device /dev/ttyUSB0 device.yaml

# Заливка по WiFi (OTA)
esphome run device.yaml
```

### Полезные топики

```bash
# Мониторинг всех сообщений
mosquitto_sub -h 127.0.0.1 -t "#" -v

# Статус подключённых клиентов
mosquitto_sub -h 127.0.0.1 -t "$SYS/broker/clients/connected"
```

---

*MQTT — основа умного дома. Простой, надёжный, проверенный.*
