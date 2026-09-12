/* Виджет «Слово дня» для футера. Самодостаточный, без зависимостей.
   Слово выбирается СЛУЧАЙНО при каждой загрузке страницы; клик раскрывает перевод. */
(function () {
  function ready(fn) {
    if (document.readyState !== 'loading') { fn(); } else { document.addEventListener('DOMContentLoaded', fn); }
  }
  ready(function () {
    var el = document.getElementById('wordday');
    if (!el || !window.SRS_DAY || !window.SRS_DAY.length) return;
    var c = window.SRS_DAY[Math.floor(Math.random() * window.SRS_DAY.length)];
    var q = el.querySelector('.wd-w'), ph = el.querySelector('.wd-ph'), t2 = el.querySelector('.wd-t2');
    q.textContent = c[0];
    ph.textContent = c[1] ? '[' + c[1] + ']' : '';
    el.addEventListener('click', function () {
      t2.textContent = c[2];
      el.classList.add('revealed');
    });
  });
})();