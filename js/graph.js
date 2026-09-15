/* Граф-навигация «Цифровой Крепости» — как Obsidian Graph View.
   Собственноручный force-layout на canvas: зум колесом, перетаскивание
   пустого места и узлов, клик по узлу — переход в раздел. */
(function () {
  var cv = document.getElementById('graph');
  if (!cv) return;
  var ctx = cv.getContext('2d');
  var dpr = Math.min(window.devicePixelRatio || 1, 2);
  var W = 0, H = 0;

  var COL = {
    home: '#35e6e0', start: '#3ef06a', study: '#ffe14d', elec: '#ff55f0',
    homelab: '#35e6e0', srv: '#3ef06a', guide: '#ffe14d', res: '#ff55f0', hobby: '#d9f7d0'
  };

  var nodes = [], links = [], byId = {};

  function node(id, label, href, g) {
    var o = { id: id, label: label, href: href, c: COL[g], x: 0, y: 0, vx: 0, vy: 0, r: 6, deg: 0 };
    nodes.push(o);
    byId[id] = o;
  }
  function link(a, b) { links.push([byId[a], byId[b]]); }

  /* ---- карта сайта ---- */
  node('home', 'Главная', 'index.html', 'home');
  node('manifest', 'Манифест', 'manifest.html', 'home');
  node('start', 'С чего начать', 'getting-started/index.html', 'start');
  node('start-ubuntu', 'Установка Ubuntu', 'getting-started/install-ubuntu.html', 'start');
  node('start-first', 'Первые шаги', 'getting-started/first-steps.html', 'start');
  node('start-flash', 'Загрузочная флешка', 'getting-started/bootable-usb.html', 'start');
  node('study', 'Обучение', 'study/index.html', 'study');
  node('study-words', 'Тренажёр', 'study/words.html', 'study');
  node('study-cheat', 'Шпаргалки', 'study/cheatsheets.html', 'study');
  node('elec', 'Электрика', 'electric/index.html', 'elec');
  node('elec-safe', 'Безопасность', 'electric/safety.html', 'elec');
  node('elec-panels', 'Щиты', 'electric/panels.html', 'elec');
  node('elec-wire', 'Кабели', 'electric/wiring.html', 'elec');
  node('elec-smart', 'Умный дом', 'electric/smart.html', 'elec');
  node('lab', 'Homelab', 'homelab/index.html', 'homelab');
  node('lab-hw', 'Железо', 'homelab/hardware.html', 'homelab');
  node('lab-net', 'Сеть', 'homelab/network.html', 'homelab');
  node('lab-ref', 'Сервер', 'homelab/server-reference.html', 'homelab');
  node('lab-lib', 'Библиотека', 'homelab/sopds-web.html', 'homelab');
  node('srv', 'Сервисы', 'services/index.html', 'srv');
  node('srv-docker', 'Docker', 'services/docker.html', 'srv');
  node('srv-samba', 'Samba', 'services/samba.html', 'srv');
  node('srv-dlna', 'MiniDLNA', 'services/minidlna.html', 'srv');
  node('srv-tr', 'Transmission', 'services/transmission.html', 'srv');
  node('srv-nav', 'Navidrome', 'services/navidrome.html', 'srv');
  node('srv-imm', 'Immich', 'services/immich.html', 'srv');
  node('srv-sopds', 'SOPDS', 'services/sopds.html', 'srv');
  node('srv-mqtt', 'MQTT', 'services/mqtt.html', 'srv');
  node('guide', 'Гайды', 'guides/index.html', 'guide');
  node('guide-disk', 'Диски', 'guides/disk-health.html', 'guide');
  node('guide-diag', 'Диагностика', 'guides/diagnostics.html', 'guide');
  node('guide-back', 'Бекапы', 'guides/backup.html', 'guide');
  node('guide-ssh', 'SSH', 'guides/ssh.html', 'guide');
  node('guide-term', 'Терминал', 'guides/terminal.html', 'guide');
  node('guide-wifi', 'Wi-Fi', 'guides/wifi-fix.html', 'guide');
  node('guide-auto', 'Автосборка', 'guides/auto-setup.html', 'guide');
  node('guide-jctl', 'journalctl', 'guides/journalctl.html', 'guide');
  node('guide-off', 'Авто-выкл', 'guides/auto-shutdown.html', 'guide');
  node('res', 'Ресурсы', 'resources/index.html', 'res');
  node('res-links', 'Ссылки', 'resources/links.html', 'res');
  node('res-git', 'Git', 'resources/git-commands.html', 'res');
  node('res-inxi', 'INXI', 'resources/inxi.html', 'res');
  node('res-oc', 'OpenCode', 'resources/opencode-windows.html', 'res');
  node('hobby', 'Досуг', 'hobbies/index.html', 'hobby');
  node('hobby-guitar', 'Гитара', 'hobbies/guitar.html', 'hobby');
  node('hobby-esp', 'ESP32', 'hobbies/esp32.html', 'hobby');

  ['manifest', 'start', 'study', 'elec', 'lab', 'srv', 'guide', 'res', 'hobby']
    .forEach(function (g) { link('home', g); });
  [
    ['start', 'start-ubuntu'], ['start', 'start-first'], ['start', 'start-flash'],
    ['study', 'study-words'], ['study', 'study-cheat'],
    ['elec', 'elec-safe'], ['elec', 'elec-panels'], ['elec', 'elec-wire'], ['elec', 'elec-smart'],
    ['lab', 'lab-hw'], ['lab', 'lab-net'], ['lab', 'lab-ref'], ['lab', 'lab-lib'],
    ['srv', 'srv-docker'], ['srv', 'srv-samba'], ['srv', 'srv-dlna'], ['srv', 'srv-tr'],
    ['srv', 'srv-nav'], ['srv', 'srv-imm'], ['srv', 'srv-sopds'], ['srv', 'srv-mqtt'],
    ['guide', 'guide-disk'], ['guide', 'guide-diag'], ['guide', 'guide-back'], ['guide', 'guide-ssh'],
    ['guide', 'guide-term'], ['guide', 'guide-wifi'], ['guide', 'guide-auto'],
    ['guide', 'guide-jctl'], ['guide', 'guide-off'],
    ['res', 'res-links'], ['res', 'res-git'], ['res', 'res-inxi'], ['res', 'res-oc'],
    ['hobby', 'hobby-guitar'], ['hobby', 'hobby-esp']
  ].forEach(function (e) { link(e[0], e[1]); });
  /* перекрёстные связи */
  link('study', 'guide-term');
  link('start', 'guide-term');
  link('lab-net', 'guide-wifi');
  link('lab-ref', 'srv-docker');
  link('srv-docker', 'guide-auto');
  link('srv-sopds', 'lab-lib');
  link('hobby-esp', 'srv-mqtt');
  link('elec-smart', 'srv-mqtt');
  link('guide-ssh', 'start-first');
  link('res-git', 'guide-term');
  link('srv-nav', 'hobby-guitar');

  var deg = {};
  nodes.forEach(function (n) { deg[n.id] = 0; });
  links.forEach(function (e) { deg[e[0].id]++; deg[e[1].id]++; });
  nodes.forEach(function (n) { n.deg = deg[n.id]; });

  /* ---- физика ---- */
  var damp = 0.82;
  var LIMX = 440, LIMY = 320;      /* границы мира = половина окна */
  var REP = 190000, CAP = 26;      /* сила отталкивания */
  var LINKLEN = 150;               /* длина пружины связи */

  /* Пружины/отталкивание подгоняем под размер окна, чтобы граф заполнял его
     без масштабирования (zoom по умолчанию 1, мировые координаты ≈ экранные). */
  function computeScale() {
    LIMX = Math.max(120, W * 0.46);
    LIMY = Math.max(120, H * 0.44);
    var cell = Math.sqrt((LIMX * 2 * LIMY * 2) / Math.max(1, nodes.length));
    LINKLEN = cell * 1.05;
    var k = LINKLEN / 150;
    REP = 190000 * k;
    CAP = 26 * k;
  }

  function step(kick) {
    var i, a, b, dx, dy, d2, d, f;
    for (i = 0; i < nodes.length; i++) {
      for (var j = i + 1; j < nodes.length; j++) {
        a = nodes[i]; b = nodes[j];
        dx = a.x - b.x; dy = a.y - b.y;
        d2 = dx * dx + dy * dy + 1;
        f = REP / d2;
        if (f > CAP) f = CAP;
        dx /= Math.sqrt(d2); dy /= Math.sqrt(d2);
        a.vx += f * dx; a.vy += f * dy;
        b.vx -= f * dx; b.vy -= f * dy;
      }
    }
    for (i = 0; i < links.length; i++) {
      a = links[i][0]; b = links[i][1];
      dx = b.x - a.x; dy = b.y - a.y;
      d = Math.sqrt(dx * dx + dy * dy) || 1;
      f = (d - LINKLEN) * 0.02;
      dx /= d; dy /= d;
      a.vx += f * dx; a.vy += f * dy;
      b.vx -= f * dx; b.vy -= f * dy;
    }
    for (i = 0; i < nodes.length; i++) {
      a = nodes[i];
      a.vx += -a.x * 0.0015;
      a.vy += -a.y * 0.0015;
      if (kick) {
        a.vx += (Math.random() - 0.5) * 0.06;
        a.vy += (Math.random() - 0.5) * 0.06;
      }
      a.vx *= damp; a.vy *= damp;
      a.x += a.vx; a.y += a.vy;
      if (a.x > LIMX) { a.x = LIMX; a.vx *= -0.3; }
      if (a.x < -LIMX) { a.x = -LIMX; a.vx *= -0.3; }
      if (a.y > LIMY) { a.y = LIMY; a.vy *= -0.3; }
      if (a.y < -LIMY) { a.y = -LIMY; a.vy *= -0.3; }
    }
  }

  /* ---- вид ---- */
  var zoom = 1, offX = 0, offY = 0, hover = null;

  /* Без авто-масштабирования: мир уже размером с окно, центрируем 1:1.
     Колесо/перетаскивание остаются для ручного зума и панорамы. */
  function fit() {
    zoom = 1;
    offX = W / 2;
    offY = H / 2;
  }
  function toScreen(o) { return { x: o.x * zoom + offX, y: o.y * zoom + offY }; }
  function toWorld(sx, sy) { return { x: (sx - offX) / zoom, y: (sy - offY) / zoom }; }

  function nodeAt(sx, sy) {
    for (var i = 0; i < nodes.length; i++) {
      var o = nodes[i], s = toScreen(o);
      var thr = Math.max(9, o.r * zoom + 5 + o.deg * 0.4);
      if (Math.hypot(sx - s.x, sy - s.y) <= thr) return o;
    }
    return null;
  }

  function draw() {
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, W, H);
    ctx.save();
    ctx.translate(offX, offY);
    ctx.scale(zoom, zoom);

    ctx.lineWidth = 1.4 / zoom;
    for (var i = 0; i < links.length; i++) {
      var a = links[i][0], b = links[i][1];
      var inc = hover && (a === hover || b === hover);
      ctx.strokeStyle = inc
        ? 'rgba(53,230,224,0.6)'
        : 'rgba(123,168,124,' + (hover ? 0.05 : 0.11) + ')';
      ctx.beginPath();
      ctx.moveTo(a.x, a.y);
      ctx.lineTo(b.x, b.y);
      ctx.stroke();
    }

    ctx.textAlign = 'left';
    ctx.textBaseline = 'middle';
    for (var n = 0; n < nodes.length; n++) {
      var o = nodes[n];
      var rs = o.r * (o.deg >= 8 ? 1.55 : o.deg >= 4 ? 1.25 : 1);
      var dim = hover && o !== hover;
      ctx.globalAlpha = dim ? 0.3 : 1;
      ctx.fillStyle = o.c;
      if (o === hover) {
        ctx.shadowColor = o.c;
        ctx.shadowBlur = 14;
        ctx.fillStyle = '#ffffff';
      }
      ctx.beginPath();
      ctx.arc(o.x, o.y, rs, 0, Math.PI * 2);
      ctx.fill();
      ctx.shadowBlur = 0;
      ctx.globalAlpha = 1;

      var fs = Math.max(8, 11.5 / zoom);
      ctx.font = '600 ' + fs + 'px ui-monospace,Consolas,monospace';
      ctx.fillStyle = o === hover ? '#fff' : 'rgba(123,168,124,.9)';
      ctx.fillText(o.label, o.x + rs + 7 / zoom, o.y);
    }
    ctx.restore();
  }

  /* ---- цикл ---- */
  var raf = null, settling = 420;
  function frame(ts) {
    step(settling > 0);
    draw();
    if (settling > 0) settling--;
    raf = requestAnimationFrame(frame);
    void ts;
  }

  function resize() {
    W = window.innerWidth;
    H = window.innerHeight;
    cv.width = Math.round(W * dpr);
    cv.height = Math.round(H * dpr);
    cv.style.width = W + 'px';
    cv.style.height = H + 'px';
    computeScale();
    fit();
  }

  W = window.innerWidth; H = window.innerHeight;
  computeScale();
  for (var i = 0; i < nodes.length; i++) {
    nodes[i].x = (Math.random() - 0.5) * 2 * LIMX * 0.9;
    nodes[i].y = (Math.random() - 0.5) * 2 * LIMY * 0.9;
  }

  window.addEventListener('resize', function () { resize(); });
  resize();
  raf = requestAnimationFrame(frame);

  /* ---- ввод ---- */
  var drag = null, moved = 0, sx0 = 0, sy0 = 0;

  cv.addEventListener('mousedown', startDrag);
  window.addEventListener('mousemove', moveDrag);
  window.addEventListener('mouseup', endDrag);
  cv.addEventListener('touchstart', function (e) {
    e.preventDefault();
    startDrag({ clientX: e.touches[0].clientX, clientY: e.touches[0].clientY, isTouch: true });
  }, { passive: false });
  window.addEventListener('touchmove', function (e) {
    if (drag) { e.preventDefault(); moveDrag({ clientX: e.touches[0].clientX, clientY: e.touches[0].clientY }); }
  }, { passive: false });
  window.addEventListener('touchend', function () { endDrag(); });

  cv.addEventListener('mousemove', function (e) {
    if (!drag) hover = nodeAt(e.clientX, e.clientY);
  });
  cv.addEventListener('mouseleave', function () { if (!drag) hover = null; });

  function startDrag(e) {
    var n = nodeAt(e.clientX, e.clientY);
    var p = toWorld(e.clientX, e.clientY);
    drag = { node: n, touch: !!e.isTouch };
    if (n) { n.vx = 0; n.vy = 0; }
    drag.px = p.x; drag.py = p.y;
    drag.sx = e.clientX; drag.sy = e.clientY;
    moved = 0;
    cv.classList.add('gd');
  }

  function moveDrag(e) {
    if (!drag) return;
    moved += Math.hypot(e.clientX - drag.sx, e.clientY - drag.sy);
    var p = toWorld(e.clientX, e.clientY);
    if (drag.node) {
      drag.node.x += p.x - drag.px;
      drag.node.y += p.y - drag.py;
      drag.node.vx = 0; drag.node.vy = 0;
    } else {
      offX += e.clientX - drag.sx;
      offY += e.clientY - drag.sy;
    }
    drag.sx = e.clientX; drag.sy = e.clientY;
    drag.px = p.x; drag.py = p.y;
  }

  function endDrag() {
    if (!drag) return;
    cv.classList.remove('gd');
    var wasMove = moved > 5;
    var n = drag.node;
    drag = null;
    if (!wasMove && n) window.location.href = n.href;
  }

  cv.addEventListener('wheel', function (e) {
    e.preventDefault();
    var f = e.deltaY < 0 ? 1.13 : 1 / 1.13;
    var nz = zoom * f;
    if (nz < 0.12 || nz > 7) return;
    zoom = nz;
    offX = e.clientX - (e.clientX - offX) * f;
    offY = e.clientY - (e.clientY - offY) * f;
  }, { passive: false });

  cv.addEventListener('dblclick', function (e) {
    var n = nodeAt(e.clientX, e.clientY);
    if (n) window.location.href = n.href;
  });
})();