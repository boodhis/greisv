/* Граф-навигация «Цифровой Крепости» — как Obsidian Graph View.
   На главной только основные разделы; клик по разделу выпускает
   «щупальца» — его подразделы (анимированно разворачиваются веером).
   Колесо мыши — зум, перетаскивание пустого — панорама, узлов — перенос,
   клик по разделу — щупальца, двойной клик — переход в раздел/страницу. */
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

  var nodes = [], links = [], byId = {}, sections = [];

  function node(id, label, href, g) {
    var o = {
      id: id, label: label, href: href, g: g, c: COL[g],
      x: 0, y: 0, vx: 0, vy: 0, r: 6, deg: 0,
      hidden: true, section: false, children: null,
      parent: null, appear: 1, appearing: false, tent: null
    };
    nodes.push(o);
    byId[id] = o;
    return o;
  }
  function topnode(id, label, href, g) { var o = node(id, label, href, g); o.hidden = false; return o; }
  function section(id, label, href, g) {
    var o = topnode(id, label, href, g);
    o.section = true; o.children = []; o.expanded = false;
    sections.push(o);
    return o;
  }
  function sub(id, label, href, g, parentId) {
    var o = node(id, label, href, g);
    o.parent = byId[parentId];
    o.appear = 0;
    o.parent.children.push(o);
    return o;
  }
  function link(a, b) { links.push([byId[a], byId[b]]); }
  function visible() { return nodes.filter(function (n) { return !n.hidden; }); }
  function active() { return nodes.filter(function (n) { return !n.hidden && !n.appearing; }); }

  /* ---- карта сайта ---- */
  topnode('home', 'Главная', 'index.html', 'home');
  topnode('manifest', 'Манифест', 'manifest.html', 'home');
  section('start', 'С чего начать', 'getting-started/index.html', 'start');
  sub('start-ubuntu', 'Установка Ubuntu', 'getting-started/install-ubuntu.html', 'start', 'start');
  sub('start-first', 'Первые шаги', 'getting-started/first-steps.html', 'start', 'start');
  sub('start-flash', 'Загрузочная флешка', 'getting-started/bootable-usb.html', 'start', 'start');
  section('study', 'Обучение', 'study/index.html', 'study');
  sub('study-words', 'Тренажёр', 'study/words.html', 'study', 'study');
  sub('study-cheat', 'Шпаргалки', 'study/cheatsheets.html', 'study', 'study');
  section('elec', 'Электрика', 'electric/index.html', 'elec');
  sub('elec-safe', 'Безопасность', 'electric/safety.html', 'elec', 'elec');
  sub('elec-panels', 'Щиты', 'electric/panels.html', 'elec', 'elec');
  sub('elec-wire', 'Кабели', 'electric/wiring.html', 'elec', 'elec');
  sub('elec-smart', 'Умный дом', 'electric/smart.html', 'elec', 'elec');
  section('lab', 'Homelab', 'homelab/index.html', 'homelab');
  sub('lab-hw', 'Железо', 'homelab/hardware.html', 'homelab', 'lab');
  sub('lab-net', 'Сеть', 'homelab/network.html', 'homelab', 'lab');
  sub('lab-ref', 'Сервер', 'homelab/server-reference.html', 'homelab', 'lab');
  sub('lab-lib', 'Библиотека', 'homelab/sopds-web.html', 'homelab', 'lab');
  section('srv', 'Сервисы', 'services/index.html', 'srv');
  sub('srv-docker', 'Docker', 'services/docker.html', 'srv', 'srv');
  sub('srv-samba', 'Samba', 'services/samba.html', 'srv', 'srv');
  sub('srv-dlna', 'MiniDLNA', 'services/minidlna.html', 'srv', 'srv');
  sub('srv-tr', 'Transmission', 'services/transmission.html', 'srv', 'srv');
  sub('srv-nav', 'Navidrome', 'services/navidrome.html', 'srv', 'srv');
  sub('srv-imm', 'Immich', 'services/immich.html', 'srv', 'srv');
  sub('srv-sopds', 'SOPDS', 'services/sopds.html', 'srv', 'srv');
  sub('srv-mqtt', 'MQTT', 'services/mqtt.html', 'srv', 'srv');
  section('guide', 'Гайды', 'guides/index.html', 'guide');
  sub('guide-disk', 'Диски', 'guides/disk-health.html', 'guide', 'guide');
  sub('guide-diag', 'Диагностика', 'guides/diagnostics.html', 'guide', 'guide');
  sub('guide-back', 'Бекапы', 'guides/backup.html', 'guide', 'guide');
  sub('guide-ssh', 'SSH', 'guides/ssh.html', 'guide', 'guide');
  sub('guide-term', 'Терминал', 'guides/terminal.html', 'guide', 'guide');
  sub('guide-wifi', 'Wi-Fi', 'guides/wifi-fix.html', 'guide', 'guide');
  sub('guide-auto', 'Автосборка', 'guides/auto-setup.html', 'guide', 'guide');
  sub('guide-jctl', 'journalctl', 'guides/journalctl.html', 'guide', 'guide');
  sub('guide-off', 'Авто-выкл', 'guides/auto-shutdown.html', 'guide', 'guide');
  section('res', 'Ресурсы', 'resources/index.html', 'res');
  sub('res-links', 'Ссылки', 'resources/links.html', 'res', 'res');
  sub('res-git', 'Git', 'resources/git-commands.html', 'res', 'res');
  sub('res-inxi', 'INXI', 'resources/inxi.html', 'res', 'res');
  sub('res-oc', 'OpenCode', 'resources/opencode-windows.html', 'res', 'res');
  section('hobby', 'Досуг', 'hobbies/index.html', 'hobby');
  sub('hobby-guitar', 'Гитара', 'hobbies/guitar.html', 'hobby', 'hobby');
  sub('hobby-esp', 'ESP32', 'hobbies/esp32.html', 'hobby', 'hobby');
  sub('sopds-web', 'Проект: Библиотека', 'homelab/sopds-web.html', 'homelab', 'lab');

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

  /* ---- щупальца ---- */
  function oEase(t) {
    if (t >= 1) return 1;
    var s = 1.70158;
    return 1 + (s + 1) * Math.pow(t - 1, 3) + s * Math.pow(t - 1, 2);
  }
  function tentacle(s, c, i, k) {
    var base = Math.atan2(s.y, s.x);
    var spread = k > 1 ? Math.min(0.55, 1.0 / (k - 1)) : 0;
    var ang = base + (i - (k - 1) / 2) * spread;
    var R = 86 + (i % 3) * 22 + Math.min(24, k * 3);
    return { a: ang, r: R };
  }
  function tip(c) {
    if (c.appearing && c.tent) {
      var p = c.parent, t = oEase(c.appear);
      var r = p.r + (c.tent.r - p.r) * t + 6;
      return { x: p.x + Math.cos(c.tent.a) * r, y: p.y + Math.sin(c.tent.a) * r, t: t };
    }
    return { x: c.x, y: c.y, t: 1 };
  }
  function toggle(s) {
    s.expanded = !s.expanded;
    var kids = s.children;
    for (var i = 0; i < kids.length; i++) {
      var c = kids[i];
      c.hidden = !s.expanded;
      c.appearing = s.expanded;
      c.appear = 0;
      if (s.expanded) c.tent = tentacle(s, c, i, kids.length);
    }
    computeScale();
  }

  /* ---- физика ---- */
  var damp = 0.82;
  var LIMX = 440, LIMY = 320;
  var REP = 190000, CAP = 26;
  var LINKLEN = 150;

  function computeScale() {
    var vc = Math.max(1, visible().length);
    LIMX = Math.max(120, W * 0.46);
    LIMY = Math.max(120, H * 0.44);
    var cell = Math.sqrt((LIMX * 2 * LIMY * 2) / vc);
    LINKLEN = cell * 1.05;
    var k = LINKLEN / 150;
    REP = 190000 * k;
    CAP = 26 * k;
  }

  function step(kick) {
    var i, a, b, dx, dy, d2, d, f, act = active();
    for (i = 0; i < act.length; i++) {
      for (var j = i + 1; j < act.length; j++) {
        a = act[i]; b = act[j];
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
      if (a.hidden || b.hidden || a.appearing || b.appearing) continue;
      dx = b.x - a.x; dy = b.y - a.y;
      d = Math.sqrt(dx * dx + dy * dy) || 1;
      f = (d - LINKLEN) * 0.02;
      dx /= d; dy /= d;
      a.vx += f * dx; a.vy += f * dy;
      b.vx -= f * dx; b.vy -= f * dy;
    }
    for (i = 0; i < act.length; i++) {
      a = act[i];
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
  function fit() { zoom = 1; offX = W / 2; offY = H / 2; }
  function toWorld(sx, sy) { return { x: (sx - offX) / zoom, y: (sy - offY) / zoom }; }

  function nodeAt(sx, sy) {
    for (var i = 0; i < nodes.length; i++) {
      var n = nodes[i];
      if (n.hidden) continue;
      var s = tip(n);
      var thr = Math.max(9, n.r * zoom + 5 + n.deg * 0.4);
      if (Math.hypot(sx - s.x * zoom - offX, sy - s.y * zoom - offY) <= thr) return n;
    }
    return null;
  }

  function draw() {
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, W, H);
    ctx.save();
    ctx.translate(offX, offY);
    ctx.scale(zoom, zoom);

    /* связи */
    ctx.lineWidth = 1.4 / zoom;
    for (var i = 0; i < links.length; i++) {
      var a = links[i][0], b = links[i][1];
      if (a.hidden || b.hidden) continue;
      var pa = a.appearing ? tip(a) : a;
      var pb = b.appearing ? tip(b) : b;
      var t = Math.min(pa.t || 1, pb.t || 1);
      var inc = hover && (a === hover || b === hover);
      ctx.strokeStyle = inc
        ? 'rgba(53,230,224,0.6)'
        : 'rgba(123,168,124,' + ((hover ? 0.05 : 0.11) * t) + ')';
      ctx.beginPath();
      ctx.moveTo(pa.x, pa.y);
      ctx.lineTo(pb.x, pb.y);
      ctx.stroke();
    }

    /* узлы */
    ctx.textAlign = 'left';
    ctx.textBaseline = 'middle';
    for (var n = 0; n < nodes.length; n++) {
      var o = nodes[n];
      if (o.hidden) continue;
      var t = o.appearing ? o.appear : 1;
      var pos = o.appearing ? tip(o) : o;
      var rs = (o.r * (o.deg >= 8 ? 1.55 : o.deg >= 4 ? 1.25 : 1)) * (0.5 + 0.5 * t);
      var dim = hover && o !== hover;
      ctx.globalAlpha = (dim ? 0.3 : 1) * Math.min(1, t * 1.4);
      ctx.fillStyle = o.c;
      if (o === hover) {
        ctx.shadowColor = o.c;
        ctx.shadowBlur = 14;
        ctx.fillStyle = '#ffffff';
      }
      ctx.beginPath();
      ctx.arc(pos.x, pos.y, rs, 0, Math.PI * 2);
      ctx.fill();
      ctx.shadowBlur = 0;
      ctx.globalAlpha = 1;

      var fs = Math.max(8, 11.5 / zoom);
      ctx.font = '600 ' + fs + 'px ui-monospace,Consolas,monospace';
      ctx.fillStyle = o === hover ? '#fff' : 'rgba(123,168,124,.9)';
      ctx.globalAlpha = Math.min(1, t * 1.6);
      ctx.fillText(o.label, pos.x + rs + 7 / zoom, pos.y);
      ctx.globalAlpha = 1;
    }
    ctx.restore();
  }

  /* ---- цикл ---- */
  var raf = null, settling = 420;
  function frame(ts) {
    var i;
    for (i = 0; i < nodes.length; i++) {
      var c = nodes[i];
      if (c.appearing && c.appear < 1) {
        c.appear = Math.min(1, c.appear + 0.045);
        if (c.appear >= 1) {
          c.appearing = false;
          var t = tip(c);
          c.x = t.x; c.y = t.y;
        }
      }
    }
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
  var ring = visible();
  for (var i = 0; i < ring.length; i++) {
    if (ring[i].id === 'home') { ring[i].x = 0; ring[i].y = 0; continue; }
    var a = (i - 1) / Math.max(1, ring.length - 1) * Math.PI * 2;
    ring[i].x = Math.cos(a) * 150;
    ring[i].y = Math.sin(a) * 150;
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
      var o = drag.node;
      if (o.appearing) { o.appear = 1; o.appearing = false; var t = tip(o); o.x = t.x; o.y = t.y; }
      o.x += p.x - drag.px;
      o.y += p.y - drag.py;
      o.vx = 0; o.vy = 0;
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
    if (wasMove || !n) return;
    if (n.section) toggle(n);
    else window.location.href = n.href;
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