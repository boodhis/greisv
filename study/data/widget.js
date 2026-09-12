/* Виджет «Слово дня» для футера. Самодостаточный, без зависимостей.
   Слово подбирается по дню года; клик раскрывает перевод. */
(function () {
  function ready(fn) {
    if (document.readyState !== 'loading') { fn(); } else { document.addEventListener('DOMContentLoaded', fn); }
  }
  ready(function () {
    var el = document.getElementById('wordday');
    if (!el || !window.SRS_DAY) return;
    var d = new Date();
    var start = new Date(d.getFullYear(), 0, 0);
    var doy = Math.floor((d - start) / 86400000);
    var c = window.SRS_DAY[doy % window.SRS_DAY.length];
    var KEY = 'wordday_seen_' + d.getFullYear() + '_' + doy;
    var q = el.querySelector('.wd-w'), ph = el.querySelector('.wd-ph'), t2 = el.querySelector('.wd-t2');
    q.textContent = c[0];
    ph.textContent = c[1] ? '[' + c[1] + ']' : '';
    el.addEventListener('click', function () {
      t2.textContent = c[2];
      el.classList.add('revealed');
      try { localStorage.setItem(KEY, '1'); } catch (e) {}
    });
  });
})();