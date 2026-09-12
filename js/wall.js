/* Стена Крепости — подложка на весь экран, на которой можно оставлять надписи.
   Сохраняется в localStorage (fortress_bgwall_v1). Кнопка «✏️ Стена» — правый нижний угол. */
(function () {
  function init() {
    var c = document.getElementById('bgwall');
    if (!c) return;
    var ctx = c.getContext('2d');
    var KEY = 'fortress_bgwall_v1';
    var COLORS = ['#4fc3f7', '#3fb950', '#e3b341', '#ff7ab6', '#e6edf3'];
    var color = COLORS[0];
    var drawing = false, active = false, last = null;

    function dpr() { return window.devicePixelRatio || 1; }
    function size() { c.width = window.innerWidth * dpr(); c.height = window.innerHeight * dpr(); }
    function reflow() {
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.scale(dpr(), dpr());
      ctx.lineCap = 'round'; ctx.lineJoin = 'round'; ctx.globalAlpha = 0.55;
      paint();
    }
    function save() { try { localStorage.setItem(KEY, c.toDataURL()); } catch (e) {} }
    function paint() {
      try {
        var d = localStorage.getItem(KEY);
        if (d) {
          var im = new Image();
          im.onload = function () { ctx.drawImage(im, 0, 0); };
          im.src = d;
        }
      } catch (e) {}
    }
    function clearAll() { ctx.clearRect(0, 0, c.width, c.height); try { localStorage.removeItem(KEY); } catch (e) {} }

    function pt(e) { return [e.clientX, e.clientY]; }
    function strokeTo(x, y) {
      ctx.strokeStyle = color;
      ctx.lineWidth = 2.6;
      ctx.beginPath();
      ctx.moveTo(last[0], last[1]);
      ctx.lineTo(x, y);
      ctx.stroke();
      last = [x, y];
    }

    c.addEventListener('pointerdown', function (e) {
      if (!active) return;
      e.preventDefault();
      drawing = true; last = pt(e);
      try { c.setPointerCapture(e.pointerId); } catch (err) {}
    });
    c.addEventListener('pointermove', function (e) {
      if (!drawing || last == null) return;
      e.preventDefault();
      var p = pt(e); strokeTo(p[0], p[1]);
    });
    ['pointerup', 'pointercancel'].forEach(function (ev) {
      c.addEventListener(ev, function () { if (!drawing) return; drawing = false; last = null; save(); });
    });

    var btn = document.getElementById('wall-btn');
    var bar = document.getElementById('wall-bar');
    var hint = document.getElementById('wall-hint');
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
    window.addEventListener('keydown', function (e) { if (e.key === 'Escape' && active) setActive(false); });

    var dots = bar ? bar.querySelectorAll('.wc') : [];
    Array.prototype.forEach.call(dots, function (b) {
      b.addEventListener('click', function () {
        color = b.getAttribute('data-c');
        Array.prototype.forEach.call(dots, function (x) { x.classList.remove('on'); });
        b.classList.add('on');
      });
    });
    if (bar) bar.querySelector('.wclear').addEventListener('click', function () { clearAll(); });

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