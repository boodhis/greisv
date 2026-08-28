---
title: INXI
description: Утилита для получения информации о системе
---

## INXI: Информация о системе

**inxi** — мощная утилита для получения подробной информации о системе, железе и софте.

### Установка

```bash
sudo apt install -y inxi
```

### Базовые команды

```bash
# Полная информация о системе
inxi -Fz

# Только процессор
inxi -C

# Только память
inxi -I

# Только диски
inxi -D

# Только сеть
inxi -N
```

:::tip[Разбор команды]
- `-F` — полная информация
- `-z` — скрыть конфиденциальные данные (MAC-адреса и т.д.)
- `-C` — информация о CPU
- `-I` — информация о памяти
- `-D` — информация о дисках
- `-N` — информация о сети
:::

### Полезные опции

```bash
# С GPIO (для ESP и Arduino)
inxi -G

# С температурами
inxi -s

# С батареей
inxi -B

# С RAID
inxi -R

# Компактный вид
inxi -Fz --memory --short
```

### Пример вывода

```bash
$ inxi -Fz
System:
  Host: homelab Kernel: 6.8.0-138-generic arch: x86_64 bits: 64
  Desktop: N/A Distro: Ubuntu 24.04.4 LTS
Machine:
  Type: Laptop System: Acer product: Extensa 2520G
  CPU: Dual Core Intel Core i5-6200U
  Memory: 8 GiB
Drives:
  Local Storage: total: 4.11 TiB
Network:
  Device-1: Qualcomm Atheros WiFi driver: ath9k
  IF: wlp3s0 state: up
```

### Использование в скриптах

```bash
# Сохранить информацию о системе
inxi -Fz > system-info.txt

# Проверить температуру CPU
inxi -s | grep -i cpu

# Проверить диски
inxi -D | grep -i "size"
```

### Готово!

Теперь ты можешь:
- ✅ Быстро узнать характеристики системы
- ✅ Проверить железо и драйверы
- ✅ Использовать в скриптах для автоматизации

---

*inxi — незаменимый инструмент для диагностики и документирования системы.*
