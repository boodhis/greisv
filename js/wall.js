/* Стена Крепости — подложка на весь экран для надписей.
   Подложка НЕЗАВИСИМА для каждой страницы: ключ хранилища включает путь страницы.
   «⌫ Удалить надпись» включает режим удаления — появляется курсор, клик по
   надписи убирает именно её (выборочно). Общие классы .drawing/.deleting
   задаются в статическом CSS страницы; режимные мелочи инжектятся здесь. */
(function () {
  function init() {
    var c = document.getElementById('bgwall');
    if (!c) return;

    var st = document.createElement('style');
    st.textContent = 'body.deleting #bgwall{cursor:grabbing}#wall-bar.deleting .wdots{opacity:.3;pointer-events:none}body.deleting .wc.on{border-color:transparent;box-shadow:none}body.deleting #wall-bar .wclear.on{color:#4fc3f7}';
    document.head.appendChild(st);

    var ctx = c.getContext('2d');
    var KEY = 'fortress_bgwall_v3_' + encodeURIComponent(location.pathname);
    var COLORS = ['#4fc3f7', '#3fb950', '#e3b341', '#ff7ab6', '#e6edf3'];
    var MAX_STROKES = 80;
    var HIT = 26;
    var color = COLORS[0];
    var alpha = 0.55;
    var width = 2.6;
    var drawing = false, active = false, deleting = false, last = null, cur = null;
    var strokes = loadStrokes();

    function dpr() { return window.devicePixelRatio || 1; }
    function size() { c.width = window.innerWidth * dpr(); c.height = window.innerHeight * dpr(); }

    function loadStrokes() {
      try {
        var d = JSON.parse(localStorage.getItem(KEY));
        if (Array.isArray(d)) return d;
      } catch (e) {}
      return [];
    }
    function save() { try { localStorage.setItem(KEY, JSON.stringify(strokes)); } catch (e) {} }

    function drawStroke(s) {
      if (!s || !s.pts || !s.pts.length) return;
      ctx.strokeStyle = s.c;
      ctx.lineWidth = s.w;
      ctx.globalAlpha = s.a;
      ctx.beginPath();
      ctx.moveTo(s.pts[0][0], s.pts[0][1]);
      for (var i = 1; i < s.pts.length; i++) ctx.lineTo(s.pts[i][0], s.pts[i][1]);
      ctx.stroke();
    }
    function paint() {
      ctx.clearRect(0, 0, c.width, c.height);
      for (var i = 0; i < strokes.length; i++) drawStroke(strokes[i]);
    }
    function reflow() {
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.scale(dpr(), dpr());
      ctx.lineCap = 'round'; ctx.lineJoin = 'round';
      paint();
    }

    function pt(e) { return [e.clientX, e.clientY]; }
    function segDist2(px, py, ax, ay, bx, by) {
      var dx = bx - ax, dy = by - ay;
      if (dx === 0 && dy === 0) {
        var q1 = px - ax, q2 = py - ay;
        return q1 * q1 + q2 * q2;
      }
      var t = ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy);
      t = Math.max(0, Math.min(1, t));
      var ex = ax + t * dx - px, ey = ay + t * dy - py;
      return ex * ex + ey * ey;
    }
    function nearest(p) {
      var best = -1, bd = HIT * HIT, x = p[0], y = p[1];
      for (var i = 0; i < strokes.length; i++) {
        var pts = strokes[i].pts;
        for (var j = 1; j < pts.length; j++) {
          var d = segDist2(x, y, pts[j - 1][0], pts[j - 1][1], pts[j][0], pts[j][1]);
          if (d < bd) { bd = d; best = i; }
        }
      }
      return best;
    }

    c.addEventListener('pointerdown', function (e) {
      if (!active) return;
      e.preventDefault();
      if (deleting) {
        var idx = nearest(pt(e));
        if (idx >= 0) { strokes.splice(idx, 1); save(); paint(); }
        return;
      }
      drawing = true; last = pt(e);
      cur = { c: color, w: width, a: alpha, pts: [last.slice()] };
      try { c.setPointerCapture(e.pointerId); } catch (err) {}
    });
    c.addEventListener('pointermove', function (e) {
      if (!drawing || deleting || last == null || !cur) return;
      e.preventDefault();
      var p = pt(e);
      ctx.strokeStyle = color; ctx.lineWidth = width; ctx.globalAlpha = alpha;
      ctx.beginPath(); ctx.moveTo(last[0], last[1]); ctx.lineTo(p[0], p[1]); ctx.stroke();
      last = p;
      cur.pts.push(p.slice());
    });
    ['pointerup', 'pointercancel'].forEach(function (ev) {
      c.addEventListener(ev, function () {
        if (!drawing) return;
        drawing = false; last = null;
        if (cur && cur.pts.length > 1) {
          strokes.push(cur);
          if (strokes.length > MAX_STROKES) strokes.splice(0, strokes.length - MAX_STROKES);
          save();
        }
        cur = null;
      });
    });

    var btn = document.getElementById('wall-btn');
    var bar = document.getElementById('wall-bar');
    var hint = document.getElementById('wall-hint');
    var del = document.getElementById('wall-undo');

    function setHint(t) { if (hint) hint.textContent = t; }
    function setActive(on) {
      active = on;
      document.body.classList.toggle('drawing', on);
      if (!on) exitDelete();
      if (btn) {
        btn.classList.toggle('on', on);
        btn.textContent = on ? '✅ Готово' : '✏️ Стена';
      }
      if (bar) bar.hidden = !on;
      if (hint) hint.hidden = !on;
      if (on && !deleting) setHint('Рисуй прямо на подложке. Готово — кнопка справа внизу, выход — Esc');
    }
    function exitDelete() {
      if (!deleting) return;
      deleting = false;
      document.body.classList.remove('deleting');
      if (bar) bar.classList.remove('deleting');
      if (del) { del.classList.remove('on'); del.textContent = '⌫ Удалить надпись'; }
      if (active && hint) setHint('Рисуй прямо на подложке. Готово — кнопка справа внизу, выход — Esc');
    }
    function enterDelete() {
      if (!active) setActive(true);
      if (deleting) return;
      deleting = true;
      document.body.classList.add('deleting');
      if (bar) bar.classList.add('deleting');
      if (del) { del.classList.add('on'); del.textContent = '✅ Готово'; }
      if (hint) { hint.hidden = false; setHint('Кликни по надписи, которую нужно убрать · выход — Esc'); }
    }
    if (btn) btn.addEventListener('click', function () { setActive(!active); });
    if (del) del.addEventListener('click', function () { deleting ? exitDelete() : enterDelete(); });
    window.addEventListener('keydown', function (e) {
      if (e.key !== 'Escape') return;
      if (deleting) exitDelete();
      else if (active) setActive(false);
    });

    var dots = bar ? bar.querySelectorAll('.wc') : [];
    Array.prototype.forEach.call(dots, function (b) {
      b.addEventListener('click', function () {
        if (deleting) return;
        color = b.getAttribute('data-c');
        Array.prototype.forEach.call(dots, function (x) { x.classList.remove('on'); });
        b.classList.add('on');
      });
    });

    size();
    window.addEventListener('resize', function () { size(); reflow(); });
    reflow();
    setActive(false);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();