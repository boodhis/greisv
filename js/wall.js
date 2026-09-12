/* Стена Крепости — подложка на весь экран, на которой можно оставлять надписи.
   Штрихи хранятся послойно (fortress_bgwall_v2) — «↩ убрать надпись» снимает
   их по одной, как они и создаются. Кнопка «✏️ Стена» — правый нижний угол. */
(function () {
  function init() {
    var c = document.getElementById('bgwall');
    if (!c) return;
    var ctx = c.getContext('2d');
    var KEY = 'fortress_bgwall_v2';
    var COLORS = ['#4fc3f7', '#3fb950', '#e3b341', '#ff7ab6', '#e6edf3'];
    var MAX_STROKES = 80;
    var color = COLORS[0];
    var alpha = 0.55;
    var width = 2.6;
    var drawing = false, active = false, last = null, cur = null;
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

    c.addEventListener('pointerdown', function (e) {
      if (!active) return;
      e.preventDefault();
      drawing = true; last = pt(e);
      cur = { c: color, w: width, a: alpha, pts: [last.slice()] };
      try { c.setPointerCapture(e.pointerId); } catch (err) {}
    });
    c.addEventListener('pointermove', function (e) {
      if (!drawing || last == null || !cur) return;
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
    var undo = document.getElementById('wall-undo');
    function setActive(on) {
      active = on;
      document.body.classList.toggle('drawing', on);
      if (btn) {
        btn.classList.toggle('on', on);
        btn.textContent = on ? '✅ Готово' : '✏️ Стена';
      }
      if (bar) bar.hidden = !on;
      if (hint) hint.hidden = !on;
    }
    if (btn) btn.addEventListener('click', function () { setActive(!active); });
    if (undo) undo.addEventListener('click', function () {
      if (!strokes.length) return;
      strokes.pop();
      save();
      paint();
    });
    window.addEventListener('keydown', function (e) { if (e.key === 'Escape' && active) setActive(false); });

    var dots = bar ? bar.querySelectorAll('.wc') : [];
    Array.prototype.forEach.call(dots, function (b) {
      b.addEventListener('click', function () {
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