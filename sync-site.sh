#!/bin/bash
# sync-site.sh — Синхронизация контента из Obsidian vault в сайт
# Использование: ./sync-site.sh

set -e

OBSID="/home/iva/obsid/серверные"
SITE="/home/iva/greisv/src/content/docs"
SHPARGALKA="/home/iva/shpargalka.md"

echo "🔄 Синхронизация контента из Obsidian..."

# Guides
echo "📚 Копирование гайдов..."
cp "$OBSID/SSH.md" "$SITE/guides/ssh.md"
cp "$OBSID/терминал на tty1.md" "$SITE/guides/terminal.md"
cp "$OBSID/📋 Мониторинг здоровья HDD SSD (Ubuntu).md" "$SITE/guides/disk-health.md"
cp "$OBSID/📦 1. Диагностика дисков и файловых систем.md" "$SITE/guides/diagnostics.md"
cp "$OBSID/загрузочная флеха на лине.md" "$SITE/getting-started/bootable-usb.md"
cp "$OBSID/journalctl — журнал системы.md" "$SITE/guides/journalctl.md"

# Services
echo "🔧 Копирование сервисов..."
cp "$OBSID/Samba.md" "$SITE/services/samba.md"
cp "$OBSID/MiniDLNA — управление службой.md" "$SITE/services/minidlna.md"
cp "$OBSID/Настройка Transmission Daemon на Ubuntu 24.04.md" "$SITE/services/transmission.md"
cp "$OBSID/🖥️ Настройка HomeLab Xubuntu-Ubuntu Server.md" "$SITE/homelab/index.mdx"

# Homelab
echo "🏠 Копирование homelab..."
cp "$OBSID/🚀 Конспект Реанимация и настройка сервера Sony VAIO (Ubuntu 24.04).md" "$SITE/getting-started/first-steps.md"
cp "$OBSID/автоматическая настройка сервера через терминал.md" "$SITE/guides/auto-setup.md"
cp "$OBSID/автоматическое выключение сервера по таймеру.md" "$SITE/guides/auto-shutdown.md"

# Resources
echo "📖 Копирование ресурсов..."
cp "$OBSID/GIT команды.md" "$SITE/resources/git-commands.md"
cp "$OBSID/INXI.md" "$SITE/resources/inxi.md"

# shpargalka.md — базовый контекст сервера
echo "📋 Копирование справочника..."
cp "$SHPARGALKA" "$SITE/homelab/server-reference.md"

echo "✅ Синхронизация завершена!"
echo ""
echo "Следующие шаги:"
echo "1. Проверь изменения: git status"
echo "2. Добавь изменения: git add ."
echo "3. Закоммить: git commit -m 'obsid sync'"
echo "4. Отправь: git push"
