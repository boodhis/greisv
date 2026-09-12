#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генератор раздела «Электрика»: electric/*.html из общего шаблона навигации.
Запуск из корня проекта:  python3 gen/gen_electric.py
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTDIR = os.path.join(ROOT, "electric")

NAV = """<div class="brand">🛡️ Цифровая Крепость</div>
<a class="nmain" href="../index.html">Главная</a><a class="nmain" href="../manifest.html">Манифест</a>

<div class="ngroup"><div class="ngt">Обучение</div>
<a class="nli" href="../study/index.html">Обучение</a>
<a class="nli" href="../study/words.html">Тренажёр карточек</a>
<a class="nli" href="../study/cheatsheets.html">Шпаргалки</a></div>

<div class="ngroup"><div class="ngt">Электрика</div>
<a class="nli" href="../electric/index.html">Раздел</a>
<a class="nli" href="../electric/safety.html">Безопасность</a>
<a class="nli" href="../electric/panels.html">Щиты и автоматы</a>
<a class="nli" href="../electric/wiring.html">Кабели и монтаж</a>
<a class="nli" href="../electric/smart.html">Умный дом</a></div>

<div class="ngroup"><div class="ngt">С чего начать</div>
<a class="nli" href="../getting-started/index.html">Обзор</a>
<a class="nli" href="../getting-started/install-ubuntu.html">Установка Ubuntu</a>
<a class="nli" href="../getting-started/first-steps.html">Первые шаги</a>
<a class="nli" href="../getting-started/bootable-usb.html">Загрузочная флешка</a></div>

<div class="ngroup"><div class="ngt">Homelab</div>
<a class="nli" href="../homelab/index.html">Концепция</a>
<a class="nli" href="../homelab/hardware.html">Железо</a>
<a class="nli" href="../homelab/network.html">Сеть</a>
<a class="nli" href="../homelab/server-reference.html">Справочник сервера</a></div>

<div class="ngroup"><div class="ngt">Сервисы</div>
<a class="nli" href="../services/index.html">Обзор</a>
<a class="nli" href="../services/docker.html">Docker</a>
<a class="nli" href="../services/samba.html">Samba</a>
<a class="nli" href="../services/minidlna.html">MiniDLNA</a>
<a class="nli" href="../services/transmission.html">Transmission</a>
<a class="nli" href="../services/navidrome.html">Navidrome</a>
<a class="nli" href="../services/immich.html">Immich</a>
<a class="nli" href="../services/sopds.html">SOPDS</a>
<a class="nli" href="../services/mqtt.html">MQTT / ESPHome</a></div>

<div class="ngroup"><div class="ngt">Гайды</div>
<a class="nli" href="../guides/index.html">Обзор</a>
<a class="nli" href="../guides/disk-health.html">Диски и SMART</a>
<a class="nli" href="../guides/diagnostics.html">Диагностика</a>
<a class="nli" href="../guides/backup.html">Бекапы</a>
<a class="nli" href="../guides/ssh.html">SSH</a>
<a class="nli" href="../guides/terminal.html">Терминал</a>
<a class="nli" href="../guides/wifi-fix.html">Wi-Fi фикс</a>
<a class="nli" href="../guides/auto-setup.html">Автосборка</a>
<a class="nli" href="../guides/journalctl.html">journalctl</a>
<a class="nli" href="../guides/auto-shutdown.html">Авто-выключение</a></div>

<div class="ngroup"><div class="ngt">Ресурсы</div>
<a class="nli" href="../resources/links.html">Ссылки</a>
<a class="nli" href="../resources/git-commands.html">Git команды</a>
<a class="nli" href="../resources/inxi.html">INXI</a>
<a class="nli" href="../resources/opencode-windows.html">OpenCode на Windows</a></div>

<div class="ngroup"><div class="ngt">Хобби</div>
<a class="nli" href="../hobbies/index.html">Досуг</a>
<a class="nli" href="../hobbies/guitar.html">Гитара</a>
<a class="nli" href="../hobbies/esp32.html">ESP32 / ESPHome</a></div>"""

# заголовок(с on), описание, body-html
PAGES = {
    "index.html": (
        "Электрика", "Раздел", "⚡ Электрика",
        "Ликбез для электриков, монтажников и владельцев домов: от правил безопасности до умного дома. Без воды, с реальными номиналами.",
        """
<div class="grid">
<div class="card"><a href="safety.html"><b>🛡 Безопасность</b><p>Обесточивание, СИЗ, первая помощь. Сначала это.</p></a></div>
<div class="card"><a href="panels.html"><b>📊 Щиты и автоматы</b><p>Автоматы, УЗО, дифавтоматы, номиналы и схема щита.</p></a></div>
<div class="card"><a href="wiring.html"><b>🔌 Кабели и монтаж</b><p>Цвета жил, сечения, розетки, порядок монтажа.</p></a></div>
<div class="card"><a href="smart.html"><b>🏡 Умный дом</b><p>Реле, датчики, ESPHome/MQTT, связка с homelab.</p></a></div>
</div>
<h2>Не путай!</h2>
<ul>
<li><strong>Ток (А) — сила</strong>, греет провода. Сечение кабеля подбирается по току.</li>
<li><strong>Напряжение (В) — разность потенциалов</strong>. В доме 220 В.</li>
<li><strong>Автомат защищает проводку</strong>, а УЗО — человека.</li>
</ul>
<div class="callout callout-warning"><div class="callout-t">Важно</div><div class="callout-body"><p>Работы под напряжением — только с квалификацией и <a href="safety.html">по правилам безопасности</a>.</p></div></div>
"""
    ),
    "safety.html": (
        "Электрика", "Безопасность", "🛡 Безопасность",
        "Правила, которые сохраняют жизнь. Прежде чем что-то трогать — прочитай.",
        """
<h2>Обесточивание</h2>
<ul>
<li>Выключи <strong>вводной автомат</strong> (главный рубильник) — не только нужную линию.</li>
<li>Проверь отсутствие напряжения <strong>индикатором на обеих клеммах</strong>.</li>
<li>Работай одной рукой, вторая — в кармане (меньше шанс удара через тело).</li>
<li>Повесь табличку «НЕ ВКЛЮЧАТЬ — работают» или запри рубильник.</li>
</ul>
<h2>СИЗ</h2>
<table><thead><tr><th>Что</th><th>Зачем</th></tr></thead><tbody>
<tr><td>Изолирующие перчатки</td><td>защита от удара при работе с проводкой</td></tr>
<tr><td>Изолированный инструмент</td><td>рукоятки с классом изоляции</td></tr>
<tr><td>Очки</td><td>от искр и опилок при штроблении</td></tr>
<tr><td>Коврик/боты с изоляцией</td><td>на сыром/бетонном полу</td></tr>
</tbody></table>
<h2>Первая помощь при ударе током</h2>
<ol>
<li>Обесточь линию (рубильник) или оттолкни провод сухой палкой <strong>не голыми руками</strong>.</li>
<li>Вызови скорую (103).</li>
<li>Если пострадавший не дышит — <strong>сердечно-лёгочная реанимация</strong>: 30 нажатий + 2 вдоха, 100–120/мин.</li>
<li>До приезда не прекращать.</li>
</ol>
<div class="callout callout-warning"><div class="callout-t">Золотое правило</div><div class="callout-body"><p>220 В убивает не «силой тока», а прохождением тока через сердце. Одна рука в кармане — не шутка.</p></div></div>
"""
    ),
    "panels.html": (
        "Электрика", "Щиты и автоматы", "📊 Щиты и автоматы",
        "Как устроен щит: автоматические выключатели, УЗО, дифавтоматы. Номиналы по сечению.",
        """
<h2>Что стоит в щите</h2>
<table><thead><tr><th>Устройство</th><th>От чего защищает</th></tr></thead><tbody>
<tr><td>Автоматический выключатель</td><td>перегрузка и короткое замыкание (линию)</td></tr>
<tr><td>УЗО</td><td>утечку тока (человека)</td></tr>
<tr><td>Дифавтомат</td><td>автомат + УЗО в одном корпусе</td></tr>
<tr><td>Реле напряжения</td><td>скачки/пропадание фазы</td></tr>
<tr><td>ГРОЗО/разрядник</td><td>грозовые перенапряжения</td></tr>
</tbody></table>
<h2>Номиналы: сечение → автомат</h2>
<table><thead><tr><th>Сечение меди</th><th>Ток жилы</th><th>Автомат</th><th>Типично</th></tr></thead><tbody>
<tr><td>1.5 мм²</td><td>16 А</td><td>10 А</td><td>освещение</td></tr>
<tr><td>2.5 мм²</td><td>25 А</td><td>16 А</td><td>розетки</td></tr>
<tr><td>4 мм²</td><td>32 А</td><td>25 А</td><td>плита/кондиционер</td></tr>
<tr><td>6 мм²</td><td>40 А</td><td>32 А</td><td>ввод в квартиру</td></tr>
</tbody></table>
<p>Правило: автомат <strong>меньше</strong> длительного тока кабеля — кабель не должен пострадать раньше автомата.</p>
<h2>Схема простого щита</h2>
<pre class="ascii">ввод 220В
  │
  ├─ АВ вводной 32А ── реле напряжения ──┐
  │                                      │
  ├─ УЗО 40А/30мА ── АВ 16А ── розетки  │
  │                └── АВ 10А ── свет    │
  └─ УЗО 40А/30мА ── АВ 25А ── плита    │
</pre>
<div class="callout"><div class="callout-t">Главное</div><div class="callout-body"><p>УЗО и автомат — не одно и то же. УЗО без автомата не защитит от короткого замыкания, а автомат без УЗО — от утечки на человека.</p></div></div>
"""
    ),
    "wiring.html": (
        "Электрика", "Кабели и монтаж", "🔌 Кабели и монтаж",
        "Цвета жил, маркировка, сечения, розетки и порядок работ от штробы до подключения.",
        """
<h2>Цвета жил (важно!)</h2>
<table><thead><tr><th>Цвет</th><th>Роль</th></tr></thead><tbody>
<tr><td>Коричневый / чёрный</td><td>фаза (L)</td></tr>
<tr><td>Синий</td><td>ноль (N)</td></tr>
<tr><td>Жёлто-зелёный</td><td>заземление (PE)</td></tr>
</tbody></table>
<p>Перепутал? Ошибка грозит поражением током. Перед работой сомневаешься — <strong>проверь индикатором</strong>.</p>
<h2>Сечение по нагрузке (медь)</h2>
<table><thead><tr><th>Нагрузка</th><th>Сечение</th></tr></thead><tbody>
<tr><td>Освещение LED</td><td>1.5 мм²</td></tr>
<tr><td>Розетки</td><td>2.5 мм²</td></tr>
<tr><td>Плита, бойлер, духовка</td><td>4–6 мм²</td></tr>
<tr><td>Ввод в квартиру</td><td>6–10 мм²</td></tr>
</tbody></table>
<h2>Порядок монтажа</h2>
<ol>
<li>Проект: где какая линия, посчитай нагрузку.</li>
<li>Штробы, кабель-каналы, гофра.</li>
<li>Укладка кабеля <strong>цельным куском</strong> без сращиваний внутри стены.</li>
<li>Монтаж подрозетников, вывод жил с запасом 10–15 см.</li>
<li>Подключение в щит → проверка индикатором → УЗО/автоматы.</li>
</ol>
<h2>Частые ошибки</h2>
<ul>
<li>Скрутки вместо клеммников (Wago и т.п.) под нагрузкой.</li>
<li>Сращивание внутри стены — только в распредкоробке с крышкой.</li>
<li>Алюминий + медь напрямую — гальваническая пара, греется.</li>
<li>Один автомат на всё — теряется селективность.</li>
</ul>
"""
    ),
    "smart.html": (
        "Электрика", "Умный дом", "🏡 Умный дом",
        "Реле, датчики, ESPHome/MQTT: как собрать умный дом своими руками и связать с homelab.",
        """
<h2>С чего начать</h2>
<ul>
<li><strong>Реле / умный выключатель</strong> — управление светом из телефона и по сценариям.</li>
<li><strong>Датчики</strong>: температуры/влажности, движения, дверного контакта, дыма.</li>
<li><strong>Обязательно</strong>: старый электрический выключатель заменяем только с правилами из раздела <a href="safety.html">Безопасность</a>.</li>
</ul>
<h2>Стек: MQTT + ESPHome</h2>
<p>ESP32/MSP-устройства работают по <strong>MQTT</strong> — лёгкому шину-протоколу «издатель/подписчик». Брокер (в хомлабе — контейнер <code>mqtt</code>) раздаёт события: «датчик → реле → сценарий».</p>
<pre class="ascii"> датчик (ESP32) ──MQTT──▶ брокер ──MQTT──▶ реле (ESP32)
                    │           └──▶ homelab (сценарии/история)
                    └──▶ телефон (виджет вкл/выкл)
</pre>
<h2>Пример: автоматический свет коридора</h2>
<pre><code># ESPHome-конфиг датчика движения + реле
sensor:
  - platform: mqtt_subscribe
    topic: corridor/motion
binary_sensor:
  - platform: mqtt_subscribe
    topic: corridor/motion
switch:
  - platform: mqtt
    name: "Corridor Light"
    topic: corridor/light/set</code></pre>
<h2>Связано с хомлабом</h2>
<ul>
<li>Брокер MQTT и ESPHome — раздел <a href="../services/mqtt.html">МQTT / ESPHome</a>.</li>
<li>Плата Heltec V3 — страница <a href="../hobbies/esp32.html">ESP32</a>.</li>
<li>Вся автоматика и скрипты живут на сервере <a href="../homelab/index.html">homelab</a>.</li>
</ul>
"""
    ),
}


def write_page(fname, active, label, title, desc, body):
    on = ' on' if active == label else ''
    html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Цифровая Крепость</title>
<meta name="description" content="{desc}">
<link rel="icon" type="image/svg+xml" href="../favicon.svg">
<link rel="stylesheet" href="../style.css">
</head>
<body>
<canvas id="bgwall" aria-hidden="true"></canvas>
<div class="layout">
<aside>
{NAV.replace(f'<a class="nli" href="../electric/{label}.html">', f'<a class="nli on" href="../electric/{label}.html">', 1)}
</aside>
<main>
<h1>{title}</h1>
<p class="desc">{desc}</p>
{body}
<footer>Цифровая Крепость — образовательный сайт. · <a href="https://github.com/boodhis/greisv">Исходный код</a></footer>
</main>
</div>
<div id="wordday" style="display:none"></div>
<script src="../study/data/wordday.js"></script>
<script src="../study/data/widget.js"></script>
<button id="wall-btn" class="btn ghost" title="Оставить надпись на стене-подложке">✏️ Стена</button>
<div id="wall-bar" hidden>
<button class="wc on" data-c="#4fc3f7" style="background:#4fc3f7" title="Голубой"></button>
<button class="wc" data-c="#3fb950" style="background:#3fb950" title="Зелёный"></button>
<button class="wc" data-c="#e3b341" style="background:#e3b341" title="Жёлтый"></button>
<button class="wc" data-c="#ff7ab6" style="background:#ff7ab6" title="Розовый"></button>
<button class="wc" data-c="#e6edf3" style="background:#e6edf3" title="Белый"></button>
<button id="wall-undo" class="wclear" type="button">↩ убрать надпись</button>
</div>
<div id="wall-hint" hidden>Рисуй прямо на подложке. Готово — кнопка справа внизу, выход — Esc</div>
<script src="../js/wall.js"></script>
<script>if("serviceWorker" in navigator){{navigator.serviceWorker.register("../sw.js");}}</script>
</body>
</html>
"""
    path = os.path.join(OUTDIR, fname)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("->", os.path.relpath(path, ROOT))


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    for fname, (group, active, title, desc, body) in PAGES.items():
        write_page(fname, active, active, title, desc, body)


if __name__ == "__main__":
    main()